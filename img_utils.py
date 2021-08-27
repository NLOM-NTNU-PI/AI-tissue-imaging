# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 08:43:11 2021

@author: lilledah
"""
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