# 🐱 Bongo Cat for Mac - Installation Guide

## What You Need
- **macOS 10.15 or newer** (works on Intel and Apple Silicon Macs)
- **Your ESP32 Bongo Cat device** (plugged into USB)
- **5 minutes** for setup

---

## 📥 Step 1: Download the App

1. Go to our [Releases page](https://github.com/your-repo/releases) 
2. Download **`Bongo-Cat-1.0.0.dmg`** (latest version)
3. Wait for download to complete

---

## 💻 Step 2: Install the App

### Open the DMG file
1. **Double-click** the downloaded `.dmg` file
2. A window will open showing the Bongo Cat app

### Install to Applications
1. **Drag** the Bongo Cat app icon to the **Applications** folder
2. Close the DMG window
3. You can now delete the `.dmg` file

---

## 🔓 Step 3: First Launch (Important!)

⚠️ **Mac will show security warnings the first time - this is normal!**

### Launch the app
1. Open **Applications** folder (Cmd+Space, type "Applications")
2. Find **Bongo Cat** app
3. **Right-click** on Bongo Cat → **"Open"**
4. Click **"Open"** again when asked
5. The app should now start!

*After the first launch, you can open it normally by double-clicking.*

---

## 🔑 Step 4: Grant Permissions

The app will ask for permissions to work properly:

### Input Monitoring Permission
- **Why needed:** To track your typing speed
- **When prompted:** Click **"Open System Preferences"**
- Go to **Privacy & Security** → **Input Monitoring**
- Check the box next to **"Bongo Cat"**

### USB/Serial Permission  
- **Why needed:** To communicate with your ESP32 device
- **When prompted:** Click **"Allow"**

---

## 🎮 Step 5: Connect Your ESP32

1. **Plug in** your ESP32 Bongo Cat device via USB
2. In the app, click the **"Refresh Ports"** button
3. **Select** your ESP32 from the dropdown (usually shows as "usbserial" or similar)
4. Click **"Connect"**
5. **Success!** Your Bongo Cat should start responding to your typing

---

## 🚨 Troubleshooting

### "App can't be opened" error
- Make sure you **right-clicked** and chose **"Open"** (don't double-click on first launch)
- Go to **System Preferences** → **Privacy & Security** → Click **"Open Anyway"**

### Can't find ESP32 device
- Try a different USB cable
- Unplug and replug the device
- Click "Refresh Ports" again
- Try a different USB port

### Permissions not working
- Go to **System Preferences** → **Privacy & Security**
- Remove Bongo Cat from the permission lists
- Launch the app again to re-grant permissions

### App won't start
- Make sure you're running **macOS 10.15 or newer**
- Try restarting your Mac
- Check you dragged the app to Applications folder

---

## 🎉 You're Done!

Your Bongo Cat should now:
- 😺 **React** to your typing speed
- 📊 **Show** system stats (CPU, RAM)
- 🕐 **Display** the current time
- 🎨 **Animate** based on your activity

**Enjoy your coding companion!** 

---

## 📧 Need Help?

- Check our [GitHub Issues](https://github.com/your-repo/issues)
- Join our Discord community
- Email support: bongo-cat@example.com

---

*Made with ❤️ by the Bongo Cat community*