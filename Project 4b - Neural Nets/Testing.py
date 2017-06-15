from NeuralNetUtil import buildExamplesFromCarData,buildExamplesFromPenData
from NeuralNet import buildNeuralNet
import cPickle 
from math import pow, sqrt

def average(argList):
    return sum(argList)/float(len(argList))

def stDeviation(argList):
    mean = average(argList)
    diffSq = [pow((val-mean),2) for val in argList]
    return sqrt(sum(diffSq)/len(argList))

penData = buildExamplesFromPenData() 
def testPenData(hiddenLayers = [24]):
    return buildNeuralNet(penData,maxItr = 200, hiddenLayerList =  hiddenLayers)

carData = buildExamplesFromCarData()
def testCarData(hiddenLayers = [16]):
    return buildNeuralNet(carData,maxItr = 200,hiddenLayerList =  hiddenLayers)

import random
def testXORData(hiddenLayers = [0]):
    earlyTrainingSet = [([0, 0], [0]), ([0, 1], [1]), ([1, 0], [1]), ([1, 1], [0])]
    finalTrainingSet = []
    for example in earlyTrainingSet:
        for i in range(50):
            finalTrainingSet.append(example)
    random.shuffle(finalTrainingSet)
    earlyTestingSet = [([1, 1], [0]),([0, 0], [0]),([1, 0], [1]),([0, 1], [1])]
    finalTestingSet = []
    for example in earlyTestingSet:
        for i in range(200):
            finalTestingSet.append(example)
    random.shuffle(finalTestingSet)
    return buildNeuralNet((finalTrainingSet, finalTestingSet),maxItr = 100,hiddenLayerList =  hiddenLayers)

hiddenLayersNums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 35, 40]
for num in hiddenLayersNums:
    testXORData(hiddenLayers = [num])
# for run in xrange(5):
#     for num in xrange(0, 45, 5):
#         testPenData(hiddenLayers = [num])
