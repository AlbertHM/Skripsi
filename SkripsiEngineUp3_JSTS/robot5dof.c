#include <math.h>
#include "serial.h"
#define PI		3.14159265358
#define DTR 	PI/180.0				   // Conversi degree to radian
#define RTD 	180.0/PI				   // Conversi degree to radian

// Panjang Asli
#define LR1 16
#define LR2 14
#define LR3 25.5
#define LR4 16
#define LR5 6
#define LR6 15
#define Rasio 0.01

#define L1	LR1*Rasio   // link1
#define L2	LR2*Rasio   // link2
#define L3	LR3*Rasio
#define L4	LR4*Rasio
#define L5	LR5*Rasio
#define L6	LR6*Rasio

float q[5];

float objx=0.3;
float objy=0.5;

void init_robot()
{
	q[0]=0.0 * DTR;
	q[1]=90 * DTR;
	q[2]=0.0 * DTR;
	q[3]=90 * DTR;
	q[4]=0.0 * DTR;
}

void Retrieve_serial(void) {
  /*int retval=1, i,j,k,l;

  unsigned char sdata[3]; 
  unsigned char baca;
  
  
	i=1;

  while (i>0) {
    fcntl(fd, F_SETFL, FNDELAY); 
    i=read(fd, &baca, 1);
    if ((i==1) && (baca == 0xF5)) {
    	//printf("masuk\n");
    	sdata[0]=baca;
    	while (i<3) {
    		  if (read(fd, &baca, 1)>0) {sdata[i]=baca; i++;}
    	}
   	  //printf("terbaca %x  %x  %x \n",sdata[0],sdata[1],sdata[2]);
   	  q1=(sdata[1])*180.0/255.0*DTR;
   	  q2=(sdata[1])*180.0/255.0*DTR;
   	  q3=(sdata[1])*180.0/255.0*DTR;
   	  q4=(sdata[1])*180.0/255.0*DTR;
   	  q5=(sdata[1])*180.0/255.0*DTR;
    }
  } */

}
