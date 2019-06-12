import serial
import time

ser = serial.Serial('/dev/ttyACM0', 250000)
time.sleep(2)
'''
u = 0
while(u<100):
	ser.write(b'xF5')
	for p in range(0,7):
		temp = u+p
		ser.write(temp.to_bytes(1,'little'))
	time.sleep(0.5)
	print("Iterasi" + str(u))
	u += 1
'''

ser.write(b'\xF5')
x = 91.5
for p in range(0,7):
	u = int(x)
	ser.write(u.to_bytes(1,'little'))
	

'''

ser.write(b'\xF5')
for i in range(0,7):
	ser.write(i.to_bytes(1,'little'))
'''

#ser.flushOutput()
