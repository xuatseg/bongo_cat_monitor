# Bongo Cat Monitor API Reference / Bongo Cat 监控 API 参考

## English Version

### Serial Communication API

#### Command Format
All commands are sent as ASCII strings terminated with `\n` (newline character).

#### System Commands

| Command | Description | Parameters | Response |
|---------|-------------|------------|----------|
| `PING` | Test connection | None | `PONG` |
| `PONG` | Connection acknowledgment | None | None |

#### Data Update Commands

| Command | Description | Parameters | Example |
|---------|-------------|------------|---------|
| `CPU:<value>` | Update CPU usage | 0-100 | `CPU:45` |
| `RAM:<value>` | Update RAM usage | 0-100 | `RAM:67` |
| `WPM:<value>` | Update typing speed | 0-999 | `WPM:25` |
| `TIME:<time>` | Update time display | HH:MM | `TIME:12:34` |
| `STATS:CPU:<cpu>,RAM:<ram>,WPM:<wpm>` | Bulk stats update | Multiple values | `STATS:CPU:45,RAM:67,WPM:25` |

#### Animation Commands

| Command | Description | Parameters | Example |
|---------|-------------|------------|---------|
| `SPEED:<speed>` | Set typing animation speed | 0-999 | `SPEED:120` |
| `STOP` | Stop current animation | None | None |
| `IDLE` | Enter idle state | None | `PONG` |
| `IDLE_START` | Enable idle progression | None | None |
| `HEARTBEAT` | Keep connection alive | None | None |

#### Animation State Commands

| Command | Description | Parameters | Example |
|---------|-------------|------------|---------|
| `ANIM:IDLE_1` | Set to idle stage 1 | None | `PONG` |
| `ANIM:IDLE_2` | Set to idle stage 2 | None | `PONG` |
| `ANIM:IDLE_3` | Set to idle stage 3 | None | `PONG` |
| `ANIM:IDLE_4` | Set to idle stage 4 | None | `PONG` |
| `ANIM:BLINK` | Trigger blink animation | None | `PONG` |
| `ANIM:EAR_TWITCH` | Trigger ear twitch | None | `PONG` |

#### Display Configuration Commands

| Command | Description | Parameters | Example |
|---------|-------------|------------|---------|
| `DISPLAY_CPU:ON/OFF` | Toggle CPU display | ON/OFF | `DISPLAY_CPU:OFF` |
| `DISPLAY_RAM:ON/OFF` | Toggle RAM display | ON/OFF | `DISPLAY_RAM:ON` |
| `DISPLAY_WPM:ON/OFF` | Toggle WPM display | ON/OFF | `DISPLAY_WPM:OFF` |
| `DISPLAY_TIME:ON/OFF` | Toggle time display | ON/OFF | `DISPLAY_TIME:ON` |
| `TIME_FORMAT:12/24` | Set time format | 12/24 | `TIME_FORMAT:12` |

#### Settings Commands

| Command | Description | Parameters | Example |
|---------|-------------|------------|---------|
| `SLEEP_TIMEOUT:<minutes>` | Set sleep timeout | 1-60 | `SLEEP_TIMEOUT:10` |
| `SENSITIVITY:<value>` | Set animation sensitivity | 0.1-5.0 | `SENSITIVITY:1.5` |
| `SAVE_SETTINGS` | Save settings to EEPROM | None | None |
| `LOAD_SETTINGS` | Load settings from EEPROM | None | None |
| `RESET_SETTINGS` | Reset to factory defaults | None | None |

### Response Messages

#### Status Messages
- `🔄 Animation state: <old> → <new>` - Animation state change
- `💾 Settings saved to EEPROM` - Settings saved successfully
- `📂 Settings loaded from EEPROM` - Settings loaded successfully
- `⚠️ Invalid settings in EEPROM, using defaults` - Settings validation failed
- `🔄 Settings reset to factory defaults` - Settings reset

#### Error Messages
- `❌ Invalid sleep timeout (1-60 minutes)` - Invalid timeout value
- `❌ Invalid sensitivity (0.1-5.0)` - Invalid sensitivity value

#### Debug Messages
- `🖥️ CPU visibility updated: ON/OFF` - CPU display toggle
- `💾 RAM visibility updated: ON/OFF` - RAM display toggle
- `⌨️ WPM visibility updated: ON/OFF` - WPM display toggle
- `🕐 Time visibility updated: ON/OFF` - Time display toggle
- `🕐 Time format: 12/24 hour` - Time format change

---

## 中文版本

### 串口通信 API

#### 命令格式
所有命令都以 ASCII 字符串形式发送，以 `\n`（换行符）结尾。

#### 系统命令

| 命令 | 描述 | 参数 | 响应 |
|------|------|------|------|
| `PING` | 测试连接 | 无 | `PONG` |
| `PONG` | 连接确认 | 无 | 无 |

#### 数据更新命令

