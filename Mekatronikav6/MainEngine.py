import sys
import time
import datetime as dtime
import matplotlib.pyplot as plt
import serial

import config as cf
from RobotEngine import *
from VisualEngine import *
from ImProcEngine import *

N = cf.N
Period = cf.Period
lt = 0
ltold = 0

def init_robot():	
	#tempq = [90, 90, 150, 90, 90, 90]
	tempq = [0, 0, 0, 0, 0, 0]
	cf.q = [radians(i) for i in tempq]
	
def transmit():
	def limit(p):
		if(p>180):
			p=90
		elif(p<0):
			p=0
		return p
		
	ser.write(b'\xF5')
	#Joint 1
	u = -int(degrees(cf.q[0]))+90
	u = limit(u)
	ser.write(u.to_bytes(1,'little'))
	#Joint 2
	u = -int(degrees(cf.q[1]))+90
	u = limit(u)
	ser.write(u.to_bytes(1,'little'))
	#Joint 3
	u = int(degrees(cf.q[2]))+90
	u = limit(u)
	ser.write(u.to_bytes(1,'little'))
	#Joint 4
	u = -int(degrees(cf.q[3]))+90
	u = limit(u)
	ser.write(u.to_bytes(1,'little'))
	#Joint 5
	u = -int(degrees(cf.q[4]))+90
	u = limit(u)
	ser.write(u.to_bytes(1,'little'))
	#Joint 6
	u = -int(degrees(cf.q[5]))+90
	u = limit(u)
	ser.write(u.to_bytes(1,'little'))
	
	temp = 180
	ser.write(temp.to_bytes(1, 'little'))
	
def cetak():
	print("Q_Awal		=  {}".format([round(degrees(p),3) for p in cf.q_awal]))
	print("Q_Sekarang	=  {}".format([round(degrees(p),3) for p in cf.q]))
	print("Q_Final 	=  {}".format([round(degrees(p),3) for p in cf.q_final]))
	print("X_Awal 		=  {}".format([round(degrees(p),3) for p in cf.xyz_init]))
	print("X_Sekarang 	=  {}".format([round(degrees(p),3) for p in cf.xyz]))
	print("X_Final 	=  {}".format([round(degrees(p),3) for p in cf.xyz_final]))
	
