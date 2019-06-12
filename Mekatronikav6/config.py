ESCAPE = 27

# Panjang Link
LR = [16, 14, 25.5, 16, 6, 15]
rasio = 0.01
L = [0, 0, 0, 0, 0, 0]
for i in range(0,len(LR)):
	L[i] = LR[i]*rasio

# Posisi Kamera
p 			= [-1.5, 1, 1.5]

# Control Parameter
q			= [0, 0, 0, 0, 0, 0]
q_awal		= [0,0,0,0,0,0]
q_cmd		= [0,0,0,0,0,0]
q_final		= [0,0,0,0,0,0]
dq			= [0,0,0,0,0,0]
dq_old		= [0,0,0,0,0,0]
dq_ref		= [0,0,0,0,0,0]
ddq_ref		= [0,0,0,0,0,0]
ddq			= [0,0,0,0,0,0]
det			= 0
'''
xyz_init	= [0,0,0,0,0,0]
xyz 		= [0,0,0,0,0,0]
xyz_cmd 	= [0,0,0,0,0,0]
xyz_final	= [0,0,0,0,0,0]
dxyz 		= [0,0,0,0,0,0]
dxyz_old	= [0,0,0,0,0,0]
ddxyz_ref	= [0,0,0,0,0,0]
ddxyz 		= [0,0,0,0,0,0]
'''
xyz_init	= [0,0,0]
xyz 		= [0,0,0]
xyz_cmd 	= [0,0,0]
xyz_final	= [0,0,0]
dxyz 		= [0,0,0]
dxyz_old	= [0,0,0]
ddxyz_ref	= [0,0,0]
ddxyz 		= [0,0,0]


KpJ			= 0.0002
KvJ			= 0.014
'''
KpT			= 0.1
KiT			= 0
KvT			= 0.1
'''
KpT			= 0.1
KiT			= 0
KvT			= 0.1
N			= 1000.0
Period		= 0.0025
k			= 0.0
JS			= -1
TS			= -1
refresh		= 0
retbase		= 0

mxyz		= [0.5,0.5]
bxyz		= [0.5,0.5,0.1]

#Button
angkat		= 0
jalan		= 0
xyobjek		= -1
CamBased 	= -1

# Image Processing
DimensiFrame	= [0,0]
camera	= 0
Xobj	= 0
Yobj	= 0
dXobj	= 0
dYobj	= 0
Fobj	= 0
