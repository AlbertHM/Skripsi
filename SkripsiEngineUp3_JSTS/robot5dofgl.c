/////////////////////////////////////////////////////////////
/* Template OpengGL sengaja dibuat untuk kuliah robotik 
*  di Departemen Teknik Elektro
*  Bagi yang ingin memodifikasi untuk keperluan yang lain,
*  dipersilahkan dengan menuliskan acknowledgement pada
*    Dr. Abdul Muis, MEng.
*    Autonomous Control Electronics (ACONICS) Research Group
*    http://www.ee.ui.ac.id/aconics
*/////////////////////////////////////////////////////////////

/*
 * Dimodif lagi oleh Albert H. Mendrofa untuk keperluan kelas robotika
 * Hehe 
 */

#include <stdio.h> 
#include <stdlib.h> 
#include <GL/glut.h> // Header File For The GLUT Library
#include <GL/gl.h> // Header File For The OpenGL32 Library
#include <GL/glu.h> // Header File For The GLu32 Library
#include <unistd.h> // Header file for sleeping.
#include <math.h> 
#include <fcntl.h>			/* File control definitions */
#include <errno.h>			/* Error number definitions */
#include <termios.h>		/* POSIX terminal control definitions */
#include <sys/time.h>
#include "robot5dof.c"

/* ascii code for the escape key */
#define ESCkey	27

/* The number/handle of our GLUT window */
int window, wcam;  

/* To draw a quadric model */
GLUquadricObj *obj;

/* ROBOT MODEL PARAMATER */
#define Xoffset	0.0	
#define Yoffset	0.0
#define Zoffset	0.3

#define Link1 L1
#define Link2 L2
#define Link3 L3
#define Link4 L4
#define Link5 L5
#define Link6 L6

/* Joint Angle */
float *theta[5]={&q[0],&q[1],&q[2],&q[3],&q[4]};

/* Camera Position */
int pov;
float px = 1.5;
float py = -0.3;
float pz = 1.5;

/* Control Parameter */
float q_awal[5];
float q_cmd[5]		= {0,0,0,0,0};
float q_final[5]	= {0,0,0,0,0};
float dq[5]			= {0,0,0,0,0};
float dq_old[5]		= {0,0,0,0,0};
float dq_ref[5]		= {0,0,0,0,0};
float ddq_ref[5]	= {0,0,0,0,0};
float ddq[5]		= {0,0,0,0,0};

float xyz_init[3] 	= {0,0,0};
float xyz[3] 		= {0,0,0};
float xyz_cmd[3] 	= {0,0,0};
float xyz_final[3]	= {0,0,0};
float dxyz[3] 		= {0,0,0};
float dxyz_old[3] 	= {0,0,0};
float ddxyz_ref[3] 	= {0,0,0};
float ddxyz[3] 		= {0,0,0};

/* Inverse Jacobian */
float J11,J12,J13,J14,J15;
float J21,J22,J23,J24,J25;
float J31,J32,J33,J34,J35;

float K11,K12,K13;
float K21,K22,K23;
float K31,K32,K33;

float X11,X12,X13;
float X21,X22,X23;
float X31,X32,X33;

float IJ11,IJ12,IJ13;
float IJ21,IJ22,IJ23;
float IJ31,IJ32,IJ33;
float IJ41,IJ42,IJ43;
float IJ51,IJ52,IJ53;

float det;
float KpJ = 0.0002, KvJ = 0.014;
float KpT = 0.9, KvT = 0.01; //Best so far.. Kp = 0.9; Kv = 0.01; hanya x yang aneh geraknya
float N = 1000.0, Period = 0.0001,  k = 0;
int JS = -1, retbase = 0, TS = -1;

char debug=0;

/* Communication */
int temp0, temp1;
unsigned char header = 0xF5;
unsigned char kirimsudut_a[5];
unsigned char kirimsudut_b[5];
unsigned char kirimsudut_0[5];

void Sim_main(void); // Deklarasi lebih awal agar bisa diakses oleh fungsi sebelumnya
void display(void); // fungsi untuk menampilkan gambar robot / tampilan camera awal

