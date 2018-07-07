# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 17:32:53 2018

@author: MGGG
"""

from walk_tools import equi_shadow_walk

def test(grid_size, k_part, steps = 100, equi = False, MH = True):

    ##Tree walks:
    tree = random_spanning_tree(graphs)
    e = list(T.edges())[0:k_part - 1]
    visited_partitions = []
    for i in range(steps):
        new = MH_step(G, T, e, equi, MH)
        #This is the step that takes in the graph G, the spanning tree T, 
        #and the list of edges e that we are currently planning to delete.
        T = new[0]
        e = new[1]
        visited_partitions.append(R(G,T,e))
        
        #R(emoval) is the function that returns the partition you get by removing e from T
    ###
    
    ##Statistics from output from tree tools:
    visited_partitions_node_format = subgraph_to_node(visited_partitions)
    histogram = make_histogram(A, visited_partitions_node_format)
    total_variation = 0
    for k in histogram.keys():
        total_variation += np.abs( histogram[k] - 1 / len(A))
    print("total variation", total_variation)
    return [histogram, A, visited_partitions]
     
def TV(p,q):
#test comment
    total_variation = 0
    for k in p.keys():
        total_variation += np.abs(p[k] - q[k])
    return total_variation
#h1, A, partitions = test([2,3], 3)
    
def tree_walk(grid_size, k_part, steps = 100, MH = True, how_many = 'one', demand_equi = False):
    G = nx.grid_graph(grid_size)
    ##Tree walks:
    T = random_spanning_tree(G)
    e = list(T.edges())[0:k_part - 1]
    visited_partitions = []
    for i in range(steps):
        if demand_equi == True:
            #new = Equi_Step(G,T,e, False, MH)
            print("You haven't set this up yet!")
        if demand_equi == False:
            new = MH_step(G, T, e, False, MH)
        #This is the step that takes in the graph G, the spanning tree T, 
        #and the list of edges e that we are currently planning to delete.
        T = new[0]
        e = new[1]
        if how_many == 1:
            visited_partitions.append(R(G,T))
        if how_many == 'all':
            T = random_spanning_tree(G)
            visited_partitions += R_all(G,T, k_part)
        if (how_many != 1) and (type(how_many) == int):
            T = random_spanning_tree(G)
            visited_partitions += R_sample(G,T, k_part, how_many)
        
    return visited_partitions


    
    