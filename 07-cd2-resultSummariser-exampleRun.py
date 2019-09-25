#!/usr/bin/env python3
import pandas as pd
import numpy as np
import sqlite3, json, pathlib
import libPrint
# Declaration of sample-dependent variables
configList = [
    {
        "branch"    : ["testing1"],
        "method"    : "dsStringtie",
        "control"   : "Control",
        "group"     : ["T1","T2","T3","T4","T5"], # without control
        "annotate"  : "speciesTAIR",
        "compare"   : [],
        "trim"      : "trimQ30", 
        "attribute" : {
            'description' : 'data/dbga-GenomeAnnotation/speciesTAIR/speciesTAIR-attributes.json',
        }
    },
    {
        "branch"    : ["testing2","testing3"],
        "method"    : "dsStringtie",
        "control"   : "Control",
        "group"     : ["S1","S2"], # without control
        "annotate"  : "speciesEnsembl",
        "compare"   : [["S1","S2"]],
        "trim"      : "trimQ30",  
        "attribute" : {
            'description' : 'data/dbga-GenomeAnnotation/speciesEnsembl/speciesEnsembl-attributes.json',
            'homolog' : 'data/dbga-GenomeAnnotation/speciesEnsembl/speciesEnsembl-homolog.json',
        }
    },
    {
        "branch"    : ["testing2","testing3"],
        "method"    : "waStringtie",
        "control"   : "Control",
        "group"     : ["S1","S2"], # without control
        "annotate"  : "speciesEnsembl",
        "compare"   : [["S1","S2"]],
        "trim"      : "trimQ30",  
        "attribute" : {
            'description' : 'data/dbga-GenomeAnnotation/speciesEnsembl/speciesEnsembl-attributes.json',
            'homolog' : 'data/dbga-GenomeAnnotation/speciesEnsembl/speciesEnsembl-homolog.json',
        }
    },
]

# Don't touch the code below if you don't know how it works
sourceFilePathStr = 'data/07-cd-CuffDiff/{branch}-{method}/{annotate}-{trim}-{targetType}Expression.db'
resultFilePathStr = 'data/07-cd-CuffDiff/{branch}-{method}/{annotate}-{trim}-{targetType}ExpressionSummary'
logFolderPathStr = 'data/07-cd-CuffDiff/{branch}-{method}/'
logFilePathStr = '{annotate}-{trim}-{targetType}ExpressionSummary'