/* define color */  
GLfloat green1[4] ={0.8, 1.0, 0.8, 1.0};
GLfloat blue1[4]  ={0.1, 0.1, 1.0, 1.0};
GLfloat blue2[4]  ={0.2, 0.2, 1.0, 1.0};
GLfloat blue3[4]  ={0.3, 0.3, 1.0, 1.0};
GLfloat yellow1[4]={0.1, 0.1, 0.0, 1.0};
GLfloat yellow2[4]={0.2, 0.2, 0.0, 1.0};
GLfloat pink6[4]  ={0.8, 0.55, 0.6, 1.0};
GLfloat yellow5[4]={0.8, 0.8, 0.0, 1.0};
GLfloat abu2[4]   ={0.5,0.5,0.5,1.0};
GLfloat gray1[4]  ={0.1, 0.1, 0.1, 1.0};
GLfloat gray2[4]  ={0.2, 0.2, 0.2, 1.0};
GLfloat gray3[4]  ={0.3, 0.3, 0.3, 1.0};
GLfloat gray4[4]  ={0.4, 0.4, 0.4, 1.0};
GLfloat gray5[4]  ={0.5, 0.5, 0.5, 1.0};
GLfloat gray6[4]  ={0.6, 0.6, 0.6, 1.0};
GLfloat gray7[4]  ={0.7, 0.7, 0.7, 1.0};
GLfloat gray8[4]  ={0.8, 0.8, 0.7, 1.0};
GLfloat gray9[4]  ={0.9, 0.9, 0.7, 1.0};

/* Create Line Model Function */
void drawOneLine(double x1, double y1, double x2, double y2) 
{
  glBegin(GL_LINES); 
	glVertex3f((x1),(y1),0.0); 
	glVertex3f((x2),(y2),0.0); 
  glEnd();
}
   
/* Create Cylinder Model Function */
void model_cylinder(GLUquadricObj * object, GLdouble lowerRadius, GLdouble upperRadius, GLdouble length, GLint res, GLfloat *color1, GLfloat *color2)
{
  glPushMatrix();
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color1);
    glTranslatef(0,0,-length/2);
	  gluCylinder(object, lowerRadius, upperRadius, length, 20, res);
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color2);
    gluDisk(object, 0.01, lowerRadius, 20, res); 
    glTranslatef(0, 0, length);
    gluDisk(object, 0.01, upperRadius, 20, res); 
  glPopMatrix();
}

/* Create box model function */
void model_box(GLfloat width, GLfloat depth, GLfloat height, GLfloat *color1, GLfloat *color2, GLfloat *color3, int color)
{
   width=width/2.0;depth=depth/2.0;height=height/2.0;
   glBegin(GL_QUADS);
// top
    if (color==1) 
		glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color1);
    glVertex3f(-width,-depth, height);
    glVertex3f( width,-depth, height);
    glVertex3f( width, depth, height);
    glVertex3f(-width, depth, height);
   glEnd();
   glBegin(GL_QUADS);
// bottom
    if (color==1) 
		glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color1);
    glVertex3f(-width,-depth,-height);
    glVertex3f( width,-depth,-height);
    glVertex3f( width, depth,-height);
    glVertex3f(-width, depth,-height);
   glEnd();
   glBegin(GL_QUAD_STRIP);
// sides
    if (color==1) 
	    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color2);
    glVertex3f(-width,-depth,height);
    glVertex3f(-width,-depth,-height);
    glVertex3f(width,-depth,height);
    glVertex3f(width,-depth,-height);
    glVertex3f(width,depth,height);
    glVertex3f(width,depth,-height);
    glVertex3f(-width,depth,height);
    glVertex3f(-width,depth,-height);
    glVertex3f(-width,-depth,height);
   glEnd();
}

/* Create floor function */
void disp_floor(void)
{
  int i,j,flagc=1;

  glPushMatrix();
  
  GLfloat dx=4.5,dy=4.5;
  GLint amount=15;
  GLfloat x_min=-dx/2.0, x_max=dx/2.0, x_sp=(GLfloat) dx/amount, y_min=-dy/2.0, y_max=dy/2.0, y_sp=(GLfloat) dy/amount;

  glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, green1);
  for(i = 0; i<=48; i++)
  {
     drawOneLine(-2.4+0.1*i, -2.4,       -2.4+0.1*i,  2.4);
     drawOneLine(-2.4,       -2.4+0.1*i,  2.4,       -2.4+0.1*i);
  }

  glPopMatrix();
}

