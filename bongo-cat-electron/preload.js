const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // App info
  getAppVersion: () => ipcRenderer.invoke('get-app-version'),
  getPlatform: () => ipcRenderer.invoke('get-platform'),

  // Serial communication (to be implemented)
  getSerialPorts: () => ipcRenderer.invoke('get-serial-ports'),
  connectToDevice: (port) => ipcRenderer.invoke('connect-to-device', port),
  disconnectDevice: () => ipcRenderer.invoke('disconnect-device'),
  sendSerialData: (data) => ipcRenderer.invoke('send-serial-data', data),

  // System monitoring (to be implemented)
  getSystemStats: () => ipcRenderer.invoke('get-system-stats'),
  startMonitoring: () => ipcRenderer.invoke('start-monitoring'),
  stopMonitoring: () => ipcRenderer.invoke('stop-monitoring'),

  // Keyboard monitoring (to be implemented)
  startKeyboardMonitoring: () => ipcRenderer.invoke('start-keyboard-monitoring'),
  stopKeyboardMonitoring: () => ipcRenderer.invoke('stop-keyboard-monitoring'),
  getTypingStats: () => ipcRenderer.invoke('get-typing-stats'),

  // Settings management (to be implemented)
  getSettings: () => ipcRenderer.invoke('get-settings'),
  applySettings: (settings) => ipcRenderer.invoke('apply-settings', settings),
  saveSettings: (settings) => ipcRenderer.invoke('save-settings', settings),
  resetSettings: () => ipcRenderer.invoke('reset-settings'),
  
  // Manual WPM testing for fallback mode



  // Event listeners
  onSerialData: (callback) => ipcRenderer.on('serial-data', callback),
  onConnectionChange: (callback) => ipcRenderer.on('connection-change', callback),
  onSystemStats: (callback) => ipcRenderer.on('system-stats', callback),
  onTypingStats: (callback) => ipcRenderer.on('typing-stats', callback),
  onKeyboardFallback: (callback) => ipcRenderer.on('keyboard-fallback', callback),
  onShowSettings: (callback) => ipcRenderer.on('show-settings', callback),

  // Remove listeners
  removeAllListeners: (channel) => ipcRenderer.removeAllListeners(channel)
});

// Log that preload script has loaded
console.log('Bongo Cat Electron - Preload script loaded');