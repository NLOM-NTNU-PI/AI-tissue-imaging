# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 08:43:11 2021
Various functions that can be used to extract computation from images
@author: Magnus Lilledahl
"""
import numpy as np

#Function computes the difference in grey levels to neighbours at different distances from a pxiel and 
#returns a hyperspectral image with the differences at different distances.
#Must 
def neighbour_diff(img,levels,isotropic=False):
    #check if ndarray
    if not(isinstance(img,np.ndarray)):
        pass
        #throw exeption
    
    #check image is NxNx1
    if (len(img.shape) != 2):
        pass
        #throw exception

    #compute num_features.
    if isotropic:
        num_features = levels
    else:
        num_features = num_neighbours(levels) + 1 #depends on levels
    #initalize data array
    data = np.zeros(list(img.shape) + [num_features]) #array to hold data
    data[:,:,0] = img 

    #Compute data
    for x,y in np.ndindex(img.shape):
        first = levels
        last = img.shape[1]-levels
        if x >= first and x <= last and y >= first and y <= last: #This could be improved...
            coord = (x,y)        
            pos = 0
            for level in range(1,levels+1):
                dI = []
                ncoords = neighbour(x, y, level)
                for ncoord in ncoords:
                    dI.append(img[coord]-img[tuple(ncoord)])
                if isotropic:
                    dI = [sum(dI)]
                data[x,y,pos+1:pos+len(dI)+1] = dI           
                pos = pos + len(dI)
    data = data[levels:-levels,levels:-levels,:] #remove padding
    return data

#Returns coordinates of neighbours at certain distances
#...can this not be hard-coded?...
def neighbour(x,y,level):
    if level>3:
        raise ValueError("levels above 3 not yet implemented")
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