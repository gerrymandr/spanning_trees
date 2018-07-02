#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 14:08:00 2018

@author: Eduardo
"""
import networkx as nx
from random import choice

def tree_edges_generation(G, size = "all"):
    """Returns a set with the edges visited in the random walk."""

    if not nx.is_connected(G) and size == "all":
        return "Graph not connected, the algorithm will never end."

    all_nodes = set(list(G.nodes()))
    edge_set = set()
    node_set = set()

    initial_node = choice((list(G.nodes())))
    node_set.add(initial_node)
    node = initial_node

    while node_set != all_nodes:
        neigh = nx.all_neighbors(G, node)
        rnd_neigh = choice(list(neigh))
        # Only adds edges if it's the first time we visit new node
        if rnd_neigh not in node_set:
            edge = frozenset([node, rnd_neigh])
            edge_set.add(edge)
        node_set.add(rnd_neigh)
        if len(node_set) == size:
            return edge_set

        node = rnd_neigh
    return edge_set





def subgraph_from_edges(G, edge_set):
    """Creates nx subgraph from set of edges."""
    edge_list = list(edge_set)
    nodes = set()
    for edge in edge_list:
        nodes =  nodes.union(edge)
    
    T = nx.subgraph(G, nodes)
    return T


def connected_subgraph_sampler(G, size = "all"):
    """Returns a uniformly random spanning tree of G."""
    edges = tree_edges_generation(G, size = size)
    T = subgraph_from_edges(G, edges)
    return T