# Python Scripts - Bongo Cat Monitor

This folder contains Python helper scripts for testing and interacting with the Bongo Cat ESP32 firmware.

## Scripts Overview

- `install_requirements.py`: Install Python dependencies (`pyserial`, `psutil`) with mirror support
- `find_ports.py`: Detect available serial ports and highlight likely ESP32 ports
- `direct_test.py`: Full-featured test script (auto-detection, commands, response reading with timeout)
- `simple_test.py`: Minimal test script (send commands, non-blocking response read)

## Quick Start

### 1) Install dependencies
```bash
python3 install_requirements.py
# or
pip3 install pyserial psutil
```

### 2) Find your ESP32 port
```bash
python3 find_ports.py
```

### 3) Run a quick test
```bash
# Auto-detect
python3 simple_test.py

# Or specify port explicitly
python3 simple_test.py /dev/ttyUSB0
python3 simple_test.py COM5
```

### 4) Full test script
```bash
# Auto-detect
python3 direct_test.py

# Or specify port explicitly
python3 direct_test.py /dev/ttyUSB0
python3 direct_test.py COM5
```

## What the scripts do

- Send basic control commands to ESP32: `PING`, `CPU`, `RAM`, `WPM`, `TIME`
- Toggle on-device displays for sensors via serial commands:
  - `DISPLAY_TEMP:ON`, `DISPLAY_HUMID:ON`, `DISPLAY_AUDIO:ON`
  - `TOUCH_ENABLE:ON`, `AUDIO_ANIMATION:ON`, `AUDIO_SENSITIVITY:150`
- Handle serial response reading with a small timeout to avoid blocking

## Troubleshooting

- If the port is busy, close Arduino Serial Monitor or other serial tools
- On Linux/macOS, you may need permissions for `/dev/tty*` devices
  ```bash
  sudo usermod -a -G dialout $USER   # Linux
  sudo chmod 666 /dev/ttyUSB0        # temporary
  ```
- If auto-detect finds multiple ports, you will be prompted to select one
- If no response is printed, it may still be working – check the ESP32 screen

## Notes

- These scripts are for local testing and development
- They do not depend on the rest of the repository and can be used standalone
- Windows, Linux, and macOS are supported