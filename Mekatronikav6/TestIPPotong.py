#Testing titik potong wrong
#Bug terjadi ketika dua titik memiliki nilai x yang sama sehingga persamaan menjadi x = konstanta

a = [[437.50006103515625, 211.50003051757812], [451.50006103515625, 197.50003051757812], [451.50006103515625, 225.50003051757812], [465.50006103515625, 211.50003051757812]]

def titikPotong(titik):
	#garis1[0] = gradien ; garis1[1] = konstanta
	garis1 = persGaris(titik[0],titik[3])
	garis2 = persGaris(titik[1],titik[2])
	x=(garis1[1]-garis2[1])/(garis2[0]-garis1[0]) #pers subtitusi y=y
	y=garis1[0]*x+garis1[1] #subtitusi x ke pers 1
	return math.floor(int(x)),math.floor(int(y))

def persGaris(titik1,titik2):
	y1 = titik1[0]
	y2 = titik2[0]
	x1 = titik1[1]
	x2 = titik2[1]
	m = (y2-y1)/(x2-x1)
	c = -m*x1+y1
	return m,c
	
	
print(titikPotong(a))
