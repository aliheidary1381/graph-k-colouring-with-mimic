# be năm ❤xodă❤
# Created by Ali Heydari
from graph.simple_graph import Vertex, Graph
from graph.coloured_graph import ColouredGraph
import random


class DVertex(Vertex):
	P: list[float]
	"""ep[c] = P(self.colour = c)"""
	cP: list[list[float]]
	"""self.ecP[c][x] = P(self.colour = x | parent.colour = c)"""

	def __init__(self, label: int):
		super().__init__(label)
		self.P: list[float] | None = None
		self.cP: list[list[float]] | None = None


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


class DependencyTree:
	root: DVertex
	V: list[DVertex]
	E: list[DEdge]
	parent: dict[DVertex, DEdge | None]
	children: dict[DVertex, list[DEdge]]

	def add_edge(self, parent: DVertex, child: DVertex):
		e = DEdge(child, parent)
		self.E.append(e)
		self.parent[child] = e
		self.children[parent].append(e)
		self.children[child] = []

	def __init__(self, G: Graph, P: callable, cP: callable):
		self.root = DVertex(0)  # any vertex is admissible
		self.root.P = P(self.root.id)
		self.V: list[DVertex] = [self.root]
		self.E: list[DEdge] = []
		self.parent: dict[DVertex, DEdge | None] = {self.root: None}
		self.children: dict[DVertex, list[DEdge]] = {self.root: []}
		for i in range(1, len(G.V)):
			self.V.append(DVertex(i))
		seen = {v: False for v in self.V}
		self.init_dfs(G, seen, cP, self.root)

	def init_dfs(self, G: Graph, seen: dict[DVertex: bool], cP: callable, v: DVertex):
		seen[v] = True
		for e in G.N[G.V[v.id]]:
			u = e.opposite_end(G.V[v.id])  # in G
			u = self.V[u.id]  # in self
			if not seen[u]:
				self.add_edge(v, u)
				u.cP = cP(v.id, u.id)
				self.init_dfs(G, seen, cP, u)

	def sample(self, Gin: Graph) -> ColouredGraph:
		Gout = ColouredGraph(Gin)
		k = len(self.root.P)
		cp = [colour for colour in range(k)]
		Gout.V[self.root.id].colour = random.choices(cp, weights=self.root.P)[0]
		self.sample_dfs(Gout, cp, self.root)
		return Gout

	def sample_dfs(self, Gout: ColouredGraph, cp: list[int], v: DVertex):
		for e in self.children[v]:
			u = e.opposite_end(v)
			Gout.V[u.id].colour = random.choices(cp, weights=u.cP[Gout.V[v.id].colour])[0]
			self.sample_dfs(Gout, cp, u)
