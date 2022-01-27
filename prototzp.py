import scipy
from matplotlib import cm
import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from stl import mesh



# # Load the STL files and add the vectors to the plot

# your_mesh = mesh.Mesh.from_file('beispiellinse.stl')
#
#
# zindex = np.random.randint(0,your_mesh.points.shape[0]-1,size=10) #using zindex to select the sampling data,the size is used to set the amount of sampling
# data = your_mesh[zindex][:,0:3] #select the first vertikel point ,format :x,y,z
#
# # create a 2D-mesh
# x = data[:,0]
# y = data[:,1]
# mn = np.min(data, axis=0)
# mx = np.max(data, axis=0)
# X, Y = np.meshgrid(np.linspace(mn[0], mx[0], 20), np.linspace(mn[1], mx[1], 20)) #the num of mesh point can set here
# XX = X.flatten()
# YY = Y.flatten()
#
# A = np.c_[np.ones(data.shape[0]), data[:, :2], np.prod(data[:, :2], axis=1), data[:, :2] ** 2]
# C, _, _, _ = scipy.linalg.lstsq(A, data[:, 2]) #parameters of the module
#
# # evaluate it on a grid
# Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX * YY, XX ** 2, YY ** 2], C).reshape(X.shape) #get the height infomation
# fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
#
# # surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, # Plot the surface.
#
# ax.scatter3D(XX, YY, Z, c=Z, cmap='Greens')
# plt.show()


#the second method using the average popints of the meshing triangle.
your_mesh = mesh.Mesh.from_file('beispiellinse.stl')
dmin = 200
print(your_mesh.points.shape)
centerofmeshtriangle_x = (your_mesh.points[:,0]+your_mesh.points[:,3]+your_mesh.points[:,6])/3
centerofmeshtriangle_y = (your_mesh.points[:,1]+your_mesh.points[:,4]+your_mesh.points[:,7])/3
centerofmeshtriangle_z = (your_mesh.points[:,2]+your_mesh.points[:,5]+your_mesh.points[:,8])/3
print(centerofmeshtriangle_x.shape)


x_range = np.concatenate([your_mesh.points[:,0],your_mesh.points[:,3],your_mesh.points[:,6]])
xmin = np.min(x_range)
xmax = np.max(x_range)

y_range = np.concatenate([your_mesh.points[:,1],your_mesh.points[:,4],your_mesh.points[:,7]])
ymin = np.min(y_range)
ymax = np.max(y_range)

print(xmin,xmax)
print(ymin,ymax)

dx = 5
dy = 5
def finddindex(a, b, meshcenter):

    for xid in range(len(meshcenter[0])):
        if(np.abs((meshcenter[0,xid] - a))<=0.3 and np.abs((meshcenter[1,xid] - b))<=0.2):
            return xid
    return

xline = np.arange(xmin,xmax,dx)
yline = np.arange(ymin,ymax,dy)

meshc = np.stack((centerofmeshtriangle_x,centerofmeshtriangle_y,centerofmeshtriangle_z))
Z = np.ones((len(xline),len(yline)))
xx,yy = np.meshgrid(xline,yline)
for xi in range(len(xline)):
    for yi in range(len(yline)):
        if (finddindex(xline[xi],yline[yi],meshc)!=None):
            Z[xi,yi] = meshc[2,finddindex(xline[xi],yline[yi],meshc)]


print(Z)
fig = plt.figure()
ax = plt.axes(projection='3d')

ax.scatter3D(xx, yy, Z, c=Z, cmap='Greens');
plt.show()