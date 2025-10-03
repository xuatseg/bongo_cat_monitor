#include "touch_screen_lib.h"

// 默认校准数据（从官方例子获取）
const uint16_t TouchScreenLib::defaultCalData[5] = { 328, 3443, 365, 3499, 3 };

TouchScreenLib::TouchScreenLib(TFT_eSPI* tft_instance) {
    tft = tft_instance;
    screenWidth = 240;
    screenHeight = 320;
    debugEnabled = true;
    calibrationSet = false;
    
    // 复制默认校准数据
    for (int i = 0; i < 5; i++) {
        calData[i] = defaultCalData[i];
    }
}

bool TouchScreenLib::init() {
    if (debugEnabled) {
        Serial.println("🔘 Initializing touch screen library...");
    }
    
    // 设置触摸屏校准数据
    tft->setTouch(calData);
    calibrationSet = true;
    
    if (debugEnabled) {
        Serial.println("✅ Touch screen library initialized");
        Serial.print("🔘 Screen size: ");
        Serial.print(screenWidth);
        Serial.print("x");
        Serial.println(screenHeight);
        Serial.print("🔘 Calibration data: {");
        for (int i = 0; i < 5; i++) {
            Serial.print(calData[i]);
            if (i < 4) Serial.print(", ");
        }
        Serial.println("}");
    }
    
    return true;
}

bool TouchScreenLib::readTouch(uint16_t* x, uint16_t* y) {
    uint16_t pressure;
    return readTouch(x, y, &pressure);
}

bool TouchScreenLib::readTouch(uint16_t* x, uint16_t* y, uint16_t* pressure) {
    if (!calibrationSet) {
        if (debugEnabled) {
            Serial.println("❌ Touch screen not calibrated!");
        }
        return false;
    }
    
    uint16_t rawX, rawY;
    bool touched = tft->getTouch(&rawX, &rawY, 600);
    
    if (touched) {
        // 获取原始数据用于调试
        if (debugEnabled) {
            Serial.println("=== 触摸识别过程 ===");
            Serial.print("1. 原始ADC读取: X=");
            Serial.print(rawX);
            Serial.print(", Y=");
            Serial.println(rawY);
        }
        
        // 应用校准数据
        *x = constrain(rawX, 0, screenWidth - 1);
        *y = constrain(rawY, 0, screenHeight - 1);
        *pressure = 600; // TFT_eSPI的getTouch函数不返回压力值，使用固定值
        
        if (debugEnabled) {
            Serial.print("2. 校准后坐标: X=");
            Serial.print(*x);
            Serial.print(", Y=");
            Serial.println(*y);
            Serial.print("3. 屏幕范围: ");
            Serial.print(screenWidth);
            Serial.print("x");
            Serial.println(screenHeight);
            Serial.println("==================");
        }
        
        return true;
    }
    
    return false;
}

bool TouchScreenLib::isTouched() {
    uint16_t x, y;
    return tft->getTouch(&x, &y, 600);
}

void TouchScreenLib::setCalibration(uint16_t newCalData[5]) {
    for (int i = 0; i < 5; i++) {
        calData[i] = newCalData[i];
    }
    tft->setTouch(calData);
    calibrationSet = true;
    
    if (debugEnabled) {
        Serial.println("🔘 Touch calibration updated");
        Serial.print("🔘 New calibration data: {");
        for (int i = 0; i < 5; i++) {
            Serial.print(calData[i]);
            if (i < 4) Serial.print(", ");
        }
        Serial.println("}");
    }
}

void TouchScreenLib::getRawTouch(uint16_t* rawX, uint16_t* rawY) {
    tft->getTouch(rawX, rawY, 600);
}

void TouchScreenLib::setDebugOutput(bool enable) {
    debugEnabled = enable;
    if (debugEnabled) {
        Serial.println("🔘 Touch screen debug output enabled");
    } else {
        Serial.println("🔘 Touch screen debug output disabled");
    }
}
