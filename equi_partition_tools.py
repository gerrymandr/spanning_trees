# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 11:42:30 2018

@author: MGGG
"""

''' Equipartition tools'''

import networkx as nx
import numpy as np
import random

def equi_score_tree_edge_pair(G,T,e):
    T.remove_edges_from([e])
    components = list(nx.connected_components(T))
    T.add_edges_from([e])
    A = len(components[0])
    B = len(components[1])
    x =  min([A / (A + B), B / (A + B)])
    return x

#def almost_equi_split(tree):
#    # Returns the partition if T can be split evenly in two
#    # Else returns False
#    label_weights(tree)
#    edge, weight = choose_best_weight(tree)
#
#    if weight == len(tree) // 2:
#        return edge
#
#    return False

def equi_split(tree, num_blocks):
    '''This will return a perfect equi-partition into num_blocks blocks
    It will do so by running choose best weight_hard to peel off pieces of 
    appropriate size
    
    this works because it is returning the edges, handling the components is done
    later...
    
    :tree:
    :num_blocks:
    '''
    label_weights(tree)
    found_edges = []
    found_blocks = 0
    while found_blocks < num_blocks - 1:
        edge = choose_best_weight_hard(tree, num_blocks)
        if edge != None:
            found_edges.append(edge)
            found_blocks += 1
            update_weights(tree, edge)
        if edge == None:
            return None
    return found_edges

def almost_equi_split(tree, num_blocks, delta):
    '''This returns a ...
    
    Def: Let T be a spanning tree, and fix $\delta > 0$. If there is a subset of k edges E, so that removing the edges E from T gives components A_1, ... A_{k+1}, with |A_i| / |A_j| <= 1 + \delta for all $i$ and $j$, then say the $A_i$ are a $\delta$-equi partition, and $T$ is a k+1 delta-equi tree.
    Chooses a random closest split for a tree...
    
    
    --- > CHanged his to 1 - delta < A / (n / k) < 1 + delta
    
    
    '''
    label_weights(tree)

    found_edges = []
    found_blocks = 0
    while found_blocks < num_blocks - 1:
        edge, ratio = choose_best_weight(tree, num_blocks)
        if (ratio >= 1 + delta) or (ratio <= 1 - delta):
            print(ratio)
            return None
        found_edges.append(edge)
        found_blocks += 1
        update_weights(tree, edge)
    return found_edges 

#graph = nx.grid_graph([160,160])
#closeness = []
#for i in range(100):
#    print("next tree:")
#    tree = random_spanning_tree_wilson(graph)
#    if almost_equi_split(tree, 2, .1) != None:
#        print("Good")

def check_delta_equi_split(subgraph_sizes, delta = .01):
    '''returns True if all ratios of sizes are all within 1 + delta
    :subgraph_sizes: list of sizes
    '''

    for i in range(len(subgraph_sizes)):
        for j in range(i, len(subgraph_sizes)):
            if subgraph_sizes[i]/subgraph_sizes[j] > 1 + delta:
                return False
    return True



#tree = random_spanning_tree(graph)
#label_weights(tree)
#test_tree(tree)      

def update_weights(tree, edge):
    '''update the weights of a graph after selecting an edge to cut
    this will set the weights above the edge to zero
    and below the edge will get decremented by 1
    '''
    
    head_node = edge[1]
    tail_node = edge[0]
    weight = tree.nodes[tail_node]["weight"] 
    set_label_zero_above(tree, tail_node)
    decrement_label_weights_below(tree, head_node, weight)
    
    
###TODO: Make these non-recursive also.
    
def set_label_zero_above(tree, node):
    '''sets the label weights to zero at and above the passed node
    '''
       
    ordering = list(nx.topological_sort(tree))
    tree.nodes[node]["weight"] = 0
    for node in ordering[::-1]:
        out_edge = list(tree.out_edges(node))
        if out_edge != []:
            if tree.nodes[out_edge[0][1]]["weight"] == 0:
                tree.nodes[node]["weight"] = 0
#            
#def set_label_zero_above_recursive(tree, node):
#    
#    in_edges = tree.in_edges(node)
#    tree.nodes[node]["weight"] = 0
#    for edge in in_edges:
#        set_label_zero_above_recursive(tree, edge[0])
#        
def test_tree(tree):
    for vertex in tree:
            tree.nodes[vertex]["pos"] = vertex
    labels = nx.get_node_attributes(tree, "weight")
    nx.draw(tree, pos=nx.get_node_attributes(tree, 'pos'), labels= labels)
    
#graph = nx.grid_graph([5,5])
#tree = random_spanning_tree(graph)
#label_weights(tree) 
    
    
def decrement_label_weights_below(tree, start_node, weight):
    
    node = start_node
    ordering = list(nx.topological_sort(tree))
    for vertex in tree:
        tree.nodes[vertex]["touched"] = 0
    tree.nodes[node]["weight"] += -1 * weight
    tree.nodes[node]["touched"] = 1
    for node in ordering:
        in_edges = list(tree.in_edges(node))
        if in_edges != []:
            parents = [edge[0] for edge in in_edges]
            for parent in parents:
                if tree.nodes[parent]["touched"] == 1:
                    tree.nodes[node]["weight"] += -1 * weight
                    tree.nodes[node]["touched"] = 1
       
#def decrement_label_weights_below_recursive(tree, node, weight):
#    '''lowers the label weights by weight at and below the passed node
#    '''
#    out_edges = list(tree.out_edges(node))
#
#    tree.nodes[node]["weight"] += -1 * weight
#    if not out_edges:
#        return
#    out_edges = out_edges[0]
#    decrement_label_weights_below_recursive(tree, out_edges[1], weight)

def label_weights(tree):
    '''
    Label nodes of of a directed, rooted tree by their weights.
#
#    :tree: NetworkX DiGraph.
#    :returns: Nothing.
#
#    The "weight" of a node is the size of the subtree rooted at itself.
#    
#    TODO: implement a priority queue of weights so that you don't need to search through the graph...
    
    This is the nonrecursive version, which makes pyhton not crash...
    
    '''

    #This is a perfect problem for topological sorting!
    
    for node in tree.nodes:
        tree.nodes[node]["weight"] = 1
    
    
    ordering = nx.topological_sort(tree)
    for node in ordering:
        parents = [ edge[0] for edge in tree.in_edges(node)]
        for parent in parents:
            tree.nodes[node]["weight"] += tree.nodes[parent]["weight"]

    

def choose_best_weight_hard(tree, num_blocks):
    '''Returns an edge that cuts of a chunk of size n_nodes/ num_blocks
    if it exists. Otherwise returns None.
    
    :graph:
    :returns: edge
    '''
    size = len(tree.nodes()) / num_blocks
    for node in tree:
        if tree.nodes[node]["weight"] == size:
            return list(tree.edges(node))[0]
    return None

def choose_best_weight(tree, num_blocks):
    """Choose edge from graph with weight closest to n_nodes / num_blocks.

    :graph: NetworkX Graph labeled by :func:`~label_weights`.
    :returns: Tuple (edge, weight).

    """
    len_tree = len(tree)
    ideal_value = len_tree/ num_blocks
    best_node = None
    best_difference = float("inf")
    tree_nodes = list(tree.nodes())
    random.shuffle(tree_nodes)
    for node in tree_nodes:
        diff = abs(ideal_value - tree.nodes[node]["weight"])
        if diff < best_difference:
            best_node = node
            best_difference = diff

    edge = list(tree.edges(best_node))[0]
    weight = tree.nodes[best_node]["weight"]

    return (edge, ideal_value /  weight)
