# -*- coding: utf-8 -*-
"""Polynomial_Regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZZRbFEa8QpW3S8ozf4FKHh46Ym_h0ovL

# ***POLYNOMIAL REGRESSION***
"""

# Importing Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""## ***Training***"""

# Sigmoid Function
def SigmoidFunction(X):
  return 1/(1+np.exp(-X))

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

# Function To Add Higher Degree Features 
def ConvertToPoly(X, degree):
  A, B, C = np.array([X[:,0]]), np.array([X[:,1]]), np.array([X[:,2]])
  A, B, C = A.T, B.T, C.T

  X_poly = np.ones((X.shape[0],1))

  for i in range(degree):
    X_poly = np.concatenate((X_poly, A**(i+1)), axis=1)
  for i in range(degree):
    X_poly = np.concatenate((X_poly, B**(i+1)), axis=1)
  for i in range(degree):
    X_poly = np.concatenate((X_poly, C**(i+1)), axis=1)

  return X_poly

# Cost Function
def Cost(X, Y, theta):
  cost = (1/(2*(X.shape[0])))*(np.sum((np.dot(X, theta) - Y)**2))
  return cost

# Polynomial Regression Function
def Predict(X, theta):
  return np.dot(X, theta)

# Normal Equation
def PolynomialRegressionTraining_N(X, Y):
  return np.dot(np.dot(np.linalg.pinv(np.dot(X.T, X)), X.T), Y)

# Gradient Descent
def PolynomialRegressionTraining_G(X, Y, theta, LearningRate, Iterations):
  m = Y.size
  CostList  = []

  for i in range(Iterations):
    Y_Predicted = Predict(X, theta)
    cost = Cost(X, Y, theta)
    CostList.append(cost)
    
    d_theta = (np.dot(X.T, Y_Predicted - Y) / m)
    theta = theta - LearningRate*d_theta

  return theta, CostList

# Impoting Data
TrainingData = pd.read_csv('drive/MyDrive/Colab Notebooks/Polynomial_train.csv')
TrainingData.pop('Unnamed: 0')
TrainingData

# Initializing X and Y
X = np.array(TrainingData.drop('label', axis=1))
Y = np.array([TrainingData['label']]).T

print('X Shape : ', X.shape)
print(X)
print('\nY Shape : ', Y.shape)
print(Y)

# Conc=verting X to Desired Format
X_poly = ConvertToPoly(X, 3)
X_poly[:,1:], AverageList, StdDevList = NormalizeTrain(X_poly[:,1:])

print('X_poly Shape : ', X_poly.shape)
print(X_poly)

# Calculating Theta Using Normal Equation
thetaN = PolynomialRegressionTraining_N(X_poly, Y)

print('thetaN Shape : ', thetaN.shape)
print(thetaN)

cost = Cost(X_poly, Y, thetaN)
print('Minimized Cost : ', cost)

# Randomly Initializing theta
thetaG = np.zeros((X_poly.shape[1], 1))
print('thetaG Shape : ', thetaG.shape)
print(thetaG)

# Calculating Theta Using Gradient Descent
Iterations = 2000
LearningRate = 1
thetaG, CostListG = PolynomialRegressionTraining_G(X_poly, Y, thetaG, LearningRate, Iterations)

print('thetaG shape : ', thetaG.shape)
print(thetaG)

# Minimized Cost and Graph
rng = np.arange(0, Iterations)
plt.plot(rng, CostListG)
plt.xlabel('Iterations')
plt.ylabel('Cost')
plt.show()

print('\nInitial Cost   : ', CostListG[0])
cost = Cost(X_poly, Y, thetaG)
print('Minimized Cost : ', cost)

# Predicting Training Labels
Y_Predicted_N = np.dot(X_poly, thetaN)
Y_Predicted_G = np.dot(X_poly, thetaG)
Compare = np.concatenate((Y, Y_Predicted_N, Y_Predicted_G), axis=1)

print('[[  EXPECTED   :   PREDICTED(N)   :  PREDICTED(G) ]]')
print(Compare)

"""## ***Testing***"""

# Importing Testing Data
TestingData = pd.read_csv('drive/MyDrive/Colab Notebooks/Polynomial_test.csv')
TestingData.pop('Unnamed: 0')
TestingData

# Initializing X_test and Y_test
X_test = np.array(TestingData.drop('label', axis=1))
Y_test = np.array([TestingData['label']]).T
print('X_test Shape : ', X_test.shape)
print(X_test)
print('\nY_test Shape : ', Y_test.shape)
print(Y_test)

# Converting X_test to Desired Format
X_test_poly = ConvertToPoly(X_test, 3)
X_test_poly[:,1:] = NormalizeTest(X_test_poly[:,1:], AverageList, StdDevList)

print('X_test_poly Shape : ', X_test_poly.shape)
print(X_test_poly)

# Predicting Test Labels
Y_test_Predicted_N = np.dot(X_test_poly, thetaN)
Y_test_Predicted_G = np.dot(X_test_poly, thetaG)
Compare = np.concatenate((Y_test, Y_test_Predicted_N, Y_test_Predicted_G), axis=1)

print('[[  EXPECTED   :   PREDICTED(N)   :  PREDICTED(G) ]]')
print(Compare)