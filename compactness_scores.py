#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 10:03:22 2018

@author: Eduardo & Natalia
Here we implement several spectral & discrete compactness score.
"""

import networkx as nx
import numpy as np


def first_evalue(H):
    spectrum = nx.laplacian_spectrum(H)

    return spectrum[1]


def heat_kernel(H,t):
    e_values = nx.laplacian_spectrum(H)
    np.delete(e_values, 0)
    exp = [np.exp((-e_value)*t) for e_value in e_values]

    return np.sum(exp)


def log_span_trees(H):
    spectrum = nx.laplacian_spectrum(H)
    non_zero_spect = np.delete(spectrum, 0)

    return np.sum(np.log(non_zero_spect))
    

def discrete_pp(G,H,boundary_nodes):
    # Adding a supernode for proper perimeter calculation
    # Name of the supernode is -1
    boundary_edges = [(-1, node) for node in G.nodes if boundary_nodes[node] is True]
    G.add_edges_from(boundary_edges)

    nodes_H = {node for node in H.nodes}
    perimeter = nx.cut_size(G, nodes_H)
    area = len(H.nodes())
    # Remove supernode as to not alter the graph G
    G.remove_node(-1)
    
    return (perimeter**2)/area
