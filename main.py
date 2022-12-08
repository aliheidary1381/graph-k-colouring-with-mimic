from graph import *
import numpy as np
import pandas as pd
k = 3
def rootP(population : list[Graph],root: Vertex):
    colours = [] # 0 1 2 ....
    probability = []
    for instance in population:
        colours.append(instance.V[root.label].colour)
    for colour in range(0,k+1):
        probability.append(colours.count(colour)/(len(colours)))
    
    return probability
def ConditionalProbability(population : list[Graph],children:Vertex,parent:Vertex):
    colours = pd.DataFrame(np.zeros((k,k))) 
    for instance in population:
        colours[instance.V[parent.label].colour][instance.V[children.label].colour] +=1
    Probability = colours.apply(lambda row : row/row.sum(),axis= 0)
    return probability

def betterHalf(population:list[Graph],costs : list[int]):
    dictionary = dict(zip(population,costs))
    sortedG = sorted(dictionary.items(),key=lambda x: x[1])
    halfG = dict(sortedG[:int(len(population)/2)])
    return halfG.keys()
def mutual_information(population:list[Graph],x:Vertex , y : Vertex):
    colours = pd.DataFrame(np.zeros((k,k))) 
    for instance in population:
        colours[instance.V[y.label].colour][instance.V[x.label].colour] +=1
    JointP = colours.apply(lambda x: x/len(population))
    Yprobability = JointP.sum(axis=0)
    temp = JointP/(Yprobability)#Yprobability
    temp = temp.apply(lambda row : row/row.sum(),axis=1) #Xprobability
    temp = np.log(temp)
    MI = (temp*JointP).values.sum()
    return MI
G = Graph()
G.add_vertex()
G.add_vertex()
G.add_edge(Edge(G.V[0], G.V[1]))
