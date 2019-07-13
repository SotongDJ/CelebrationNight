#!/usr/bin/env python3
import libPrint
import pathlib, sqlite3, json
import pandas as pd
import numpy as np

sampleList = [
    {
        "string": {
            "branch" : "testing1",
            "method" : "dsStringtie",
            "annotate" : "brapaEnsembl",
            "trim" : "trimQ30",
            "title" : "homoDEG",
            "level" : "1",
            "type" : "significant",
            "compare" : [
                "[DOWN in compare-T2_vs_T1]_and_[UP in ratio-T1_vs_Control]",
                "[DOWN in ratio-T1_vs_Control]_and_[UP in compare-T2_vs_T1]",
                "[MINOR in compare-T2_vs_T1]_and_[UP in ratio-T1_vs_Control]",
                "[DOWN in ratio-T1_vs_Control]_and_[MINOR in compare-T2_vs_T1]",
            ],
        },
        "condition" : {
            "GO" : {
                "gene2term"    : "data/dbgo-GOdatabase/tair-gene2term.json",
                "term2gene"    : "data/dbgo-GOdatabase/tair-term2gene.json",
                "count"        : "data/dbgo-GOdatabase/tair-count.json",
                "hierarchical" : "data/dbgo-GOdatabase/tair-branchSummary.json",
                "description"  : "data/dbgo-GOdatabase/tair-description.json",
            },
            "KEGG" : {
                "gene2term"    : "data/dbkg-KEGG-hirTree/ath00001-gene2term.json",
                "term2gene"    : "data/dbkg-KEGG-hirTree/ath00001-term2gene.json",
                "count"        : "data/dbkg-KEGG-hirTree/ath00001-count.json",
                "hierarchical" : "data/dbkg-KEGG-hirTree/ath00001-branchSummary.json",
                "description"  : "data/dbkg-KEGG-hirTree/ath00001-description.json",
            },
            "TF": {
                "gene2term"     : "data/dbtf-TFdb/at-tf-gene2term.json",
                "term2gene"     : "data/dbtf-TFdb/at-tf-term2gene.json",
                "count"         : "data/dbtf-TFdb/at-tf-count.json",
                "hierarchical"  : "",
                "description"   : "",
            },
        }
    },
]

