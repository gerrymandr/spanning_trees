# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 11:44:50 2018

@author: MGGG
"""

from equi_partition_tools import equi_split
import itertools
import networkx as nx
from tree_sampling_tools import random_spanning_tree
import random
from tree_tools import cut_edges
######Projection tools:
    
'''use exercise 2 on dual graph and trees for isospannimetric 
because when you delete the super node... the number of edges you remove is equal
to the perimeter...'''
    
def remove_edges_map(graph,tree,edge_list):
    '''Short description....
    
    :graph: the graph to be partitioned
    :tree: a chosen spanning tree on the graph
    :edge_list: a list of edges of the tree
    
    returns list of subgraphs induced by the components of the forest
    obtained by removing 'edge_list edges from  tree
    
    these correspond to the 'districts'

    '''
    tree.remove_edges_from(edge_list)
    components = list(nx.connected_components(tree))
    tree.add_edges_from(edge_list)
    subgraphs = [nx.induced_subgraph(graph, subtree) for subtree in components]
    #This is expensive - TODO in case of error
    return subgraphs

def partition_spectrum(graph,tree,num_blocks):
    '''
    graph = the graph to be partitioned
    tree = a chosen spanning tree on the graph
    num_blocks = number of blocks in the partitions returned
    
    applies partitioning_map to all possible (num_blocks - 1)-tuples of
    edges of 'tree.'  The effect is to return the list of all num_blocks-partitions
    that can be obtained from 'tree.'
    
    recall that for a partition P = (P_1, P_2, ... , P_n), the P_i are 
    referred to as the 'blocks' of the partition.
    
    
    '''
    if num_blocks < 2:
        return [graph]    
    tree_edges = set(tree.edges())
    partitions = []

    for edge_list in itertools.combinations(tree_edges, num_blocks - 1):
        partitions.append(remove_edges_map(graph,tree,list(edge_list)))
    return partitions

def partition_spectrum_sample(graph,tree,num_blocks,sample_size):
    
    '''
    graph = the graph to be partitioned
    tree = a chosen spanning tree on the graph
    num_blocks = number of blocks in the partitions returned
    sample_sze = number of partitions to be returned
    
    this returns a random sample of sample_size partitions in
    the n-partition spectrum of tree
    '''
    tree_edges = set(tree.edges())
    partitions = []
    
    iteration = random.sample(list(itertools.combinations(tree_edges,\
                                        num_blocks)), sample_size)
    
    for edge_list in iteration:
        partitions.append(partition_spectrum(graph,tree,list(edge_list)))
    return partitions


def random_lift(graph, subgraphs):
    '''
    
    '''
    print("You haven't fixed this to be directed...)
    number_of_parts = len(subgraphs)
    subgraph_trees = [random_spanning_tree(g) for g in subgraphs]
    
    #This builds a graph with nodes the subgraph, and they are connected
    #if there is an edge connecting the two subgraphs
    #and each edge gets 'choices' = to all the edges in G that connect the two subgraphs
    connector_graph = nx.Graph()
    connector_graph.add_nodes_from(subgraphs)
    for subgraph_1 in subgraphs:
        for subgraph_2 in subgraphs:
            if subgraph_1 != subgraph_2:
                cutedges = cut_edges(graph, subgraph_1, subgraph_2)
                if cutedges != []:
                    connector_graph.add_edge(subgraph_1, subgraph_2, choices = cutedges)
                    #need to worry about directendess!!???
                    
                    
    connector_meta_tree = random_spanning_tree(connector_graph)
    connector_tree = nx.Graph()
    for e in connector_meta_tree.edges():
        w = random.choice(connector_graph[e[0]][e[1]]['choices'])
        connector_tree.add_edges_from([w])
        
    
    tree = nx.Graph()
    for sub_tree in subgraph_trees:
        tree.add_edges_from(sub_tree.edges())
    tree.add_edges_from(connector_tree.edges())
    edge_list = random.sample(list(T.edges()),number_of_parts - 1)
    return [tree, edge_list]