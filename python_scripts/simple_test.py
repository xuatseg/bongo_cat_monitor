#!/usr/bin/env python3
"""
Simple ESP32 Test - Minimal script to avoid blocking issues (English version)
"""
import serial
import serial.tools.list_ports
import time
import sys

def find_esp32_port():
    """Auto-detect an ESP32 serial port"""
    print("🔍 Scanning for ESP32...")
    
    ports = serial.tools.list_ports.comports()
    esp32_ports = []
    
    for port in ports:
        if any(keyword in port.description.lower() for keyword in 
               ['cp210', 'ch340', 'ch341', 'usb serial', 'usb-serial', 'uart', 'usb uart']):
            esp32_ports.append(port.device)
            print(f"  📍 Found: {port.device} ({port.description})")
    
    if not esp32_ports:
        print("❌ No ESP32 ports found!")
        return None
    
    if len(esp32_ports) == 1:
        print(f"✅ Auto-selected: {esp32_ports[0]}")
        return esp32_ports[0]
    
    print("\n🔢 Multiple ports found:")
    for i, port in enumerate(esp32_ports):
        print(f"  {i+1}. {port}")
    
    while True:
        try:
            choice = int(input("Enter choice (1-{}): ".format(len(esp32_ports))))
            if 1 <= choice <= len(esp32_ports):
                return esp32_ports[choice-1]
            else:
                print("❌ Invalid choice!")
        except (ValueError, KeyboardInterrupt):
            print("\n👋 Cancelled")
            return None

def simple_test():
    print("🐱 Simple ESP32 Test")
    print("=" * 30)
    
    # Get port
    if len(sys.argv) > 1:
        port = sys.argv[1]
        print(f"🔌 Using port: {port}")
    else:
        port = find_esp32_port()
        if not port:
            return
    
    try:
        # Open serial port
        print(f"🔌 Connecting to {port}...")
        ser = serial.Serial(port, 115200, timeout=1)
        print(f"✅ Connected!")
        
        # Send basic commands
        commands = [
            "PING",
            "CPU:50",
            "RAM:60", 
            "WPM:30",
            "TIME:12:34"
        ]
        
        print("\n📤 Sending commands:")
        for cmd in commands:
            ser.write(f"{cmd}\n".encode())
            print(f"  ✅ Sent: {cmd}")
            time.sleep(0.2)
        
        print("\n⏱️ Waiting 2 seconds...")
        time.sleep(2)
        
        # Read responses (no loop)
        print("\n📥 Checking for responses:")
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            print(f"📨 Response: {repr(data)}")
        else:
            print("📥 No immediate response (normal)")
        
        ser.close()
        print("\n✅ Test completed!")
        print("💡 Check your ESP32 screen for updates")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    simple_test()