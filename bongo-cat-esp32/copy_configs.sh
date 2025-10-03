#!/bin/bash

echo "=================================================="
echo "Copying configuration files..."
echo "=================================================="

# Copy User_Setup.h to TFT_eSPI
if [ -f "include/User_Setup.h" ]; then
    mkdir -p .pio/libdeps/esp32dev/TFT_eSPI
    cp include/User_Setup.h .pio/libdeps/esp32dev/TFT_eSPI/
    echo "✅ Copied User_Setup.h to TFT_eSPI"
else
    echo "⚠️ User_Setup.h not found!"
fi

# Copy lv_conf.h to lvgl
if [ -f "lv_conf.h" ]; then
    mkdir -p .pio/libdeps/esp32dev/lvgl
    cp lv_conf.h .pio/libdeps/esp32dev/lvgl/
    echo "✅ Copied lv_conf.h to lvgl"
else
    echo "⚠️ lv_conf.h not found!"
fi

echo "=================================================="
echo "Configuration files copied successfully!"
echo "=================================================="


