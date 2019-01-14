import numpy as np
from random import choice, randint, randrange
from time import time
import copy
from problem import Problem
from tqdm import tqdm
import os
# HEURISTICAS VERTEX

def FirstVertex(problem):
	for i in range(len(problem.vertices)):
		if(problem.vertices[i].color == None):
			return i
	return RandomVertex(problem)

def MinimumDegreeVertex(problem):
	'''
	Returns the first None vertex with the min number of adjacent vertices
	'''
	for i in range(len(problem.neighbors)):
		numberOfNeighbors, vertexIndex = problem.neighbors[i]
		if(problem.vertices[vertexIndex].color == None):
			return vertexIndex

	#Couldn't find vertex (problem solved?) anyway return random
	return RandomVertex(problem)

def MaxDegreeVertex(problem):
	'''
	Returns the first None vertex with the max number of adjacent vertices
	'''
	for i in range(len(problem.neighbors)-1, -1, -1):
		numberOfNeighbors, vertexIndex = problem.neighbors[i]
		if(problem.vertices[vertexIndex].color == None):
			return vertexIndex

	#Couldn't find vertex (problem solved?) anyway return random
	return RandomVertex(problem)

def LessFrequentColorVertex(problem):
	#print(np.argmax(problem.colors)) #Most frequently used color
	minColorNodes = max(problem.colors)
	minColorIndex = np.argmax(problem.colors)
	for i in range(len(problem.colors)-1, -1, -1):
		if(problem.colors[i] < minColorNodes):
			minColorNodes = problem.colors[i]
			minColorIndex = i

	#By this point Point we have the least 
	for i in range(len(problem.vertices)-1, -1, -1):
		if(problem.vertices[i].color == minColorIndex):
			return i
	return RandomVertex(problem)

#No lo usaremos
# def MoreFrequentColorVertex(problem):
# 	#print(np.argmax(problem.colors)) #Most frequently used color
# 	mostFrequentColor = np.argmax(problem.colors)
# 	for i in range(len(problem.vertices)-1, -1, -1):
# 		if(problem.vertices[i].color == mostFrequentColor):
# 			return i
# 	return RandomVertex(problem) 

def RandomVertex(problem):
	return choice(problem.vertices).idVertex-1

# HEURISTICAS COLOR
def MoreFrequentColorHeuristic(problem, vertex):
	mostFrequentColor = np.argmax(problem.colors)
	if(problem.MoveIsValid(vertex, mostFrequentColor)):
		return mostFrequentColor
	else:
		return GreedyColoring(problem, vertex)

# def Uncoloring(problem, vertex):
# 	r = np.count_nonzero(problem.colors)
# 	if(r > 1):
# 		color = problem.colors[randrange(r)]
# 		while(not problem.MoveIsValid(vertex, color)):
# 			color = problem.colors[randrange(r)]
# 		return color
# 	else:
# 		return None

def Uncoloring(problem, vertex):
	return None

def GreedyColoring(problem, vertex):
	for i in range(len(problem.colors)):
		if(problem.MoveIsValid(vertex, i)):
			return i
	raise Exception('ColorException', 'No valid color')

# 15 heuristic vertex-color function tuple
HeuristicFunctionArray = [
	(FirstVertex, MoreFrequentColorHeuristic),
	(MinimumDegreeVertex, MoreFrequentColorHeuristic),
	(MaxDegreeVertex, MoreFrequentColorHeuristic),
	(LessFrequentColorVertex, MoreFrequentColorHeuristic),
	(RandomVertex, MoreFrequentColorHeuristic),

	(FirstVertex, Uncoloring),
	(MinimumDegreeVertex, Uncoloring),
	(MaxDegreeVertex, Uncoloring),
	(LessFrequentColorVertex, Uncoloring),
	(RandomVertex, Uncoloring),

	(FirstVertex, GreedyColoring),
	(MinimumDegreeVertex, GreedyColoring),
	(MaxDegreeVertex, GreedyColoring),
	(LessFrequentColorVertex, GreedyColoring),
	(RandomVertex, GreedyColoring),
	]


# Eval Fitness:
def evalMove(problemToEval, vertexHeuristic, colorHeuristic):
	vertex = vertexHeuristic(problemToEval)
	color = colorHeuristic(problemToEval, vertex)
	return (vertex, color)

def rargmax(vector):
	""" Argmax that chooses randomly among eligible maximum indices. """
	m = np.amax(vector)
	indices = np.nonzero(vector == m)[0]
	return choice(indices)

def RandomEval(problem):
	h = choice(HeuristicFunctionArray)
	vert = h[0](problem)
	color = h[1](problem, vert)
	problem.assignColor(vert, color)

def EvalPosibilities(problem):
	#Tuple of problem:heurstic
	moveArray = []
	fitnessArray = [0] * len(HeuristicFunctionArray)
	for i in range(len(HeuristicFunctionArray)):
		vertexHeuristic = HeuristicFunctionArray[i][0]
		colorHeuristic = HeuristicFunctionArray[i][1]

		moveArray.append(evalMove(problem, vertexHeuristic, colorHeuristic))

	# print("MOVES: ", moveArray)

	for i in range(len(moveArray)):
		move = moveArray[i]
		fitnessArray[i] = (problem.EvalMove(move[0], move[1], i))

	# maxFitnessIndex = np.random.choice(np.floatnonzero(fitnessArray == fitnessArray.max()))
	maxFitnessIndex = np.argmax(fitnessArray)
	# print(fitnessArray)
	# print(maxFitnessIndex)
	bestMove = moveArray[maxFitnessIndex]
	problem.assignColor(bestMove[0], bestMove[1])
	return maxFitnessIndex, fitnessArray[maxFitnessIndex]

if __name__ == '__main__':
	# problemFile = "./Instances/queen/queen16_16.col"
	problemFile = "./Instances/mulsol/mulsol.i.1.col"
	name = problemFile.split("/")[-1]

	if(not os.path.isdir("data/{}".format(name))):
		os.mkdir("data/{}".format(name))

	problem = None
	for i in range(10):
		problem = Problem.LoadProblem(problemFile)
		file = open("data/{}/{}.csv".format(name, i), "w")
		t0 = time()
		file.write("currentColorRatio, currentNodeRatio, averageNodesUsedPerColor, averageEdgesPerNode, minNeighbors, maxNeighbors, bestH\n")
		with tqdm(total=len(problem.colors)) as bar:
			while(not problem.isSolved()):
				bestH, fit = EvalPosibilities(problem)
				# file.write("Heuristic {} Fitness: {}\n".format(bestH, fit))
				file.write("{},{}\n".format(problem.Status(), bestH))
				# print(np.sum(problem.colors))
				progress = np.sum(problem.colors)
				bar.update(progress - bar.n)
				# problem.printNodes()
			t1 = time()
			print("Finished in {}".format(t1-t0))
		problem.FINAL("data/{}/Solution{}.txt".format(name, i))
	# while(not problem.isSolved()):
	# 	RandomEval(problem)

	# # print("Finished in {}".format(t1-t0))
	# problem.FINAL()