#import matplotlib as mpl
import math
#from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
import constants 

from matplotlib import gridspec


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
 
def det_plot(recentShowerVector, recentShowerDetectors, ax):

	ax.clear()
	VecIn= [[0,0,recentShowerVector[0]], [0,0,recentShowerVector[1]], 
		[0,0,recentShowerVector[2]], [0,0,recentShowerVector[3]]]  #expects 4x[x,y,z] so input is [t1[0], t1[1], t1[2], t1[3]]
	shDet = recentShowerDetectors #expects array [0,1,1,1]

	const = constants.Constants()

	#vectors = [[0.5,0, 0], [3.5,0,0], [5.5,0,0], [9.5,0,0]]
	vectors = [[const.det_X[0],0, 0], [const.det_X[1],0,0], [const.det_X[2],0,0], [const.det_X[3],0,0]]

	i=0

	for v in vectors:
		if shDet[i]==0:
			VecIn[i] = v
			#print("shDet = " + str(shDet[i]) + " v = " + str(v) + " VecE = " + str(VecE) + " i = " + str(i) + " len vector)
		else:
			VecE=VecIn[i]
			#print("shDet = " + str(shDet[i]) + " v = " + str(v) + " VecE = " + str(VecE) + " i = " + str(i))
			dec_a = Arrow3D(xs=[v[0], v[0]+VecE[0]/2], ys =[v[1],v[1]+VecE[1]/2],
					zs=[v[2],v[2]+VecE[2]/2 + 0.2], mutation_scale=20, #+0.2 if time is 0 than still something is drawn
		            lw=5, arrowstyle="-", color="r")

			ax.add_artist(dec_a)
		i=i+1	

	r = [0.25,-0.25]
	w = 0.5
	ax.set_xlim([-1,10])
	ax.set_ylim([-1.5, 1.5])
	ax.set_zlim3d(-5, 50) #-0.20, 1.2)	

	X1, Y1 = np.meshgrid([vectors[0][0] - w,vectors[0][0] + w], r)	#for position of the detector to match
	X2, Y2 = np.meshgrid([vectors[1][0] - w,vectors[1][0] + w], r)	#detectors fired
	X3, Y3 = np.meshgrid([vectors[2][0] - w,vectors[2][0] + w], r)
	X4, Y4 = np.meshgrid([vectors[3][0] - w,vectors[3][0] + w], r)

	X = [X1,X2,X3,X4]
	Y = [Y1,Y2,Y3,Y4]

	h = 0
	z, Z0 = np.meshgrid(h, h)
	Z =[z,z,z,z]
##	print("variable")

	for i in range(0,4):
		if shDet[i]==1:
			col = "lime"
		else:
			col = 'g'
		ax.plot_surface(X[i],Y[i],Z[i], color = col)

	return ax

'''
f2 = plt.figure()
gs = gridspec.GridSpec(3,3)
a = f2.add_subplot(gs[0,:-1])
a_txt = f2.add_subplot(gs[0,-1])
ax = f2.add_subplot(gs[1:,:-1], projection='3d')
ax_h = f2.add_subplot(gs[-1, -1])
det_plot([[0.1,-0.2,0.7],[0.1,-0.2,0.6],[-0.1,0.2,0.9],[0.01,0.4,0.9]],[0,1,0,1], ax)
plt.show()
'''
