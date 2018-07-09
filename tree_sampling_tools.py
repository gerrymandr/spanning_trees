# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 11:43:31 2018

@author: MGGG
"""

#####For creating a spanning tree
import networkx as nx
import random
from equi_partition_tools import equi_split, almost_equi_split, check_delta_equi_split
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
    allowable_set = set(graph.nodes())
    len_graph = len(graph)
    len_hitting_set = 1
    while len_hitting_set < len_graph:
        #allowable_set = list(set(graph.nodes()).difference(hitting_set))
        #If we can handle the step of choosing the allowable set more 
        #efficiently, we can speed stuff up... this is the bottle neck
        start_node = random.choice(list(allowable_set))
        trip = random_walk_until_hit(graph, start_node, hitting_set)
        new_branch, branch_length = loop_erasure(trip)
        for i in range(branch_length - 1):
            tree_edges.append( [ new_branch[i], new_branch[i + 1]])
        for v in new_branch[:-1]:
            hitting_set.add(v)
            len_hitting_set += 1
            allowable_set.remove(v)
    tree = nx.DiGraph()
    tree.add_nodes_from(list(graph.nodes()))
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
    branch_length = 0
    while trip[loop_erased_walk_indices[-1]] != trip[-1]:
        last_occurance = n -  trip[::-1].index(trip[loop_erased_walk_indices[-1]])  -1
        loop_erased_walk_indices.append(last_occurance + 1)
        branch_length += 1
    loop_erased_trip = [trip[i] for i in loop_erased_walk_indices]
    
    return (loop_erased_trip, branch_length + 1)
    #I don't think that passing the length sped it up at all...

#################3
    


def random_equi_partitions(graph, num_partitions, num_blocks, algorithm = "Wilson"):
    found_partitions = []
    counter = 0
    while len(found_partitions) < num_partitions:
        counter += 1
        if algorithm == "Broder":
            tree = random_spanning_tree(graph)
        if algorithm == "Wilson":
            tree = random_spanning_tree_wilson(graph)
        edge_list = equi_split(tree, num_blocks)
        if edge_list != None:
            found_partitions.append( remove_edges_map(graph, tree, edge_list))
            print(len(found_partitions), "waiting time:", counter)
            counter = 0
    return found_partitions

#def random_equi_partition_fast(graph, log2_num_blocks):
#    found_partitions = []
#    if log2_num_blocks == 1:
#        found_partitions = random_equi_partitions(graph, 1, 2)[0]
#    if log2_num_blocks > 1: 
#        parts = random_equi_partitions(graph, 1, 2)[0]
#        for subgraph in parts:    
#            found_partitions += random_equi_partition_fast(subgraph, log2_num_blocks - 1)
#    
#    return found_partitions

def random_equi_partition_fast_nonrecursive(graph, log2_num_blocks):
    blocks = random_equi_partitions(graph, 1, 2)[0]
    while len(blocks) < 2**log2_num_blocks:
        subgraph_splits = []
        for subgraph in blocks:
            subgraph_splits += random_equi_partitions(subgraph, 1, 2)[0]
        blocks = subgraph_splits
    return blocks

def random_equi_partitions_fast(graph, num_partitions, log2_num_blocks):
    found_partitions = []
    while len(found_partitions) < num_partitions:
        found_partitions.append(random_equi_partition_fast_nonrecursive(graph, log2_num_blocks))
    return found_partitions


############ Almost equi-partitions:


def random_almost_equi_partitions(graph, num_partitions, num_blocks, delta):
    '''This produces a delta almost equi partition
    
    '''
    found_partitions = []
    counter = 0
    while len(found_partitions) < num_partitions:
        counter += 1
        tree = random_spanning_tree_wilson(graph)
        edge_list = almost_equi_split(tree, num_blocks)   
        blocks = remove_edges_map(graph, tree, edge_list)
        if check_delta_equi_split([len(x) for x in blocks], delta):
            found_partitions.append( blocks)
            print(len(found_partitions), "waiting time:", counter)
            counter = 0
    return found_partitions

##
def random_almost_equi_partition_fast_nonrecursive(graph, log2_num_blocks, delta):
    blocks = random_equi_partitions(graph, 1, 2)[0]
    while len(blocks) < 2**log2_num_blocks:
        subgraph_splits = []
        for subgraph in blocks:
            subgraph_splits += random_almost_equi_partitions(subgraph, 1, 2, delta)[0]
        blocks = subgraph_splits
    return blocks

def random_almost_equi_partitions_fast(graph, num_partitions, log2_num_blocks, delta):
    print("note: still need to addthe delta stuff ot this...")
    found_partitions = []
    while len(found_partitions) < num_partitions:
        found_partitions.append(random_almost_equi_partition_fast_nonrecursive(graph, log2_num_blocks, delta))
    return found_partitions