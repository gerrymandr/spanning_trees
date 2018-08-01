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
import copy

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

def acceptable(weight_of_sub_arb, acceptable_sizes):
    for interval in acceptable_sizes:
        if ((weight_of_sub_arb >= interval[0]) and (weight_of_sub_arb <= interval[1])):
            return True
    return False

def random_split_no_delta(graph, tree, num_blocks, delta):
    was_good = False
    while was_good == False:
        num_blocks = 4
        pop = [tree.nodes[i]["POP10"] for i in tree.nodes()]
        total_population = np.sum(pop)
        
        ideal_weight = total_population/ num_blocks
        
        label_weights(tree)
        
        acceptable_nodes = list(tree.nodes())
        acceptable_nodes.remove(tree.graph["root"])
        delta = .1
        helper_list = copy.deepcopy(acceptable_nodes)
        acceptable_sizes = [ [ m * (ideal_weight* ( 1 - delta)), m* (ideal_weight *(1 + delta))] for m in range(1,num_blocks)]
        
        '''The way to look at the acceptable sizes is as follows:
           
           1) We have a list of acceptable sizes for each district
    2) Thus, we havea  list of acceptable sizes for each subtree, formed in the following way:
    
    A weight (for a subtree) is acceptable iff there is a m so that its weight is the union of m pieces of weight ideal +- delta.
    
    That is, if it's weight is in [m (ideal - delta) , m (ideal + delta)] for some m.
    
    For any given vertex,we have access to the weight of its sub arborescance.
    So we write a helper function that determines if that subarborescance is acceptable or not.
    
    Sanity check: The case we are checking below, i.e. leaves too big or too small, amounts to the case m = 1 and num_blocks - 1
    
    The heuristic is that we pick delta small enough so that there is no overlap between these regions for different m.'''
        
        for vertex in helper_list:
            if not acceptable(tree.node[vertex]["weight"], acceptable_sizes):
                acceptable_nodes.remove(vertex)
#            if tree.node[vertex]["weight"] < ideal_weight* ( 1- delta):
#                acceptable_nodes.remove(vertex)
#            if tree.node[vertex]["weight"] > ideal_weight*(num_blocks - 1 + delta):
#                acceptable_nodes.remove(vertex)
        #print([tree.node[x]["weight"] for x in acceptable_nodes])
                
        
        vertices = random.sample(acceptable_nodes, num_blocks -1)
        
        
        was_good= checker(tree,vertices, ideal_weight, delta, total_population)
    edges = [list(tree.out_edges(x))[0] for x in vertices]
    partition = remove_edges_map(graph, tree, edges) 
    
    ratios = []
    for block in partition:
        block_pop = np.sum( [tree.nodes[x]["POP10"] for x in block.nodes()])
        ratios.append( block_pop / ideal_weight)
    
    print(ratios)
        
    return ratios 

def checker(tree, chosen_vertices, ideal_weight, delta, total):
    '''return True or False depending on whether the choice of vertices producesa
    delta equipartition. [for each vertex, we remove the unique edge coing out of it]
    
    '''
    #Why is this letting in some very large partitions?
    
    minima = copy.deepcopy(chosen_vertices)
    for vertex in chosen_vertices:
        above_vertex = immediately_above(tree, vertex, chosen_vertices)
        weight =tree.node[vertex]["weight"] - np.sum( [tree.node[x]["weight"] for x in above_vertex])
        for larger_vertex in above_vertex:
            if larger_vertex in minima:
                minima.remove(larger_vertex)
        #print(weight, len(above_vertex))
        if (weight/ideal_weight) >= 1 + delta:
            return False
        if (weight/ideal_weight) <= 1 - delta:
            return False
    
    for vertex in minima:
        weight  = total - tree.node[vertex]["weight"]
        if (weight/ideal_weight) >= 1 + delta:
            return False
        if (weight/ideal_weight) <= 1 - delta:
            return False
    return True
    

