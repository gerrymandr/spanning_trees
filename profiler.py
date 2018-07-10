#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 14:03:15 2018

@author: edu
"""

from main import explore_random

import networkx
import json
import networkx as nx

state = "33"


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

explore_random(graph, 1, 3, pictures = True)