#include <Arduino.h>

// Multi-Function Shield - Reaction Game
// A random LED lights up. Press the matching button (BTN1-3) as fast as you can.
// BTN1=LED2, BTN2=LED3, BTN3=LED4

#define LED1 13  // unused
#define LED2 12  // target for BTN1
#define LED3 11  // target for BTN2
#define LED4 10  // target for BTN3
#define BTN1 A1
#define BTN2 A2
#define BTN3 A3
#define BUZZER 3

const int targetLeds[] = {LED2, LED3, LED4};
const int targetBtns[] = {BTN1, BTN2, BTN3};
const char* btnNames[] = {"BTN1", "BTN2", "BTN3"};

enum State { WAITING, COUNTDOWN, SHOW_TARGET, WAIT_PRESS, RESULT };
State state = WAITING;
int target = 0;
unsigned long targetTime = 0;
unsigned long reactionTime = 0;
int roundNum = 0;
int bestTime = 9999;

void allLedsOff() {
  for (int i = 0; i < 4; i++) {
    pinMode(i + 10, OUTPUT);
    digitalWrite(i + 10, HIGH);
  }
}

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 3; i++) pinMode(targetBtns[i], INPUT_PULLUP);
  pinMode(BUZZER, OUTPUT);
  digitalWrite(BUZZER, HIGH); // buzzer OFF
  allLedsOff();
  randomSeed(analogRead(A5)); // seed from floating pin
  Serial.println("=== Reaction Game ===");
  Serial.println("Press any button to start a round");
}

void loop() {
  switch (state) {

    case WAITING:
      // Wait for any button press to start
      for (int i = 0; i < 3; i++) {
        if (digitalRead(targetBtns[i]) == LOW) {
          delay(50); // debounce
          state = COUNTDOWN;
          roundNum++;
          Serial.print("\n--- Round ");
          Serial.print(roundNum);
          Serial.println(" ---");
          Serial.println("Get ready...");
          targetTime = millis();
        }
      }
      break;

    case COUNTDOWN:
      // Random delay 1-3 seconds before showing target
      if (millis() - targetTime > random(1000, 3000)) {
        target = random(0, 3);
        digitalWrite(targetLeds[target], LOW); // ON
        state = SHOW_TARGET;
        targetTime = millis();
        Serial.print("GO! Press ");
        Serial.println(btnNames[target]);
      }
      break;

    case SHOW_TARGET:
    case WAIT_PRESS:
      state = WAIT_PRESS;
      // Check for button press
      for (int i = 0; i < 3; i++) {
        if (digitalRead(targetBtns[i]) == LOW) {
          reactionTime = millis() - targetTime;
          delay(50); // debounce

          allLedsOff();

          if (i == target) {
            Serial.print("HIT! Reaction: ");
            Serial.print(reactionTime);
            Serial.println("ms");
            if (reactionTime < bestTime) {
              bestTime = reactionTime;
              Serial.print(">> New best! <<");
            }
          } else {
            Serial.print("MISS! You pressed ");
            Serial.print(btnNames[i]);
            Serial.print(" but target was ");
            Serial.println(btnNames[target]);
          }

          Serial.print("Best: ");
          Serial.print(bestTime);
          Serial.println("ms");
          Serial.println("Press any button for next round");

          state = WAITING;
          break;
        }
      }

      // Timeout after 3 seconds
      if (state == WAIT_PRESS && millis() - targetTime > 3000) {
        allLedsOff();
        Serial.println("TIMEOUT! Too slow.");
        Serial.println("Press any button for next round");
        state = WAITING;
      }
      break;

    case RESULT:
      break;
  }
}
