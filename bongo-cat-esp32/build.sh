#!/bin/bash

# Bongo Cat ESP32 Build Script
# This script builds the ESP32 project using PlatformIO

echo "🐱 Building Bongo Cat ESP32..."

# Check if PlatformIO is installed
if ! command -v pio &> /dev/null; then
    echo "❌ PlatformIO not found. Please install PlatformIO first."
    echo "   Visit: https://platformio.org/install"
    exit 1
fi

# Clean previous build
echo "🧹 Cleaning previous build..."
pio run --target clean

# Build the project
echo "🔨 Building project..."
pio run

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Connect your ESP32 via USB"
    echo "   2. Run: pio run --target upload"
    echo "   3. Monitor serial output: pio device monitor"
else
    echo "❌ Build failed!"
    exit 1
fi
