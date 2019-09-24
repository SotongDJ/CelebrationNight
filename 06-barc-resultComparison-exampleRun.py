import json
import libPrint
filenameStr = "T??Q**-testing-trimQ30"
folderStr = "data/06-ba-blat/speciesEnsembl/"
targetTypeList = ["gene","transcript"]
for targetTypeStr in targetTypeList:
    pairList = open("{}{}-nameList-{}.tsv".format(folderStr,filenameStr,targetTypeStr)).read().splitlines()

    Print = libPrint.timer()
    Print.logFilenameStr = "{}-{}Comparison".format(filenameStr,targetTypeStr)
    Print.folderStr = folderStr
    Print.testingBool = False
    Print.startLog()

    query2targetDict = dict()
    target2queryDict = dict()
    Print.printing("[Disolve pair list]")
    Print.printing("\tPair Count: {}".format(len(pairList)))
    for pairStr in pairList:
        objectList = pairStr.split("\t")
        queryStr = objectList[0]
        targetStr = objectList[1]

        q2tSet = query2targetDict.get(queryStr,set())
        q2tSet.update({targetStr})
        query2targetDict.update({ queryStr : q2tSet })

        t2qSet = target2queryDict.get(targetStr,set())
        t2qSet.update({queryStr})
        target2queryDict.update({ targetStr : t2qSet })

    Print.printDashLine()
    Print.printing("[Arrange Target distribution]")
    Print.printing("\tQuery Count: {}".format(len(query2targetDict)))
    q2tCountDict = dict()
    for queryStr in list(query2targetDict.keys()):
        targetSet = query2targetDict[queryStr]
        q2tCountSet = q2tCountDict.get(len(targetSet),set())
        q2tCountSet.update({queryStr})
        q2tCountDict.update({ len(targetSet) : q2tCountSet })

    Print.printDashLine()
    Print.printing("[Arrange Query distribution]")
    Print.printing("\tTarget Count: {}".format(len(target2queryDict)))
    t2qCountDict = dict()
    for targetStr in list(target2queryDict.keys()):
        querySet = target2queryDict[targetStr]
        t2qCountSet = t2qCountDict.get(len(querySet),set())
        t2qCountSet.update({targetStr})
        t2qCountDict.update({ len(querySet) : t2qCountSet })

    Print.printDashLine()
    Print.printing("[Count Target distribution]")
    q2tQuerySet = q2tCountDict[1]
    q2tTargetSet = set()
    for queryStr in q2tQuerySet:
        q2tTargetSet.update(query2targetDict[queryStr])
    q2tQueryList = list(q2tQuerySet)
    q2tTargetList = list(q2tTargetSet)

    for targetCountInt in sorted(list(q2tCountDict.keys())):
        Print.printing("\t{} Q {}s were 1 Q vs {} T".format(len(q2tCountDict[targetCountInt]),targetTypeStr,targetCountInt))

    Print.printDashLine()
    Print.printing("[Count Query distribution]")
    t2qQuerySet = set()
    t2qTargetSet = t2qCountDict[1]
    for targetStr in t2qTargetSet:
        t2qQuerySet.update(target2queryDict[targetStr])
    t2qQueryList = list(t2qQuerySet)
    t2qTargetList = list(t2qTargetSet)

    for queryCountInt in sorted(list(t2qCountDict.keys())):
        Print.printing("\t{} T {}s were {} Q vs 1 T".format(len(t2qCountDict[queryCountInt]),targetTypeStr,queryCountInt))

    Print.printDashLine()
    Print.printing("[Count one-to-one pair]")
    O2oQuerySet = set()
    Q2tExclusiveSet = set()
    for queryStr in q2tQueryList: 
        if queryStr in t2qQueryList:
            O2oQuerySet.update({queryStr})
        else:
            Q2tExclusiveSet.update({queryStr})
    
    O2oTargetSet = set()
    q2TExclusiveSet = set()
    for queryStr in q2tTargetList:
        if queryStr in t2qTargetList:
            O2oTargetSet.update({queryStr})
        else:
            q2TExclusiveSet.update({queryStr})
    
    O2oQueryList = list(O2oQuerySet)
    O2oTargetList = list(O2oTargetSet)
    Print.printing("\tQ {}s: {}".format(targetTypeStr,len(O2oQueryList)))
    Print.printing("\tT {}s: {}".format(targetTypeStr,len(O2oTargetList)))

    Print.printDashLine()
    Print.printing("[Count no-one-to-one pair]")
    Q2tExclusiveList = list(Q2tExclusiveSet)
    t2QExclusiveList = list(set([ n for n in t2qQueryList if n not in q2tQueryList ]))
    Print.printing("\tExclusive in [Q]2t (not in t2[Q]): {} Q {}s".format(len(Q2tExclusiveList),targetTypeStr))
    Print.printing("\tExclusive in t2[Q] (not in [Q]2t): {} Q {}s".format(len(t2QExclusiveList),targetTypeStr))
    q2TExclusiveList = list(q2TExclusiveSet)
    T2qExclusiveList = list(set([ n for n in t2qTargetList if n not in q2tTargetList ]))
    Print.printing("\tExclusive in q2[T]: {} T {}s".format(len(q2TExclusiveList),targetTypeStr))
    Print.printing("\tExclusive in [T]2q: {} T {}s".format(len(T2qExclusiveList),targetTypeStr))

    resultDict = {
        "query2targetDict" : { x: list(y) for x,y in query2targetDict.items()},
        "target2queryDict" : { x: list(y) for x,y in target2queryDict.items()},
        "q2tCountDict" : { x: list(y) for x,y in q2tCountDict.items()},
        "t2qCountDict" : { x: list(y) for x,y in t2qCountDict.items()},
        "q2tQueryList" : q2tQueryList,
        "t2qQueryList" : t2qQueryList,
        "q2tTargetList" : q2tTargetList,
        "t2qTargetList" : t2qTargetList,
        "O2oQueryList" : O2oQueryList,
        "O2oTargetList" : O2oTargetList,
        "Q2tExclusiveList" : Q2tExclusiveList,
        "t2QExclusiveList" : t2QExclusiveList,
        "q2TExclusiveList" : q2TExclusiveList,
        "T2qExclusiveList" : T2qExclusiveList,
    }
    with open("{}{}-{}Comparison.json".format(folderStr,filenameStr,targetTypeStr),'w') as targetHandle:
        json.dump(resultDict,targetHandle, indent=1, sort_keys=True)

    Print.stopLog()