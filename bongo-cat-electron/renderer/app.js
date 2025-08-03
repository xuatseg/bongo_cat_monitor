// DOM elements
const connectionStatus = document.getElementById('connectionStatus');
const portSelect = document.getElementById('portSelect');
const connectBtn = document.getElementById('connectBtn');
const refreshBtn = document.getElementById('refreshBtn');
const connectionInfo = document.getElementById('connectionInfo');

const settingsBtn = document.getElementById('settingsBtn');
const settingsModal = document.getElementById('settingsModal');
const closeSettings = document.getElementById('closeSettings');
const applySettings = document.getElementById('applySettings');
const saveSettings = document.getElementById('saveSettings');
const resetSettings = document.getElementById('resetSettings');


// Stat display elements
const wpmValue = document.getElementById('wpmValue');
const cpuValue = document.getElementById('cpuValue');
const ramValue = document.getElementById('ramValue');
const timeValue = document.getElementById('timeValue');

// Setting elements
const showCpu = document.getElementById('showCpu');
const showRam = document.getElementById('showRam');
const showWpm = document.getElementById('showWpm');
const showTime = document.getElementById('showTime');
const timeFormat = document.getElementById('timeFormat');
const sleepTimeout = document.getElementById('sleepTimeout');

// Application state
let isConnected = false;
let currentPort = null;

// Initialize the application
async function initializeApp() {
    try {
        const platform = await window.electronAPI.getPlatform();
        const version = await window.electronAPI.getAppVersion();
        

        
        // Load settings
        await loadSettings();
        
        // Refresh serial ports
        await refreshSerialPorts();
        
        // Set up event listeners
        setupEventListeners();
        
        // Update time display
        updateTimeDisplay();
        setInterval(updateTimeDisplay, 1000);
        

        
    } catch (error) {
        console.error('Failed to initialize app:', error);

    }
}

// Set up event listeners
function setupEventListeners() {
    // Connection controls
    connectBtn.addEventListener('click', toggleConnection);
    refreshBtn.addEventListener('click', refreshSerialPorts);
    

    
    // Settings modal
    settingsBtn.addEventListener('click', showSettings);
    closeSettings.addEventListener('click', hideSettings);
    applySettings.addEventListener('click', applyAppSettings);
    saveSettings.addEventListener('click', saveAppSettings);
    resetSettings.addEventListener('click', resetAppSettings);
    
    // Close modal when clicking outside
    settingsModal.addEventListener('click', (e) => {
        if (e.target === settingsModal) {
            hideSettings();
        }
    });
    
    // Electron API event listeners
    window.electronAPI.onConnectionChange((event, data) => {
        updateConnectionStatus(data.connected, data.port);
    });
    
    window.electronAPI.onSystemStats((event, stats) => {
        updateSystemStats(stats);
    });
    
    window.electronAPI.onTypingStats((event, stats) => {

        updateTypingStats(stats);
    });
    
    window.electronAPI.onKeyboardFallback((event, data) => {
        console.log('⚠️ Keyboard fallback mode activated');

    });
    
    window.electronAPI.onSerialData((event, data) => {

    });
    
    window.electronAPI.onShowSettings(() => {
        showSettings();
    });
}

// Refresh available serial ports
async function refreshSerialPorts() {
    try {

        const ports = await window.electronAPI.getSerialPorts();
        
        // Clear existing options
        portSelect.innerHTML = '<option value="">Select ESP32 Port...</option>';
        
        // Add available ports
        ports.forEach(port => {
            const option = document.createElement('option');
            option.value = port.path;
            option.textContent = `${port.path} - ${port.manufacturer || 'Unknown'}`;
            portSelect.appendChild(option);
        });
        

        
    } catch (error) {
        console.error('Failed to refresh ports:', error);

    }
}

// Toggle device connection
async function toggleConnection() {
    try {
        if (isConnected) {
            // Disconnect
            await window.electronAPI.disconnectDevice();

        } else {
            // Connect
            const selectedPort = portSelect.value;
            if (!selectedPort) {

                return;
            }
            

            const result = await window.electronAPI.connectToDevice(selectedPort);
            
            if (result.success) {
                currentPort = selectedPort;

            } else {

            }
        }
    } catch (error) {
        console.error('Connection error:', error);

    }
}

