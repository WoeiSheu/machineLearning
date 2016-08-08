# coding:utf-8
import numpy as np

def loadDataSet():
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    # 1代表侮辱性文字, 0代表正常言论
    return postingList, classVec
    
def createVocabularyList(dataSet):
    vocabularySet = set([])
    for document in dataSet:
        vocabularySet = vocabularySet | set(document)
    return list(vocabularySet)

def setOfWords2Vec(vocabularyList, inputSet):
    returnVector = len(vocabularyList)*[0]
    for word in inputSet:
        if word in vocabularyList:
            returnVector[vocabularyList.index(word)] = 1
        else:
            print 'the word: %s is not in my vocabulary!' % word
    return returnVector

def trainNBO(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    p0Num = np.zeros(numWords)
    p1Num = np.zeros(numWords)
    p0Denom = 0.0
    p1Denom = 0.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vector = p1Num/p1Denom        #change to log()
    p0Vector = p0Num/p0Denom        #change to log()
    return p0Vector, p1Vector, pAbusive

def classifyNB(vector2Classify, p0Vector, p1Vector, pClass1):
    p1 = sum(vector2Classify * p1Vector) + log(pClass1)
    p0 = sum(vector2Classify * p0Vector) + log(1.0-pClass1)
    if p1 > p0:
        return 1
    else:
        return 0

def testingNB():
    listOPosts, listClasses = loadDataSet()
    myVocabularyList = createVocabularyList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append( setOfWords2Vector(myVocabularyList, postinDoc) )
    p0V, p1V, pAb = trainNB0( np.array(trainMat), np.array(listClasses) )
    testEntry = ['love', 'my', 'dalmation']
    thisDoc = np.array( setOfWords2Vector(myVocabularyList, testEntry) )
    print testEntry, 'classified as: ', classiFyNB(thisDoc, p0V, p1V, pAb)
    testEntry = ['stupid', 'garbage']
    thisDoc = np.array( setOfWords2Vector(myVocabularyList, testEntry) )
    print testEntry, 'classified as: ', classiFyNB(thisDoc, p0V, p1V, pAb)

def bagOfWords2VectorMN(vocabularyList, inputSet):
    returnVector = len(vocabularyList)*[0]
    for word in inputSet:
        if word in vocabularyList:
            returnVector[vocabularyList.index(word)] += 1
    return returnVector

def textParse(bigString):
    import re
    listOfTokens = re.split(r'\w*', bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]

def spamTest():
    docList = []
    classList = []
    fullText = []
    for i in range(1,26):
        wordList = textParse( open('email/spam/%d.txt' % i).read() )
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse( open('email/ham/%d.txt' % i).read() )
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
    vocabularyList = createVocabularyList(docList)
    trainingSet = range(50)
    testSet = []
    for i range(10):
        randIndex = int( random.uniform(0, len(trainingSet)) )
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat = []
    trainClasses = []
    for docIndex in trainingSet:
        trainMat.append( setOfWords2Vector(vocabularyList, docList[docIndex]) )
        trainClasses.append( classList[docIndex] )
    p0V, p1V, pSpam = trainNB0( np.array(trainMat), np.array(trainClasses) )
    errorCount = 0
    for docIndex in testSet:
        wordVector = setOfWords2Vector( vocabularyList, docList[docIndex] )
        if classifyNB( array(wordVector), p0V, p1V, pSpam ) != classList[docIndex]:
            errorCount += 1
    print 'the error rate is: ', float(errorCount)/len(testSet)

def calculateMostFreq(vocabularyList, fullText):
    import operator
    freqDict = {}
    for token in vocabularyList:
        freqDict[token] = fullText.count[token]
    sortedFreq = sorted(freqDict.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedFreq[:30]

def localWords(feed1,feed0):
    import feedparser
    doctList = []
    classList = []
    fullText = []
    minLen = min( len(feed1['entries']), len(feed0['entries']) )
    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.append(wordList)
        classList.append(1)
        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.append(wordList)
        classList.append(0)
    vocabularyList = createVocabularyList(docList)
    top30Words = calculateMostFreq(vocabularyList, fullText)
    for pairW in top30Words:
        if pairW[0] in vocabularyList:
            vocabularyList.remove(pairW[0])
    trainingSet = range(2*minLen)
    testSet = []

    for i in range(20):
        randIndex = int( random.uniform(0, len(trainingSet)) )
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat = []
    trainClasses = []
    for docIndex in trainingSet:
        trainMat.append( bagOfWords2VectorMN(vocabularyList, docList[docIndex]) )
        trainClasses.append(classList[docIndex])
    p0V, p1V, pSpam = trainNB0( np.array(trainMat), np.array(trainClasses) )
    errorCount = 0
    for docIndex in testSet:
        wordVector = bagOfWords2VectorMN(vocabularyList, docIndex[docIndex])
        if classifyNB( np.array(wordVector), p0V, p1V, pSpam ) != classList[docIndex]:
            errorCount += 1
    print 'the error rate is: ', float(errorCount)/len(testSet)
    return vocabularyList, p0V, p1V

def getTopWords(ny, sf):
    import operator
    vocabularyList, p0V, p1V = localWords(ny, sf)
    topNY = []
    topSF = []
    for i in range(len(p0V)):
        if p0V[i] > -6.0:
            topSF.append( (vocabularyList[i], p0V[i]) )
        if p1V[i] > -6.0:
            topNY.append( (vocabularyList[i], p1V[i]) )
    sortedSF = sorted(topSF, key=lambda pair: pair[1], reverse=True)
    print "SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**"
    for item in sortedSF:
        print item[0]
    sortedNY = sorted(topNY, key=lambda pair: pair[1], reverse=True)
    print "NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**"
    for item in sortedNY:
        print item[0]

if __name__=="__main__":
    import feedparser
    ny = feedparser.parse('http://newyork.craigslist.org/stp/index.css')
