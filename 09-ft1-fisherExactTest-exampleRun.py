#!/usr/bin/env python3
import pathlib, json
# import sqlite3
import pandas, numpy, math
import scipy.stats as stats

pairList = [ 
    {
        "title" : "GO",
        "count" : "data/09-an-annotation/speciesEnsembl/speciesEnsembl-GO-count.json",
        "hierarchical" : "data/dbgo-GOdatabase/tair-branchSummary.json",
        "description"  : "data/dbgo-GOdatabase/tair-description.json",
        "dividendTitle" : "[UP in ratio-sample1_vs_control]",
        "dividendPath" : "data/09-fa-GO-functionalAnalysis/testing1-dsStringtie-speciesEnsembl-trimQ30/testing1-condition1-FoldChange-1-significant.json",
        "divisorTitle" : "[UP in ratio-sample2_vs_control]",
        "divisorPath" : "data/09-fa-GO-functionalAnalysis/testing2-dsStringtie-speciesEnsembl-trimQ30/testing2-condition2-FoldChange-1-significant.json",
        "resultFolder" : "data/09-ft-FisherExactTest/",
        "resultFilename" : "GO-title.{typeStr}",
    },
    {
        "title" : "KEGG",
        "count" : "data/09-an-annotation/speciesEnsembl/speciesEnsembl-KEGG-count.json",
        "hierarchical" : "data/dbkg-KEGG-hirTree/ath00001-branchSummary.json",
        "description"  : "data/dbkg-KEGG-hirTree/ath00001-description.json",
        "dividendTitle" : "[UP in ratio-sample1_vs_control]",
        "dividendPath" : "data/09-fa-KEGG-functionalAnalysis/testing1-dsStringtie-speciesEnsembl-trimQ30/testing1-condition1-FoldChange-1-significant.json",
        "divisorTitle" : "[UP in ratio-sample2_vs_control]",
        "divisorPath" : "data/09-fa-KEGG-functionalAnalysis/testing2-dsStringtie-speciesEnsembl-trimQ30/testing2-condition2-FoldChange-1-significant.json",
        "resultFolder" : "data/09-ft-FisherExactTest/",
        "resultFilename" : "KEGG-title.{typeStr}",
    },
    {
        "title" : "TF",
        "count" : "data/09-an-annotation/speciesEnsembl/speciesEnsembl-TF-count.json",
        "hierarchical" : "",
        "description"  : "",
        "dividendTitle" : "[UP in ratio-sample1_vs_control]",
        "dividendPath" : "data/09-fa-TF-functionalAnalysis/testing1-dsStringtie-speciesEnsembl-trimQ30/testing1-condition1-FoldChange-1-significant.json",
        "divisorTitle" : "[UP in ratio-sample2_vs_control]",
        "divisorPath" : "data/09-fa-TF-functionalAnalysis/testing2-dsStringtie-speciesEnsembl-trimQ30/testing2-condition2-FoldChange-1-significant.json",
        "resultFolder" : "data/09-ft-FisherExactTest/",
        "resultFilename" : "TF-title.{typeStr}",
    },
]

