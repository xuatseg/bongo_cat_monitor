# ESP32 Project Setup and Debugging Guide

## Project Migration Summary

This document describes the process of migrating the Arduino `.ino` project to a PlatformIO-based ESP32 project structure.

## Key Steps Completed

### 1. Project Structure Setup
- Created `bongo-cat-esp32/` folder following naming convention
- Organized files into PlatformIO standard structure:
  ```
  bongo-cat-esp32/
  ├── src/main.cpp          # Main application (converted from .ino)
  ├── include/              # Header files
  ├── lib/                  # Local libraries
  ├── platformio.ini        # Build configuration
  └── docs/                 # Documentation
  ```

### 2. PlatformIO Configuration
- **Board**: `esp32dev` (ESP32-WROOM-32 module)
- **Framework**: Arduino
- **Upload speed**: 460800 baud
- **Monitor speed**: 115200 baud

### 3. Major Issues Resolved

#### Issue 1: Serial Port Conflict
**Problem**: `Serial` object not declared
```
error: 'Serial' was not declared in this scope
```

**Root Cause**: USB CDC configuration flags caused Serial redefinition

**Solution**: Removed conflicting USB CDC build flags:
```ini
; Removed these flags
-DARDUINO_USB_CDC_ON_BOOT=1
-DARDUINO_USB_MODE=1
-DARDUINO_USB_CDC_MODE=1
```

#### Issue 2: LVGL Configuration Path
**Problem**: LVGL couldn't find `lv_conf.h`
```
fatal error: ../../lv_conf.h: No such file or directory
```

**Solution**: 
- Added `LV_CONF_INCLUDE_SIMPLE` build flag
- Created `extra_script.py` to auto-copy config files
- Placed `lv_conf.h` in project root

#### Issue 3: TFT_eSPI Configuration
**Problem**: `TFT_WIDTH` and `TFT_HEIGHT` not defined
```
error: 'TFT_WIDTH' was not declared in this scope
```

**Solution**: Defined all TFT_eSPI settings via build flags in `platformio.ini`:
```ini
build_flags = 
    -DTFT_WIDTH=240
    -DTFT_HEIGHT=320
    -DILI9341_2_DRIVER=1
    -DTFT_MISO=12
    -DTFT_MOSI=13
    -DTFT_SCLK=14
    -DTFT_CS=15
    -DTFT_DC=2
    -DTFT_RST=-1
    -DTFT_BL=27
    ; ... more settings
```

#### Issue 4: Display Not Showing Content
**Problem**: Backlight on, but screen blank (white)

**Root Cause**: Missing backlight initialization in setup()

**Solution**: Added backlight control:
```cpp
#ifdef TFT_BL
pinMode(TFT_BL, OUTPUT);
digitalWrite(TFT_BL, HIGH);
#endif
```

#### Issue 5: Animation File Paths
**Problem**: Animation sprite files not found
```
fatal error: animations/body/standardbody1.c: No such file or directory
```

**Solution**: Updated include paths in `animations_sprites.h`:
```cpp
// Before
#include "animations/body/standardbody1.c"

// After  
#include "../lib/bongo_cat_animations/src/body/standardbody1.c"
```

## Hardware Configuration

### Display Pins (ILI9341)
- **MISO**: GPIO 12
- **MOSI**: GPIO 13
- **SCLK**: GPIO 14
- **CS**: GPIO 15
- **DC**: GPIO 2
- **RST**: -1 (not used)
- **BL**: GPIO 27 (backlight)
- **Touch CS**: GPIO 33

### Display Settings
- **Driver**: ILI9341_2_DRIVER
- **Resolution**: 240x320
- **Color Depth**: 16-bit (RGB565)
- **Byte Swap**: Enabled (`LV_COLOR_16_SWAP 1`)
- **Inversion**: ON

## Build Process

### Prerequisites
```bash
# Install PlatformIO
pip install platformio
```

### Build Commands
```bash
# Navigate to project directory
cd bongo-cat-esp32

# Build only
pio run

# Build and upload
pio run --target upload

# Build, upload, and monitor
pio run --target upload --target monitor

# Clean build
pio run --target clean
```

### Helper Scripts
- **copy_configs.sh**: Manually copy configuration files
- **build.sh**: Build script with error checking
- **extra_script.py**: Auto-copy configs before build (runs automatically)

## Verification Steps

### Serial Output (Success)
```
🐱 Bongo Cat with Sprites Starting...
📂 Settings loaded from EEPROM
🔦 Backlight initialized on pin 27
📺 Initializing TFT display...
📺 TFT initialized, setting rotation...
📺 Filling screen white...
📺 Screen filled!
🎨 Initializing LVGL...
🐱 Sprite manager initialized
🎨 Creating Bongo Cat UI...
🎨 Setting background color...
🎨 Creating labels...
🎨 CPU label created
🎨 Rendering initial sprite...
🎨 UI creation complete!
✅ Bongo Cat Ready!
🖼️ First flush callback triggered!
🖼️ Area: x1=0 y1=0 x2=239 y2=9
```

### Expected Display
- White background
- Bongo Cat animation in center
- CPU/RAM/WPM labels (top left)
- Time display (top right)

## Library Dependencies

```ini
lib_deps = 
    lvgl/lvgl@^8.3.11
    bodmer/TFT_eSPI@^2.5.43
    WiFi@^1.0.0
```

## Code Comments and Logs

All code comments and serial logs use English for better accessibility and maintainability.

## Future Improvements

1. Consider adding OTA (Over-The-Air) update support
2. Add Wi-Fi configuration portal
3. Implement power saving modes
4. Add touch screen support (hardware already configured)

## Troubleshooting

### Display Issues
1. Check pin connections match `platformio.ini` definitions
2. Verify backlight pin is correctly powered
3. Check SPI frequency (reduce if seeing corruption)

### Compilation Issues
1. Clean build directory: `pio run --target clean`
2. Run config copy script: `./copy_configs.sh`
3. Check library versions match

### Upload Issues
1. Reduce upload speed in `platformio.ini`
2. Hold BOOT button during upload
3. Check USB cable supports data transfer

## References

- [PlatformIO ESP32 Documentation](https://docs.platformio.org/en/latest/platforms/espressif32.html)
- [LVGL Documentation](https://docs.lvgl.io/)
- [TFT_eSPI Library](https://github.com/Bodmer/TFT_eSPI)

