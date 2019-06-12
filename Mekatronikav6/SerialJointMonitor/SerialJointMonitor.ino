//Mekatronika V6.0

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_GFX.h>

#define OLED_ADDR 0x3c

Adafruit_SSD1306 display(-1);

#if (SSD1306_LCDHEIGHT != 64)
#error("Height incorrect, please fix Adafruit_SSD1306.h!");
#endif

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
int x,temp;
int go = 0;

int sudutT0(long int p)
{
  int u = 3600+((405*p)/180);
  return u;
}

void setup() {
  Serial.begin(250000);
  Serial.flush();
  Serial.println("Joint 2 Test!");
  pinMode(LED_BUILTIN, OUTPUT);
  display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);
  display.clearDisplay();
  display.display();

  // display a pixel in each corner of the screen
  display.drawPixel(0, 0, WHITE);
  display.drawPixel(127, 0, WHITE);
  display.drawPixel(0, 63, WHITE);
  display.drawPixel(127, 63, WHITE);

  // display a line of text
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(20,30);
  display.println("Bekerja");
  display.print("New line");

  // update display with all of the above graphics
  display.display();
  
  pwm.begin();
  pwm.setPWMFreq(50);
/*
  Wire.setClock(1000);
  for (uint8_t pin=0; pin<16; pin++) 
  {
  pwm.setPWM(pin, sudutT0(90),4095);
  }
  pwm.setPWM(3, sudutT0(180), 4095);*/
}

void loop() {
    /*
    if(Serial.available())
    {
      display.clearDisplay();
      display.setCursor(0,0);
      display.println("Diterima");
      display.display();
      delay(100);      
    }*/
    if(Serial.available() == 8){
      display.clearDisplay();
      display.setCursor(0,0);
      display.display();
      if(Serial.read() == 0xF5)
      {
      for(uint8_t u = 0; u<7; u++)
      {
        temp = Serial.read();
        display.println(temp);
        //x = sudutT0(temp);
        //pwm.setPWM(u,x,4095);
      }
      display.display();
      delay(100);
      //delay(4000);
      }
    }
    else
    {
      display.clearDisplay();
      display.setCursor(0,0);
      display.print("Empty");
      display.display();      
    }
}
