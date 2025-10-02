# Bongo Cat Monitor Framework Documentation / Bongo Cat 监控框架文档

## English Version

### Overview

The Bongo Cat Monitor is an ESP32-based animated display system that shows a cute cat animation responding to typing activity, system statistics, and environmental sensors. The framework is built using LVGL for graphics rendering and supports real-time communication with Python scripts.

### Architecture

#### Core Components

1. **Display System (LVGL)**
   - TFT display rendering (240x320)
   - Canvas-based sprite animation
   - Real-time UI updates

2. **Animation System**
   - Multi-layer sprite management
   - State machine for animation control
   - Frame-based animation timing

3. **Serial Communication**
   - Bidirectional communication with Python scripts
   - Command parsing and response handling
   - Real-time data streaming

4. **Configuration Management**
   - EEPROM-based settings persistence
   - Runtime configuration updates
   - Settings validation and checksums

#### Data Structures

```cpp
// Main settings structure
struct BongoCatSettings {
    bool show_cpu = true;
    bool show_ram = true;
    bool show_wpm = true;
    bool show_time = true;
    bool time_format_24h = true;
    int sleep_timeout_minutes = 5;
    float animation_sensitivity = 1.0;
    uint32_t checksum = 0;
};

// Sprite manager for animation control
sprite_manager_t sprite_manager;
```

#### Animation States

- `ANIM_STATE_IDLE_STAGE1` - Normal idle (paws visible)
- `ANIM_STATE_IDLE_STAGE2` - Hands hidden under table
- `ANIM_STATE_IDLE_STAGE3` - Sleepy face preparation
- `ANIM_STATE_IDLE_STAGE4` - Deep sleep with effects
- `ANIM_STATE_TYPING_SLOW` - Slow typing animation
- `ANIM_STATE_TYPING_NORMAL` - Normal typing animation
- `ANIM_STATE_TYPING_FAST` - Fast typing with effects

#### Communication Protocol

**Commands from Python:**
- `SPEED:120` - Set typing speed
- `CPU:45` - Update CPU usage
- `RAM:67` - Update RAM usage
- `WPM:25` - Update typing speed
- `TIME:12:34` - Update time display
- `PING` - Connection test
- `STOP` - Stop animation
- `IDLE_START` - Enable idle progression

**Responses to Python:**
- `PONG` - Connection acknowledgment
- `🔄 Animation state: IDLE_STAGE1 → TYPING_FAST` - State changes
- `💾 Settings saved to EEPROM` - Configuration updates

### Key Functions

#### Initialization
```cpp
void setup() {
    // Initialize EEPROM, display, LVGL
    // Load settings from EEPROM
    // Initialize sprite manager
    // Create UI elements
}
```

#### Main Loop
```cpp
void loop() {
    handleSerialCommands();     // Process incoming commands
    sprite_manager_update();    // Update animations
    updateSystemStats();        // Update display
    lv_timer_handler();        // Handle LVGL events
}
```

#### Animation Control
```cpp
void sprite_manager_set_state(sprite_manager_t* manager, 
                             animation_state_t new_state, 
                             uint32_t current_time);
```

### Configuration Commands

| Command | Description | Example |
|---------|-------------|---------|
| `DISPLAY_CPU:ON/OFF` | Toggle CPU display | `DISPLAY_CPU:OFF` |
| `DISPLAY_RAM:ON/OFF` | Toggle RAM display | `DISPLAY_RAM:ON` |
| `DISPLAY_WPM:ON/OFF` | Toggle WPM display | `DISPLAY_WPM:OFF` |
| `DISPLAY_TIME:ON/OFF` | Toggle time display | `DISPLAY_TIME:ON` |
| `TIME_FORMAT:12/24` | Set time format | `TIME_FORMAT:12` |
| `SLEEP_TIMEOUT:5` | Set sleep timeout (1-60 min) | `SLEEP_TIMEOUT:10` |
| `SENSITIVITY:1.5` | Set animation sensitivity | `SENSITIVITY:2.0` |
| `SAVE_SETTINGS` | Save to EEPROM | `SAVE_SETTINGS` |
| `LOAD_SETTINGS` | Load from EEPROM | `LOAD_SETTINGS` |
| `RESET_SETTINGS` | Reset to defaults | `RESET_SETTINGS` |

---

## 中文版本

### 概述

Bongo Cat Monitor 是一个基于 ESP32 的动画显示系统，显示一只可爱的猫咪动画，响应打字活动、系统统计和环境传感器。该框架使用 LVGL 进行图形渲染，支持与 Python 脚本的实时通信。

### 架构

#### 核心组件

1. **显示系统 (LVGL)**
   - TFT 显示渲染 (240x320)
   - 基于画布的精灵动画
   - 实时 UI 更新

2. **动画系统**
   - 多层精灵管理
   - 动画控制状态机
   - 基于帧的动画时序

3. **串口通信**
   - 与 Python 脚本双向通信
   - 命令解析和响应处理
   - 实时数据流

4. **配置管理**
   - 基于 EEPROM 的设置持久化
   - 运行时配置更新
   - 设置验证和校验和

#### 数据结构

