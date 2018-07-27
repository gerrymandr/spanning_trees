# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 20:58:10 2018

@author: MGGG
"""

from tree_tools import log_number_trees
from projection_tools import remove_edges_map
from visualization_tools import visualize_partition
import networkx as nx
from random import shuffle
from random import uniform, choice
import numpy as np
#https://homes.cs.washington.edu/~shayan/courses/cse599/adv-approx-4.pdf for why effective resistance computes prob


def kirkoff_sampler(graph):
    size = len(graph) - 1
    T = []
    edge_list = list(graph.edges())
    edge = edge_list[0]
    shuffle(edge_list)
    while len(T) <= size - 1:
        edge = choice(list(graph.edges()))
        H = nx.contracted_edge(graph, edge)
        p = np.exp(log_number_trees(H)) / np.exp(log_number_trees(graph))
        print(p)
        c = uniform(0,1)
        if c <= p:
            T.append(edge)
            graph = nx.contracted_edge(graph, edge, self_loops=False)
        else:
            graph.remove_edge(edge[0], edge[1])
    tree = nx.Graph()
    tree.add_edges_from(T)
    return tree

def visualize(graph, partition):
    for i in range(len(partition)):
        for vertex in partition[i].nodes():
            graph.nodes[vertex]["district"] = i + 1
            graph.nodes[vertex]["pos"] = vertex

    color_map = {i : i for i in range(100)}
    node_colors = [color_map[graph.nodes[vertex]["district"] ] for vertex in graph.nodes()]

    import matplotlib.pyplot as plt
    nx.draw(graph, pos=nx.get_node_attributes(graph, 'pos'), cmap=plt.get_cmap('jet'), node_color=node_colors, node_size = 20, width = .5)

def kirkoff_inverse_sampler(graph):

    size = len(graph) - 1
    T = []
    edge_list = list(graph.edges())
    edge = edge_list[0]
    shuffle(edge_list)
    while len(T) <= size - 1:
        print("T currently", len(T))
        edge = choice(list(graph.edges()))
        total_inverse = 0
        for edge in list(graph.edges()):
            H = nx.contracted_edge(graph, edge)
            p = np.exp(log_number_trees(H)) / np.exp(log_number_trees(graph))
            #Replace this with a computation of effective resistance!
            #You also don't need to compute this so many times!
            total_inverse += 1/p
        edge = choice(list(graph.edges()))
        H = nx.contracted_edge(graph, edge)
        q = np.exp(log_number_trees(H)) / np.exp(log_number_trees(graph))
        p = (1 / q) / total_inverse
        print(p, q, total_inverse)
        c = uniform(0,1)
        if c <= p:
            T.append(edge)
            graph = nx.contracted_edge(graph, edge, self_loops=False)
        else:
            if q < .999999:
                graph.remove_edge(edge[0], edge[1])
    tree = nx.Graph()
    tree.add_edges_from(T)
    edge = T[0]
    return (tree, edge)

m = 6
graph = nx.grid_graph([m,m])
tree, edge = kirkoff_inverse_sampler(graph)

nx.draw(tree)

partition = remove_edges_map(graph, graph, [edge])
visualize(graph, partition)
????
