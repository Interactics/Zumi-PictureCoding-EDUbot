#include <Wire.h>

#define MOTOR_LEFT_A 5
#define MOTOR_LEFT_B 6
#define MOTOR_RIGHT_A 10
#define MOTOR_RIGHT_B 9

const int my_i2c_addr = 4; // 이 부분은 각 장치마다 다르게 변경하여 컴파일/업로드
const int led_pin =  13;

void velocity(int LeftVel, int RightVel);

void setup() {


  pinMode(led_pin, OUTPUT);
  pinMode(MOTOR_LEFT_A, OUTPUT);
  pinMode(MOTOR_LEFT_B, OUTPUT);
  pinMode(MOTOR_RIGHT_A, OUTPUT);
  pinMode(MOTOR_RIGHT_B, OUTPUT);
  Serial.begin(9600);
  
  Wire.begin(my_i2c_addr);
  Wire.onReceive(motorSPD);
  //Wire.onRequest(sendData); // 이 부분은 현재 사용하지 않음
}

void loop() {


  delay(100);
}
void motorSPD(int byte_count){
  if(Wire.available()){
    int spd_origin = Wire.read();
    Serial.println(spd_origin);
    
    int leftSPD;
    int rightSPD;
    
    if (spd_origin/10 >5){
      leftSPD = ((spd_origin/10)-4) * 10;
    }
    else if(spd_origin/10 <5){
      leftSPD = ((spd_origin/10)-6) *10;
    }
    else
      leftSPD = 0;
    
    if (spd_origin%10 > 5){
      rightSPD = ((spd_origin%10)-4) * 10;
    }
    else if(spd_origin%10 < 5){
      rightSPD = ((spd_origin%10)-6) * 10;
    }
    else 
      rightSPD = 0;

    velocity(leftSPD, rightSPD);
  }
}


//
//
//void recvData(int byte_count) {
//  while( Wire.available()) {
//    int on_off = Wire.read();
//    if (on_off == 1) {
//      digitalWrite(led_pin, HIGH);
//      velocity(100,100);
//
//
//    } else if(on_off == 2){
//      digitalWrite(led_pin, LOW);
//       velocity(100,-100);
//
//    }
//   else if(on_off == 3){
//      digitalWrite(led_pin, HIGH);
//       velocity(-100,100);
//
//    }
//     else if(on_off == 4){
//      digitalWrite(led_pin, LOW);
//       velocity(-100,-100);
//
//    }
//    else {
//      digitalWrite(led_pin, HIGH);
//       velocity(0,0);
//
//    }
//  }
//}





void sendData() {
  Wire.write(1);
}

void inv_trans_spd(int velocity){
  
  
}

void velocity(int LeftVel, int RightVel){

  if(LeftVel > 0){
    analogWrite(MOTOR_LEFT_A,LeftVel); //toggle led
    analogWrite(MOTOR_LEFT_B,0); //toggle led
  }
  else{
    LeftVel=-LeftVel;
    analogWrite(MOTOR_LEFT_A,0); //toggle led
    analogWrite(MOTOR_LEFT_B,LeftVel); //toggle led
  }

  if(RightVel > 0){
    analogWrite(MOTOR_RIGHT_A,RightVel); //toggle led
    analogWrite(MOTOR_RIGHT_B,0); //toggle led
  }
  else{
    RightVel=-RightVel;
    analogWrite(MOTOR_RIGHT_A,0); //toggle led
    analogWrite(MOTOR_RIGHT_B,RightVel); //toggle led
  }

}
