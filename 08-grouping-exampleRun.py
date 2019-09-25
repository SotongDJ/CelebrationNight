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
            "targetList" : ["gene","transcript"]
            # "title" : "",
            # "level" : "",
            # "targetType" : "",
            # "sginiType" : "",
        },
        "condition" : {
            "testing1-homoDEG" : {
                "column" : "homolog",
                "regulate" : [
                    "[ratio:T1>Control]","[ratio:T2>Control]",
                    "[ratio:T1<Control]","[ratio:T2<Control]",
                    "[ratio:T1~Control]","[ratio:T2~Control]",
                    "[FPKM:Total>0]","[FPKM:Total=0]",
                ],
                "compare" : [
                    ["[ratio:T1>Control]","[ratio:T2~Control]"],
                    ["[ratio:T1<Control]","[ratio:T2~Control]"],
                    ["[ratio:T1>Control]","[ratio:T2<Control]"],
                    ["[ratio:T1<Control]","[ratio:T2>Control]"],
                ],
                "levelList" : [1,4,7],
            },
            "testing1-speSEG" : {
                "column" : "Gene_ID",
                "regulate" : [
                    "[ratio:T1<Control]","[ratio:T1>Control]",
                    "[compare-T2<T1]","[compare-T2>T1]","[compare-T2~T1]",
                ],
                "compare" : [
                    ["[ratio:T1>Control]","[compare-T2<T1]"],
                    ["[ratio:T1<Control]","[compare-T2>T1]"],
                    ["[ratio:T1>Control]","[compare-T2~T1]"],
                    ["[ratio:T1<Control]","[compare-T2~T1]"],
                ],
                "levelList" : [1,4,7],
            },
        },
    },
]

databasePathStr = 'data/07-cd-CuffDiff/{branch}-{method}/{annotate}-{trim}-{targetType}ExpressionSummary.tsv'
jsonPathStr = 'data/08-grouping/{branch}-{method}-{annotate}-{trim}/{title}-{level}-{targetType}List-{sginiType}.json'
tsvPathStr = 'data/08-grouping/{branch}-{method}-{annotate}-{trim}/{title}-{level}-{targetType}List-{sginiType}.tsv'
logFolderPathStr = 'data/08-grouping/{branch}-{method}-{annotate}-{trim}/'
logFilePathStr = '{title}-list'
printOutStr = "    Count of {target} is {number}"

