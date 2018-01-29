import matplotlib.animation as animation
from matplotlib import gridspec
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

import numpy as np
from random import randint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from vec import det_plot


def animate(i, q_min, a, a_txt, ax_h):
        print("IN ANIMATE")
        xar=[]
        tableOfFluxInEveryMinute=q_min.get()
        for x in range(0,60):
                xar.append(x+i)

        a.clear()
        print(tableOfFluxInEveryMinute)
        a.plot(xar, tableOfFluxInEveryMinute)
        txt=round(q_min.get(),4)
        a_txt.clear()
        a_txt.axis('off')
        a_txt.text(0.7,1, "QNet", horizontalalignment='right',
        verticalalignment='top', fontsize = 60,
        transform=a_txt.transAxes)
        a_txt.text(0.7,0.5, txt, horizontalalignment='right',
        verticalalignment='top', fontsize = 40,
        transform=a_txt.transAxes)
        recentZenithHisto=q_min.get()
        ax_h.clear()
        ind = np.arange(len(recentZenithHisto))
        ax_h.bar(ind, recentZenithHisto, color='orange')
        print("OUT ANIMATE")

def ani_shower(i, vec_t, vec_d, a_sh):	
	
        a_sh.clear()	
        print(vec_t)
        rot = det_plot(vec_t,vec_d, a_sh)
        rot.view_init(elev = 30, azim = i%360)

def animate_his(i, recentZenithHisto, ax_h):

	ax_h.clear()
	ind = np.arange(len(recentZenithHisto))
	ax_h.bar(ind, recentZenithHisto, color='orange')


def flux_text(i, in_q, a_txt):
	
        txt=round(in_q.get(),4)
        a_txt.clear()
        a_txt.axis('off')
        a_txt.text(0.7,1, "QNet", horizontalalignment='right',
        verticalalignment='top', fontsize = 60,
        transform=a_txt.transAxes)
        a_txt.text(0.7,0.5, txt, horizontalalignment='right',
        verticalalignment='top', fontsize = 40,
        transform=a_txt.transAxes)
        
