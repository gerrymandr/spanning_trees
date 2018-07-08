# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 17:32:53 2018

@author: MGGG
"""

from walk_tools import equi_shadow_walk
import networkx as nx
from tree_sampling_tools import random_equi_partitions, random_spanning_tree, random_spanning_tree_wilson, random_equi_partitions_fast, random_almost_equi_partitions_fast, random_almost_equi_partitions
from equi_partition_tools import check_delta_equi_split
from visualization_tools import visualize_partition
import numpy as np
def explore_random( graph_size, num_maps, num_blocks, pictures = False, divide_and_conquer = False, equi = False, graph_type = "grid", delta = .1):
    '''This samples random equi-partitoins according to natural likelihood
    
    :fast: The divide and conquer strategy. Currently unclear what distirbution this gives.
    :pictures: whether to display pictures of the found plan
    
    
    '''
    if graph_type == "grid":
        graph = nx.grid_graph([graph_size, graph_size])
    if graph_type == "triangle":
        graph = nx.triangular_lattice_graph(graph_size, graph_size)
#    if graph_type == "dodeca":
#        graph = nx.dodecahedral_graph()
        
    if equi == True:
        if divide_and_conquer == False:
            tree_partitions = random_equi_partitions(graph, num_maps, num_blocks)
        if divide_and_conquer == True:
            log2_num_blocks = np.log2(num_blocks)
            if int(log2_num_blocks) != log2_num_blocks:
                print("Must be power of 2 number of blocks")
                return
            tree_partitions = random_equi_partitions_fast(graph, num_maps, log2_num_blocks)
    if equi == False:
        if divide_and_conquer == False:
            tree_partitions = random_almost_equi_partitions(graph, num_maps, num_blocks, delta)
        if divide_and_conquer == True:
            log2_num_blocks = np.log2(num_blocks)
            if int(log2_num_blocks) != log2_num_blocks:
                print("Must be power of 2 number of blocks")
                return
            tree_partitions = random_almost_equi_partitions_fast(graph, num_maps, log2_num_blocks)
    if pictures == True:
        for partition in tree_partitions:
            visualize_partition(graph, partition)
            print([len(x) for x in partition])
            
    return tree_partitions


def explore_walk(graph_size, num_blocks):
    '''
    This does tree walk to sample equi-partitions
    '''
    graph = nx.grid_graph( [graph_size, graph_size])
    tree = random_spanning_tree(graph)
    tree_partitions =  equi_shadow_walk(graph, tree,  3, num_blocks)
    return tree_partitions

#graph = nx.grid_graph( [100,100])
#tree = random_spanning_tree_wilson(graph)
#tree = random_spanning_tree(graph)
#Wilson is more than 10 times faster for larger graphs...
#    

#parts = explore_random(120,1,8, pictures = True, divide_and_conquer = False, equi = False, delta = .1)
#check_delta_equi_split([len(x) for x in parts[0]], .01)
#explore_walk(8,4)
#
#parts = explore_random(10,1,3, pictures = True, divide_and_conquer = False, equi = False, graph_type = "dodeca")

'''
Todo: intead of hard equi partitions, expand it to delta equi... and 
get all delta equi partitions... is this going to slow down the check step?

Add a score function -- 

1. Draw a random tree
2. Add node weights
3. Draw random edges until you get one that lives within delta of ok (hard or soft...)
4. Accept it.

"Turtles on turtles..." but may work well.

'''

############Old tests:
#
#def test(grid_size, k_part, steps = 100, equi = False, MH = True):
#
#    ##Tree walks:
#    tree = random_spanning_tree(graphs)
#    e = list(T.edges())[0:k_part - 1]
#    visited_partitions = []
#    for i in range(steps):
#        new = MH_step(G, T, e, equi, MH)
#        #This is the step that takes in the graph G, the spanning tree T, 
#        #and the list of edges e that we are currently planning to delete.
#        T = new[0]
#        e = new[1]
#        visited_partitions.append(R(G,T,e))
#        
#        #R(emoval) is the function that returns the partition you get by removing e from T
#    ###
#    
#    ##Statistics from output from tree tools:
#    visited_partitions_node_format = subgraph_to_node(visited_partitions)
#    histogram = make_histogram(A, visited_partitions_node_format)
#    total_variation = 0
#    for k in histogram.keys():
#        total_variation += np.abs( histogram[k] - 1 / len(A))
#    print("total variation", total_variation)
#    return [histogram, A, visited_partitions]
#     
#
##h1, A, partitions = test([2,3], 3)
#    
#def tree_walk(grid_size, k_part, steps = 100, MH = True, how_many = 'one', demand_equi = False):
#    G = nx.grid_graph(grid_size)
#    ##Tree walks:
#    T = random_spanning_tree(G)
#    e = list(T.edges())[0:k_part - 1]
#    visited_partitions = []
#    for i in range(steps):
#        if demand_equi == True:
#            #new = Equi_Step(G,T,e, False, MH)
#            print("You haven't set this up yet!")
#        if demand_equi == False:
#            new = MH_step(G, T, e, False, MH)
#        #This is the step that takes in the graph G, the spanning tree T, 
#        #and the list of edges e that we are currently planning to delete.
#        T = new[0]
#        e = new[1]
#        if how_many == 1:
#            visited_partitions.append(R(G,T))
#        if how_many == 'all':
#            T = random_spanning_tree(G)
#            visited_partitions += R_all(G,T, k_part)
#        if (how_many != 1) and (type(how_many) == int):
#            T = random_spanning_tree(G)
#            visited_partitions += R_sample(G,T, k_part, how_many)
#        
#    return visited_partitions
#

    
    