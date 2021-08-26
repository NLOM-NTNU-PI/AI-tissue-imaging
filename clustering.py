# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 13:51:15 2021

@author: lilledah
"""

#Creating a dataset for clustering an image

from skimage import io
from skimage.transform import resize

from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
import numpy as np

import tkinter as tk

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#Import data
#fname = 'chordae.jpg'
fname = 'cartilage surface 4.jpg'
img = io.imread(fname)

#Preprocess data
##Select channel
img = img[:,:,0]
##resize
shape = [100,100]
img = resize(img,shape)

#Parameters
maxlevel = 3
data_dim = shape #...seems unnecessary...
#Allocate array for features
data_dim.append(9) #depends on levels
data = np.zeros(data_dim)

x = 1
y = 1
d = 1

#Returns coordinates of neighbours at certain distances
#...can this not be hard-coded?...
def neighbour(x,y,level):
    if level == 1:
        coords = [[x-1,y],[x+1,y],[x,y-1],[x,y+1]]
    elif level == 2:
        coords = [[x-1,y-1],[x-1,y+1],[x+1,y-1],[x+1,y+1]]
    elif level == 3:
        coords = [[x-2,y],[x+2,y],[x,y-2],[x,y+2]]
        # etc..
    return coords    

#Calculates the total number of neighbours up to a certain level. 
#Can be used to preassign size of arrays.
def num_neighbours(level):
    num = 0
    for i in range(1,level+1):
        num = num + len(neighbour(0,0,i))
    return num

#Compute delta I for nearest neighbours
isotropic = 1
for x,y in np.ndindex(img.shape):
    first = maxlevel
    last = img.shape[1]-maxlevel
    if x >= first and x <= last and y >= first and y <= last:
        coord = (x,y)
        #img[coord]
       
        #dI.append(img[coord] - img[x-d,y])
        #dI.append(img[coord] - img[x+d,y])
        #dI.append(img[coord] - img[x,y-d])
        #dI.append(img[coord] - img[x,y+d])
        pos = 0
        for level in range(1,maxlevel+1):
            dI = []
            ncoords = neighbour(x, y, level)
            for ncoord in ncoords:
                dI.append(img[coord]-img[tuple(ncoord)])
            if isotropic:
                dI = [sum(dI)]
            data[x,y,pos+1:pos+len(dI)+1] = dI           
            pos = pos + len(dI)
data[:,:,0] = img

#remove edgesd
data = data[1:-1,1:-1,0:2]

dim = data.shape

#flatten
data_array = data.reshape((data.shape[0]*data.shape[1],data.shape[2]))

#Cluster
num_clusters = 2
km = KMeans(n_clusters=num_clusters)
km.fit(data_array)

labels = km.labels_

labels = labels.reshape(dim[0],dim[1])

fig = plt.figure('clusters')


ax = fig.add_subplot(121)
ax.imshow(img)
ax = fig.add_subplot(122)
ax.imshow(labels)

#Set position of window on screen
mngr = plt.get_current_fig_manager() #FigureManagerQT which inherits from QWidget
geom = mngr.window.geometry()
x,y,dx,dy = geom.getRect()
mngr.window.setGeometry(1500,100,dx,dy)
