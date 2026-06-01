---
name: firmware-upload
description: Upload firmware to Arduino boards. Handles CH340 clone quirks (DTR pulse, serial port cleanup, retry logic). Use when flashing firmware to an Arduino or ESP32 board.
---

# Firmware Upload

Uploads firmware to Arduino boards with CH340 clone workaround.

## Before uploading

The serial port can only be used by one process. **Always clean up first:**

1. Kill tmux sessions:
```bash
tmux kill-session -t serial 2>/dev/null
```

2. Kill monitor/avrdude processes:
```bash
pkill -f "pio device monitor" 2>/dev/null
pkill -f "avrdude" 2>/dev/null
```

3. Wait briefly:
```bash
sleep 1
```

## Upload

### Genuine Arduino (usbmodem)

```bash
cd <demo-dir> && pio run -t upload
```

### CH340 clone (usbserial)

`pio run -t upload` does NOT work on CH340 clones. Use the upload script:

```bash
python3 scripts/upload.py <demo-dir>
```

The script auto-detects the serial port, kills monitors, pulses DTR, and retries up to 5 times.

## Detecting the board

Use the board-detect skill, or manually:

```bash
# Find serial port
ls /dev/cu.usbserial* /dev/cu.usbmodem* 2>/dev/null

# usbmodem* → genuine Arduino → pio run -t upload
# usbserial* → CH340 clone → python3 scripts/upload.py <demo-dir>
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `stk500_getsync() not in sync` | DTR pulse missed. Retry or reboot. |
| `tcsetattr() failed` | CH340 driver corrupted. **Reboot Mac.** |
| `port is busy` | Kill monitor/tmux sessions first. |
| Upload keeps failing after retries | **Reboot Mac** — driver state corrupted. |
| `No CH340 serial port found` | Board not plugged in or different chip. |

## Key rules

1. **Always kill serial monitor before uploading**
2. **CH340 clones need upload script — `pio run -t upload` never works**
3. **If all retries fail, tell user to reboot**
4. **After reboot, upload immediately — don't start a monitor first**
