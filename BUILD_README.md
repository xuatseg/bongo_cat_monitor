# 🐱 Bongo Cat Application - EXE Build Guide

## 📋 Prerequisites

1. **Python 3.8+** installed on Windows
2. **NSIS** (Nullsoft Scriptable Install System) for installer creation
   - Download from: https://nsis.sourceforge.io/Download
   - Required for professional installer (optional for standalone exe)
3. **ESP32** with Bongo Cat firmware (optional for testing)
4. **Git** (if cloning from repository)

## 🚀 Quick Build (Recommended)

### Method 1: Using Batch File (Easiest)
```batch
# Double-click or run:
build_exe.bat
```

### Method 2: Manual Build
```bash
# 1. Install minimal dependencies
pip install -r bongo_cat_app/requirements_minimal.txt

# 2. Run the build script
python build_exe.py
```

## 📦 Build Output

After successful build:
- **EXE Location**: `dist/BongoCat.exe` (~15-25 MB, standalone)
- **Installer Location**: `BongoCat_Setup.exe` (~16-26 MB, professional installer)
- **Type**: Complete Windows integration with startup support

## 🔧 Build Process Details

### What the build script does:
1. ✅ Checks/installs PyInstaller
2. 🧹 Cleans previous build files
3. 📝 Creates optimized PyInstaller spec file
4. 🏗️ Builds single-file executable
5. 📦 Creates professional Windows installer (if NSIS available)
6. 📊 Reports final sizes and locations

### Included in EXE:
- ✅ All Python modules (config, engine, tray, gui)
- ✅ Tray icon (tray_icon.png)
- ✅ Default configuration file
- ✅ All required dependencies

### Excluded (for smaller size):
- ❌ Heavy ML libraries (numpy, scipy, tensorflow)
- ❌ Unnecessary modules
- ❌ Development files

## 🧪 Testing the EXE

### Basic Test:
1. Run `dist/BongoCat.exe`
2. Check system tray for cat icon
3. Right-click tray icon → test menu options
4. Open Settings → verify GUI works

### Full Test (with ESP32):
1. Connect ESP32 with Bongo Cat firmware
2. Run EXE
3. Verify connection status shows "[✓] Connected"
4. Test typing → verify animations on display
5. Test settings → verify changes apply immediately

## 🔍 Troubleshooting

### Build Issues:

**"ModuleNotFoundError" during build:**
```bash
# Install missing dependency
pip install [missing-module]
```

**"Permission denied" errors:**
```bash
# Run as administrator or close antivirus
```

**Large EXE size (>50MB):**
- Check if unnecessary packages were included
- Use `requirements_minimal.txt` instead of `requirements_app.txt`

### Runtime Issues:

**EXE won't start:**
- Check Windows antivirus isn't blocking it
- Run EXE from command line to see error messages

**Tray icon doesn't appear:**
- Ensure assets/tray_icon.png exists
- Check if another instance is already running

**ESP32 connection fails:**
- Verify ESP32 is plugged in and recognized
- Check COM port permissions
- Try running as administrator

## 📁 File Structure After Build

```
project/
├── dist/
│   └── BongoCat.exe          ← Final executable
├── build/                    ← Temporary build files
├── bongo_cat.spec           ← PyInstaller configuration
├── build_exe.py             ← Build script
├── build_exe.bat            ← Quick build batch file
└── bongo_cat_app/
    ├── main.py               ← Entry point
    ├── requirements_minimal.txt
    └── assets/
        └── tray_icon.png     ← Included in EXE
```

## 🚀 Distribution

### Option 1: Professional Installer (Recommended)
Use `BongoCat_Setup.exe` for:
- ✅ Automatic installation to Program Files
- ✅ Windows startup integration
- ✅ Proper uninstaller in Add/Remove Programs
- ✅ Professional user experience

### Option 2: Standalone EXE
Use `dist/BongoCat.exe` for:
- ✅ Portable installation
- ✅ No installation required
- ✅ Manual startup configuration needed

## 🔧 Advanced Build Options

### Debug Build:
Edit `build_exe.py` and change:
```python
console=True   # Shows console window for debugging
```

### Custom Icon:
Replace `bongo_cat_app/assets/tray_icon.png` with your icon before building.

### Optimizations:
- UPX compression is enabled by default
- Excludes heavy packages automatically
- Single-file build for easy distribution

## 📝 Build Logs

Build process creates detailed logs showing:
- Dependencies found/installed
- Files included in EXE
- Final EXE size and location
- Any warnings or errors

Happy building! 🎉 