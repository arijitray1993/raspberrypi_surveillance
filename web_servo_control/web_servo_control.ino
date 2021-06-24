#include <Servo.h>

Servo myservo;
//Servo myservo1;

int pos = 0;

void setup() {
  // put your setup code here, to run once:
  // put your setup code here, to run once:
  Serial.begin(9600);
  myservo.attach(9);
  //myservo1.attach(10);

}

void turn_right(){
  for(int pos=100; pos<125; pos++){
    myservo.write(pos);
    delay(10);
  }
  for(int pos=125; pos>100; pos--){
    myservo.write(pos);
    delay(10);
  }
  myservo.write(95);
}

void turn_left(){
  for(int pos=90; pos>65; pos--){
    myservo.write(pos);
    delay(10);
  }
  for(int pos=65; pos<90; pos++){
    myservo.write(pos);
    delay(10);
  }
  myservo.write(95);
}


void loop() {
  // put your main code here, to run repeatedly:
  myservo.write(95);
  if(Serial.available()>0){
        
        String dir = Serial.readString();

        //Serial.print(dir);
        
        if(dir=="left"){
          turn_left();
        }
        else if(dir=="right"){
          turn_right();
        }
        
  }

}