/* Penunjuk Titik */
void penunjuk()
{
  glPushMatrix();
    double x=0;
    double y=0;
    double radius=0.1;
    double y1=0;
	double x1=0;
	glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, green1);
	glBegin(GL_LINES);
	for(double angle=0.0f;angle<=(2.0f*3.14159);angle+=0.01f)
	{
		double x2=x-(radius*(float)sin((double)angle));
		double y2=y-(radius*(float)cos((double)angle));
		glVertex3f(x1,y1,0);
		y1=y2;
		x1=x2;
	}
    glEnd();
  glPopMatrix();
}

void lighting(void)
{
	GLfloat light_ambient[] =  {0.2, 0.2, 0.2, 1.0};
	GLfloat light_diffuse[] =  {0.4, 0.4, 0.4, 1.0};
	GLfloat light_specular[] = {0.3, 0.3, 0.3, 1.0};
	GLfloat light_position[] = {2, 0.1, 7,1.0};
	GLfloat spot_direction[] = {0.0, -0.1, -1.0, 1.0};

	glClearColor(0.0, 0.0, 0.0, 0.0);     
  
	glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient);
	glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse);
	glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular);
	glLightfv(GL_LIGHT0, GL_POSITION, light_position);
	glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 40.0);
	glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, spot_direction);
	glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 4);

	glEnable(GL_LIGHTING);
	glEnable(GL_LIGHT0);
	glEnable(GL_DEPTH_TEST);
}

void disp_robot(void)
{
	/* //===> Template
	 * glPushMatrix(); // Set current matrix on the stack
	 * glTranslatef(someX, someY, someZ); // transformation 1
	 * glRotatef(someangle,someaxis);// transformation 2
	 * DrawObject(ONE);
	 * glPopMatrix();
	 */
	 // Pembuatan silinder selalu mulai dari tengah
	 
	glPushMatrix(); /*Begin robot building */
  
	/* Draw base */
		glTranslatef(0, 0, Link1/2); //Menuju titik pusat objek yg ingin digambar
		model_box(0.3, 0.5, Link1, gray8, gray7, gray6,1); //width,depth,height,*color1,*color2,*color3, int color
    // Menuju joint-1
    //glTranslatef(0, 0, 0.13); //(hasil ketebalan box/2 + 0.5 * panjang silinder)
		glTranslatef(0, 0, -(Link1/2)); //Mundur dulu ke World 0,0,0
		glTranslatef(0, 0, Link1/2);
    //glRotatef(*theta1*RTD,0,0,1); //Untuk memutar link selanjutnya
    /* Gambar Link-1 */
		glPushMatrix();
		model_cylinder(obj, 0.02, 0.02, Link1, 2, blue1, yellow2);//GLUquadricObj * object,lowerRadius,upperRadius,length,res,*color1,*color2
		glPopMatrix();
    /* Menuju Joint-2 */
		glTranslatef(0, 0, Link1/2); //move x,y,z
		glRotatef(*theta[0]*RTD, 0,0,1); //sudut,x,y,z
    /* Gambar Link-2 */
		glTranslatef(0, 0, Link2/2);
		glPushMatrix();
		model_cylinder(obj, 0.02, 0.02, Link2, 2, pink6, yellow2);
		glPopMatrix();
    /* Menuju Joint-3 */
		glTranslatef(0, 0, Link2/2);
		glRotatef(*theta[1]*RTD-90, 1,0,0);
    /* Gambar Link-3 */
		glTranslatef(0, 0, Link3/2);
		glPushMatrix();
		model_cylinder(obj, 0.02, 0.02, Link3, 2, pink6, yellow2);
		glPopMatrix();
    /* Menuju Joint-4 */
		glTranslatef(0,0, Link3/2);
		glRotatef(*theta[2]*RTD, 1,0,0);
    /* Gambar Link-4 */
		glTranslatef(0, 0, Link4/2);
		glPushMatrix();
		model_cylinder(obj, 0.02, 0.02, Link4, 2, yellow5, yellow2);
		glPopMatrix();
    /* Menuju Joint-5 */
		glTranslatef(0,0, Link4/2);
		glRotatef(*theta[3]*RTD-90, 1,0,0);
    /* Gambar Link-5 */
		glTranslatef(0, 0, Link5/2);
		glPushMatrix();
		model_cylinder(obj, 0.02, 0.02, Link5, 2, yellow5, yellow2);
		glPopMatrix();
    /* Menuju Joint-6 */
		glTranslatef(0,0, Link5/2);
		glRotatef(*theta[4]*RTD, 0,0,1);
    /* Gambar Link-6 */
		glTranslatef(0, 0, Link6/2);
		penunjuk();
		glPushMatrix();
		model_cylinder(obj, 0.02, 0.02, Link6, 2, yellow5, yellow2);
		glPopMatrix();
    
	glPopMatrix(); /*End robot building */
  
  /* Pop when all robot body finished 
   * Matrix reset when popped up
   * */
}

