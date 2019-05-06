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
geneExpPathStr = "data/05-ds-stringtie2/{branch}/{ant}-{trim}/{sample}-expression.tsv"
transcriptExpPathStr = "data/05-ds-ballgown/{branch}/{ant}-{trim}-{sample}/t_data.ctab"
sqlFolderStr = "data/07-sl-expressionTable-SQLite3/{branch}-ds/"
pathlib.Path( sqlFolderStr.format(branch=branchStr) ).mkdir(parents=True,exist_ok=True)
sqlPathStr = 'data/07-sl-expressionTable-SQLite3/{branch}-ds/Expression-{ant}-{trim}.db'

for conditionTup in conditionList:
    antStr = conditionTup[0]
    trimStr = conditionTup[1]
    for sampleStr in sampleList:
        print("-- Data format conversion for Gene Expression --")
        geneSamplePath = geneExpPathStr.format(
                branch=branchStr,
                ant=antStr,
                trim=trimStr,
                sample=sampleStr
            )
        sampleDF = pd.read_csv(geneSamplePath,delimiter="\t",header=0)
        print("[Pandas:Read]"+geneSamplePath)
        
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
            print("    "+sampleStr+": Same")
        elif compareSet == set(compareList):
            print("    "+sampleStr+": Different")

        sqlPath = sqlPathStr.format(branch=branchStr,ant=antStr,trim=trimStr)
        Connect = sqlite3.connect(sqlPath)
        Cursor = Connect.cursor()
        ReturnMsg = Cursor.execute("""CREATE TABLE GeneExpression_{}
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
        print("[SQLite3:CreateTable] "+sqlPath)

        insertComStr = "INSERT INTO GeneExpression_{} ('UUID','GeneID','GeneName','Reference','Strand','Start','End','Coverage','FPKM','TPM')\
                        VALUES (?,?,?,?,?,?,?,?,?,?)".format(sampleStr)
        for rowInt in range(countInt):
            insertList = []
            sourceList = rowList[rowInt]
            insertList.append("UUID."+str(rowInt))       
            insertList.extend(sourceList)
            ReturnMsg = Cursor.execute(insertComStr,insertList)

        Connect.commit()
        print("[SQLite3:Insert] "+sqlPath)
        Connect.close()
        print("[SQLite3:Close]\n")

        # Transcript
        print("-- Data format conversion for Transcript Expression --")

        transcriptSamplePath = transcriptExpPathStr.format(
                branch=branchStr,
                ant=antStr,
                trim=trimStr,
                sample=sampleStr
            )
        sampleDF = pd.read_csv(transcriptSamplePath,delimiter="\t",header=0)
        print("[Pandas:Read] "+transcriptSamplePath)
        
        rowList = sampleDF.values.tolist()
        countInt = len(rowList)
        
        # check
        compareList = list()
        for rowInt in range(countInt):
            insertList = []
            sourceList = rowList[rowInt]
            insertList.append("UUID."+str(rowInt))
            insertList.extend(sourceList[0:10])
            compareStr = "\t".join([str(x) for x in insertList])
            compareList.append(compareStr)
        
        if compareSet == set():
            print("    "+sampleStr+": Empty")
            compareSet = set(compareList)
        elif compareSet != set(compareList):
            print("    "+sampleStr+": Same")
        elif compareSet == set(compareList):
            print("    "+sampleStr+": Different")

        sqlPath = sqlPathStr.format(branch=branchStr,ant=antStr,trim=trimStr)
        Connect = sqlite3.connect(sqlPath)
        Cursor = Connect.cursor()
        ReturnMsg = Cursor.execute("""CREATE TABLE TranscriptExpression_{}
                    ('UUID'     TEXT    PRIMARY KEY NOT NULL, 
                    'TranscriptID'  INTEGER    NOT NULL,
                    'Chromosome'    TEXT, 
                    'Strand'    TEXT    NOT NULL, 
                    'Start' INTEGER NOT NULL, 
                    'End'   INTEGER NOT NULL, 
                    'TranscriptName'    TEXT    NOT NULL, 
                    'ExonCount'    INTEGER  NOT NULL, 
                    'Length'    INTEGER  NOT NULL, 
                    'GeneID'    TEXT  NOT NULL, 
                    'GeneName'    TEXT  NOT NULL, 
                    'Coverage'  REAL    NOT NULL, 
                    'FPKM'  REAL    NOT NULL);""".format(sampleStr))
        Connect.commit()
        print("[SQLite3:CreateTable] "+sqlPath)

        insertComStr = "INSERT INTO TranscriptExpression_{} ('UUID','TranscriptID','Chromosome','Strand','Start','End','TranscriptName','ExonCount','Length','GeneID','GeneName','Coverage','FPKM')\
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)".format(sampleStr)
        for rowInt in range(countInt):
            insertList = []
            sourceList = rowList[rowInt]
            insertList.append("UUID."+str(rowInt))       
            insertList.extend(sourceList)
            ReturnMsg = Cursor.execute(insertComStr,insertList)

        Connect.commit()
        print("[SQLite3:Insert] "+sqlPath)
        Connect.close()
        print("[SQLite3:Close]\n")

    print("-- Summarising for Gene Expression --")
    createComStr = "CREATE TABLE GeneExpressionSummary ({})"
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

    Connect = sqlite3.connect(sqlPath)
    Cursor = Connect.cursor()
    ReturnMsg = Cursor.execute(createComStr.format(",".join(createColumnList)))
    Connect.commit()
    print("[SQLite3:CreateTable] "+sqlPath)

    resultDict = dict()
    controlExc = Cursor.execute("SELECT UUID, GeneID, GeneName from GeneExpression_{}".format(controlStr))
    for rowList in controlExc:
        uuid, geneid, genename = rowList
        subDict = {
            "UUID" : uuid,
            "GeneID" : geneid,
            "GeneName" : genename
        }
        resultDict.update({ uuid : subDict })


    for sampleStr in sampleList:
        sampleExc = Cursor.execute("SELECT UUID, FPKM, TPM  from GeneExpression_{}".format(sampleStr))
        for rowList in sampleExc:
            uuid, fpkm, tpm = rowList
            subDict = resultDict[uuid]
            subDict.update({
                "FPKM_{}".format(sampleStr) : fpkm,
                "TPM_{}".format(sampleStr) : tpm
            })
            resultDict.update({ uuid : subDict })


    insertComStr = "INSERT INTO GeneExpressionSummary ({column}) VALUES ({value})"
    a = 0
    for uuid in resultDict.keys():
        valueList = list()
        for posInt in range(len(insertColumnList)):
            valueList.append(resultDict[uuid][insertColumnList[posInt]])

        insertCommand = insertComStr.format(column=",".join(insertColumnList),value=(("?,"*(len(valueList)-1)))+"?")
        ReturnMsg = Cursor.execute(insertCommand,valueList)

    Connect.commit()
    print("[SQLite3:Insert] "+sqlPath)
    Connect.close()
    print("[SQLite3:Close]\n")

    # Transcript
    print("-- Summarising for Transcript Expression --")
    createComStr = "CREATE TABLE TranscriptExpressionSummary ({})"
    createColumnList = [
        "'UUID'  TEXT PRIMARY KEY NOT NULL", 
        "'TranscriptID' INTEGER",
        "'TranscriptName' TEXT",
        "'GeneID' TEXT",
        "'GeneName' TEXT",
    ]
    insertColumnList = ["UUID", "TranscriptID", "TranscriptName", "GeneID", "GeneName"]
    for sampleStr in sampleList:
        columnStr = "FPKM_{sample} REAL".format(sample=sampleStr)
        createColumnList.append(columnStr)
        insertColumnList.append("FPKM_{sample}".format(sample=sampleStr))

    Connect = sqlite3.connect(sqlPath)
    Cursor = Connect.cursor()
    ReturnMsg = Cursor.execute(createComStr.format(",".join(createColumnList)))
    Connect.commit()
    print("[SQLite3:CreateTable] "+sqlPath)

    resultDict = dict()
    controlExc = Cursor.execute("SELECT UUID, TranscriptID, TranscriptName, GeneID, GeneName from TranscriptExpression_{}".format(controlStr))
    for rowList in controlExc:
        uuid, tid, tname, geneid, genename = rowList
        subDict = {
            "UUID" : uuid,
            "TranscriptID" : tid,
            "TranscriptName" : tname,
            "GeneID" : geneid,
            "GeneName" : genename
        }
        resultDict.update({ uuid : subDict })


    for sampleStr in sampleList:
        sampleExc = Cursor.execute("SELECT UUID, FPKM  from TranscriptExpression_{}".format(sampleStr))
        for rowList in sampleExc:
            uuid, fpkm = rowList
            subDict = resultDict[uuid]
            subDict.update({
                "FPKM_{}".format(sampleStr) : fpkm
            })
            resultDict.update({ uuid : subDict })


    insertComStr = "INSERT INTO TranscriptExpressionSummary ({column}) VALUES ({value})"
    a = 0
    for uuid in resultDict.keys():
        valueList = list()
        for posInt in range(len(insertColumnList)):
            valueList.append(resultDict[uuid][insertColumnList[posInt]])

        insertCommand = insertComStr.format(column=",".join(insertColumnList),value=(("?,"*(len(valueList)-1)))+"?")
        ReturnMsg = Cursor.execute(insertCommand,valueList)

    Connect.commit()
    print("[SQLite3:Insert] "+sqlPath)
    Connect.close()
    print("[SQLite3:Close]\n")
