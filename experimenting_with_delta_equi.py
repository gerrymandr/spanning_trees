# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 16:31:31 2018

@author: MGGG
"""
from projection_tools import remove_edges_map
from equi_partition_tools import label_weights
import random
import numpy as np
from Broder_Wilson_algorithms import random_spanning_tree_wilson, random_greedy_tree
import networkx as nx

def random_split(graph, tree, num_blocks, delta):
    
    #You can make this smarter by preprocessing the set of edges to the much smaller set of allowable edges (using tree weights)
    #and also forcing the edges to be chosen from their respective intervals only... which cuts down the search space a lot also.
    
    pop = [tree.nodes[i]["POP10"] for i in tree.nodes()]
    total_population = np.sum(pop)
    
    ideal_value = total_population/ num_blocks
    
    label_weights(tree)
    okay_weight_nodes = set()
    non_root_nodes= list(tree.nodes)
    non_root_nodes.remove(tree.graph["root"])
    for vertex in non_root_nodes:
        for j in range(1, num_blocks):

            if abs( tree.nodes[vertex]["weight"] - (ideal_value*j)) < delta:
                #This isn't really right...
                okay_weight_nodes.add(vertex)
    okay_weight_nodes = list(okay_weight_nodes)
    okay_edges = [list(tree.out_edges(vertex))[0] for vertex in okay_weight_nodes]
    edges = random.sample(okay_edges, num_blocks - 1)
    partition = remove_edges_map(graph, tree, edges)
    

    ratios = []
    for block in partition:
        block_pop = np.sum( [tree.nodes[x]["POP10"] for x in block.nodes()])
        ratios.append( block_pop / ideal_value)
        
    return ratios

def random_split_no_delta(graph, tree, num_blocks):
    
    #You can make this smarter by preprocessing the set of edges to the much smaller set of allowable edges (using tree weights)
    #and also forcing the edges to be chosen from their respective intervals only... which cuts down the search space a lot also.
    
    pop = [tree.nodes[i]["POP10"] for i in tree.nodes()]
    total_population = np.sum(pop)
    
    ideal_value = total_population/ num_blocks
    
    label_weights(tree)

    edges = random.sample(list(tree.edges()), num_blocks - 1)
    partition = remove_edges_map(graph, tree, edges)
    

    ratios = []
    for block in partition:
        block_pop = np.sum( [tree.nodes[x]["POP10"] for x in block.nodes()])
        ratios.append( block_pop / ideal_value)
        
    return ratios

graph= nx.grid_graph([50,50])
for vertex in graph:
    graph.nodes[vertex]["POP10"] = 1
sample_best = []
testing_length= 100
for k in range(testing_length):
        
    tree = random_spanning_tree_wilson(graph)
    #tree = random_greedy_tree(graph)
    num_blocks = 4
    delta = 10000
    #ratio_list = []
    #for i in range(1000):
    #    ratios = random_split(graph, tree, 4)
    #    ratio_list.append( abs( 1 - np.max([ abs( np.max(ratios) - 1), abs(1 - np.min(ratios))] )) )
    #np.min(ratio_list)
    
    ratio_list = []
    ratios = random_split(graph, tree, num_blocks, delta)
    ratio_list.append( abs( np.max([ abs( np.max(ratios) - 1), abs(1 - np.min(ratios))] )) )
    counter = 0
    while (np.min(ratio_list) > .1) and (counter < 1000):
        ratios = random_split_no_delta(graph, tree, num_blocks)
        ratio_list.append( np.max([ abs( np.max(ratios) - 1), abs(1 - np.min(ratios))] ) )
        counter += 1
    print(len(ratio_list), min(ratio_list))
    sample_best.append(min(ratio_list))