def immediately_above(tree, base_vertex, chosen_vertices):
    '''
    Finds the vertices of the tree that are immediately about the base_vertex
    
    I'm not sure that the topological sort is enough information... it's not, in fact
    
    compare the ordering [a,b,c] (with more fluff)...
    This can correspond to a path tree, or to a y tree. 
    
    
    Question:
        
        I have a directed, and rooted tree T. 
        I want to preprocess the edges, so that given any collection of edges, e_1,\ldots, e_k (k is fixed)
        I can quickly (o(1) -a constant depending on k, but only ---weakly??-- on |T|), [even if we have the vertices of T sorte, I want to make sure that I only need to traverse the tree once...]
        we want to store the poset structure, really..
        
        then for eachvertex in chosen_vertices:
            if eachvertex > vertex:
                add eachvertex to list
        then for eachvertexin list:
            if anothevertex in list < eachvertex:
                remove eachvertex from list
                
        this k^2 which is fine. k issmall...
        s
    
    NOTE: we want to make T rooted at a leaf.... then geq behaves as we want.
    
    Suppose T is a (large) tree. After some proprecssing, is there an efficient way to call the geq function?
    We could just build the table. This requires |T|^2 space (and T^2 preprocessing).. which is too much.. (is it?)
    '''
    list_of_vertices_above_base = []
    for eachvertex in chosen_vertices:
        if geq(tree, eachvertex, base_vertex):
            list_of_vertices_above_base.append(eachvertex)
    for eachvertex in list_of_vertices_above_base:
        for comparevertex in list_of_vertices_above_base:
            if geq(tree, eachvertex, comparevertex):
                list_of_vertices_above_base.remove(eachvertex)
        #May need to check this because we are modifying behavior...
    #This is $k^2n$, which is fine... we can afford linear in size of tree, and quadratic in number of edges... perhaps.
    return list_of_vertices_above_base
    
    
def build_geq(tree, ordered_vertices):
    '''
    takes an directed, rooted tree, along with an ordering on its vertices, and returns an array on its vertices by vertices, populated with whether that vertex precedes the next
    okay, we definately want to use dynamical programming to build this table... otherwise we will encur n^6 time if naively comparing, which is starting to get crazy...
    
    to do this, we can start with a topological sort of the tree...
    
    actually, the top sort will let us populate alot of this table... maybe there's even a nice randomzied result, like drawing N top sorts, and checking the ordering in each will give a high guarantee on the correct comparison in this table... that's a neat question TODO... anyway, we should first build the geq table, so we can test this conjecture.
    
    how to do this dynamically? let's not even yet.
    
    wait am I being dumb ? isn't this what a top sort does?
    
    no... because top sort will give false positives.... its more usefl for orgganizing a workflow, for example making sure thatchildren get processed after their parents.
    
    
    '''
    n = len(tree)
    M = np.zeros([n,n])
    for index_1 in range(n):
        for index_2 in range(index_1, n):
            if index_2 == index_1:
                M[index_1, index_2] = 1
            else:
                is_geq = geq(tree, ordered_vertices[index_1], ordered_vertices[index_2])
                if is_geq:
                    M[index_1, index_2] = 1
                else:
                    M[index_2, index_1] = 1
                #th
                
    return M
    
def geq(tree, a, b):
    '''
    tests whether a > b in the directedtree tree
    maybe we just use this?
    '''
    while list(tree.out_edges(a)) != []:
        '''
        this is the right direction to set this up in, because our tree have only one outgoing edge perertex
        '''
        a =  list(tree.out_edges(a))[0][1]
        if a == b:
            return True
    return False
    

#graph = nx.grid_graph([15,15])
#tree = random_spanning_tree_wilson(graph)
#order = list(tree.nodes())
#M = build_geq(tree, order)
#
#other_order= list(nx.topological_sort(tree))
#These orders appear to be the same... so we don't have access to a uniformly random top sort anyway.
'''what are some sanity check properties that M should have?
transitivity (easy matrix way to check), antimmetry (check this), 

N = np.sign( np.matmul(M,M))
M == N

'''

'''this is the topic on wiki linked to from top order... about completing a dag under transitivity... should check that out.    
    
'''

graph= nx.grid_graph([20,20])
for vertex in graph:
    graph.nodes[vertex]["POP10"] = 1
tree = random_spanning_tree_wilson(graph)
#sample_best = []
#testing_length= 100
#for k in range(testing_length):
#        
#    tree = random_spanning_tree_wilson(graph)
#    #tree = random_greedy_tree(graph)
#    num_blocks = 4
#    delta = 10000
#    #ratio_list = []
#    #for i in range(1000):
#    #    ratios = random_split(graph, tree, 4)
#    #    ratio_list.append( abs( 1 - np.max([ abs( np.max(ratios) - 1), abs(1 - np.min(ratios))] )) )
#    #np.min(ratio_list)
#    
#    ratio_list = []
#    ratios = random_split(graph, tree, num_blocks, delta)
#    ratio_list.append( abs( np.max([ abs( np.max(ratios) - 1), abs(1 - np.min(ratios))] )) )
#    counter = 0
#    while (np.min(ratio_list) > .1) and (counter < 1000):
#        ratios = random_split_no_delta(graph, tree, num_blocks)
#        ratio_list.append( np.max([ abs( np.max(ratios) - 1), abs(1 - np.min(ratios))] ) )
#        counter += 1
#    print(len(ratio_list), min(ratio_list))
#    sample_best.append(min(ratio_list))
