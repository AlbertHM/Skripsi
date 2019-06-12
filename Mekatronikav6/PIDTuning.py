#PID Tuning
#Albert Harazaki Mendrofa
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import config as cf
from RobotEngine import *

class app(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self,parent)
		self.parent = parent
		label1 = tk.Label(self, text =  "AYY", bg='Red',fg='white')
		self.logx = [0]
		self.logy = [0]
		self.logz = [0]		
		
		FrameUtama = tk.Frame(self.parent, relief='groove',borderwidth=3)
		fGraph = tk.Frame(self.parent, relief = 'groove', borderwidth =3)
		
		fTS = tk.Frame(FrameUtama, relief='groove',borderwidth=3)
		fJS = tk.Frame(FrameUtama, relief='groove',borderwidth=3)
		fPID =  tk.Frame(FrameUtama, relief='groove',borderwidth=3)
		bsim = tk.Button(FrameUtama, text = 'Simulate', bg='red', command=lambda:self.runSim())
		
		#Joint Space
		fJS1 = tk.Frame(fJS)
		fJS2 = tk.Frame(fJS)
		
		fq11 = tk.Frame(fJS1)
		fq21 = tk.Frame(fJS1)
		fq31 = tk.Frame(fJS1)
		fq41 = tk.Frame(fJS1)
		fq51 = tk.Frame(fJS1)
		fq61 = tk.Frame(fJS1)
		
		fq12 = tk.Frame(fJS2)
		fq22 = tk.Frame(fJS2)
		fq32 = tk.Frame(fJS2)
		fq42 = tk.Frame(fJS2)
		fq52 = tk.Frame(fJS2)
		fq62 = tk.Frame(fJS2)
		fq =[fq11,fq21,fq31,fq41,fq51,fq61,fq12,fq22,fq32,fq42,fq52,fq62]
		
		self.q11 = tk.DoubleVar()
		self.q21 = tk.DoubleVar()
		self.q31 = tk.DoubleVar()
		self.q41 = tk.DoubleVar()
		self.q51 = tk.DoubleVar()
		self.q61 = tk.DoubleVar()
		self.q12 = tk.DoubleVar()
		self.q22 = tk.DoubleVar()
		self.q32 = tk.DoubleVar()
		self.q42 = tk.DoubleVar()
		self.q52 = tk.DoubleVar()
		self.q62 = tk.DoubleVar()
		
		lq11 = tk.Label(fq11, text = "Q1 Awal")
		lq21 = tk.Label(fq21, text = "Q2 Awal")
		lq31 = tk.Label(fq31, text = "Q3 Awal")
		lq41 = tk.Label(fq41, text = "Q4 Awal")
		lq51 = tk.Label(fq51, text = "Q5 Awal")
		lq61 = tk.Label(fq61, text = "Q6 Awal")
		self.lq1 = [lq11, lq21, lq31, lq41, lq51, lq61]
		
		eq11 = tk.Entry(fq11, width = 5, textvariable = self.q11)
		eq21 = tk.Entry(fq21, width = 5, textvariable = self.q21)
		eq31 = tk.Entry(fq31, width = 5, textvariable = self.q31)
		eq41 = tk.Entry(fq41, width = 5, textvariable = self.q41)
		eq51 = tk.Entry(fq51, width = 5, textvariable = self.q51)
		eq61 = tk.Entry(fq61, width = 5, textvariable = self.q61)
		self.eq1 = [eq11, eq21, eq31, eq41, eq51, eq61]
				
		lq12 = tk.Label(fq12, text = "Q1 Akhir")
		lq22 = tk.Label(fq22, text = "Q2 Akhir")
		lq32 = tk.Label(fq32, text = "Q3 Akhir")
		lq42 = tk.Label(fq42, text = "Q4 Akhir")
		lq52 = tk.Label(fq52, text = "Q5 Akhir")
		lq62 = tk.Label(fq62, text = "Q6 Akhir")
		self.lq2 = [lq12, lq22, lq32, lq42, lq52, lq62]
		
		eq12 = tk.Entry(fq12, width = 5, textvariable = self.q12)
		eq22 = tk.Entry(fq22, width = 5, textvariable = self.q22)
		eq32 = tk.Entry(fq32, width = 5, textvariable = self.q32)
		eq42 = tk.Entry(fq42, width = 5, textvariable = self.q42)
		eq52 = tk.Entry(fq52, width = 5, textvariable = self.q52)
		eq62 = tk.Entry(fq62, width = 5, textvariable = self.q62)
		self.eq2 = [eq12, eq22, eq32, eq42, eq52, eq62]
		
		#Task Space		
		fTS1 = tk.Frame(fTS)
		fTS2 = tk.Frame(fTS)
		
		fx1 = tk.Frame(fTS1)
		fy1 = tk.Frame(fTS1)
		fz1 = tk.Frame(fTS1)
		fr1 = tk.Frame(fTS1)
		fp1 = tk.Frame(fTS1)
		fw1 = tk.Frame(fTS1)
		
		fx2 = tk.Frame(fTS2)
		fy2 = tk.Frame(fTS2)
		fz2 = tk.Frame(fTS2)
		fr2 = tk.Frame(fTS2)
		fp2 = tk.Frame(fTS2)
		fw2 = tk.Frame(fTS2)
		
		self.x1 = tk.DoubleVar()
		self.y1 = tk.DoubleVar()
		self.z1 = tk.DoubleVar()
		self.r1 = tk.DoubleVar()
		self.p1 = tk.DoubleVar()
		self.w1 = tk.DoubleVar()
		self.x2 = tk.DoubleVar()
		self.y2 = tk.DoubleVar()
		self.z2 = tk.DoubleVar()
		self.r2 = tk.DoubleVar()
		self.p2 = tk.DoubleVar()
		self.w2 = tk.DoubleVar()
		
		lx1 = tk.Label(fx1, text = "X Awal")
		ly1 = tk.Label(fy1, text = "Y Awal")
		lz1 = tk.Label(fz1, text = "Z Awal")
		lr1 = tk.Label(fr1, text = "R Awal")
		lp1 = tk.Label(fp1, text = "P Awal")
		lw1 = tk.Label(fw1, text = "W Awal")
		self.lx1 = [lx1, ly1, lz1, lr1, lp1, lw1]
		
		ex1 = tk.Entry(fx1, width = 5, textvariable = self.x1)
		ey1 = tk.Entry(fy1, width = 5, textvariable = self.y1)
		ez1 = tk.Entry(fz1, width = 5, textvariable = self.z1)
		er1 = tk.Entry(fr1, width = 5, textvariable = self.r1)
		ep1 = tk.Entry(fp1, width = 5, textvariable = self.p1)
		ew1 = tk.Entry(fw1, width = 5, textvariable = self.w1)
		self.exyz1 = [ex1, ey1, ez1, er1, ep1, ew1]
				
		lx2 = tk.Label(fx2, text = "X Akhir")
		ly2 = tk.Label(fy2, text = "Y Akhir")
		lz2 = tk.Label(fz2, text = "Z Akhir")
		lr2 = tk.Label(fr2, text = "R Akhir")
		lp2 = tk.Label(fp2, text = "P Akhir")
		lw2 = tk.Label(fw2, text = "W Akhir")
		self.lx2 = [lx2, ly2, lz2, lr2, lp2, lw2]
		
		ex2 = tk.Entry(fx2, width = 5, textvariable = self.x2)
		ey2 = tk.Entry(fy2, width = 5, textvariable = self.y2)
		ez2 = tk.Entry(fz2, width = 5, textvariable = self.z2)
		er2 = tk.Entry(fr2, width = 5, textvariable = self.r2)
		ep2 = tk.Entry(fp2, width = 5, textvariable = self.p2)
		ew2 = tk.Entry(fw2, width = 5, textvariable = self.w2)
		self.exyz2 = [ex2, ey2, ez2, er2, ep2, ew2]
		
		fKpJ = tk.Frame(fPID)
		fKiJ = tk.Frame(fPID)
		fKvJ = tk.Frame(fPID)
		fKpT = tk.Frame(fPID)
		fKiT = tk.Frame(fPID)
		fKvT = tk.Frame(fPID)
		AFK = [fKpJ, fKiJ, fKvJ, fKpT, fKiT, fKvT]
		
		lk1 = tk.Label(fKpJ, text="Kp J")
		lk2 = tk.Label(fKiJ, text="Ki J")
		lk3 = tk.Label(fKvJ, text="Kv J")
		lk4 = tk.Label(fKpT, text="Kp T")
		lk5 = tk.Label(fKiT, text="Ki T")
		lk6 = tk.Label(fKvT, text="Kv T")
		self.lk = [lk1, lk2, lk3, lk4, lk5, lk6]
		
		self.KpJ = tk.DoubleVar()
		self.KiJ = tk.DoubleVar()
		self.KvJ = tk.DoubleVar()
		self.KpT = tk.DoubleVar()
		self.KiT = tk.DoubleVar()
		self.KvT = tk.DoubleVar()
		self.Kons = [self.KpJ, self.KiJ, self.KvJ, self.KpT, self.KiT, self.KvT]
		
		eKpJ = tk.Entry(fKpJ, width = 10, textvariable = self.KpJ)
		eKiJ = tk.Entry(fKiJ, width = 10, textvariable = self.KiJ)
		eKvJ = tk.Entry(fKvJ, width = 10, textvariable = self.KvJ)
		eKpT = tk.Entry(fKpT, width = 10, textvariable = self.KpT)
		eKiT = tk.Entry(fKiT, width = 10, textvariable = self.KiT)
		eKvT = tk.Entry(fKvT, width = 10, textvariable = self.KvT)
		self.AEK = [eKpJ, eKiJ, eKvJ, eKpT, eKiT, eKvT]
		
		PKpJ = tk.Button(fKpJ, text = '+', bg = 'blue', command=lambda:self.nambah(1))
		PKiJ = tk.Button(fKiJ, text = '+', bg = 'blue', command=lambda:self.nambah(2))
		PKvJ = tk.Button(fKvJ, text = '+', bg = 'blue', command=lambda:self.nambah(3))
		PKpT = tk.Button(fKpT, text = '+', bg = 'blue', command=lambda:self.nambah(4))
		PKiT = tk.Button(fKiT, text = '+', bg = 'blue', command=lambda:self.nambah(5))
		PKvT = tk.Button(fKvT, text = '+', bg = 'blue', command=lambda:self.nambah(6))
		APEK = [PKpJ, PKiJ, PKvJ, PKpT, PKiT, PKvT]
		
		NKpJ = tk.Button(fKpJ, text = '-', bg = 'blue', command=lambda:self.kurang(1))
		NKiJ = tk.Button(fKiJ, text = '-', bg = 'blue', command=lambda:self.kurang(2))
		NKvJ = tk.Button(fKvJ, text = '-', bg = 'blue', command=lambda:self.kurang(3))
		NKpT = tk.Button(fKpT, text = '-', bg = 'blue', command=lambda:self.kurang(4))
		NKiT = tk.Button(fKiT, text = '-', bg = 'blue', command=lambda:self.kurang(5))
		NKvT = tk.Button(fKvT, text = '-', bg = 'blue', command=lambda:self.kurang(6))
		ANEK = [NKpJ, NKiJ, NKvJ, NKpT, NKiT, NKvT]
		
		fig = Figure()
		self.ax = fig.add_subplot(111)
		self.linex, = self.ax.plot(self.logx)

		self.canvas = FigureCanvasTkAgg(fig,master=fGraph)
		self.canvas.draw()
		self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
		
		#Packing
		FrameUtama.pack(side="left")
		fGraph.pack(side="left")
		fTS.pack()
		fJS.pack()
		fPID.pack()
		bsim.pack()
		
		fTS1.grid(row=1,column=1)
		fTS2.grid(row=1,column=2)		
		fJS1.grid(row=1,column=1)
		fJS2.grid(row=1,column=2)
		
		for i in fq:
			i.pack()
		for i in self.lq1:
			i.pack(side='left')
		for i in self.eq1:
			i.pack(side='left')
		for i in self.lq2:
			i.pack(side='left')
		for i in self.eq2:
			i.pack(side='left')
			
		
		fx1.pack()
		fy1.pack()
		fz1.pack()
		fr1.pack()
		fp1.pack()
		fw1.pack()
		
		fx2.pack()
		fy2.pack()
		fz2.pack()
		fr2.pack()
		fp2.pack()
		fw2.pack()
		
		for i in self.lx1 :
			i.grid(column = 1)
		for i in self.exyz1:
			i.grid(column = 2)
		for i in self.lx2 :
			i.grid(column = 1)
		for i in self.exyz2:
			i.grid(column = 2)		
		for i in AFK:
			i.pack()
		for i in self.lk:
			i.grid(row=1,column=1)
		for i in self.AEK:
			i.grid(row=1,column=2)
		for i in APEK:
			i.grid(row=1,column=3)
		for i in ANEK:
			i.grid(row=1,column=4)
		
		label1.pack()
		
	def nambah(self, blok):
		blok -= 1
		a = float(self.AEK[blok].get())+0.1
		self.AEK[blok].delete(0, tk.END)
		self.AEK[blok].insert(0, str(a))
		self.runSim()
	
	def kurang(self, blok):
		blok -= 1
		a = float(self.AEK[blok].get())-0.1
		self.AEK[blok].delete(0, tk.END)
		self.AEK[blok].insert(0, str(a))
		self.runSim()
	
	def runSim(self):
		cf.ddxyz = [0,0,0]
		self.logx = []
		self.logy = []
		self.logz = []
		cf.k=0
		N = 1000
		cf.KpT = float(self.AEK[3].get())
		cf.KiT = float(self.AEK[4].get())
		cf.KvT = float(self.AEK[5].get())
		
		for i in range(0,len(self.eq1)):
			cf.q[i] = float(self.eq1[i].get())
		#for i in range(0,len(self.exyz2)):
		for i in range(0,3):
			cf.xyz_final[i] = float(self.exyz2[i].get())
		akhir = [i for i in cf.xyz_final]
		
		forward_kinematic()
		awal = [i for i in cf.xyz]
		trajectory_init()
		while(cf.k <= N):
			self.logx.append(cf.xyz[0])
			self.logy.append(cf.xyz[1])
			self.logz.append(cf.xyz[2])
			
			trajectory_planning()
			double_differential()
			control_task()
			inverse_jacobian()
			double_integrator()
			forward_kinematic()
			cf.k += 1
		print(awal)
		print("final")
		print(akhir)
		#self.linex.set_xdata(p)
		self.ax.clear()
		self.linex, = self.ax.plot(self.logx)
		#print(self.logx)
		#self.linex.set_xdata(self.logx)
		#self.linex.set_ydata(len(self.logx))
		self.ax.set_xlim(0,1000)
		#self.ax.set_ylim([max(self.logx), min(self.logx)])
		self.ax.set_ylim(min(self.logx),max(self.logx))
		#self.linex.set_xdata(range(500))
		self.canvas.draw()
	

if __name__ == '__main__':
	root = tk.Tk()
	run = app(root)
	root.mainloop()
