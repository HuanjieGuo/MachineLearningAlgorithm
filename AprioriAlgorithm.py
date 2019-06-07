countTupleList = []
# high -> low
confidenceRelations = []
minSupportCount = 2

# load data
def loadDataSet():
    return [["a1", "a5"], ["a1", "a3", "a4"], ["a2", "a3", "a5"], ["a1", "a2", "a3", "a5"],
            ["a2", "a5"], ["a1", "a2", "a3", "a4", "a5"], ["a1", "a2", "a3", "a4"]]

def createC1(dataSet):
    C1 = []
    #add all items
    for transaction in dataSet:
        getSubList(transaction)
    #rank
    C1.sort()
    #frozenset  can not add or delete any elements
    return map(frozenset,C1)

def getSubList(list):
    allSubList = [list]
    # use 0101 to replace [1,2,3,4]
    for i in range(2**len(list)-1):
        # 0001
        binnumber = bin(i)[2:len(bin(i))]
        if binnumber=="0":
            continue
        # supplement zero
        if len(binnumber)<len(list):
            for i in range(len(list)-len(binnumber)):
                binnumber = "0"+binnumber
        newElement = []
        for i in range(len(binnumber)):
           # print(list,i)
            if binnumber[i] == "1":
                newElement.append(list[i])
        allSubList.append(newElement)
    calculate_count(allSubList)


# calculate it
def calculate_count(all_list):
    for childList in all_list:
        isFirstTime = 1
        for i in range(len(countTupleList)):
            if countTupleList[i][0] == childList:
                countTupleList[i] = (childList, countTupleList[i][1]+1)
                isFirstTime = 0
                break
        # first time to insert
        if isFirstTime == 1:
            countTupleList.append((childList, 1))


# delete those relations that are less that minSupport Count
def trim_relations():
    for tupleSample in countTupleList:
        if tupleSample[1]<2:
            countTupleList.remove(tupleSample)

def rank_insert_confidence(param,result,confidence):
    if len(confidenceRelations)==0:
        confidenceRelations.insert(0, (param, result, confidence))
        return
    for i in range(len(confidenceRelations)):
        if confidence>confidenceRelations[i][2]:
            confidenceRelations.insert(i, (param, result, confidence))
            return
    confidenceRelations.append((param, result, confidence))




def calculate_confidence():
    for i in range(len(countTupleList)-1):
        for j in range(i+1, len(countTupleList)):
            # calculate confidence
            if set(countTupleList[i][0]).issubset(set(countTupleList[j][0])):
                # i位是j位的子集
                rank_insert_confidence(countTupleList[i][0], countTupleList[j][0],
                                       round(countTupleList[j][1]/countTupleList[i][1], 4))
            if set(countTupleList[j][0]).issubset(set(countTupleList[i][0])):
                # j位是i位的子集
                rank_insert_confidence(countTupleList[j][0], countTupleList[i][0],
                                       round(countTupleList[i][1] / countTupleList[j][1], 4))


def mainEntrance():
    # all order List
    myDat = loadDataSet()
    # all element list
    C1 = createC1(myDat)
    # delete those sample which are less than minSupportCount
    trim_relations()
    print("After trim ", countTupleList)
    # calculate
    calculate_confidence()
    # print
    for sample in confidenceRelations:
        print(sample[0], "\t-> ", sample[1], "\t  confidence = ", sample[2]*100, "%")

