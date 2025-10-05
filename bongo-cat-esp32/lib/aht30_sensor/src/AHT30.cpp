#include "AHT30.h"

AHT30::AHT30(uint8_t sda_pin, uint8_t scl_pin) 
    : sda_pin(sda_pin), scl_pin(scl_pin), initialized(false), 
      lastTemperature(0.0), lastHumidity(0.0), lastReadSuccess(false),
      calibrationEnabled(true), tempOffset(DEFAULT_TEMP_OFFSET),
      humiScale(DEFAULT_HUMI_SCALE), humiOffset(DEFAULT_HUMI_OFFSET) {
    
    Serial.println("AHT30: Constructor called with calibration:");
    Serial.print("  Temperature offset: ");
    Serial.println(tempOffset);
    Serial.print("  Humidity scale: ");
    Serial.println(humiScale);
    Serial.print("  Humidity offset: ");
    Serial.println(humiOffset);
}

bool AHT30::begin() {
    // Initialize I2C with custom pins
    Wire.begin(sda_pin, scl_pin);
    Wire.setClock(100000); // 100kHz for AHT30
    
    // Wait for sensor to stabilize after power-on
    delay(20);
    
    // Check if sensor is connected
    if (!isConnected()) {
        Serial.println("AHT30: Sensor not found at address 0x38!");
        return false;
    }
    
    Serial.println("AHT30: Sensor found at address 0x38");
    
    // Soft reset (recommended for reliability)
    Serial.println("AHT30: Performing soft reset...");
    Wire.beginTransmission(AHT30_I2C_ADDRESS);
    Wire.write(AHT30_CMD_SOFT_RESET);
    if (Wire.endTransmission() != 0) {
        Serial.println("AHT30: Soft reset failed, but continuing...");
    }
    delay(20); // Wait for reset to complete
    
    // Load calibration data (important for AHT30)
    Serial.println("AHT30: Loading calibration data...");
    if (!loadCalibrationData()) {
        Serial.println("AHT30: Calibration load failed, but continuing...");
    } else {
        Serial.println("AHT30: Calibration data loaded successfully");
    }
    delay(10); // Wait for calibration to complete
    
    // Check calibration status
    Serial.println("AHT30: Checking calibration status...");
    if (!checkCalibrationStatus()) {
        Serial.println("⚠️ AHT30: Sensor not calibrated!");
        return false;
    } else {
        Serial.println("✅ AHT30: Sensor is properly calibrated");
    }
    
    // Test read to verify sensor is working
    float temp, hum;
    if (!readTemperatureAndHumidity(&temp, &hum)) {
        Serial.println("AHT30: Test measurement failed!");
        return false;
    }
    
    initialized = true;
    Serial.println("AHT30: Sensor initialized successfully!");
    Serial.print("AHT30: Initial reading - Temp: ");
    Serial.print(temp, 1);
    Serial.print("°C, Humidity: ");
    Serial.print(hum, 1);
    Serial.println("%");
    
    return true;
}

bool AHT30::isConnected() {
    Wire.beginTransmission(AHT30_I2C_ADDRESS);
    return Wire.endTransmission() == 0;
}

bool AHT30::triggerMeasurement() {
    // Send trigger measurement command: 0xAC 0x33 0x00
    Wire.beginTransmission(AHT30_I2C_ADDRESS);
    Wire.write(AHT30_CMD_TRIGGER_MEASUREMENT);
    Wire.write(0x33);
    Wire.write(0x00);
    return Wire.endTransmission() == 0;
}

bool AHT30::readTemperatureAndHumidity(float* temperature, float* humidity) {
    // Trigger measurement
    if (!triggerMeasurement()) {
        Serial.println("AHT30: Failed to trigger measurement!");
        lastReadSuccess = false;
        return false;
    }
    
    // Wait for measurement to complete
    delay(AHT30_MEASUREMENT_DELAY);
    
    // Read measurement data (6 bytes)
    uint8_t data[6];
    if (!readData(data, 6)) {
        Serial.println("AHT30: Failed to read measurement data!");
        lastReadSuccess = false;
        return false;
    }
    
    // Check if sensor is busy (bit 7 of status byte should be 0)
    if (data[0] & 0x80) {
        Serial.println("AHT30: Sensor still busy!");
        lastReadSuccess = false;
        return false;
    }
    
    // Convert raw data to temperature and humidity (correct bit manipulation)
    // Humidity: 20 bits from data[1], data[2], data[3]
    uint32_t humidityRaw = ((uint32_t)data[1] << 12) | ((uint32_t)data[2] << 4) | (data[3] >> 4);
    
    // Temperature: 20 bits from data[3], data[4], data[5]
    uint32_t temperatureRaw = (((uint32_t)data[3] & 0x0F) << 16) | ((uint32_t)data[4] << 8) | data[5];
    
    *humidity = convertHumidity(humidityRaw);
    *temperature = convertTemperature(temperatureRaw);
    
    // Apply calibration if enabled
    if (calibrationEnabled) {
        float originalTemp = *temperature;
        float originalHumidity = *humidity;
        
        *temperature = applyCalibration(*temperature, true);
        *humidity = applyCalibration(*humidity, false);
        
        // Debug output to show calibration effect
        Serial.print("AHT30: Raw -> Calibrated: ");
        Serial.print("Temp ");
        Serial.print(originalTemp, 1);
        Serial.print("°C -> ");
        Serial.print(*temperature, 1);
        Serial.print("°C, Humidity ");
        Serial.print(originalHumidity, 1);
        Serial.print("% -> ");
        Serial.print(*humidity, 1);
        Serial.println("%");
        
        // Limit humidity range
        if (*humidity < 0) *humidity = 0;
        if (*humidity > 100) *humidity = 100;
    }
    
    // Store last readings
    lastTemperature = *temperature;
    lastHumidity = *humidity;
    lastReadSuccess = true;
    
    return true;
}

