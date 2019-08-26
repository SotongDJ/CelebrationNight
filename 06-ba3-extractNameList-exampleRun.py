#!/usr/bin/env python3
import pathlib, sqlite3, math, json
import numpy as np
import pandas as pd

conditionList = [
    {
        "dataPath"  : "data/06-ba-blat/speciesEnsembl/T??Q**-testing-trimQ30",
        "referPath" : "data/dbga-GenomeAnnotation/arathTAIR/arathTAIR-attributes.json"
    },
]
percentageLimit = 90 # lower than 100

matchRatio = percentageLimit/100
for conditionDict in conditionList:
    pathStr = conditionDict.get("dataPath","")
    print("Data: {}".format(pathStr))
    referStr = conditionDict.get("referPath","")
    blatDF = pd.read_csv("{}.tsv".format(pathStr),delimiter="\t",header=0)
    rowList = blatDF.values.tolist()
    tscpFilterDict = dict()
    geneFilterDict = dict()
    qDict = dict()
    tDict = dict()
    tscpRoundDict = dict()
    geneRoundDict = dict()
    for matchList in rowList:
        matchInt = matchList[0]
        qNameStr = matchList[9]
        tNameStr = matchList[13]
        qSizeInt = matchList[10]
        tSizeInt = matchList[14]
        qMatchFlt = round(matchInt/qSizeInt,4)
        tMatchFlt = round(matchInt/tSizeInt,4)
        qRoundInt = math.floor(matchInt/qSizeInt*10)
        tRoundInt = math.floor(matchInt/tSizeInt*10)
        
        tscpPairStr = "{}\t{}".format(qNameStr,tNameStr)

        qGeneNameList = [ query.replace("transcript","gene") for query in qNameStr.split(".")]
        del qGeneNameList[-1]
        qGeneNameStr = ".".join(qGeneNameList)

        tGeneNameList = [ target.replace("transcript","gene") for target in tNameStr.split(".")]
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
        
        minRoundInt = min([qRoundInt,tRoundInt])
        tempList = tscpRoundDict.get(minRoundInt,list())
        tempList.append([qNameStr,tNameStr])
        tscpRoundDict.update( { minRoundInt : tempList } )

        minRoundInt = min([qRoundInt,tRoundInt])
        tempSet = geneRoundDict.get(minRoundInt,set())
        tempSet.update({genePairStr})
        geneRoundDict.update( { minRoundInt : tempSet } )
        
    with open("{}-nameList-transcript.tsv".format(pathStr),"w") as targetHandle:
        targetHandle.write("Query\tTarget\n")
        targetHandle.write("\n".join(list(tscpFilterDict.keys())))
    with open("{}-nameList-transcript.json".format(pathStr),"w") as targetHandle:
        resultDict = dict()
        for targetStr in list(tscpFilterDict.keys()):
            keyStr, valueStr = targetStr.split("\t")
            tempSet = set(resultDict.get(keyStr,list()))
            tempSet.update({valueStr})
            resultDict.update({ keyStr : list(tempSet) })
        
        json.dump(resultDict,targetHandle,indent=2,sort_keys=True)

    # len(geneFilterDict.keys())
    with open("{}-nameList-gene.tsv".format(pathStr),"w") as targetHandle:
        targetHandle.write("Query\tTarget\n")
        targetHandle.write("\n".join(list(geneFilterDict.keys())))
    with open("{}-nameList-gene.json".format(pathStr),"w") as targetHandle:
        resultDict = dict()
        for targetStr in list(geneFilterDict.keys()):
            keyStr, valueStr = targetStr.split("\t")
            tempSet = set(resultDict.get(keyStr,list()))
            tempSet.update({valueStr})
            resultDict.update({ keyStr : list(tempSet) })

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

    if referStr != "": 
        print("Reference: {}".format(referStr))
        referDict = json.load(open(referStr,'r'))    
        descriptDict = dict()
        synonymDict = dict()
        for targetStr in list(geneFilterDict.keys()):
            keyStr, valueStr = targetStr.split("\t")

            tempList = synonymDict.get(keyStr,list())
            tempList.append(valueStr)
            synonymDict.update({ keyStr : tempList })

            descriptList = [valueStr]
            if valueStr in list(referDict.keys()):
                descriptList.append(referDict[valueStr])
            valueStr = " => ".join(descriptList)

            tempStr = descriptDict.get(keyStr,"")
            tempList = tempStr.split(",")
            if tempList == ['']:
                tempList = list()
            tempList.append(valueStr)
            tempStr = "; ".join(tempList)
            descriptDict.update({ keyStr : tempStr })

        with open("{}-descriptionList.json".format(pathStr),"w") as targetHandle:
            json.dump(descriptDict,targetHandle,indent=2,sort_keys=True)

        with open("{}-synonymList.json".format(pathStr),"w") as targetHandle:
            json.dump(synonymDict,targetHandle,indent=2,sort_keys=True)
        
        with open("{}-descriptionList.tsv".format(pathStr),"w") as targetHandle:
            targetHandle.write("Query\tTarget\n")
            targetHandle.write("\n".join([ "{}\t{}".format(keyStr,descriptDict.get(keyStr,"")) for keyStr in sorted(list(descriptDict.keys())) ]))
