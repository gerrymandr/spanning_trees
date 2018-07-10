# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 17:32:53 2018

@author: MGGG
"""

from walk_tools import equi_shadow_walk
import networkx as nx
from tree_sampling_tools import random_equi_partitions, random_spanning_tree, random_spanning_tree_wilson, random_equi_partitions_fast, random_almost_equi_partitions_fast, random_almost_equi_partitions, random_almost_equi_partitions_with_walk, random_almost_equi_partitions_fast_with_walk
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
    if graph_type == "torus":
        cycle_1 = nx.cycle_graph(graph_size)
        cycle_2 = nx.cycle_graph(graph_size)
        graph = nx.cartesian_product(cycle_1, cycle_2)
        
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
            tree_partitions = random_almost_equi_partitions_fast(graph, num_maps, log2_num_blocks, delta)
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

def test(graph_size, num_blocks, delta):
    graph = nx.grid_graph([graph_size, graph_size])
    tree_partitions = random_almost_equi_partitions_with_walk(graph, 1, num_blocks, delta)
    for partition in tree_partitions:
        visualize_partition(graph, partition)
        print([len(x) for x in partition])
        
def test_fast_with_walk(graph_size, num_blocks, delta):
    graph = nx.grid_graph([graph_size, graph_size])
    tree_partitions = random_almost_equi_partitions_fast_with_walk(graph, 1, num_blocks, delta)
    for partition in tree_partitions:
        visualize_partition(graph, partition)
        print([len(x) for x in partition])
    
        
        
test_fast_with_walk(160, 3, .1)


#The efficiency of this can depend on a lot whether you land near somewhere thats an
#equipartition... maybe can be faster if we do the label updating in a smart way.

#parts = explore_random(40,1,2, pictures = True, divide_and_conquer = True, equi = False, graph_type = "grid", delta = .2)
#parts = explore_random(120,1,12, pictures = True, divide_and_conquer = False, equi = False, delta = .1)
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

    
    