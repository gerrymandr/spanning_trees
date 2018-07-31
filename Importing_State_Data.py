# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 10:39:18 2018

@author: MGGG
"""

from main import explore_random, total_pop

import json
import networkx as nx

state = "55"

with open("../vtd-adjacency-graphs/vtd-adjacency-graphs/"+str(state)+"/rook.json") as f:
    data = json.load(f)

graph = nx.readwrite.json_graph.adjacency_graph(data)

import glob
import pandas as pd

allFiles = glob.glob("../redistricting/adjacency_matrix_demo/spatial_indexes/"+str(state)+"_*_idx.txt")
frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=None)
    list_.append(df)
frame = pd.concat(list_)

df = frame.rename(index=str, columns={0 : "GEOID", 1: "xaxis", 2:"yaxis"})
pos = df.set_index('GEOID').T.to_dict('list')
pos = {str(i) : (pos[i][0], pos[i][1]) for i in pos.keys()}

node_list = list(graph.nodes())
for node in node_list:
    try:
        graph.nodes[node]["geopos"] = pos[str(node)]
    except:
        exception = node
        print(node, type(node))
        print(graph.nodes[node])

import matplotlib.pyplot as plt
#
#plt.figure(figsize = (10,7))
#nx.draw(graph, pos = pos, node_size=0)
#
#print(len(graph))
#
#
parts = explore_random(graph, 2, 2, pictures = True, divide_and_conquer=False,with_walk = False, delta = .005)

#populations = [total_pop]

#WHy do they still look compact? here are the node sizes for ten runs of wisconsin.

#list_of_sizes = [[466, 602, 724, 687, 1123, 1146, 944, 598], [448, 438, 808, 1036, 1063, 703, 1132, 662],[431, 628, 643, 996, 1257, 897, 729, 709], [478, 464, 722, 1156, 721, 699, 972, 1078], [507, 408, 769, 817, 1167, 703, 907, 1012],[504, 486, 769, 777, 1234, 731, 702, 1087],  [449, 435, 973, 1087, 1081, 830, 692, 743], [502, 447, 704, 1029, 1246, 853, 784, 725], [434, 607, 596, 825, 1133, 727, 881, 1087], [438, 636, 667, 903, 711, 1214, 675, 1046]]
#
#sorted_sizes = [np.sort(sizes) for sizes in list_of_sizes]
#
#[array([ 466,  598,  602,  687,  724,  944, 1123, 1146]),
# array([ 438,  448,  662,  703,  808, 1036, 1063, 1132]),
# array([ 431,  628,  643,  709,  729,  897,  996, 1257]),
# array([ 464,  478,  699,  721,  722,  972, 1078, 1156]),
# array([ 408,  507,  703,  769,  817,  907, 1012, 1167]),
# array([ 486,  504,  702,  731,  769,  777, 1087, 1234]),
# array([ 435,  449,  692,  743,  830,  973, 1081, 1087]),
# array([ 447,  502,  704,  725,  784,  853, 1029, 1246]),
# array([ 434,  596,  607,  727,  825,  881, 1087, 1133]),
# array([ 438,  636,  667,  675,  711,  903, 1046, 1214])]

#This partially explains it -- the distribution of sizes of the districts tends to be fairly uniform...so for the mth district, it must be appx size X, and among all districts of size X, it favors the (larger) ones with smaller perimeter... but they cannot all be uniformly larger, so overall it is the perimeter that makes the decision...?