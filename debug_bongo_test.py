💓 Heartbeat:💓 Heartbeat:🔄 Keep-alive🔄 Keep-alive#!/usr/bin/env python3
"""
Debug Bongo Cat Test - Minimal version to isolate animation issues
"""

import time
import serial
import serial.tools.list_ports
import threading
from collections import deque
from pynput import keyboard

class DebugBongoCat:
    def __init__(self):
        # CONSERVATIVE timing to prevent buffer overflow
        self.min_command_interval = 1.0   # INCREASED from 0.5 to 1.0 second
        self.idle_timeout = 1.0
        
        # Simplified tracking
        self.keystroke_buffer = deque(maxlen=10)  # Reduced buffer
        self.last_keystroke_time = 0
        self.typing_active = False
        self.current_wpm = 0
        self.last_command_time = 0
        self.running = False
        self.serial_conn = None
        
        # Debug counters
        self.commands_sent = 0
        self.last_sent_command = ""
        
        # Lock for thread safety
        self._data_lock = threading.Lock()
    
    def find_esp32_port(self):
        """Find ESP32 port"""
        ports = serial.tools.list_ports.comports()
        for port in ports:
            description = str(port.description).upper()
            if any(keyword in description for keyword in ['CH340', 'CP210', 'ESP32']):
                print(f"✅ Found ESP32: {port.device}")
                return port.device
        return None
    
    def connect_serial(self):
        """Connect to ESP32"""
        port = self.find_esp32_port()
        if not port:
            print("❌ No ESP32 found")
            return False
        
        try:
            self.serial_conn = serial.Serial(port, 115200, timeout=0, writeTimeout=0)
            time.sleep(2)
            print(f"✅ Connected to {port}")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def send_command_debug(self, command):
        """Send command with extensive debugging"""
        if not self.serial_conn or not self.serial_conn.is_open:
            return
            
        current_time = time.time()
        time_since_last = current_time - self.last_command_time
        
        try:
            self.serial_conn.write(f"{command}\n".encode())
            self.commands_sent += 1
            self.last_sent_command = command
            self.last_command_time = current_time
            
            print(f"🔧 CMD #{self.commands_sent}: {command} (gap: {time_since_last:.2f}s)")
            
        except Exception as e:
            print(f"❌ Command failed: {command} - {e}")
    
    def on_key_press(self, key):
        """Simple keystroke detection"""
        current_time = time.time()
        
        with self._data_lock:
            self.keystroke_buffer.append(current_time)
            self.last_keystroke_time = current_time
            
            if not self.typing_active:
                self.typing_active = True
                print("⌨️ Typing STARTED")
    
    def calculate_simple_wpm(self):
        """Simplified WPM calculation"""
        if len(self.keystroke_buffer) < 2:
            return 0
        
        now = time.time()
        recent_keystrokes = [t for t in self.keystroke_buffer if now - t < 5.0]
        
        if len(recent_keystrokes) < 2:
            return 0
        
        time_span = now - recent_keystrokes[0]
        if time_span > 0.5:
            return (len(recent_keystrokes) / 5.0) * (60 / time_span)
        return 0
    
    def update_animation_debug(self):
        """Simplified animation with debugging"""
        current_time = time.time()
        
        # Check for idle timeout
        if current_time - self.last_keystroke_time > self.idle_timeout:
            if self.typing_active:
                with self._data_lock:
                    self.typing_active = False
                    self.current_wpm = 0
                    self.keystroke_buffer.clear()
                
                print("💤 Typing STOPPED - sending STOP command")
                self.send_command_debug("STOP")
                return
        
        # Calculate WPM and send commands
        if self.typing_active:
            new_wmp = self.calculate_simple_wpm()
            
            # Only send command if enough time has passed
            if current_time - self.last_command_time >= self.min_command_interval:
                if new_wmp > 0:
                    # Simple speed mapping: higher WPM = lower delay
                    speed = max(100, min(500, 500 - (new_wmp * 10)))
                    print(f"📊 WPM: {new_wmp:.1f} → Speed: {speed}ms")
                    self.send_command_debug(f"SPEED:{int(speed)}")
                else:
                    print("📊 WPM: 0 → STOP")
                    self.send_command_debug("STOP")
    
    def animation_loop(self):
        """Main animation loop"""
        print("🎬 Debug animation loop started")
        while self.running:
            try:
                self.update_animation_debug()
                time.sleep(0.1)  # 10 FPS for easier debugging
            except Exception as e:
                print(f"❌ Animation error: {e}")
                time.sleep(0.1)
    
    def start_debug(self):
        """Start debug test"""
        print("🚀 Debug Bongo Cat Test")
        print("=" * 50)
        print("🎯 This test uses CONSERVATIVE timing to isolate issues")
        print("   • 1.0s minimum between commands (vs 0.5s)")
        print("   • 10 FPS animation loop (vs 12.5 FPS)")
        print("   • Extensive command logging")
        print("   • Simplified WPM calculation")
        print("")
        print("📝 Start typing to test...")
        print("🛑 Press Ctrl+C to stop")
        print("-" * 50)
        
        if not self.connect_serial():
            return False
        
        self.running = True
        
        # Start animation thread
        animation_thread = threading.Thread(target=self.animation_loop, daemon=True)
        animation_thread.start()
        
        # Start keyboard listener on main thread
        try:
            with keyboard.Listener(on_press=self.on_key_press) as listener:
                listener.join()
        except KeyboardInterrupt:
            pass
        
        self.running = False
        print(f"\n📊 Debug Summary:")
        print(f"   Commands sent: {self.commands_sent}")
        print(f"   Last command: {self.last_sent_command}")
        return True

if __name__ == "__main__":
    debug = DebugBongoCat()
    debug.start_debug() 