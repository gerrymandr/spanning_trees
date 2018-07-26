# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 22:15:36 2018

@author: MGGG
"""

from tree_tools import log_number_trees
import networkx as nx

def boundary_perimeter(graph):
    #Given a subgraph of the grid graph, as a collection of nodes of the form $(i,j)$, returns the perimeter of that subgraph.
    
    graph_nodes = list(graph.nodes())
    boundary_nodes = [node for node in graph_nodes if graph.degree(node) < 4]
    return len(boundary_nodes)

def edge_perimeter(graph):
    #for grid graphs
    num_edges = len(list(graph.edges()))
    num_nodes = len(list(graph.nodes()))
    return 4*num_nodes - 2*num_edges
    #4V - P = 2E, so P = 4*V- 2E ... this is only for grid graphs
    
    
def refinement(graph):
    #Given a subgraph of the grid graph, in the form (i,j), compute the refinement at double the scale.
    #is this really the right kind of refinement?
    
    #The right kind of refinement is the refinement corresponding to epsilon -> epsilon/2 and the shape staying the same.... maybe this isn't well defined just in terms of the graph, because it could very well also depend on the specific hoice of shape used to cut out tha grap.
    
    #This code does htis procedure in the case that the vertices of the shape are also vertices for graph.
    #graph = nx.grid_graph([2,2])
    graph_nodes = list(graph.nodes())
    shifted_nodes = [ (node[0] + 1, node[1] + 1) for node in graph_nodes]
    x_coords = [node[0] for node in graph_nodes]
    y_coords = [node[1] for node in graph_nodes]
    x_min = min(x_coords) - 1
    x_max = max(x_coords) + 1
    y_min = min(y_coords) - 1
    y_max = max(y_coords) + 1
    
    ambient_graph = nx.grid_graph([2*x_max+ 100, 2*y_max + 100])
    rescaled_nodes = set([ (2*node[0], 2*node[1]) for node in shifted_nodes])
    new_nodes = set([])
    
    for x in ambient_graph.nodes():
        if ((x[0] - 1, x[1]) in rescaled_nodes) and ( ( x[0] + 1, x[1]) in rescaled_nodes) :
            new_nodes.add(x)
        if ( ( x[0], x[1] + 1) in rescaled_nodes) and ( ( x[0], x[1] - 1) in rescaled_nodes):
            new_nodes.add(x)
        if ( ( x[0] - 1, x[1] - 1) in rescaled_nodes) and ( (x[0] - 1, x[1] + 1) in rescaled_nodes) and ( (x[0] + 1, x[1] -1 ) in rescaled_nodes) and ( (x[0] + 1, x[1] + 1) in rescaled_nodes):
            new_nodes.add(x)
    new_nodes = new_nodes.union(rescaled_nodes)
    new_graph= nx.subgraph(ambient_graph, new_nodes)
    
    return new_graph

def subdivision_refinement(graph):
    #This refinement breaks each square in the subgraph into 4 new squares.... I think 

def plot_test(graph):
    for vertex in graph:
            graph.nodes[vertex]["pos"] = vertex
    nx.draw(graph, pos=nx.get_node_attributes(graph, 'pos'), labels = nx.get_node_attributes(graph, 'pos'))
    
def compare(shape_1, shape_2, num = 7):
    '''compares the number of spanning trees in the two shapes under
    sequential refinement'''
    spanning_trees = []
    for i in range(num):
        sp_1 = log_number_trees(shape_1)
        sp_2 = log_number_trees(shape_2)
        spanning_trees.append([sp_1, sp_2])
        print( len( list(shape_1.nodes())), len(list(shape_2.nodes())))
        shape_1 = refinement(shape_1)
        shape_2 = refinement(shape_2)
    return spanning_trees

    
rectangle = nx.grid_graph([2,5])
square = nx.grid_graph([3,3])
big_square = nx.grid_graph([4,4])
new_nodes = list(square.nodes())
new_nodes.append( (3,0) )
square_with_child = nx.subgraph(big_square, new_nodes)
#plot_test(square_with_child)
refined = refinement(rectangle)
plot_test(refined)
plot_test(rectangle)
compare(square_with_child, rectangle)
print("Is this working right?")
#    
# [[5.257495372027781, 5.342334251964811],
# [20.139095026954607, 10.319067994385385],
# [78.10476660047742, 29.935803013616148],
# [306.26374953371106, 97.27766394968938]]
    
#You can see the rectangle star tout ahead of the square_with_child, and then start to lose to it as we refine the shape. This indicates that there isn't a general theorem. (And in fact this intuition about refinment is in general wrong. Perhaps it is right for rectangles though...)
    


m = 6
a = 1
b = 2
compare(nx.grid_graph([a*m,int(m/a)]), nx.grid_graph([b*m,int(m/b)]))
