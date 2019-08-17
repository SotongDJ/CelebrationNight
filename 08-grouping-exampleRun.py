#!/usr/bin/env python3
import libPrint
import pathlib, sqlite3, json
import pandas as pd
import numpy as np

sampleList = [
    {
        "string" : {
            "branch" : "testing1",
            "method" : "dsStringtie",
            "description" : "data/dbga-GenomeAnnotation/speciesEnsembl/speciesEnsembl-attributes.json",
            "annotate" : "speciesEnsembl",
            "trim" : "trimQ30",
            "title" : "",
            "level" : "",
            "type" : ""
        },
        "condition" : {
            "testing1-homoDEG" : {
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
                # "condition" : ["UP","MINOR","DOWN","APR","DIS","VALUE","NOVALUE"],
                "condition" : ["UP","MINOR","DOWN","APR","DIS","VALUE","NOVALUE"],
                "levelList" : [1,4,7],
            },
            "testing1-homoSEG" : {
                "column" : "homolog",
                "regulate" : [
                    "ratio-T1_vs_Control","ratio-T2_vs_Control","compare-T2_vs_T1"
                ],
                "compare" : [
                    ["[UP in ratio-T1_vs_Control]","[DOWN in compare-T2_vs_T1]"],
                    ["[DOWN in ratio-T1_vs_Control]","[UP in compare-T2_vs_T1]"],
                    ["[UP in ratio-T1_vs_Control]","[MINOR in compare-T2_vs_T1]"],
                    ["[DOWN in ratio-T1_vs_Control]","[MINOR in compare-T2_vs_T1]"],
                ],
                "condition" : ["UP","MINOR","DOWN"],
                "levelList" : [1,4,7],
            },
        },
    },
]

databasePathStr = 'data/07-cd-CuffDiff/{branch}-{method}/{annotate}-{trim}-expressionSummary.db'
jsonPathStr = 'data/08-grouping/{branch}-{method}-{annotate}-{trim}/{title}-{level}-list-{type}.json'
tsvPathStr = 'data/08-grouping/{branch}-{method}-{annotate}-{trim}/{title}-{level}-list-{type}.tsv'
logFolderPathStr = 'data/08-grouping/{branch}-{method}-{annotate}-{trim}/'
logFilePathStr = '{title}-list'
printOutStr = "    Count of {target} is {number}"

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

for sampleDict in sampleList:
    stringDict = sampleDict["string"]
    conditionDict = sampleDict["condition"]

    descriPathStr = stringDict.get("description","")
    if descriPathStr != "":
        descriDict = json.load(open(descriPathStr,'r'))
    else:
        descriDict = dict()
    
    for titleStr in list(conditionDict.keys()):
        conditionSubDict = conditionDict[titleStr]
        stringDict.update({"title":titleStr})

        databaseStr = databasePathStr.format(**stringDict)
        logFolderStr = logFolderPathStr.format(**stringDict)
        pathlib.Path( logFolderStr ).mkdir(parents=True,exist_ok=True)
        logFileStr = logFilePathStr.format(**stringDict)

        Print = libPrint.timer()
        Print.logFilenameStr = logFileStr
        Print.folderStr = logFolderStr
        Print.testingBool = False
        Print.startLog()
        Print.printing("Process: {}".format(titleStr))
        Print.printing("Source: {}".format(databasePathStr.format(**stringDict)))

        columnStr = conditionSubDict["column"]
        regulateList = conditionSubDict["regulate"]
        compareList = conditionSubDict["compare"]
        conditionList = conditionSubDict["condition"]
        levelList = conditionSubDict["levelList"]

        Connect = sqlite3.connect(databaseStr)
        summaryDF = pd.read_sql_query("SELECT * FROM Summary", Connect)
        countInt = len(summaryDF.index)

        for levelInt in levelList:
            # levelInt = levelList[0]
            stringDict.update({"level":str(levelInt)})

            combinationDict = dict()
            significantDict = dict()

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

            Print.printing("[Deduplicating] start: combinationDict")
            for combinationStr in list(combinationDict.keys()):
                combinationDict[combinationStr] = sorted(list(set(combinationDict[combinationStr])))
                Print.printing(printOutStr.format(target=combinationStr,number=str(len(combinationDict[combinationStr]))))

            Print.printing("[Deduplicating] start: significantDict")

            for combinationStr in list(significantDict.keys()):
                significantDict[combinationStr] = sorted(list(set(significantDict[combinationStr])))
                Print.printing(printOutStr.format(target=combinationStr,number=str(len(significantDict[combinationStr]))))

            Print.printing("[Deduplicating] finish")

            Print.printing("[Rearranging] start")
            crossSet = set()

            for compareSubList in compareList:
                crossSet.update({"_and_".join(sorted(compareSubList))})

            Print.printing("[Rearranging] finish")

            dictionaryDict = {
                "comparison" : combinationDict,
                "significant" : significantDict,
            }
            for targetTypeStr in list(dictionaryDict.keys()):
                Print.printing("[Concluding] start: {}".format(targetTypeStr))
                stringDict.update({"type":targetTypeStr})
                targetDict = dict()
                targetDict.update(dictionaryDict[targetTypeStr])
                totalSetInt = len(crossSet)
                countSetInt = 0

                tsvStr = tsvPathStr.format(**stringDict)
                with open(tsvStr, "w") as targetHandle:
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
                            "_and_".join(sorted([frontStr,backStr])) : list(set(andList)),
                            frontStr+"_without_"+backStr             : list(set(frontOnlyList)),
                            backStr+"_without_"+frontStr             : list(set(backOnlyList)),
                        })
                        targetHandle.write("Condition: {}\n".format("_and_".join(sorted([frontStr,backStr]))))
                        targetHandle.write("Count: {}\nGeneID\tDescription\n".format(str(len(andList))))
                        targetHandle.write("\n".join([ "{}\t{}".format(keyStr,descriDict.get(keyStr,"")) for keyStr in list(set(andList)) ]))
                        targetHandle.write("\n")

                        targetHandle.write("Condition: {}\n".format("{}_without_{}\n".format(frontStr,backStr)))
                        targetHandle.write("Count: {}\nGeneID\tDescription\n".format(str(len(frontOnlyList))))
                        targetHandle.write("\n".join([ "{}\t{}".format(keyStr,descriDict.get(keyStr,"")) for keyStr in list(set(frontOnlyList)) ]))
                        targetHandle.write("\n")

                        targetHandle.write("Condition: {}\n".format("{}_without_{}\n".format(backStr,frontStr)))
                        targetHandle.write("Count: {}\nGeneID\tDescription\n".format(str(len(backOnlyList) )))
                        targetHandle.write("\n".join([ "{}\t{}".format(keyStr,descriDict.get(keyStr,"")) for keyStr in list(set(backOnlyList)) ]))
                        targetHandle.write("\n")

                        Print.printing(printOutStr.format(target="_and_".join(sorted([frontStr,backStr])),number=str(len(andList))))
                        Print.printing(printOutStr.format(target=frontStr+"_only", number=str(len(frontOnlyList))))
                        Print.printing(printOutStr.format(target=backStr+"_only",  number=str(len(backOnlyList) )))

                Print.printing("[Concluding] finish: {}".format(targetTypeStr))
                Print.printing("[Exporting] start: {}".format(targetTypeStr))
                
                jsonStr = jsonPathStr.format(**stringDict)
                with open(jsonStr, "w") as targetHandle:
                    json.dump(targetDict,targetHandle,indent=2)

                Print.printing("[Exporting] finish: {}".format(targetTypeStr))
        Print.stopLog()
