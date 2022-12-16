# be năm ❤xodă❤
# Created by Ali Heydari
from graph.simple_graph import Vertex, Edge, Graph
import fibheap  # https://en.wikipedia.org/wiki/Fibonacci_heap


class MIEdge(Edge):
	weight: float
	"""mutual information"""

	def __init__(self, v: Vertex, u: Vertex | None, w: float):
		super().__init__(v, u)
		self.weight = w

	def __eq__(self, other):
		return self.weight == other.weight

	def __lt__(self, other):
		return self.weight > other.weight

	def __gt__(self, other):
		return self.weight < other.weight

	def __le__(self, other):
		return self.weight >= other.weight

	def __ge__(self, other):
		return self.weight <= other.weight


class MutualInformationGraph:
	V: list[Vertex]
	E: list[MIEdge]
	N: dict[Vertex, list[MIEdge]]

	def add_vertex(self):
		v = Vertex(len(self.V))
		self.V.append(v)
		self.N[v] = []
		return v

	def add_edge(self, e: MIEdge):
		self.E.append(e)
		v: Vertex
		u: Vertex
		v, u = e.ends
		self.N[v].append(e)
		self.N[u].append(e)

	def __init__(self, n: int, I: callable):
		self.V: list[Vertex] = []
		self.E: list[MIEdge] = []
		self.N: dict[Vertex, list[MIEdge]] = {}
		for i in range(n):
			self.add_vertex()
		for i in range(n):
			v = self.V[i]
			for j in range(i):
				u = self.V[j]
				self.add_edge(MIEdge(v, u, I(i, j)))

	def MST(self) -> Graph:
		"""https://en.wikipedia.org/wiki/Prim%27s_algorithm"""
		inf = float("inf")
		T = Graph(len(self.V))
		is_in_Q: dict[Vertex, bool] = {v: True for v in self.V}
		Q_dict: dict[Vertex, fibheap.Node] = {v: fibheap.Node(MIEdge(v, None, -inf)) for v in self.V}
		Q = fibheap.makefheap()
		for v in self.V:
			Q.insert(Q_dict[v])
		while Q.num_nodes > 0 and len(T.E) < len(T.V) - 1:
			e: MIEdge = fibheap.fheappop(Q)
			w = e.weight
			v, p = e.ends
			if v is None or not is_in_Q[v]:
				v, p = p, v
			Q_dict.pop(v)
			is_in_Q[v] = False
			if w != -inf:
				T.add_edge(Edge(T.V[v.id], T.V[p.id]))
			for e in self.N[v]:
				u = e.opposite_end(v)
				if is_in_Q[u] and e < Q_dict[u].key:
					Q.decrease_key(Q_dict[u], MIEdge(v, u, e.weight))
		return T
