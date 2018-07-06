# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 11:43:31 2018

@author: MGGG
"""

#####For creating a spanning tree
import networkx as nx
import random
def srw(G,a):
    '''takes'''
    wet = set([a])
    trip = [a]
    while len(wet) < len(G.nodes()):
        b = random.choice(list(G.neighbors(a)))
        wet.add(b)
        trip.append(b)
        a = b
    return trip

def forward_tree(G,a):
    walk = srw(G,a)
    edges = []
    for x in G.nodes():
        if (x != walk[0]):
            t = walk.index(x)
            edges.append( [walk[t], walk[t-1]])
    return edges

def random_spanning_tree(graph):
    #It's going to be faster to use the David Wilson algorithm here instead.
    tree_edges = forward_tree(graph, random.choice(list(graph.nodes())))
    tree = nx.DiGraph()
    tree.add_nodes_from(list(graph.nodes()))
    tree.add_edges_from(tree_edges)
    return tree

def random_spanning_tree_wilson(G):
    #The David Wilson random spanning tree algorithm
    
    return T