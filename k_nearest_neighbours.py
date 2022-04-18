# -*- coding: utf-8 -*-
"""K_Nearest_Neighbours.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/192DFTsxA9fs_BY8_-xruBU9MeoOU_mMX

# ***K Nearest Neighbour***
"""

# Importing Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Importing Training Data 
TrainingData = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/emnist-letters-train.csv")
TrainingData

# Initializing X (Feature Values) for training
X = np.array(TrainingData.drop('23', axis=1))

print(X.shape)
print(X)

# Importing Testing Data 
TestingData = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/emnist-letters-test.csv")
TestingData

# Initializing Y (Labels) for testing
Y = np.array([TestingData['1']]).T

print('Y Shape : ', Y.shape)
print(Y)

# Initialing A (Inputs) for teesting
Start = 0
Size  = 2500
A = np.array(TestingData.drop('1', axis=1))[Start:Start+Size]

print('A Shape : ', A.shape)
print(A)

# Main / Finding K Nearest Neighbours and Predicting Label
Y_Predicted = np.zeros((A.shape[0], 1))
Y_Probability = []
rows = A.shape[0]
for j in range(0, rows):
  Distance = []

  m = X.shape[0]
  for i in range(0, m):
    Distance.append( np.sqrt(np.sum(( X[i] - A[j] )**2)) )

  TrainingData['Distance'] = Distance

  X_Sorted = np.array(TrainingData.sort_values(by = ['Distance']))

  k = 7
  K_Neighbours = np.array(X_Sorted[0:k, 0])

  count = []
  for i in range(0, 26):
    count.append(np.count_nonzero(K_Neighbours == (i+1)))

  max = 0
  for i in range(0,26):
    if count[i] > count[max]:
      max = i

  Y_Predicted[j] = max+1
  Y_Probability.append(str(round(count[max]*100/k)) + ' %')

# Output
print('EXPECTED vs PREDICTED')
print(np.concatenate((Y[Start:Start+Size], Y_Predicted, np.array([Y_Probability]).T), axis=1))

# Calculating Accuracy
c = 0
for i in range(rows):
  if Y[Start+i] == Y_Predicted[i]:
    c+=1

print('Accuracy : ', (c/rows)*100, '%')

