from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import degrees, radians
import math
import cv2
import sys
import numpy

ESCAPE = 27

#Panjang Link
LR = [16, 14, 25.5, 16, 6, 15]
rasio = 0.01
L = [0, 0, 0, 0, 0, 0]
for i in range(0,len(LR)):
	L[i] = LR[i]*rasio

#Sudut Link
q = [0, 0, 0, 0, 0]

#Posisi Kamera
p = [1.5, -0.3, 1.5]

#Warna
green1	= [0.8, 1.0, 0.8, 1.0]
blue1	= [0.1, 0.1, 1.0, 1.0]
blue2	= [0.2, 0.2, 1.0, 1.0]
blue3	= [0.3, 0.3, 1.0, 1.0]
yellow1	= [0.1, 0.1, 0.0, 1.0]
yellow2 = [0.2, 0.2, 0.0, 1.0]
yellow5 = [0.8, 0.8, 0.0, 1.0]
pink6	= [0.8, 0.55, 0.6, 1.0]
gray1	= [0.1, 0.1, 0.1, 1.0]
gray2	= [0.2, 0.2, 0.2, 1.0]
gray3	= [0.3, 0.3, 0.3, 1.0]
gray4	= [0.4, 0.4, 0.4, 1.0]
gray5	= [0.5, 0.5, 0.5, 1.0]
gray6	= [0.6, 0.6, 0.6, 1.0]
gray7	= [0.7, 0.7, 0.7, 1.0]
gray8	= [0.8, 0.8, 0.7, 1.0]
gray9	= [0.9, 0.9, 0.7, 1.0]

def drawOneLine(x1, y1, x2, y2):
	glBegin(GL_LINES)
	glVertex3f(x1, y1, 0.0)
	glVertex3f(x2, y2, 0.0)
	glEnd()
	
def model_cylinder(obj, lowerRadius, upperRadius, length, res, color1, color2):
	glPushMatrix()
	glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color1)
	glTranslatef(0, 0, -length/2)
	gluCylinder(obj, lowerRadius, upperRadius, length, 20, res)
	glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color2)
	gluDisk(obj, 0.01, lowerRadius, 20, res)
	glTranslatef(0, 0, length)
	gluDisk(obj, 0.01, upperRadius, 20, res)
	glPopMatrix()
	
def model_box(width, depth, height, color1, color2, color3, color):
	width	= width/2.0
	depth	= depth/2.0
	height	= height/2.0
	
	glBegin(GL_QUADS);
	# Top
	if (color==1) :
		glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color1)
		glVertex3f(-width,-depth, height)
		glVertex3f( width,-depth, height)
		glVertex3f( width, depth, height)
		glVertex3f(-width, depth, height)
		glEnd()
		glBegin(GL_QUADS)
	# bottom
		glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color1)
		glVertex3f(-width,-depth,-height)
		glVertex3f( width,-depth,-height)
		glVertex3f( width, depth,-height)
		glVertex3f(-width, depth,-height)
		glEnd()
		glBegin(GL_QUAD_STRIP)
	# sides
		glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color2)
		glVertex3f(-width,-depth,height)
		glVertex3f(-width,-depth,-height)
		glVertex3f(width,-depth,height)
		glVertex3f(width,-depth,-height)
		glVertex3f(width,depth,height)
		glVertex3f(width,depth,-height)
		glVertex3f(-width,depth,height)
		glVertex3f(-width,depth,-height)
		glVertex3f(-width,-depth,height)
		glEnd()

def pencahayaan():
	light_ambient = [0.2, 0.2, 0.2, 1.0]
	light_diffuse = [0.4, 0.4, 0.4, 1.0]
	light_specular = [0.3, 0.3, 0.3, 1.0]
	light_position = [2.0, 0.1, 7.0, 1.0]
	spot_direction = [0.0, -0.1, -0.1, 1.0]
	
	glClearColor(0.0, 0.0, 0.0, 0.0)
	
	glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
	glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
	glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
	glLightfv(GL_LIGHT0, GL_POSITION, light_position)
	glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 40.0)
	glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, spot_direction)
	glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 4)
	
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glEnable(GL_DEPTH_TEST)

def init_robot():
	global q
	
	tempq = [0.0, 90, 0.0, 90, 0.0]
	for i in range(0, len(tempq)):
		q[i] = radians(tempq[i])
	
