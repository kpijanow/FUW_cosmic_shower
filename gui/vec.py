import matplotlib as mpl
import math
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
from matplotlib.collections import PolyCollection
from mpl_toolkits.mplot3d import proj3d
import random
from matplotlib._png import read_png
from matplotlib.cbook import get_sample_data


class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)



#ustawic autostart
#ustawić auto-size okna 
def det_plot(recentShowerVector, recentShowerDetectors, ax):

	ax.clear()
	VecE = recentShowerVector  #expects [x,y,z]
	shDet = recentShowerDetectors #expects array [0,1,1,1]
	#mpl.rcParams['legend.fontsize'] = 10

	VecS = [0,0,0] 
	VecV = [0,0,1]

	#VecE = [0.02, 0.1, 0.9] #from vector
	#shDet = [0, 1, 0, 1]

	
	#ax = fig.gca(projection='3d', facecolor='gray')
	a = Arrow3D(xs=[VecS[0], VecE[0]], ys =[VecS[1],VecE[1]],
					zs=[VecS[2],VecE[2]], mutation_scale=20, 
		            lw=3, arrowstyle="-|>", color="r")
	ax.add_artist(a)

	b = Arrow3D(xs=[VecS[0], VecV[0]], ys =[VecS[1],VecV[1]],
	 				zs=[VecS[2],VecV[2]], mutation_scale=20, 
		            lw=3, arrowstyle="-|>", color="b")
	#ax.add_artist(b)
	x = 0.05
	z = -0.4
	vectors = [[x,x,z], [x,-x,z], [-x,x,z], [-x,-x,z], [x,x,-z], [x,-x,-z], [-x,x,-z], [-x,-x,-z],
	[x/2,x/2,0], [x/2,-x/2,0], [-x/2,x/2,0], [-x/2,-x/2,0]]

	for v in vectors:
		dec_a = Arrow3D(xs=[v[0], v[0]+VecE[0]/2], ys =[v[1],v[1]+VecE[1]/2],
					zs=[v[2],v[2]+VecE[2]/2], mutation_scale=20, 
		            lw=2, arrowstyle="-|>", color="pink")

		ax.add_artist(dec_a)	

	
	r1 = [-0.15, -0.05]
	r = [0.05, 0.15]
	X1, Y1 = np.meshgrid(r1, r1)	
	X2, Y2 = np.meshgrid(r, r)	
	X3, Y3 = np.meshgrid(r1, r)
	X4, Y4 = np.meshgrid(r, r1)

	X = [X1,X2,X3,X4]
	Y = [Y1,Y2,Y3,Y4]

	for i in range(0,4):
		if shDet[i]==1:
			col = "lime"
		else:
			col = 'g'
		ax.plot_surface(X[i],Y[i],-0.4, color = col)
	

	vec1 = VecV
	vec2 = VecE

	angle=np.arccos(np.dot(vec1,vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2)))
	#print(angle)

	ax.set_zlim((1, -0.5))

	return ax, angle



