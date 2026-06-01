---
name: pin-map
description: Pin mappings and peripheral tables for common microcontroller boards and shields. Use when writing firmware code that references GPIO pins, I2C, SPI, UART, or when connecting sensors/displays. Covers Arduino Uno, ESP32, and common shields/sensors.
---

# Pin Map

Reference for board pins, shields, and common peripherals.

## Usage

Read the relevant reference file for the board or shield you're working with:

- [Arduino Uno](references/arduino-uno.md)
- [ESP32 DevKit](references/esp32-devkit.md)
- [Multi-Function Shield](references/multi-function-shield.md)
- [Common Sensors](references/sensors.md)

## When to use

- Writing `pinMode()`, `digitalRead()`, `digitalWrite()` calls
- Connecting a sensor, display, or shield
- Setting up I2C, SPI, or UART
- User asks "which pin does X?"
