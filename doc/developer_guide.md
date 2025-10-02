# Bongo Cat Monitor Developer Guide / Bongo Cat 监控开发者指南

## English Version

### Quick Start / 快速开始

#### Prerequisites / 前置条件
- Arduino IDE 2.0+
- ESP32 board support package
- TFT_eSPI library
- LVGL library
- Python 3.7+ (for testing scripts)

#### Hardware Setup / 硬件设置
1. **ESP32 Development Board** - Any ESP32 variant
2. **TFT Display** - 240x320 resolution, SPI interface
3. **USB Cable** - For programming and serial communication

#### Software Installation / 软件安装

1. **Install Arduino IDE**
   ```bash
   # Download from https://www.arduino.cc/en/software
   ```

2. **Install ESP32 Board Package**
   - Open Arduino IDE
   - Go to File → Preferences
   - Add to Additional Board Manager URLs:
     ```
     https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
     ```
   - Go to Tools → Board → Boards Manager
   - Search for "ESP32" and install

3. **Install Required Libraries**
   ```bash
   # In Arduino IDE Library Manager, install:
   - TFT_eSPI
   - LVGL
   ```

4. **Install Python Dependencies**
   ```bash
   cd python_scripts
   python3 install_requirements.py
   ```

#### Configuration / 配置

1. **TFT_eSPI Configuration**
   - Edit `User_Setup.h` in TFT_eSPI library
   - Uncomment your display configuration
   - Set correct pin definitions

2. **LVGL Configuration**
   - Edit `lv_conf.h` in project root
   - Enable required features
   - Adjust memory settings

3. **ESP32 Configuration**
   - Select board: ESP32 Dev Module
   - Set partition scheme: Huge APP (3MB No OTA/1MB SPIFFS)
   - Set CPU frequency: 240MHz
   - Set Flash size: 4MB

#### Building and Uploading / 编译和上传

1. **Open the Project**
   - Open `bongo_cat.ino` in Arduino IDE

2. **Configure Settings**
   - Adjust pin definitions in `User_Setup.h`
   - Modify display settings if needed

3. **Upload to ESP32**
   - Select correct COM port
   - Click Upload button
   - Wait for upload to complete

4. **Test Connection**
   ```bash
   cd python_scripts
   python3 simple_test.py
   ```

### Development Workflow / 开发工作流

#### Adding New Features / 添加新功能

1. **New Animation States**
   ```cpp
   // 1. Add to animation_state_t enum
   typedef enum {
       // ... existing states
       ANIM_STATE_NEW_FEATURE
   } animation_state_t;
   
   // 2. Implement in sprite_manager_set_state()
   case ANIM_STATE_NEW_FEATURE:
       // Set appropriate sprites
       break;
   
   // 3. Update get_state_name()
   case ANIM_STATE_NEW_FEATURE: return "NEW_FEATURE";
   ```

2. **New Serial Commands**
   ```cpp
   // Add to handleSerialCommands()
   else if (command.startsWith("NEW_CMD:")) {
       String value = command.substring(8);
       // Process command
       Serial.println("✅ New command processed");
   }
   ```

3. **New Display Elements**
   ```cpp
   // 1. Add global variable
   lv_obj_t * new_element = NULL;
   
   // 2. Create in createBongoCat()
   new_element = lv_label_create(screen);
   lv_label_set_text(new_element, "New Element");
   
   // 3. Update in updateDisplayVisibility()
   if (new_element) {
       // Show/hide logic
   }
   ```

#### Debugging / 调试

1. **Serial Monitor**
   - Open Arduino IDE Serial Monitor
   - Set baud rate to 115200
   - Monitor debug messages

2. **Python Testing**
   ```bash
   # Test basic functionality
   python3 simple_test.py
   
   # Test all features
   python3 direct_test.py
   
   # Debug port issues
   python3 find_ports.py
   ```

3. **Common Issues**
   - **Display not working**: Check TFT_eSPI configuration
   - **Animation stuck**: Verify sprite manager state
   - **Serial not responding**: Check baud rate and connections
   - **Memory issues**: Adjust LVGL memory settings

### Performance Optimization / 性能优化

#### Memory Management / 内存管理
- Canvas buffer: 64x64 pixels (4KB)
- LVGL buffer: 240x10 pixels (4.8KB)
- EEPROM usage: 512 bytes
- Total RAM usage: ~200KB

#### Frame Rate Optimization / 帧率优化
- Target: 40 FPS
- Animation update: 25ms intervals
- LVGL timer: 20ms intervals
- Serial processing: Immediate

#### Power Management / 电源管理
- CPU frequency: 240MHz
- Sleep modes: Not implemented
- Power consumption: ~200mA

---

## 中文版本

### 快速开始

#### 前置条件
- Arduino IDE 2.0+
- ESP32 开发板支持包
- TFT_eSPI 库
- LVGL 库
- Python 3.7+ (用于测试脚本)

#### 硬件设置
1. **ESP32 开发板** - 任何 ESP32 变体
2. **TFT 显示屏** - 240x320 分辨率，SPI 接口
3. **USB 数据线** - 用于编程和串口通信

#### 软件安装

