#ifndef AHT30_H
#define AHT30_H

#include <Arduino.h>
#include <Wire.h>

// AHT30 I2C address
#define AHT30_I2C_ADDRESS 0x38

// AHT30 commands
#define AHT30_CMD_TRIGGER_MEASUREMENT 0xAC
#define AHT30_CMD_SOFT_RESET 0xBA
#define AHT30_CMD_CALIBRATE 0xBE

// Measurement delay
#define AHT30_MEASUREMENT_DELAY 80  // ms

// Default calibration offsets (adjusted based on actual sensor comparison)
// Temperature is 7°C too high -> offset -7.0
// Humidity is 20% too low -> offset +20.0
#define DEFAULT_TEMP_OFFSET   -7.0f
#define DEFAULT_HUMI_SCALE     1.0f
#define DEFAULT_HUMI_OFFSET   20.0f

class AHT30 {
public:
    AHT30(uint8_t sda_pin = 21, uint8_t scl_pin = 22);
    
    bool begin();
    bool isConnected();
    bool readTemperatureAndHumidity(float* temperature, float* humidity);
    bool readTemperature(float* temperature);
    bool readHumidity(float* humidity);
    void softReset();
    
    // Calibration methods
    void setCalibration(float tempOffset, float humiScale, float humiOffset);
    void enableCalibration(bool enable);
    bool isCalibrationEnabled() const { return calibrationEnabled; }
    
    // Getter methods for last readings
    float getLastTemperature() const { return lastTemperature; }
    float getLastHumidity() const { return lastHumidity; }
    bool getLastReadSuccess() const { return lastReadSuccess; }
    
private:
    uint8_t sda_pin;
    uint8_t scl_pin;
    bool initialized;
    float lastTemperature;
    float lastHumidity;
    bool lastReadSuccess;
    
    // Calibration parameters
    bool calibrationEnabled;
    float tempOffset;
    float humiScale;
    float humiOffset;
    
    bool triggerMeasurement();
    bool readData(uint8_t* buffer, uint8_t length);
    bool loadCalibrationData();
    bool checkCalibrationStatus();
    float convertTemperature(uint32_t raw);
    float convertHumidity(uint32_t raw);
    float applyCalibration(float value, bool isTemperature);
};

#endif // AHT30_H