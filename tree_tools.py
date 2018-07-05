# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 13:40:29 2018

@author: MGGG
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 12:01:21 2018

@author: MGGG
"""

import networkx as nx
import random
import itertools
import numpy as np
import scipy.linalg
from scipy.sparse import csc_matrix
import scipy
from scipy import array, linalg, dot
import equi_partition_tools
import projection_tools

#from naive_graph_partitions import k_connected_graph_partitions

######Tree counting

def log_number_trees(graph, weight = False):
    '''Computes the log of the number of trees, weighted or unweighted. 
    
    :graph: The input graph
    :weight: the edge variable name that describes the edge weights
    
    '''
    #Kirkoffs is the determinant of the minor..
    #at some point this should be replaced with a Cholesky decomposition based algorithm, which is supposedly faster. 
    if weight == False:
        m = nx.laplacian_matrix(graph)[1:,1:]
    if weight == True:
        m = nx.laplacian_matrix(graph, weight = "weight")[1:,1:]
    m = csc_matrix(m)
    splumatrix = scipy.sparse.linalg.splu(m)
    diag_L = np.diag(splumatrix.L.A)
    diag_U = np.diag(splumatrix.U.A)
    S_log_L = [np.log(np.abs(s)) for s in diag_L]
    S_log_U = [np.log(np.abs(s)) for s in diag_U]
    LU_prod = np.sum(S_log_U) + np.sum(S_log_L)
    return  LU_prod


def likelihood_tree_edges_pair(graph,tree,edge_list):
    '''
    
    This computes the partition associated ot (graph, tree, edge_list)
    and computes the log-likelihood that that partition is drawn via uniform tree
    with uniform edge_list sampling method
    
    graph = the graph to be partitioned
    tree = a chosen spanning tree on the graph
    edge_list = list of edges that determine the partition
    
    there are two terms in the log-likelihood:
        tree_term = from the number of spanning trees within each block
        connector_term = from the number of ways to pick a spanning tree to 
        hook up the blocks
    
    the way that connector_term works:
        1. It builds a graph whose nodes are the blocks in the partitions
        and whose multi-edges correspond to the set of edges connecting those blocks
        2. It uses the multi-graph (or weighted graph) version of Kirkoffs theorem to compute the
        ways to 
        
    the way that tree_term works:
        for each block of hte partition, it compute the number of spanning trees
        that that induced subgraph as.
    returns (tree term + connector term)
    TODO -- rewrite score to be 1 / this
    
    '''
    partition = projection_tools.remove_edges_map(graph, tree, edge_list)
    #this gets the list of subgraphs from (tree, edges) pair
    tree_term = np.sum([log_number_trees(g) for g in partition])

    #Building connector term:
    connector_graph = nx.Graph()
    connector_graph.add_nodes_from(partition)
    for subgraph_1 in partition:
        for subgraph_2 in partition:
            if subgraph_1 != subgraph_2:
                cutedges = cut_edges(graph, subgraph_1, subgraph_2)
                if cutedges != []:
                    connector_graph.add_edge(subgraph_1, subgraph_2, weight = len(cutedges))
    cut_weight = log_number_trees(connector_graph, True)
    return (tree_term + cut_weight)
    

def effective_resistance(G, vertex_a, vertex_2, LU = 0):
    #Can pass LU decomposition...
    
    return None
    

#####For lifting:

def cut_edges(graph, subgraph_1, subgraph_2):
    '''Finds the edges in graph from 
    subgraph_1 to subgraph_2
    
    :graph: The ambient graph
    :subgraph_1: 
    :subgraph_2:
        
    TODO: Think about algorithm
    
    
    '''
    edges_of_graph = list(graph.edges())

    list_of_cut_edges = []
    for e in edges_of_graph:
        if e[0] in subgraph_1 and e[1] in subgraph_2:
            list_of_cut_edges.append(e)
        if e[0] in subgraph_2 and e[1] in subgraph_1:
            list_of_cut_edges.append(e)
    return list_of_cut_edges


###Tree walk
    
def propose_step(graph,tree):
    '''
    this proposes a basis exchange move on the spanning trees
    definedin Broder //// also in /// (for matroid case)
    :graph: the ambient graph
    :tree: the current spanning tree
    
    '''
    tree_edges = list(tree.edges())
    tree_edges_flipped = [ tuple((e[1], e[0])) for e in tree_edges]
    graph_edges = graph.edges()
    #Because of stupid stuff in networkx - if we don't include the flipped
    #list also, then the problem is that graph_edges might have an edge
    #stored as (a,b) and tree_edges the same edge stored as (b,a), so it
    #won't realize not to use that edge
    
    edges_not_in_tree = [e for e in graph_edges if e not in tree_edges and e not in tree_edges_flipped]
    e = random.choice(edges_not_in_tree)
    tree.add_edges_from([e])
    cycle = nx.find_cycle(tree, orientation = 'ignore')
    w = random.choice(cycle)
    new_tree = nx.Graph()
    new_tree.add_edges_from(list(tree.edges()))
    new_tree.remove_edges_from([w])
    tree.remove_edges_from([e])
#    print(len(U.edges()))
#    print(U.edges())
    return U
    

def MH_step(G, T,e, equi = False, MH = True):
    n = len(e)
    U = propose_step(G,T)
    if equi == False:
        e2 = random.sample(list(U.edges()),n)
    if equi == True:
        e2 = best_edge_for_equipartition(G,U)[0]
    if MH == True:
        current_score = score_tree_edges_pair(G,T,e)
        new_score = score_tree_edges_pair(G, U, e2)
        if new_score > current_score:
            return [U,e2]
        else:
           p = np.exp(new_score - current_score)
           a = np.random.uniform(0,1)
           if a < p:
               return [U,e2]
           else:
               return [T,e]
    if MH == False:
        return [U,e2]





        
########Validation -- 
        
            
       
###Emperical distribution creation tools

def count(x, visited_partitions):

    x_lens = np.sort([len(k) for k in x])
    count = 0
    for sample_nodes in visited_partitions:
        #sample_nodes = set([frozenset(g.nodes()) for g in i])
        sample_lens = np.sort([len(k) for k in sample_nodes])
        #if (x_lens == sample_lens).all():
        if np.array_equal(x_lens , sample_lens):
            if x == sample_nodes:
                count += 1
    return count


def make_histogram(A, visited_partitions):
    A_node_lists = [ set([frozenset(g.nodes()) for g in x]) for x in A]
    dictionary = {}
    for x in A_node_lists:
        dictionary[str(x)] = count(x,visited_partitions) / len(visited_partitions)
    return dictionary

##########################
    
def test(grid_size, k_part, steps = 100, equi = False, MH = True):
    from naive_graph_partitions import k_connected_graph_partitions
    #k_part = 3 nnum partitions
    G = nx.grid_graph(grid_size)
    A = list(k_connected_graph_partitions(G, k_part))
    
    ##Tree walks:
    T = random_spanning_tree(G)
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


    
    