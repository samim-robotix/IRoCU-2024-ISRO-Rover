#include <Wire.h>

// Define slave address (0x09 for this example)
const int slaveAddress = 0x09;

void setup() {
  // Initialize I2C communication as slave
  Wire.begin(slaveAddress);
  Serial.begin(9600);  // Optional: uncomment for serial communication

  // Register event handler for receiving data
  Wire.onReceive(receiveEvent);
  Serial.println("Arduino Slave Ready");
}

void loop() {
  // No blocking code needed here, data reception handled in interrupt
}

// Interrupt function called when data is received from master
void receiveEvent(int howMany) {
  if (Wire.available() > 0) {  // Check if data is available
    byte data[howMany];
    Wire.readBytes(data, howMany);  // Read received data

    // Process received data
    Serial.print("Received data: ");
    for (int i = 0; i < howMany; i++) {
      Serial.print(data[i]);
      Serial.print(" ");
    }
    Serial.println();

    // Send acknowledgement message (replace with your actual acknowledgement data)
    byte ackData = 0xAF;  // Replace with your desired acknowledgement byte
    Wire.write(ackData);

    Serial.println("Sent acknowledgement message");
  }
}
