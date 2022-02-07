import scipy
from matplotlib import cm
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import shutil
import xml.etree.cElementTree as et
import zipfile
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


# the second method using the average popints of the meshing triangle.

# this is the process tp read stl file
def readstlfile():
    your_mesh = mesh.Mesh.from_file('beispiellinse.stl')

    print(your_mesh.points.shape)
    # centerofmeshtriangle_x = (your_mesh.points[:, 0] + your_mesh.points[:, 3] + your_mesh.points[:, 6]) / 3
    # centerofmeshtriangle_y = (your_mesh.points[:, 1] + your_mesh.points[:, 4] + your_mesh.points[:, 7]) / 3
    # centerofmeshtriangle_z = (your_mesh.points[:, 2] + your_mesh.points[:, 5] + your_mesh.points[:, 8]) / 3
    # print(centerofmeshtriangle_x.shape)

    x_range = np.concatenate([your_mesh.points[:, 0], your_mesh.points[:, 3], your_mesh.points[:, 6]])
    y_range = np.concatenate([your_mesh.points[:, 1], your_mesh.points[:, 4], your_mesh.points[:, 7]])
    z_range = np.concatenate([your_mesh.points[:, 2], your_mesh.points[:, 5], your_mesh.points[:, 8]])
    return x_range, y_range, z_range


# this is process to extract the geometry information from 3mf file
def read3mfinfo():
    shutil.copy('beispiellinse.3mf', 'jg.zip')
    with zipfile.ZipFile("jg.zip", "r") as zip_ref:
        zip_ref.extractall()

    tree = et.parse('3D/3dmodel.model')
    root = tree.getroot()
    vertictes = []
    xgather = []
    ygather = []
    zgather = []
    for x in root[0][1][0][0]:
        vertictes.append(x.attrib)
        for key, value in x.items():
            if key == 'x':
                xgather.append(float(value))
            if key == 'y':
                ygather.append(float(value))
            if key == 'z':
                zgather.append(float(value))
    return np.array(xgather), np.array(ygather), np.array(zgather)

def finddindex(a, b, meshcenter):
    for xid in range(len(meshcenter[0])):
        if np.abs((meshcenter[0, xid] - a)) <= 0.3 and np.abs((meshcenter[1, xid] - b)) <= 0.3:
            return xid
    return


x_range = readstlfile()[0]
y_range = readstlfile()[1]
z_range = readstlfile()[2]

xmin = np.min(x_range)
xmax = np.max(x_range)

ymin = np.min(y_range)
ymax = np.max(y_range)

zmin = np.min(z_range)
zmax = np.max(z_range)

print(xmin, xmax)
print(ymin, ymax)
print(zmin, zmax)
print(type(x_range))

dx = 5
dy = 5

xline = np.arange(xmin, xmax, dx)
yline = np.arange(ymin, ymax, dy)

meshc = np.stack((x_range, y_range, z_range))

Z = np.ones((len(xline), len(yline)))
xx, yy = np.meshgrid(xline, yline)
for xi in range(len(xline)):
    for yi in range(len(yline)):
        if finddindex(xline[xi], yline[yi], meshc) is not None:
            Z[xi, yi] = meshc[2, finddindex(xline[xi], yline[yi], meshc)]

print(Z)
fig = plt.figure()
ax = plt.axes(projection='3d')

ax.scatter3D(xx, yy, Z, c=Z, cmap='Greens')
plt.show()

##the belowed code for showing the plot of original stl file
# from stl import mesh
# from mpl_toolkits import mplot3d
# from matplotlib import pyplot
#
# # Create a new plot
# figure = pyplot.figure()
# axes = mplot3d.Axes3D(figure)
#
# # Load the STL files and add the vectors to the plot
# your_mesh = mesh.Mesh.from_file('beispiellinse.stl')
# axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
#
# # Auto scale to the mesh size
# scale = your_mesh.points.flatten()
# axes.auto_scale_xyz(scale, scale, scale)
#
# # Show the plot to the screen
# pyplot.show()
