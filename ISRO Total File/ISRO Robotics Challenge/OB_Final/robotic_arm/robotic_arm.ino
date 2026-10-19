#include <Arduino.h>
#include "Servo.h"
#include "Wire.h"

TwoWire Wire1;

 //Servos
 Servo shoulder;
 Servo elbow;
 Servo pitch;
 Servo roll;

 //Gripper
 #define ENB 3
 #define DIRG 6 // Gripper
 #define PULG 12 // Gripper

 //Force sensor
#define F1 A0
#define F2 A1

// Limit switch
#define LIM 2

int ACK = 0;
int cmd = 900;

int sh_pos = 120;
int el_pos = 90;
int pit_pos = 0;
int rol_pos = 90;

void move_angle(Servo now, int angle, int p_angle);
void hold_position();
void digitalToggle(uint8_t pin);
void gripper_home();
void gripper_close();
void receiveEvent(int bytes);
void requestEvent(void);


void setup(){

  Serial.begin(9600);

  //attching servos
  shoulder.attach(8);
  elbow.attach(11);
  pitch.attach(10);
  roll.attach(9);

  //gripper
  pinMode(DIRG, OUTPUT);
  pinMode(PULG, OUTPUT);
  pinMode(ENB, OUTPUT);

  //Servo Homing
  shoulder.write(sh_pos);
  elbow.write(el_pos);
  pitch.write(pit_pos);
  roll.write(rol_pos);

  //gripper homing
  digitalWrite(ENB, HIGH);
  pinMode(LIM, INPUT_PULLUP);
  gripper_home();


  //i2c initialization
  Wire.begin(8);
  //a function to trigger when something is received.
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);

   delay(500);


}

void loop(){
  if (cmd>=100 && cmd<=280){
    
    move_angle(shoulder, cmd - 100, sh_pos);
    sh_pos = cmd - 100;
    ACK = cmd;
    cmd = 900;

  }

  else if (cmd>=300 && cmd<=480){

    move_angle(elbow, cmd - 300, el_pos);
    el_pos = cmd - 300;
    ACK = cmd;
    cmd = 900;
    
  }

  else if (cmd>=500 && cmd<=680){

    move_angle(pitch, cmd - 500, pit_pos);
    pit_pos = cmd - 500;
    ACK = cmd;
    cmd = 900;
    
  }
  else if (cmd>=700 && cmd<=880){
    move_angle(roll, cmd - 700, rol_pos);
    rol_pos = cmd - 700;
    ACK = cmd;
    cmd = 900;
  }

  else if (cmd==30){
    //gripper open
    gripper_home();
    ACK = cmd;
    cmd = 900;
  }
  else if (cmd==40){
    //gripper close
    gripper_close();
    ACK = cmd;
    cmd = 900;
    
  }
  else if (cmd==50){
    //pickup sequence
    
  }

  else if (cmd==60){
    //place sequence
    
  }

  else if (cmd==70){
    //holding position
    hold_position();
    ACK = cmd;
    cmd = 900;
    
  }


}

//---------------------------------------------------------------------
void move_angle(Servo now, int angle, int p_angle) {

  if (angle>=p_angle){
    for (int i = p_angle; i < angle; i++)
    {
      now.write(i);
      delay(50);
    }
  }

  else{
    for (int i = p_angle; i > angle; i--)
    {
      now.write(i);
      delay(50);
    }
  }

}

//---------------------------------------------------------------------
void hold_position(){
//holding position
  move_angle(shoulder, 120, sh_pos);
  sh_pos = 120;

  move_angle(elbow, 90, el_pos);
  el_pos = 90;

  move_angle(roll, 0, rol_pos);
  rol_pos = 0;

  move_angle(pitch, 90, pit_pos);
  pit_pos = 90;


}

//---------------------------------------------------------------------
void digitalToggle(uint8_t pin)
{
  int currentState = digitalRead(pin);
  digitalWrite(pin, !currentState);
}
//---------------------------------------------------------------------
void gripper_home()
{
  while (digitalRead(LIM) != 0)
  {
    digitalWrite(DIRG, HIGH);
    digitalToggle(PULG);
    delayMicroseconds(800);
  }
}
//---------------------------------------------------------------------
void gripper_close()
{
  bool grasp = false;
  while (grasp == false)
  {
    digitalWrite(DIRG, LOW);
    digitalToggle(PULG);
    delayMicroseconds(800);
    if (analogRead(F1) < 20 || analogRead(F2) < 20)
    {
      grasp = true;
      break;
    }
  }
}

//---------------------------------------------------------------------
void receiveEvent(int bytes)
{
  while (Wire.available())
  {
    cmd = Wire.read();   // receive byte as an integer
    Serial.println(cmd); // print the integer
  }
}

//---------------------------------------------------------------------

void requestEvent(void)
{
  Serial.println("Current Command: ");
  Wire.write(ACK);
  ACK = 0;
}