for configDict in configList:    
    branchList    = configDict.get("branch",[])
    methodStr     = configDict.get("method","")
    annotateStr   = configDict.get("annotate","")
    trimStr       = configDict.get("trim","")
    targetTypeStr = configDict.get("targetType","")
    controlStr    = configDict.get("control","")
    groupList     = configDict.get("group",[])
    compareList   = configDict.get("compare",[])
    compareCStr   = "; ".join([ "\t".join(sorted(x)) for x in compareList ])
    attriDict     = configDict.get("attribute",dict())
    
    descriDict = dict()
    descriList = list(attriDict.keys())
    for labelStr in descriList:
        labelDict = json.load(open(attriDict[labelStr]))
        descriDict.update({ labelStr : labelDict })
    
    for branchStr in branchList:
        infoDict = {
            "branch"     : branchStr,
            "method"     : methodStr,
            "annotate"   : annotateStr,
            "trim"       : trimStr,
            "targetType" : targetTypeStr
        }
        sourcePathStr = sourceFilePathStr.format(**infoDict)
        resultPathStr = resultFilePathStr.format(**infoDict)
        logFolderPath = logFolderPathStr.format(**infoDict)
        logPathStr = logFilePathStr.format(**infoDict)

        Print = libPrint.timer()
        Print.logFilenameStr = logPathStr
        Print.folderStr = logFolderPath
        Print.testingBool = False
        Print.startLog()

        Print.printing("branch = {branch}\nmethod = {method}\nannotate = {annotate}\ntrim = {trim}\ntype = {targetType}".format(**infoDict))
        Print.printing("[SQL-load] open expression database")
        Connect = sqlite3.connect(sourcePathStr)
        Cursor = Connect.cursor()
        selectStr = "SELECT * FROM Expression"
        expExc = Cursor.execute(selectStr)

        Print.printing("[Compare] adjust combination")
        columnSet = {'Gene_ID'}
        resultDict = dict()
        countInt = 0
        for expList in expExc:
            tempList = list(expList)
            geneidStr = tempList[2]
            sampleAStr = tempList[5]
            sampleBStr = tempList[6]
            sampleStr = "\t".join(sorted([sampleAStr, sampleBStr]))
            testStr = tempList[7]
            fpkmAFlt = tempList[8]
            fpkmBFlt = tempList[9]
            foldFlt = tempList[10]
            pvFlt = tempList[12]
            qvFlt = tempList[13]
            sigStr = tempList[14]
            
            errorInt = 0
            subDict = resultDict.get(geneidStr,dict())
            # haveSignalBool = (fpkmAFlt > 0) or (fpkmBFlt > 0)
            # if controlStr in sampleStr and haveSignalBool:
            if controlStr in sampleStr:
                if sampleAStr == controlStr:
                    aStr = sampleAStr
                    bStr = sampleBStr
                    faFlt = fpkmAFlt
                    fbFlt = fpkmBFlt
                    fcFlt = foldFlt
                    diFlt = fbFlt - faFlt
                elif sampleBStr == controlStr:
                    aStr = sampleBStr
                    bStr = sampleAStr
                    faFlt = fpkmBFlt
                    fbFlt = fpkmAFlt
                    fcFlt = foldFlt * -1
                    diFlt = fbFlt - faFlt
                else:
                    errorInt = errorInt + 1
                    print("[ERROR{}:A!=Control,B!=Control]".format(str(errorInt)))
                
                inputDict = {
                    "fpkm：{}".format(aStr) : faFlt,
                    "fpkm：{}".format(bStr) : fbFlt,
                    "diff：{}－{}".format(bStr,aStr) : diFlt,
                    "ratio：{}／{}".format(bStr,aStr) : fcFlt,
                    "pass：{}／{}".format(bStr,aStr) : testStr,
                    "pVal：{}／{}".format(bStr,aStr) : pvFlt,
                    "qVal：{}／{}".format(bStr,aStr) : qvFlt,
                    "signi：{}／{}".format(bStr,aStr) : sigStr,
                }
                subDict.update(inputDict)
                columnSet.update(set(inputDict.keys()))
                resultDict.update({ geneidStr : subDict })

            # elif sampleStr in compareCStr and haveSignalBool:
            elif sampleStr in compareCStr:
                for compareSubList in compareList:
                    baseStr = compareSubList[0]
                    elemStr = compareSubList[1]
                    if (baseStr in sampleStr) and (elemStr in sampleStr):
                        if sampleAStr == baseStr:
                            aStr = sampleAStr
                            bStr = sampleBStr
                            faFlt = fpkmAFlt
                            fbFlt = fpkmBFlt
                            fcFlt = foldFlt
                            diFlt = fbFlt - faFlt
                        elif sampleBStr == baseStr:
                            aStr = sampleBStr
                            bStr = sampleAStr
                            faFlt = fpkmBFlt
                            fbFlt = fpkmAFlt
                            fcFlt = foldFlt * -1
                            diFlt = fbFlt - faFlt
                        else:
                            errorInt = errorInt + 1
                            print("[ERROR{}:A!=Control,B!=Control]".format(str(errorInt)))
                        
                        inputDict = {
                            "compare：{}／{}".format(bStr,aStr) : fcFlt,
                            "diff：{}－{}".format(bStr,aStr) : diFlt,
                            "pass：{}／{}".format(bStr,aStr) : testStr,
                            "pVal：{}／{}".format(bStr,aStr) : pvFlt,
                            "qVal：{}／{}".format(bStr,aStr) : qvFlt,
                            "signi：{}／{}".format(bStr,aStr) : sigStr,
                        }
                        subDict.update(inputDict)
                        columnSet.update(set(inputDict.keys()))
                        resultDict.update({ geneidStr : subDict })

            countInt = countInt + 1
            print("[{}]".format(countInt),end='\r')
        
        print("")
        Print.printing("[Finish] scan throught {} lines (with \"OK\")".format(str(countInt)))
        Connect.close()

        Print.printing("[Organise] create list of column names")
        columnList = ['Gene_ID']
        columnList.extend(descriList)
        columnList.append("fpkm：{}".format(controlStr))
        columnList.extend(["fpkm：{}".format(x) for x in groupList])
        sampleSectionList = [
            "diff：{}－{}",
            "ratio：{}／{}",
            "pass：{}／{}",
            "pVal：{}／{}",
            "qVal：{}／{}",
            "signi：{}／{}",
        ]
        for groupStr in groupList:
            for sampleSectionStr in sampleSectionList:
                columnList.append(sampleSectionStr.format(groupStr,controlStr))
        
        compareSectionList = [
            "diff：{}－{}",
            "compare：{}／{}",
            "pass：{}／{}",
            "pVal：{}／{}",
            "qVal：{}／{}",
            "signi：{}／{}",
        ]
        for compareSubList in compareList:
            for compareSectionStr in compareSectionList:
                baseStr = compareSubList[0]
                elemStr = compareSubList[1]
                columnList.append(compareSectionStr.format(elemStr,baseStr))

        Print.printing("[Arrange] fill the values into DataFrame")
        geneList = list(resultDict.keys())
        resultDF = pd.DataFrame(index=range(len(geneList)), columns=columnList)
        for rowInt in range(len(geneList)):
            print("[{}/{}]".format(str(rowInt),str(len(geneList))),end="\r")
            geneStr = geneList[rowInt]
            resultDF.at[rowInt, 'Gene_ID'] = geneStr
            valueDict = resultDict[geneList[rowInt]]
            for titleStr in [ x for x in columnList if x != 'Gene_ID' ]:
                resultDF.at[rowInt, titleStr] = valueDict.get(titleStr,np.NaN)
            
            for labelStr in descriList:
                resultDF.at[rowInt, labelStr] = descriDict.get(labelStr,dict()).get(geneStr,np.NaN)
        
        print("")
        Print.printing("[Export] export as expressionSummary.db")
        if pathlib.Path(resultPathStr+".db").exists():
            pathlib.Path(resultPathStr+".db").unlink()
        Connect = sqlite3.connect(resultPathStr+".db")
        resultDF.to_sql(name='Summary', con=Connect)
        Connect.commit()
        Connect.close()

        Print.printing("[Export] export as expressionSummary.tsv")
        resultDF.to_csv(resultPathStr+".tsv", index=False, sep='\t', encoding='utf-8')
        
        Print.stopLog()
        print("\n")
