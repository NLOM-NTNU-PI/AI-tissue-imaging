# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 13:51:15 2021

This program loads an image, extracts features/data and performs a KMeans
clustering of the data to identify specific structures in the image. The data
features are based on differences in intensity between neighbours at different
separations

@author: lilledah
"""

from skimage import io
from skimage.transform import resize

from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
import numpy as np

import tkinter as tk

import img_utils as utils

#Parameters
img_shape = [100,100] #resample image to this shape
maxlevel = 2 #separation perhaps better name.
isotropic = 0 #if 1 sum all intensity differences at specific level
if isotropic:
    num_features = maxlevel
else:
    num_features = utils.num_neighbours(maxlevel) + 1 #depends on levels
num_clusters = 2 #Clusters

#Import
#fname = 'chordae.jpg'
fname = 'cartilage_surface.jpg'
img = io.imread(fname)

#Preprocess
img = img[:,:,0] #Select channel 
img = resize(img,img_shape) ##resize

data = np.zeros(img_shape + [num_features]) #array to hold data
data[:,:,0] = img

#Compute delta I for neighbours
for x,y in np.ndindex(img.shape):
    first = maxlevel
    last = img.shape[1]-maxlevel
    if x >= first and x <= last and y >= first and y <= last:
        coord = (x,y)        
        pos = 0
        for level in range(1,maxlevel+1):
            dI = []
            ncoords = utils.neighbour(x, y, level)
            for ncoord in ncoords:
                dI.append(img[coord]-img[tuple(ncoord)])
            if isotropic:
                dI = [sum(dI)]
            data[x,y,pos+1:pos+len(dI)+1] = dI           
            pos = pos + len(dI)

img_dp = img[maxlevel:-maxlevel,maxlevel:-maxlevel] #remove padding
data = data[maxlevel:-maxlevel,maxlevel:-maxlevel,:] #remove padding
data_flat = data.reshape((data.shape[0]*data.shape[1],data.shape[2])) #flatten

#Perform K-means clustering
km = KMeans(n_clusters=num_clusters)
km.fit(data_flat)
labels = km.labels_.reshape(data.shape[0],data.shape[1]) #reshape to image

#Visualization
fig = plt.figure()

ax = fig.add_subplot(121)
ax.imshow(img_dp)
ax.set_title('Original')
ax.set_axis_off()
ax = fig.add_subplot(122)
ax.imshow(labels)
ax.set_title('Clusters')
ax.set_axis_off()
fig.text(.05,.05,"{:d} clusters".format(num_clusters)\
         + "\n{:d} levels".format(maxlevel)\
         + "\nIsotropic: {!r}".format(bool(isotropic))\
         + "\n{:d} Pixels".format(img_shape[0])
         + "\nFile: " + fname)

run_fname = "clusters_" + "l" + str(maxlevel) + "_c" + str(num_clusters) + "_i" + str(isotropic)
plt.savefig("experiments/run1/" + run_fname)

#Set position of window on screen
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
mngr = plt.get_current_fig_manager() #FigureManagerQT which inherits from QWidget
geom = mngr.window.geometry()
x,y,dx,dy = geom.getRect()
mngr.window.setGeometry(200,200,dx,dy)