for sampleDict in sampleList:
    stringDict = sampleDict["string"]
    for databaseStr in list(sampleDict["condition"].keys()):
        databaseDict = sampleDict["condition"][databaseStr]

        levelStr = stringDict["level"]
        columnList = stringDict["compare"]
        branchStr = stringDict["branch"]
        titleStr = stringDict["title"]

        g2termDict = json.load(open(databaseDict["gene2term"],'r'))
        t2geneDict = json.load(open(databaseDict["term2gene"],'r'))
        countDict = json.load(open(databaseDict["count"],'r'))
        if databaseDict["hierarchical"] != "":
            pathDict = json.load(open(databaseDict["hierarchical"],'r'))
        else:
            pathDict = dict()

        if databaseDict["description"] != "":
            descriDict = json.load(open(databaseDict["description"],'r'))
        else:
            descriDict = dict()

        detailPathStr = 'data/06-cd-CuffDiff/{branch}-{method}/{annotate}-{trim}-expressionSummary.db'
        detailPath = detailPathStr.format(**stringDict)
        groupPathStr = 'data/08-grouping/{branch}-{method}-{annotate}-{trim}/{branch}-{title}-{level}-list-{type}.json'
        groupPath = groupPathStr.format(**stringDict)

        # expressionDict = json.load(open(detailPathStr,'r'))
        groupDict      = json.load(open(groupPath,'r'))

        # --- Directory confirmation ---
        pathlib.Path( 'data/09fa-{}-functionalAnalysis'.format(databaseStr) ).mkdir(parents=True,exist_ok=True)
        pathlib.Path( "data/09fa-{}-functionalAnalysis/{}-{}".format(databaseStr, branchStr, titleStr) ).mkdir(parents=True,exist_ok=True)

        foldchangeDict = dict()
        sumDict = dict()
        compareList = []
        #
        print("Fold Change: "+levelStr)
        print("Step 0: Check combination")
        for compare in columnList:
            if compare in set(groupDict.keys()):
                compareList.append(compare)
            else:
                print("    {} doesn't appeared in DEG libraries".format(compare))

        print("Step 1: Comparing "+databaseStr)
        for compare in compareList:
            compareDict = dict()
            targetSet = set(groupDict[compare])
            #
            totalCountStr = str(len(targetSet))
            countInt = 0
            #
            for gene in targetSet:
                #
                countInt = countInt + 1
                print("{}:[{}/{}]{}".format(compare,str(countInt),totalCountStr,gene),end="\r")
                #
                if gene in set(g2termDict.keys()):
                    for termID in g2termDict[gene]:
                        # detailDict = expressionDict[gene]
                        detailDict = dict()

                        tempList = compareDict.get(termID,[])
                        tempList.append(detailDict)
                        compareDict.update({ termID : tempList })

                    tempList = sumDict.get(compare,[])
                    tempList.append(gene)
                    sumDict.update({ compare : list(set(tempList)) })

            foldchangeDict.update({ compare : compareDict })

        for compare in list(sumDict.keys()):
            sumDict.update({ compare : len(sumDict[compare]) })

        foldchangeDict.update({ "#SUM" : sumDict })

        print("")
        print("Step 2: Exporting results into JSON files")

        targetFilenameStr = "data/09fa-{databaseStr}-functionalAnalysis/{branchStr}-{titleStr}/FoldChange-{foldStr}.json".format(
            databaseStr=databaseStr,
            branchStr=branchStr,
            titleStr=titleStr,
            foldStr=levelStr
        )
        with open(targetFilenameStr,'w') as resultFile:
            json.dump(foldchangeDict,resultFile,indent=2,sort_keys=True)

        print("Step 3: Generating TSV files")

        targetFilenameStr = "data/09fa-{databaseStr}-functionalAnalysis/{branchStr}-{titleStr}/FoldChange-{foldStr}.tsv".format(
            databaseStr=databaseStr,
            branchStr=branchStr,
            titleStr=titleStr,
            foldStr=levelStr,
        )
        with open(targetFilenameStr,'w') as resultFile:
            columnTup = tuple(compareList)
            pathBool = (pathDict != dict())
            descriBool = (descriDict != dict())

            columnHeaderList = list()
            footerList = list()
            columnHeaderList.append("{} id".format(databaseStr))
            footerList.append("Total genes with {} annotation".format(databaseStr))
            if pathBool:
                columnHeaderList.append("{} Path".format(databaseStr))
                footerList.append('')
            if descriBool:
                columnHeaderList.append("{} Annotation".format(databaseStr))            
                footerList.append('')
            columnHeaderList.append("{} Sum".format(databaseStr))

            columnStr = "{}\t{}\n".format( "\t".join(columnHeaderList), "\t".join(columnTup))
            resultFile.write(columnStr)
            
            for termID in list(t2geneDict.keys()):
                valueList = list()
                valueList.append(termID)
                if pathBool:
                    valueList.append(pathDict.get(termID,'NONE'))
                if descriBool:
                    valueList.append(descriDict.get(termID,'NONE'))            
                valueList.append(str(countDict[termID]))

                resultFile.write("\t".join(valueList))

                for colName in columnTup: # colName = name of compare combination
                    resultFile.write(str(len(foldchangeDict[colName].get(termID,[])))+"\t")
                resultFile.write("\n")

            sumTup = tuple([ str(sumDict.get(x,'NONE')) for x in compareList])
            
            footerList.append(str(countDict["#SUM"]))
            footerList.extend(sumTup)
            resultFile.write("\t".join(footerList))

        print("Finish\n")