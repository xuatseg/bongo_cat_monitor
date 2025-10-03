# Changelog

All notable changes to TouchScreenLib will be documented in this file.

## [1.0.0] - 2024-10-02

### Added
- Initial release of TouchScreenLib
- Basic touch screen functionality with TFT_eSPI integration
- Calibration data management
- Debug output support
- Raw touch data access
- Simple API for touch detection
- Pre-calibrated data for 240x320 displays

### Features
- `TouchScreenLib(TFT_eSPI* tft_instance)` - Constructor
- `bool init()` - Initialize touch screen
- `bool readTouch(uint16_t* x, uint16_t* y)` - Read touch coordinates
- `bool readTouch(uint16_t* x, uint16_t* y, uint16_t* pressure)` - Read touch with pressure
- `bool isTouched()` - Check if screen is touched
- `void setCalibration(uint16_t calData[5])` - Set calibration data
- `void getRawTouch(uint16_t* rawX, uint16_t* rawY)` - Get raw ADC values
- `void setDebugOutput(bool enable)` - Enable/disable debug output
- `uint16_t getScreenWidth()` - Get screen width
- `uint16_t getScreenHeight()` - Get screen height

### Technical Details
- Compatible with TFT_eSPI library
- Supports 240x320 display resolution
- Uses resistive touch screen technology
- Includes detailed debug output in Chinese
- Pre-configured with tested calibration data: `{328, 3443, 365, 3499, 3}`
