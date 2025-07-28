# Creating Bongo Cat Supporting Application

## Overview

Convert the Python typing monitor script into a professional Windows executable that:
- Installs once and runs automatically on PC startup
- Provides user-friendly configuration options
- Runs silently in the background via system tray
- Eliminates the need for users to manage Python dependencies

## Architecture Plan

### Core Components

1. **Main Application (`main.py`)**
   - Entry point with system tray integration
   - Handles auto-startup functionality
   - Manages application lifecycle

2. **Monitoring Engine (`engine.py`)**
   - Refactored core logic from existing script
   - Configurable parameters via settings
   - Real-time settings updates without restart

3. **Configuration Manager (`config.py`)**
   - JSON-based settings persistence
   - Default configuration management
   - Runtime settings validation

4. **Settings GUI (`gui.py`)**
   - User-friendly configuration interface
   - Real-time preview of changes
   - Intuitive controls for all options

5. **Installation Utilities (`installer.py`)**
   - Auto-startup setup
   - Desktop shortcut creation
   - First-run configuration wizard

## Key Features

### Auto-Startup Integration
- **Method**: Windows Startup Folder (reliable and user-controllable)
- **Location**: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\`
- **Behavior**: Start minimized to system tray
- **Fallback**: Registry entry if startup folder fails

### System Tray Integration
- **Library**: `pystray` for cross-platform tray support
- **Features**:
  - Right-click context menu
  - Connection status indicators
  - Quick access to settings
  - Graceful exit option

### Configuration Options

#### Display Settings
- **CPU Usage**: Show/hide CPU percentage
- **RAM Usage**: Show/hide memory usage
- **WPM Counter**: Show/hide typing speed
- **Clock**: Show/hide current time
- **Time Format**: 12-hour vs 24-hour format

#### Behavior Settings
- **Sleep Timeout**: 1-60 minutes (when cat goes to sleep)
- **Animation Sensitivity**: 0.5x - 2.0x speed multiplier
- **Idle Timeout**: How long before stopping animations
- **Auto-Reconnect**: Automatic ESP32 reconnection

#### Connection Settings
- **COM Port**: Auto-detect or manual selection
- **Baudrate**: Configurable (default 115200)
- **Connection Timeout**: Retry parameters

### Configuration Storage
```json
{
  "sleep_timeout_minutes": 5,
  "display": {
    "show_cpu": true,
    "show_ram": true, 
    "show_wpm": true,
    "show_time": true,
    "time_format_24h": true
  },
  "connection": {
    "com_port": "AUTO",
    "baudrate": 115200,
    "auto_reconnect": true,
    "timeout_seconds": 5
  },
  "animation": {
    "sensitivity": 1.0,
    "idle_timeout": 3.0
  },
  "startup": {
    "start_with_windows": true,
    "start_minimized": true,
    "show_notifications": true
  }
}
```

## Implementation Strategy

### Phase 1: Core Refactoring
1. **Extract monitoring logic** from current script
2. **Create configurable parameters** for all settings
3. **Implement runtime configuration** updates
4. **Add callback system** for settings changes

### Phase 2: GUI Development
1. **Create settings window** with tkinter
2. **Implement system tray** with pystray
3. **Add configuration persistence** with JSON
4. **Create first-run wizard** for initial setup

### Phase 3: Installation System
1. **Develop auto-startup** functionality
2. **Create desktop shortcuts** and start menu entries
3. **Implement configuration migration** for updates
4. **Add uninstaller** capabilities

### Phase 4: Packaging
1. **Configure PyInstaller** for optimal packaging
2. **Bundle all dependencies** including icons
3. **Create one-file executable** for easy distribution
4. **Test on clean Windows** systems

## Technical Requirements

### Dependencies
```txt
# Core dependencies (existing)
pyserial>=3.5
pynput>=1.7.6
psutil>=5.8.0

