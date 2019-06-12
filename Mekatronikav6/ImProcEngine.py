import config as cf
from collections import deque
import cv2
import numpy as np
import time
import math

(dX,dY) = (0,0)
counter = 0
pts = deque(maxlen=32)

#Konstanta Warna

#Kuning
#BatasBawah	= [0,157,117]
#BatasAtas 	= [29,233,220]


BatasBawah	= [50,100,70]
BatasAtas 	= [70,175,120]

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
	v_min = np.array(BatasBawah,dtype = "uint8")
	v_max = np.array(BatasAtas,dtype = "uint8")
	if(cf.CamBased == -1 and cf.xyobjek == -1):
		cv2.destroyAllWindows()
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
		cv2.drawContours(frame, [rect], -1, (0,255,0), 2)
		titik = sorted(titik.tolist())
		kemiringan = fkemiringan(titik[2], titik[3])
		try:
			center = titikPotong(titik) #dapat center = [x,y]
			pts.appendleft(center)
			cf.Xobj = center[1]
			cf.Yobj = center[0]
			cf.Fobj = 1
		except:
			print("Image Processing Engine Failure")
			print(titik)
			#Error persamaan x = c
			center = [0,0]
			pts.appendleft(center)
			cf.Xobj = center[1]
			cf.Yobj = center[0]
			cf.Fobj = 1
		for i in np.arange(1, len(pts)):
			if pts[i-1] is None or pts[i] is None :
				continue
			if counter >= 10 and i == 1 and len(pts) >= 10and pts[-10] is not None:
				dX = pts[-10][0] - pts[i][0]
				dY = pts[-10][1] - pts[i][1]
				cf.dXobj = dX
				cf.dYobj = dY
		a =2
		b =2
		x0, x1, y0, y1 = frame.shape[1]//2-a, frame.shape[1]//2+a, frame.shape[0]//2-b, frame.shape[0]//2+b
		cv2.rectangle(frame, (x0,y0), (x1,y1), 255, -1)
		cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
		cv2.putText(frame, "{},{},{}*".format(center[0],center[1],"%.2f"%kemiringan), (center[1],center[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255,200,0), 1)
	
	#cv2.imshow("Filter",thresh)# Display Actual Video + Frame
	#cv2.rectangle(frame, (x0,y0), (x1,y1), (255,255,0),1)
	if(cf.xyobjek!=1):
		cv2.imshow("Video", frame)	
	counter +=1
