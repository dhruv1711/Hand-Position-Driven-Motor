#include <Stepper.h>
// Define number of steps per rotation:
const int stepsPerRevolution = 2048;
// Wiring:
// Pin 9 to IN1 on the ULN2003 driver
// Pin 10 to IN2 on the ULN2003 driver
// Pin 11 to IN3 on the ULN2003 driver
// Pin 12 to IN4 on the ULN2003 driver
// Create stepper object called 'myStepper', note the pin order:
Stepper myStepper = Stepper(stepsPerRevolution, 9, 10, 11, 12);
void setup() {
  // Set the speed to 10 rpm:
  myStepper.setSpeed(10);
  
  // Begin Serial communication at a baud rate of 9600:
  Serial.begin(9600);
  while(!Serial){
    ;
    }
}

int num;

void loop() {
  // Step one revolution in one direction:
  if (Serial.available()>0){
    num = Serial.read();
  }
  
  if(num=='1'){
  Serial.println("clockwise");
  myStepper.step(stepsPerRevolution);
  }
  if(num=='0'){
    Serial.println("stop");
  }
}
