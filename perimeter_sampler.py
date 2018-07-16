# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 17:58:52 2018

@author: MGGG
"""

import networkx as nx
import random
graph = nx.triangular_lattice_graph(20,20)

s = (10,10)


def next_step(graph, start_node, current_node, steps_remaining):
    d = nx.shortest_path_length(graph, current_node, start_node)
    if d > steps_remaining:
        return None
    else:
        options = list(graph.neighbors(current_node))
        return random.choice(options)
    option_distances = {}
    for option in options:
        option_distances[option] = nx.shortest_path_length(graph, option, start_node)
 

def simple_random_loop(graph, start_node, length):

    current_node = random.choice(list(graph.neighbors(start_node)))
    path = [start_node, current_node]
    path_length = 2
    while path[-1] != start_node:
        proposal = next_step(graph, start_node, current_node, length - path_length)
        while proposal not in path:
            proposal = next_step(graph, start_node, current_node, length - path_length)
        path.append(proposal)
        current_node = proposal
        path_length += 1
        if proposal == None:
            return None
    return path
    if path_length == length:
        return path
    else:
        return None
        
loops = []
counter = 0
while counter < 100:
    candidate_path = simple_random_loop(graph, s, 100)
    if candidate_path != None:
        loops.append(candidate_path)
        counter += 1