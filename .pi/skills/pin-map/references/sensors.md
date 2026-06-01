# Common Sensors and Peripherals

## DHT11 / DHT22 (Temperature + Humidity)

| Pin | Connection |
|-----|------------|
| VCC | 3.3V or 5V |
| DATA | Any digital pin (with 10K pullup) |
| GND | GND |

Library: `DHT sensor library`

## HC-SR04 (Ultrasonic Distance)

| Pin | Connection |
|-----|------------|
| VCC | 5V |
| TRIG | Any digital pin |
| ECHO | Any digital pin |
| GND | GND |

```cpp
#define TRIG 9
#define ECHO 10
pinMode(TRIG, OUTPUT);
pinMode(ECHO, INPUT);
digitalWrite(TRIG, LOW); delayMicroseconds(2);
digitalWrite(TRIG, HIGH); delayMicroseconds(10);
digitalWrite(TRIG, LOW);
long duration = pulseIn(ECHO, HIGH);
float cm = duration * 0.034 / 2;
```

## SG90 Servo

| Pin | Connection |
|-----|------------|
| VCC | 5V (red) |
| GND | GND (brown) |
| Signal | PWM pin (orange) |

Library: `Servo.h`

## BMP280 / BME280 (Pressure/Temp/Humidity)

I2C address: 0x76 or 0x77

| Pin | Connection |
|-----|------------|
| VCC | 3.3V |
| GND | GND |
| SDA | A4 (Uno) / 21 (ESP32) |
| SCL | A5 (Uno) / 22 (ESP32) |

Library: `Adafruit BMP280` or `Adafruit BME280`

## SSD1306 OLED (128x64 I2C)

I2C address: 0x3C

| Pin | Connection |
|-----|------------|
| VCC | 3.3V |
| GND | GND |
| SDA | A4 (Uno) / 21 (ESP32) |
| SCL | A5 (Uno) / 22 (ESP32) |

Library: `Adafruit SSD1306` + `Adafruit GFX`

## PIR Motion Sensor (HC-SR501)

| Pin | Connection |
|-----|------------|
| VCC | 5V |
| OUT | Any digital pin |
| GND | GND |

```cpp
pinMode(7, INPUT);
bool motion = digitalRead(7) == HIGH;
```

## LDR (Light Dependent Resistor)

Voltage divider: LDR + 10K resistor to GND, junction to analog pin.

```cpp
int light = analogRead(A0); // 0=dark, 1023=bright
```

## WS2812B / NeoPixel LED Strip

| Pin | Connection |
|-----|------------|
| 5V | External 5V (not Arduino 5V for long strips) |
| DIN | Any digital pin (with 470Ω resistor) |
| GND | GND (common with power supply) |

Library: `Adafruit NeoPixel`

## NRF24L01 (2.4GHz Radio)

SPI + 2 extra pins:

| Pin | Connection (Uno) |
|-----|------------------|
| VCC | 3.3V (not 5V!) |
| GND | GND |
| CE | Any digital pin (e.g. 9) |
| CSN | Any digital pin (e.g. 10) |
| SCK | 13 |
| MOSI | 11 |
| MISO | 12 |

Library: `RF24`
