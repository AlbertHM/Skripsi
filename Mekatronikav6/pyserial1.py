#Integrate with communicateup2.ino
#Success, sending 2 bytes
#Order from left to right
# 255 = b'\xff\x00'; 256 = b'\x00\x01'

import time
import serial

ser = serial.Serial('/dev/ttyACM0', 9600) # Establish the connection on a specific port
time.sleep(2)


print(ser.readline())
#ser.write('1'.encode())

while True:
	var = input("Give me : ") #get input from user
	print("you entered " + var) #print the input for confirmation
	temp = int(var)
	sign = 1
	#ser.write(b'\xF5');
	ser.write(temp.to_bytes(2,'little')) #1 bytes
	#ser.write(sign.to_bytes(1,'little')) #2 bytes
	print("==")
	print(temp.to_bytes(2,'little'))
	print(sign.to_bytes(1,'little'))
	print("==")
	while(ser.in_waiting):
		print(ser.readline())
	ser.flushInput()
	ser.flushOutput()
	#print(ser.readline())

'''
while True:
	var = input("Give me : ") #get input from user
	print("you entered " + var) #print the input for confirmation
	if (var == '1'): #if the value is 1
		ser.write('1'.encode()) #send 1
		print ("LED turned ON")
		time.sleep(1)

	if (var == '0'): #if the value is 0
		ser.write('0'.encode()) #send 0
		print ("LED turned OFF")
		time.sleep(1)
'''
