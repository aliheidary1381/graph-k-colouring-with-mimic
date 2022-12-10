# be năm ❤xodă❤
# Created by Ali Heydari
from graph import Vertex, Edge, Graph, DTree


class MIEdge(Edge):
	weight: float  # Mutual Information

	def __init__(self, v: Vertex, u: Vertex, w: float = 1):
		super().__init__(v, u)
		self.weight = w


class MIGraph(Graph):
	E: list[MIEdge] = []
	N: dict[Vertex, list[MIEdge]] = {}

	def add_edge(self, e: MIEdge):
		self.E.append(e)
		v: Vertex
		u: Vertex
		v, u = e.ends
		self.N[v].append(e)
		self.N[u].append(e)

	def __init__(self, n: int):  # complete graph with n vertices
		for i in range(n):
			v = self.add_vertex()
			for u in self.V[:-1]:
				self.add_edge(MIEdge(v, u))


def MST(G: MIGraph) -> DTree:
	pass