// Draw Object
void display(void)
{
   glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT) ; // Clear The Screen and The Depth Buffer 
   
   glLoadIdentity();  // Reset View
   if(pov==1)
   {
	   gluLookAt(px,pz,pz,  0, 0.0, 0.4,  0.0, 0.0, 1.0); //(position of eye point, position of ref point, direction of up vector
   }
   else if(pov==2)
   {	   
	   gluLookAt(2, 0, 3,  0, 0.0, 0.4,  0.0, 0.0, 1.0);
   }
   
   /* Create floor */
   disp_floor();
   /* Create robot */
   disp_robot();

   /* since window is double buffered, 
      Swap the front and back buffers (used in double buffering). */
   glutSwapBuffers() ; 
   
}

void control_joint(int i)
{
	q_cmd[i] = q_awal[i] + ((q_final[i]-q_awal[i]) * (k/(N*Period)));
	dq_old[i] = dq[i];
	dq_ref[i] = (q_cmd[i] - q[i]) / Period;
	ddq_ref[i] = (dq_ref[i] - dq_old[i])/Period;
	ddq[i] = KpJ * dq[i] + KvJ * ddq_ref[i];
	dq[i] = dq[i] + ddq[i] * Period;
	q[i] = q[i] + dq[i] * Period;
	//printf("%.2f\t%.2f\t%.2f\n",q_final[0], q_cmd[0],q[0]);
	//printf("%.2f\n",q_awal[0]);
}

void forward_kinematic()
{
	xyz[0] = 0.08*cos(q[0] + q[1] + q[2]) + 0.105*sin(q[1] - 1.0*q[0] + q[2] + q[3]) + 0.127*cos(q[0] - 1.0*q[1]) + 0.105*sin(q[0] + q[1] + q[2] + q[3]) + 0.127*cos(q[0] + q[1]) + 0.08*cos(q[1] - 1.0*q[0] + q[2]) + 1.29e-17*sin(q[0]);
	xyz[1] = 0.08*sin(q[0] + q[1] + q[2]) + 0.105*cos(q[1] - 1.0*q[0] + q[2] + q[3]) + 0.127*sin(q[0] - 1.0*q[1]) - 0.105*cos(q[0] + q[1] + q[2] + q[3]) + 0.127*sin(q[0] + q[1]) - 0.08*sin(q[1] - 1.0*q[0] + q[2]) - 1.29e-17*cos(q[0]);
	xyz[2] = 0.16*sin(q[1] + q[2]) - 0.21*cos(q[1] + q[2] + q[3]) + 0.255*sin(q[1]) + 0.3;
}

void trajectory_init()
{
	forward_kinematic();
	for(int p = 0; p<3; p++)
	{
		xyz_init[p] = xyz[p];
	}
}

void trajectory_planning()
{
	for(int p = 0; p<3; p++)
	{
		xyz_cmd[p] = xyz_init[p] + (xyz_final[p]-xyz_init[p]) * (k/(N*Period));
	}
}

void double_differential()
{
	for(int p = 0; p<3; p++)
	{
		dxyz_old[p] = dxyz[p];
		dxyz[p] = (xyz_cmd[p] - xyz[p])/Period;
		ddxyz_ref[p] = (dxyz[p] - dxyz_old[p])/Period;
	}
}

void control_task()
{
	for(int p = 0; p<3; p++)
	{
		ddxyz[p] = KpT * dxyz[p] + KvT * ddxyz_ref[p];
	}
}