```cpp
// 主设置结构
struct BongoCatSettings {
    bool show_cpu = true;           // 显示CPU
    bool show_ram = true;           // 显示RAM
    bool show_wpm = true;           // 显示WPM
    bool show_time = true;          // 显示时间
    bool time_format_24h = true;    // 24小时制
    int sleep_timeout_minutes = 5;  // 睡眠超时(分钟)
    float animation_sensitivity = 1.0; // 动画敏感度
    uint32_t checksum = 0;          // 校验和
};

// 动画控制的精灵管理器
sprite_manager_t sprite_manager;
```

#### 动画状态

- `ANIM_STATE_IDLE_STAGE1` - 正常空闲 (爪子可见)
- `ANIM_STATE_IDLE_STAGE2` - 手隐藏在桌子下
- `ANIM_STATE_IDLE_STAGE3` - 困倦表情准备
- `ANIM_STATE_IDLE_STAGE4` - 深度睡眠带特效
- `ANIM_STATE_TYPING_SLOW` - 慢速打字动画
- `ANIM_STATE_TYPING_NORMAL` - 正常打字动画
- `ANIM_STATE_TYPING_FAST` - 快速打字带特效

#### 通信协议

**来自 Python 的命令:**
- `SPEED:120` - 设置打字速度
- `CPU:45` - 更新 CPU 使用率
- `RAM:67` - 更新 RAM 使用率
- `WPM:25` - 更新打字速度
- `TIME:12:34` - 更新时间显示
- `PING` - 连接测试
- `STOP` - 停止动画
- `IDLE_START` - 启用空闲进度

**发送给 Python 的响应:**
- `PONG` - 连接确认
- `🔄 Animation state: IDLE_STAGE1 → TYPING_FAST` - 状态变化
- `💾 Settings saved to EEPROM` - 配置更新

### 关键函数

#### 初始化
```cpp
void setup() {
    // 初始化 EEPROM、显示器、LVGL
    // 从 EEPROM 加载设置
    // 初始化精灵管理器
    // 创建 UI 元素
}
```

#### 主循环
```cpp
void loop() {
    handleSerialCommands();     // 处理传入命令
    sprite_manager_update();    // 更新动画
    updateSystemStats();        // 更新显示
    lv_timer_handler();        // 处理 LVGL 事件
}
```

#### 动画控制
```cpp
void sprite_manager_set_state(sprite_manager_t* manager, 
                             animation_state_t new_state, 
                             uint32_t current_time);
```

### 配置命令

| 命令 | 描述 | 示例 |
|------|------|------|
| `DISPLAY_CPU:ON/OFF` | 切换CPU显示 | `DISPLAY_CPU:OFF` |
| `DISPLAY_RAM:ON/OFF` | 切换RAM显示 | `DISPLAY_RAM:ON` |
| `DISPLAY_WPM:ON/OFF` | 切换WPM显示 | `DISPLAY_WPM:OFF` |
| `DISPLAY_TIME:ON/OFF` | 切换时间显示 | `DISPLAY_TIME:ON` |
| `TIME_FORMAT:12/24` | 设置时间格式 | `TIME_FORMAT:12` |
| `SLEEP_TIMEOUT:5` | 设置睡眠超时(1-60分钟) | `SLEEP_TIMEOUT:10` |
| `SENSITIVITY:1.5` | 设置动画敏感度 | `SENSITIVITY:2.0` |
| `SAVE_SETTINGS` | 保存到EEPROM | `SAVE_SETTINGS` |
| `LOAD_SETTINGS` | 从EEPROM加载 | `LOAD_SETTINGS` |
| `RESET_SETTINGS` | 重置为默认值 | `RESET_SETTINGS` |

---

## Development Guide / 开发指南

### Adding New Features / 添加新功能

1. **New Animation States / 新动画状态**
   - Add to `animation_state_t` enum
   - Implement in `sprite_manager_set_state()`
   - Update `get_state_name()` function

2. **New Serial Commands / 新串口命令**
   - Add parsing in `handleSerialCommands()`
   - Implement command logic
   - Add to documentation

3. **New Display Elements / 新显示元素**
   - Create LVGL objects in `createBongoCat()`
   - Add update functions
   - Update `updateDisplayVisibility()`

### Performance Considerations / 性能考虑

- **Frame Rate**: Limited to 40 FPS for smooth animation
- **Memory Usage**: Canvas buffer is 64x64 pixels (4KB)
- **Serial Buffer**: Commands processed immediately
- **EEPROM**: Settings saved with checksum validation

### Troubleshooting / 故障排除

- **Display Issues**: Check LVGL initialization and canvas buffer
- **Animation Problems**: Verify sprite manager state transitions
- **Serial Communication**: Ensure proper baud rate (115200)
- **Settings Corruption**: Use `RESET_SETTINGS` command

---

## File Structure / 文件结构

```
bongo_cat.ino                 # Main Arduino sketch / 主Arduino程序
├── Display System / 显示系统
│   ├── LVGL initialization / LVGL初始化
│   ├── Canvas rendering / 画布渲染
│   └── UI element management / UI元素管理
├── Animation System / 动画系统
│   ├── Sprite management / 精灵管理
│   ├── State machine / 状态机
│   └── Frame timing / 帧时序
├── Communication / 通信
│   ├── Serial command parsing / 串口命令解析
│   ├── Response handling / 响应处理
│   └── Data streaming / 数据流
└── Configuration / 配置
    ├── EEPROM storage / EEPROM存储
    ├── Settings validation / 设置验证
    └── Runtime updates / 运行时更新
```

---

*Last updated: October 2024 / 最后更新: 2024年10月*
