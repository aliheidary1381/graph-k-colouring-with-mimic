from graph import *
import numpy as np

k = 3


def rootP(population: list[Graph], root: Vertex):
	colours = []  # 0 1 2 ....
	probability = []
	for instance in population:
		colours.append(instance.V[root.id].colour)
	for colour in range(0, k + 1):
		probability.append(colours.count(colour) / (len(colours)))

	return probability


def ConditionalProbability(population: list[Graph], children: Vertex, parent: Vertex):
	colours = np.zeros((k, k))
	probability = np.zeros((k, k))
	for instance in population:
		colours[instance.V[parent].colour][instance.V[children].colour] += 1  # bug!
	for parentColour in range(0, k + 1):
		for childColour in range(0, k + 1):
			probability[parentColour][childColour] = colours[parentColour][childColour] / (colours[parentColour].sum())
	return probability


def betterHalf(population: list[Graph], costs: list[int]):
	dictionary = dict(zip(population, costs))
	sortedG = sorted(dictionary.items(), key=lambda x: x[1])
	halfG = dict(sortedG[:int(len(population) / 2)])  # bug!
	return halfG.keys()


G = Graph()
G.add_vertex()
G.add_vertex()
G.add_edge(Edge(G.V[0], G.V[1]))
