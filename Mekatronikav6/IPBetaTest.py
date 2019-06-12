#from ImProcEngine import *
import config as cf
import sys
from collections import deque
import cv2
import numpy as np
import time
import math

#format titik pada pemrosesan selalu y,x

(dX,dY) = (0,0)
counter = 0
pts = deque(maxlen=32)
lebarframe = [0,0]

def persGaris(titik1,titik2):
	y1 = titik1[0]
	y2 = titik2[0]
	x1 = titik1[1]
	x2 = titik2[1]
	m = (y2-y1)/(x2-x1)
	c = -m*x1+y1
	return m,c
	
def titikPotong(titik):
	#garis1[0] = gradien ; garis1[1] = konstanta
	garis1 = persGaris(titik[0],titik[3])
	garis2 = persGaris(titik[1],titik[2])
	x=(garis1[1]-garis2[1])/(garis2[0]-garis1[0]) #pers subtitusi y=y
	y=garis1[0]*x+garis1[1] #subtitusi x ke pers 1
	return math.floor(int(x)),math.floor(int(y))
	
def fkemiringan(titik1,titik2):	
	m = persGaris(titik1,titik2)[0]
	return math.degrees(math.atan(m))
	
def nothing(x):
	pass

def preview():
	cf.camera = cv2.VideoCapture(2)
	#print

def tracking():
	global counter, dX, dY
	cf.Fobj = 0
	v_min = np.array([0,157,117],dtype = "uint8")
	v_max = np.array([29,233,220],dtype = "uint8")
	#cf.camera = cv2.VideoCapture(0)
	(grabbed, frame) = cf.camera.read()
	if not grabbed:
		return
	frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	thresh = cv2.inRange(frame1, v_min, v_max)
	color_desired = cv2.GaussianBlur(thresh, (11,11), 0)
	(_, cnts, _) = cv2.findContours(color_desired, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	
	if(len(cnts)>0):
		cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
		titik = cv2.boxPoints(cv2.minAreaRect(cnt))
		rect = np.int32(titik)
		cv2.drawContours(frame, [rect], -1, (0,255,0), 2) #gambar objek yang terdeteksi
		
		titikdasar = [scaleperspective(x) for x in titik]
		print("%%%%")
		print(titik)
		print(titikdasar)
		print("%%%%")
		rectdasar = np.int32(titikdasar)
		cv2.drawContours(frame, [rectdasar], -1, (255,0,0), 1) #gambar dasar objek yang terdeteksi
				
		titik = sorted(titik.tolist())
		kemiringan = fkemiringan(titik[2], titik[3])
		try:
			center = titikPotong(titik)
			pts.appendleft(center)
			cf.Yobj = center[0]
			cf.Xobj = center[1]
			cf.Fobj = 1
		except:
			print("Image Processing Engine Failure")
			print(titik)
		for i in np.arange(1, len(pts)):
			if pts[i-1] is None or pts[i] is None :
				continue
			if counter >= 10 and i == 1 and len(pts) >= 10 and pts[-10] is not None:
				dX = pts[-10][0] - pts[i][0]
				dY = pts[-10][1] - pts[i][1]
				cf.dXobj = dX
				cf.dYobj = dY
		cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
		cv2.putText(frame, "{},{},{}*".format(center[0],center[1],"%.2f"%kemiringan), (center[1],center[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255,200,0), 1)
	
	#cv2.imshow("Filter",thresh)# Display Actual Video + Frame
	#cv2.rectangle(frame, (x0,y0), (x1,y1), (255,255,0),1)
	cv2.imshow("Video", frame)	
	counter +=1


def scaleperspective(titik):
	tinggikamera = 1.1
	sudutkamera  = math.radians(60) #https://support.logitech.com/en_us/article/17556
	tinggiobjek = 0.1 #m
	ymaxreal = 0.68 / 2
	xmaxreal = 0.89 /2
	p = [0,0]
	dfalse = [titik[x]-lebarframe[x] for x in range(len(titik))]
	#Y Correction
	yfalse = dfalse[0] * (ymaxreal/(lebarframe[1]/2))
	print("DPXFalse :" + str(dfalse))
	theta = math.atan2(yfalse,(tinggikamera-tinggiobjek))
	yreal = (theta/(0.5*sudutkamera))*(lebarframe[1]/2)
	'''
	if(titik[0] < lebarframe[0]/2):
		p[0] = (lebarframe[0]/2)- yreal
	else:
		p[0] = (lebarframe[0]/2)+ yreal	'''	
		
	#X Correction
	xfalse = dfalse[1] * (xmaxreal/(lebarframe[0]/2))
	theta = math.atan2(xfalse,(tinggikamera-tinggiobjek))
	xreal = (theta/(0.5*sudutkamera))*(lebarframe[0]/2)
	'''
	if(titik[0] < lebarframe[0]/2):
		p[1] = (lebarframe[1]/2)- yreal
	else:
		p[1] = (lebarframe[1]/2)+ yreal		'''
	print("DPXReal :" + str(yreal) +" "+ str(xreal))

	p[0] = titik[0]-(yfalse-yreal)
	p[1] = titik[1]-(xfalse-xreal)
	return [int(i) for i in p]
	

def main():
	global lebarframe
	
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
	if not grab:
		print("Gagal mengambil gambar dari kamera")
		sys.exit()
	lebarframe = frame.shape[:]
	
	while(True):
		tracking()
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
		
	
if __name__ == '__main__':
	main()
