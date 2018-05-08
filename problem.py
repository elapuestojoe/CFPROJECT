import numpy as np
import copy
import random
class Vertex():
	color = None
	idVertex = None
	def __init__(self, idVertex):
		self.idVertex = idVertex


class Problem():

	# verticesNumber = None
	# edgesNumber = None
	# vertices = []
	# colors = None
	# edges = set()
	# fitness = 0
	# neighbors = None

	def __init__(self, vertices, edges):
		self.verticesNumber = vertices
		self.edgesNumber = edges
		self.colors = [0]*vertices
		self.vertices = []
		self.edges = set()
		for i in range(vertices):
			self.vertices.append(Vertex(i+1))

	def updateFitness(self):
		currentColorFitness = (1 - (np.count_nonzero(self.colors)/len(self.colors))) 
		currentNodeFitness = np.sum(self.colors) / len(self.colors)

		self.fitness = currentNodeFitness #* currentColorFitness

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
			if(oldColor == None and color != None):
				self.colors[color]+=1

		self.updateFitness()
		return True

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

	def ColoredRatio(self):
		colored = 0
		for vertex in self.vertices:
			if(vertex.color != None):
				colored += 1
		return colored / len(self.vertices)

	def AvgColorRatio(self):
		total = 0
		colors = 0
		for vertex in self.vertices:
			if(vertex.color != None):
				total += self.colors[vertex.color]
				colors += 1
		if(colors != 0):
			return total / colors
		return 0

	def FINAL(self, filename):
		# maxColor = -1
		# for vertex in self.vertices:
		# 	if(vertex.color > maxColor):
		# 		maxColor = vertex.color
		maxColor = np.count_nonzero(self.colors)
		file = open(filename, "w")
		file.write("YOU NEED {} COLORS\n".format(maxColor+1))
		file.write("HERE IS THE LIST OF EACH NODE WITH ITS CORRESPONDING COLOR CODE\n")
		self.printNodes()
		file.write("COLORS: {}".format(self.colors))
		# print(np.sum(self.colors))

	def MoveIsValid(self, vertex, color):
		oldColor = self.vertices[vertex].color
		self.vertices[vertex].color = color
		if(self.checkConflicts() != 0):
			# print("Can't assign color: Conflict")
			self.vertices[vertex].color = oldColor
			return False
		else:
			self.vertices[vertex].color = oldColor
			return True

	def getFitness(self):
		currentColorFitness = (1 - (np.count_nonzero(self.colors)/len(self.colors)))
		currentNodeFitness = np.sum(self.colors) / len(self.colors)
		avgColor = self.AvgColorRatio()
		return (currentNodeFitness*2) + (currentColorFitness*1) + (avgColor / len(self.colors)*1.3)

	def EvalMove(self, vertex, color, epsilon):
		oldColor = self.vertices[vertex].color
		self.assignColor(vertex, color)
		fitness = self.getFitness()
		self.assignColor(vertex, oldColor)
		return fitness #- (epsilon)

	def Status(self):
		#Returns 6 features:
		currentColorRatio = np.count_nonzero(self.colors)/len(self.colors) #ratio of used colors
		currentNodeRatio = np.sum(self.colors) / len(self.colors) #ratio of nodes already colored
		averageNodesUsedPerColor = self.AvgColorRatio()
		averageEdgesPerNode = len(self.colors) / len(self.edges)
		minNeighbors = self.neighbors[0][0]
		maxNeighbors = self.neighbors[-1][0]

		return "{},{},{},{},{},{}".format(currentColorRatio, currentNodeRatio, averageNodesUsedPerColor, averageEdgesPerNode, minNeighbors, maxNeighbors)

	def setNeighbors(self):
		neighbors = [0] * len(self.vertices)
		for edge in self.edges:
			neighbors[edge[0]] += 1
			neighbors[edge[1]] += 1
		self.neighbors = sorted(list(zip(neighbors, range(len(neighbors)))), key=lambda x: x[0], reverse=True) #list of tuples ordered by neighbor number
		
	def LoadProblem(filename):
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

		problem.setNeighbors()
		return problem