def disp_robot():
	global objek, q
	
	'''
	# Template
	/*
	* glPushMatrix(); // Set current matrix on the stack
	* glTranslatef(someX, someY, someZ); // transformation 1
	* glRotatef(someangle,someaxis);// transformation 2
	* DrawObject(ONE);
	* glPopMatrix();
	*/
	# Pembuatan silinder selalu mulai dari tengah
	'''

	glPushMatrix() # Begin robot building

	# Draw base
	glTranslatef(0, 0, L[0]/2); #Menuju titik pusat objek yg ingin digambar
	model_box(0.3, 0.5, L[0], gray8, gray7, gray6,1)
	
	# Menuju joint-1
	#glTranslatef(0, 0, 0.13); //(hasil ketebalan box/2 + 0.5 * panjang silinder)
	glTranslatef(0, 0, -(L[0]/2)) # Mundur dulu ke World 0,0,0
	glTranslatef(0, 0, L[0]/2)
	#glRotatef(*theta1*RTD,0,0,1); # Untuk memutar link selanjutnya
	# Gambar Link-1
	glPushMatrix()
	model_cylinder(objek, 0.02, 0.02, L[0], 2, blue1, yellow2)
	glPopMatrix()
	
	# Menuju Joint-2
	glTranslatef(0, 0, L[0]/2) #move x,y,z
	glRotatef(degrees(q[0]), 0,0,1) #sudut,x,y,z
	# Gambar Link-2
	glTranslatef(0, 0, L[1]/2)
	glPushMatrix()
	model_cylinder(objek, 0.02, 0.02, L[1], 2, pink6, yellow2)
	glPopMatrix()
	
	# Menuju Joint-3
	glTranslatef(0, 0, L[1]/2)
	glRotatef(degrees(q[1])-90, 1,0,0)
	# Gambar Link-3
	glTranslatef(0, 0, L[2]/2)
	glPushMatrix()
	model_cylinder(objek, 0.02, 0.02, L[2], 2, pink6, yellow2)
	glPopMatrix()
	
	# Menuju Joint-4 */
	glTranslatef(0,0, L[2]/2)
	glRotatef(degrees(q[2]), 1,0,0)
	# Gambar Link-4
	glTranslatef(0, 0, L[3]/2)
	glPushMatrix()
	model_cylinder(objek, 0.02, 0.02, L[3], 2, yellow5, yellow2)
	glPopMatrix()
	
	# Menuju Joint-5
	glTranslatef(0,0, L[3]/2)
	glRotatef(degrees(q[3])-90, 1,0,0)
	# Gambar Link-5
	glTranslatef(0, 0, L[4]/2)
	glPushMatrix()
	model_cylinder(objek, 0.02, 0.02, L[4], 2, yellow5, yellow2)
	glPopMatrix()
	
	# Menuju Joint-6
	glTranslatef(0,0, L[4]/2)
	glRotatef(degrees(q[4]), 0,0,1)
	# Gambar Link-6
	glTranslatef(0, 0, L[5]/2)
	#penunjuk();
	glPushMatrix()
	model_cylinder(objek, 0.02, 0.02, L[5], 2, yellow5, yellow2)
	glPopMatrix()

	glPopMatrix() # End robot building

	'''
	Pop when all robot body finished 
	Matrix reset when popped up
	'''

def disp_floor():
	glPushMatrix()
	
	glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, green1)
	for i in range(0,49):
		drawOneLine(-2.4+0.1*i, -2.4, -2.4+0.1*i, 2.4)
		drawOneLine(-2.4, -2.4+0.1*i, 2.4, -2.4+0.1*i)
		
	glPopMatrix()

def tampilkan():
	glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)
	glLoadIdentity()
	gluLookAt(p[0], p[1], p[2], 0, 0.0, 0.4, 0.0, 0.0, 1.0)
	
	disp_floor()
	disp_robot()
	
	glutSwapBuffers()

def Sim_main():
	pass

def keyPressed(key, x, y):
	global window
	
	# JIka ditekan tombol escape
	if key == ESCAPE:
		sys.exit()
	elif key == '1':
		pass
	
def init():
	global objek
	objek = gluNewQuadric()
	glClearColor(0.0, 0.0, 0.0, 0.0)
	glEnable(GL_DEPTH_TEST)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(40.0, 1, 0.2, 8)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	pencahayaan()
	
	glShadeModel(GL_SMOOTH)
	
	glutDisplayFunc(tampilkan)
	glutKeyboardFunc(keyPressed)
	
def main():
	global window
	
	glutInit(sys.argv)
	
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
	
	glutInitWindowSize(400,400)
	glutInitWindowPosition(40,100)
	
	window = glutCreateWindow("5 DOF Robot")
	
	init_robot()
	init()
	
	glutIdleFunc(Sim_main)
	
	glutMainLoop()
	
if __name__ == "__main__":
	print("Engine Started")
	main()