bool AHT30::readTemperature(float* temperature) {
    float humidity;
    return readTemperatureAndHumidity(temperature, &humidity);
}

bool AHT30::readHumidity(float* humidity) {
    float temperature;
    return readTemperatureAndHumidity(&temperature, humidity);
}

void AHT30::softReset() {
    Wire.beginTransmission(AHT30_I2C_ADDRESS);
    Wire.write(AHT30_CMD_SOFT_RESET);
    Wire.endTransmission();
    delay(20); // Wait for reset to complete
    initialized = false;
}

bool AHT30::readData(uint8_t* buffer, uint8_t length) {
    Wire.requestFrom(AHT30_I2C_ADDRESS, length);
    
    // Wait a bit for data to be available
    uint32_t startTime = millis();
    while (Wire.available() < length) {
        if (millis() - startTime > 100) { // 100ms timeout
            Serial.print("AHT30: Timeout waiting for data. Available: ");
            Serial.println(Wire.available());
            return false;
        }
        delay(1);
    }
    
    for (uint8_t i = 0; i < length; i++) {
        buffer[i] = Wire.read();
    }
    
    return true;
}

float AHT30::convertTemperature(uint32_t raw) {
    // Temperature formula: T = (raw * 200) / 2^20 - 50
    return (raw * 200.0) / 1048576.0 - 50.0;
}

float AHT30::convertHumidity(uint32_t raw) {
    // Humidity formula: RH = (raw * 100) / 2^20
    return (raw * 100.0) / 1048576.0;
}

bool AHT30::loadCalibrationData() {
    // Load calibration data command: 0xBE 0x08 0x00
    // This command loads the factory calibration coefficients
    Wire.beginTransmission(AHT30_I2C_ADDRESS);
    Wire.write(AHT30_CMD_CALIBRATE);
    Wire.write(0x08);
    Wire.write(0x00);
    
    if (Wire.endTransmission() != 0) {
        Serial.println("AHT30: Failed to send calibration command");
        return false;
    }
    
    Serial.println("AHT30: Calibration command sent successfully");
    return true;
}

bool AHT30::checkCalibrationStatus() {
    // Read status register (0x71) to check calibration bit (bit 3)
    Wire.beginTransmission(AHT30_I2C_ADDRESS);
    Wire.write(0x71); // Status register command
    if (Wire.endTransmission() != 0) {
        Serial.println("AHT30: Failed to read status register");
        return false;
    }
    
    Wire.requestFrom(AHT30_I2C_ADDRESS, 1);
    if (Wire.available() < 1) {
        Serial.println("AHT30: No data received from status register");
        return false;
    }
    
    uint8_t status = Wire.read();
    Serial.print("AHT30: Status register: 0x");
    Serial.println(status, HEX);
    
    // Check calibration bit (bit 3 = 0x08)
    bool isCalibrated = (status & 0x08) != 0;
    Serial.print("AHT30: Calibration bit (0x08): ");
    Serial.println(isCalibrated ? "SET" : "NOT SET");
    
    return isCalibrated;
}

void AHT30::setCalibration(float tempOffset, float humiScale, float humiOffset) {
    this->tempOffset = tempOffset;
    this->humiScale = humiScale;
    this->humiOffset = humiOffset;
    Serial.println("AHT30: Calibration parameters updated");
    Serial.print("  Temperature offset: ");
    Serial.println(tempOffset);
    Serial.print("  Humidity scale: ");
    Serial.println(humiScale);
    Serial.print("  Humidity offset: ");
    Serial.println(humiOffset);
}

void AHT30::enableCalibration(bool enable) {
    calibrationEnabled = enable;
    Serial.print("AHT30: Calibration ");
    Serial.println(enable ? "enabled" : "disabled");
}

float AHT30::applyCalibration(float value, bool isTemperature) {
    if (isTemperature) {
        // Apply temperature offset
        return value + tempOffset;
    } else {
        // Apply humidity scale and offset
        return value * humiScale + humiOffset;
    }
}