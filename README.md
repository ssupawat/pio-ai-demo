# Firmware Development on the CLI

When you develop firmware entirely from the command line, an AI coding agent can help you at every stage.

No GUI. No drag-and-drop. Just shell commands that an agent can read, edit, run, and react to.

This repo was built with [pi.dev](https://pi.dev), a CLI coding agent that drives the entire development loop via natural language.

## The loop

```
Understand the board → Write code → Build → Flash → Monitor → Debug → Repeat
```

Every step happens in the terminal. Every step is something an agent can do.

## Agent skills

This repo includes pi agent skills in `.pi/skills/` that handle the practical work:

- **board-detect**: identifies the connected board via USB
- **pin-map**: pin tables for Arduino Uno, ESP32, shields, and sensors
- **firmware-upload**: flashes firmware with CH340 clone workaround

When you tell pi "which board is connected?", "what's pin A0?", or "upload the led demo", it uses these skills.

## What's here

Three PlatformIO demos for Arduino Uno R3 with a multi-function shield, each a standalone project inside `demos/`.

| Demo | What it teaches |
|------|-----------------|
| LED Patterns | Digital output, button input, timing without delay() |
| 7-Segment Counter | Shift register cascade, multiplexing, analog input |
| Reaction Game | State machine, multiple inputs, serial output |

## GPIO map

| Component | Pin | Notes |
|-----------|-----|-------|
| LED1–4 | 13, 12, 11, 10 | Active LOW |
| BTN1–3 | A1, A2, A3 | Active LOW, INPUT_PULLUP |
| Potentiometer | A0 | 0–1023 |
| Buzzer | 3 | Active LOW |
| 7-Segment | 4, 7, 8 | 74HC595, common anode |

## Known quirks

CH340 clone boards: `pio run -t upload` never works because the DTR auto-reset circuit doesn't trigger reliably. The firmware-upload skill pulses DTR manually via pyserial and retries.

macOS: After heavy serial communication, the CH340 driver state corrupts. DTR stops working. Only a reboot fixes it.
