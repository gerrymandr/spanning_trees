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
    #Takes the components of the subforest produced
    #And accepts a fewer than numleaves nodes from each components
    #In total goal is to pick num_blocks - 1 nodes
    
    #the goal is also to pick the tuples with the correct probabilities...
    #Do we always need to pick 1 from each components/
    
    #IMPORTANT QUESTION: Make sure this samples uniformly!
    
    #We have m bins,and n balls. Each bin has a number k_i, and we allow k_i balls to be put in bin i. We want to sample uniformly from among all ways to place the n balls.
    
    this can be said in these terms: we are trying to sample rank n elements from the partition matroid corresponding to the bins and the numbers k_i.
    '''
    
   # USe this:  https://stats.stackexchange.com/questions/184348/how-to-generate-samples-uniformly-at-random-from-multiple-discrete-variables-sub
    
    
    random.shuffle(components)
    total = 0
    list_of_vertices = []
    unexhausted = []
    for component in components:
        if total < num_blocks - 1:
            leaves = num_leaves(component)
            if leaves == 0:
                #This is the case of a single vertex
                total += 1
                list_of_vertices.append(list(component.nodes())[0])
            else:
                num_to_pick = random.choice(range(1, min(leaves - 1, num_blocks - 1 - total) + 1))
                total += num_to_pick
                list_of_vertices += random.sample(list(component.nodes()), num_to_pick)
                if num_to_pick < leaves - 1:
                    unexhausted.append(component)
                
    if total < num_blocks - 1:
        print("Add the bit using the unexhausted components")
        
    #I think it's possible for some path components to have no-one in them
    return list_of_vertices
    

def random_split_fast(graph, tree, num_blocks, delta, allowed_counts = 100):
    pop = [tree.nodes[i]["POP10"] for i in tree.nodes()]
    total_population = np.sum(pop)
    
    ideal_weight = total_population/ num_blocks
    
    label_weights(tree)
    
    acceptable_nodes = list(tree.nodes())
    acceptable_nodes.remove(tree.graph["root"])
    helper_list = copy.deepcopy(acceptable_nodes)
    acceptable_sizes = [ [ m* (ideal_weight* ( 1 - delta)), m* (ideal_weight *(1 + delta))] for m in range(1,num_blocks)]
    ##Need to work out what this is...
   # print("Can we get some elimination test based on not all the intervals appearing")
    '''
A weight (for a subtree) is acceptable iff it's weight is in [m (ideal - delta) , m (ideal + delta)] for some m. Heuristically, take delta small '''

    
    for vertex in helper_list:
        if not acceptable(tree.node[vertex]["weight"], acceptable_sizes):
            acceptable_nodes.remove(vertex)

    sample_subforest = nx.subgraph(tree, acceptable_nodes)
    sample_subforest = sample_subforest.to_undirected()
    components = list(nx.connected_component_subgraphs(sample_subforest))
    [num_leaves(x) for x in components]
    #test_tree(sample_subforest)
    if len(acceptable_nodes) < num_blocks - 1:
        print("bad tree")
        return False
    
    #Nextthing to add: only choose one edge from each component of acceptable_nodes[tree] induced subtree... this doesn't work, unless the component is a path.... there are simple examples on Y graphs.
    #What does work is that we can only ever choose k-1 nodes from a subtree that has k leaves... there isn't a unique number..
    #If its a path, do we always need to pick one from it?
    
    
    was_good = False
    counter = 0
    while (was_good == False) and (counter < allowed_counts):

        vertices = component_sampler(components, num_blocks)
        counter += 1
        was_good= checker(tree,vertices, ideal_weight, delta, total_population)
    if counter >= allowed_counts:
        return False
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

graph= nx.grid_graph([160,160])
for vertex in graph:
    graph.node[vertex]["POP10"] = 1
tree = random_spanning_tree_wilson(graph)

random_split_fast(graph, tree, 8, .1)
