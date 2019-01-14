from pandas import read_csv, DataFrame, concat
from keras import Sequential
from keras.layers import LSTM, Dense, BatchNormalization, Dropout
import numpy as np
from keras.utils import to_categorical
from keras.models import model_from_json
from os.path import isfile
import os
import tensorflow as tf
from random import choice
import sys
from matplotlib import pyplot as plt
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
	n_vars = 1 if type(data) is list else data.shape[1]
	df = DataFrame(data)
	cols, names = list(), list()
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		cols.append(df.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
	# forecast sequence (t, t+1, ... t+n)
	for i in range(0, n_out):
		cols.append(df.shift(-i))
		if i == 0:
			names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
		else:
			names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
	# put it all together
	agg = concat(cols, axis=1)
	agg.columns = names
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg

def getXY(filename):
	dataset = read_csv(filename, header=0)
	values = dataset.values
	n_steps = 3
	n_features = 6

	reframed = series_to_supervised(values, n_steps, 1)
	values = reframed.values
	print(values.shape)
	n_obs = n_steps * n_features
	# x, y = values[:-n_steps+1, :n_obs], values[n_steps+1:, 1]
	x,y = values[:,:-7], values[:,-1]

	#Reshape as 3d for LSTM
	x = x.reshape((x.shape[0], n_steps, n_features+1))
	# x = x.reshape((x.shape[0], n_steps, n_features+1))

	return x, to_categorical(y, 15)

def loadOrCreateModel(x):
	if(isfile("model.json") and isfile("model.h5")):
		print("Loadmodel")
	# if False:
		json_file = open("model.json", "r")
		loaded_model_json = json_file.read()
		json_file.close()
		model = model_from_json(loaded_model_json)
		model.load_weights("model.h5")
		model.compile(loss="categorical_crossentropy", optimizer='adam', metrics=["categorical_accuracy"])
		return model
	else:
		model = Sequential()
		model.add(LSTM(256, input_shape=(x.shape[1], x.shape[2]), return_sequences=False))
		model.add(Dropout(0.5))
		model.add(Dense(256, activation="relu"))
		model.add(Dropout(0.5))
		model.add(Dense(15, activation="softmax"))

		model.compile(loss="categorical_crossentropy", optimizer='adam', metrics=["categorical_accuracy"])
		# fit network
		return model

def saveHistory(categorical_accuracy, val_categorical_accuracy, folder, title):
	plt.figure()
	plt.plot(categorical_accuracy)
	plt.plot(val_categorical_accuracy)
	plt.title("{} Accuracy".format(title))
	plt.ylabel("Accuracy")
	plt.xlabel("epoch")
	plt.legend(["train", "test"], loc="upper left")
	plt.savefig("./plots/{}/{}.png".format(folder,title))
	plt.clf()
def saveModel(model):
	#Save model
	model_json = model.to_json()
	with open("model.json", "w") as json_file:
		json_file.write(model_json)
	#seralize weights to HDF5
	model.save_weights("model.h5")

def main():

	folder = "data/{}".format(sys.argv[1])
	os.mkdir("plots/{}".format(sys.argv[1]))
	for file in os.listdir(folder):

		if(file.split(".")[-1] == "csv"):
			train_X, train_y = getXY('{}/{}'.format(folder,file))
			
			print(train_X.shape, len(train_X), train_y.shape)

			val_X, val_Y = getXY('{}/{}'.format("data/zeroin.i.1.col/", file))

			print(val_X.shape, len(val_X), val_Y.shape)

			with tf.Session() as sess:
				model = loadOrCreateModel(train_X)
				history = model.fit(train_X, train_y, epochs=50, batch_size=train_X.shape[0], validation_data=(val_X, val_Y), verbose=2, shuffle=False)

				saveModel(model)
				saveHistory(history.history["categorical_accuracy"], history.history["val_categorical_accuracy"], sys.argv[1], file)
if __name__ == '__main__':
	main()