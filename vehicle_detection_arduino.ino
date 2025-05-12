#include <Servo.h>

// Ultrasonic sensors
#define trigPin1 2
#define echoPin1 3
#define trigPin2 4
#define echoPin2 5

// Servo + ESP32 trigger
#define servoPin 6
#define espTriggerPin 7  // OUTPUT to ESP32-CAM input pin

Servo myServo;

void setup() {
  Serial.begin(9600);

  // Set ultrasonic pins
  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);

  // Servo setup
  myServo.attach(servoPin);
  myServo.write(90); // Start at neutral

  // ESP32-CAM trigger pin
  pinMode(espTriggerPin, OUTPUT);
  digitalWrite(espTriggerPin, LOW); // Default LOW
}

// Measure distance using ultrasonic sensor
long readDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  return pulseIn(echoPin, HIGH) * 0.034 / 2;
}

// Trigger ESP32 to capture image
void triggerESP32() {
  digitalWrite(espTriggerPin, HIGH);
  delay(100); // Short HIGH pulse
  digitalWrite(espTriggerPin, LOW);
}

void loop() {
  long distance1 = readDistance(trigPin1, echoPin1);
  long distance2 = readDistance(trigPin2, echoPin2);

  Serial.print("Slot 1: ");
  Serial.print(distance1);
  Serial.print(" cm | Slot 2: ");
  Serial.print(distance2);
  Serial.println(" cm");

  if (distance1 < 5 && distance2 < 5) {
    Serial.println("Both slots occupied - scanning both");

    myServo.write(45); // Face Slot 1
    delay(1000);
    triggerESP32(); // Trigger capture
    Serial.println("Scanning Slot 1 - Waiting 10 seconds...");
    delay(10000);

    myServo.write(135); // Face Slot 2
    delay(1000);
    triggerESP32(); // Trigger capture
    Serial.println("Scanning Slot 2 - Waiting 10 seconds...");
    delay(10000);

    myServo.write(90); // Neutral
  }
  else if (distance1 < 5) {
    Serial.println("Slot 1 occupied - Scanning...");
    myServo.write(45);
    delay(1000);
    triggerESP32();
    delay(10000);
    myServo.write(90);
  }
  else if (distance2 < 5) {
    Serial.println("Slot 2 occupied - Scanning...");
    myServo.write(135);
    delay(1000);
    triggerESP32();
    delay(10000);
    myServo.write(90);
  }
  else {
    myServo.write(90);
    Serial.println("No vehicle - Servo at neutral");
  }

  delay(1000); // Delay between cycles
}