# New dependencies for GUI application
pystray>=0.19.0
Pillow>=8.0.0
PyInstaller>=5.0.0
```

### File Structure
```
bongo_cat_app/
├── main.py              # Application entry point
├── engine.py            # Core monitoring logic
├── config.py            # Configuration management
├── gui.py               # Settings GUI window
├── installer.py         # Installation utilities
├── build.py             # PyInstaller build script
├── icon.ico             # Application icon
├── requirements.txt     # Python dependencies
└── dist/                # Built executable output
```

### Build Configuration (PyInstaller)
```python
# build.spec
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('icon.ico', '.')],
    hiddenimports=['pystray._win32', 'PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BongoCat',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'
)
```

## Arduino Firmware Updates Required

### New Serial Commands
```cpp
// Display control commands
DISPLAY_CPU:ON/OFF     // Toggle CPU display
DISPLAY_RAM:ON/OFF     // Toggle RAM display  
DISPLAY_WPM:ON/OFF     // Toggle WPM display
DISPLAY_TIME:ON/OFF    // Toggle time display
TIME_FORMAT:12/24      // Set time format

// Behavior commands
SLEEP_TIMEOUT:X        // Set sleep timeout in minutes
SENSITIVITY:X.X        // Set animation sensitivity multiplier
```

### EEPROM Settings Storage
- Store user preferences in EEPROM
- Load settings on startup
- Validate settings ranges
- Provide factory reset option

## User Experience Flow

### Installation Process
1. **Download executable** from GitHub releases
2. **Run installer** (or portable executable)
3. **First-run wizard** appears:
   - Welcome screen
   - ESP32 connection setup
   - Initial configuration
   - Test connection
4. **Installation complete** - app runs in system tray

### Daily Usage
1. **Auto-starts** with Windows (silent)
2. **Runs in background** - no visible windows
3. **System tray icon** shows connection status
4. **Right-click menu** provides:
   - Settings
   - Connection status
   - Show/hide features
   - Exit

### Configuration Changes
1. **Right-click tray icon** → Settings
2. **Settings window opens** with current values
3. **Make changes** with immediate preview
4. **Apply changes** - no restart required
5. **Settings persist** automatically

## Development Workflow

### Step 1: Setup Development Environment
```bash
# Create virtual environment
python -m venv bongo_cat_app
cd bongo_cat_app
Scripts\activate

# Install development dependencies
pip install -r requirements.txt
```

### Step 2: Create Modular Structure
1. Refactor existing script into engine.py
2. Create configuration system
3. Build GUI components
4. Implement system tray

### Step 3: Testing Strategy
1. **Unit tests** for configuration management
2. **Integration tests** for ESP32 communication
3. **GUI tests** for settings interface
4. **Installation tests** on clean Windows VMs

### Step 4: Build and Package
```bash
# Build executable
python build.py

# Test executable
dist\BongoCat.exe

# Create installer (optional)
# Using NSIS or Inno Setup
```

## Benefits for End Users

### Technical Benefits
- **No Python installation** required
- **No dependency management** needed
- **Automatic updates** via GitHub releases
- **Professional installation** experience
- **System integration** (startup, tray)

### User Experience Benefits
- **One-time setup** process
- **Intuitive configuration** interface
- **Background operation** - doesn't interfere
- **Instant customization** without code editing
- **Reliable auto-startup** after reboots

## Distribution Strategy

### GitHub Releases
- **Pre-built executable** for Windows
- **Installation instructions** with screenshots
- **Arduino firmware** (existing .ino file)
- **Quick setup guide** for new users

### Documentation
- **User manual** with screenshots
- **Troubleshooting guide** for common issues
- **FAQ** for configuration questions
- **Video tutorial** for initial setup

## Success Metrics

### Technical Goals
- ✅ Single executable under 50MB
- ✅ Startup time under 5 seconds
- ✅ Memory usage under 100MB
- ✅ 99% successful auto-detection
- ✅ Configuration changes in real-time

### User Experience Goals
- ✅ Complete setup in under 5 minutes
- ✅ No technical knowledge required
- ✅ Intuitive settings interface
- ✅ Reliable unattended operation
- ✅ Easy troubleshooting

This comprehensive plan transforms the Python script into a professional Windows application that provides the exact user experience requested: install once, runs automatically, simple customization, no technical hassle. 