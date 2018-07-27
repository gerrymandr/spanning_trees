# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 00:19:54 2018

@author: MGGG
"""

from tree_tools import log_number_trees
import numpy as np
from scipy.spatial import Delaunay
import networkx as nx



def split(points, triangle):
    #takes a triangle and returns the edges in it
    return [ [tuple(points[triangle[j]]), tuple(points[triangle[(j + 1) % 3]])] for j in [0,1,2]]

def delaunay_to_edge_list(points, triangles):
    edges = []
    for triangle in triangles.simplices:

        edges += split(points, triangle)
    return edges

    import matplotlib.pyplot as plt
    plt.triplot(points[:,0], points[:,1], triangles.simplices.copy())
    plt.plot(points[:,0], points[:,1], 'o')
    plt.show()
    
def points_to_delaunay_graph(points):
    triangles = Delaunay(points)
    edge_list = delaunay_to_edge_list(points, triangles)
    G = nx.Graph()
    G.add_edges_from(edge_list)
    return G

def viz(graph):
    for vertex in graph.nodes():
            graph.nodes[vertex]["pos"] = vertex

    nx.draw(graph, pos=nx.get_node_attributes(graph, 'pos'), node_size = 20, width = .5)

def make_rectangle(number_samples, skew):
    return list(zip(np.random.uniform(0,1,number_samples), np.random.uniform(0,skew,number_samples)))


#repititions = 20
#for number_samples in [100,1000,10000,50000]:
#    square_trees = []
#    rectangle_trees = []
#    for i in range(repititions):
#        sample_square = make_rectangle(number_samples, 1)
#        sample_rectangle = make_rectangle(number_samples,200)
#        
#        rectangle_graph = points_to_delaunay_graph(sample_rectangle)
#        square_graph = points_to_delaunay_graph(sample_square)
#        #viz(square_graph)
#        #viz(rectangle_graph)
#        rectangle_trees.append(log_number_trees(rectangle_graph))
#        square_trees.append(log_number_trees(square_graph))
#    print(np.mean(rectangle_trees), np.std(rectangle_trees))
#    print(np.mean(square_trees), np.std(square_trees))
#    print("difference:", np.mean(rectangle_trees) - np.mean(square_trees), "total std:", np.std(rectangle_trees) + np.std(square_trees))
    
square_data = {}
repititions = 20
sample_size_set = [100,1000,10000]
for number_samples in sample_size_set:
    square_trees = []
    rectangle_trees = []
    for i in range(repititions):
        sample_rectangle = make_rectangle(number_samples,1)           
        rectangle_graph = points_to_delaunay_graph(sample_rectangle)
        rectangle_trees.append(log_number_trees(rectangle_graph))
    square_data[number_samples] =  [ [np.mean(rectangle_trees), np.std(rectangle_trees)] ] 

data = {}
repititions = 20
sample_size_set = [100,1000,10000]
skew_size_set = [10,100]
for skews in skew_size_set:
    data[skews] = {}
    for number_samples in sample_size_set:
        square_trees = []
        rectangle_trees = []
        for i in range(repititions):
            sample_rectangle = make_rectangle(number_samples,skews)           
            rectangle_graph = points_to_delaunay_graph(sample_rectangle)
            rectangle_trees.append(log_number_trees(rectangle_graph))
        data[skews][number_samples] = [ [ np.mean(rectangle_trees), np.std(rectangle_trees)] ] 
        

        
        
#Maybe you should use the geometric laplacian instead. idk. It's disconcerning how long it takes 
        #to tell the difference... on the other hand... this essentially is because we are looking for a second order effect, so in order to tell the difference we have to stretch it a lot.
        
        #What shold we compare -- do  [ log(T for rectangle) -  log(T for square)]