# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 11:43:31 2018

@author: MGGG
"""

#####For creating a spanning tree
import networkx as nx
import random
from equi_partition_tools import equi_split
from projection_tools import remove_edges_map
def simple_random_walk(graph,node):
    '''takes'''
    wet = set([node])
    trip = [node]
    while len(wet) < len(graph.nodes()):
        next_step = random.choice(list(graph.neighbors(node)))
        wet.add(next_step)
        trip.append(next_step)
        node = next_step
    return trip

def forward_tree(graph,node):
    walk = simple_random_walk(graph, node)
    edges = []
    for vertex in graph.nodes():
        if (vertex != walk[0]):
            first_occurance = walk.index(vertex)
            edges.append( [walk[first_occurance], walk[first_occurance-1]])
    return edges

def random_spanning_tree(graph):
    #It's going to be faster to use the David Wilson algorithm here instead.
    tree_edges = forward_tree(graph, random.choice(list(graph.nodes())))
    tree = nx.DiGraph()
    tree.add_nodes_from(list(graph.nodes()))
    tree.add_edges_from(tree_edges)
    return tree

def random_spanning_tree_wilson(graph):
    #The David Wilson random spanning tree algorithm
    tree = 0
    return tree

def random_equi_partitions(graph, num_partitions, num_blocks):
    found_partitions = []
    counter = 0
    while len(found_partitions) < num_partitions:
        counter += 1
        tree = random_spanning_tree(graph)
        edge_list = equi_split(tree, num_blocks)
        if edge_list != None:
            found_partitions.append( remove_edges_map(graph, tree, edge_list))
            print(len(found_partitions), "waiting time:", counter)
            counter = 0
    return found_partitions