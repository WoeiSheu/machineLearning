import os
import operator
import numpy as np

def classify0(inX, dataSet, labels, k):
    '''
    input variable: inX,
    training set: dataSet
    training set labels: labels
    choose first k nearset.
    '''
    dataSetSize = len(dataSet)
    diffMat = np.array(dataSetSize*[inX]) - np.array(dataSet)   #sub inX with each line of dataSet.
    sqDiffMat = diffMat**2      #square the diffrence.
#sqDistances = sqDiffMat.sum(axis=1)
#distances = sqDistances**0.5
    distances = sqDiffMat.sum(axis=1)   #sum the matrix by lines, and it can be the distances.
    sortedDistanceIndicies = distances.argsort()    #get the sort index of distances.
    classCount = {}
    for i in range(k):  #for the first k.
        voteILabel = labels[sortedDistanceIndicies[i]]  #the i-th label.
        classCount[voteILabel] = classCount.get(voteILabel,0) + 1   #count the number of i-th label
#sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True) #sort the number of this label.   
#return sortedClassCount[0][0]   #choose the first label as the result.
    countToLabel = {}
    for i in classCount.keys():
        countToLabel[ classCount[i] ] = i
    return countToLabel[ max(countToLabel.keys()) ]

def img2vector(filename):   #Read a file with 32*32 data, turn it to a 1*1024 list.
    returnVect = []
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect.append( int(lineStr[j]) )
    return returnVect

def handwritingClass():
    #Training
    handwritingLabels = []
    trainingFileList = os.listdir('trainingDigits')
    mTrain = len(trainingFileList)
    trainingMat = mTrain*[ 1024*[0] ]   #initialize trainingMat, making it mTrain*1024 dimensions.
    for i in range(mTrain):             #for each digit
        fileNameStr = trainingFileList[i]
        classNumStr = int( fileNameStr.split('_')[0] )  #this is the real value of the file, equals label.
        handwritingLabels.append(classNumStr)
        trainingMat[i] = img2vector('trainingDigits/%s' % fileNameStr)  #convert each file to a 1204-long list, and append into trainingMat.

    #Testing
    testFileList = os.listdir('testDigits')
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        classNumStr = int( fileNameStr.split('_')[0] )
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, handwritingLabels, 3)    #use classify0 to classify testDigits.
#print "The classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr)
        if(classifierResult != classNumStr):    #error classification
            errorCount += 1.0

    print "\nThe total number of errors is: %d" % errorCount
    print "\nThe total error rate is: %f" % (errorCount/float(mTest))

if __name__ == "__main__":
    handwritingClass()
