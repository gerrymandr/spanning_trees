# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 17:32:53 2018

@author: MGGG
"""

from walk_tools import equi_shadow_walk
import networkx as nx
from tree_sampling_tools import random_equi_partitions, random_spanning_tree, random_spanning_tree_wilson, random_equi_partitions_fast, random_almost_equi_partitions_fast, random_almost_equi_partitions, random_almost_equi_partitions_with_walk, random_almost_equi_partitions_fast_with_walk
#from equi_partition_tools import check_delta_equi_split
from visualization_tools import visualize_partition, visualize_partition_with_populations
import numpy as np


def explore_random(graph, num_maps, num_blocks, pictures = False, divide_and_conquer = False, equi = False, with_walk = True, delta = .1):
    '''This samples random equi-partitoins according to natural likelihood
    
    :fast: The divide and conquer strategy. Currently unclear what distirbution this gives.
    :pictures: whether to display pictures of the found plan
    :num_maps: number of maps to produce
    :num_blocks: number of blocks in each map
    :pictures: whether to display a picture at the end
    :divide_and_conquer: whether to use a divide and conquer algorithm... currently
    input muts by a power of 2
    :equi: Whether to hard constraint to same sized partitions
    :delta: the tolerance with which to accept partitions that are not equal sized.
     
    '''
    
    if with_walk == True:
        step = "Broder"
        jump_size = 1
        tree_partitions = random_almost_equi_partitions_with_walk(graph, 1, num_blocks, delta, step, jump_size)
    if with_walk == False:
     # Checking partition parameter selections
        if equi and divide_and_conquer:
            log2_num_blocks = np.log2(num_blocks)
            if int(log2_num_blocks) != log2_num_blocks:
                print("Must be power of 2 number of blocks")
                return
            tree_partitions = random_equi_partitions_fast(graph, num_maps, log2_num_blocks)
        elif equi and not divide_and_conquer:
            tree_partitions = random_equi_partitions(graph, num_maps, num_blocks)
        elif not equi and divide_and_conquer:
            log2_num_blocks = np.log2(num_blocks)
            if int(log2_num_blocks) != log2_num_blocks:
                print("Must be power of 2 number of blocks")
                return
            tree_partitions = random_almost_equi_partitions_fast(graph, num_maps, log2_num_blocks, delta)
        elif not equi and not divide_and_conquer:
            tree_partitions = random_almost_equi_partitions(graph, num_maps, num_blocks, delta)
    
    # Visualizations        
    if pictures == True:
        for partition in tree_partitions:
            visualize_partition(graph, partition)
            print("Node sizes", [len(x) for x in partition])
            print("Population", [total_pop(x) for x in partition])
            
    return tree_partitions

def total_pop(graph):
    
    return np.sum( [graph.nodes[x]["POP10"] for x in graph.nodes()] )


        
     
cuts = 4
graph = nx.grid_graph([10*cuts,10*cuts])
for vertex in graph:
    graph.nodes[vertex]["geopos"] = vertex
    graph.nodes[vertex]["POP10"] = 1
partition = explore_random(graph, 1, cuts, pictures = True, divide_and_conquer = True, equi = False, with_walk = False, delta = .1)[0]


    
    