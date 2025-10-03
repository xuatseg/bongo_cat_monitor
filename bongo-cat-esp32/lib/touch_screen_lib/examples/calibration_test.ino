/*
  TouchScreenLib Calibration Test
  
  This example helps you test and verify touch screen calibration.
  It shows:
  - Raw ADC values
  - Calibrated coordinates
  - Calibration data verification
  
  Hardware: ESP32 + TFT display with resistive touch
*/

#include "touch_screen_lib.h"
#include <TFT_eSPI.h>

TFT_eSPI tft = TFT_eSPI();
TouchScreenLib touchScreen(&tft);

void setup() {
  Serial.begin(115200);
  Serial.println("TouchScreenLib Calibration Test");
  
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
  
  // Set calibration data
  uint16_t calData[5] = { 328, 3443, 365, 3499, 3 };
  touchScreen.setCalibration(calData);
  
  // Enable debug output
  touchScreen.setDebugOutput(true);
  
  // Draw calibration test grid
  drawCalibrationGrid();
  
  Serial.println("Calibration Test Ready");
  Serial.println("Touch the corners and center to test calibration");
  Serial.println("Watch serial output for detailed information");
}

void loop() {
  uint16_t x, y, pressure;
  uint16_t rawX, rawY;
  
  // Get raw touch data
  touchScreen.getRawTouch(&rawX, &rawY);
  
  // Check for touch
  if (touchScreen.readTouch(&x, &y, &pressure)) {
    Serial.println("=== Calibration Test ===");
    Serial.print("Raw ADC: X=");
    Serial.print(rawX);
    Serial.print(", Y=");
    Serial.println(rawY);
    
    Serial.print("Calibrated: X=");
    Serial.print(x);
    Serial.print(", Y=");
    Serial.println(y);
    
    Serial.print("Screen bounds: 0-");
    Serial.print(touchScreen.getScreenWidth()-1);
    Serial.print(", 0-");
    Serial.println(touchScreen.getScreenHeight()-1);
    
    // Test corner accuracy
    if (x < 10 && y < 10) {
      Serial.println("✓ Top-left corner detected correctly");
    } else if (x > touchScreen.getScreenWidth()-10 && y < 10) {
      Serial.println("✓ Top-right corner detected correctly");
    } else if (x < 10 && y > touchScreen.getScreenHeight()-10) {
      Serial.println("✓ Bottom-left corner detected correctly");
    } else if (x > touchScreen.getScreenWidth()-10 && y > touchScreen.getScreenHeight()-10) {
      Serial.println("✓ Bottom-right corner detected correctly");
    } else if (x > touchScreen.getScreenWidth()/2-10 && x < touchScreen.getScreenWidth()/2+10 && 
               y > touchScreen.getScreenHeight()/2-10 && y < touchScreen.getScreenHeight()/2+10) {
      Serial.println("✓ Center area detected correctly");
    }
    
    Serial.println("========================");
    
    // Draw touch point
    tft.fillCircle(x, y, 5, TFT_WHITE);
    
    // Show coordinates on screen
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.setTextSize(1);
    tft.setCursor(10, 280);
    tft.print("X:");
    tft.print(x);
    tft.print(" Y:");
    tft.println(y);
  }
  
  delay(100);
}

void drawCalibrationGrid() {
  // Draw corner markers
  tft.fillCircle(10, 10, 8, TFT_RED);           // Top-left
  tft.fillCircle(230, 10, 8, TFT_GREEN);        // Top-right
  tft.fillCircle(10, 310, 8, TFT_BLUE);         // Bottom-left
  tft.fillCircle(230, 310, 8, TFT_YELLOW);      // Bottom-right
  
  // Draw center marker
  tft.fillCircle(120, 160, 8, TFT_CYAN);        // Center
  
  // Draw grid lines
  tft.setTextColor(TFT_WHITE, TFT_BLACK);
  tft.setTextSize(1);
  
  // Vertical lines
  for (int i = 0; i < touchScreen.getScreenWidth(); i += 40) {
    tft.drawLine(i, 0, i, touchScreen.getScreenHeight(), TFT_DARKGREY);
    if (i % 80 == 0) {
      tft.setCursor(i+2, 2);
      tft.print(i);
    }
  }
  
  // Horizontal lines
  for (int i = 0; i < touchScreen.getScreenHeight(); i += 40) {
    tft.drawLine(0, i, touchScreen.getScreenWidth(), i, TFT_DARKGREY);
    if (i % 80 == 0) {
      tft.setCursor(2, i+2);
      tft.print(i);
    }
  }
  
  // Add labels
  tft.setTextColor(TFT_RED, TFT_BLACK);
  tft.setCursor(20, 20);
  tft.println("TL");
  
  tft.setTextColor(TFT_GREEN, TFT_BLACK);
  tft.setCursor(200, 20);
  tft.println("TR");
  
  tft.setTextColor(TFT_BLUE, TFT_BLACK);
  tft.setCursor(20, 300);
  tft.println("BL");
  
  tft.setTextColor(TFT_YELLOW, TFT_BLACK);
  tft.setCursor(200, 300);
  tft.println("BR");
  
  tft.setTextColor(TFT_CYAN, TFT_BLACK);
  tft.setCursor(110, 150);
  tft.println("C");
}
