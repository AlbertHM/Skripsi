//Mekatronika V6.0

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
int x,temp;

int sudutT0(long int p)
{
  int u = 3600+((405*p)/180);
  return u;
}

void setup() {
  Serial.begin(250000);
  Serial.println("Joint 2 Test!");
  pwm.begin();
  pwm.setPWMFreq(50);

  Wire.setClock(1000);
  for (uint8_t pin=0; pin<16; pin++) 
  {
  pwm.setPWM(pin, sudutT0(90),4095);
  }
  pwm.setPWM(3, sudutT0(90), 4095);
}

void loop() {
    if(Serial.available() == 8){
      if(Serial.read() == 0xF5)
      {
        //Joint 1
      temp = Serial.read();
      x = sudutT0(temp);
      pwm.setPWM(0,x,4095);
      // Joint 2 Servo kiri dan kanan
      temp = Serial.read();
      x = sudutT0(temp);
      pwm.setPWM(1,x,4095);
      x = sudutT0(180-temp); //810 - theta
      pwm.setPWM(2,x,4095);
      //Joint 3 - 6, Gripper
      for(uint8_t u = 3; u<8; u++)
      {
        temp = Serial.read();
        x = sudutT0(temp);
        pwm.setPWM(u,x,4095);
      }
      //delay(100);
      }
    }
}
