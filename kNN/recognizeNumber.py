import os
import operator
import numpy as np

def classify0(inX, dataSet, labels, k):
    dataSetSize = len(dataSet)
    diffMat = np.array(dataSetSize*[inX]) - np.array(dataSet)
    sqDiffMat = diffMat**2
#sqDistances = sqDiffMat.sum(axis=1)
#distances = sqDistances**0.5
    distances = sqDiffMat.sum(axis=1)
    sortedDistanceIndicies = distances.argsort()
    classCount = {}
    for i in range(k):
        voteILabel = labels[sortedDistanceIndicies[i]]
        classCount[voteILabel] = classCount.get(voteILabel,0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def img2vector(filename):
    returnVect = []
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect.append( int(lineStr[j]) )
    return returnVect

def handwritingClass():
    handwritingLabels = []
    trainingFileList = os.listdir('trainingDigits')
    mTrain = len(trainingFileList)
    trainingMat = mTrain*[ 1024*[0] ]
    for i in range(mTrain):
        fileNameStr = trainingFileList[i]
        classNumStr = int( fileNameStr.split('_')[0] )
        handwritingLabels.append(classNumStr)
        trainingMat[i] = img2vector('trainingDigits/%s' % fileNameStr)
    
    testFileList = os.listdir('testDigits')
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        classNumStr = int( fileNameStr.split('_')[0] )
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, handwritingLabels, 3)
#print "The classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr)
        if(classifierResult != classNumStr):
            errorCount += 1.0

    print "\nThe total number of errors is: %d" % errorCount
    print "\nThe total error rate is: %f" % (errorCount/float(mTest))

if __name__ == "__main__":
    handwritingClass()
