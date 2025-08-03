#!/usr/bin/env python3
"""
Direct ESP32 Test - Send data directly to COM9
"""
import serial
import time
import psutil

def test_direct_esp32():
    print("🔧 Direct ESP32 Test")
    print("=" * 40)
    
    try:
        # Connect to ESP32
        print("🔌 Connecting to COM9...")
        ser = serial.Serial('COM9', 115200, timeout=1)
        print("✅ Connected to COM9!")
        
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
            'ANIM:2'   # Test animation
        ]
        
        print("\n📤 Sending commands:")
        for cmd in commands:
            full_cmd = f'{cmd}\n'
            ser.write(full_cmd.encode())
            print(f"  Sent: {cmd}")
            time.sleep(0.1)  # Small delay between commands
        
        print("\n⏱️ Waiting 3 seconds...")
        time.sleep(3)
        
        # Check if ESP32 responds
        if ser.in_waiting > 0:
            response = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            print(f"📥 ESP32 Response: {repr(response)}")
        else:
            print("📥 No response from ESP32 (this is normal)")
        
        ser.close()
        print("✅ Test completed!")
        print("\n💡 Check your ESP32 screen - you should see:")
        print(f"   CPU: {cpu}%")
        print(f"   RAM: {ram}%") 
        print(f"   WPM: 25")
        print(f"   Time: {current_time}")
        print("   Animation should change!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_direct_esp32()