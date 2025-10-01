#!/usr/bin/env python3
"""
Direct ESP32 Test - Send data directly to ESP32 (English version)
"""
import serial
import serial.tools.list_ports
import time
import psutil
import sys

def find_esp32_port():
    """Auto-detect an ESP32 serial port"""
    print("🔍 Scanning for ESP32...")
    
    # Get all available ports
    ports = serial.tools.list_ports.comports()
    esp32_ports = []
    
    for port in ports:
        # Check common ESP32 USB-to-UART chip identifiers
        if any(keyword in port.description.lower() for keyword in 
               ['cp210', 'ch340', 'ch341', 'usb serial', 'usb-serial', 'uart', 'usb uart']):
            esp32_ports.append(port.device)
            print(f"  📍 Found potential ESP32 port: {port.device} ({port.description})")
    
    if not esp32_ports:
        print("❌ No ESP32 ports found!")
        print("💡 Make sure your ESP32 is connected and drivers are installed")
        return None
    
    if len(esp32_ports) == 1:
        print(f"✅ Auto-selected: {esp32_ports[0]}")
        return esp32_ports[0]
    
    # Multiple ports found - let the user choose
    print("\n🔢 Multiple ports found. Please select:")
    for i, port in enumerate(esp32_ports):
        print(f"  {i+1}. {port}")
    
    while True:
        try:
            choice = int(input("Enter choice (1-{}): ".format(len(esp32_ports))))
            if 1 <= choice <= len(esp32_ports):
                selected_port = esp32_ports[choice-1]
                print(f"✅ Selected: {selected_port}")
                return selected_port
            else:
                print("❌ Invalid choice!")
        except ValueError:
            print("❌ Please enter a number!")
        except KeyboardInterrupt:
            print("\n👋 Cancelled by user")
            return None

def test_direct_esp32():
    print("🔧 Direct ESP32 Test")
    print("=" * 40)
    
    # Auto-detect or use a provided port from CLI
    if len(sys.argv) > 1:
        port = sys.argv[1]
        print(f"🔌 Using specified port: {port}")
    else:
        port = find_esp32_port()
        if not port:
            return
    
    try:
        # Connect to ESP32
        print(f"🔌 Connecting to {port}...")
        ser = serial.Serial(port, 115200, timeout=1)
        print(f"✅ Connected to {port}!")
        
        # Get current system stats
        cpu = int(psutil.cpu_percent(interval=1))
        ram = int(psutil.virtual_memory().percent)
        current_time = time.strftime("%H:%M")
        
        print(f"📊 System Stats: CPU={cpu}%, RAM={ram}%, Time={current_time}")
        
        # Send commands one by one
        commands = [
            f'CPU:{cpu}',
            f'RAM:{ram}', 
            f'WPM:25',  # Test with a fixed WPM
            f'TIME:{current_time}',
            'SPEED:120',  # Test typing animation
            'PING'  # Test connection
        ]
        
        print("\n📤 Sending basic commands:")
        for cmd in commands:
            full_cmd = f'{cmd}\n'
            ser.write(full_cmd.encode())
            print(f"  Sent: {cmd}")
            time.sleep(0.1)  # Small delay between commands
        
        # Test sensor-related display/settings commands
        print("\n🔧 Testing sensor commands:")
        sensor_commands = [
            'DISPLAY_TEMP:ON',
            'DISPLAY_HUMID:ON', 
            'DISPLAY_AUDIO:ON',
            'TOUCH_ENABLE:ON',
            'AUDIO_ANIMATION:ON',
            'AUDIO_SENSITIVITY:150'
        ]
        
        for cmd in sensor_commands:
            full_cmd = f'{cmd}\n'
            ser.write(full_cmd.encode())
            print(f"  Sent: {cmd}")
            time.sleep(0.1)
        
        print("\n⏱️ Waiting 3 seconds for responses...")
        time.sleep(3)
        
        # Read ESP32 responses with a small timeout
        print("\n📥 Reading ESP32 responses:")
        response_count = 0
        start_time = time.time()
        timeout_duration = 2.0  # 2s timeout
        
        while time.time() - start_time < timeout_duration:
            if ser.in_waiting > 0:
                try:
                    response = ser.readline().decode('utf-8', errors='ignore').strip()
                    if response:
                        print(f"  📨 {response}")
                        response_count += 1
                except Exception as e:
                    print(f"  ⚠️ Error reading response: {e}")
                    break
            time.sleep(0.01)  # 10ms delay
        
        if response_count == 0:
            print("  📥 No response from ESP32 (this can be normal if the sketch prints nothing)")
        else:
            print(f"  ✅ Received {response_count} responses")
        
        ser.close()
        print("\n✅ Test completed!")
        print("\n💡 Check your ESP32 screen - you should see:")
        print(f"   CPU: {cpu}%")
        print(f"   RAM: {ram}%") 
        print(f"   WPM: 25")
        print(f"   Time: {current_time}")
        print("   T: XX.X°C (temperature)")
        print("   H: XX% (humidity)")
        print("   A: XXXX (audio level)")
        print("   Animation should be active!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    print("🐱 Bongo Cat Monitor - Direct Test Script")
    print("=" * 50)
    print("Usage:")
    print("  python direct_test.py              # Auto-detect ESP32 port")
    print("  python direct_test.py COM3         # Use specific port (Windows)")
    print("  python direct_test.py /dev/ttyUSB0 # Use specific port (Linux/Mac)")
    print("=" * 50)
    print()
    
    test_direct_esp32()
