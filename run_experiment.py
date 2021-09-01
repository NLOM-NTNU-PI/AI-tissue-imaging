#Script which runs an experiment, that is, an analysis og data using a set of parameters.
#Data are stored in a run<#>-folder (an experiment) together with the results 
#Load data to analyse (should be stored in run folder - to ensure data is constant)

testing = True #Set false to run an experiment where data is to be stored.

#LIBRARIES
from skimage import io
from skimage.transform import resize
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import img_utils as utils

#DATA
#fname = 'chordae.jpg'
fname = 'cartilage_surface.jpg' #data that are used in the analysis should be stored with analysis data
img = io.imread(fname)

#PARAMETERS
#Set experiment parameters
if testing: #testing parameters
    img_shape = [200,200] #resample image to this shape
    levels = 5 #separation perhaps better name.
    isotropic = False #if 1 sum all intensity differences at specific level
    num_clusters = 4
else: #run parameters
    pass

#PREPROCESSING (select subset, ...)
img = img[:,:,0] #Select channel 
img = resize(img,img_shape) #resample 

#ANALYSIS
data = utils.neighbour_diff(img, levels, isotropic=isotropic, method='circle')
data_flat = data.reshape((data.shape[0]*data.shape[1],data.shape[2])) #flatten
km = KMeans(n_clusters=num_clusters) #Perform K-means clustering
km.fit(data_flat)
labels = km.labels_.reshape(data.shape[0],data.shape[1]) #reshape to image

#RESULTS
#Results
if testing: #Show results
    pass
    #Visualization
    fig = plt.figure()
    ax = fig.add_subplot(121)
    ax.imshow(data[:,:,0])
    ax.set_title('Original')
    ax.set_axis_off()
    ax = fig.add_subplot(122)
    ax.imshow(labels)
    ax.set_title('Clusters')
    ax.set_axis_off()
    fig.text(.05,.05,"{:d} clusters".format(num_clusters)\
            + "\n{:d} levels".format(levels)\
            + "\nIsotropic: {!r}".format(bool(isotropic))\
            + "\n{:d} Pixels".format(img_shape[0])
            + "\nFile: " + fname)
    run_fname = "clusters_" + "l" + str(levels) + "_c" + str(num_clusters) + "_i" + str(isotropic)
    plt.show()
    #plt.savefig("experiments/run1/" + run_fname)

else: #Store results
    #Store commit hash of current code in readme file together with repository
    #Place original data files together with the results
    #e.g. numpy.save
    pass