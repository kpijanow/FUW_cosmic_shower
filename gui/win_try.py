import matplotlib
matplotlib.use("TkAgg")
from matplotlib import style
style.use('ggplot')
from matplotlib import gridspec

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation

import tkinter as tk
from tkinter import ttk
import time
from random import randint
import threading
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.misc import imread

from vec import det_plot




def animate(i):

	pullData = open('sampleText.txt','r').read()
	dataArray = pullData.split('\n')
	xar=[]
	yar=[]

	#Flux graph
	a = f2.add_subplot(gs[0,:-1])
	
	for eachLine in dataArray:
		if len(eachLine)>1:
			x,y = eachLine.split(',')
			xar.append(int(x))
			yar.append(int(y))

	a.clear()
	a.plot(xar[-200:],yar[-200:])

	#What will happend without new data to read? 
	t = threading.Thread(target=sim_one)
	t.start()	

	#return vec_t


def ani_shower(i, vec_t, vec_d):	
	
	a_sh = f2.add_subplot(gs[1:,:-1], projection='3d')
	a_sh.clear()
	#print(vec_t)
	rot, angle = det_plot(vec_t,vec_d, a_sh)
	rot.view_init(elev = 30, azim = i%360)
	app.set_angle(angle)

def animate_his(i):

	ax_h = f2.add_subplot(gs[-1, -1])
	ang = app.get_angle_arr()
	ang.append(app.get_angle())
	#print(ang)
	ax_h.clear()
	ax_h.hist(ang, bins = 100)


def sim_one():
	
	with open('sampleText.txt', 'a+') as file:
		file.seek(0, 0)
		ll = file.readlines()[-1]
		#print(ll)
		i = int((ll.split(',')[0]))+1
		text = str(i) + ","+ str(randint(0,40))+ "\n"
		addData = file.write(text)

def flux_text(i, txt):
	
	#Flux text
	a_txt = f2.add_subplot(gs[0,-1])
	a_txt.axis('off')
	a_txt.text(0.7,1, "QNet", horizontalalignment='right',
			verticalalignment='top', fontsize = 60,
			transform=a_txt.transAxes)
	a_txt.text(0.7,0.5, txt, horizontalalignment='right',
			verticalalignment='top', fontsize = 40,
			transform=a_txt.transAxes)	

class Detect(tk.Tk):

	def __init__(self, *args, **kwargs):

        
		tk.Tk.__init__(self, *args, **kwargs)

		#tk.Tk.iconbitmap(self, default="clienticon.xbm")
		tk.Tk.wm_title(self, "Cosmic Shower")
		
		w, h = tk.Tk.winfo_screenwidth(self), tk.Tk.winfo_screenwidth(self)
		tk.Tk.geometry(self,"%dx%d+0+0" % (w, h))

		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand = True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		
		frame = Page(container, self)
		self.frame = frame
		frame.grid(row=0, column=0, sticky="nsew")
		frame.tkraise()
		
		fig = frame.get_fig()
		self.fig = fig
		
		self.angle = 0
		self.angle_arr = []

	def set_angle(self, angle):
		self.angle = angle

	def get_angle(self):
		return self.angle

	def set_angle_arr(self, angle_arr):
		self.angle_arr = angle_arr
	
	def get_angle_arr(self):
		return self.angle_arr

	def get_fig(self):
		return self.fig



class Page(tk.Frame):
	

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		LARGE_FONT= ("Verdana", 20)
		label = tk.Label(self, text="QNet", font=LARGE_FONT)
		label.pack(pady=10,padx=10)	

		vec_t = [0,0.02,0.9]
		vec_d = [0,1,1,1]
		txt = str(999.66)	

		f2 = plt.figure()
		self.f2 = f2
		canvas = FigureCanvasTkAgg(f2, self)
		canvas.show()	
		canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


		
		toolbar = NavigationToolbar2TkAgg(canvas, self)
		toolbar.update()
		canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		
	def get_fig(self):
		return self.f2



vec_t = [0, 0.03, 0.98]
vec_d = [ 1, 1, 0 , 1]
txt = str(901.8)

app = Detect()
f2 = app.get_fig()
gs = gridspec.GridSpec(3,3)
ani = animation.FuncAnimation(f2, animate, interval=1000)
ani3 = animation.FuncAnimation(f2, ani_shower, fargs = [vec_t, vec_d], interval=50)
ani4 = animation.FuncAnimation(f2, flux_text, fargs = [txt], interval=1000)
ani2 = animation.FuncAnimation(f2, animate_his, interval=1000)

app.mainloop()



