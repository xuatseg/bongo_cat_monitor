const Store = require('electron-store');

/**
 * Settings Manager for Bongo Cat Electron App
 * Handles persistent storage of user preferences
 */
class SettingsManager {
    constructor() {
        // Initialize electron-store with schema validation
        this.store = new Store({
            name: 'bongo-cat-settings',
            schema: {
                updateInterval: {
                    type: 'number',
                    minimum: 100,
                    maximum: 10000,
                    default: 1000
                },
                autoConnect: {
                    type: 'boolean',
                    default: false
                },
                minimizeToTray: {
                    type: 'boolean',
                    default: true
                },
                startMinimized: {
                    type: 'boolean',
                    default: false
                },
                lastUsedPort: {
                    type: 'string',
                    default: ''
                },
                esp32Settings: {
                    type: 'object',
                    properties: {
                        baudRate: {
                            type: 'number',
                            default: 115200
                        },
                        timeout: {
                            type: 'number',
                            default: 1000
                        },
                        autoReconnect: {
                            type: 'boolean',
                            default: true
                        }
                    },
                    default: {
                        baudRate: 115200,
                        timeout: 1000,
                        autoReconnect: true
                    }
                }
            }
        });
        
        console.log('Settings Manager initialized');
    }

    /**
     * Get all settings
     */
    getAllSettings() {
        try {
            return this.store.store;
        } catch (error) {
            console.error('Failed to get settings:', error);
            return this.getDefaultSettings();
        }
    }

    /**
     * Get default settings
     */
    getDefaultSettings() {
        return {
            updateInterval: 1000,
            autoConnect: false,
            minimizeToTray: true,
            startMinimized: false,
            lastUsedPort: '',
            esp32Settings: {
                baudRate: 115200,
                timeout: 1000,
                autoReconnect: true
            }
        };
    }

    /**
     * Get specific setting value
     */
    get(key, defaultValue = null) {
        try {
            return this.store.get(key, defaultValue);
        } catch (error) {
            console.error(`Failed to get setting ${key}:`, error);
            return defaultValue;
        }
    }

    /**
     * Set specific setting value
     */
    set(key, value) {
        try {
            this.store.set(key, value);
            console.log(`Setting updated: ${key} = ${value}`);
            return true;
        } catch (error) {
            console.error(`Failed to set setting ${key}:`, error);
            return false;
        }
    }

    /**
     * Update multiple settings at once
     */
    updateSettings(newSettings) {
        try {
            // Validate and merge with existing settings
            const currentSettings = this.getAllSettings();
            const updatedSettings = { ...currentSettings, ...newSettings };
            
            // Set each setting individually to trigger validation
            for (const [key, value] of Object.entries(newSettings)) {
                this.store.set(key, value);
            }
            
            console.log('Settings updated successfully:', newSettings);
            return true;
        } catch (error) {
            console.error('Failed to update settings:', error);
            return false;
        }
    }

    /**
     * Reset all settings to defaults
     */
    resetToDefaults() {
        try {
            this.store.clear();
            console.log('Settings reset to defaults');
            return true;
        } catch (error) {
            console.error('Failed to reset settings:', error);
            return false;
        }
    }

    /**
     * Get ESP32 specific settings
     */
    getESP32Settings() {
        return this.get('esp32Settings', {
            baudRate: 115200,
            timeout: 1000,
            autoReconnect: true
        });
    }

    /**
     * Update ESP32 specific settings
     */
    updateESP32Settings(esp32Settings) {
        const currentESP32Settings = this.getESP32Settings();
        const updatedESP32Settings = { ...currentESP32Settings, ...esp32Settings };
        return this.set('esp32Settings', updatedESP32Settings);
    }

    /**
     * Save last used port for auto-connection
     */
    saveLastUsedPort(port) {
        return this.set('lastUsedPort', port);
    }

    /**
     * Get last used port
     */
    getLastUsedPort() {
        return this.get('lastUsedPort', '');
    }

    /**
     * Check if auto-connect is enabled
     */
    shouldAutoConnect() {
        return this.get('autoConnect', false);
    }

    /**
     * Get update interval for monitoring
     */
    getUpdateInterval() {
        return this.get('updateInterval', 1000);
    }

    /**
     * Check if app should start minimized
     */
    shouldStartMinimized() {
        return this.get('startMinimized', false);
    }

    /**
     * Check if app should minimize to tray
     */
    shouldMinimizeToTray() {
        return this.get('minimizeToTray', true);
    }
}

module.exports = SettingsManager;