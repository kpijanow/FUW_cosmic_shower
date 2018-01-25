import matplotlib
matplotlib.use("TkAgg")
from matplotlib import gridspec

from matplotlib.figure import Figure
import matplotlib.animation as animation

import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

import numpy as np
from random import randint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


from vec import det_plot



def animate(i, tableOfFluxInEveryMinute, a):

	xar=[]	
	for x in range(0,60):
                xar.append(x+i) 
	
	a.clear()
	a.plot(xar, tableOfFluxInEveryMinute)


def ani_shower(i, vec_t, vec_d, a_sh):	
	
	#a_sh = f2.add_subplot(gs[1:,:-1], projection='3d')
	a_sh.clear()
	print(vec_t)
	rot = det_plot(vec_t,vec_d, a_sh)
	rot.view_init(elev = 30, azim = i%360)

def animate_his(i, recentZenithHisto, ax_h):

	#ax_h = f2.add_subplot(gs[-1, -1])
	#ang = app.get_angle_arr()
	#ang.append(app.get_angle())
	#print(ang)
	ax_h.clear()
	ind = np.arange(len(recentZenithHisto))
	ax_h.bar(ind, recentZenithHisto, color='orange')

def sim_one():
	
	with open('sampleText.txt', 'a+') as file:
		file.seek(0, 0)
		ll = file.readlines()[-1]
		#print(ll)
		i = int((ll.split(',')[0]))+1
		text = str(i) + ","+ str(randint(0,40))+ "\n"
		addData = file.write(text)

def flux_text(i, txt, a_txt):
	
	#Flux text
        #gs = gridspec.GridSpec(3,3)
        #a_txt = f2.add_subplot(gs[0,-1])
        a_txt.axis('off')
        a_txt.text(0.7,1, "QNet", horizontalalignment='right',
        verticalalignment='top', fontsize = 60,
        transform=a_txt.transAxes)
        a_txt.text(0.7,0.5, txt, horizontalalignment='right',
        verticalalignment='top', fontsize = 40,
        transform=a_txt.transAxes)
        

class Holder():
        def __init__(self):
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


app = Holder()

'''
vec_t = [0, 0.03, 0.98]
vec_d = [ 1, 1, 0 , 1]
txt = str(901.8)

app = Holder()
#app = Detect()
f2 = plt.figure()
#app.get_fig()
gs = gridspec.GridSpec(3,3)
ani = animation.FuncAnimation(f2, animate, interval=1000)
ani3 = animation.FuncAnimation(f2, ani_shower, fargs = [vec_t, vec_d], interval=50)
ani4 = animation.FuncAnimation(f2, flux_text, fargs = [txt], interval=1000)
ani2 = animation.FuncAnimation(f2, animate_his, interval=1000)
plt.show()
#app.mainloop()
'''


