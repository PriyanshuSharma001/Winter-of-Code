# -*- coding: utf-8 -*-
"""Linear_Regression_Gradient_Descent.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oR-4oNyLdOmMUE6fPsqDwCfArSaZXDOM

# ***LINEAR REGRESSION (Gradient Descent)***
"""

# Importing Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""## ***Training***"""

# Cost Function
def Cost(X, Y, theta):
  cost = (1/(2*(X.shape[0])))*(np.sum((np.dot(X, theta) - Y)**2))
  return cost

# Predict Function
def Predict(X, theta):
  return np.dot(X, theta)

# Function to calculate RMSE
def RootMeanSquaredError(Y, Prediction):
  return (np.sum((Prediction-Y)**2))**(0.5)

# Normalize Function
def NormalizeTrain(X):
  AverageList = []
  StdDevList = []

  for i in range(X.shape[1]):
    Average = np.mean(X[:,i])
    AverageList.append(Average)
    StdDev  = np.std(X[:,i])
    StdDevList.append(StdDev)
    X[:,i] = (X[:,i] - Average)/StdDev
  
  return X, AverageList, StdDevList


def NormalizeTest(X, AverageList, StdDevList):
  for i in range(X.shape[1]):
    X[:,i] = (X[:,i] - AverageList[i])/StdDevList[i]
  
  return X

# Linear Regression Training Function using Gradient Descent
def LinearRegressionTraining(X, Y, theta, LearningRate, Iterations):
  m = Y.size
  CostList = []

  for i in range(Iterations):
    Y_Predicted = Predict(X, theta)
    cost = Cost(X, Y, theta)
    CostList.append(cost)
    
    d_theta = (np.dot(X.T, Y_Predicted - Y) / m)
    theta = theta - LearningRate*d_theta

  return theta, CostList

# Importing Training Data 
TrainingData = pd.read_csv('drive/MyDrive/Colab Notebooks/Linear_train.csv')
TrainingData.pop('Unnamed: 0')
TrainingData

# Initializing X (Feature Values) for training
X = np.array(TrainingData.drop('label', axis=1))
X, AverageList, StdDevList = NormalizeTrain(X)
X = np.concatenate((np.ones((X.shape[0],1)),X), axis=1)

print('X Shape : ', X.shape)
print(X)

# Initializing Y (Labels) for training
Y = np.array([TrainingData['label']]).T

print('Y Shape : ', Y.shape)
print(Y)

# Randomly Initializing Theta
theta = np.zeros((X.shape[1], 1))

print('theta shape : ', theta.shape)
print(theta)

# Main / Determining Coefficient Values
Iterations = 1000
LearningRate = 0.1
theta, CostList = LinearRegressionTraining(X, Y, theta, LearningRate, Iterations)

print('theta shape : ', theta.shape)
print(theta)

# Minimized Cost and Graph
rng = np.arange(0, len(CostList))
plt.plot(rng, CostList)
plt.xlabel('Iterations')
plt.ylabel('Cost')
plt.show()

print('\nInitial Cost   : ', CostList[0])
cost = Cost(X, Y, theta)
print('Minimized Cost : ', cost)

# Predicting Training labels
Y_Predicted = Predict(X, theta)

print('[[  EXPECTED    :    PREDICTED ]]')
print(np.concatenate((Y, Y_Predicted), axis=1))

print('\nRoot Mean Squared Error :', RootMeanSquaredError(Y, Y_Predicted))

"""## ***Testing***"""

# TESTING
# Importing Data
TestingData = pd.read_csv('drive/MyDrive/Colab Notebooks/Linear_test.csv')
TestingData.pop('Unnamed: 0')
TestingData

# Initializing X_test
X_test = np.array(TestingData.drop('label', axis=1))
X_test = NormalizeTest(X_test, AverageList, StdDevList)
X_test = np.concatenate((np.ones((X_test.shape[0],1)),X_test), axis=1)

print('X_test shape : ', X_test.shape)
print(X_test)

# Initializing Y_test
Y_test = np.array([TestingData['label']]).T

print('Y_test shape : ', Y_test.shape)
print(Y_test)

# Predicting test labels
Y_test_Predicted = Predict(X_test, theta)

print('[[  EXPECTED    :    PREDICTED ]]')
print(np.concatenate((Y_test, Y_test_Predicted), axis=1))

print('\nRoot Mean Squared Error :', RootMeanSquaredError(Y_test, Y_test_Predicted))