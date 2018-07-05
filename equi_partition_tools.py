# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 11:42:30 2018

@author: MGGG
"""

''' Equipartition tools'''

def return_equipartition_if_exists(graph, tree, num_blocks):
    '''
    graph = the graph to be partitioned
    tree = a chosen spanning tree on the graph
    num_blocks = number of blocks in the partitions returned
    
    This returns the num_blocks equi-partition if it exists. Otherwise returns
    none.
    '''
    block_size = len(graph.nodes()) / num_blocks
    if int(block_size) != block_size:
        print("impossible due to divisibility")
        return None


def build_node_weights(tree):
    '''arbitrarily directs the tree, and adds weights to each node to make
    dynamical code for finding the equi-split fast
    
    :tree: the tree we want to split. This needs to be passed to this as a
    directed tree rooted at vertex q...
    
    #Todo: Note that in the future we should be careful about
    #keeping track of the orientation on our trees that come from the various
    #constructions
    '''

    return 
    
def find_cut_of_size(graph, tree, size):
    '''
    graph = the graph to be partitioned
    tree = a chosen spanning tree on the graph
    ratio = a number between 0 and 1
    
    this returns the edge so that the (tree, edge) pair gives a partition
    with smallest piece of specified size
    '''
    tree_edges = tree.edges()
    for edge in tree_edges:
        if equi_score_tree_edge_pair(graph, tree, edge) == size:
            return edge
    return None
            
    

def best_edge_for_equipartition(graph,tree, num_blocks  = 2):
    '''
    Note: Currently this only works for 2 partitions!!
    NOte: this is not the best way to do this. .... what you should do instead
    is start at any leaf, and move the edge (by gradient ascent kind of thing)
    until you get to a global min for balancing.
    
    Does this actually work? 
    
    Same for tuples -- check all possible moves, and gradient ascent. If at a
    critical point, return. (Criticla point means -- all possible local moves
    decrease the goodness f the balance...)
    
    I'm confused about how this touches balanced cut: 
        http://lucafoschini.com/papers/Balanced_Algorithmica.pdf
        
    #A better algorithm is just to do this recursively... if there is a perfect
    partitioning...
    
    TODO -- USE DYNAMICAL PROGRAMMING!!


    graph = the graph to be partitioned
    tree = a chosen spanning tree on the graph
    num_blocks = number of blocks in the partitions returned
    
    find the edge_list from the edges of tree so that the resulting partition
    minimizes the differences in size between the blocks
    
    '''
    if num_blocks > 2:
        print("you haven't made this work for blocks > 2")
        return None
    list_of_edges = list(tree.edges())
    best = 0
    candidate = 0
    for e in list_of_edges:
        score = equi_score_tree_edge_pair(G,T,e)
        if score > best:
            best = score
            candidate = e
    return [candidate, best]

def equi_score_tree_edge_pair(G,T,e):
    T.remove_edges_from([e])
    components = list(nx.connected_components(T))
    T.add_edges_from([e])
    A = len(components[0])
    B = len(components[1])
    x =  np.min([A / (A + B), B / (A + B)])
    return x

def random_equi_partition_trees(graph, k_part, number = 100):
    equi_partitions = [] 
    counter = 0
    while len(equi_partitions) < number:
        counter += 1
        T = random_spanning_tree(graph)
        e = equi_partition(T, k_part)
        if e != False:
            print(len(equi_partitions), "waiting time:", counter)
            equi_partitions.append( R(graph, T, e) )
            counter = 0
    return equi_partitions
    
def equi_partition(T, num_blocks):
    #Returns the partition if T can give an equi partition in num_blocks,
    #Else return false
    
    #Currently this is hard coded for 4 partitions -- but there shold be a good
    #and scalable algorithm
    if num_blocks == 4:
        e = equi_split(T)
        if e == False:
            return False
        if e != False:
            T.remove_edges_from([e])
            components = list(nx.connected_component_subgraphs(T))
            T.add_edges_from([e])
            e1 = equi_split(components[0])
            if e1 == False:
                return False
            e2 = equi_split(components[1])
            if e2 == False:
                return False
    else:
        print("you didn't set up functionality for more than 4 partitions yet!")
    return [e, e1, e2]

def equi_split(T):
    #Returns the partition if T can be split evenly in two
    #Else returns False
    T_edges = T.edges()
    for e in T_edges:
        T.remove_edges_from([e])
        components = list(nx.connected_components(T))
        T.add_edges_from([e])
        A = len(components[0])
        B = len(components[1])
        if A == B:
            return e
    return False
