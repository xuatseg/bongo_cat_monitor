# 🐱 Bongo Cat Electron

Cross-platform desktop application for the Bongo Cat ESP32 project, bringing the beloved coding companion to Mac users and beyond!

## 🚀 Features

- **📡 ESP32 Communication** - Automatic device detection and serial communication
- **⌨️ Keyboard Monitoring** - Real-time typing speed tracking (WPM)
- **📊 System Stats** - CPU and RAM usage monitoring
- **🕒 Time Display** - Current time synchronization
- **🖥️ System Tray** - Background operation with tray integration
- **⚙️ Settings** - Customizable update intervals and preferences
- **🍎 Mac Ready** - Optimized for macOS with proper permissions and signing

## 🛠️ Development Setup

### Prerequisites
- Node.js 16 or higher
- npm or yarn
- ESP32 Bongo Cat device

### Installation
```bash
# Clone or navigate to the electron project
cd bongo-cat-electron

# Install dependencies
npm install

# Run in development mode
npm run dev

# Build for production
npm run build

# Build specifically for Mac
npm run build:mac
```

## 📱 Usage

1. **Connect ESP32** - Plug in your Bongo Cat ESP32 device
2. **Select Port** - Choose the correct serial port from the dropdown
3. **Connect** - Click connect to establish communication
4. **Start Monitoring** - Begin tracking keyboard and system stats
5. **Enjoy** - Watch your Bongo Cat react to your coding activity!

## 🔧 Configuration

Access settings through the app interface to configure:
- Update interval for system monitoring
- Auto-connect preferences
- System tray behavior
- Startup options

## 🍎 Mac-Specific Features

- **Native App Bundle** - Proper .app structure for macOS
- **System Permissions** - Handles input monitoring permissions
- **Gatekeeper Ready** - Code signing and notarization support
- **Launch Agents** - Auto-start functionality
- **Retina Ready** - High-DPI display support

## 📋 Build Requirements for Mac Distribution

For distributing on Mac, you'll need:
- Apple Developer account
- Code signing certificate
- Notarization credentials

Configure in `package.json` build section or use environment variables:
```bash
export CSC_LINK="path/to/certificate.p12"
export CSC_KEY_PASSWORD="certificate-password"
export APPLE_ID="your-apple-id"
export APPLE_ID_PASSWORD="app-specific-password"
```

## 🚨 Permissions

On macOS, the app will request permissions for:
- **Input Monitoring** - For keyboard tracking
- **System Events** - For system stats monitoring
- **USB/Serial Devices** - For ESP32 communication

Grant these permissions in System Preferences > Security & Privacy.

## 🗂️ Project Structure

```
bongo-cat-electron/
├── main.js                 # Main Electron process
├── preload.js             # Secure IPC bridge
├── renderer/              # UI files
│   ├── index.html
│   ├── app.js
│   └── style.css
├── src/                   # Core functionality modules
│   ├── serial-handler.js  # ESP32 communication
│   ├── system-monitor.js  # System stats
│   ├── keyboard-monitor.js # Keyboard tracking
│   └── tray-manager.js    # System tray
├── assets/               # Icons and resources
├── build/               # Build configurations
└── dist/               # Built applications
```

## 🤝 Contributing

This Electron app is part of the larger Bongo Cat ESP32 project. See the main project README for contribution guidelines.

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Original Bongo Cat meme creators
- ESP32 community
- Electron.js team
- All contributors to the Bongo Cat project