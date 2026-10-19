#include <Arduino.h>
#include <math.h>

// Define constants
const float h = 0.001; // Step size
const int t_final = 20000; // Final time in milliseconds (20 seconds)
const float l1 = 0.22839; // Length of link 1
const float l2 = 0.248;   // Length of link 2

// Initial values
float th4 = 0.17; // 10 degrees
float th5 = 0.26; // 15 degrees

// Iteration counter
int iter = 0;

// Initial position of the end effector
float qx = 0.001; // X-coordinate of the end effector
float qy = 0.001; // Y-coordinate of the end effector
float qz = 0.001; // Z-coordinate of the end effector

// Function to convert radians to degrees
float rad2deg(float rad) {
  return rad * 180.0 / PI;
}

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Update iteration counter
  iter++;

  // Calculate initial joint angles
  float th1 = atan2(qy, qx);
  float th3 = acos((qx * qx + qy * qy + qz * qz - l1 * l1 - l2 * l2) / (2 * l1 * l2));
  float th2 = atan2((l1 + l2 * cos(th3)), (l2 * sin(th3))) + atan2((qx * cos(th1) + qy * sin(th1)), qz);

  // Calculate rotation matrix elements
  float r11 = cos(th1) * cos(th2 + th3 + th4) * cos(th5) - sin(th1) * sin(th5);
  float r12 = -cos(th1) * cos(th2 + th3 + th4) * sin(th5) - sin(th1) * cos(th5);
  float r13 = cos(th1) * sin(th2 + th3 + th4);
  float r21 = sin(th1) * cos(th2 + th3 + th4) * cos(th5) + cos(th1) * sin(th5);
  float r22 = -sin(th1) * cos(th2 + th3 + th4) * sin(th5) + cos(th1) * cos(th5);
  float r23 = sin(th1) * sin(th2 + th3 + th4);
  float r31 = -sin(th2 + th3 + th4) * cos(th5);
  float r32 = sin(th2 + th3 + th4) * sin(th5);
  float r33 = cos(th2 + th3 + th4);

  // Update end effector position
  qx += h / 6000;
  qy += h / 6000;
  qz += h / 6000;

  // Calculate new joint angles
  th1 = atan2(qy, qx);
  th2 = atan2((l1 + l2 * cos(th3)), (l2 * sin(th3))) + atan2((qx * cos(th1) + qy * sin(th1)), qz);
  th3 = acos((qx * qx + qy * qy + qz * qz - l1 * l1 - l2 * l2) / (2 * l1 * l2));
  th4 = atan2((r13 * cos(th1) + r23 * sin(th1)), r33) - th2 - th3;
  th5 = (r12 * cos(th1) - r11 * sin(th1)) / (r22 * cos(th1) - r21 * sin(th1));

  // Print or use the calculated angles and positions
  Serial.print("th1: ");
  Serial.println(rad2deg(th1));
  // Similar print statements for th2, th3, th4, th5, qx, qy, qz

  // Check if end effector reaches the desired position
  if (qx >= 10 && qy >= 10 && qz >= 10) {
    Serial.println("End effector reached desired position.");
    while (true); // Infinite loop to halt further execution
  }

  // Delay to control simulation speed
  delay(h);
}