def Sim_main():
	global lt, ltold
	logger = []
	loggery = []
	loggerz = []
	if(cf.CamBased == 1):
		cf.k = 0.0;
		tracking()
		if(cf.Fobj):
			cf.q_awal = cf.q[:]
			'''
			if(cf.Xobj in range(426,640) and cf.Yobj in range(160,320)):
				lt = 1
				cf.q_final = [radians(120), radians(90), radians(150), radians(90), radians(90), radians(90)]
			elif(cf.Xobj in range(0,213) and cf.Yobj in range(160,320)):
				lt = 2
				cf.q_final = [radians(60), radians(90), radians(150), radians(90), radians(90), radians(90)]
			elif(cf.Xobj in range(213,426) and cf.Yobj in range(0,160)):
				lt = 3
				cf.q_final = [radians(90), radians(120), radians(150),radians(90), radians(90), radians(90)]
			elif(cf.Xobj in range(213,426) and cf.Yobj in range(320,480)):
				lt = 4
				cf.q_final = [radians(90), radians(90), radians(150),radians(90), radians(90), radians(90)]
			'''
			a = (cf.DimensiFrame[1]//2-cf.Yobj) * (0.7 /cf.DimensiFrame[1]) # (Titik pusat objek - pusat frame) * m/px
			b = (cf.DimensiFrame[0]//2-cf.Xobj) * (0.94/cf.DimensiFrame[0])
			#print("Cam {} | {} | {} | {}".format(cf.Xobj,cf.Yobj,cf.dXobj,cf.dYobj))
			print("Cam {} | {} | {} | {}".format(cf.Xobj,cf.Yobj,a,b))
			'''
			if(lt != ltold):
				while(cf.k <= N):
					for p in range(0,2):
						control_joint(p)
					cf.k += 1
					forward_kinematic()
					tampilkan()
					if(cf.k%10 == 0):
						transmit()
						'''
			ltold = lt
		else:
			print("Objek tidak ditemukan")
		if cv2.waitKey(1) & 0xFF == ord("c"):
			cv2.destroyAllWindows()
			cf.CamBased = -1
			tracking()
	#Refresh	
	if(cf.refresh == 1):
		tampilkan()
		print("Refresh : qAwal({}), qcmd({}), qfinal({})".format([round(degrees(p),3) for p in cf.q_awal], [round(degrees(p),3) for p in cf.q_cmd], [round(degrees(p),3) for p in cf.q_final]))
		cf.refresh = 0
		
	#Return to Base
	if(cf.retbase == 1):
		print("++++++++++++++++++++++++++++++++++++++++++++++++")
		print("RETURN TO BASE")
		print("++++++++++++++++++++++++++++++++++++++++++++++++")
		cf.k = 0.0;
		cf.q_awal = cf.q[:]
		temp = [0,70,-20,0,0,0]
		cf.q_final = [radians(x) for x in temp]
		a = dtime.datetime.now()
		
		while(cf.k <= N):
			for p in range(0,6):
				control_joint(p)
			cf.k += 1
			forward_kinematic()
			tampilkan()
			#print("Sudut " + str([ round(degrees(p),3) for p in cf.q]))
			#print("Posisi " + str([ round(p,3) for p in xyz]))
			if(cf.k%10 == 0):
				transmit()
			
		b = dtime.datetime.now()
		c = b-a
		print("Elapsed Time : {} ms".format(c.total_seconds()*1000))
		cf.retbase = 0;
		
	#Joint Space
	if(cf.JS != -1) :
		print("++++++++++++++++++++++++++++++++++++++++++++++++")
		print("Joint Space : Joint({}), qAwal({}), qfinal({})".format(cf.JS, [round(degrees(p),3) for p in cf.q_awal], [round(degrees(p),3) for p in cf.q_final]))
		print("++++++++++++++++++++++++++++++++++++++++++++++++")
		cf.k = 0.0
		cf.q_awal = cf.q[:]
		a = dtime.datetime.now()
		while(cf.k <= N):
			#logging
			logger.append(degrees(cf.q[cf.JS]))
			control_joint(cf.JS)
			forward_kinematic()
			cf.k += 1
			tampilkan()			
			print("Sudut " + str([ round(degrees(p),3) for p in cf.q]))
			#print("Posisi " + str([ round(p,3) for p in xyz]))
			if(cf.k%10 == 0):
				transmit()
				#break
		b = dtime.datetime.now()
		c = b-a
		print("Elapsed Time : {} ms".format(c.total_seconds()*1000))
		#plt.plot(logger)
		#plt.show()
		cf.JS = -1;
		
	#Task Space	
	if(cf.TS != -1) :
		print("++++++++++++++++++++++++++++++++++++++++++++++++")
		print("Task Space")
		print("++++++++++++++++++++++++++++++++++++++++++++++++")
		cf.k = 0.0
		a = dtime.datetime.now()
		trajectory_init()
		
		while(cf.k <= N):
			print("+++ {}".format(cf.k))
			
			#Logging
			logger.append(cf.xyz[0])
			loggery.append(cf.xyz[1])
			loggerz.append(cf.xyz[2])
			
			#Proses
			trajectory_planning()
			double_differential()
			control_task()
			inverse_jacobian()
			double_integrator()
			forward_kinematic()
			
			if(cf.k%10 == 0):
				transmit()
			
			cf.k += 1
			tampilkan()
			
		b = dtime.datetime.now()
		c = b-a
		print("Elapsed Time : {} ms".format(c.total_seconds()*1000))
		plt.plot(logger,'g-',loggery,'r-', loggerz, 'b-')
		plt.legend(["X", "Y", "Z"])
		plt.show()
		cf.TS = -1
	
	#Bergerak menuju objek
	if(cf.xyobjek != -1):
		#Return to base
		cf.q_awal = cf.q[:]
		cf.k = 0.0;
		temp = [0,70,-20,0,0,0]
		cf.q_final = [radians(x) for x in temp]
		a = dtime.datetime.now()
		print("Sebelum retbase")
		cetak()
		while(cf.k <= N):
			for p in range(0,6):
				control_joint(p)
			cf.k += 1
			forward_kinematic()
			tampilkan()
			if(cf.k%10 == 0):
				transmit()
			
		b = dtime.datetime.now()
		c = b-a
		print("Elapsed Time : {} ms".format(c.total_seconds()*1000))
		
		#Moving X,Y
		cf.q_awal = cf.q[:]
		forward_kinematic()	
		cf.xyz_init = cf.xyz[:]
		cf.xyz_final = cf.xyz[:]
		cf.k = 0.0;
		tracking()
		
		if(cf.Fobj):
			print("Cam {} | {}".format(cf.Xobj,cf.Yobj))
			
			a = dtime.datetime.now()
			trajectory_init()
			
			#Positioning calculation
			cf.xyz_final[0] = (cf.DimensiFrame[1]//2-cf.Yobj) * (0.7 /cf.DimensiFrame[1]) # (Titik pusat objek - pusat frame) * m/px
			cf.xyz_final[1] = (cf.DimensiFrame[0]//2-cf.Xobj) * (0.94/cf.DimensiFrame[0])
			
			print("Sesudah Retbase Sebelum XY")
			cetak()
			while(cf.k <= N):
				#Proses
				trajectory_planning()
				double_differential()
				control_task()
				inverse_jacobian()
				double_integrator()
				forward_kinematic()				
				
				cf.k += 1
				forward_kinematic()
				tampilkan()
				if(cf.k%10 == 0):
					transmit()
			b = dtime.datetime.now()
			c = b-a
			print("XY Elapsed Time : {} ms".format(c.total_seconds()*1000))
			
			#Dropping
			forward_kinematic()	
			cf.q_awal = cf.q[:]
			cf.xyz_init = cf.xyz[:]
			cf.xyz_final = cf.xyz[:]
			cf.k = 0
			
			a = dtime.datetime.now()
			trajectory_init()
			
			#Positioning calculation
			cf.xyz_final[2] -= 0.2
			print("Sesudah XY Sebelum Z")
			cetak()
			
			while(cf.k <= N):
				#Proses
				trajectory_planning()
				double_differential()
				control_task()
				inverse_jacobian()
				double_integrator()
				forward_kinematic()				
				
				cf.k += 1
				forward_kinematic()
				tampilkan()
				if(cf.k%10 == 0):
					transmit()
			b = dtime.datetime.now()
			c = b-a
			print("Z Elapsed Time : {} ms".format(c.total_seconds()*1000))
			print("Selesai")
			cetak()
			
		else:
			print("Objek tidak ditemukan")
			
		if cv2.waitKey(1) & 0xFF == ord("n"):
			cv2.destroyAllWindows()
			cf.xyobjek = -1
			tracking()
		cf.xyobjek = -cf.xyobjek
	
	#Simulasi Gerak 
	if(cf.jalan == 1):
		cf.k = 0
		while(cf.k <= N):
			cf.mxyz[0] = cf.mxyz[0] - (0.5/N)
			cf.bxyz[0] = cf.mxyz[0]
			cf.k += 1
			tampilkan()
		cf.jalan = 0
		

def keyPressed(key, x, y):
	global CamBased
	forward_kinematic()
	cf.q_final = cf.q[:]
	cf.xyz_final = cf.xyz[:]
	
	ch = key.decode("utf-8")
	
	# JIka ditekan tombol escape
	if ch == chr(27):
		cf.camera.release() #jangan lupa direlease
		cv2.destroyAllWindows()
		sys.exit()
		
	# Return to base
	elif ch == 'z':
		print("a")
		cf.retbase = 1
	# Refresh
	elif ch == 'x':
		cf.refresh = 1
	# Toggling Camera
	elif ch == 'c':
		cf.CamBased = -cf.CamBased
		
	#Joint space
	elif ch == 'a':
		cf.q_final[0] += radians(10)
		cf.JS = 0
	elif ch == 'A':
		cf.q_final[0] += -radians(10)
		cf.JS = 0
	elif ch == 's':
		cf.q_final[1] += radians(10)
		cf.JS = 1
	elif ch == 'S':
		cf.q_final[1] += -radians(10)
		cf.JS = 1
	elif ch == 'd':
		cf.q_final[2] += radians(10)
		cf.JS = 2
	elif ch == 'D':
		cf.q_final[2] += -radians(10)
		cf.JS = 2
	elif ch == 'f':
		cf.q_final[3] += radians(10)
		cf.JS = 3
	elif ch == 'F':
		cf.q_final[3] += -radians(10)
		cf.JS = 3
	elif ch == 'g':
		cf.q_final[4] += radians(10)
		cf.JS = 4
	elif ch == 'G':
		cf.q_final[4] += -radians(10)
		cf.JS = 4
	elif ch == 'h':
		cf.q_final[5] += radians(10)
		cf.JS = 5
	elif ch == 'H':
		cf.q_final[5] += -radians(10)
		cf.JS = 5
		
	#Task Space
	elif ch == 'q':
		cf.xyz_final[0]	+= 0.1
		cf.TS = 1
	elif ch == 'w':
		cf.xyz_final[1]	+= 0.1
		cf.TS = 1
	elif ch == 'e':
		cf.xyz_final[2]	+= 0.1
		cf.TS = 1
	elif ch == 'Q':
		cf.xyz_final[0]	-= 0.1
		cf.TS = 1
	elif ch == 'W':
		cf.xyz_final[1]	-= 0.1
		cf.TS = 1
	elif ch == 'E':
		cf.xyz_final[2]	-= 0.1
		cf.TS = 1
	
	#ETC
	elif ch == 'v':
		cf.jalan = 1
	elif ch == 'b':
		'''
		cf.xyz_final[0] = cf.bxyz[0]
		cf.xyz_final[1] = cf.bxyz[1]
		cf.xyz_final[2] = cf.bxyz[2]'''
		cf.xyz_final[0] = 0.307
		cf.xyz_final[1] = 0
		cf.xyz_final[2] = -0.196
		cf.TS = 1
		
	elif ch == 'n':
		cf.xyobjek = -cf.xyobjek
	
def init():
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
	
	window = glutCreateWindow("6 DOF Robot")
	
	init_robot()
	init()
	
	glutIdleFunc(Sim_main)
	
	glutMainLoop()
	
if __name__ == "__main__":
	ser = serial.Serial('/dev/ttyACM0', 250000) # Establish the connection on a specific port
	cf.camera = cv2.VideoCapture(1) #untuk ganti kamera selanjutnya ganti angka 1
	print("---Warming Up Camera!---")
	
	#Progress Bar
	toolbar_width = 20 #2 Sec
	sys.stdout.write("[%s]" % (" " * toolbar_width))
	sys.stdout.flush()
	sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['
	for i in range(toolbar_width):
		time.sleep(0.1) # do real work here
		# update the bar
		sys.stdout.write("#")
		sys.stdout.flush()
	sys.stdout.write("\n")
	#End of progress bar
	
	(grab, frame) = cf.camera.read()
	cf.DimensiFrame[0] = frame.shape[1]	
	cf.DimensiFrame[1] = frame.shape[0]
	if not grab:
		print("Gagal mengambil gambar dari kamera")
	
	print("Program Jalan!")
	main()
