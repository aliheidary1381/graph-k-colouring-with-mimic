# be năm ❤xodă❤
# Created by Ali Heydari
from graph import Vertex, Edge, Graph, ColouredVertex, EdgeForColoured, ColouredGraph
import random


class DVertex(Vertex):
	P: list[list[float]]  # self.P[c] is probability distribution function of self,  given that self's parent's colour is c
	# self.P[c][x] = P(self.colour == x | parent.colour == c)
	eP: list[float]  # ep[c] = empirical probability that self's colour is c


class DEdge:
	ends: set[DVertex, DVertex]

	def __init__(self, v: DVertex, u: DVertex):
		self.ends = {v, u}

	def opposite_end(self, v: DVertex) -> DVertex:
		u1, u2 = self.ends
		if v == u1:
			return u2
		elif v == u2:
			return u1


class DTree:  # dependency graph + tree structure
	root: DVertex
	V: list[DVertex] = []
	E: list[DEdge] = []
	parent: dict[DVertex, DEdge | None] = {}
	children: dict[DVertex, list[DEdge]] = {}

	def add_edge(self, parent: DVertex, child: DVertex):
		e = DEdge(child, parent)
		self.E.append(e)
		self.parent[child] = e
		self.children[parent].append(e)
		self.children[child] = []

	def __init__(self, G: Graph = None):
		self.root = DVertex(0)  # TODO
		self.V.append(self.root)
		self.children[self.root] = []
		self.parent[self.root] = None
		if G is None:
			return
		for i in range(1, len(G.V)):
			self.V.append(DVertex(i))
		seen = {v: False for v in self.V}
		self.init_dfs(G, seen, self.root)

	def init_dfs(self, G: Graph, seen: dict[DVertex: bool], v: DVertex):
		seen[v] = True
		for e in G.N[G.V[v.id]]:
			u = e.opposite_end(v)  # in G
			u = self.V[u.id]  # in self
			if not seen[u]:
				self.add_edge(v, u)
				self.init_dfs(G, seen, u)

	def sample(self, Gin: Graph) -> ColouredGraph:
		Gout = ColouredGraph(Gin)
		Gout.V[self.root.id].colour = random.choices([c for c in range(len(self.root.eP))], weights=self.root.eP)[0]
		self.sample_dfs(Gout, self.root)
		return Gout

	def sample_dfs(self, Gout: ColouredGraph, v: DVertex):
		for e in self.children[v]:
			u = e.opposite_end(v)
			Gout.V[u.id].colour = random.choices([c for c in range(len(u.P[Gout.V[v.id].colour]))], weights=u.P[Gout.V[v.id].colour])[0]
			self.sample_dfs(Gout, u)
