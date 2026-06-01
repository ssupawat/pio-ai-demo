#include <Arduino.h>

#define LED1 13
#define LED2 12
#define LED3 11
#define LED4 10
#define BTN1 A1

const int leds[] = {LED1, LED2, LED3, LED4};
const char* patternNames[] = {"Knight Rider", "Binary Counter", "All Blink"};
int currentPattern = 0;
int step = 0;
int direction = 1;
unsigned long lastStep = 0;
const unsigned long STEP_DELAY = 200;

bool buttonPressed() {
  static bool lastState = HIGH;
  bool state = digitalRead(BTN1);
  if (state == LOW && lastState == HIGH) {
    lastState = state;
    delay(50);
    return true;
  }
  lastState = state;
  return false;
}

void allLedsOff() {
  for (int i = 0; i < 4; i++) digitalWrite(leds[i], HIGH);
}

void allLedsOn() {
  for (int i = 0; i < 4; i++) digitalWrite(leds[i], LOW);
}

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 4; i++) pinMode(leds[i], OUTPUT);
  pinMode(BTN1, INPUT_PULLUP);
  allLedsOff();
  Serial.println("=== LED Patterns ===");
  Serial.println("Pattern: Knight Rider");
  Serial.println("Press BTN1 to switch pattern");
}

void loop() {
  if (buttonPressed()) {
    currentPattern = (currentPattern + 1) % 3;
    step = 0;
    direction = 1;
    allLedsOff();
    Serial.print("Pattern: ");
    Serial.println(patternNames[currentPattern]);
  }

  if (millis() - lastStep < STEP_DELAY) return;
  lastStep = millis();

  switch (currentPattern) {
    case 0:
      allLedsOff();
      digitalWrite(leds[step], LOW);
      step += direction;
      if (step >= 3 || step <= 0) direction = -direction;
      break;

    case 1:
      allLedsOff();
      for (int i = 0; i < 4; i++) {
        if (step & (1 << i)) digitalWrite(leds[i], LOW);
      }
      step = (step + 1) % 16;
      break;

    case 2:
      if (step % 2 == 0) allLedsOn();
      else allLedsOff();
      step++;
      break;
  }
}
