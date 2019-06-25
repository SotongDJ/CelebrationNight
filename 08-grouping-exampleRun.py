#!/usr/bin/env python3
import libPrint
import pathlib, sqlite3, json
import pandas as pd
import numpy as np

conditionDict = {
    "tripleRep-homoDEG" : {
        "branch" : "testing1",
        "method" : "dsStringtie",
        "annotate" : "speciesEnsembl",
        "trim" : "trimQ30",
        "column" : "homolog",
        "regulate" : ["ratio-T1_vs_Control","ratio-T2_vs_Control"],
        "compare" : [
            ["[UP in ratio-T1_vs_Control]","[MINOR in ratio-T2_vs_Control]"],
            ["[DOWN in ratio-T1_vs_Control]","[MINOR in ratio-T2_vs_Control]"],
            ["[UP in ratio-T1_vs_Control]","[DOWN in ratio-T2_vs_Control]"],
            ["[DOWN in ratio-T1_vs_Control]","[UP in ratio-T2_vs_Control]"],
            ["[APR in ratio-T1_vs_Control]","[NOVALUE in ratio-T2_vs_Control]"],
            ["[DIS in ratio-T1_vs_Control]","[VALUE in ratio-T2_vs_Control]"],
        ],
        "condition" : ["UP","MINOR","DOWN","APR","DIS","VALUE","NOVALUE"],
        "levelList" : [1,4,7],
    },
}

databasePathStr = 'data/06-cd-CuffDiff/{branch}-{method}/{annotate}-{trim}-expressionSummary.db'
jsonPathStr = 'data/08-grouping/{branch}-{method}-{annotate}-{trim}/{title}-{level}-list-{type}-.json'
logFolderPathStr = 'data/08-grouping/{branch}-{method}-{annotate}-{trim}/'
logFilePathStr = '{title}-{level}-list'
printOutStr = "\tCount of {target} is {number}"

def action(targetStr,inputValue,levelInt,conditionStr):
    exportStr = ""
    if targetStr == None:
        targetStr = ""
    if inputValue == np.float64('0.0') and conditionStr == "NOVALUE":
        exportStr = targetStr
    elif inputValue != np.float64('0.0') and conditionStr == "VALUE":
        exportStr = targetStr
    else:
        if inputValue == np.float64('-inf') and conditionStr == "DIS":
            exportStr = targetStr
        elif inputValue == np.float64('inf') and conditionStr == "APR":
            exportStr = targetStr
        elif inputValue != np.float64('-inf') and inputValue != np.float64('inf'):
            if inputValue > levelInt and conditionStr == "UP":
                exportStr = targetStr
            elif inputValue < (levelInt*-1) and conditionStr == "DOWN":
                exportStr = targetStr
            elif inputValue <= levelInt and inputValue >= (levelInt*-1) and conditionStr == "MINOR":
                exportStr = targetStr
            
    return exportStr

