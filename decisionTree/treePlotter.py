#!usr/bin/env python
#coding=utf-8

import matplotlib.pyplot as plt

decisionNode = dict(boxstyle='sawtooth', fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrowArgs = dict(arrowstyle="<-")

def plotNode(nodeText, centerPoint, parentPoint, nodeType):
    createPlot.ax1.annotate(nodeText, xy=parentPoint, xycoords='axes fraction', xytext=centerPoint, textcoords='axes fraction',\
            va="center", ha="center", bbox=nodeType, arrowprops=arrowArgs)

def createPlot():
    fig = plt.figure(1,facecolor='white')
    fig.clf()
    createPlot.ax1 = plt.subplot(111, frameon=False)
    plotNode(U'决策节点', (0.5,0.1), (0.1,0.5), decisionNode )
    plotNode(U'叶节点', (0.8,0.1), (0.3,0.8), leafNode )
    plt.show()

def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs

def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:
            thisDepth = 1
        if thisDepth > maxDepth:
            maxDepth = thisDepth
    return maxDepth

def retrieveTree(i):
    listOfTrees = [{'no surfacing':\
        {0: 'no', 1:\
            {'flippers':\
                {0: 'no', 1: 'yes'}}}},
    {'no surfacing':\
        {0: 'no', 1:\
            {'flippers':\
                {0: 'no', 1: 'yes'}}}}
    ]
    return listOfTrees[i]

def plotMidText(centerPoint, parentPoint, textString):
    xMid = (parentPoint[0]-centerPoint[0]) / 2.0 + centerPoint[0]
    yMid = (parentPoint[1]-centerPoint[1]) / 2.0 + centerPoint[1]
    createPlot.ax1.text(xMid,yMid,textString)

def plotTree(myTree, parentPoint, nodeText):
    numLeafs = getNumLeafs(myTree)
    depth = getTreeDepth(myTree)
    firstStr = myTree.keys()[0]
    centerPoint = (plotTree.xOff + (1.0 + float(numLeafs)) / 2.0 / plotTree.totalW, plotTree.yOff)
    plotMidText(centerPoint, parentPoint, nodeText)
    plotNode(firstStr, centerPoint, parentPoint, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD

    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            plotTree(secondDict[key], centerPoint, str(key))
        else:
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), centerPoint, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), centerPoint, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD

def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW
    plotTree.yOff = 1.0
    plotTree(inTree, (0.5,1.0), '')
    plt.show()

if __name__ == "__main__":
    myTree = retrieveTree(0)
    createPlot(myTree)
