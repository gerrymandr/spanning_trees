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

##############
    
'''Wilsons Algorithm'''

def random_spanning_tree_wilson(graph):
    #The David Wilson random spanning tree algorithm
    tree_edges = []
    hitting_set = set ( [ random.choice(list(graph.nodes()))])
    while len(hitting_set) < len(graph):
        start_node = random.choice([ v for v in graph.nodes() if v not in hitting_set])
        trip = random_walk_until_hit(graph, start_node, hitting_set)
        new_branch = loop_erasure(trip)
        for i in range(len(new_branch) - 1):
            tree_edges.append( [ new_branch[i], new_branch[i + 1]])
        for v in trip:
            hitting_set.add(v)
    tree = nx.DiGraph()
    tree.add_edges_from(tree_edges)
    return tree

def random_walk_until_hit(graph, start_node, hitting_set):
    '''Does a random walk from start_node until it hits the hitting_set
    '''
    
    current_node = start_node
    trip = [current_node]
    while current_node not in hitting_set:
        current_node = random.choice(list(graph.neighbors(current_node)))
        trip.append(current_node)
    return trip

def loop_erasure(trip):
    '''erases loops from a trip
    
    :trip: input of node names...
    
    TODO: What's the right way to get the last element...
    '''
    n = len(trip)
    loop_erased_walk_indices = []
    last_occurance = n - trip[::-1].index(trip[0]) - 1
    loop_erased_walk_indices.append(last_occurance)
        
    while trip[loop_erased_walk_indices[-1]] != trip[-1]:
        last_occurance = n -  trip[::-1].index(trip[loop_erased_walk_indices[-1]])  -1
        loop_erased_walk_indices.append(last_occurance + 1)
        
    loop_erased_trip = [trip[i] for i in loop_erased_walk_indices]
    
    return loop_erased_trip
    

#################3

def random_equi_partitions(graph, num_partitions, num_blocks, algorithm = "Wilson"):
    found_partitions = []
    counter = 0
    while len(found_partitions) < num_partitions:
        counter += 1
        if algorithm == "Broder":
            tree = random_spanning_tree(graph)
        if algorithm == "Wilson":
            tree = random_spanning_tree(graph)
        edge_list = equi_split(tree, num_blocks)
        if edge_list != None:
            found_partitions.append( remove_edges_map(graph, tree, edge_list))
            print(len(found_partitions), "waiting time:", counter)
            counter = 0
    return found_partitions