for sampleDict in sampleList:
    # sampleDict = sampleList[0]
    stringDict = sampleDict["string"]
    conditionDict = sampleDict["condition"]

    descriPathStr = stringDict.get("description","")
    if descriPathStr != "":
        descriDict = json.load(open(descriPathStr,'r'))
    else:
        descriDict = dict()
    
    targetList = stringDict.get("targetList",list())
    for targetTypeStr in targetList:
        for titleStr in list(conditionDict.keys()):
            # targetTypeStr = targetTypeStr[0]
            # titleStr = list(conditionDict.keys())[0]
            conditionSubDict = conditionDict[titleStr]
            stringDict.update({"title":titleStr})
            stringDict.update({"targetType":targetTypeStr})

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
            levelList = conditionSubDict["levelList"]

            # Connect = sqlite3.connect(databaseStr)
            # summaryDF = pd.read_sql_query("SELECT * FROM Summary", Connect)
            summaryDF = pd.read_csv(databaseStr,delimiter="\t",header=0)
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
                        sigInputBoo = False
                        if "[FPKM:" in regulateStr and len(regulateStr.replace(">",":").replace("=",":").split(":")):
                            valColumStr = "[log10(FPKM:{})]".format(regulateStr.replace(">",":").replace("=",":").split(":")[1])
                            sigInputBoo = True
                        else:
                            valColumStr = regulateStr.replace(">","/").replace("<","/").replace("~","/")
                            sigColumStr = regulateStr.replace("ratio:","signi:").replace("compare:","signi:")
                            sigColumStr = sigColumStr.replace(">","/").replace("<","/").replace("~","/")
                            sigInputStr = summaryDF.at[rowInt,sigColumStr] # pylint: disable=maybe-no-member

                        targetBoo = False
                        if "[FPKM:" in regulateStr and ">0]" in regulateStr:
                            inputValue = summaryDF.at[rowInt,valColumStr] # pylint: disable=maybe-no-member
                            if inputValue != "noSignal":
                                targetBoo = True
                        elif "[FPKM:" in regulateStr and "=0]" in regulateStr:
                            inputValue = summaryDF.at[rowInt,valColumStr] # pylint: disable=maybe-no-member
                            if inputValue == "noSignal":
                                targetBoo = True
                        elif ">" in regulateStr:
                            inputValue = summaryDF.at[rowInt,valColumStr.replace(">","/")] # pylint: disable=maybe-no-member
                            if inputValue>levelInt:
                                targetBoo = True
                        elif "<" in regulateStr:
                            inputValue = summaryDF.at[rowInt,valColumStr.replace("<","/")] # pylint: disable=maybe-no-member
                            if inputValue<(levelInt*-1):
                                targetBoo = True
                        elif "~" in regulateStr:
                            inputValue = summaryDF.at[rowInt,valColumStr.replace("~","/")] # pylint: disable=maybe-no-member
                            if (levelInt*-1)<inputValue and inputValue<levelInt:
                                targetBoo = True

                        if targetBoo:
                            combinationSet = combinationDict.get(regulateStr,set())
                            combinationSet.update({targetStr})
                            combinationDict.update({ regulateStr : combinationSet })
                        
                        if targetBoo and ( sigInputStr == "yes" or sigInputBoo ):
                            significantSet = significantDict.get(regulateStr,set())
                            significantSet.update({targetStr})
                            significantDict.update({ regulateStr : significantSet })

                Print.printing("[Comparing] finish")

                Print.printing("[Deduplicating] start: combinationDict")
                for combinationStr in list(combinationDict.keys()):
                    combinationDict[combinationStr] = sorted(list(combinationDict[combinationStr]))
                    Print.printing(printOutStr.format(target=combinationStr,number=len(combinationDict[combinationStr])))

                Print.printing("[Deduplicating] start: significantDict")

                for combinationStr in list(significantDict.keys()):
                    significantDict[combinationStr] = sorted(list(significantDict[combinationStr]))
                    Print.printing(printOutStr.format(target=combinationStr,number=len(significantDict[combinationStr])))

                Print.printing("[Deduplicating] finish")

                Print.printing("[Rearranging] start")
                crossSet = set()

                for compareSubList in compareList:
                    crossSet.update({"{}_and_{}".format(*sorted(compareSubList))})

                Print.printing("[Rearranging] finish")

                dictionaryDict = {
                    "comparison" : combinationDict,
                    "significant" : significantDict,
                }
                for targetTypeStr in list(dictionaryDict.keys()):
                    Print.printing("[Concluding] start: {}".format(targetTypeStr))
                    stringDict.update({"sginiType":targetTypeStr})
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
                            frontStr, backStr = crossStr.split("_and_")
                            unionSet = set()
                            unionSet.update(set(targetDict.get(frontStr,[])))
                            unionSet.update(set(targetDict.get(backStr,[])))

                            andList = [ x for x in unionSet if (( x in targetDict.get(frontStr,[]) )and( x in targetDict.get(backStr,[]) ))]
                            frontOnlyList = [ x for x in unionSet if (( x in targetDict.get(frontStr,[]) )and( x not in targetDict.get(backStr,[]) ))]
                            backOnlyList = [ x for x in unionSet if (( x not in targetDict.get(frontStr,[]) )and( x in targetDict.get(backStr,[]) ))]

                            targetDict.update({
                                "{}_and_{}".format(*sorted([frontStr,backStr])) : list(set(andList)),
                                "{}_without_{}".format(frontStr,backStr) : list(set(frontOnlyList)),
                                "{}_without_{}".format(backStr,frontStr) : list(set(backOnlyList)),
                            })
                            targetHandle.write("Condition: {}\n".format("{}_and_{}".format(*sorted([frontStr,backStr]))))
                            targetHandle.write("Count: {}\nGeneID\tDescription\n".format(str(len(andList))))
                            targetHandle.write("\n".join([ "{}\t{}".format(keyStr,descriDict.get(keyStr,"")) for keyStr in list(set(andList)) ]))
                            targetHandle.write("\n\n")

                            targetHandle.write("Condition: {}\n".format("{}_without_{}".format(frontStr,backStr)))
                            targetHandle.write("Count: {}\nGeneID\tDescription\n".format(str(len(frontOnlyList))))
                            targetHandle.write("\n".join([ "{}\t{}".format(keyStr,descriDict.get(keyStr,"")) for keyStr in list(set(frontOnlyList)) ]))
                            targetHandle.write("\n\n")

                            targetHandle.write("Condition: {}\n".format("{}_without_{}".format(backStr,frontStr)))
                            targetHandle.write("Count: {}\nGeneID\tDescription\n".format(str(len(backOnlyList) )))
                            targetHandle.write("\n".join([ "{}\t{}".format(keyStr,descriDict.get(keyStr,"")) for keyStr in list(set(backOnlyList)) ]))
                            targetHandle.write("\n\n")

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
