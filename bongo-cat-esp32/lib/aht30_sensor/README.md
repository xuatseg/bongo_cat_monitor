# AHT30 Temperature and Humidity Sensor Library

这是一个用于ESP32的AHT30温湿度传感器库。

## 硬件连接

- **I2C地址**: 0x38
- **SCL引脚**: GPIO22
- **SDA引脚**: GPIO21
- **VCC**: 3.3V
- **GND**: 地线

## 初始化流程

AHT30的正确初始化流程（与AHT10不同）：

1. 上电延时 20ms
2. 发送软复位命令 0xBA
3. 延时 20ms
4. **加载校准数据：发送 0xBE 0x08 0x00** (重要！)
5. 延时 10ms
6. **检查校准状态：读取状态寄存器 0x71，检查bit 3** (确保校准成功)
7. 触发测量：发送 0xAC 0x33 0x00
8. 等待 80ms 测量完成
9. 读取 6 字节数据

**注意**: 
- AHT30不需要像AHT10那样发送0xE1初始化命令！
- 0xBE命令用于加载校准数据，这对AHT30很重要

## 使用示例

### 基本使用

```cpp
#include "AHT30.h"

// 创建AHT30对象 (SDA=21, SCL=22)
AHT30 aht30(21, 22);

void setup() {
    Serial.begin(115200);
    
    // 初始化传感器（会自动加载校准数据和应用默认校准参数）
    if (aht30.begin()) {
        Serial.println("AHT30初始化成功!");
    } else {
        Serial.println("AHT30初始化失败!");
    }
}

void loop() {
    float temperature, humidity;
    
    // 读取温湿度（已自动应用校准）
    if (aht30.readTemperatureAndHumidity(&temperature, &humidity)) {
        Serial.print("温度: ");
        Serial.print(temperature, 1);
        Serial.print("°C, 湿度: ");
        Serial.print(humidity, 1);
        Serial.println("%");
    }
    
    delay(2000);
}
```

### 自定义校准参数

如果默认校准参数不适合你的传感器，可以自定义：

```cpp
#include "AHT30.h"

AHT30 aht30(21, 22);

void setup() {
    Serial.begin(115200);
    
    if (aht30.begin()) {
        // 设置自定义校准参数
        // 例如：如果你的传感器温度高5度，湿度低15%
        aht30.setCalibration(
            -5.0,   // 温度偏移 (°C) - 传感器偏高则用负值
            1.0,    // 湿度缩放系数 - 通常保持1.0
            15.0    // 湿度偏移 (%) - 传感器偏低则用正值
        );
        
        // 也可以禁用校准（使用原始数据）
        // aht30.enableCalibration(false);
    }
}

void loop() {
    float temperature, humidity;
    
    if (aht30.readTemperatureAndHumidity(&temperature, &humidity)) {
        Serial.printf("Temperature: %.2f°C, Humidity: %.2f%%\n", 
                      temperature, humidity);
    }
    
    delay(2000);
}
```

## API参考

### 构造函数
```cpp
AHT30(uint8_t sda_pin = 21, uint8_t scl_pin = 22)
```

### 方法

**基本方法**
- `bool begin()` - 初始化传感器（包括加载校准数据）
- `bool isConnected()` - 检查传感器是否连接
- `bool readTemperatureAndHumidity(float* temperature, float* humidity)` - 读取温度和湿度
- `bool readTemperature(float* temperature)` - 仅读取温度
- `bool readHumidity(float* humidity)` - 仅读取湿度
- `void softReset()` - 软复位传感器

**校准方法**
- `void setCalibration(float tempOffset, float humiScale, float humiOffset)` - 设置校准参数
- `void enableCalibration(bool enable)` - 启用/禁用校准
- `bool isCalibrationEnabled()` - 检查校准是否启用

**获取数据方法**
- `float getLastTemperature()` - 获取上次读取的温度
- `float getLastHumidity()` - 获取上次读取的湿度
- `bool getLastReadSuccess()` - 获取上次读取是否成功

## 测量范围

- **温度**: -40°C ~ +85°C
- **湿度**: 0% ~ 100% RH
- **精度**: ±0.3°C (温度), ±2% RH (湿度)

## 重要注意事项

### 测量频率限制
- **推荐测量间隔**: 15秒或更长
- **原因**: 连续测量会导致芯片自热2-5°C
- **库默认**: 15秒间隔，避免自热影响

### 数据解析精度
- 使用正确的位操作确保数据解析准确
- 错误的位移操作会导致温度偏差数度
- 库已使用经过验证的解析算法

## 校准说明

### 默认校准参数

库默认使用以下校准参数（已启用）：
- 温度偏移: **-7.0°C** (传感器读数偏高7度)
- 湿度缩放: **1.0** (不缩放)
- 湿度偏移: **+20.0%** (传感器读数偏低20%)

这些参数是根据实际高精度传感器对比测试得出的。

### 如何调整校准参数

1. 准备一个高精度温湿度计作为参考
2. 禁用校准查看原始数据：`aht30.enableCalibration(false);`
3. 同时读取AHT30和标准温湿度计的数值
4. 计算差值并调整校准参数：
   - `tempOffset` = 标准温度 - AHT30原始温度
   - `humiOffset` = 标准湿度 - AHT30原始湿度
   - `humiScale` = 标准湿度 / AHT30原始湿度（通常保持1.0）

5. 使用 `setCalibration()` 方法应用新的校准参数
6. 重新启用校准：`aht30.enableCalibration(true);`

**示例：**
- 如果AHT30显示 35°C，标准温度计显示 28°C
  - 温度偏移 = 28 - 35 = **-7.0°C**
- 如果AHT30显示 35%，标准湿度计显示 55%
  - 湿度偏移 = 55 - 35 = **+20.0%**

### 禁用校准

如果你想使用原始数据，可以禁用校准：
```cpp
aht30.enableCalibration(false);
```

## 故障排除

如果初始化失败，请检查：

1. 硬件连接是否正确
2. I2C地址是否为0x38
3. 传感器是否有足够的上电延时
4. SCL和SDA引脚是否正确配置
5. 是否成功加载了校准数据（0xBE命令）
6. **校准状态位是否正确设置（状态寄存器bit 3）**

如果看到 "⚠️ AHT30: Sensor not calibrated!" 错误：
- 尝试重新发送 0xBE 0x08 0x00 命令
- 增加延时时间
- 检查传感器是否正常工作

如果读数不准确：

1. 检查是否已启用校准
2. 尝试调整校准参数
3. 确保传感器在稳定的环境中测量
4. 等待传感器稳定（通常需要几分钟）

## 版本历史

- v1.0.1 - 添加校准功能和0xBE命令支持
- v1.0.0 - 初始版本，支持AHT30传感器的基本功能
