#include <Arduino.h>

// constants
const int trigPin = 9;
const int echoPin = 10;

// variables
float duration, distance;

// put function declarations here:
void handleEcho();

void setup() {
    // initialize digital pin LED_BUILTIN as an output.
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
    Serial.begin(9600);
}

// the loop function runs over and over again forever
void loop() {
    handleEcho();
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
    Serial.print("\nDistance: ");
    Serial.print(distance);
    delay(100);
}