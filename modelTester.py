from problem import Problem
import numpy as np
from keras.models import model_from_json
import tensorflow as tf

from solver import FirstVertex, MinimumDegreeVertex, MaxDegreeVertex, LessFrequentColorVertex, RandomVertex
from solver import MoreFrequentColorHeuristic, Uncoloring, GreedyColoring
from time import time
from random import choice

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

def loadModel():
	json_file = open("model.json", "r")
	loaded_model_json = json_file.read()
	json_file.close()
	model = model_from_json(loaded_model_json)
	model.load_weights("model.h5")
	model.compile(loss="categorical_crossentropy", optimizer='adam', metrics=["categorical_accuracy"])
	return model	

def test(problemFile):
	print("TEST")
	problem = Problem.LoadProblem(problemFile)
	t0 = time()
	while(not problem.isSolved()):
		vertexHeuristic, colorHeuristic = choice(HeuristicFunctionArray)
		vertex = vertexHeuristic(problem)
		color = colorHeuristic(problem, vertex)
		problem.assignColor(vertex, color)
	t1 = time()
	print("Finished in {}".format(t1-t0))
	print("PROBLEM SOLVED USING {} colors".format(np.count_nonzero(problem.colors)))
	problem.printNodes()

def main():

	# problemFile = "./Instances/queen/queen8_8.col"
	problemFile = "./Instances/le450/le450_5c.col"
	problem = Problem.LoadProblem(problemFile)

	hist = np.zeros((1,3,7))
	currentStatus = problem.Status()
	for i in range(0, len(hist[0])):
		hist[0][i] = np.concatenate((problem.NumericalStatus(), [0]),axis=0)

	with tf.Session() as sess:
		model = loadModel()
		t0 = time()
		while(not problem.isSolved()):
			heuristic = np.argmax(model.predict(hist)) #From one hot to index
			vertexHeuristic, colorHeuristic = HeuristicFunctionArray[heuristic]
			vertex = vertexHeuristic(problem)
			color = colorHeuristic(problem, vertex)

			problem.assignColor(vertex, color)
			#Update hist and predict next step
			hist[0][0] = hist[0][1]
			hist[0][1] = hist[0][2]
			hist[0][2] = np.concatenate((problem.NumericalStatus(), [heuristic]))
	t1 = time()
	print("Finished in {}".format(t1-t0))
	print("PROBLEM SOLVED USING {} colors".format(np.count_nonzero(problem.colors)))
	problem.printNodes()

	print("RANDOM TEST")
	test(problemFile)

if __name__ == '__main__':
	main()