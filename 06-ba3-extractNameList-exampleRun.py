#!/usr/bin/env python3
import pathlib, sqlite3, math, json
import numpy as np
import pandas as pd

pathList = [
    "data/06-ba-blat/speciesEnsembl/T??Q**-testing-trimQ30",
]
percentageLimit = 90 # lower than 100


matchRatio = percentageLimit/100
# lossLimit = 0
# lossDiff = 0

for pathStr in pathList:
    blatDF = pd.read_csv("{}.tsv".format(pathStr),delimiter="\t",header=0)
    rowList = blatDF.values.tolist()
    tscpFilterDict = dict()
    geneFilterDict = dict()
    qDict = dict()
    tDict = dict()
    tscpRoundDict = dict()
    geneRoundDict = dict()
    # 
    # matchList = rowList[0]
    # for n in range(21):
    #     [n,str(blatDF.columns.tolist()[n]),str(rowList[0][n])]
    for matchList in rowList:
        matchInt = matchList[0]
        # lossInt = matchList[1]
        qNameStr = matchList[9]
        tNameStr = matchList[13]
        qSizeInt = matchList[10]
        tSizeInt = matchList[14]
        qMatchFlt = round(matchInt/qSizeInt,4)
        tMatchFlt = round(matchInt/tSizeInt,4)
        qRoundInt = math.floor(matchInt/qSizeInt*10)
        tRoundInt = math.floor(matchInt/tSizeInt*10)
        
        tscpPairStr = "{}\t{}".format(qNameStr,tNameStr)

        qGeneNameList = qNameStr.split(".")
        del qGeneNameList[-1]
        qGeneNameStr = ".".join(qGeneNameList)

        tGeneNameList = tNameStr.split(".")
        del tGeneNameList[-1]
        tGeneNameStr = ".".join(tGeneNameList)
        
        genePairStr = "{}\t{}".format(qGeneNameStr,tGeneNameStr)
        
        if qMatchFlt > matchRatio and tMatchFlt > matchRatio:

            filteredList = geneFilterDict.get(genePairStr,list())
            filteredList.append({
                "Q Name" : qNameStr,
                "T Name" : tNameStr,
                "Q Size" : qSizeInt,
                "T Size" : tSizeInt,
                "Q Ratio" : qMatchFlt,
                "T Ratio" : tMatchFlt,
            })
            geneFilterDict.update({ genePairStr : filteredList })

            tscpFilterDict.update({ 
                tscpPairStr : {
                    "Q Name" : qNameStr,
                    "T Name" : tNameStr,
                    "Q Size" : qSizeInt,
                    "T Size" : tSizeInt,
                    "Q Ratio" : qMatchFlt,
                    "T Ratio" : tMatchFlt,
                } 
            })
        
        # tempList = qDict.get(qRoundInt,list())
        # tempList.append([qNameStr,tNameStr])
        # qDict.update( { qRoundInt : tempList } )
        
        # tempList = tDict.get(tRoundInt,list())
        # tempList.append([qNameStr,tNameStr])
        # tDict.update( { tRoundInt : tempList } )
        
        minRoundInt = min([qRoundInt,tRoundInt])
        tempList = tscpRoundDict.get(minRoundInt,list())
        tempList.append([qNameStr,tNameStr])
        tscpRoundDict.update( { minRoundInt : tempList } )

        minRoundInt = min([qRoundInt,tRoundInt])
        tempSet = geneRoundDict.get(minRoundInt,set())
        tempSet.update({genePairStr})
        geneRoundDict.update( { minRoundInt : tempSet } )
        
    # print("\n".join([ str(n) + " "  + str(len(tscpRoundDict[n])) for n in sorted(list(tscpRoundDict.keys())) ]))
    # with open("{}-grouping-transcript.tsv","w") as targetHandle:
    # print("\n".join([ str(n) + " "  + str(len(geneRoundDict[n])) for n in sorted(list(geneRoundDict.keys())) ]))
    # with open("{}-grouping-gene.tsv","w") as targetHandle:
    # len(tscpFilterDict.keys())
    with open("{}-nameList-transcript.tsv".format(pathStr),"w") as targetHandle:
        targetHandle.write("Query\tTarget\n")
        targetHandle.write("\n".join(list(tscpFilterDict.keys())))
    with open("{}-nameList-transcript.json".format(pathStr),"w") as targetHandle:
        resultDict = dict()
        for targetStr in list(tscpFilterDict.keys()):
            keyStr, valueStr = targetStr.split("\t")
            resultDict.update({ keyStr : valueStr })
        
        json.dump(resultDict,targetHandle,indent=2,sort_keys=True)

    # len(geneFilterDict.keys())
    with open("{}-nameList-gene.tsv".format(pathStr),"w") as targetHandle:
        targetHandle.write("Query\tTarget\n")
        targetHandle.write("\n".join(list(geneFilterDict.keys())))
    with open("{}-nameList-gene.json".format(pathStr),"w") as targetHandle:
        resultDict = dict()
        for targetStr in list(geneFilterDict.keys()):
            keyStr, valueStr = targetStr.split("\t")
            resultDict.update({ keyStr : valueStr })

        json.dump(resultDict,targetHandle,indent=2,sort_keys=True)

    with open("{}-nameList.log".format(pathStr),"w") as targetHandle:
        targetHandle.write("Threshold:\t{}%\n".format(str(percentageLimit)))
        targetHandle.write("Amount of transcript pair:\t{}\n".format(str(len(tscpFilterDict.keys()))))
        targetHandle.write("Amount of gene pair:\t{}\n".format(str(len(geneFilterDict.keys()))))
        targetHandle.write("\nDistribution of coverage (Transcript level)\n")
        for levelInt in sorted(list(tscpRoundDict.keys())):
            targetHandle.write("{}\t{}\n".format(str(levelInt),str(len(tscpRoundDict[levelInt]))))
        targetHandle.write("\nDistribution of coverage (Gene level)\n")
        for levelInt in sorted(list(geneRoundDict.keys())):
            targetHandle.write("{}\t{}\n".format(str(levelInt),str(len(geneRoundDict[levelInt]))))