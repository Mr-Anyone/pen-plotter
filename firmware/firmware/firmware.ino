#include <Servo.h>
#include "path.h"

// math theta to angle servo
// for back motor: angle = theta 
// for fron motor: angle = 90 - theta

constexpr int FRONT_MOTOR_DATA_PIN = 10; 
constexpr int BACK_MOTOR_DATA_PIN = 9; 
constexpr int PEN_LIFTER_MOTOR = 11;
constexpr int SECOND_IN_MILLISECOND = 1000;

Servo frontServo; 
Servo penLifterServo;
Servo backServo;

void setup() {
  frontServo.attach(FRONT_MOTOR_DATA_PIN);
  backServo.attach(BACK_MOTOR_DATA_PIN);
  penLifterServo.attach(PEN_LIFTER_MOTOR);

  // default position
  frontServo.write(90); 
  backServo.write(90);
}

// void calibrateMotors(){
//   frontServo.write(90);
//   backServo.write(0); 
// }

// void draw_circle(double seconds){
//   double delay_time = seconds / 180;
//   for(int i =0; i<180; ++i){
//     backServo.write(i); 
//     delay(delay_time * SECOND_IN_MILLISECOND);
//   }
// }

// void test_pen_lifter(){
//   penLifterServo.write(90); // lifting up the pen
//   draw_circle(5); 
//   penLifterServo.write(90); // lifting up the pen
//   draw_circle(0);
// }

// void main_loop(){
//   for(int i =0; i<180; ++i){
//     backServo.write(i); 
//     delay(0.1 * SECOND_IN_MILLISECOND);
//   }
// }

// void solve_length(){
//   Serial.println("writing front: 0 back 0");
//   frontServo.write(90); // 0 and 0 degree 
//   backServo.write(0);
//   delay(10 * SECOND_IN_MILLISECOND); 

//   frontServo.write(80); // 10 and 10 degree 
//   backServo.write(10);
//   Serial.println("writing front: 10 back 10");

//   delay(10 * SECOND_IN_MILLISECOND); 

// }

void print_path(){
  for(int i = 0; i<sizeof(path)/ sizeof(char);  i+= 2){
    int front_servo_angle =  path[i];
    int back_servo_angle = path[i +1]; 

    frontServo.write(front_servo_angle); 
    backServo.write(back_servo_angle);
    delay(0.1 * SECOND_IN_MILLISECOND); 

  }
}

void loop() {
  // put your main code here, to run repeatedly:
  //calibrateMotors();
  //frontServo.write(90);
  // x:10, y:15
  // backServo.write(79.79218127796581);
  // frontServo.write(87.79577249602796);
  // delay(10 * SECOND_IN_MILLISECOND);
  
  // // x:10, y:10
  // backServo.write(103.96251903294149);
  // frontServo.write(111.23410626265819);

  // delay(10 * SECOND_IN_MILLISECOND);

  print_path();
  // solve_length();

  //test_pen_lifter();
  //main_loop();


}
