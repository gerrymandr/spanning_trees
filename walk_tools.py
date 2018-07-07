# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 17:28:34 2018

@author: MGGG
"""
from equi_partition_tools import equi_split, equi_score_tree_edge_pair
import random
import networkx as nx
###Tree walk
    
def propose_step(graph,tree):
    '''
    this proposes a basis exchange move on the spanning trees
    definedin Broder //// also in /// (for matroid case)
    :graph: the ambient graph
    :tree: the current spanning tree
    
    Need to modify this so that it spits out a tree with appropriate directedness
    
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
    
    return nx.dfs_tree(new_tree, list(new_tree.nodes())[0]).reverse()


def equi_shadow_walk(graph, tree, num_blocks):
    '''
    Keeps walking on trees from current tree until it reaches a new tree that 
    has an equipartition
    
    :graph: the ambient graph
    :tree: the current tree
    :num_blocks: number of blocks
    '''
    
    while True:
        new_tree = propose_step(graph, tree)
        edges = equi_split(new_tree, num_blocks)
        if edges != None:
            return (new_tree, edges)
        
def test():
    graph = nx.grid_graph([10,10])
    tree = random_spanning_tree(graph)
    equi_shadow_walk(graph, tree, 2)
    
def shadow_walk(graph, tree,e, equi_partition = False, metropolis = False):
    '''
    Proposes a 
    
    '''
    n = len(e)
    U = propose_step(G,T)
    if equi_partition == False:
        e2 = random.sample(list(U.edges()),n)
    if equi == True:
        e2 = equi_split(G,T, n)
    if MH == True:
        current_score = 1 / likelihood_tree_edges_pair(G,T,e)
        new_score = 1 / likelihood_tree_edges_pair(G, U, e2)
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

