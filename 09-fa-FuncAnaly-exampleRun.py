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
            "annotate" : "speciesEnsembl",
            "trim" : "trimQ30",
            # use Arabidopsis homolog id instead of species geneid
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
            pathBool = True
        else:
            pathDict = dict()
            pathBool = False

        if databaseDict["description"] != "":
            descriDict = json.load(open(databaseDict["description"],'r'))
            descriBool = True
        else:
            descriDict = dict()
            descriBool = False

        for typeStr in ["significant","comparison"]:
            stringDict.update({ "type" : typeStr })
            stringDict.update({ "database" : databaseStr })
            detailPathStr = 'data/07-cd-CuffDiff/{branch}-{method}/{annotate}-{trim}-expressionSummary.db'
            detailPath = detailPathStr.format(**stringDict)
            groupPathStr = 'data/08-grouping/{branch}-{method}-{annotate}-{trim}/{branch}-{title}-{level}-list-{type}.json'
            groupPath = groupPathStr.format(**stringDict)

            Connect = sqlite3.connect(detailPath)
            expressionDF = pd.read_sql_query("SELECT * FROM Summary", Connect)
            expressionDict = expressionDF.set_index('Gene_ID').T.to_dict('dict')
            groupDict = json.load(open(groupPath,'r'))

            # --- Directory confirmation ---
            pathlib.Path( "data/09-fa-{database}-functionalAnalysis/{branch}-{method}-{annotate}-{trim}/".format(**stringDict) ).mkdir(parents=True,exist_ok=True)

            foldchangeDict = dict()
            sumDict = dict()
            compareList = []
            absenceList = []
            #
            print("Target: "+levelStr)
            print("Step 0: Check combination")
            for compare in columnList:
                if compare in set(groupDict.keys()):
                    compareList.append(compare)
                else:
                    absenceList.append(compare)

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
                            detailDict = expressionDict[gene]

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

            targetFilenameStr = "data/09-fa-{database}-functionalAnalysis/{branch}-{method}-{annotate}-{trim}/{branch}-{title}-FoldChange-{level}-{type}.json".format(**stringDict)
            with open(targetFilenameStr,'w') as resultFile:
                json.dump(foldchangeDict,resultFile,indent=2,sort_keys=True)

            print("Step 3: Generating TSV files")

            targetFilenameStr = "data/09-fa-{database}-functionalAnalysis/{branch}-{method}-{annotate}-{trim}/{branch}-{title}-FoldChange-{level}-{type}.tsv".format(**stringDict)
            with open(targetFilenameStr,'w') as resultFile:
                columnTup = tuple(sorted(compareList))

                headerList = list()
                calculationList = list()
                headerList.append("{} id".format(databaseStr))
                calculationList.append("Total genes with {} annotation".format(databaseStr))
                if pathBool:
                    headerList.append("{} Path".format(databaseStr))
                    calculationList.append('')
                if descriBool:
                    headerList.append("{} Annotation".format(databaseStr))            
                    calculationList.append('')
                headerList.append("{} Sum".format(databaseStr))
                calculationList.append(str(countDict["#SUM"]))

                resultFile.write("\t".join(headerList))
                resultFile.write("\t")
                resultFile.write("\t".join([ n.replace("_"," ") for n in columnTup ]))
                resultFile.write("\t")
                resultFile.write("\t".join(absenceList))
                resultFile.write("\n")
                
                sumList = [ str(sumDict.get(x,'irrelevant')) for x in columnTup ]
                calculationList.extend(sumList)
                resultFile.write("\t".join(calculationList))
                resultFile.write("\t")
                resultFile.write("\t".join([ 'absence' for x in absenceList ]))
                resultFile.write("\n")
                
                for termID in list(t2geneDict.keys()):
                    valueIdentityList = list()
                    valueIdentityList.append(termID)
                    if pathBool:
                        valueIdentityList.append(pathDict.get(termID,'NONE'))

                    if descriBool:
                        valueIdentityList.append(descriDict.get(termID,'NONE'))  

                    valueIdentityList.append(str(countDict[termID]))

                    resultFile.write("\t".join(valueIdentityList))
                    resultFile.write("\t")

                    valueNumberList = list()
                    # colName = name of compare combination
                    valueNumberList = [str(len(foldchangeDict[colName].get(termID,[]))) for colName in columnTup]
                    
                    resultFile.write("\t".join(valueNumberList))
                    resultFile.write("\n")

            print("Finish\n")