void inverse_jacobian()
{
	J11 = 0.105*cos(q[0] + q[1] + q[2] + q[3]) - 0.105*cos(q[1] - q[0] + q[2] + q[3]) - 0.1275*sin(q[0] - q[1]) - 0.08*sin(q[0] + q[1] + q[2]) - 0.1275*sin(q[0] + q[1]) + 0.08*sin(q[1] - q[0] + q[2]);
	J12 = 0.105*cos(q[1] - q[0] + q[2] + q[3]) - 0.08*sin(q[0] + q[1] + q[2]) + 0.1275*sin(q[0] - q[1]) + 0.105*cos(q[0] + q[1] + q[2] + q[3]) - 0.1275*sin(q[0] + q[1]) - 0.08*sin(q[1] - q[0] + q[2]);
	J13 = 0.105*cos(q[1] - q[0] + q[2] + q[3]) - 0.08*sin(q[0] + q[1] + q[2]) + 0.105*cos(q[0] + q[1] + q[2] + q[3]) - 0.08*sin(q[1] - q[0] + q[2]);
	J14 = 0.105*cos(q[1] - q[0] + q[2] + q[3]) + 0.105*cos(q[0] + q[1] + q[2] + q[3]);
	J15 = 0;
	J21 = 0.08*cos(q[0] + q[1] + q[2]) + 0.105*sin(q[1] - q[0] + q[2] + q[3]) + 0.1275*cos(q[0] - q[1]) + 0.105*sin(q[0] + q[1] + q[2] + q[3]) + 0.1275*cos(q[0] + q[1]) + 0.08*cos(q[1] - q[0] + q[2]);
	J22 = 0.08*cos(q[0] + q[1] + q[2]) - 0.105*sin(q[1] - q[0] + q[2] + q[3]) - 0.1275*cos(q[0] - q[1]) + 0.105*sin(q[0] + q[1] + q[2] + q[3]) + 0.1275*cos(q[0] + q[1]) - 0.08*cos(q[1] - q[0] + q[2]);
	J23 = 0.08*cos(q[0] + q[1] + q[2]) - 0.105*sin(q[1] - q[0] + q[2] + q[3]) + 0.105*sin(q[0] + q[1] + q[2] + q[3]) - 0.08*cos(q[1] - q[0] + q[2]);
	J24 = 0.105*sin(q[0] + q[1] + q[2] + q[3]) - 0.105*sin(q[1] - q[0] + q[2] + q[3]);
	J25 = 0;
	J31 = 0;
	J32 = 0.21*sin(q[1] + q[2] + q[3]) + 0.16*cos(q[1] + q[2]) + 0.255*cos(q[1]);
	J33 = 0.21*sin(q[1] + q[2] + q[3]) + 0.16*cos(q[1] + q[2]);
	J34 = 0.21*sin(q[1] + q[2] + q[3]);
	J35 = 0;
	
	K11 = J11*J11 + J12*J12 + J13*J13 + J14*J14 + J15*J15;
	K12 = J11*J21 + J12*J22 + J13*J23 + J14*J24 + J15*J25;
	K13 = J11*J31 + J12*J32 + J13*J33 + J14*J34 + J15*J35;
	K21 = J11*J21 + J12*J22 + J13*J23 + J14*J24 + J15*J25;
	K22 = J21*J21 + J22*J22 + J23*J23 + J24*J24 + J25*J25;
	K23 = J21*J31 + J22*J32 + J23*J33 + J24*J34 + J25*J35;
	K31 = J11*J31 + J12*J32 + J13*J33 + J14*J34 + J15*J35;
	K32 = J21*J31 + J22*J32 + J23*J33 + J24*J34 + J25*J35;
	K33 = J31*J31 + J32*J32 + J33*J33 + J34*J34 + J35*J35;
	det = K11*K22*K33-K11*K23*K32-K12*K21*K33+K12*K23*K31+K13*K21*K32-K13*K22*K31;

	X11 = (K22*K33 - K32*K23)/det;
	X12 = (K13*K32 - K12*K33)/det;
	X13 = (K12*K23 - K13*K22)/det;
	X21 = (K23*K31 - K21*K33)/det;
	X22 = (K11*K33 - K13*K31)/det;
	X23 = (K13*K21 - K11*K23)/det;
	X31 = (K21*K32 - K22*K31)/det;
	X32 = (K12*K31 - K11*K32)/det;
	X33 = (K11*K22 - K12*K21)/det;
	
	IJ11 = J11*X11 + J21*X21 + J31*X31;
	IJ12 = J11*X12 + J21*X22 + J31*X32;
	IJ13 = J11*X13 + J21*X23 + J31*X33;
	IJ21 = J12*X11 + J22*X21 + J32*X31;
	IJ22 = J12*X12 + J22*X22 + J32*X32;
	IJ23 = J12*X13 + J22*X23 + J32*X33;
	IJ31 = J13*X11 + J23*X21 + J33*X31;
	IJ32 = J13*X12 + J23*X22 + J33*X32;
	IJ33 = J13*X13 + J23*X23 + J33*X33;
	IJ41 = J14*X11 + J24*X21 + J34*X31;
	IJ42 = J14*X12 + J24*X22 + J34*X32;
	IJ43 = J14*X13 + J24*X23 + J34*X33;
	IJ51 = J15*X11 + J25*X21 + J35*X31;
	IJ52 = J15*X12 + J25*X22 + J35*X32;
	IJ53 = J15*X13 + J25*X23 + J35*X33;
	
	ddq[0] = IJ11*ddxyz[0] + IJ12*ddxyz[1] + IJ13*ddxyz[2];
	ddq[1] = IJ21*ddxyz[0] + IJ22*ddxyz[1] + IJ23*ddxyz[2];
	ddq[2] = IJ31*ddxyz[0] + IJ32*ddxyz[1] + IJ33*ddxyz[2];
	ddq[3] = IJ41*ddxyz[0] + IJ42*ddxyz[1] + IJ43*ddxyz[2];
	ddq[4] = IJ51*ddxyz[0] + IJ52*ddxyz[1] + IJ53*ddxyz[2];
}

