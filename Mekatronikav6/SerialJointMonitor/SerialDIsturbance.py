import serial
import time

ser = serial.Serial('/dev/ttyACM0', 250000)
time.sleep(2)

ser.write(b'\xFF')
