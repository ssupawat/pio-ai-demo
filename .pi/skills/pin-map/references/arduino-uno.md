# Arduino Uno R3 Pin Map

## ATmega328P

- 14 digital pins (0–13)
- 6 analog inputs (A0–A5)
- 2KB RAM, 32KB Flash, 16MHz clock

## Digital Pins

| Pin | Special Functions | Notes |
|-----|-------------------|-------|
| 0 | RX (UART) | Don't use if serial debug active |
| 1 | TX (UART) | Don't use if serial debug active |
| 2 | INT0 | External interrupt |
| 3 | INT1, PWM (~) | External interrupt, PWM |
| 4 | | |
| 5 | PWM (~) | |
| 6 | PWM (~) | |
| 7 | | |
| 8 | | |
| 9 | PWM (~) | |
| 10 | PWM (~), SS (SPI) | |
| 11 | PWM (~), MOSI (SPI) | |
| 12 | MISO (SPI) | |
| 13 | SCK (SPI), LED | Built-in LED |

## Analog Pins

| Pin | Special Functions |
|-----|-------------------|
| A0 | ADC0 |
| A1 | ADC1 |
| A2 | ADC2 |
| A3 | ADC3 |
| A4 | ADC4, SDA (I2C) |
| A5 | ADC5, SCL (I2C) |

## Power

| Pin | Voltage |
|-----|---------|
| 5V | 5V output |
| 3.3V | 3.3V output (50mA max) |
| GND | Ground (multiple pins) |
| VIN | External power input (7-12V recommended) |
| IOREF | Logic level reference (5V) |
| AREF | Analog reference voltage |

## Communication

| Bus | Pins | Notes |
|-----|------|-------|
| UART | 0 (RX), 1 (TX) | Used by Serial |
| I2C | A4 (SDA), A5 (SCL) | Wire library |
| SPI | 10 (SS), 11 (MOSI), 12 (MISO), 13 (SCK) | SPI library |

## PWM

Pins 3, 5, 6, 9, 10, 11 (8-bit, ~490Hz default)

## External Interrupts

Pins 2 (INT0), 3 (INT1)
