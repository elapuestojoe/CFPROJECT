from keras.utils import plot_model
from modelTester import loadModel
import sys

model = loadModel()
plot_model(model, to_file='model.png')