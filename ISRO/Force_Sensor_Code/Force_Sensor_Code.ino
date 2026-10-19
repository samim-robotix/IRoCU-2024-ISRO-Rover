const int forceSensorPin = A0; // Analog pin connected to the force sensor
const int ledPin = 13; // LED pin for visual feedback

void setup() {
  Serial.begin(9600); // Initialize serial communication
  pinMode(ledPin, OUTPUT); // Set LED pin as output
}

void loop() {
  // Read the voltage from the force sensor
  int sensorValue = analogRead(forceSensorPin);

  // Map the sensor value to a range (0-1023) to a force range (0-100)
  int force = map(sensorValue, 0, 1023, 0, 100);

  // Print the force value to the Serial Monitor
  Serial.print("Force: ");
  Serial.print(force);
  Serial.println("%");

  // Turn on LED if force exceeds a threshold (for visual feedback)
  if (force > 50) {
    digitalWrite(ledPin, HIGH);
  } else {
    digitalWrite(ledPin, LOW);
  }

  delay(100); // Delay for stability, adjust as needed
}