void double_integrator()
{
	for(int p = 0; p<5; p++)
	{
		dq[p] = dq[p] + ddq[p] * Period;
		q[p] = q[p] + dq[p] * Period;
	}
}

void kirimdata()
{
	for(int p=0; p<5; p++)
	{
		if(q[p]<0)
		{
			kirimsudut_0[p]=1;
		}
		else
		{
			kirimsudut_0[p]=0;
		}
		temp0 = abs(q[p]*RTD);
		temp1 = fmod(temp0, 360);
		if(temp1 > 255)
		{
			kirimsudut_a[p] = 255;
			kirimsudut_b[p] = temp1 - 255;
		}
		else
		{
			kirimsudut_a[p] = temp1;
			kirimsudut_b[p] = 0;
		}
	}
	write(fd,&header,sizeof(header));//header
	for(int p=0; p<5; p++)
	{
		write(fd,&kirimsudut_0[p],sizeof(kirimsudut_0[p]));
		write(fd,&kirimsudut_a[p],sizeof(kirimsudut_a[p]));
		write(fd,&kirimsudut_b[p],sizeof(kirimsudut_b[p]));
	}
	usleep(5000);
}

void tampilkan()
{
	pov = 1;
	glutSetWindow(window);
	display();
	pov = 2;
	glutSetWindow(wcam);
	display();	
}

void Sim_main(void)
{
	if(retbase == 1)
	{
		k = 0.0;
		q_final[0] = 0;
		q_final[1] = 0 * DTR;
		q_final[2] = 0;
		q_final[3] = 0 * DTR;
		q_final[4] = 0;
		for(int j = 0; j<5; j++)
		{
			q_awal[j] = q[j];
		}
		while(k <= N*Period)
		{
			for(int p = 0; p<5; p++)
			{
				control_joint(p);
			}
			k+=Period;
			forward_kinematic();
			tampilkan();
			
			printf("%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t\n",q[0]*RTD,q[1]*RTD,q[2]*RTD,q[3]*RTD,q[4]*RTD);
			printf("%.3f\t%.3f\t%.3f\n", xyz[0], xyz[1], xyz[2]);
		}
		retbase = 0;
		kirimdata();
	}
	
	if(JS != -1)
	{
		k = 0.0;
		for(int j = 0; j<5; j++)
		{
			q_awal[j] = q[j];
		}
		while(k <= N*Period)
		{
			//printf("[%.f]",k/Period);
			control_joint(JS);
			forward_kinematic();
			k+=Period;
			tampilkan();
			
			printf("%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t\n",q[0]*RTD,q[1]*RTD,q[2]*RTD,q[3]*RTD,q[4]*RTD);
			printf("%.3f\t%.3f\t%.3f\n", xyz[0], xyz[1], xyz[2]);
		}
		JS = -1;
		kirimdata();
	}
	
	if(TS != -1)
	{
		k = 0.0;
		trajectory_init();
		while(k <= N*Period)
		{
			trajectory_planning();
			double_differential();
			control_task();
			inverse_jacobian();
			double_integrator();
			forward_kinematic();
			k+=Period;
			tampilkan();
			
			//printf("%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t\n",q[0]*RTD,q[1]*RTD,q[2]*RTD,q[3]*RTD,q[4]*RTD);
			printf("%.3f\t%.3f\t%.3f\n", xyz[0], xyz[1], xyz[2]);
		}
		TS = -1;
		kirimdata();
	}
}

