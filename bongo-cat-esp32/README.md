# Bongo Cat ESP32

An ESP32-based Bongo Cat animation display with system monitoring capabilities.

## Features

- **Animated Bongo Cat**: Multiple animation states including idle, typing, and sleep modes
- **System Monitoring**: Real-time CPU, RAM, and WPM (Words Per Minute) display
- **Time Display**: 12/24 hour format with automatic updates
- **Configurable Settings**: Persistent settings stored in EEPROM
- **Serial Communication**: Python script integration for real-time control
- **Sprite-based Animation**: Layered sprite system for smooth animations

## Hardware Requirements

- ESP32 development board
- TFT display (240x320 recommended)
- TFT_eSPI compatible display driver

## Software Requirements

- PlatformIO IDE or Arduino IDE
- ESP32 Arduino Core
- Required libraries (automatically installed via PlatformIO):
  - LVGL (v8.3.11+)
  - TFT_eSPI (v2.5.43+)
  - WiFi (built-in)

## Project Structure

```
bongo-cat-esp32/
├── src/
│   └── main.cpp              # Main application code
├── include/
│   ├── animations_sprites.h  # Sprite definitions and animation states
│   ├── Free_Fonts.h         # Font definitions
│   ├── lv_conf.h            # LVGL configuration
│   └── User_Setup.h         # TFT_eSPI display configuration
├── animations/               # Animation sprite source files
├── Sprites/                  # Sprite image assets
├── platformio.ini           # PlatformIO configuration
└── README.md                # This file
```

## Installation

1. Clone this repository
2. Open the project in PlatformIO IDE
3. Install dependencies: `pio lib install`
4. Configure your display settings in `include/User_Setup.h`
5. Build and upload to your ESP32

## Configuration

### Display Configuration
Edit `include/User_Setup.h` to match your TFT display:
- Display driver type
- Pin connections
- Display resolution
- Color format

### LVGL Configuration
Edit `include/lv_conf.h` to customize LVGL settings:
- Memory allocation
- Feature enable/disable
- Performance settings

## Serial Commands

The ESP32 accepts various serial commands for control:

### Animation Control
- `SPEED:<value>` - Set typing speed (0-255)
- `STOP` - Stop typing animation
- `IDLE_START` - Enable idle progression
- `STREAK_ON/OFF` - Enable/disable streak mode

### System Stats
- `STATS:CPU:45,RAM:67,WPM:23` - Update system statistics
- `TIME:14:30` - Update time display
- `CPU:45`, `RAM:67`, `WPM:23` - Individual stat updates

### Display Settings
- `DISPLAY_CPU:ON/OFF` - Show/hide CPU display
- `DISPLAY_RAM:ON/OFF` - Show/hide RAM display
- `DISPLAY_WPM:ON/OFF` - Show/hide WPM display
- `DISPLAY_TIME:ON/OFF` - Show/hide time display
- `TIME_FORMAT:12/24` - Set time format

### Settings Management
- `SAVE_SETTINGS` - Save current settings to EEPROM
- `LOAD_SETTINGS` - Load settings from EEPROM
- `RESET_SETTINGS` - Reset to factory defaults

## Animation States

1. **IDLE_STAGE1**: Normal state with paws visible
2. **IDLE_STAGE2**: Paws hidden under table
3. **IDLE_STAGE3**: Sleepy face, preparing for sleep
4. **IDLE_STAGE4**: Deep sleep with cycling effects
5. **TYPING_SLOW**: Slow typing animation
6. **TYPING_NORMAL**: Normal typing animation
7. **TYPING_FAST**: Fast typing with click effects

## Python Integration

This ESP32 project is designed to work with the Python monitoring script. The Python script:
- Monitors keyboard activity and system stats
- Sends real-time updates via serial communication
- Controls animation states based on typing activity
- Provides configuration interface

## Troubleshooting

### Common Issues

1. **Display not working**: Check `User_Setup.h` configuration
2. **Compilation errors**: Ensure all libraries are installed
3. **Serial communication issues**: Verify baud rate (115200)
4. **Memory issues**: Adjust LVGL memory settings in `lv_conf.h`

### Debug Output

The ESP32 provides detailed debug output via Serial:
- Animation state changes
- Settings updates
- Error messages
- Performance metrics

## License

This project is part of the Bongo Cat Monitor system. See the main project README for license information.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the debug output
3. Check the main project documentation
4. Open an issue on GitHub
