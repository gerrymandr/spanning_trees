# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 04:41:10 2018

@author: Temporary
"""

import numpy as np
import networkx as nx

graph = nx.grid_graph([40,40])

def mst(graph):
    make_edge_weights(graph)
    return nx.minimum_spanning_tree(graph)

def make_edge_weights(graph):
    values = np.random.uniform(0,1,len(graph.edges()))
    i = 0
    for edge in graph.edges():
        graph.edges[edge]["weight"] = values[i]
        i += 1
        
mst_trees = []
uniform_trees = []
for i in range(10):
    mst_trees.append(mst(graph))
    uniform_trees.append(random_spanning_tree_wilson(graph))
    

