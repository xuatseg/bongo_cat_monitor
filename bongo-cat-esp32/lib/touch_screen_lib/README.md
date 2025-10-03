# TouchScreenLib

A simple and easy-to-use touch screen library for ESP32 with TFT_eSPI display.

## Features

- **Easy Integration**: Simple API for touch screen functionality
- **Calibration Support**: Built-in calibration data management
- **Debug Output**: Detailed touch detection information
- **TFT_eSPI Compatible**: Works seamlessly with TFT_eSPI library
- **Raw Touch Data**: Access to raw ADC values for debugging

## Installation

1. Copy the `touch_screen_lib` folder to your project's `lib` directory
2. Include the library in your `platformio.ini`:
   ```ini
   lib_extra_dirs = lib
   ```

## Quick Start

```cpp
#include "touch_screen_lib.h"
#include <TFT_eSPI.h>

TFT_eSPI tft = TFT_eSPI();
TouchScreenLib touchScreen(&tft);

void setup() {
    // Initialize display
    tft.init();
    tft.setRotation(0);
    
    // Initialize touch screen
    touchScreen.init();
    
    // Set calibration data (optional, uses default if not set)
    uint16_t calData[5] = { 328, 3443, 365, 3499, 3 };
    touchScreen.setCalibration(calData);
}

void loop() {
    uint16_t x, y, pressure;
    
    if (touchScreen.readTouch(&x, &y, &pressure)) {
        Serial.print("Touch: X=");
        Serial.print(x);
        Serial.print(", Y=");
        Serial.print(y);
        Serial.print(", Pressure=");
        Serial.println(pressure);
    }
}
```

## API Reference

### Constructor

```cpp
TouchScreenLib(TFT_eSPI* tft_instance)
```
Creates a new TouchScreenLib instance.

**Parameters:**
- `tft_instance`: Pointer to TFT_eSPI instance

### Methods

#### `bool init()`
Initializes the touch screen library.

**Returns:**
- `true` if initialization successful
- `false` if initialization failed

#### `bool readTouch(uint16_t* x, uint16_t* y)`
Reads touch coordinates.

**Parameters:**
- `x`: Pointer to store X coordinate (0-239)
- `y`: Pointer to store Y coordinate (0-319)

**Returns:**
- `true` if touch detected
- `false` if no touch

#### `bool readTouch(uint16_t* x, uint16_t* y, uint16_t* pressure)`
Reads touch coordinates with pressure value.

**Parameters:**
- `x`: Pointer to store X coordinate (0-239)
- `y`: Pointer to store Y coordinate (0-319)
- `pressure`: Pointer to store pressure value

**Returns:**
- `true` if touch detected
- `false` if no touch

#### `bool isTouched()`
Checks if screen is currently being touched.

**Returns:**
- `true` if screen is touched
- `false` if not touched

#### `void setCalibration(uint16_t calData[5])`
Sets touch screen calibration data.

**Parameters:**
- `calData`: Array of 5 calibration values
  - `calData[0]`: Top-left X ADC value
  - `calData[1]`: Top-right X ADC value
  - `calData[2]`: Top-left Y ADC value
  - `calData[3]`: Bottom-left Y ADC value
  - `calData[4]`: Rotation flag

#### `void getRawTouch(uint16_t* rawX, uint16_t* rawY)`
Gets raw touch ADC values for debugging.

**Parameters:**
- `rawX`: Pointer to store raw X ADC value
- `rawY`: Pointer to store raw Y ADC value

#### `void setDebugOutput(bool enable)`
Enables or disables debug output.

**Parameters:**
- `enable`: `true` to enable debug output, `false` to disable

#### `uint16_t getScreenWidth()`
Gets screen width.

**Returns:**
- Screen width in pixels (240)

#### `uint16_t getScreenHeight()`
Gets screen height.

**Returns:**
- Screen height in pixels (320)

## Calibration

The library comes with pre-calibrated data for 240x320 displays:
```cpp
uint16_t calData[5] = { 328, 3443, 365, 3499, 3 };
```

### Calibration Data Format

- **calData[0]**: Top-left corner X ADC value
- **calData[1]**: Top-right corner X ADC value  
- **calData[2]**: Top-left corner Y ADC value
- **calData[3]**: Bottom-left corner Y ADC value
- **calData[4]**: Rotation flag (0-3)

### Custom Calibration

To use your own calibration data:

```cpp
uint16_t myCalData[5] = { /* your values */ };
touchScreen.setCalibration(myCalData);
```

## Debug Output

When debug output is enabled, the library provides detailed information:

```
=== 触摸识别过程 ===
1. 原始ADC读取: X=1200, Y=800
2. 校准后坐标: X=120, Y=160
3. 屏幕范围: 240x320
==================
```

## Hardware Requirements

- ESP32 development board
- TFT display with resistive touch screen (240x320)
- TFT_eSPI library

## Dependencies

- TFT_eSPI library
- Arduino framework

## Example Projects

### Basic Touch Detection
```cpp
void loop() {
    if (touchScreen.isTouched()) {
        uint16_t x, y;
        if (touchScreen.readTouch(&x, &y)) {
            Serial.print("Touch at: ");
            Serial.print(x);
            Serial.print(", ");
            Serial.println(y);
        }
    }
    delay(10);
}
```

### Touch Event Handling
```cpp
void handleTouch() {
    uint16_t x, y, pressure;
    
    if (touchScreen.readTouch(&x, &y, &pressure)) {
        // Check touch regions
        if (x < 120 && y < 160) {
            Serial.println("Top-left area touched");
        } else if (x >= 120 && y < 160) {
            Serial.println("Top-right area touched");
        } else if (x < 120 && y >= 160) {
            Serial.println("Bottom-left area touched");
        } else {
            Serial.println("Bottom-right area touched");
        }
    }
}
```

## Troubleshooting

### Touch Not Working
1. Check hardware connections
2. Verify calibration data
3. Enable debug output to see raw ADC values
4. Ensure TFT_eSPI is properly configured

### Inaccurate Touch Coordinates
1. Recalibrate the touch screen
2. Check if calibration data is correct
3. Verify screen rotation settings

### No Debug Output
1. Call `touchScreen.setDebugOutput(true)`
2. Check Serial monitor baud rate (115200)

## License

This library is part of the Bongo Cat Monitor project.

## Version History

- **v1.0.0**: Initial release with basic touch functionality
