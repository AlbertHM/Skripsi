from math import degrees, radians, cos, sin, atan2, sqrt, pow

e = [0, 0, -90, 0, 90, 45]
q = [radians(i) for i in e]


x = [ cos(q[5])*(cos(q[4])*(sin(q[0])*sin(q[3]) - cos(q[3])*(sin(q[0] + q[1] + q[2])/2 + sin(q[1] - q[0] + q[2])/2)) - sin(q[4])*(cos(q[0] + q[1] + q[2])/2 + cos(q[1] - q[0] + q[2])/2)) + sin(q[5])*(sin(q[0] - q[3])/2 + cos(q[0] - q[1] - q[2] + q[3])/4 - cos(q[0] + q[1] + q[2] + q[3])/4 + sin(q[0] + q[3])/2 + cos(q[0] + q[1] + q[2] - q[3])/4 - cos(q[1] - q[0] + q[2] + q[3])/4), cos(q[5])*(sin(q[0] - q[3])/2 + cos(q[0] - q[1] - q[2] + q[3])/4 - cos(q[0] + q[1] + q[2] + q[3])/4 + sin(q[0] + q[3])/2 + cos(q[0] + q[1] + q[2] - q[3])/4 - cos(q[1] - q[0] + q[2] + q[3])/4) - sin(q[5])*(cos(q[4])*(sin(q[0])*sin(q[3]) - cos(q[3])*(sin(q[0] + q[1] + q[2])/2 + sin(q[1] - q[0] + q[2])/2)) - sin(q[4])*(cos(q[0] + q[1] + q[2])/2 + cos(q[1] - q[0] + q[2])/2)), sin(q[4])*(sin(q[0])*sin(q[3]) - cos(q[3])*(sin(q[0] + q[1] + q[2])/2 + sin(q[1] - q[0] + q[2])/2)) + cos(q[4])*(cos(q[0] + q[1] + q[2])/2 + cos(q[1] - q[0] + q[2])/2), cos(q[0])/25 - (13*cos(q[0])*sin(q[1]))/100 + (19*sin(q[4])*(sin(q[0])*sin(q[3]) - cos(q[3])*(sin(q[0] + q[1] + q[2])/2 + sin(q[1] - q[0] + q[2])/2)))/200 + (19*cos(q[4])*(cos(q[0] + q[1] + q[2])/2 + cos(q[1] - q[0] + q[2])/2))/200]
y = [ - sin(q[5])*(cos(q[0] - q[3])/2 - sin(q[0] - q[1] - q[2] + q[3])/4 + sin(q[0] + q[1] + q[2] + q[3])/4 + cos(q[0] + q[3])/2 - sin(q[0] + q[1] + q[2] - q[3])/4 - sin(q[1] - q[0] + q[2] + q[3])/4) - cos(q[5])*(sin(q[4])*(sin(q[0] + q[1] + q[2])/2 - sin(q[1] - q[0] + q[2])/2) + cos(q[0])*cos(q[4])*sin(q[3])), sin(q[5])*(sin(q[4])*(sin(q[0] + q[1] + q[2])/2 - sin(q[1] - q[0] + q[2])/2) + cos(q[0])*cos(q[4])*sin(q[3])) - cos(q[5])*(cos(q[0] - q[3])/2 - sin(q[0] - q[1] - q[2] + q[3])/4 + sin(q[0] + q[1] + q[2] + q[3])/4 + cos(q[0] + q[3])/2 - sin(q[0] + q[1] + q[2] - q[3])/4 - sin(q[1] - q[0] + q[2] + q[3])/4), cos(q[4])*(sin(q[0] + q[1] + q[2])/2 - sin(q[1] - q[0] + q[2])/2) - cos(q[0])*sin(q[3])*sin(q[4]), sin(q[0])/25 - (13*sin(q[0])*sin(q[1]))/100 + (19*cos(q[4])*(sin(q[0] + q[1] + q[2])/2 - sin(q[1] - q[0] + q[2])/2))/200 - (19*cos(q[0])*sin(q[3])*sin(q[4]))/200]
z = [ cos(q[5])*(cos(q[4])*(cos(q[1] + q[2] + q[3])/2 + cos(q[1] + q[2] - q[3])/2) - sin(q[1] + q[2])*sin(q[4])) - sin(q[5])*(sin(q[1] + q[2] + q[3])/2 - sin(q[1] + q[2] - q[3])/2), - sin(q[5])*(cos(q[4])*(cos(q[1] + q[2] + q[3])/2 + cos(q[1] + q[2] - q[3])/2) - sin(q[1] + q[2])*sin(q[4])) - cos(q[5])*(sin(q[1] + q[2] + q[3])/2 - sin(q[1] + q[2] - q[3])/2), sin(q[1] + q[2] + q[4])/2 - sin(q[1] + q[2] - q[3] - q[4])/4 + sin(q[1] + q[2] - q[4])/2 + sin(q[1] + q[2] + q[3] + q[4])/4 - sin(q[1] + q[2] + q[3] - q[4])/4 + sin(q[1] + q[2] - q[3] + q[4])/4, (13*cos(q[1]))/100 + (9*cos(q[1])*cos(q[2]))/500 + (197*cos(q[1])*sin(q[2]))/1000 + (197*cos(q[2])*sin(q[1]))/1000 - (9*sin(q[1])*sin(q[2]))/500 + (19*cos(q[1])*cos(q[4])*sin(q[2]))/200 + (19*cos(q[2])*cos(q[4])*sin(q[1]))/200 + (19*cos(q[1])*cos(q[2])*cos(q[3])*sin(q[4]))/200 - (19*cos(q[3])*sin(q[1])*sin(q[2])*sin(q[4]))/200 + 81/1000]
u = [0,0,0,1]

#Pitch
pitch = atan2(x[2],sqrt((y[2]**2)+(z[2]**2)))
#Roll
if(pitch==radians(90) or pitch == radians(-90)):
	roll = 0
else:
	roll = atan2((-y[2]/cos(pitch)),(z[2]/cos(pitch)))
#Yaw
if(pitch == radians(90)):
	yaw = atan2(z[1],y[1])
elif(pitch == radians(-90)):
	yaw = -atan2(z[1],y[1])
else:
	yaw = atan2((-x[1]/cos(pitch)),(x[0]/cos(pitch)))


xyz	= [x[3], y[3], z[3], degrees(roll), degrees(pitch), degrees(yaw)]
print(xyz)
