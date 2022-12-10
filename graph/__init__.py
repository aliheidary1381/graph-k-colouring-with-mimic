from coloured_graph import *
from graphical_mutual_information import *
from dependency_tree import *


class Vertex:
	id: int  # Vertex's index in G.V

	def __init__(self, label: int):
		self.id = label


class Edge:
	ends: set[Vertex, Vertex]

	def __init__(self, v: Vertex, u: Vertex):
		self.ends = {v, u}

	def opposite_end(self, v: Vertex) -> Vertex:
		u1, u2 = self.ends
		if v == u1:
			return u2
		elif v == u2:
			return u1


class Graph:
	V: list[Vertex] = []
	E: list[Edge] = []
	N: dict[Vertex, list[Edge]] = {}

	def add_vertex(self):
		v = Vertex(len(self.V))
		self.V.append(v)
		self.N[v] = []
		return v

	def add_edge(self, e: Edge):
		self.E.append(e)
		v: Vertex
		u: Vertex
		v, u = e.ends
		self.N[v].append(e)
		self.N[u].append(e)
