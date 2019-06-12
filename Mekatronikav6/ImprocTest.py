from ImProcEngine import *
import sys

def main():
	cf.camera = cv2.VideoCapture(0) #untuk ganti kamera selanjutnya ganti angka 1
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
	
	while(True):
		tracking()
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
		
	
if __name__ == '__main__':
	main()
