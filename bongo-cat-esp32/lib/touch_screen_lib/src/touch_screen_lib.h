#ifndef TOUCH_SCREEN_LIB_H
#define TOUCH_SCREEN_LIB_H

#include <Arduino.h>
#include <TFT_eSPI.h>

class TouchScreenLib {
public:
    // 构造函数
    TouchScreenLib(TFT_eSPI* tft_instance);
    
    // 初始化触摸屏
    bool init();
    
    // 读取触摸坐标
    bool readTouch(uint16_t* x, uint16_t* y);
    
    // 读取触摸坐标（带压力值）
    bool readTouch(uint16_t* x, uint16_t* y, uint16_t* pressure);
    
    // 检查是否有触摸
    bool isTouched();
    
    // 设置校准数据
    void setCalibration(uint16_t calData[5]);
    
    // 获取原始触摸数据（用于调试）
    void getRawTouch(uint16_t* rawX, uint16_t* rawY);
    
    // 启用/禁用调试输出
    void setDebugOutput(bool enable);
    
    // 获取屏幕尺寸
    uint16_t getScreenWidth() { return screenWidth; }
    uint16_t getScreenHeight() { return screenHeight; }

private:
    TFT_eSPI* tft;
    uint16_t screenWidth;
    uint16_t screenHeight;
    bool debugEnabled;
    uint16_t calData[5];
    bool calibrationSet;
    
    // 默认校准数据（从官方例子获取）
    static const uint16_t defaultCalData[5];
};

#endif // TOUCH_SCREEN_LIB_H