for pairDict in pairList:
    titleStr = pairDict["title"]
    countDict = json.load(open(pairDict["count"],"r"))
    if pairDict["hierarchical"] != "":
        hierarchicalDict = json.load(open(pairDict["hierarchical"],'r'))
        hierarchicalBool = True
    else:
        hierarchicalDict = dict()
        hierarchicalBool = False

    if pairDict["description"] != "":
        descriptionDict = json.load(open(pairDict["description"],'r'))
        descriptionBool = True
    else:
        descriptionDict = dict()
        descriptionBool = False

    dividendTitleStr = pairDict["dividendTitle"]
    dividendDict = json.load(open(pairDict["dividendPath"],"r"))[dividendTitleStr]
    dividendSumDict = json.load(open(pairDict["dividendPath"],"r"))["# Involved Genes"]
    divisorTitleStr = pairDict["divisorTitle"]
    divisorDict = json.load(open(pairDict["divisorPath"],"r"))[divisorTitleStr]
    divisorSumDict = json.load(open(pairDict["divisorPath"],"r"))["# Involved Genes"]
    resultFolderStr = pairDict["resultFolder"]
    resultFilenameStr = pairDict["resultFilename"]
    resultDict = dict()

    # crossSet = set([ n for n in list(dividendDict.keys()) if n in list(divisorDict.keys()) ])
    combineList = list()
    combineList.extend(list(dividendDict.keys()))
    combineList.extend(list(divisorDict.keys()))
    combineSet = set(combineList)

    columnList = list()
    sumDict = dict()
    columnList.append("{} id".format(titleStr))
    sumDict.update({ "{} id".format(titleStr) : "Total genes with {} annotation".format(titleStr) })
    if hierarchicalBool:
        columnList.append("{} Path".format(titleStr))
        sumDict.update({ "{} Path".format(titleStr) : '' })
    if descriptionBool:
        columnList.append("{} Annotation".format(titleStr))
        sumDict.update({ "{} Annotation".format(titleStr) : '' })
    columnList.append("{} Sum".format(titleStr))
    sumDict.update({ "{} Sum".format(titleStr) : str(countDict["#SUM"]) })

    columnList.append(dividendTitleStr)
    dividendSumList = dividendSumDict.get(dividendTitleStr,list())
    dividendSumInt = len(dividendSumList)
    sumDict.update({ dividendTitleStr : str(dividendSumInt) })
    columnList.append(divisorTitleStr)
    divisorSumList = divisorSumDict.get(divisorTitleStr,list())
    divisorSumInt = len(divisorSumList)
    sumDict.update({ divisorTitleStr : str(divisorSumInt) })

    columnList.append("Odds ratio")
    sumDict.update({ "Odds ratio" : '' })
    columnList.append("Fisher's Exact Test (in log10)")
    sumDict.update({ "Fisher's Exact Test (in log10)" : '' })

    combineList = sorted(list(combineSet))
    resultDF = pandas.DataFrame(index=range(len(combineList)+1), columns=columnList)
    for keyStr in sumDict:
        resultDF.at[len(combineSet), keyStr] = sumDict[keyStr]

    for rowInt in range(len(combineList)):
        idStr = combineList[rowInt]
        resultSubDict = dict()

        dividendList = dividendDict.get(idStr,list())
        dividendCountInt = len(dividendList)
        divisorList = divisorDict.get(idStr,list())
        divisorCountInt = len(divisorList)
        oddsRatioFlt, pValueFlt = stats.fisher_exact([[dividendCountInt, divisorCountInt], [dividendSumInt-dividendCountInt, divisorSumInt-divisorCountInt]])

        if titleStr == "KEGG":
            resultDF.at[rowInt, "{} id".format(titleStr)] = "ko{}".format(idStr)
            resultSubDict["{} id".format(titleStr)] = "ko{}".format(idStr)
        else:
            resultDF.at[rowInt, "{} id".format(titleStr)] = idStr
            resultSubDict["{} id".format(titleStr)] = idStr
        
        if hierarchicalBool:
            resultDF.at[rowInt, "{} Path".format(titleStr)] = hierarchicalDict.get(idStr,"")
            resultSubDict["{} Path".format(titleStr)] = hierarchicalDict.get(idStr,"")
        if descriptionBool:
            resultDF.at[rowInt, "{} Annotation".format(titleStr)] = descriptionDict.get(idStr,"")
            resultSubDict["{} Annotation".format(titleStr)] = descriptionDict.get(idStr,"")
        
        resultDF.at[rowInt, "{} Sum".format(titleStr) ] = str(countDict[idStr])
        resultDF.at[rowInt, dividendTitleStr ] = dividendCountInt
        resultDF.at[rowInt, divisorTitleStr ] = divisorCountInt
        resultDF.at[rowInt, "Odds ratio" ] = oddsRatioFlt
        resultDF.at[rowInt, "Fisher's Exact Test (in log10)" ] = math.log10(pValueFlt)

        resultSubDict["{} Sum".format(titleStr)] = str(countDict[idStr])
        resultSubDict["dividendCountInt"] = dividendCountInt
        resultSubDict["divisorCountInt"] = divisorCountInt
        resultSubDict["dividendSumInt"] = dividendSumInt
        resultSubDict["divisorSumInt"] = divisorSumInt
        resultSubDict["Odds ratio"] = oddsRatioFlt
        resultSubDict["Fisher's Exact Test (in log10)"] = math.log10(pValueFlt)

        if titleStr == "KEGG":
            resultDict["ko{}".format(idStr)] = resultSubDict
        else:
            resultDict[idStr] = resultSubDict

    pathlib.Path( resultFolderStr ).mkdir(parents=True,exist_ok=True)
    resultDF.to_csv( resultFolderStr+resultFilenameStr.format(typeStr='tsv') , index=False, sep='\t', encoding='utf-8')
    with open(resultFolderStr+resultFilenameStr.format(typeStr='json'),'w') as targetHandle:
        json.dump(resultDict, targetHandle)
