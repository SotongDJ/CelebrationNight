#!/usr/bin/env python3
import pandas as pd
import numpy as np
import sqlite3
import libPrint

configList = [
    {
        "branch"  : "testing1",
        "method"  : ["dsStringtie","waStringtie"],
        "control" : "Control",
        "group"   : ["Control","T1","T2","T3","T4","T5"],
    },
    {
        "branch"  : "testing2",
        "method"  : ["dsStringtie","waStringtie"],
        "control" : "Control",
        "group"   : ["Control","S1","S2"],
    }
]
annotateStr = "speciesEnsembl"
trimStr = "trimQ30"

sourceFilePathStr = 'data/06-cd-CuffDiff/{branch}-{method}/{annotate}-{trim}-geneExpression.db'
resultFilePathStr = 'data/06-cd-CuffDiff/{branch}-{method}/{annotate}-{trim}-expressionSummary.db'
referencePathStr = 'data/dbga-GenomeAnnotation/speciesEnsembl/speciesEnsembl-attributes.db'
logFolderPathStr = 'data/06-cd-CuffDiff/{branch}-{method}/'
logFilePathStr = '{annotate}-{trim}-expressionSummary'

for configDict in configList:    
    branchStr = configDict.get("branch","")
    methodList = configDict.get("method",[])
    controlStr = configDict.get("control","")
    groupList = configDict.get("group",[])
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
        Print.printing("[SQL-load] open attribute database")
        Connect = sqlite3.connect(referencePathStr)
        Cursor = Connect.cursor()
        selectStr = " SELECT ID , description FROM Attributes;"
        attriExc = Cursor.execute(selectStr)

        Print.printing("[Convert] generating dictionary")
        descriDict = dict()
        countInt = 0
        for rowList in attriExc:
            idStr, descriStr = rowList
            if idStr != None and descriStr != None:
                if descriDict.get(idStr,"") == "":
                    descriDict.update({ idStr : descriStr })
                else:
                    descriDict.update({ idStr : "{}; {}".format(descriDict.get(idStr),descriStr) })
            countInt = countInt + 1
            print(countInt,end='\r')
        Print.printing("[Finish] scan throught {} lines".format(str(countInt)))
        Connect.close()

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
            sampleStr = sampleAStr+";"+sampleBStr
            testStr = tempList[7]
            fpkmAFlt = tempList[8]
            fpkmBFlt = tempList[9]
            foldFlt = tempList[10]
            pvFlt = tempList[12]
            qvFlt = tempList[13]
            sigStr = tempList[14]
            
            errorInt = 0
            subDict = resultDict.get(geneidStr,dict())
            if controlStr in sampleStr and testStr == 'OK':
                if sampleAStr == controlStr:
                    aStr = sampleAStr
                    bStr = sampleBStr
                    faFlt = fpkmAFlt
                    fbFlt = fpkmBFlt
                    fcFlt = foldFlt
                elif sampleBStr == controlStr:
                    aStr = sampleBStr
                    bStr = sampleAStr
                    faFlt = fpkmBFlt
                    fbFlt = fpkmAFlt
                    fcFlt = foldFlt * -1
                else:
                    errorInt = errorInt + 1
                    print("[ERROR{}:A!=Control,B!=Control]".format(str(errorInt)),end="\r")
                
                inputDict = {
                    "FPKM_{}".format(aStr) : faFlt,
                    "FPKM_{}".format(bStr) : fbFlt,
                    "foldChangeInLog2_{}".format(bStr) : fcFlt,
                    "pValue_{}".format(bStr) : pvFlt,
                    "qValue_{}".format(bStr) : qvFlt,
                    "significant_{}".format(bStr) : sigStr
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
        for n in groupList:
            if n == controlStr:
                columnList.append("FPKM_{}".format(n))
            else:
                columnList.extend([
                    "FPKM_{}".format(n),
                    "foldChangeInLog2_{}".format(n),
                    "pValue_{}".format(n),
                    "qValue_{}".format(n),
                    "significant_{}".format(n),
                ])
        
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
        Connect = sqlite3.connect(resultPathStr)
        resultDF.to_sql(name='Summary', con=Connect)
        Connect.commit()
        Connect.close()

        Print.stopLog()
        print("\n")