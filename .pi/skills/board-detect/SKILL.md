---
name: board-detect
description: Detect connected Arduino/ESP32 boards via USB. Returns board name, PlatformIO board ID, serial port, and USB chip. Use when starting a firmware project, before flashing, or when the user says "detect my board" or "what board is connected".
---

# Board Detect

Identifies connected microcontroller boards via USB.

## Usage

```bash
python3 scripts/detect.py
```

Output is JSON:
```json
{
  "port": "/dev/cu.usbserial-110",
  "board_name": "Arduino Uno R3 (CH340 clone)",
  "platformio_id": "uno",
  "usb_chip": "CH340G",
  "vid": "0x1A86",
  "pid": "0x7523",
  "framework": "arduino",
  "upload_note": "CH340 clone — use upload-ch340.py instead of pio run -t upload"
}
```

## How it works

1. Scans USB devices via `ioreg` (macOS)
2. Matches VID/PID against known board database
3. Finds the corresponding serial port
4. Returns PlatformIO-compatible board info

## Known boards

| VID | PID | Board | PlatformIO ID | USB Chip | Upload |
|-----|-----|-------|---------------|----------|--------|
| 0x2341 | 0x0043 | Arduino Uno R3 (genuine) | uno | ATmega16U2 | pio run -t upload |
| 0x1A86 | 0x7523 | Arduino Uno R3 (CH340 clone) | uno | CH340G | upload-ch340.py |
| 0x1A86 | 0x1A86 | Arduino Nano (CH340 clone) | nanoatmega328 | CH340G | upload-ch340.py |
| 0x2341 | 0x0243 | Arduino Mega 2560 | megaatmega2560 | ATmega16U2 | pio run -t upload |
| 0x0403 | 0x6001 | Arduino clone (FTDI) | various | FT232RL | pio run -t upload |
| 0x10C4 | 0xEA60 | Arduino clone (CP2102) | various | CP2102 | upload-ch340.py |
| 0x2341 | 0x8015 | Arduino Leonardo | leonardo | ATmega32U4 | pio run -t upload |
| 0x239A | 0x8012 | Adafruit Feather M4 | adafruit_feather_m4 | ATSAMD51 | pio run -t upload |
| 0x303A | 0x1001 | ESP32-S3 (native USB) | esp32-s3-devkitc-1 | ESP32-S3 USB | pio run -t upload |
| 0x10C4 | 0xEA60 | ESP32 (CP2102) | esp32dev | CP2102 | upload-ch340.py |

## When to use

- User asks "what board do I have?"
- Before running `pio project init --board <id>`
- Before uploading (to choose upload method)
- When debugging connection issues
