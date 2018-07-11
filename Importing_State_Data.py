# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 10:39:18 2018

@author: MGGG
"""

from main import explore_random

import json
import networkx as nx

state = 19

with open("../vtd-adjacency-graphs-master/vtd-adjacency-graphs/"+str(state)+"/rook.json") as f:
    data = json.load(f)

graph = nx.readwrite.json_graph.adjacency_graph(data)

import glob
import pandas as pd

allFiles = glob.glob("../zach_graphs/spatial_indexes/"+str(state)+"_*_idx.txt")
frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=None)
    list_.append(df)
frame = pd.concat(list_)

df = frame.rename(index=str, columns={0 : "GEOID", 1: "xaxis", 2:"yaxis"})
pos = df.set_index('GEOID').T.to_dict('list')
pos = {str(i) : (pos[i][0], pos[i][1]) for i in pos.keys()}

for node in graph.nodes():
    graph.nodes[node]["geopos"] = pos[node]

import matplotlib.pyplot as plt

plt.figure(figsize = (10,7))
nx.draw(graph, pos = pos, node_size=0)


explore_random(graph, 1, 4, pictures = True, divide_and_conquer=True)