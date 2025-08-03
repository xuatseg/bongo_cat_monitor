#!/usr/bin/env python3
"""
Quick ESP32 Connection Test
Tests if we can connect to COM9 directly
"""

import serial
import serial.tools.list_ports
import time

def test_esp32_connection():
    print("🔍 ESP32 Connection Test")
    print("=" * 40)
    
    # List all ports
    print("📡 Available COM ports:")
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"  {port.device} - {port.description}")
    
    print()
    
    # Test COM9 specifically
    try:
        print("🔌 Testing COM9 connection...")
        ser = serial.Serial('COM9', 115200, timeout=1)
        print("✅ Successfully connected to COM9!")
        
        # Send a test command
        print("📤 Sending test command: CPU:50")
        ser.write(b'CPU:50\n')
        time.sleep(0.1)
        
        # Try to read response
        if ser.in_waiting > 0:
            response = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            print(f"📥 Received: {repr(response)}")
        else:
            print("📥 No response (this is normal for ESP32)")
        
        ser.close()
        print("✅ COM9 test successful!")
        
    except Exception as e:
        print(f"❌ COM9 test failed: {e}")
        print("💡 Make sure:")
        print("  - ESP32 is connected via USB")
        print("  - No other app is using COM9")
        print("  - ESP32 firmware is flashed correctly")

if __name__ == "__main__":
    test_esp32_connection()