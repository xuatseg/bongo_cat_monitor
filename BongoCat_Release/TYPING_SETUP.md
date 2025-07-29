# 🐱 Bongo Cat Typing Monitor Setup

Make your bongo cat react to your typing speed in real-time with system monitoring!

## ⚡ Features

- **Real-time typing speed tracking** (Words Per Minute)
- **System monitoring display** showing CPU and RAM usage
- **Automatic bongo cat animation** that matches your typing speed
- **Smart idle detection** - cat rests when you stop typing
- **Speed-based animation intensity**:
  - Slow typing: Gentle bongo taps
  - Medium typing: Steady rhythm  
  - Fast typing: Intense drumming action! 🔥
- **Color-coded system stats** in top-left corner:
  - Green: Low usage
  - Yellow: Medium usage
  - Red: High usage

## 📋 Requirements

- ESP32 with Bongo Cat code uploaded
- Python 3.7 or newer
- USB cable connecting ESP32 to PC

## 🚀 Quick Setup

### 1. Install Python Dependencies

```bash
pip install pyserial pynput psutil
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

### 2. Find Your ESP32 COM Port

**Windows:**
- Open Device Manager
- Look for "Silicon Labs CP210x USB to UART Bridge" or similar
- Note the COM port (e.g., COM3, COM4)

**Linux/Mac:**
```bash
ls /dev/tty*
# Look for /dev/ttyUSB0 or /dev/ttyACM0
```

### 3. Update the Python Script

Edit `bongo_cat_typing_monitor.py` line 183:
```python
controller = BongoCatController(port='COM3')  # Change to your port
```

### 4. Upload Updated Arduino Code

Upload the modified `bongo_cat.ino` to your ESP32.

### 5. Run the Typing Monitor

```bash
python bongo_cat_typing_monitor.py
```

## 🎮 How It Works

- **Slow typing (0-30 WPM)**: Cat moves slowly 🐌
- **Medium typing (30-60 WPM)**: Cat gets energetic ⚡
- **Fast typing (60+ WPM)**: Cat goes crazy! 🔥
- **Stop typing**: Cat goes idle after 2 seconds 😴

## 🎛️ Customization

### Adjust Speed Ranges
In the Python script, modify these values:
```python
self.max_wpm = 120  # Your maximum typing speed
self.min_animation_speed = 1000  # Slowest animation (ms)
self.max_animation_speed = 50    # Fastest animation (ms)
```

### Change Idle Timeout
```python
self.idle_timeout = 2.0  # Seconds before going idle
```

## 🐛 Troubleshooting

### "Failed to connect" Error
- Check ESP32 is plugged in
- Verify COM port in Device Manager
- Close Arduino IDE Serial Monitor
- Try different USB cable

### Python Permission Errors (Linux/Mac)
```bash
sudo usermod -a -G dialout $USER
# Then logout and login again
```

### Cat Not Responding
1. Check Serial Monitor in Arduino IDE for messages
2. Send test command: Type anything to trigger animation
3. Verify upload was successful

## 🎯 Commands

The Python script sends these commands to ESP32:
- `SPEED:150` - Set animation speed to 150ms between frames
- `IDLE` - Stop animation, cat rests
- `SLOW` - Slow typing mode
- `PING` - Test connection

## 🔥 Pro Tips

1. **Minimize latency**: Close other serial applications
2. **Better accuracy**: Script ignores special keys (Ctrl, Alt, etc.)
3. **Smooth animation**: Speed changes are gradual, not instant
4. **Visual feedback**: Watch the console for real-time WPM display

Enjoy your reactive bongo cat! 🐱✨ 