for titleStr in list(conditionDict.keys()):
    conditionSubDict = conditionDict[titleStr]
    conditionSubDict.update({"title":titleStr})
    columnStr = conditionSubDict["column"]
    regulateList = conditionSubDict["regulate"]
    compareList = conditionSubDict["compare"]
    conditionList = conditionSubDict["condition"]
    levelList = conditionSubDict["levelList"]

    databaseStr = databasePathStr.format(**conditionSubDict)
    logFolderStr = logFolderPathStr.format(**conditionSubDict)
    pathlib.Path( logFolderStr ).mkdir(parents=True,exist_ok=True)

    Connect = sqlite3.connect(databaseStr)
    summaryDF = pd.read_sql_query("SELECT * FROM Summary", Connect)
    countInt = len(summaryDF.index)

    for levelInt in levelList:
        # levelInt = levelList[0]
        conditionSubDict.update({"level":str(levelInt)})

        logFileStr = logFilePathStr.format(**conditionSubDict)

        Print = libPrint.timer()
        Print.logFilenameStr = logFileStr
        Print.folderStr = logFolderStr
        Print.testingBool = False
        Print.startLog()

        combinationDict = dict()
        significantDict = dict()
        Print.printing("Process: {}".format(titleStr))
        Print.printing("Source: {}".format(databasePathStr.format(**conditionSubDict)))
        Print.printing("Threshold: {}".format(str(levelInt)))
        Print.printing("[Comparing] start")
        for rowInt in range(countInt):
            print("[{}/{}]".format(str(rowInt),str(countInt)),end="\r")
            targetStr = summaryDF.at[rowInt,columnStr] # pylint: disable=maybe-no-member

            for regulateStr in regulateList:
                sigColumStr = regulateStr.replace("ratio-","sig-").replace("compare-","sig-")
                sigInputStr = summaryDF.at[rowInt,sigColumStr] # pylint: disable=maybe-no-member
                inputValue = summaryDF.at[rowInt,regulateStr] # pylint: disable=maybe-no-member

                for conditionStr in conditionList:
                    tempStr = action(targetStr,inputValue,levelInt,conditionStr)
                    dictNameStr = "[{} in {}]".format(conditionStr,regulateStr)
                    if tempStr != "":
                        combinationList = combinationDict.get(dictNameStr,list())
                        combinationList.append(tempStr)
                        combinationDict.update({ dictNameStr : combinationList })
                    
                    if tempStr != "" and sigInputStr == "yes" :
                        significantList = significantDict.get(dictNameStr,list())
                        significantList.append(tempStr)
                        significantDict.update({ dictNameStr : significantList })

        Print.printing("[Comparing] finish")

        Print.printing("[Deduplicating] finish")
        for combinationStr in list(combinationDict.keys()):
            combinationDict[combinationStr] = sorted(list(set(combinationDict[combinationStr])))
            Print.printing(printOutStr.format(target=combinationStr,number=str(len(combinationDict[combinationStr]))))

        Print.printing("[Deduplicating] finish")

        Print.printing("[Rearranging] start")
        crossSet = set()
        """
        for frontStr in list(combinationDict.keys()):
            for backStr in list(combinationDict.keys()):
                if frontStr != backStr:
                    crossSet.update({"_and_".join(sorted([frontStr,backStr]))})
        """
        for compareSubList in compareList:
            crossSet.update({"_and_".join(sorted(compareSubList))})

        Print.printing("[Rearranging] finish")

        dictionaryDict = {
            "comparison" : combinationDict,
            "significant" : significantDict,
        }
        for targetStr in list(dictionaryDict.keys()):
            Print.printing("[Concluding] start: {}".format(targetStr))
            conditionSubDict.update({"type":targetStr})
            targetDict = dictionaryDict[targetStr]
            totalSetInt = len(crossSet)
            countSetInt = 0
            for crossStr in crossSet:
                countSetInt = countSetInt + 1
                print("[{}/{}] {}".format(str(countSetInt),str(totalSetInt),crossStr),end="\r")
                # crossStr = list(crossSet)[0]
                frontStr = crossStr.split("_and_")[0]
                backStr  = crossStr.split("_and_")[1]
                unionSet = set()
                unionSet.update(set(targetDict.get(frontStr,[])))
                unionSet.update(set(targetDict.get(backStr,[])))

                andList = [ x for x in unionSet if (( x in targetDict.get(frontStr,[]) )and( x in targetDict.get(backStr,[]) ))]
                frontOnlyList = [ x for x in unionSet if (( x in targetDict.get(frontStr,[]) )and( x not in targetDict.get(backStr,[]) ))]
                backOnlyList = [ x for x in unionSet if (( x not in targetDict.get(frontStr,[]) )and( x in targetDict.get(backStr,[]) ))]

                targetDict.update({
                    "_and_".join(sorted([frontStr,backStr])) : andList,
                    frontStr+"_only" : frontOnlyList,
                    backStr+"_only" : backOnlyList,
                })

                Print.printing(printOutStr.format(target="_and_".join(sorted([frontStr,backStr])),number=str(len(andList))))
                Print.printing(printOutStr.format(target=frontStr+"_only", number=str(len(frontOnlyList))))
                Print.printing(printOutStr.format(target=backStr+"_only",  number=str(len(backOnlyList) )))

            Print.printing("[Concluding] finish: {}".format(targetStr))
            Print.printing("[Exporting] start: {}".format(targetStr))
            
            jsonStr = jsonPathStr.format(**conditionSubDict)
            with open(jsonStr, "w") as targetHandle:
                json.dump(targetDict,targetHandle,indent=2)

            Print.printing("[Exporting] finish: {}".format(targetStr))
        Print.stopLog()
        print("\n")
