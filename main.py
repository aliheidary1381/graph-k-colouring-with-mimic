import math

from graph import *


class MIMIC:
	"""
	mutual information maximizing input clustering
	"""
	initial_population: int = 50
	death_rate: float = 0.5
	birth_rate: float = 1
	k: int
	G: Graph  # len(V) = n
	Pt: list[ColouredGraph]  # len = N
	"""population at current generation t"""
	t: int = 0  # generation #

	def run(self) -> ColouredGraph:
		while C(self.Pt[0]) > 0:
			self.Pt += self.beta_mu(self.alpha_MIMIC(self.S(self.Pt)))
			self.t += 1
		return self.Pt[0]

	def beta_mu(self, model: DependencyTree) -> list[ColouredGraph]:
		"""
		β_μ = sampling operator ∈ O(Nn)

		Generate more samples from the distribution p^{θ_t}.
		"""
		sampling_ratio = self.birth_rate
		cnt = round(len(self.Pt) * sampling_ratio)
		# model ≈ p^{θ_t}
		return [model.sample(self.G) for _ in range(cnt)]

	def S(self, population: list[ColouredGraph]) -> list[ColouredGraph]:
		"""
		S = selection operator ∈ O(N lg N)

		Set θ_{t + 1} equal to the Nth percentile of the data.
		Retain only the points less than θ_{t + 1}.
		"""
		survival_rate = 1 - self.death_rate  # survival_rate ∝ N
		cnt = round(len(population) * survival_rate)  # Nth percentile
		population.sort(key=C)
		# θ_{t + 1} = population[cnt]
		return population[:cnt]

	def alpha_MIMIC(self, sample: list[ColouredGraph]) -> DependencyTree:
		"""
		α_MIMIC = model-building operator ∈ O(N n^2)

		Update the parameters of density estimator of p^{θ_t} from a sample.
		"""
		self.Pt = sample
		gmi = MutualInformationGraph(len(self.G.V), self.I)
		T = gmi.MST()
		return DependencyTree(T, self.eP, self.ecP)  # ≈ p^{θ_t}

	def eP(self, vid: int) -> list[float]:
		"""
		empirical (unconditional) probability
		"""
		eP = [0 for _ in range(self.k)]
		for G in self.Pt:
			eP[G.V[vid].colour] += 1
		t = len(self.Pt)
		return [cnt / t for cnt in eP]

	def ecP(self, parent_id: int, child_id: int) -> list[list[float]]:
		"""
		empirical conditional probability
		"""
		P = [[0 for _ in range(self.k)] for _ in range(self.k)]
		for G in self.Pt:
			P[G.V[parent_id].colour][G.V[child_id].colour] += 1
		count_sum = [max(1, sum(P[colour])) for colour in range(self.k)]
		return [[P[i][j] / count_sum[i] for j in range(self.k)] for i in range(self.k)]

	def I(self, vid: int, uid: int) -> float:
		"""
		mutual information

		https://en.wikipedia.org/wiki/Mutual_information#In_terms_of_PMFs_for_discrete_distributions
		"""
		Pvu = [[0 for _ in range(self.k)] for _ in range(self.k)]
		Pv = [0 for _ in range(self.k)]
		Pu = [0 for _ in range(self.k)]
		for G in self.Pt:
			Pvu[G.V[vid].colour][G.V[uid].colour] += 1
			Pv[G.V[vid].colour] += 1
			Pu[G.V[uid].colour] += 1
		den = len(self.Pt)
		ans = 0
		for cv in range(self.k):
			for cu in range(self.k):
				ans += Pvu[cv][cu] / den * math.log(max(1, Pvu[cv][cu]) * den / max(1, Pv[cv] * Pu[cu]))
		return ans

	def __init__(self, k: int, G: Graph):
		self.k = k
		self.G = G

		def uP(_):
			return [1 / k for _ in range(k)]

		def ucP(_, __):
			return [[1 / k for _ in range(k)] for _ in range(k)]

		def I(vid, uid):
			return len(G.N[G.V[vid]]) + len(G.N[G.V[uid]])

		gmi = MutualInformationGraph(len(G.V), I)
		T = gmi.MST()
		model = DependencyTree(T, uP, ucP)
		self.Pt = [model.sample(self.G) for _ in range(self.initial_population)]
		self.t = 0


def solve(k: int, G: Graph) -> ColouredGraph:
	return MIMIC(k, G).run()


solution = solve(3, Petersen)

print("vertices' colours are:", end=' ')
for x in solution.V:
	print(x.colour, end=' ')
