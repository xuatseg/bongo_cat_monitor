# Quick Start Guide

## Prerequisites

1. **PlatformIO**: Install PlatformIO IDE or CLI
   ```bash
   pip install platformio
   ```

2. **Hardware**:
   - ESP32-WROOM-32 development board
   - ILI9341 TFT display (240x320)
   - Proper wiring according to pin configuration

## Quick Build and Upload

```bash
# Navigate to project directory
cd bongo-cat-esp32

# Build, upload, and monitor in one command
pio run --target upload --target monitor
```

## Pin Configuration (ESP32 to ILI9341)

| Function | ESP32 GPIO | ILI9341 Pin |
|----------|-----------|-------------|
| MISO     | 12        | SDO (MISO)  |
| MOSI     | 13        | SDI (MOSI)  |
| SCLK     | 14        | SCK         |
| CS       | 15        | CS          |
| DC       | 2         | DC/RS       |
| RST      | -         | RST (3.3V)  |
| BL       | 27        | LED/BL      |
| VCC      | 3.3V      | VCC         |
| GND      | GND       | GND         |

## First Time Setup

If this is your first build after cloning:

```bash
# 1. Copy configuration files (if extra_script.py doesn't work)
./copy_configs.sh

# 2. Build and upload
pio run --target upload --target monitor
```

## Common Commands

```bash
# Build only
pio run

# Upload only (must build first)
pio run --target upload

# Monitor serial output
pio device monitor

# Clean build
pio run --target clean
```

## Verify Success

### Serial Output
You should see:
```
🐱 Bongo Cat with Sprites Starting...
🔦 Backlight initialized on pin 27
📺 TFT initialized, setting rotation...
✅ Bongo Cat Ready!
🖼️ First flush callback triggered!
```

### Display
- White background
- Bongo Cat animation
- System stats (CPU, RAM, WPM)
- Time display

## Troubleshooting

### Build Fails
```bash
# Clean and rebuild
pio run --target clean
pio run
```

### Upload Fails
1. Check USB connection
2. Try holding BOOT button during upload
3. Reduce upload speed in `platformio.ini`

### Display Blank
1. Check wiring
2. Verify backlight connection (GPIO 27)
3. Check serial output for errors

## Next Steps

- Read [DEBUGGING_GUIDE.md](DEBUGGING_GUIDE.md) for detailed information
- Check [../README.md](../README.md) for project overview
- Configure display settings in `platformio.ini` if needed


