/*
  TouchScreenLib Basic Example
  
  This example demonstrates basic touch screen functionality.
  It shows how to:
  - Initialize the touch screen
  - Read touch coordinates
  - Handle touch events
  
  Hardware: ESP32 + TFT display with resistive touch
*/

#include "touch_screen_lib.h"
#include <TFT_eSPI.h>

TFT_eSPI tft = TFT_eSPI();
TouchScreenLib touchScreen(&tft);

void setup() {
  Serial.begin(115200);
  Serial.println("TouchScreenLib Basic Example");
  
  // Initialize display
  tft.init();
  tft.setRotation(0);
  tft.fillScreen(TFT_BLACK);
  
  // Initialize touch screen
  if (touchScreen.init()) {
    Serial.println("Touch screen initialized successfully!");
  } else {
    Serial.println("Touch screen initialization failed!");
    return;
  }
  
  // Set calibration data (optional, uses default if not set)
  uint16_t calData[5] = { 328, 3443, 365, 3499, 3 };
  touchScreen.setCalibration(calData);
  
  // Enable debug output
  touchScreen.setDebugOutput(true);
  
  // Draw some test elements
  tft.setTextColor(TFT_WHITE, TFT_BLACK);
  tft.setTextSize(2);
  tft.setCursor(10, 10);
  tft.println("Touch Test");
  tft.setCursor(10, 40);
  tft.println("Touch the screen");
  tft.setCursor(10, 70);
  tft.println("Check serial output");
  
  // Draw touch areas
  tft.fillRect(20, 100, 80, 40, TFT_RED);
  tft.setTextColor(TFT_WHITE, TFT_RED);
  tft.setCursor(35, 115);
  tft.println("Area 1");
  
  tft.fillRect(140, 100, 80, 40, TFT_GREEN);
  tft.setTextColor(TFT_WHITE, TFT_GREEN);
  tft.setCursor(155, 115);
  tft.println("Area 2");
  
  tft.fillRect(20, 160, 80, 40, TFT_BLUE);
  tft.setTextColor(TFT_WHITE, TFT_BLUE);
  tft.setCursor(35, 175);
  tft.println("Area 3");
  
  tft.fillRect(140, 160, 80, 40, TFT_YELLOW);
  tft.setTextColor(TFT_BLACK, TFT_YELLOW);
  tft.setCursor(155, 175);
  tft.println("Area 4");
}

void loop() {
  uint16_t x, y, pressure;
  
  // Check for touch
  if (touchScreen.readTouch(&x, &y, &pressure)) {
    Serial.print("Touch detected: X=");
    Serial.print(x);
    Serial.print(", Y=");
    Serial.print(y);
    Serial.print(", Pressure=");
    Serial.println(pressure);
    
    // Check which area was touched
    if (x >= 20 && x <= 100 && y >= 100 && y <= 140) {
      Serial.println("Area 1 (Red) touched!");
      tft.fillCircle(x, y, 5, TFT_WHITE);
    } else if (x >= 140 && x <= 220 && y >= 100 && y <= 140) {
      Serial.println("Area 2 (Green) touched!");
      tft.fillCircle(x, y, 5, TFT_WHITE);
    } else if (x >= 20 && x <= 100 && y >= 160 && y <= 200) {
      Serial.println("Area 3 (Blue) touched!");
      tft.fillCircle(x, y, 5, TFT_WHITE);
    } else if (x >= 140 && x <= 220 && y >= 160 && y <= 200) {
      Serial.println("Area 4 (Yellow) touched!");
      tft.fillCircle(x, y, 5, TFT_WHITE);
    } else {
      Serial.println("Touch outside defined areas");
      tft.fillCircle(x, y, 3, TFT_CYAN);
    }
    
    // Show coordinates on screen
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.setTextSize(1);
    tft.setCursor(10, 220);
    tft.print("Last touch: ");
    tft.print(x);
    tft.print(", ");
    tft.println(y);
  }
  
  delay(50);
}
