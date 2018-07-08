# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 16:31:04 2018

@author: MGGG

"""
import networkx as nx

import matplotlib.pyplot as plt
def visualize_partition(graph, partition):
    for i in range(len(partition)):
        for vertex in partition[i].nodes():
            graph.nodes[vertex]["district"] = i
            graph.nodes[vertex]["pos"] = vertex
    for edge in graph.edges():
        graph.edges[edge]["tree"] = 0
    color_map = {i : i for i in range(100)}
    node_colors = [color_map[graph.nodes[vertex]["district"] ] for vertex in graph.nodes()]
    edge_colors = [graph.edges[edge]["tree"] for edge in graph.edges()]
    nx.draw(graph, pos=nx.get_node_attributes(graph, 'pos'), cmap=plt.get_cmap('jet'), node_color=node_colors, edge_color=edge_colors, node_size = 10)
    plt.show()
    
def visualize_partition_and_tree(graph, partitoin, tree):
    for i in range(len(partition)):
        for vertex in partition[i].nodes():
            graph.nodes[vertex]["district"] = i
            graph.nodes[vertex]["pos"] = vertex
    for edge in graph.edges():
        graph.edges[edge]["tree"] = 0
    for edge in tree.edges():
        graph.edges[edge]["tree"] = 1
    color_map = {i : i for i in range(100)}
    node_colors = [color_map[graph.nodes[vertex]["district"] ] for vertex in graph.nodes()]
    edge_colors = [graph.edges[edge]["tree"] for edge in graph.edges()]
    nx.draw(graph, pos=nx.get_node_attributes(graph, 'pos'), cmap=plt.get_cmap('jet'), node_color=node_colors, edge_color=edge_colors)
    plt.show()
    