import math

from graph import *


class MIMIC:
	k: int  # constant
	body: Graph  # constant
	gmi: MIGraph
	model: DTree
	current_generation: list[ColouredGraph]

	def __init__(self, k: int, G: Graph):
		self.iteration = 0
		self.k = k
		self.body = G
		self.gmi = MIGraph(len(G.V))
		for v in G.V:
			c = len(G.N[v])
			v = self.gmi.V[v.id]
			for e in self.gmi.N[v]:
				u = e.opposite_end(v)
				e.weight = c + len(G.N[G.V[u.id]])
		self.model = self.gmi.MST(k)
		self.current_generation = self.produce_new_generation(1)

	def run(self) -> ColouredGraph:
		reproduction_rate = 1
		death_rate = 0.5
		while self.current_generation[0].fitness() != len(self.body.E):
			self.iteration += 1
			self.pick_best(death_rate)
			self.update_model()
			self.estimate_distribution()
			self.current_generation += self.produce_new_generation(reproduction_rate)
		return self.current_generation[0]

	def calculate_eP(self, v: DVertex):
		v.eP = [0 for _ in range(self.k)]
		for G in self.current_generation:
			v.eP[G.V[v.id].colour] += 1
		den = len(self.current_generation)
		v.eP = [cnt / den for cnt in v.eP]

	def calculate_P(self, parent: DVertex, child: DVertex):
		child.P = [[0 for _ in range(self.k)] for _ in range(self.k)]
		for G in self.current_generation:
			child.P[G.V[parent.id].colour][G.V[child.id].colour] += 1
		count_sum = [max(1, sum(child.P[colour])) for colour in range(self.k)]
		child.P = [[child.P[i][j] / count_sum[i] for j in range(self.k)] for i in range(self.k)]

	def estimate_distribution(self):
		for v in self.model.V:
			if v == self.model.root:
				self.calculate_eP(v)
			else:
				self.calculate_P(self.model.parent[v].opposite_end(v), v)

	def generate_candidate_solution(self) -> ColouredGraph:
		return self.model.sample(self.body)

	def produce_new_generation(self, sampling_ratio) -> list[ColouredGraph]:
		if self.iteration == 0:
			new_population = 10*len(self.body.V)
		else:
			old_generation = self.current_generation
			new_population = len(old_generation)
		new_generation = []

		for i in range(new_population * sampling_ratio):
			new_generation.append(self.generate_candidate_solution())
		return new_generation

	def evaluate_fitness(self):
		self.current_generation.sort(key=lambda G: G.fitness(), reverse=True)

	def pick_best(self, ratio: float):
		self.evaluate_fitness()
		self.current_generation = self.current_generation[:round(len(self.current_generation) * ratio)]

	def calculate_mutual_information(self, e: MIEdge):
		v, u = e.ends
		vid, uid = v.id, u.id
		Pvu = [[0 for _ in range(self.k)] for _ in range(self.k)]
		Pv = [0 for _ in range(self.k)]
		Pu = [0 for _ in range(self.k)]
		for G in self.current_generation:
			Pvu[G.V[vid].colour][G.V[uid].colour] += 1
			Pv[G.V[vid].colour] += 1
			Pu[G.V[uid].colour] += 1
		den = len(self.current_generation)
		for cv in range(self.k):
			for cu in range(self.k):
				e.weight += Pvu[cv][cu]/den*math.log(max(1, Pvu[cv][cu])*den/max(1, Pv[cv]*Pu[cu]))

	def fill_gmi(self):
		for e in self.gmi.E:
			self.calculate_mutual_information(e)

	def update_model(self):
		self.fill_gmi()
		self.model = self.gmi.MST(self.k)


H = Graph(4)
H.add_edge(Edge(H.V[0], H.V[1]))
H.add_edge(Edge(H.V[1], H.V[2]))
H.add_edge(Edge(H.V[2], H.V[3]))
AI = MIMIC(2, H)
CG = AI.run()
print("vertices' colours are:", end=' ')
for x in CG.V:
	print(x.colour, end=' ')
