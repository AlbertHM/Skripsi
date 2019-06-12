import time
import datetime as dtime
x = 0

while(x<100):
	a = dtime.datetime.now()
	#0.001 = 1ms
	#0.0001 = 100 us
	time.sleep(0.0007)
	b = dtime.datetime.now()
	c = b-a
	#print("Elapsed Time : {} ms".format(c.total_seconds()*1000))
	print("Elapsed Time : {} us".format(c.total_seconds()*1000000))
	x+=1

'''
#this logic consume 11 us
u = 1000
p = 500

a = dtime.datetime.now()

f = u-p
if(x>1):
	pass
b = dtime.datetime.now()
c = b-a
print("Elapsed Time : {} us".format(c.total_seconds()*1000000))'''