1. **安装 Arduino IDE**
   ```bash
   # 从 https://www.arduino.cc/en/software 下载
   ```

2. **安装 ESP32 开发板包**
   - 打开 Arduino IDE
   - 转到 文件 → 首选项
   - 在附加开发板管理器网址中添加：
     ```
     https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
     ```
   - 转到 工具 → 开发板 → 开发板管理器
   - 搜索 "ESP32" 并安装

3. **安装必需的库**
   ```bash
   # 在 Arduino IDE 库管理器中安装：
   - TFT_eSPI
   - LVGL
   ```

4. **安装 Python 依赖**
   ```bash
   cd python_scripts
   python3 install_requirements.py
   ```

#### 配置

1. **TFT_eSPI 配置**
   - 编辑 TFT_eSPI 库中的 `User_Setup.h`
   - 取消注释你的显示器配置
   - 设置正确的引脚定义

2. **LVGL 配置**
   - 编辑项目根目录的 `lv_conf.h`
   - 启用所需功能
   - 调整内存设置

3. **ESP32 配置**
   - 选择开发板：ESP32 Dev Module
   - 设置分区方案：Huge APP (3MB No OTA/1MB SPIFFS)
   - 设置 CPU 频率：240MHz
   - 设置 Flash 大小：4MB

#### 编译和上传

1. **打开项目**
   - 在 Arduino IDE 中打开 `bongo_cat.ino`

2. **配置设置**
   - 在 `User_Setup.h` 中调整引脚定义
   - 根据需要修改显示设置

3. **上传到 ESP32**
   - 选择正确的 COM 端口
   - 点击上传按钮
   - 等待上传完成

4. **测试连接**
   ```bash
   cd python_scripts
   python3 simple_test.py
   ```

### 开发工作流

#### 添加新功能

1. **新动画状态**
   ```cpp
   // 1. 添加到 animation_state_t 枚举
   typedef enum {
       // ... 现有状态
       ANIM_STATE_NEW_FEATURE
   } animation_state_t;
   
   // 2. 在 sprite_manager_set_state() 中实现
   case ANIM_STATE_NEW_FEATURE:
       // 设置适当的精灵
       break;
   
   // 3. 更新 get_state_name()
   case ANIM_STATE_NEW_FEATURE: return "NEW_FEATURE";
   ```

2. **新串口命令**
   ```cpp
   // 添加到 handleSerialCommands()
   else if (command.startsWith("NEW_CMD:")) {
       String value = command.substring(8);
       // 处理命令
       Serial.println("✅ New command processed");
   }
   ```

3. **新显示元素**
   ```cpp
   // 1. 添加全局变量
   lv_obj_t * new_element = NULL;
   
   // 2. 在 createBongoCat() 中创建
   new_element = lv_label_create(screen);
   lv_label_set_text(new_element, "New Element");
   
   // 3. 在 updateDisplayVisibility() 中更新
   if (new_element) {
       // 显示/隐藏逻辑
   }
   ```

#### 调试

1. **串口监视器**
   - 打开 Arduino IDE 串口监视器
   - 设置波特率为 115200
   - 监控调试消息

2. **Python 测试**
   ```bash
   # 测试基本功能
   python3 simple_test.py
   
   # 测试所有功能
   python3 direct_test.py
   
   # 调试端口问题
   python3 find_ports.py
   ```

3. **常见问题**
   - **显示器不工作**：检查 TFT_eSPI 配置
   - **动画卡住**：验证精灵管理器状态
   - **串口无响应**：检查波特率和连接
   - **内存问题**：调整 LVGL 内存设置

### 性能优化

#### 内存管理
- 画布缓冲区：64x64 像素 (4KB)
- LVGL 缓冲区：240x10 像素 (4.8KB)
- EEPROM 使用：512 字节
- 总 RAM 使用：约 200KB

#### 帧率优化
- 目标：40 FPS
- 动画更新：25ms 间隔
- LVGL 定时器：20ms 间隔
- 串口处理：立即

#### 电源管理
- CPU 频率：240MHz
- 睡眠模式：未实现
- 功耗：约 200mA

---

## Project Structure / 项目结构

```
bongo_cat_monitor/
├── bongo_cat.ino              # Main Arduino sketch / 主Arduino程序
├── animations_sprites.h        # Sprite definitions / 精灵定义
├── Free_Fonts.h               # Font definitions / 字体定义
├── lv_conf.h                  # LVGL configuration / LVGL配置
├── User_Setup.h               # TFT_eSPI configuration / TFT_eSPI配置
├── python_scripts/            # Python testing tools / Python测试工具
│   ├── README.md
│   ├── install_requirements.py
│   ├── find_ports.py
│   ├── simple_test.py
│   └── direct_test.py
├── doc/                       # Documentation / 文档
│   ├── bongo_cat_framework.md
│   ├── api_reference.md
│   └── developer_guide.md
├── Sprites/                   # Sprite images / 精灵图像
├── animations/                # Animation source files / 动画源文件
└── 3d_printing/              # 3D printing files / 3D打印文件
```

---

*Last updated: October 2024 / 最后更新: 2024年10月*
