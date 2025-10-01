#!/usr/bin/env python3
"""
Find ESP32 Ports - List available serial ports (English version)
"""
import serial
import serial.tools.list_ports
import sys
import time

def find_all_ports():
    """List all available serial ports"""
    print("🔍 Scanning for all available ports...")
    print("=" * 50)
    
    ports = serial.tools.list_ports.comports()
    
    if not ports:
        print("❌ No serial ports found!")
        print("💡 Make sure your device is connected and drivers are installed")
        return
    
    print(f"📋 Found {len(ports)} port(s):")
    print()
    
    esp32_ports = []
    for i, port in enumerate(ports, 1):
        # Check whether the port looks like an ESP32 (common USB-UART chips)
        is_esp32 = any(keyword in port.description.lower() for keyword in 
                      ['cp210', 'ch340', 'ch341', 'usb serial', 'usb-serial', 'uart', 'usb uart'])
        
        status = "🟢 ESP32" if is_esp32 else "⚪ Other"
        print(f"  {i:2d}. {status} {port.device}")
        print(f"      Description: {port.description}")
        print(f"      Hardware ID: {port.hwid}")
        print()
        
        if is_esp32:
            esp32_ports.append(port.device)
    
    if esp32_ports:
        print("✅ ESP32 ports found:")
        for port in esp32_ports:
            print(f"   📍 {port}")
        print()
        print("💡 Use one of these ports in your scripts:")
        print(f"   python direct_test.py {esp32_ports[0]}")
    else:
        print("⚠️  No ESP32 ports detected")
        print("💡 Try connecting your ESP32 and running this script again")
        print("💡 Make sure you have the correct drivers installed:")
        print("   - CP210x drivers (for most ESP32 boards)")
        print("   - CH340 drivers (for some ESP32 boards)")

def test_port(port_name):
    """Test whether a specific port can be opened"""
    print(f"🧪 Testing port: {port_name}")
    print("=" * 30)
    
    try:
        ser = serial.Serial(port_name, 115200, timeout=2)
        print(f"✅ Port {port_name} is available!")
        
        # Try to read some data
        print("📥 Checking for data...")
        time.sleep(1)
        
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            print(f"📨 Received data: {repr(data)}")
        else:
            print("📥 No data received (this is normal if ESP32 is not running)")
        
        ser.close()
        print("✅ Port test completed!")
        
    except serial.SerialException as e:
        print(f"❌ Port {port_name} is not available: {e}")
    except Exception as e:
        print(f"❌ Error testing port: {e}")

if __name__ == "__main__":
    print("🐱 Bongo Cat Monitor - Port Finder")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        # Test specific port
        port = sys.argv[1]
        test_port(port)
    else:
        # List all ports
        find_all_ports()
    
    print("\n💡 Tips:")
    print("   - Windows: Use COM3, COM4, etc.")
    print("   - Linux/Mac: Use /dev/ttyUSB0, /dev/ttyACM0, etc.")
    print("   - Check Device Manager (Windows) or lsusb (Linux) for more info")
