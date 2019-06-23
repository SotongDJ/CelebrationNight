#!/usr/bin/env python3
import pandas as pd
import numpy as np
import sqlite3, json
import libPrint
# Declaration of sample-dependent variables
configList = [
    {
        "branch"  : ["testing1"],
        "method"  : ["dsStringtie"],
        "control" : "Control",
        "group"   : ["T1","T2","T3","T4","T5"], # without control
        "annotate" : "speciesTAIR",
        "compare"  : [["T1","T2"],["T3","T4"]],
        "trim"     : "trimQ30", 
    },
    {
        "branch"  : ["testing2","testing3"],
        "method"  : ["dsStringtie","waStringtie"],
        "control" : "Control",
        "group"   : ["S1","S2"], # without control
        "annotate" : "speciesEnsembl",
        "compare"  : [],
        "trim"     : "trimQ30", 
    },
]
sourceFilePathStr = 'data/06-cd-CuffDiff/{branch}-{method}/{annotate}-{trim}-geneExpression.db'
resultFilePathStr = 'data/06-cd-CuffDiff/{branch}-{method}/{annotate}-{trim}-expressionSummary'
referencePathStr = 'data/dbga-GenomeAnnotation/{annotate}/{annotate}-attributes.json'
logFolderPathStr = 'data/06-cd-CuffDiff/{branch}-{method}/'
logFilePathStr = '{annotate}-{trim}-expressionSummary'

for configDict in configList:    
    branchList  = configDict.get("branch",[])
    methodList  = configDict.get("method",[])
    controlStr  = configDict.get("control","")
    groupList   = configDict.get("group",[])
    compareList = configDict.get("compare",[])
    compareCStr = "; ".join([ "\t".join(sorted(x)) for x in compareList ])
    annotateStr = configDict.get("annotate","")
    trimStr     = configDict.get("trim","")
    
    descriDict  = json.load(open(referencePathStr.format(annotate=annotateStr),'r'))

    for branchStr in branchList:
        for methodStr in methodList:
            sourcePathStr = sourceFilePathStr.format(branch=branchStr,method=methodStr,annotate=annotateStr,trim=trimStr)
            resultPathStr = resultFilePathStr.format(branch=branchStr,method=methodStr,annotate=annotateStr,trim=trimStr)
            logFolderPath = logFolderPathStr.format(branch=branchStr,method=methodStr)
            logPathStr = logFilePathStr.format(branch=branchStr,method=methodStr,annotate=annotateStr,trim=trimStr)

            Print = libPrint.timer()
            Print.logFilenameStr = logPathStr
            Print.folderStr = logFolderPath
            Print.testingBool = False
            Print.startLog()

            Print.printing("branch = {branch}\nmethod = {method}\nannotate = {annotate}\ntrim = {trim}".format(branch=branchStr,method=methodStr,annotate=annotateStr,trim=trimStr))
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
                haveSignalBool = (fpkmAFlt > 0) or (fpkmBFlt > 0)
                if controlStr in sampleStr and haveSignalBool:
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
                        "fpkm-{}".format(aStr) : faFlt,
                        "fpkm-{}".format(bStr) : fbFlt,
                        "diff-{}_m_{}".format(bStr,aStr) : diFlt,
                        "ratio-{}_vs_{}".format(bStr,aStr) : fcFlt,
                        "pass-{}_vs_{}".format(bStr,aStr) : testStr,
                        "p-{}_vs_{}".format(bStr,aStr) : pvFlt,
                        "q-{}_vs_{}".format(bStr,aStr) : qvFlt,
                        "sig-{}_vs_{}".format(bStr,aStr) : sigStr,
                    }
                    subDict.update(inputDict)
                    columnSet.update(set(inputDict.keys()))
                    resultDict.update({ geneidStr : subDict })

                elif sampleStr in compareCStr and haveSignalBool:
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
                                "compare-{}_vs_{}".format(bStr,aStr) : fcFlt,
                                "diff-{}_m_{}".format(bStr,aStr) : diFlt,
                                "pass-{}_vs_{}".format(bStr,aStr) : testStr,
                                "p-{}_vs_{}".format(bStr,aStr) : pvFlt,
                                "q-{}_vs_{}".format(bStr,aStr) : qvFlt,
                                "sig-{}_vs_{}".format(bStr,aStr) : sigStr,
                            }
                            subDict.update(inputDict)
                            columnSet.update(set(inputDict.keys()))
                            resultDict.update({ geneidStr : subDict })


                countInt = countInt + 1
                print(countInt,end='\r')
            Print.printing("[Finish] scan throught {} lines (with \"OK\")".format(str(countInt)))
            Connect.close()

            Print.printing("[Organise] create list of column names")
            columnList = ['Gene_ID','Description']
            columnList.append("fpkm-{}".format(controlStr))
            columnList.extend(["fpkm-{}".format(x) for x in groupList])
            sampleSectionList = [
                "diff-{}_m_{}",
                "ratio-{}_vs_{}",
                "pass-{}_vs_{}",
                "p-{}_vs_{}",
                "q-{}_vs_{}",
                "sig-{}_vs_{}",
            ]
            for groupStr in groupList:
                for sampleSectionStr in sampleSectionList:
                    columnList.append(sampleSectionStr.format(groupStr,controlStr))
            
            compareSectionList = [
                "diff-{}_m_{}",
                "compare-{}_vs_{}",
                "pass-{}_vs_{}",
                "p-{}_vs_{}",
                "q-{}_vs_{}",
                "sig-{}_vs_{}",
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
                
                resultDF.at[rowInt, 'Description'] = descriDict.get(geneStr,np.NaN)

            Print.printing("[Export] export as expressionSummary.db")
            Connect = sqlite3.connect(resultPathStr+".db")
            resultDF.to_sql(name='Summary', con=Connect)
            Connect.commit()
            Connect.close()

            Print.printing("[Export] export as expressionSummary.tsv")
            resultDF.to_csv(resultPathStr+".tsv", index=False, sep='\t', encoding='utf-8')
            
            Print.stopLog()
            print("\n")
