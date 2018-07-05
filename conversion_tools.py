# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 15:25:18 2018

@author: MGGG
"""

        
def subgraph_to_node(list_of_subgraph_partitions):
    '''This takes a list of lists of subgraphs, into a list of sets of 
    frozen sets of the nodes of those subgraphs:
        
        e.g. [[g_1, g_2], [h_1, h_2]] goes to:
        [ (frozen_set(nodes of g_1), frozen_set(nodes of g_2)), 
        ( frozen_set(nodes of h_1), frozen_set(nodes of h_2))]
        
    This is because it expensive to check whether two partitions are the same, and this format
    is easier for doing so, because frozen sets are hashable.
    
    :list_of_subgraph_partitions: The list of lists of subgraphs
    '''
    
    frozen_set_partition_list  = []
    for partitions in list_of_subgraph_partitions:
        frozen_set_partition_list.append(set([frozenset(g.nodes()) for g in partitions]))
        
    return frozen_set_partition_list