// Update connection status UI
function updateConnectionStatus(connected, port) {
    isConnected = connected;
    currentPort = port;
    
    const statusDot = connectionStatus.querySelector('.status-dot');
    const statusText = connectionStatus.querySelector('.status-text');
    
    if (connected) {
        statusDot.className = 'status-dot connected';
        statusText.textContent = `Connected to ${port}`;
        connectBtn.textContent = 'Disconnect';
        connectBtn.className = 'btn btn-danger';
        connectionInfo.innerHTML = `<p>Connected to ESP32 on port ${port}</p>`;
    } else {
        statusDot.className = 'status-dot disconnected';
        statusText.textContent = 'Disconnected';
        connectBtn.textContent = 'Connect';
        connectBtn.className = 'btn btn-primary';
        connectionInfo.innerHTML = '<p>Select a port and click Connect to start monitoring</p>';
    }
}



// Update system stats display
function updateSystemStats(stats) {
    if (stats.cpu !== undefined) {
        cpuValue.textContent = `${Math.round(stats.cpu)}%`;
    }
    if (stats.memory !== undefined) {
        ramValue.textContent = `${Math.round(stats.memory)}%`;
    }
}

// Update typing stats display
function updateTypingStats(stats) {

    if (stats.wpm !== undefined) {
        const wpmText = `${Math.round(stats.wpm)} WPM`;

        wpmValue.textContent = wpmText;
    } else {

    }
}

// Update time display
function updateTimeDisplay() {
    const now = new Date();
    const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    timeValue.textContent = timeString;
}

// Settings management
function showSettings() {
    settingsModal.classList.add('show');
}

function hideSettings() {
    settingsModal.classList.remove('show');
}

async function loadSettings() {
    try {
        const settings = await window.electronAPI.getSettings();
        
        // Display settings
        showCpu.checked = settings.showCpu !== false; // default true
        showRam.checked = settings.showRam !== false; // default true
        showWpm.checked = settings.showWpm !== false; // default true
        showTime.checked = settings.showTime !== false; // default true
        timeFormat.value = settings.timeFormat || '24'; // default 24-hour
        sleepTimeout.value = settings.sleepTimeout || 5; // default 5 minutes
        
    } catch (error) {
        console.error('Failed to load settings:', error);

    }
}

async function applyAppSettings() {
    try {
        // Validate electronAPI is available
        if (!window.electronAPI) {
            throw new Error('electronAPI not available. Check preload script.');
        }
        
        if (!window.electronAPI.applySettings) {
            throw new Error('applySettings method not available in electronAPI.');
        }
        
        // Show applying state
        const applyBtn = document.getElementById('applySettings');
        const originalText = applyBtn.textContent;
        applyBtn.textContent = 'Applying...';
        applyBtn.disabled = true;
        
        const settings = {
            showCpu: showCpu.checked,
            showRam: showRam.checked,
            showWpm: showWpm.checked,
            showTime: showTime.checked,
            timeFormat: timeFormat.value,
            sleepTimeout: parseInt(sleepTimeout.value)
        };
        
        console.log('Attempting to apply settings:', settings);
        await window.electronAPI.applySettings(settings);
        
        // Show success state briefly
        applyBtn.textContent = 'Applied!';
        setTimeout(() => {
            applyBtn.textContent = originalText;
            applyBtn.disabled = false;
        }, 1000);
        
    } catch (error) {
        console.error('Failed to apply settings:', error);
        console.error('Error details:', {
            message: error.message,
            stack: error.stack,
            name: error.name
        });
        
        // Reset button state on error
        const applyBtn = document.getElementById('applySettings');
        applyBtn.textContent = 'Apply';
        applyBtn.disabled = false;
        alert(`Failed to apply settings. Error: ${error.message}\nCheck console for details.`);
    }
}

async function saveAppSettings() {
    try {
        // Show saving state
        const saveBtn = document.getElementById('saveSettings');
        const originalText = saveBtn.textContent;
        saveBtn.textContent = 'Saving...';
        saveBtn.disabled = true;
        
        const settings = {
            showCpu: showCpu.checked,
            showRam: showRam.checked,
            showWpm: showWpm.checked,
            showTime: showTime.checked,
            timeFormat: timeFormat.value,
            sleepTimeout: parseInt(sleepTimeout.value)
        };
        
        await window.electronAPI.saveSettings(settings);
        
        // Show success state briefly
        saveBtn.textContent = 'Saved!';
        setTimeout(() => {
            saveBtn.textContent = originalText;
            saveBtn.disabled = false;
            hideSettings();
        }, 1000);
        
    } catch (error) {
        console.error('Failed to save settings:', error);
        
        // Reset button state on error
        const saveBtn = document.getElementById('saveSettings');
        saveBtn.textContent = 'Save Settings';
        saveBtn.disabled = false;
        alert('Failed to save settings. Please try again.');
    }
}

async function resetAppSettings() {
    try {
        await window.electronAPI.resetSettings();
        await loadSettings(); // Reload the reset settings

        
    } catch (error) {
        console.error('Failed to reset settings:', error);

    }
}





// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeApp);