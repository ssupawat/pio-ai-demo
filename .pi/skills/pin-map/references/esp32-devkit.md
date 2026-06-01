# ESP32 DevKit Pin Map

## ESP32-WROOM-32

- 34 GPIO pins
- 520KB RAM, 4MB Flash typical, 240MHz dual-core
- Built-in Wi-Fi + Bluetooth

## Safe to Use

| Pin | Notes |
|-----|-------|
| 2 | Built-in LED, safe |
| 4 | Safe |
| 5 | Safe |
| 12 | Must be LOW during boot (MTDI) |
| 13 | Safe |
| 14 | Safe |
| 15 | Safe |
| 16 | Safe (UART2 RX) |
| 17 | Safe (UART2 TX) |
| 18 | Safe (SPI SCK) |
| 19 | Safe (SPI MISO) |
| 21 | I2C SDA (default) |
| 22 | I2C SCL (default) |
| 23 | SPI MOSI |
| 25 | DAC1 |
| 26 | DAC2 |
| 27 | Safe |
| 32 | Safe, ADC1 |
| 33 | Safe, ADC1 |
| 34 | Input only, ADC1 |
| 35 | Input only, ADC1 |
| 36 | Input only, ADC1 (VP) |
| 39 | Input only, ADC1 (VN) |

## DO NOT USE (or with caution)

| Pin | Reason |
|-----|--------|
| 0 | Boot button, must be HIGH at boot |
| 1 | TX0 (debug serial) |
| 3 | RX0 (debug serial) |
| 6 | Connected to internal flash |
| 7 | Connected to internal flash |
| 8 | Connected to internal flash |
| 9 | Connected to internal flash |
| 10 | Connected to internal flash |
| 11 | Connected to internal flash |
| 12 | Boot mode select (must be LOW at boot) |
| 15 | Boot message enable (must be HIGH at boot) |

## Default I2C

| Function | Pin |
|----------|-----|
| SDA | 21 |
| SCL | 22 |

## Default SPI (VSPI)

| Function | Pin |
|----------|-----|
| MOSI | 23 |
| MISO | 19 |
| SCK | 18 |
| SS | 5 |

## Default UART

| Port | TX | RX |
|------|----|----|
| UART0 (debug) | 1 | 3 |
| UART1 | 10 | 9 (conflicts with flash) |
| UART2 | 17 | 16 |

## ADC

- ADC1: CH0–CH7 (GPIO 32–39) — works with Wi-Fi on
- ADC2: CH0–CH9 (GPIO 0, 2, 4, 12–15, 25–27) — unreliable with Wi-Fi on

## DAC

GPIO 25 (DAC1), GPIO 26 (DAC2) — 8-bit, 0–3.3V