| 命令 | 描述 | 参数 | 示例 |
|------|------|------|------|
| `CPU:<value>` | 更新CPU使用率 | 0-100 | `CPU:45` |
| `RAM:<value>` | 更新RAM使用率 | 0-100 | `RAM:67` |
| `WPM:<value>` | 更新打字速度 | 0-999 | `WPM:25` |
| `TIME:<time>` | 更新时间显示 | HH:MM | `TIME:12:34` |
| `STATS:CPU:<cpu>,RAM:<ram>,WPM:<wpm>` | 批量统计更新 | 多个值 | `STATS:CPU:45,RAM:67,WPM:25` |

#### 动画命令

| 命令 | 描述 | 参数 | 示例 |
|------|------|------|------|
| `SPEED:<speed>` | 设置打字动画速度 | 0-999 | `SPEED:120` |
| `STOP` | 停止当前动画 | 无 | 无 |
| `IDLE` | 进入空闲状态 | 无 | `PONG` |
| `IDLE_START` | 启用空闲进度 | 无 | 无 |
| `HEARTBEAT` | 保持连接活跃 | 无 | 无 |

#### 动画状态命令

| 命令 | 描述 | 参数 | 示例 |
|------|------|------|------|
| `ANIM:IDLE_1` | 设置为空闲阶段1 | 无 | `PONG` |
| `ANIM:IDLE_2` | 设置为空闲阶段2 | 无 | `PONG` |
| `ANIM:IDLE_3` | 设置为空闲阶段3 | 无 | `PONG` |
| `ANIM:IDLE_4` | 设置为空闲阶段4 | 无 | `PONG` |
| `ANIM:BLINK` | 触发眨眼动画 | 无 | `PONG` |
| `ANIM:EAR_TWITCH` | 触发耳朵抽动 | 无 | `PONG` |

#### 显示配置命令

| 命令 | 描述 | 参数 | 示例 |
|------|------|------|------|
| `DISPLAY_CPU:ON/OFF` | 切换CPU显示 | ON/OFF | `DISPLAY_CPU:OFF` |
| `DISPLAY_RAM:ON/OFF` | 切换RAM显示 | ON/OFF | `DISPLAY_RAM:ON` |
| `DISPLAY_WPM:ON/OFF` | 切换WPM显示 | ON/OFF | `DISPLAY_WPM:OFF` |
| `DISPLAY_TIME:ON/OFF` | 切换时间显示 | ON/OFF | `DISPLAY_TIME:ON` |
| `TIME_FORMAT:12/24` | 设置时间格式 | 12/24 | `TIME_FORMAT:12` |

#### 设置命令

| 命令 | 描述 | 参数 | 示例 |
|------|------|------|------|
| `SLEEP_TIMEOUT:<minutes>` | 设置睡眠超时 | 1-60 | `SLEEP_TIMEOUT:10` |
| `SENSITIVITY:<value>` | 设置动画敏感度 | 0.1-5.0 | `SENSITIVITY:1.5` |
| `SAVE_SETTINGS` | 保存设置到EEPROM | 无 | 无 |
| `LOAD_SETTINGS` | 从EEPROM加载设置 | 无 | 无 |
| `RESET_SETTINGS` | 重置为出厂默认值 | 无 | 无 |

### 响应消息

#### 状态消息
- `🔄 Animation state: <old> → <new>` - 动画状态变化
- `💾 Settings saved to EEPROM` - 设置保存成功
- `📂 Settings loaded from EEPROM` - 设置加载成功
- `⚠️ Invalid settings in EEPROM, using defaults` - 设置验证失败
- `🔄 Settings reset to factory defaults` - 设置重置

#### 错误消息
- `❌ Invalid sleep timeout (1-60 minutes)` - 无效的超时值
- `❌ Invalid sensitivity (0.1-5.0)` - 无效的敏感度值

#### 调试消息
- `🖥️ CPU visibility updated: ON/OFF` - CPU显示切换
- `💾 RAM visibility updated: ON/OFF` - RAM显示切换
- `⌨️ WPM visibility updated: ON/OFF` - WPM显示切换
- `🕐 Time visibility updated: ON/OFF` - 时间显示切换
- `🕐 Time format: 12/24 hour` - 时间格式变化

---

## Code Examples / 代码示例

### Python Integration / Python 集成

```python
import serial
import time

# Connect to ESP32
ser = serial.Serial('COM3', 115200, timeout=1)

# Send system stats
ser.write(b'CPU:45\n')
ser.write(b'RAM:67\n')
ser.write(b'WPM:25\n')
ser.write(b'TIME:12:34\n')

# Control animation
ser.write(b'SPEED:120\n')
ser.write(b'PING\n')

# Read responses
if ser.in_waiting > 0:
    response = ser.readline().decode('utf-8').strip()
    print(f"Response: {response}")

ser.close()
```

### Arduino Integration / Arduino 集成

```cpp
// Send command to ESP32
void sendCommand(String cmd) {
    Serial.println(cmd);
}

// Example usage
sendCommand("CPU:45");
sendCommand("SPEED:120");
sendCommand("PING");
```

---

*Last updated: October 2024 / 最后更新: 2024年10月*
