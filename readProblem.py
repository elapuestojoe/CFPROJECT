import numpy as np
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
			print("Can't assign color: Conflict")
			self.vertices[vertex].color = oldColor
		else:
			if(oldColor != None and oldColor != color):
				self.colors[oldColor] -= 1
				self.colors[color] += 1
			if(oldColor == None):
				self.colors[color]+=1

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
		for vertex in self.vertices:
			print(vertex.color)

def MoreFrequentColorVertex(problem):
	#print(np.argmax(problem.colors)) #Most frequently used color
	mostFrequentColor = np.argmax(problem.colors)
	for i in range(len(problem.vertices)-1, -1, -1):
		if(problem.vertices[i].color == mostFrequentColor):
			return i

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
	problem = loadProblem("./Instances/queen/queen8_8.col")

	print(problem.isSolved())
	print(problem.edges)

	problem.assignColor(0, 0)
	# problem.assignColor(9, 0)

	problem.assignColor(0, 0)
	problem.assignColor(9, 1)

	problem.assignColor(10,3)
	problem.assignColor(35,1)
	# problem.printCurrentColors()
	print(MoreFrequentColorVertex(problem))

