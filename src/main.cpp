#include <Arduino.h>
#include <Servo.h>

// Pin definitions - modify these based on your wiring
#define SERVO_PIN 6        // PWM pin for servo
#define TRIG_PIN 9         // Trigger pin for ultrasonic sensor
#define ECHO_PIN 10         // Echo pin for ultrasonic sensor

// Create servo object
Servo radarServo;

// Configuration constants
const int ANGLE_STEP = 2;           // Degrees to move each step (1-5 recommended)
const int DELAY_TIME = 50;          // Delay between measurements (ms)
const int MIN_ANGLE = 0;            // Minimum servo angle
const int MAX_ANGLE = 180;          // Maximum servo angle
const unsigned long ECHO_TIMEOUT = 30000; // Ultrasonic timeout (microseconds)

// Variables for servo control
int currentAngle = MIN_ANGLE;       // Current servo position
int servoDirection = 1;             // 1 for counterclockwise, -1 for clockwise

// Variables for ultrasonic sensor
long duration;
float distance;

// Function declarations
float measureDistance();
void printSerialHeader();
void updateServoPosition();

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  while (!Serial) {
    ; // Wait for serial port to connect (needed for some boards)
  }
  
  // Initialize servo
  radarServo.attach(SERVO_PIN);
  radarServo.write(MIN_ANGLE); // Start at minimum angle
  
  // Initialize ultrasonic sensor pins
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  
  // Ensure trigger pin starts LOW
  digitalWrite(TRIG_PIN, LOW);
  
  // Wait for servo to reach initial position
  delay(1000);
  
  // Print startup information
  printSerialHeader();
}

void loop() {
  // Move servo to current angle
  radarServo.write(currentAngle);
  delay(DELAY_TIME); // Wait for servo to reach position and stabilize
  
  // Take ultrasonic measurement
  distance = measureDistance();
  
  // Output to serial in CSV format: Angle, Distance
  Serial.print(currentAngle);
  Serial.print(",");
  
  if (distance < 0) {
    Serial.println("OUT_OF_RANGE");
  } else {
    Serial.print(distance, 2); // 2 decimal places
    Serial.println();
  }
  
  // Update servo position for next iteration
  updateServoPosition();
}

float measureDistance() {
  // Ensure trigger pin is LOW
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  
  // Send a 10 microsecond HIGH pulse to trigger pin
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  
  // Read the echo pin and measure duration
  duration = pulseIn(ECHO_PIN, HIGH, ECHO_TIMEOUT);
  
  // Check for timeout (no echo received)
  if (duration == 0) {
    return -1.0; // Indicate no echo/out of range
  }
  
  // Calculate distance in centimeters
  // Speed of sound ≈ 343 m/s = 0.0343 cm/microsecond
  // Distance = (duration * speed_of_sound) / 2 (divide by 2 for round trip)
  float calculatedDistance = (duration * 0.0343) / 2.0;
  
  // Basic range validation (HC-SR04 typical range: 2cm - 400cm)
  if (calculatedDistance < 2.0 || calculatedDistance > 400.0) {
    return -1.0; // Out of sensor range
  }
  
  return calculatedDistance;
}

void updateServoPosition() {
  // Calculate next angle
  int nextAngle = currentAngle + (ANGLE_STEP * servoDirection);
  
  // Check boundaries and reverse direction if needed
  if (nextAngle >= MAX_ANGLE) {
    currentAngle = MAX_ANGLE;
    servoDirection = -1; // Change to clockwise
    Serial.println("# Direction: Clockwise");
  } 
  else if (nextAngle <= MIN_ANGLE) {
    currentAngle = MIN_ANGLE;
    servoDirection = 1; // Change to counterclockwise  
    Serial.println("# Direction: Counterclockwise");
  }
  else {
    currentAngle = nextAngle;
  }
}

void printSerialHeader() {
  Serial.println("# Arduino Ultrasonic Radar System");
  Serial.println("# PlatformIO Version");
  Serial.print("# Servo Range: ");
  Serial.print(MIN_ANGLE);
  Serial.print("° to ");
  Serial.print(MAX_ANGLE);
  Serial.println("°");
  Serial.print("# Step Size: ");
  Serial.print(ANGLE_STEP);
  Serial.println("°");
  Serial.print("# Delay: ");
  Serial.print(DELAY_TIME);
  Serial.println("ms");
  Serial.println("# Format: Angle,Distance_cm");
  Serial.println("# ========================");
  Serial.println("# Direction: Counterclockwise");
}