#!usr/bin/env python
#coding=utf-8

import math
import operator

def calculateShannonEnergy(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featureVector in dataSet:
        currentLabel = featureVector[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnergy = 0.0
    for key in labelCounts:
        probability = float(labelCounts[key]) / numEntries
        shannonEnergy -= probability * math.log(probability,2)
    return shannonEnergy

def splitDataSet(dataSet, axis, value):
    returnDataSet = []
    for featureVector in dataSet:
        if featureVector[axis] == value:
            reducedFeatureVector = featureVector[:axis]
            reducedFeatureVector.extend(featureVector[axis+1:])
            returnDataSet.append(reducedFeatureVector)
    return returnDataSet

def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calculateShannonEnergy(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featureList = [example[i] for example in dataSet]
        uniqueValues = set(featureList)
        newEntropy = 0.0
        for value in uniqueValues:
            subDataSet = splitDataSet(dataSet, i, value)
            probability = len(subDataSet) / float(len(dataSet))
            newEntropy += probability * calculateShannonEnergy(subDataSet)
        infoGain = baseEntropy - newEntropy
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def majorityCount(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet[0]) == 1:
        return majorityCount(classList)
    bestFeature = chooseBestFeatureToSplit(dataSet)
    bestFeatureLabel = labels[bestFeature]
    myTree = { bestFeatureLabel:{} }
    del(labels[bestFeature])
    featureValues = [example[bestFeature] for example in dataSet]
    uniqueValues = set(featureValues)
    for value in uniqueValues:
        subLabels = labels[:]
        myTree[bestFeatureLabel][value] = createTree( splitDataSet(dataSet, bestFeature, value), subLabels )

    return myTree

def classify(inputTree, featureLabels, testVector):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featureIndex = featureLabels.index(firstStr)
    for key in secondDict.keys():
        if testVector[featureIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featureLabels, testVector)
            else:
                classLabel = secondDict[key]
    return classLabel

def storeTree(inputTree, filename):
    import pickle
    fw = open(filename, 'w')
    pickle.dump(inputTree, fw)
    fw.close()

def grabTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)

if __name__=="__main__":
    fr = open('lenses.txt')
    lenses = [inst.strip().split('\t') for inst in fr.readlines()]
    lensesLabels = ['age','prescript','astigmatic','tearRate']
    lensesTree = createTree(lenses, lensesLabels)
    print lensesTree,'\n\n\n'
    import treePlotter
    treePlotter.createPlot(lensesTree)