void keyboard(unsigned char key, int i, int j)
{
	forward_kinematic();	
	for(int p = 0; p<5; p++)
	{
		q_final[p] = q[p];
	}
	for(int p = 0; p<3; p++)
	{
		xyz_final[p] = xyz[p];
	}
switch(key)
	{
		/* Program Control */
		case ESCkey: exit(1); break;
		/* Task Control*/
		case '2' : xyz_final[0] += 0.2; TS = 1; break;
		case '3' : xyz_final[0] += -0.2; TS = 1; break;
		case '4' : xyz_final[1] += 0.2; TS = 1; break;
		case '5' : xyz_final[1] += -0.2; TS = 1; break;
		case '6' : xyz_final[2] += 0.2; TS = 1; break;
		case '7' : xyz_final[2] += -0.2; TS = 1; break;
		
		/* Joint Control */
		case 'z': //for return to base
			retbase = 1;
			break;
		case 'a': q_final[0] += 10*DTR; JS = 0; break;
		case 'A': q_final[0] += -10*DTR; JS = 0;break;
		case 's': q_final[1] += 10*DTR; JS = 1;break;
		case 'S': q_final[1] += -10*DTR; JS = 1;break;
		case 'd': q_final[2] += 10*DTR; JS = 2;break;
		case 'D': q_final[2] += -10*DTR; JS = 2;break;
		case 'f': q_final[3] += 10*DTR; JS = 3;break;
		case 'F': q_final[3] += -10*DTR; JS = 3;break;
		case 'g': q_final[4] += 10*DTR; JS = 4;break;
		case 'G': q_final[4] += -10*DTR; JS = 4;break;
		  
		/* Camera control */
		case 'j': px += 0.1; break;
		case 'J': px += -0.1; break;
		case 'k': py += 0.1; break;
		case 'K': py += -0.1; break;
		case 'l': pz += 0.1; break;
		case 'L': pz += -0.1; break;
    }
}

void init(void) 
{ 
	obj = gluNewQuadric(); 
	/* Clear background to (Red, Green, Blue, Alpha) */
	glClearColor(0.0f, 0.0f, 0.0f, 0.0f) ;
	glEnable(GL_DEPTH_TEST); // Enables Depth Testing
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	gluPerspective(40.0, 1, 0.2, 8);
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
	lighting();

	/* When the shading model is GL_FLAT only one colour per polygon is used, 
	  whereas when the shading model is set to GL_SMOOTH the colour of 
	  a polygon is interpolated among the colours of its vertices.  */
	glShadeModel(GL_SMOOTH) ; 

	glutDisplayFunc (&display) ;
	glutKeyboardFunc(&keyboard);

}

/* Main Program */
int main(int argc, char** argv)
{
 /* Initialize GLUT */
	/* Initialize GLUT state - glut will take any command line arguments 
	  see summary on OpenGL Summary */  
	glutInit (&argc, argv);

	/* Berikut jika ingin menggunakan serial port */
	//fd = open_port();
	//init_port(fd);

	/* Select type of Display mode:   
	  Double buffer 
	  RGBA color
	  Alpha components supported 
	  Depth buffer */  
	  
	//glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB );

	/* Set a 400 (width) x 400 (height) window and its position */
	glutInitWindowSize(400,400);	// Ukuran window
	glutInitWindowPosition (40, 100); // Posisi window

	/* Open a window */  
	pov = 1;
	window = glutCreateWindow ("5 DOF Robot"); // Bikin window dan judul


	/* Initialize our window. */
	init_robot();
	init() ;
	
	pov = 2;
	wcam = glutCreateWindow ("Kamera");
	init() ;
	
	/* Register the function to do all our OpenGL drawing. */
	glutIdleFunc(&Sim_main); // fungsi untuk simulasi utama

	/* Start Event Processing Engine */ 
	glutMainLoop () ;
	return 0 ;
}           
