# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 20:14:13 2018

@author: Temporary
"""

#This samples from rank B elements from a partition matroid with constraints d_i.
#Said more simply, we want to sample a total of B balls from I urns, subject to the contraint that we take no more than b_i balls from urn i.
#https://stats.stackexchange.com/questions/184348/how-to-generate-samples-uniformly-at-random-from-multiple-discrete-variables-sub

#We first dynamically compute $P( n_I | B, b_{1:I})$.


#For a given tree, and given subforest of acceptable nodes, we should as much of this data as possible. Don't prematurely optimie though.



