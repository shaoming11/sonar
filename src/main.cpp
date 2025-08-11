#include <Arduino.h>
#include <Servo.h>

// constants
const int trigPin = 9;
const int echoPin = 10;

// variables
float duration, distance;
String output;
char userInput;
Servo myservo;
int pos = 0;
int posChange = 3;

// put function declarations here:
void handleEcho();
void handleServo();
void handleStop();

void setup() {
    // initialize digital pin LED_BUILTIN as an output.
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);

    myservo.attach(6);

    Serial.begin(9600);
}

// the loop function runs over and over again forever
void loop() {
    handleServo();
    handleEcho();
    handleStop();

    Serial.println(Serial.available());
    if (Serial.available() > 0) {
        userInput = Serial.read();
        Serial.println(userInput)
    }
}
// put function definitions here:
void handleEcho() {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    duration = pulseIn(echoPin, HIGH);
    distance = (duration*0.0343)/2; // distance in cm
    delay(100);
}

void handleServo() {
    if (pos <= 0) {
      posChange = 3;
    }

    if (pos >= 180) {
      posChange = -3;
    }
    pos += posChange;
    myservo.write(pos);
    delay(15);
}

void handleStop() {
  if (Serial.available()) {
    String command = Serial.readString();
    command.trim();
    
    if (command.equals("STOP")) {
      Serial.println("Program stopped!");
      while(1) {
        delay(1000);  // Infinite loop stops program
      }
    }
  }
}