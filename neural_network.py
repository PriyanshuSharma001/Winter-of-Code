# -*- coding: utf-8 -*-
"""Neural_Network.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15QZjPeZRwLc0w9SMxu9YuD4fzr9kKqA5
"""

# Importing Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Importing Training Data 
TrainingData = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/emnist-letters-train.csv")
TrainingData

X = np.array(TrainingData.drop('23', axis=1))
print('X Shape : ', X.shape)
print(X)

Y = np.array([TrainingData['23']]).T
print('Y Shape : ', Y.shape)
print(Y)

# Importing Testing Data 
TestingData = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/emnist-letters-test.csv")
TestingData

X_test = np.array(TestingData.drop('1', axis=1))
print('X_test Shape : ', X_test.shape)
print(X_test)

Y_test = np.array([TestingData['1']]).T
print('Y_test Shape : ', Y_test.shape)
print(Y_test)

class NeuralNetwork():
  def __init__(self, LayerSizes, Iterations, LearningRate):
    self.LayerSizes = LayerSizes
    self.Iterations = Iterations
    self.LearningRate = LearningRate
    self.Weights = self.Initialization()
    #self.Bias = np.ones(())
  
  def Initialization(self):
    InputLayer = self.LayerSizes[0]
    HiddenLayer1 = self.LayerSizes[1]
    HiddenLayer2 = self.LayerSizes[2]
    OutputLayer = self.LayerSizes[3]

    Parameters = {
        'W1' : np.zeros((HiddenLayer1, InputLayer)),
        'W2' : np.zeros((HiddenLayer2, HiddenLayer1)),
        'W3' : np.zeros((OutputLayer, HiddenLayer2))
    }

    return Parameters

  def Sigmoid(self, X):
    return 1/(1 + np.exp(-X))
  
  def d_Sigmoid(self, X):
    return (np.exp(-X))/((1 + np.exp(-X))**2)
  
  def SoftMax(self, X):
    exps = np.exp(X - X.max())
    return exps / np.sum(exps, axis=0)
  
  def d_SoftMax(self, X):
    exps = np.exp(X - X.max())
    return exps / np.sum(exps, axis=0) * (1 - exps / np.sum(exps, axis=0))
  
  def ForwardPropogation(self, X):
        Weights = self.Weights

        Weights['A0'] = X

        Weights['Z1'] = np.dot(Weights["W1"], Weights['A0'])
        Weights['A1'] = self.Sigmoid(Weights['Z1'])

        Weights['Z2'] = np.dot(Weights["W2"], Weights['A1'])
        Weights['A2'] = self.Sigmoid(Weights['Z2'])

        Weights['Z3'] = np.dot(Weights["W3"], Weights['A2'])
        Weights['A3'] = self.SoftMax(Weights['Z3'])

        return Weights['A3']
  
  def BackwardPropogation(self, Y, Output):
    Weights = self.Weights
    ChangeWeight = {}

    error = 2*(Output - Y) * self.d_SoftMax(Weights['Z3'])
    ChangeWeight['W3'] = np.outer(error, Weights['A2'])

    error = np.dot(Weights['W3'].T, error) * self.d_Sigmoid(Weights['Z2'])
    ChangeWeight['W2'] = np.outer(error, Weights['A1'])

    error = np.dot(Weights['W2'].T, error) * self.d_Sigmoid(Weights['Z1'])
    ChangeWeight['W1'] = np.outer(error, Weights['A0'])

    return ChangeWeight
  
  def UpdateWeights(self, ChangeWeight):
    for key, value in ChangeWeight.items():
      self.Weights[key] = self.Weights[key] - self.LearningRate * value

  def TestAccuracy(self, X_test, Y_test):
    Predictions = []

    for x,y in zip(X_test, Y_test):
      Output = self.ForwardPropogation(x.T)
      Predictions.append(Output == y)
    
    return np.mean(Predictions) * 100

  
  def Train(self, X, Y, X_test, Y_test):
    for i in range(self.Iterations):
      for x,y in zip(X, Y):
        Output = self.ForwardPropogation(x.T)
        ChangeWeight = self.BackwardPropogation(y, Output)
        self.UpdateWeights(ChangeWeight)
    
    Accuracy = self.TestAccuracy(X_test, Y_test)
    print('Accuracy : ', Accuracy)

LayerSizes = [784, 26, 26, 1]
Iterations = 1
LearningRate = 0.01

NN = NeuralNetwork(LayerSizes, Iterations, LearningRate)
NN.Train(X, Y, X_test, Y_test)