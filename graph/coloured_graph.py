# be năm ❤xodă❤
# Created by Ali Heydari
from graph import Vertex, Edge, Graph


class ColouredVertex(Vertex):
	colour: int

	def __init__(self, label: int, colour=None):
		super().__init__(label)
		self.colour = colour


class EdgeForColoured(Edge):
	ends: set[ColouredVertex, ColouredVertex]

	def __init__(self, v: ColouredVertex, u: ColouredVertex):
		super().__init__(v, u)

	def opposite_end(self, v: ColouredVertex) -> ColouredVertex:
		u1, u2 = self.ends
		if v == u1:
			return u2
		elif v == u2:
			return u1

	@property
	def weight(self) -> bool:
		v: ColouredVertex
		u: ColouredVertex
		v, u = self.ends
		return v.colour == u.colour


class ColouredGraph(Graph):
	V: list[ColouredVertex] = []
	E: list[EdgeForColoured] = []
	N: dict[ColouredVertex, list[EdgeForColoured]] = {}

	def __init__(self, G: Graph=None):
		for v in G.V:
			self.add_vertex()
		for e in G.E:
			v, u = e.ends
			self.add_edge(EdgeForColoured(self.V[v.id], self.V[u.id]))

	def add_vertex(self):
		v = ColouredVertex(len(self.V))
		self.V.append(v)
		self.N[v] = []
		return v

	def add_edge(self, e: EdgeForColoured):
		self.E.append(e)
		v: ColouredVertex
		u: ColouredVertex
		v, u = e.ends
		self.N[v].append(e)
		self.N[u].append(e)

	def count_neighbors_with_same_colour(self):
		sum(e.weight for e in self.E)
