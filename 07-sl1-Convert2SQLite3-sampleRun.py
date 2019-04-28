import pathlib
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

branchStr = "testing"
conditionList = [("speciesTestingA","trimQ20"),("speciesTestingA","trimQ30")]
controlStr = "Controlr1"
sampleList = ["Controlr1","T1r1","T2r1","T3r1","T4r1","T5r1"]
compareSet = set()

for conditionTup in conditionList:
    antStr = conditionTup[0]
    trimStr = conditionTup[1]
    for sampleStr in sampleList:
        pathStr = "data/05-stringtie2/{branch}/{ant}-{trim}/{sample}-expression.tsv"
        samplePath = pathStr.format(branch=branchStr,ant=antStr,trim=trimStr,sample=sampleStr)
        sampleDF = pd.read_csv(samplePath,delimiter="\t",header=0)
        print("[Pandas]\n    "+pathStr)
        
        rowList = sampleDF.values.tolist()
        countInt = len(rowList)
        
        # check
        compareList = list()
        for rowInt in range(countInt):
            insertList = []
            sourceList = rowList[rowInt]
            insertList.append("UUID."+str(rowInt))
            insertList.extend(sourceList[0:7])
            compareStr = "\t".join([str(x) for x in insertList])
            compareList.append(compareStr)
        
        if compareSet == set():
            print("    "+sampleStr+": Empty")
            compareSet = set(compareList)
        elif compareSet != set(compareList):
            print("    "+sampleStr+": same")
        elif compareSet == set(compareList):
            print("    "+sampleStr+": different")

        pathlib.Path( "data/07-expressionTable-SQLite3/{}/".format(branchStr) ).mkdir(parents=True,exist_ok=True)
        fileStr = 'data/07-expressionTable-SQLite3/{branch}/Expression-{ant}-{trim}.db'
        filePath = fileStr.format(branch=branchStr,ant=antStr,trim=trimStr)
        Connect = sqlite3.connect(filePath)
        print("[SQLite3]\n    "+filePath)
        Cursor = Connect.cursor()
        ReturnMsg = Cursor.execute("""CREATE TABLE {}_Expression
                    ('UUID'  TEXT    PRIMARY KEY NOT NULL, 
                    'GeneID'   TEXT    NOT NULL,
                    'GeneName' TEXT    NOT NULL, 
                    'Reference' TEXT    NOT NULL, 
                    'Strand'    TEXT    NOT NULL, 
                    'Start' INTEGER NOT NULL, 
                    'End'   INTEGER NOT NULL, 
                    'Coverage'  REAL    NOT NULL, 
                    'FPKM'  REAL    NOT NULL, 
                    'TPM'   REAL    NOT NULL);""".format(sampleStr))
        Connect.commit()

        insertComStr = "INSERT INTO {}_Expression ('UUID','GeneID','GeneName','Reference','Strand','Start','End','Coverage','FPKM','TPM')\
                        VALUES (?,?,?,?,?,?,?,?,?,?)".format(sampleStr)
        for rowInt in range(countInt):
            insertList = []
            sourceList = rowList[rowInt]
            insertList.append("UUID."+str(rowInt))       
            insertList.extend(sourceList)
            ReturnMsg = Cursor.execute(insertComStr,insertList)

        Connect.commit()
        Connect.close()

    createComStr = "CREATE TABLE ExpressionSummary ({})"
    createColumnList = [
        "'UUID'  TEXT PRIMARY KEY NOT NULL", 
        "'GeneID' TEXT",
        "'GeneName' TEXT",
    ]
    insertColumnList = ["UUID", "GeneID", "GeneName"]
    for targetStr in ["FPKM","TPM"]:
        for sampleStr in sampleList:
            columnStr = "{target}_{sample} REAL".format(target=targetStr,sample=sampleStr)
            createColumnList.append(columnStr)
            insertColumnList.append("{target}_{sample}".format(target=targetStr,sample=sampleStr))

    fileStr = 'data/07-expressionTable-SQLite3/{branch}/Expression-{ant}-{trim}.db'
    filePath = fileStr.format(branch=branchStr,ant=antStr,trim=trimStr)
    Connect = sqlite3.connect(filePath)
    print("[SQLite3]\n    "+filePath)
    Cursor = Connect.cursor()
    ReturnMsg = Cursor.execute(createComStr.format(",".join(createColumnList)))
    Connect.commit()

    resultDict = dict()
    controlExc = Cursor.execute("SELECT UUID, GeneID, GeneName from {}_Expression".format(controlStr))
    for rowList in controlExc:
        uuid, geneid, genename = rowList
        subDict = {
            "UUID" : uuid,
            "GeneID" : geneid,
            "GeneName" : genename
        }
        resultDict.update({ uuid : subDict })


    for sampleStr in sampleList:
        sampleExc = Cursor.execute("SELECT UUID, FPKM, TPM  from {}_Expression".format(sampleStr))
        for rowList in sampleExc:
            uuid, fpkm, tpm = rowList
            subDict = resultDict[uuid]
            subDict.update({
                "FPKM_{}".format(sampleStr) : fpkm,
                "TPM_{}".format(sampleStr) : tpm
            })
            resultDict.update({ uuid : subDict })


    insertComStr = "INSERT INTO ExpressionSummary ({column}) VALUES ({value})"
    a = 0
    for uuid in resultDict.keys():
        valueList = list()
        for posInt in range(len(insertColumnList)):
            valueList.append(resultDict[uuid][insertColumnList[posInt]])

        insertCommand = insertComStr.format(column=",".join(insertColumnList),value=(("?,"*(len(valueList)-1)))+"?")
        ReturnMsg = Cursor.execute(insertCommand,valueList)

    Connect.commit()
    Connect.close()