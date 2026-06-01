# Multi-Function Shield for Arduino Uno

Common shield with LEDs, buttons, buzzer, potentiometer, and 4-digit 7-segment display.

## Pin Map

| Component | Pin | Type | Active | Notes |
|-----------|-----|------|--------|-------|
| LED1 | 13 | Digital OUT | LOW = ON | |
| LED2 | 12 | Digital OUT | LOW = ON | |
| LED3 | 11 | Digital OUT | LOW = ON | |
| LED4 | 10 | Digital OUT | LOW = ON | |
| BTN1 | A1 | Digital IN | LOW = pressed | Use INPUT_PULLUP |
| BTN2 | A2 | Digital IN | LOW = pressed | Use INPUT_PULLUP |
| BTN3 | A3 | Digital IN | LOW = pressed | Use INPUT_PULLUP |
| Potentiometer | A0 | Analog IN | 0–1023 | 10K trim pot |
| Buzzer | 3 | Digital OUT | LOW = ON (loud) | HIGH = silent |

## 7-Segment Display (74HC595 shift registers)

Two cascaded 74HC595 chips drive the 4-digit common anode display.

| Function | Pin |
|----------|-----|
| Latch (ST_CP) | 4 |
| Clock (SH_CP) | 7 |
| Data (DS) | 8 |

### Segment byte format (MSBFIRST, common anode)

LOW = segment ON, HIGH = segment OFF

| Bit | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
|-----|---|---|---|---|---|---|---|---|
| Seg | dp | g | f | e | d | c | b | a |

### Digit values

| Char | Hex | Char | Hex |
|------|-----|------|-----|
| 0 | 0xC0 | 8 | 0x80 |
| 1 | 0xF9 | 9 | 0x90 |
| 2 | 0xA4 | A | 0x88 |
| 3 | 0xB0 | b | 0x83 |
| 4 | 0x99 | C | 0xC6 |
| 5 | 0x92 | d | 0xA1 |
| 6 | 0x82 | E | 0x86 |
| 7 | 0xF8 | F | 0x8E |
| OFF | 0xFF | | |

### Digit select bytes

| Digit | Select Byte |
|-------|-------------|
| 1 (leftmost) | 0xF1 |
| 2 | 0xF2 |
| 3 | 0xF3 |
| 4 (rightmost) | 0xF8 |

### Send data

```cpp
void sendToSegment(byte digitSelect, byte segValue) {
  digitalWrite(LATCH_PIN, LOW);
  shiftOut(DATA_PIN, CLK_PIN, MSBFIRST, segValue);
  shiftOut(DATA_PIN, CLK_PIN, MSBFIRST, digitSelect);
  digitalWrite(LATCH_PIN, HIGH);
}
```

## Code template

```cpp
// LEDs (active LOW)
const int leds[] = {13, 12, 11, 10};
for (int i = 0; i < 4; i++) {
  pinMode(leds[i], OUTPUT);
  digitalWrite(leds[i], HIGH); // OFF
}
// Turn on: digitalWrite(leds[i], LOW);

// Buttons (active LOW, use pullup)
const int btns[] = {A1, A2, A3};
for (int i = 0; i < 3; i++) {
  pinMode(btns[i], INPUT_PULLUP);
}
// Pressed: digitalRead(btns[i]) == LOW

// Potentiometer
int val = analogRead(A0); // 0-1023

// Buzzer (active LOW)
#define BUZZER 3
pinMode(BUZZER, OUTPUT);
digitalWrite(BUZZER, HIGH); // OFF (silent)
// digitalWrite(BUZZER, LOW); // ON (loud)
```
