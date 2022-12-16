from graph.simple_graph import *
from graph.coloured_graph import *
from graph.dependency_tree import *
from graph.graphical_mutual_information import *

# exemplar
Petersen = Graph(10)
"""https://en.wikipedia.org/wiki/Petersen_graph"""
Petersen.add_edge(Edge(Petersen.V[0], Petersen.V[1]))
Petersen.add_edge(Edge(Petersen.V[1], Petersen.V[2]))
Petersen.add_edge(Edge(Petersen.V[2], Petersen.V[3]))
Petersen.add_edge(Edge(Petersen.V[3], Petersen.V[4]))
Petersen.add_edge(Edge(Petersen.V[4], Petersen.V[0]))
Petersen.add_edge(Edge(Petersen.V[5], Petersen.V[6]))
Petersen.add_edge(Edge(Petersen.V[6], Petersen.V[7]))
Petersen.add_edge(Edge(Petersen.V[7], Petersen.V[8]))
Petersen.add_edge(Edge(Petersen.V[8], Petersen.V[9]))
Petersen.add_edge(Edge(Petersen.V[9], Petersen.V[5]))
Petersen.add_edge(Edge(Petersen.V[0], Petersen.V[5]))
Petersen.add_edge(Edge(Petersen.V[1], Petersen.V[7]))
Petersen.add_edge(Edge(Petersen.V[2], Petersen.V[9]))
Petersen.add_edge(Edge(Petersen.V[3], Petersen.V[6]))
Petersen.add_edge(Edge(Petersen.V[4], Petersen.V[8]))
