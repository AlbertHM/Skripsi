#include<Wire.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_GFX.h>

#define OLED_ADDR 0x3c

Adafruit_SSD1306 display(-1);

#if (SSD1306_LCDHEIGHT != 64)
#error("Height incorrect, please fix Adafruit_SSD1306.h!");
#endif

int temp0, temp1, tulis=0, sign;
int sudut[5]={0,0,0,0,0};

void setup()
{
  Serial.begin(9600);
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
}

void loop()
{
  while(Serial.available()>=1)
  {
    if(Serial.read()==0xF5)
    {
     display.clearDisplay();
     display.setCursor(0,0);
     for(int i=0; i<5; i++)
     {
      sign = Serial.read();
      temp0 = Serial.read();
      temp1 = Serial.read();
      sudut[i] = temp0 + temp1;
      display.print("Q");
      display.print(i);
      display.print(" : ");
      if(sign == 1)
      {
        display.print("-");
      }
      /*display.print(sign);
      display.print(" ");
      display.print(temp0);
      display.print(" ");
      display.print(temp1);
      display.print(" ");*/
      display.println(sudut[i]);      
     }
     display.display();
    }    
  }
     delay(100);
}
