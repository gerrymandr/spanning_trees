# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 12:21:16 2018

@author: MGGG
"""
'''
Goals: make a Sampler which will be populated by many Trees
'''
class Sampler:
    '''    This allows for easy sampling by storing all desired sampling parametrics.
    '''
    def __init__(self, graph, num_partitions, num_blocks, trees, sampling_function):
        '''
        :graph: the map graph
        :num_partitions: number of partitions/districts
        :num_blocks: number of blocks in each map
        :trees: list of trees
        :sampling_function: method of partition sampling (takes in TODO)
        '''
        self.graph = graph
        self.num_partitions = num_partitions
        self.num_blocks = num_blocks
        self.trees = trees
        self.sampling_function = sampling_function
        self.working_subgraph = graph
        self.old_pairs = []
        #self.current_pair = Tree_Partition_Pair(TODO)

    def set_working_subgraph(self, subgraph):
        self.working_subraph = subgraph
    
    def update_pair(self, new_pair): # TODO
        self.old_pairs.append(self.current_pair)
        self.current_pair = new_pair



class Tree_Partition_Pair:
    '''
    This is meant to be an extension of a networkx graph to keep track of root and topological ordering.
    '''
    def __init__(self, root, topological_ordering, partition):
        '''
        :root:
        :topological_ordering:
        :partition
        '''
        self.root = root
        self.topological_ordering = topological_ordering
        self.partition = partition
