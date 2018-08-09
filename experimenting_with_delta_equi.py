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
from rankrsampler_testing import sampler

def acceptable(weight_of_sub_arb, acceptable_sizes):
    for interval in acceptable_sizes:
        if ((weight_of_sub_arb >= interval[0]) and (weight_of_sub_arb <= interval[1])):
            return True
    return False

def num_leaves(tree):
    #Returns the number of leaves that a tree has
    return np.sum([1 for x in tree.nodes() if tree.degree(x) ==1])

def component_sampler(components, num_blocks):
    '''
    Caveat: We need to be in the regime where delta is so small that the leaf counting heuristic is true.
    
    #Takes the components of the subforest produced
    #And accepts a fewer than numleaves nodes from each components
    #In total goal is to pick num_blocks - 1 nodes
    '''
    

    list_of_vertices = []
    leaf_constraints = []
    for component in components:
        leaves = num_leaves(component)
        if leaves > 0:
            leaf_constraints.append(int(num_leaves(component) - 1))
        else:
            leaf_constraints.append(1)
    if np.sum(leaf_constraints) < num_blocks - 1:
        return False
        
    size_marginals = sampler(leaf_constraints, num_blocks - 1)
    for i in range(len(components)):
        list_of_vertices += random.sample(components[i].nodes(), size_marginals[i])
                
    return list_of_vertices
    

def random_split_fast(graph, tree, num_blocks, delta, allowed_vector = False, allowed_counts = 100):
    
    
    
    pop = [tree.nodes[i]["POP10"] for i in tree.nodes()]
    total_population = np.sum(pop)
    
    ideal_weight = total_population/ num_blocks
    
    label_weights(tree)

    
    acceptable_nodes = list(tree.nodes())
    acceptable_nodes.remove(tree.graph["root"])
    helper_list = copy.deepcopy(acceptable_nodes)
    
        
    acceptable_sizes = [ [ m* (ideal_weight* ( 1 - delta)), m* (ideal_weight *(1 + delta))] for m in range(1,num_blocks)]


    '''
A weight (for a subtree) is acceptable iff it's weight is in [m (ideal - delta) , m (ideal + delta)] for some m. Heuristically, take delta small '''

    
    for vertex in helper_list:
        if not acceptable(tree.node[vertex]["weight"], acceptable_sizes):
            acceptable_nodes.remove(vertex)

    sample_subforest = nx.subgraph(tree, acceptable_nodes)
    sample_subforest = sample_subforest.to_undirected()
    components = list(nx.connected_component_subgraphs(sample_subforest))
    #test_tree(sample_subforest)
    if len(acceptable_nodes) < num_blocks - 1:
        print("bad tree")
        return False
    
    
    was_good = False
    counter = 0
    while (was_good == False) and (counter < allowed_counts):

        vertices = component_sampler(components, num_blocks)
        if vertices == False:
            return False
            #This is the case when the allowable set isn't big enough support a partition... this relies on the assumption that delta is small so that no allowable interval of nodes can contain a district...
        counter += 1
        was_good= checker(tree,vertices, ideal_weight, delta, total_population)
    if counter >= allowed_counts:
        return "FailedToFind"
    print(checker(tree, vertices, ideal_weight, delta, total_population))
    print("counter:", counter)

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
    #Need to add root to chosen_vertices in order tosee the bottom piece.

    for vertex in chosen_vertices:
        above_vertex = immediately_above(tree, vertex, chosen_vertices)
        weight =tree.node[vertex]["weight"] - np.sum( [tree.node[x]["weight"] for x in above_vertex])
        #print(weight, len(above_vertex))
        if (weight/ideal_weight) >= 1 + delta:
            return False
        if (weight/ideal_weight) <= 1 - delta:
            return False
    vertex = tree.graph["root"]
    above_vertex = immediately_above(tree, vertex, chosen_vertices)
    weight =tree.node[vertex]["weight"] - np.sum( [tree.node[x]["weight"] for x in above_vertex])
    #print(weight, len(above_vertex))
    if (weight/ideal_weight) >= 1 + delta:
        return False
    if (weight/ideal_weight) <= 1 - delta:
        return False
    return True
    

def immediately_above(tree, base_vertex, chosen_vertices):
    '''
    Finds the vertices of the tree that are immediately about the base_vertex
    Note that top. sort isn't enough information ...compare the ordering [a,b,c] (with more refinments)... This can correspond to a path tree, or to a y tree. 
    
    This is not too slow -- linear in size of tree, * num_districts^3
    '''
    list_of_vertices_above_base = []
    for eachvertex in chosen_vertices:
        if geq(tree, eachvertex, base_vertex):
            list_of_vertices_above_base.append(eachvertex)
    for eachvertex in list_of_vertices_above_base:
        for comparevertex in list_of_vertices_above_base:
            if geq(tree, eachvertex, comparevertex):
                if eachvertex in list_of_vertices_above_base:
                    list_of_vertices_above_base.remove(eachvertex)

    return list_of_vertices_above_base
    
    
def build_geq(tree, ordered_vertices):
    '''
    takes an directed, rooted tree, along with an ordering on its vertices, and returns an array on its vertices by vertices, populated with whether that vertex precedes the next
    This is incredibly inefficient to build. I wonder if there is  a dynmical programming solution her
    
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
                    M[index_2, index_1] = -1
                #th
                
    return M
    
def geq(tree, a, b):
    '''
    tests whether a > b in the directedtree tree
    maybe we just use this?
    '''
    while list(tree.out_edges(a)) != []:
        '''
        this is the right direction to set this up in, because our tree have only one outgoing edge per vertex
        '''
        a =  list(tree.out_edges(a))[0][1]
        if a == b:
            return True
    return False
    


graph= nx.grid_graph([160,160])
for vertex in graph:
    graph.node[vertex]["POP10"] = 1
    
for i in range(15):
    tree = random_spanning_tree_wilson(graph)
    print(random_split_fast(graph, tree, 16, .2,50))
    
#They get super rare... which is why it's important to use the divide and conquer algorithm. Divide and conquer biases the distribution on spanning trees towards those which can be split. Can we analyze the way in which it does so?
