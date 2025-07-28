#!/usr/bin/env python3
"""
Bongo Cat Typing Monitor - Enhanced v2.2
Based on industry-standard WPM calculation and best practices from research.
Now with automatic computer time sync and optimized algorithms.
"""

import time
import serial
import serial.tools.list_ports
import threading
from collections import deque
from pynput import keyboard
import sys
import platform
import psutil
import datetime

class BongoCatController:
    def __init__(self, port='AUTO', baudrate=115200):
        """Initialize the Bongo Cat controller with industry-standard WPM calculation"""
        self.port = port
        self.baudrate = baudrate
        self.serial_conn = None
        self.running = False
        
        # Enhanced animation control with reduced command frequency
        self.last_sent_speed = -1
        self.last_sent_state = ""
        self.last_command_time = 0
        self.min_command_interval = 0.5   # Minimum 500ms between commands (2 FPS max) - prevent Arduino overload
        
        # Proper keystroke detection and timing
        self.keystroke_buffer = deque(maxlen=50)  # Store recent keystrokes
        self.last_keystroke_time = 0
        self.typing_active = False
        self.idle_start_time = 0
        self.idle_timeout = 3.0  # 3 seconds before going idle
        
        # Improved WPM calculation with stability optimizations
        self.typing_sessions = deque(maxlen=10)  # Reduced from 20 for faster response
        self.wpm_history = deque(maxlen=5)       # Reduced history for responsiveness
        self.current_wpm = 0
        self.max_wpm = 100               # Reasonable ceiling for most users
        
        # Enhanced state management with better hysteresis
        self.current_state = "IDLE"
        self.state_change_time = time.time()
        self.state_stability_time = 0.5  # Reduced from longer delays for responsiveness
        
        # Enhanced timing settings based on research
        self.idle_timeout = 1.0          # Industry standard: 1 second for responsiveness
        self.update_interval = 0.08      # ~12 FPS for smooth animation
        self.stats_update_interval = 1.0 # System stats every second
        self.heartbeat_interval = 2.0    # Keep connection alive
        self.last_stats_update = 0
        self.last_heartbeat = 0
        
        # Industry-standard WPM calculation (5 characters = 1 word)
        self.chars_per_word = 5.0        # Standard definition
        self.min_wpm = 0
        self.min_animation_speed = 500   # Slower minimum for better granularity
        self.max_animation_speed = 40    # Optimal maximum for visual feedback
        
        # Refined WPM thresholds based on 2024 typing speed research
        # Research shows: Average 40-45 WPM, Slow <20, Good 50-60, Professional 70+
        self.slow_threshold = 20         # Below average (matches research: <20 WPM is slow)
        self.normal_threshold = 40       # Average range (matches research: 40-45 WPM average)
        self.fast_threshold = 65         # Good/Professional range (matches research: 60+ WPM is good)
        self.streak_threshold = 85       # Excellent range (matches research: 80+ WPM is excellent)
        
        self.last_sent_speed = -1
        self.current_state = "IDLE"
        self.last_state = "IDLE"
        self.last_streak_state = False  # Initialize streak state tracking
        
        # System monitoring
        self.cpu_percent = 0
        self.ram_percent = 0
        
        # Idle management
        self.idle_start_time = 0
        self.idle_progression_started = False
        
        # Advanced WPM smoothing for stability
        self.wpm_history = deque(maxlen=3)  # Smaller window for faster response
        self.raw_wpm_history = deque(maxlen=10)  # Track raw WPM for analysis
        
        # Thread synchronization
        self._data_lock = threading.Lock()  # Protect shared data structures
        
    def find_esp32_port(self):
        """Auto-detect ESP32 COM port"""
        print("🔍 Scanning for ESP32...")
        
        ports = serial.tools.list_ports.comports()
        esp32_ports = []
        
        for port in ports:
            # Common ESP32 identifiers
            esp32_keywords = [
                'CP210',  # Silicon Labs CP2102/CP2104
                'CH340',  # CH340 USB-to-serial chip
                'CH341',  # CH341 USB-to-serial chip  
                'FT232',  # FTDI chip
                'ESP32',  # Direct ESP32 reference
                'Silicon Labs',
                'QinHeng Electronics'
            ]
            
            description = str(port.description).upper()
            manufacturer = str(port.manufacturer).upper() if port.manufacturer else ""
            
            for keyword in esp32_keywords:
                if keyword.upper() in description or keyword.upper() in manufacturer:
                    esp32_ports.append(port)
                    print(f"🎯 Found potential ESP32: {port.device} - {port.description}")
                    break
        
        if not esp32_ports:
            print("❌ No ESP32 found automatically")
            print("📋 Available ports:")
            for port in ports:
                print(f"   {port.device} - {port.description}")
            return None
        
        if len(esp32_ports) == 1:
            selected_port = esp32_ports[0].device
            print(f"✅ Auto-selected: {selected_port}")
            return selected_port
        else:
            print("🤔 Multiple ESP32 devices found:")
            for i, port in enumerate(esp32_ports):
                print(f"   {i+1}: {port.device} - {port.description}")
            
            try:
                choice = input("Enter number (or press Enter for first): ").strip()
                if not choice:
                    selected_port = esp32_ports[0].device
                else:
                    index = int(choice) - 1
                    selected_port = esp32_ports[index].device
                
                print(f"✅ Selected: {selected_port}")
                return selected_port
            except (ValueError, IndexError):
                print("❌ Invalid selection, using first device")
                return esp32_ports[0].device

    def connect_serial(self, retries=3):
        """Connect to ESP32 via serial with retry logic"""
        if self.port == 'AUTO' or not self.port:
            detected_port = self.find_esp32_port()
            if detected_port:
                self.port = detected_port
            else:
                print("❌ Could not auto-detect ESP32. Please specify port manually.")
                return False
        
        for attempt in range(retries):
            try:
                if attempt > 0:
                    print(f"🔄 Retry attempt {attempt + 1}/{retries}...")
                    time.sleep(2)
                
                print(f"🔌 Connecting to {self.port}...")
                self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=0, writeTimeout=0)
                time.sleep(2)  # Wait for ESP32 to restart
                
                # Test connection
                self.send_command("PING")
                time.sleep(0.1)
                
                if self.serial_conn.in_waiting > 0:
                    response = self.serial_conn.readline().decode().strip()
                    if "PONG" in response:
                        print(f"✅ Connected to Bongo Cat on {self.port}")
                        print(f"🐱 ESP32 Response: {response}")
                        # Send initial time sync
                        self.send_initial_sync()
                        return True
                
                print(f"✅ Connected to {self.port}")
                # Send initial time sync
                self.send_initial_sync()
                return True
                
            except Exception as e:
                print(f"❌ Connection failed: {e}")
                if attempt < retries - 1:
                    continue
                return False
        
        return False
    
    def send_initial_sync(self):
        """Send initial time and system stats when connection is established"""
        try:
            # Send current time immediately
            current_time_str = datetime.datetime.now().strftime("%H:%M")
            time_command = f"TIME:{current_time_str}"
            self.send_command(time_command)
            print(f"🕐 Initial time sync: {current_time_str}")
            
            # Send initial system stats
            cpu, ram = self.get_system_stats()
            stats_command = f"STATS:CPU:{cpu},RAM:{ram},WPM:0"
            self.send_command(stats_command)
            print(f"📊 Initial stats: CPU {cpu}%, RAM {ram}%")
            
            # Initialize timing variables
            self.last_stats_sent = time.time()
            self.last_time_sent = time.time()
            
        except Exception as e:
            print(f"⚠️ Initial sync error: {e}")
    
    def disconnect_serial(self):
        """Disconnect from ESP32"""
        if self.serial_conn and self.serial_conn.is_open:
            self.send_command("STOP")  # Use explicit stop command
            time.sleep(0.1)
            self.serial_conn.close()
            print("📱 Disconnected from Bongo Cat")
    
    def send_command(self, command):
        """Send command to ESP32 with non-blocking error handling"""
        if self.serial_conn and self.serial_conn.is_open:
            try:
                message = f"{command}\n"
                self.serial_conn.write(message.encode())
                # Remove flush() to prevent blocking
            except serial.SerialTimeoutException:
                print(f"⚠️ Serial timeout: {command}")
            except Exception as e:
                print(f"❌ Serial error: {e}")
    
    def get_system_stats(self):
        """Get current CPU and RAM usage"""
        try:
            cpu_usage = psutil.cpu_percent(interval=None)
            memory = psutil.virtual_memory()
            ram_usage = memory.percent
            
            self.cpu_percent = int(cpu_usage)
            self.ram_percent = int(ram_usage)
            
            return self.cpu_percent, self.ram_percent
        except Exception as e:
            print(f"⚠️ System monitoring error: {e}")
            return 0, 0
    
    def send_system_stats(self):
        """Send system stats and current computer time to ESP32"""
        cpu, ram = self.get_system_stats()
        wpm = int(self.current_wpm)
        
        # Send system stats
        stats_command = f"STATS:CPU:{cpu},RAM:{ram},WPM:{wpm}"
        self.send_command(stats_command)
        
        # Send current computer time (automatically synced)
        current_time = datetime.datetime.now().strftime("%H:%M")
        time_command = f"TIME:{current_time}"
        self.send_command(time_command)
    
    def update_system_stats(self):
        """Update system stats with rate limiting to prevent overwhelming ESP32"""
        current_time = time.time()
        
        # Rate limit to prevent overwhelming the serial connection
        # Send stats every 2 seconds, time updates every 30 seconds or on first call
        if not hasattr(self, 'last_stats_sent'):
            self.last_stats_sent = 0
            self.last_time_sent = 0
        
        # Always update local stats for WPM calculation
        self.get_system_stats()
        
        # Send system stats every 2 seconds
        if current_time - self.last_stats_sent >= 2.0:
            try:
                cpu, ram = self.get_system_stats()
                wpm = int(self.current_wpm)
                stats_command = f"STATS:CPU:{cpu},RAM:{ram},WPM:{wpm}"
                self.send_command(stats_command)
                self.last_stats_sent = current_time
            except Exception as e:
                print(f"⚠️ Stats update error: {e}")
        
        # Send time updates every 30 seconds or on first call
        if current_time - self.last_time_sent >= 30.0 or self.last_time_sent == 0:
            try:
                current_time_str = datetime.datetime.now().strftime("%H:%M")
                time_command = f"TIME:{current_time_str}"
                self.send_command(time_command)
                self.last_time_sent = current_time
                print(f"🕐 Time synced: {current_time_str}")
            except Exception as e:
                print(f"⚠️ Time sync error: {e}")
    
    def calculate_wpm_industry_standard(self):
        """Optimized WPM calculation - simplified for performance during rapid typing"""
        now = time.time()
        
        # Cache WPM calculation to reduce CPU load during rapid typing
        if hasattr(self, '_last_wpm_calc_time') and (now - self._last_wpm_calc_time) < 0.25:
            return getattr(self, '_cached_wpm', 0)  # Return cached value if calculated recently
        
        # Thread-safe access to keystroke buffer - simplified approach
        with self._data_lock:
            if len(self.keystroke_buffer) < 2:
                self._cached_wpm = 0
                self._last_wpm_calc_time = now
                return 0
            
            # Only use recent keystrokes to avoid expensive deque operations
            recent_keystrokes = list(self.keystroke_buffer)[-8:]  # Last 8 keystrokes only
            
            if len(recent_keystrokes) < 2:
                self._cached_wpm = 0
                self._last_wpm_calc_time = now
                return 0
            
            time_span = now - recent_keystrokes[0]
            keystroke_count = len(recent_keystrokes)
        
        if time_span > 0.4:  # Minimum time span
            # Simplified WPM calculation without expensive smoothing
            raw_wpm = (keystroke_count / self.chars_per_word) * (60 / time_span)
            
            # Very simple smoothing: just average with previous value
            if hasattr(self, '_cached_wpm') and self._cached_wpm > 0:
                smoothed_wpm = (self._cached_wpm * 0.6) + (raw_wpm * 0.4)  # Simple blend
            else:
                smoothed_wpm = raw_wpm
            
            # Cache the result
            self._cached_wpm = min(smoothed_wpm, self.max_wpm)
            self._last_wpm_calc_time = now
            return self._cached_wpm
        
        # Cache zero result
        self._cached_wpm = 0
        self._last_wpm_calc_time = now
        return 0
    
    def wpm_to_animation_speed(self, wpm):
        """Convert WPM to animation speed with research-based optimization"""
        if wpm <= 0:
            return self.min_animation_speed
        
        # Research-based mapping: more responsive at lower speeds, smooth at higher speeds
        import math
        normalized = min(wpm / self.max_wpm, 1.0)
        
        # Use a curve that feels natural based on typing research
        # Faster response for lower speeds, smoother for higher speeds
        if normalized < 0.3:  # For slow typing (0-30 WPM range)
            curved = normalized * 1.5  # More responsive
        else:  # For faster typing (30+ WPM range)
            curved = 0.45 + (normalized - 0.3) * 0.8  # Smoother progression
        
        curved = min(curved, 1.0)  # Ensure we don't exceed 1.0
        
        speed = self.min_animation_speed - (curved * (self.min_animation_speed - self.max_animation_speed))
        return int(max(speed, self.max_animation_speed))
    
    def determine_animation_state(self, wpm):
        """Determine animation state with improved hysteresis"""
        # Enhanced hysteresis to prevent rapid state changes
        hysteresis = 2  # Reduced for more responsiveness while maintaining stability
        
        if self.current_state == "IDLE":
            if wpm >= 3:  # Very low threshold to start typing animation
                if wpm < self.slow_threshold:
                    return "SLOW"
                elif wpm < self.normal_threshold:
                    return "NORMAL"
                else:
                    return "FAST"
        elif self.current_state == "SLOW":
            if wpm < 2:
                return "IDLE"
            elif wpm >= self.slow_threshold + hysteresis:
                if wpm < self.normal_threshold:
                    return "NORMAL"
                else:
                    return "FAST"
        elif self.current_state == "NORMAL":
            if wpm < self.slow_threshold - hysteresis:
                return "SLOW" if wpm >= 2 else "IDLE"
            elif wpm >= self.normal_threshold + hysteresis:
                return "FAST"
        elif self.current_state == "FAST":
            if wpm < self.normal_threshold - hysteresis:
                if wpm >= self.slow_threshold:
                    return "NORMAL"
                else:
                    return "SLOW" if wpm >= 2 else "IDLE"
        
        return self.current_state  # No change if within hysteresis range
    
    def is_streak_active(self, wpm):
        """Determine if streak mode should be active based on WPM"""
        return wpm >= self.fast_threshold  # 65+ WPM triggers streak mode
    
    def handle_idle_progression(self, now):
        """Handle controlled idle progression"""
        if not self.typing_active:
            if not self.idle_progression_started:
                # Start idle progression after a brief delay
                if now - self.idle_start_time > 1.5:  # Slightly reduced delay
                    self.send_command("IDLE_START")
                    self.idle_progression_started = True
                    print("😴 Starting idle progression...")
        else:
            # Reset idle when typing resumes
            self.idle_start_time = 0
            self.idle_progression_started = False
    
    def on_key_press(self, key):
        """Lightweight keystroke detection - minimal processing to prevent blocking"""
        try:
            current_time = time.time()
            
            # Thread-safe keystroke recording
            with self._data_lock:
                self.keystroke_buffer.append(current_time)
                self.last_keystroke_time = current_time
                
                # Mark as actively typing
                if not self.typing_active:
                    self.typing_active = True
                    print("⌨️ Typing started")
            
            # NO heavy operations here - everything moved to background thread
                
        except Exception as e:
            print(f"❌ Keystroke detection error: {e}")
            # Continue processing even if there's an error
    
    def send_animation_command(self, wpm, force_update=False):
        """Send animation command with improved rate limiting and separate streak handling"""
        current_time = time.time()
        
        # Rate limiting to prevent overwhelming Arduino
        if not force_update and (current_time - self.last_command_time) < self.min_command_interval:
            return  # Skip this update to maintain stable communication
        
        # Determine animation state and speed
        new_state = self.determine_animation_state(wpm)
        animation_speed = self.wpm_to_animation_speed(wpm)
        is_streak = self.is_streak_active(wpm)
        
        # Track streak state changes
        if not hasattr(self, 'last_streak_state'):
            self.last_streak_state = False
        
        # Enhanced change detection with forced periodic updates
        speed_changed = abs(animation_speed - self.last_sent_speed) > 25  # Filter micro-adjustments: 25ms threshold
        state_changed = new_state != self.last_sent_state
        streak_changed = is_streak != self.last_streak_state
        
        # CRITICAL FIX: Force periodic updates to prevent Arduino animation freezing
        time_since_last_command = current_time - self.last_command_time
        force_periodic_update = time_since_last_command > 4.0  # Force update every 4 seconds - reduce Arduino load
        
        if state_changed or speed_changed or streak_changed or force_update or force_periodic_update:
            # Update state tracking regardless of serial connection
            self.last_sent_speed = animation_speed
            self.last_sent_state = new_state
            self.last_command_time = current_time
            
            # Handle streak state tracking
            if streak_changed:
                self.last_streak_state = is_streak
            
            # Update current state and print changes
            # Debug output for different types of updates
            if force_periodic_update and not (state_changed or speed_changed or streak_changed or force_update):
                print(f"🔄 Keep-alive: {new_state} | WPM: {self.current_wpm:.1f} | Speed: {animation_speed}ms | Gap: {time_since_last_command:.1f}s")
            elif state_changed or streak_changed or force_update:
                if self.current_state != new_state or streak_changed:
                    # Emoji based on state and streak
                    base_emoji = {"SLOW": "🐌", "NORMAL": "👐", "FAST": "⚡"}.get(new_state, "")
                    emoji = f"{base_emoji}😊" if is_streak else base_emoji
                    streak_text = " (HAPPY)" if is_streak else ""
                    print(f"🐱 {self.current_state} → {new_state}{streak_text} | WPM: {self.current_wpm:.1f} | Speed: {animation_speed}ms {emoji} | T: {current_time:.1f}")
                    self.current_state = new_state
                    self.state_change_time = current_time
            
            # Send commands to Arduino if connected
            if self.serial_conn and self.serial_conn.is_open:
                try:
                    # Combine commands to reduce serial writes and prevent buffer overflow
                    commands_to_send = []
                    
                    if wpm <= 0:
                        commands_to_send.append("STOP")
                        # Turn off streak when stopping
                        if self.last_streak_state:
                            commands_to_send.append("STREAK_OFF")
                            self.last_streak_state = False
                    else:
                        commands_to_send.append(f"SPEED:{animation_speed}")
                        # Handle streak mode separately
                        if streak_changed:
                            if is_streak:
                                commands_to_send.append("STREAK_ON")
                            else:
                                commands_to_send.append("STREAK_OFF")
                    
                    # Send all commands in one write operation to prevent buffer overflow
                    if commands_to_send:
                        combined_command = '\n'.join(commands_to_send) + '\n'
                        self.serial_conn.write(combined_command.encode())
                        
                except serial.SerialTimeoutException:
                    # Non-blocking write timed out - Arduino buffer full, skip this update
                    print("⚠️ Serial buffer full - skipping command")
                except Exception as e:
                    print(f"❌ Command send error: {e}")
    
    def update_animation(self):
        """Enhanced animation update with proper idle progression and thread safety"""
        try:
            current_time = time.time()
            
            # Handle system stats periodically (moved from keystroke handler)
            try:
                self.update_system_stats()
            except Exception as stats_error:
                print(f"⚠️ Stats update error: {stats_error}")
            
            # Thread-safe access to keystroke data
            with self._data_lock:
                last_keystroke_time = self.last_keystroke_time
                keystroke_buffer_copy = list(self.keystroke_buffer)  # Copy for processing
                typing_active = self.typing_active
            
            # Check for idle timeout
            if current_time - last_keystroke_time > self.idle_timeout:
                # Typing has stopped
                if typing_active:
                    with self._data_lock:
                        self.typing_active = False
                        self.current_wpm = 0
                        self.idle_start_time = current_time
                        # Clear the keystroke buffer
                        self.keystroke_buffer.clear()
                    
                    # Send final animation command with WPM = 0 to reset display
                    self.send_animation_command(0, force_update=True)
                    
                    # Send IDLE_START to enable Arduino idle progression
                    if self.serial_conn and self.serial_conn.is_open:
                        self.serial_conn.write(b"IDLE_START\n")
                        print("💤 Typing stopped - enabling idle progression")
                
                # Don't send any more commands when idle
                return
            
            # Currently typing - calculate WPM
            if keystroke_buffer_copy:
                new_wpm = self.calculate_wpm_industry_standard()
                
                # Smooth WPM changes to prevent rapid fluctuations
                if self.current_wpm == 0:
                    self.current_wpm = new_wpm  # Initial value
                else:
                    # Adaptive smoothing: faster response for big changes, stability for small ones
                    wpm_diff = abs(new_wpm - self.current_wpm)
                    if wpm_diff > 15:  # Big change - respond quickly
                        smoothing = 0.7
                    elif wpm_diff > 5:  # Medium change - moderate smoothing  
                        smoothing = 0.4
                    else:  # Small change - heavy smoothing
                        smoothing = 0.2
                    
                    self.current_wpm = (self.current_wpm * (1 - smoothing)) + (new_wpm * smoothing)
                
                # Send animation command with rate limiting
                self.send_animation_command(self.current_wpm)
                        
        except Exception as e:
            print(f"❌ Animation update error: {e}")
    
    def update_animation_loop(self):
        """Background thread with optimized update logic and freeze detection"""
        print("🎬 Animation thread started")
        last_heartbeat = time.time()
        
        while self.running:
            try:
                current_time = time.time()
                
                # Anti-freeze watchdog: output heartbeat every 5 seconds during activity
                if current_time - last_heartbeat > 5.0:
                    print(f"💓 Heartbeat: WPM={self.current_wpm:.1f}, State={self.current_state}, Active={self.typing_active}")
                    last_heartbeat = current_time
                
                self.update_animation()  # Use the new optimized method
                time.sleep(0.08)  # ~12 FPS - balanced performance
                
            except Exception as e:
                print(f"❌ Animation loop error: {e}")
                # Continue running even if there's an error
                time.sleep(0.1)
        print("🛑 Animation thread stopped")
    
    def start_monitoring(self):
        """Start the enhanced typing monitor"""
        print("🚀 Bongo Cat Typing Monitor v2.2 - Industry Standard")
        print("=" * 65)
        print("🎯 Enhanced Features:")
        print("   • Industry-standard WPM calculation (5 chars = 1 word)")
        print("   • Automatic computer time synchronization")
        print("   • Optimized animation curves based on typing research")
        print("   • Smart hysteresis prevents animation flickering")
        print("   • Enhanced responsiveness with stability")
        print("")
        print("📊 Animation States:")
        print(f"   • Slow: < {self.slow_threshold} WPM (4-step paw pattern)")
        print(f"   • Normal: {self.slow_threshold}-{self.normal_threshold-1} WPM (4-step paw pattern)")
        print(f"   • Fast: {self.normal_threshold}+ WPM (4-step paw + click effects)")
        print("")
        print("😊 Happy Face Mode:")
        print(f"   • Activates at {self.fast_threshold}+ WPM (overlays on any animation state)")
        print("")
        print("📝 Start typing to see your cat react!")
        print("🛑 Press Ctrl+C to stop")
        print("-" * 65)
        
        if not self.connect_serial():
            return False
        
        self.running = True
        
        # Start the animation update thread
        update_thread = threading.Thread(target=self.update_animation_loop, daemon=True)
        update_thread.start()
        
        # Start keyboard listener
        try:
            with keyboard.Listener(on_press=self.on_key_press) as listener:
                listener.join()
        except KeyboardInterrupt:
            pass
        
        return True
    
    def stop_monitoring(self):
        """Stop the typing monitor"""
        print("\n🛑 Stopping Bongo Cat monitor...")
        self.running = False
        self.disconnect_serial()
        print("👋 Thank you for using Bongo Cat! Keep typing! ⌨️🐱")

def main():
    """Main function"""
    print("🐱 Bongo Cat Typing Monitor - Industry Standard Edition")
    print("💪 Version 2.2 - Time Fixed & WPM Optimized!")
    
    controller = BongoCatController(port='AUTO')
    
    try:
        if controller.start_monitoring():
            pass
    except KeyboardInterrupt:
        pass
    finally:
        controller.stop_monitoring()

if __name__ == "__main__":
    main() 