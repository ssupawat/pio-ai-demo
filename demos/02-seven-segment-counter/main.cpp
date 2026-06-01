#include <Arduino.h>

// Multi-Function Shield - 7-Segment Counter
// Displays a counter (0-9999) on the 4-digit 7-segment display.
// BTN1: pause/resume  BTN2: reset  BTN3: count up faster
// Pot (A0): controls counting speed

#define LATCH_PIN 4
#define CLK_PIN   7
#define DATA_PIN  8
#define BTN1 A1
#define BTN2 A2
#define BTN3 A3
#define POT  A0

const byte SEGMENT_MAP[] = {
  0xC0, // 0
  0xF9, // 1
  0xA4, // 2
  0xB0, // 3
  0x99, // 4
  0x92, // 5
  0x82, // 6
  0xF8, // 7
  0x80, // 8
  0x90, // 9
};
#define SEG_OFF 0xFF

const byte DIGIT_SELECT[] = {0xF1, 0xF2, 0xF4, 0xF8};

byte displayBuf[4] = {0, 0, 0, 0};
byte displayOn[4] = {0, 0, 0, 0};

int counter = 0;
bool paused = false;
unsigned long lastCount = 0;
int countDelay = 500;

void sendToSegment(byte digitSelect, byte segValue) {
  digitalWrite(LATCH_PIN, LOW);
  shiftOut(DATA_PIN, CLK_PIN, MSBFIRST, segValue);
  shiftOut(DATA_PIN, CLK_PIN, MSBFIRST, digitSelect);
  digitalWrite(LATCH_PIN, HIGH);
}

void updateDisplayBuffer(int value) {
  if (value < 0) value = 0;
  if (value > 9999) value = 9999;

  displayBuf[0] = value / 1000;
  displayBuf[1] = (value / 100) % 10;
  displayBuf[2] = (value / 10) % 10;
  displayBuf[3] = value % 10;

  for (int i = 0; i < 4; i++) displayOn[i] = 1;
  if (value < 1000) displayOn[0] = 0;
  if (value < 100)  displayOn[1] = 0;
  if (value < 10)   displayOn[2] = 0;
  displayOn[3] = 1;
}

bool readButton(int pin) {
  static unsigned long lastPress[3] = {0, 0, 0};
  int idx = pin - A1;
  if (digitalRead(pin) == LOW && millis() - lastPress[idx] > 250) {
    lastPress[idx] = millis();
    return true;
  }
  return false;
}

void setup() {
  Serial.begin(9600);
  pinMode(LATCH_PIN, OUTPUT);
  pinMode(CLK_PIN, OUTPUT);
  pinMode(DATA_PIN, OUTPUT);
  pinMode(BTN1, INPUT_PULLUP);
  pinMode(BTN2, INPUT_PULLUP);
  pinMode(BTN3, INPUT_PULLUP);
  updateDisplayBuffer(0);
  Serial.println("=== 7-Segment Counter ===");
  Serial.println("BTN1: pause/resume");
  Serial.println("BTN2: reset");
  Serial.println("BTN3: speed up");
  Serial.println("Pot:  speed control");
}

void loop() {
  int potVal = analogRead(POT);
  countDelay = map(potVal, 0, 1023, 1000, 100);

  if (readButton(BTN1)) {
    paused = !paused;
    Serial.println(paused ? "PAUSED" : "RUNNING");
  }
  if (readButton(BTN2)) {
    counter = 0;
    updateDisplayBuffer(counter);
    Serial.println("RESET");
  }
  if (readButton(BTN3)) {
    counter += 100;
    if (counter > 9999) counter = 0;
    updateDisplayBuffer(counter);
    Serial.print("Jumped to: ");
    Serial.println(counter);
  }

  if (!paused && millis() - lastCount > countDelay) {
    counter++;
    if (counter > 9999) counter = 0;
    updateDisplayBuffer(counter);
    lastCount = millis();
    if (counter % 10 == 0) {
      Serial.print("Count: ");
      Serial.print(counter);
      Serial.print(" | Speed: ");
      Serial.print(countDelay);
      Serial.println("ms");
    }
  }

  for (int i = 0; i < 4; i++) {
    if (displayOn[i]) {
      sendToSegment(DIGIT_SELECT[i], SEGMENT_MAP[displayBuf[i]]);
    } else {
      sendToSegment(DIGIT_SELECT[i], SEG_OFF);
    }
    delay(2);
    sendToSegment(DIGIT_SELECT[i], SEG_OFF);
  }
}
