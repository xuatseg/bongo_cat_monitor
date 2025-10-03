# Bongo Cat ESP32 Documentation

Welcome to the Bongo Cat ESP32 project documentation!

## Documentation Structure

### Quick Start
- **English**: [QUICK_START.md](QUICK_START.md) - Get up and running quickly
- **中文**: [快速开始.md](快速开始.md) - 快速上手指南

### Detailed Guides
- **English**: [DEBUGGING_GUIDE.md](DEBUGGING_GUIDE.md) - Complete setup and troubleshooting guide
- **中文**: [调试指南.md](调试指南.md) - 完整的设置和故障排除指南

## What's Inside

### QUICK_START / 快速开始
- Prerequisites and hardware requirements
- Quick build and upload commands
- Pin configuration table
- Basic troubleshooting

### DEBUGGING_GUIDE / 调试指南
- Detailed project migration process
- All issues encountered and solutions
- Hardware configuration details
- Build process explanation
- Advanced troubleshooting

## Project Overview

This ESP32 project provides:
- **Animated Bongo Cat display** with multiple states
- **System monitoring** (CPU, RAM, WPM)
- **Real-time clock display**
- **Serial command interface** for Python integration
- **Persistent settings** via EEPROM

## Key Technologies

- **Hardware**: ESP32-WROOM-32 + ILI9341 Display
- **Framework**: Arduino (via PlatformIO)
- **Graphics**: LVGL 8.x
- **Display Driver**: TFT_eSPI

## Quick Links

- [Project README](../README.md)
- [PlatformIO Configuration](../platformio.ini)
- [Main Source Code](../src/main.cpp)

## Support

For issues or questions:
1. Check the troubleshooting sections in the guides
2. Review serial output for debug information
3. Refer to the main project repository

---

## 文档结构

### 快速开始
- **English**: [QUICK_START.md](QUICK_START.md) - 快速入门
- **中文**: [快速开始.md](快速开始.md) - 快速上手

### 详细指南
- **English**: [DEBUGGING_GUIDE.md](DEBUGGING_GUIDE.md) - 完整指南
- **中文**: [调试指南.md](调试指南.md) - 详细文档

## 项目概述

本 ESP32 项目提供：
- **Bongo Cat 动画显示**，支持多种状态
- **系统监控**（CPU、RAM、WPM）
- **实时时钟显示**
- **串口命令接口**，用于 Python 集成
- **持久化设置**，通过 EEPROM

## 核心技术

- **硬件**: ESP32-WROOM-32 + ILI9341 显示屏
- **框架**: Arduino（通过 PlatformIO）
- **图形库**: LVGL 8.x
- **显示驱动**: TFT_eSPI


