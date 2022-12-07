# be năm ❤xodă❤
# Created by Ali Heydari
class Vertex:
	label: int
	colour: int
	P: list[list[float]]  # self.P[c] is probability distribution function of self,  given that self's parent's colour is c
	# self.P[c][x] = P(self.colour == x | parent.colour == c)

	def __init__(self, label: int, colour: int = None):
		self.label = label
		self.colour = colour


class Edge:
	weight: float  # Mutual Information
	ends: set[Vertex, Vertex]

	def __init__(self, v: Vertex, u: Vertex, w: float = 1):
		self.weight = w
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


class RootedTree:
	root: Vertex
	V: list[Vertex] = []
	E: list[Edge] = []
	parent: dict[Vertex, Edge] = {}
	children: dict[Vertex, list[Edge]] = {}

	def __init__(self, root: Vertex):
		self.root = root
		self.V.append(root)

	def add_child(self, parent: Vertex, child: Vertex, weight: float):
		self.V.append(child)
		e = Edge(child, parent, weight)
		self.E.append(e)
		self.parent[child] = e
		self.children[parent].append(e)

	def construct_from(self, G: Graph):
		seen = {v: False for v in G.V}
		self.dfs(G, seen, self.root)

	def dfs(self, G: Graph, seen: dict[Vertex: bool], v: Vertex):
		for e in G.N[v]:
			u = e.opposite_end(v)
			if not seen[u]:
				seen[u] = True
				self.add_child(v, u, e.weight)
				self.dfs(G, seen, u)


def MST(G: Graph) -> RootedTree:
	pass

