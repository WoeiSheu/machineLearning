#!usr/bin/env python
#coding=utf-8

import math
import operator

def calculateShannonEnergy(dataSet):    #Calculate Shannon Energy
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

def splitDataSet(dataSet, axis, value): #divide dataSet into sub.
    returnDataSet = []
    for featureVector in dataSet:
        if featureVector[axis] == value:    #choose the item that meet the value, and then remove it.
            reducedFeatureVector = featureVector[:axis]
            reducedFeatureVector.extend(featureVector[axis+1:])
            returnDataSet.append(reducedFeatureVector)
    return returnDataSet

def chooseBestFeatureToSplit(dataSet):  #Calculate the shannon energy of the sub-tree divided by each feature.
    numFeatures = len(dataSet[0]) - 1   #the feature nums.
    baseEntropy = calculateShannonEnergy(dataSet)   #the origin entropy.
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):        #for each feature
        featureList = [example[i] for example in dataSet]   #the last column of dataset is the feature list.
        uniqueValues = set(featureList) #remove the repeat item.
        newEntropy = 0.0
        for value in uniqueValues:
            subDataSet = splitDataSet(dataSet, i, value)    #divide the dataset into sub-dataset by feature of 'value'.
            probability = len(subDataSet) / float(len(dataSet))
            newEntropy += probability * calculateShannonEnergy(subDataSet)
        infoGain = baseEntropy - newEntropy
        if infoGain > bestInfoGain:     #if the infoGain larger than zero, get new infoGain.
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def majorityCount(classList):   #find which value appears most.
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]    #select the last column of dataSet
    if classList.count(classList[0]) == len(classList): #if the first item of the classList is the only value, it is the leave node.
        return classList[0]
    if len(dataSet[0]) == 1:    #if dataSet[0] remains only one item, which means that we have disposed all the attribute.
        return majorityCount(classList) #return the class label that count most.
    bestFeature = chooseBestFeatureToSplit(dataSet)
    bestFeatureLabel = labels[bestFeature]
    myTree = { bestFeatureLabel:{} }
    del(labels[bestFeature])    #delete the label that has been chosen.
    featureValues = [example[bestFeature] for example in dataSet]
    uniqueValues = set(featureValues)   #use set to remove the repeat word.
    for value in uniqueValues:
        subLabels = labels[:]
        myTree[bestFeatureLabel][value] = createTree( splitDataSet(dataSet, bestFeature, value), subLabels )

    return myTree

def classify(inputTree, featureLabels, testVector): #the classify algorithm.
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

def storeTree(inputTree, filename): #store the decision tree that had been trained.
    import pickle
    fw = open(filename, 'w')
    pickle.dump(inputTree, fw)
    fw.close()

def grabTree(filename): #get the tree that was stored in the 'filename'.
    import pickle
    fr = open(filename)
    return pickle.load(fr)

if __name__=="__main__":
    fr = open('lenses.txt')     #open the file 'lenses.txt'
    lenses = [inst.strip().split('\t') for inst in fr.readlines()]  #dispose the file.
    lensesLabels = ['age','prescript','astigmatic','tearRate']  #set labels.
    lensesTree = createTree(lenses, lensesLabels)       #create tree.
    print lensesTree,'\n\n\n'   #print lenses tree in text
    import treePlotter
    treePlotter.createPlot(lensesTree)  #print lenses tree in diagram
