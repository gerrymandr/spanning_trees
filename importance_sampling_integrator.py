# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 13:38:04 2018

@author: Lorenzo Najt
"""
from projection_tools import cut_edges
from main import explore_random
from Broder_Wilson_algorithms import random_spanning_tree_wilson
from projection_tools import remove_edges_map 
import random
import networkx as nx
from tree_tools import log_number_trees
import numpy as np
from point_process import make_graph, viz

class partition_class:
    def __init__(self, graph, partition, tree, edge,total_number_trees_edges_pairs):
        self.partition = partition
        self.tree = tree
        self.edge = edge
        self.graph = graph
        self.total_number_trees_edges_pairs = total_number_trees_edges_pairs
        
    def set_likelihood(self):
        total = 0
        for block in self.partition:
            total += log_number_trees(block) 
        connector_graph = nx.Graph()
        connector_graph.add_nodes_from(self.partition)
        for subgraph_1 in self.partition:
            for subgraph_2 in self.partition:
                if subgraph_1 != subgraph_2:
                    cutedges = cut_edges(graph, subgraph_1, subgraph_2)
                    if cutedges != []:
                        connector_graph.add_edge(subgraph_1, subgraph_2, weight = len(cutedges))
        cut_weight = log_number_trees(connector_graph, True)
        total += cut_weight
        self.likelihood = np.exp(total) / self.total_number_trees_edges_pairs
        self.connector_graph = connector_graph

def cut_size(partition):
    return np.exp(log_number_trees(partition.connector_graph, True))

def likelihood_function(partition):
    return partition.likelihood

def constant_function(partition):
    return 1


def total_variation(partition):
    return np.abs(partition.likelihood - 1 / partition.estimated_sample_space_size)

def integrate(list_of_partitions, function):
    total = 0
    for partition in list_of_partitions:
        total += function(partition) / partition.likelihood
    return total / len(list_of_partitions)


def make_partition_list(graph, number_samples = 100):
    
    #Note -- currently this is configured only for 2 partitions
    total_number_trees_edges_pairs = np.exp(log_number_trees(graph))*(len(graph.nodes()) - 1)
    
    uniform_trees = []
    for i in range(number_trees):
        uniform_trees.append(random_spanning_tree_wilson(graph))
        
    partitions = []
    for tree in uniform_trees:
        e = random.choice(list(tree.edges()))
        blocks = remove_edges_map(graph, tree, [e])
        new_partition = partition_class(graph, blocks, tree, e, total_number_trees_edges_pairs)
        new_partition.set_likelihood()
        partitions.append(new_partition)
    return partitions

def estimate_number_partitions(graph, partition_list):

    return integrate(partition_list, constant_function)

def expectation(graph, list_of_partitions, function):
    #This computes expectations against the tree measure

    total = 0
    for partition in list_of_partitions:
        total += function(partition)
    return total / len(list_of_partitions)

def make_histogram(graph, list_of_partitions, function):
    values = {}
    total_likelihood = 0
    for partition in list_of_partitions:
        values[function(partition)] = 0
        total_likelihood += 1
    for partition in list_of_partitions:
        values[function(partition)] += 1 / total_likelihood
    return values

def merge_historgrams(histogram_1, histogram_2):
    out = {}
    for key in histogram_1.keys():
        out[key] = 0
    for key in histogram_2.keys():
        out[key] = 0
    for key in out.keys():
        if key in histogram_1.keys():
            out[key] += histogram_1[key]
        if key in histogram_2.keys():
            out[key] += histogram_2[key]
    return out

def normalize_histogram(hist):
    total = 0
    for x in hist.keys():
        total += hist[x]
    for x in hist.keys():
        hist[x] = hist[x] / total
    return hist

#for m in range(2,10):
#    graph = nx.grid_graph([m*5,m*5])
#    #graph = make_graph(30*30,1)
#    partition_list = make_partition_list(graph, number_trees)
#    expectation(graph, partition_list, cut_size)
#    hist = make_histogram(graph, partition_list, cut_size)
#    plt.xlim(0,max(hist.keys()) + 1)
#    plt.bar(list(hist.keys()), hist.values(), color='g')
#    name = " grid_graph "  + "size: " + str( m*5) + "by" + str(m*5) +  " number_trees:" + str(number_trees)
#    plt.savefig(name)
#    print("made", name)
    
    
batch_number_trees = 1000
num_batches = 100
#Need to do it in batches to avoid heavy memory use
histograms = []

for m in range(10,11):
    histograms = []
    for i in range(num_batches):
        graph = make_graph((m*5)**2,1)
        partition_list = make_partition_list(graph, batch_number_trees)
        hist = make_histogram(graph, partition_list, cut_size)
        histograms.append(hist)
    hist = histograms[0]
    histograms.remove(hist)
    for histogram in histograms:
        hist = merge_historgrams(hist, histogram)
    hist = normalize_histogram(hist)
    plt.xlim(0,max(hist.keys()) + 1)
    plt.bar(list(hist.keys()), hist.values(), color='g')
    name = "poisson_triangulation "  + "size: " + str( (m*5)**2) +  " number_trees:" + str(batch_number_trees * num_batches)
    plt.savefig(name)
    print("made", name)

#Here's a practical issue - the numbers here are literally too big to do importance sampling with.

def test():
    number_trees = 10
    graph = nx.grid_graph([10,10])
    
    #For 10x10 grid, estimated sample space size using 30000 trees is:
    sample_size = 3.14529733509e+12
        
    
    total_number_trees_edges_pairs = np.exp(log_number_trees(graph))*(len(graph.nodes()) - 1)
        
    ongoing_partition_list = []
    for i in range(10):
        partition_list = make_partition_list(graph, number_trees)
        for partition in partition_list:
            partition.estimated_sample_space_size = sample_size
        ongoing_partition_list += partition_list
        #cut_total = integrate(partition_list, cut_size)
        #size_total = integrate(partition_list, constant_function)
        #likelihood = integrate(partition_list, likelihood_function)
        #print(total_number_trees_edges_pairs / size_total)
        #This computes the average likelihood T_A T_B cut(A,B)
        print(integrate(partition_list, total_variation))
        #print(cut_total/ size_total)
        #print(cut_total, size_total)
        
    print(estimate_number_partitions(graph, ongoing_partition_list))

#TODO -- figure out how to compute the distribution for divide and conquer
#
##Both of these estimators might be inconsistant. See here: https://stats.stackexchange.com/questions/367534/whats-the-best-estimator-for-expectation-if-we-can-draw-samples-iid-and-we-kn
#def expectation(graph, list_of_partitions, function):
#    #This computes expectations against the tree measure
#
#    total = 0
#    total_likelihood = 0
#    for partition in list_of_partitions:
#        total += function(partition) * partition.likelihood
#        total_likelihood += partition.likelihood
#    return total / total_likelihood
#
#def make_histogram(graph, list_of_partitions, function):
#    values = {}
#    total_likelihood = 0
#    for partition in list_of_partitions:
#        values[function(partition)] = 0
#        total_likelihood += partition.likelihood
#    for partition in list_of_partitions:
#        values[function(partition)] += function(partition)*partition.likelihood / total_likelihood
#    return values
