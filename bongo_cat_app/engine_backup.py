#!/usr/bin/env python3
"""
Bongo Cat Monitoring Engine - Refactored
Core logic extracted from the original script with configuration support
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
from typing import Callable, Optional, Dict, Any

class BongoCatEngine:
    """Core Bongo Cat monitoring engine with configuration support"""
    
    def __init__(self, config_manager=None):
        """Initialize the Bongo Cat engine with optional configuration manager"""
        self.config = config_manager
        
        # Get connection settings from config or use defaults
        if self.config:
            conn_settings = self.config.get_connection_settings()
            self.port = conn_settings.get('com_port', 'AUTO')
            self.baudrate = conn_settings.get('baudrate', 115200)
            behavior_settings = self.config.get_behavior_settings()
            self.idle_timeout = behavior_settings.get('idle_timeout_seconds', 3.0)
        else:
            self.port = 'AUTO'
            self.baudrate = 115200
            self.idle_timeout = 3.0
        
        self.serial_conn = None
        self.running = False
        
        # Enhanced animation control with reduced command frequency
        self.last_sent_speed = -1
        self.last_sent_state = ""
        self.last_command_time = 0
        self.min_command_interval = 0.5   # Minimum 500ms between commands (2 FPS max)
        
        # Proper keystroke detection and timing
        self.keystroke_buffer = deque(maxlen=50)  # Store recent keystrokes
        self.last_keystroke_time = 0
        self.typing_active = False
        self.idle_start_time = 0
        
        # Improved WPM calculation with stability optimizations
        self.typing_sessions = deque(maxlen=10)  # Reduced from 20 for faster response
        self.wpm_history = deque(maxlen=5)       # Fixed: was wmp_history
        self.current_wpm = 0
        self.max_wpm = 100               # Reasonable ceiling for most users
        
        # Enhanced state management with better hysteresis
        self.current_state = "IDLE"
        self.state_change_time = time.time()
        self.state_stability_time = 0.5  # Reduced from longer delays for responsiveness
        
        # Enhanced timing settings based on research
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
        self.slow_threshold = 20         # Below average
        self.normal_threshold = 40       # Average range
        self.fast_threshold = 65         # Good/Professional range
        self.streak_threshold = 85       # Excellent range
        
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
        
        # Configuration change callbacks
        self.config_callbacks: Dict[str, Callable] = {}
        
        # Setup configuration callbacks if config manager provided
        if self.config:
            self.config.add_change_callback(self._on_config_change)
    
    def _on_config_change(self, key: str, value: Any):
        """Handle configuration changes"""
        print(f"🔧 Engine: Config changed {key} = {value}")
        
        # Apply configuration changes to Arduino
        if key == "display.show_cpu":
            self.send_command(f"DISPLAY_CPU:{'ON' if value else 'OFF'}")
        elif key == "display.show_ram":
            self.send_command(f"DISPLAY_RAM:{'ON' if value else 'OFF'}")
        elif key == "display.show_wpm":
            self.send_command(f"DISPLAY_WPM:{'ON' if value else 'OFF'}")
        elif key == "display.show_time":
            self.send_command(f"DISPLAY_TIME:{'ON' if value else 'OFF'}")
        elif key == "display.time_format_24h":
            self.send_command(f"TIME_FORMAT:{'24' if value else '12'}")
        elif key == "behavior.sleep_timeout_minutes":
            self.send_command(f"SLEEP_TIMEOUT:{value}")
        elif key == "behavior.animation_sensitivity":
            self.send_command(f"SENSITIVITY:{value}")
        elif key == "behavior.idle_timeout_seconds":
            self.idle_timeout = value
    
    def save_config_to_arduino(self):
        """Save current configuration to Arduino EEPROM"""
        print("💾 Saving configuration to Arduino EEPROM...")
        self.send_command("SAVE_SETTINGS")
        print("✅ Configuration saved to Arduino EEPROM")

    def apply_all_config_to_arduino(self):
        """Send all current configuration settings to Arduino"""
        if not self.config:
            return
        
        print("📤 Applying all configuration to Arduino...")
        
        # Apply display settings
        display = self.config.get_display_settings()
        self.send_command(f"DISPLAY_CPU:{'ON' if display.get('show_cpu') else 'OFF'}")
        self.send_command(f"DISPLAY_RAM:{'ON' if display.get('show_ram') else 'OFF'}")
        self.send_command(f"DISPLAY_WPM:{'ON' if display.get('show_wpm') else 'OFF'}")
        self.send_command(f"DISPLAY_TIME:{'ON' if display.get('show_time') else 'OFF'}")
        self.send_command(f"TIME_FORMAT:{'24' if display.get('time_format_24h') else '12'}")
        
        # Apply behavior settings  
        behavior = self.config.get_behavior_settings()
        self.send_command(f"SLEEP_TIMEOUT:{behavior.get('sleep_timeout_minutes', 5)}")
        self.send_command(f"SENSITIVITY:{behavior.get('animation_sensitivity', 1.0)}")
        
        # Save settings to Arduino EEPROM
        self.send_command("SAVE_SETTINGS")
        
        print("✅ Configuration applied to Arduino")

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
            
            # For automated mode, just use the first one
            selected_port = esp32_ports[0].device
            print(f"✅ Auto-selected first device: {selected_port}")
            return selected_port

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
                        # Send initial sync and apply configuration
                        self.send_initial_sync()
                        return True
                
                print(f"✅ Connected to {self.port}")
                # Send initial sync and apply configuration
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
            
            # Apply all configuration settings to Arduino
            self.apply_all_config_to_arduino()
            
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
        wmp = int(self.current_wpm)
        
        # Send system stats
        stats_command = f"STATS:CPU:{cpu},RAM:{ram},WPM:{wmp}"
        self.send_command(stats_command)
        
        # Send current computer time (automatically synced)
        current_time = datetime.datetime.now().strftime("%H:%M")
        time_command = f"TIME:{current_time}"
        self.send_command(time_command)
    
    def update_system_stats(self):
        """Update system stats with rate limiting to prevent overwhelming ESP32"""
        current_time = time.time()
        
        # Rate limit to prevent overwhelming the serial connection
        if not hasattr(self, 'last_stats_sent'):
            self.last_stats_sent = 0
            self.last_time_sent = 0
        
        # Always update local stats for WPM calculation
        self.get_system_stats()
        
        # Send system stats every 2 seconds
        if current_time - self.last_stats_sent >= 2.0:
            try:
                cpu, ram = self.get_system_stats()
                wmp = int(self.current_wpm)
                stats_command = f"STATS:CPU:{cpu},RAM:{ram},WPM:{wmp}"
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
            return getattr(self, '_cached_wpm', 0)
        
        # Thread-safe access to keystroke buffer
        with self._data_lock:
            if len(self.keystroke_buffer) < 2:
                self._cached_wpm = 0
                self._last_wpm_calc_time = now
                return 0
            
            recent_keystrokes = list(self.keystroke_buffer)[-8:]
            
            if len(recent_keystrokes) < 2:
                self._cached_wpm = 0
                self._last_wpm_calc_time = now
                return 0
            
            time_span = now - recent_keystrokes[0]
            keystroke_count = len(recent_keystrokes)
        
        if time_span > 0.4:
            raw_wpm = (keystroke_count / self.chars_per_word) * (60 / time_span)
            
            if hasattr(self, '_cached_wpm') and self._cached_wpm > 0:
                smoothed_wpm = (self._cached_wpm * 0.6) + (raw_wpm * 0.4)
            else:
                smoothed_wpm = raw_wpm
        
            self._cached_wpm = min(smoothed_wpm, self.max_wpm)
            self._last_wpm_calc_time = now
            return self._cached_wpm
        
        self._cached_wpm = 0
        self._last_wpm_calc_time = now
        return 0
    
    def wpm_to_animation_speed(self, wpm):
        """Convert WPM to animation speed with research-based optimization"""
        if wpm <= 0:
            return self.min_animation_speed
        
        import math
        normalized = min(wpm / self.max_wpm, 1.0)
        
        if normalized < 0.3:
            curved = normalized * 1.5
        else:
            curved = 0.45 + (normalized - 0.3) * 0.8
        
        curved = min(curved, 1.0)
        speed = self.min_animation_speed - (curved * (self.min_animation_speed - self.max_animation_speed))
        return int(max(speed, self.max_animation_speed))
    
    def determine_animation_state(self, wpm):
        """Determine animation state with improved hysteresis"""
        hysteresis = 2
        
        if self.current_state == "IDLE":
            if wpm >= 3:
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
        
        return self.current_state
    
    def is_streak_active(self, wpm):
        """Determine if streak mode should be active based on WPM"""
        return wpm >= self.fast_threshold
    
    def handle_idle_progression(self, now):
        """Handle controlled idle progression"""
        if not self.typing_active:
            if not self.idle_progression_started:
                if now - self.idle_start_time > 1.5:
                    self.send_command("IDLE_START")
                    self.idle_progression_started = True
                    print("😴 Starting idle progression...")
        else:
            self.idle_start_time = 0
            self.idle_progression_started = False
    
    def on_key_press(self, key):
        """Lightweight keystroke detection"""
        try:
            current_time = time.time()
            
            with self._data_lock:
                self.keystroke_buffer.append(current_time)
                self.last_keystroke_time = current_time
                
                if not self.typing_active:
                    self.typing_active = True
                    print("⌨️ Typing started")
                
        except Exception as e:
            print(f"❌ Keystroke detection error: {e}")
    
    def send_animation_command(self, wpm, force_update=False):
        """Send animation command with improved rate limiting"""
        current_time = time.time()
        
        if not force_update and (current_time - self.last_command_time) < self.min_command_interval:
            return
        
        new_state = self.determine_animation_state(wpm)
        animation_speed = self.wpm_to_animation_speed(wpm)
        is_streak = self.is_streak_active(wpm)
        
        if not hasattr(self, 'last_streak_state'):
            self.last_streak_state = False
        
        speed_changed = abs(animation_speed - self.last_sent_speed) > 25
        state_changed = new_state != self.last_sent_state
        streak_changed = is_streak != self.last_streak_state
        
        time_since_last_command = current_time - self.last_command_time
        force_periodic_update = time_since_last_command > 4.0
        
        if state_changed or speed_changed or streak_changed or force_update or force_periodic_update:
            self.last_sent_speed = animation_speed
            self.last_sent_state = new_state
            self.last_command_time = current_time
            
            if streak_changed:
                self.last_streak_state = is_streak
            
            if force_periodic_update and not (state_changed or speed_changed or streak_changed or force_update):
                print(f"🔄 Keep-alive: {new_state} | WPM: {self.current_wpm:.1f} | Speed: {animation_speed}ms")
            elif state_changed or streak_changed or force_update:
                if self.current_state != new_state or streak_changed:
                    base_emoji = {"SLOW": "🐌", "NORMAL": "👐", "FAST": "⚡"}.get(new_state, "")
                    emoji = f"{base_emoji}😊" if is_streak else base_emoji
                    streak_text = " (HAPPY)" if is_streak else ""
                    print(f"🐱 {self.current_state} → {new_state}{streak_text} | WPM: {self.current_wpm:.1f} | Speed: {animation_speed}ms {emoji}")
                    self.current_state = new_state
                    self.state_change_time = current_time
            
            if self.serial_conn and self.serial_conn.is_open:
                try:
                    commands_to_send = []
                    
                    if wpm <= 0:
                        commands_to_send.append("STOP")
                        if self.last_streak_state:
                            commands_to_send.append("STREAK_OFF")
                            self.last_streak_state = False
                    else:
                        commands_to_send.append(f"SPEED:{animation_speed}")
                        if streak_changed:
                            if is_streak:
                                commands_to_send.append("STREAK_ON")
                            else:
                                commands_to_send.append("STREAK_OFF")
                    
                    if commands_to_send:
                        combined_command = '\n'.join(commands_to_send) + '\n'
                        self.serial_conn.write(combined_command.encode())
                        
                except serial.SerialTimeoutException:
                    print("⚠️ Serial buffer full - skipping command")
                except Exception as e:
                    print(f"❌ Command send error: {e}")
    
    def update_animation(self):
        """Enhanced animation update with proper idle progression"""
        try:
            current_time = time.time()
            
            try:
                self.update_system_stats()
            except Exception as stats_error:
                print(f"⚠️ Stats update error: {stats_error}")
            
            with self._data_lock:
                last_keystroke_time = self.last_keystroke_time
                keystroke_buffer_copy = list(self.keystroke_buffer)
                typing_active = self.typing_active
            
            if current_time - last_keystroke_time > self.idle_timeout:
                if typing_active:
                    with self._data_lock:
                        self.typing_active = False
                        self.current_wpm = 0
                        self.idle_start_time = current_time
                        self.keystroke_buffer.clear()
                    
                    self.send_animation_command(0, force_update=True)
                    
                    if self.serial_conn and self.serial_conn.is_open:
                        self.serial_conn.write(b"IDLE_START\n")
                        print("💤 Typing stopped - enabling idle progression")
                
                return
            
            if keystroke_buffer_copy:
                new_wpm = self.calculate_wpm_industry_standard()
                
                if self.current_wpm == 0:
                    self.current_wpm = new_wpm
                else:
                    wpm_diff = abs(new_wpm - self.current_wpm)
                    if wpm_diff > 15:
                        smoothing = 0.7
                    elif wpm_diff > 5:
                        smoothing = 0.4
                    else:
                        smoothing = 0.2
                    
                    self.current_wpm = (self.current_wpm * (1 - smoothing)) + (new_wpm * smoothing)
                
                self.send_animation_command(self.current_wpm)
                        
        except Exception as e:
            print(f"❌ Animation update error: {e}")
    
    def update_animation_loop(self):
        """Background thread with optimized update logic"""
        print("🎬 Animation thread started")
        last_heartbeat = time.time()
        
        while self.running:
            try:
                current_time = time.time()
                
                if current_time - last_heartbeat > 5.0:
                    print(f"💓 Heartbeat: WPM={self.current_wpm:.1f}, State={self.current_state}, Active={self.typing_active}")
                    last_heartbeat = current_time
                
                # Remove redundant idle progression - handled in update_animation
                self.update_animation()
                time.sleep(0.08)
                
            except Exception as e:
                print(f"❌ Animation loop error: {e}")
                time.sleep(0.1)
        print("🛑 Animation thread stopped")
    
    def start_monitoring(self):
        """Start the enhanced typing monitor"""
        print("🚀 Bongo Cat Engine v2.2 - Industry Standard")
        print("=" * 65)
        print("🎯 Enhanced Features:")
        print("   • Industry-standard WPM calculation (5 chars = 1 word)")
        print("   • Automatic computer time synchronization")
        print("   • Configuration management support")
        print("   • Real-time settings updates")
        print("")
        print("📊 Animation States:")
        print(f"   • Slow: < {self.slow_threshold} WPM (4-step paw pattern)")
        print(f"   • Normal: {self.slow_threshold}-{self.normal_threshold-1} WPM (4-step paw pattern)")
        print(f"   • Fast: {self.normal_threshold}+ WPM (4-step paw + click effects)")
        print("")
        print("😊 Happy Face Mode:")
        print(f"   • Activates at {self.fast_threshold}+ WPM")
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

# For backwards compatibility 
BongoCatController = BongoCatEngine
