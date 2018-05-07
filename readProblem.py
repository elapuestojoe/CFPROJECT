import numpy as np
from random import choice, randint
from time import time

class Vertex():
	color = None
	idVertex = None
	def __init__(self, idVertex):
		self.idVertex = idVertex
class Problem():

	verticesNumber = None
	edgesNumber = None
	vertices = []
	colors = None
	edges = set()
	def __init__(self, vertices, edges):
		self.verticesNumber = vertices
		self.edgesNumber = edges
		self.colors = [0]*vertices
		for i in range(vertices):
			self.vertices.append(Vertex(i+1))

	def assignColor(self, vertex, color):

		oldColor = self.vertices[vertex].color
		self.vertices[vertex].color = color

		if(self.checkConflicts() != 0):
			# print("Can't assign color: Conflict")
			self.vertices[vertex].color = oldColor
			return False
		else:

			if(oldColor != None and color == None):
				self.colors[oldColor] -= 1

			if(oldColor != None and color != None and oldColor != color):
				self.colors[oldColor] -= 1
				self.colors[color] += 1
			if(oldColor == None):
				self.colors[color]+=1

		return True

	# def uncolor(self, vertex):
	# 	if(self.vertices.vertex)
	# 	self.vertices
	def checkConflicts(self):
		conflicts = 0
		for edge in self.edges:
			aColor = self.vertices[edge[0]].color
			bColor = self.vertices[edge[1]].color
			if(aColor is not None and bColor is not None and aColor == bColor):
				conflicts+=1
		return conflicts

	def isSolved(self):
		for vertex in self.vertices:
			if(vertex.color is None):
				return False
		return True

	def printCurrentColors(self):
		print("CurrentColors")
		print(self.colors)
		# for vertex in self.vertices:
			# print(vertex.color)
	def printNodes(self):
		nodes = []
		for vertex in self.vertices:
			nodes.append(vertex.color)
		print(nodes)

	def Fitness(self):
		colored = 0
		for vertex in self.vertices:
			if(vertex.color != None):
				colored += 1

		return colored
	def FINAL(self):
		maxColor = -1
		for vertex in self.vertices:
			if(vertex.color > maxColor):
				maxColor = vertex.color
		print("YOU NEED {} COLORS".format(maxColor+1))
		print("HERE IS THE LIST OF EACH NODE WITH ITS CORRESPONDING COLOR CODE")
		self.printNodes()

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
	neighbors = [0] * len(problem.vertices)
	for edge in problem.edges:
		neighbors[edge[0]] += 1
		neighbors[edge[1]] += 1
	neighbors = sorted(list(zip(neighbors, range(len(neighbors)))), key=lambda x: x[0]) #list of tuples ordered by neighbor number
	
	for i in range(len(neighbors)):
		numberOfNeighbors, vertexIndex = neighbors[i]
		if(problem.vertices[vertexIndex].color == None):
			return vertexIndex

	#Couldn't find vertex (problem solved?) anyway return random
	return RandomVertex(problem)

def MaxDegreeVertex(problem):
	'''
	Returns the first None vertex with the max number of adjacent vertices
	'''
	neighbors = [0] * len(problem.vertices)
	for edge in problem.edges:
		neighbors[edge[0]] += 1
		neighbors[edge[1]] += 1
	neighbors = sorted(list(zip(neighbors, range(len(neighbors)))), key=lambda x: x[0], reverse=True) #list of tuples ordered by neighbor number
	
	for i in range(len(neighbors)):
		numberOfNeighbors, vertexIndex = neighbors[i]
		if(problem.vertices[vertexIndex].color == None):
			return vertexIndex

	#Couldn't find vertex (problem solved?) anyway return random
	return RandomVertex(problem)

def MoreFrequentColorVertex(problem):
	#print(np.argmax(problem.colors)) #Most frequently used color
	mostFrequentColor = np.argmax(problem.colors)
	for i in range(len(problem.vertices)-1, -1, -1):
		if(problem.vertices[i].color == mostFrequentColor):
			return i
	return RandomVertex(problem)

def RandomVertex(problem):
	return choice(problem.vertices).idVertex-1

# HEURISTICAS COLOR
def MoreFrequentColorHeuristic(problem, vertex):
	mostFrequentColor = np.argmax(problem.colors)
	if(problem.assignColor(vertex, mostFrequentColor)):
		return True
	else:
		return GreedyColoring(problem, vertex)

def Uncoloring(problem, vertex):
	if(problem.vertices[vertex].color != None):
		return problem.assignColor(vertex, None)

def GreedyColoring(problem, vertex):
	for i in range(len(problem.colors)):
		if(problem.assignColor(vertex, i)):
			return True
	return False
# OTHER
def loadProblem(filename):
	line = 0
	problem = None
	with open(filename, "r") as file:
		for line in file:
			line = line.strip("").split(" ")
			
			if(line[0] == "c"):		#Ignorar comentarios
				pass 
			elif(line[0] == "p"):
				problem = Problem(int(line[-2]), int(line[-1]))
			elif(line[0] == "e"):
				startEdge = int(line[1])-1
				destinationEdge = int(line[2])-1

				mi = min(startEdge, destinationEdge)
				ma = max(startEdge, destinationEdge)
				problem.edges.add((mi, ma))

	return problem

if __name__ == '__main__':
	# problem = loadProblem("./Instances/queen/queen8_8.col")
	problem = loadProblem("./Instances/le450/le450_15c.col")

	vertexHeuristics = [FirstVertex, MinimumDegreeVertex, MaxDegreeVertex, MoreFrequentColorVertex, RandomVertex]
	vertexFNames = ["FirstVertex", "MinimumDegreeVertex", "MaxDegreeVertex", "MoreFrequentColorVertex", "RandomVertex"]
	colorHeuristics = [MoreFrequentColorHeuristic, Uncoloring, GreedyColoring]
	colorFNames = ["MoreFrequentColorHeuristic", "Uncoloring", "GreedyColoring"]

	# file = open("RESULTS.txt", "w")
	# t0 = time()
	# while(not problem.isSolved()):
	# 	vertexN = randint(0, 4)
	# 	colorN = randint(0,2)
	# 	vertexF = vertexHeuristics[vertexN](problem)
	# 	colorF = colorHeuristics[colorN](problem, vertexF)

	# 	file.write("{}-{} Fitness: {}\n".format(vertexFNames[vertexN], colorFNames[colorN], problem.Fitness()))

	# 	# print(vertexF)
	# 	#problem.Fitness() # Imprime el numero de nodos con color
	# t1 = time()
	# print("MinimumDegreeVertex-MoreFrequentColorHeuristic Finished in {}".format(t1-t0))
	# problem.FINAL()

	file = open("RESULTS.txt", "w")
	t0 = time()
	while(not problem.isSolved()):
		vertexN = randint(0, 4)
		colorN = randint(0,2)
		vertexF = vertexHeuristics[vertexN](problem)
		colorF = colorHeuristics[colorN](problem, vertexF)

		file.write("{}-{} Fitness: {}\n".format(vertexFNames[vertexN], colorFNames[colorN], problem.Fitness()))

		# print(vertexF)
		#problem.Fitness() # Imprime el numero de nodos con color
	t1 = time()
	print("MinimumDegreeVertex-MoreFrequentColorHeuristic Finished in {}".format(t1-t0))
	problem.FINAL()
	print(problem.colors)
	# MinimumDegreeVertex(problem)