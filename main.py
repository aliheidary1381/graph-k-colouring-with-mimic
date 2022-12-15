import math

from graph import *


class MIMIC:
	initial_population: int = 50
	reproduction_rate: float = 1
	death_rate: float = 0.5
	k: int
	G: Graph  # len(V) = n
	_model: DTree
	_current_generation: list[ColouredGraph]  # len = t

	def run(self) -> ColouredGraph:
		while self._current_generation[0].fitness() != len(self.G.E):
			self.select_best()  # O(t lg t)
			self.update_model()  # O(tn^2)
			self.produce_new_generation()  # O(tn)
		return self._current_generation[0]

	def produce_new_generation(self):
		sampling_ratio = self.reproduction_rate
		cnt = round(len(self._current_generation) * sampling_ratio)
		self._current_generation += [self._model.sample(self.G) for _ in range(cnt)]

	def select_best(self):
		survival_rate = 1 - self.death_rate
		cnt = round(len(self._current_generation) * survival_rate)
		self._current_generation.sort(key=lambda G: G.fitness(), reverse=True)
		self._current_generation = self._current_generation[:cnt]

	def update_model(self):
		gmi = MIGraph(len(self.G.V), self.I)
		T = gmi.MST()
		self._model = DTree(T, self.eP, self.cP)

	def eP(self, vid: int) -> list[float]:
		eP = [0 for _ in range(self.k)]
		for G in self._current_generation:
			eP[G.V[vid].colour] += 1
		den = len(self._current_generation)
		return [cnt / den for cnt in eP]

	def cP(self, parent_id: int, child_id: int) -> list[list[float]]:
		P = [[0 for _ in range(self.k)] for _ in range(self.k)]
		for G in self._current_generation:
			P[G.V[parent_id].colour][G.V[child_id].colour] += 1
		count_sum = [max(1, sum(P[colour])) for colour in range(self.k)]
		return [[P[i][j] / count_sum[i] for j in range(self.k)] for i in range(self.k)]

	def I(self, vid: int, uid: int) -> float:
		Pvu = [[0 for _ in range(self.k)] for _ in range(self.k)]
		Pv = [0 for _ in range(self.k)]
		Pu = [0 for _ in range(self.k)]
		for G in self._current_generation:
			Pvu[G.V[vid].colour][G.V[uid].colour] += 1
			Pv[G.V[vid].colour] += 1
			Pu[G.V[uid].colour] += 1
		den = len(self._current_generation)
		ans = 0
		for cv in range(self.k):
			for cu in range(self.k):
				ans += Pvu[cv][cu] / den * math.log(max(1, Pvu[cv][cu]) * den / max(1, Pv[cv] * Pu[cu]))
		return ans

	def __init__(self, k: int, G: Graph):
		self.k = k
		self.G = G

		def eP(_):
			return [1 / k for _ in range(k)]

		def cP(_, __):
			return [[1 / k for _ in range(k)] for _ in range(k)]

		def I(vid, uid):
			return len(G.N[G.V[vid]]) + len(G.N[G.V[uid]])

		gmi = MIGraph(len(G.V), I)
		T = gmi.MST()
		self._model = DTree(T, eP, cP)
		self._current_generation = [self._model.sample(self.G) for _ in range(self.initial_population)]


def solve(k: int, G: Graph) -> ColouredGraph:
	return MIMIC(k, G).run()


solution = solve(3, Petersen)

print("vertices' colours are:", end=' ')
for x in solution.V:
	print(x.colour, end=' ')
