import pathlib, sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import libConfig, libPrint

class sqlImporter:
    def __init__(self):
        self.branchStr = ""
        self.testingBool = False
        self.expressionInputDict = {
            "sqlPath" : str(),
            "count" : int(),
            "rowList" : list(),
            "createCommand" : str(),
            "insertCommand" : str(),
        }
    
    def exportingExpression(self,clPrint):
        sqlPath = self.expressionInputDict.get("sqlPath",str())
        countInt = self.expressionInputDict.get("count",int())
        rowList = self.expressionInputDict.get("rowList",list())
        createCommandStr = self.expressionInputDict.get("createCommand",str())
        insertCommandStr = self.expressionInputDict.get("insertCommand",str())
    
        Connect = sqlite3.connect(sqlPath)
        Cursor = Connect.cursor()
        clPrint.printing("[SQLite3:CreateTable] "+sqlPath)
        ReturnMsg = Cursor.execute(createCommandStr)
        Connect.commit()
        clPrint.printing("[SQLite3:FinishCreating]")

        for rowInt in range(countInt):
            insertList = []
            sourceList = rowList[rowInt]
            insertList.append("UUID."+str(rowInt))       
            insertList.extend(sourceList)
            ReturnMsg = Cursor.execute(insertCommandStr,insertList)       

        Connect.commit()
        clPrint.printing("[SQLite3:Insert] "+sqlPath)
        Connect.close()
        clPrint.printing("[SQLite3:Close]\n")

        self.expressionInputDict = {
            "sqlPath" : str(),
            "count" : int(),
            "rowList" : list(),
            "createCommand" : str(),
            "insertCommand" : str(),
        }

    def importing(self):
        # ---- Initialization for Converting ----
        Target = libConfig.config()
        Target.queryStr = self.branchStr
        Target.folderStr = "config/"
        Target.modeStr = "UPDATE"
        Target.load()

        branchStr = self.branchStr

        controlStr = Target.storeDict.get("controlSample","")
        groupList = Target.storeDict.get("group",[])
        replicationList = Target.storeDict.get("replication",[])
        patternStr = Target.storeDict.get("samplePattern","")

        sampleList = list()
        for groupStr in groupList:
            for replicationStr in replicationList:
                sampleList.append(patternStr.format(group=groupStr,replication=replicationStr))

        conditionList = Target.storeDict.get("conditionList",[])
        methodList = Target.storeDict.get("methodList",[])
        geneSourceDict = Target.storeDict.get("[sqlite]geneSourceDict",dict())
        transcriptSourceDict = Target.storeDict.get("[sqlite]transcriptSourceDict",dict())

        geneExpPathStr = Target.storeDict.get("[sqlite]geneSourcePathStr","")
        transcriptExpPathStr = Target.storeDict.get("[sqlite]transcriptSourcePathStr","")
        sqlFolderStr = Target.storeDict.get("sqlFolderStr","")
        sqlPathStr = Target.storeDict.get("sqlPathStr","")
        sqlLogStr = Target.storeDict.get("[sqlite]logFilename","")

        for methodStr in methodList:
            pathlib.Path( sqlFolderStr.format(branch=branchStr,method=methodStr) ).mkdir(parents=True,exist_ok=True)
            geneFolderStr = geneSourceDict.get(methodStr,"")
            transcriptFolderStr = transcriptSourceDict.get(methodStr,"")
            compareSet = set()

            for conditionTup in conditionList:
                antStr = conditionTup[0]
                trimStr = conditionTup[1]
                                
                Print = libPrint.timer()
                Print.logFilenameStr = sqlLogStr.format(ant=antStr,trim=trimStr)
                Print.folderStr = sqlFolderStr.format(branch=branchStr,method=methodStr)
                Print.testingBool = self.testingBool
                Print.startLog()

                for sampleStr in sampleList:
                    Print.phraseStr = "-- Data format conversion for Gene Expression in {} --".format(sampleStr)
                    Print.printTimeStamp()
                    geneSamplePath = geneExpPathStr.format(
                            folder=geneFolderStr,
                            branch=branchStr,
                            ant=antStr,
                            trim=trimStr,
                            sample=sampleStr
                        )
                    sampleDF = pd.read_csv(geneSamplePath,delimiter="\t",header=0)
                    Print.printing("[Pandas:Read]"+geneSamplePath)
                    
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
                        Print.printing("    "+sampleStr+": Empty")
                        compareSet = set(compareList)
                    elif compareSet != set(compareList):
                        Print.printing("    "+sampleStr+": Same")
                    elif compareSet == set(compareList):
                        Print.printing("    "+sampleStr+": Different")

                    sqlPath = sqlPathStr.format(branch=branchStr,method=methodStr,ant=antStr,trim=trimStr)
                    createCommandStr = """CREATE TABLE GeneExpression_{}
                        ('UUID'  TEXT    PRIMARY KEY NOT NULL, 
                        'GeneID'   TEXT    NOT NULL,
                        'GeneName' TEXT    NOT NULL, 
                        'Reference' TEXT    NOT NULL, 
                        'Strand'    TEXT    NOT NULL, 
                        'Start' INTEGER NOT NULL, 
                        'End'   INTEGER NOT NULL, 
                        'Coverage'  REAL    NOT NULL, 
                        'FPKM'  REAL    NOT NULL, 
                        'TPM'   REAL    NOT NULL);""".format(sampleStr)
                    insertCommandStr = "INSERT INTO GeneExpression_{} ('UUID','GeneID','GeneName','Reference','Strand','Start','End','Coverage','FPKM','TPM')\
                        VALUES (?,?,?,?,?,?,?,?,?,?)".format(sampleStr)
                    self.expressionInputDict = {
                        "sqlPath" : sqlPath,
                        "count" : countInt,
                        "rowList" : rowList,
                        "createCommand" : createCommandStr,
                        "insertCommand" : insertCommandStr,
                    }
                    self.exportingExpression(Print)
                    # Transcript
                    Print.phraseStr = "-- Data format conversion for Transcript Expression in {} --".format(sampleStr)
                    Print.printTimeStamp()

                    transcriptSamplePath = transcriptExpPathStr.format(
                            folder=transcriptFolderStr,
                            branch=branchStr,
                            ant=antStr,
                            trim=trimStr,
                            sample=sampleStr
                        )
                    sampleDF = pd.read_csv(transcriptSamplePath,delimiter="\t",header=0)
                    Print.printing("[Pandas:Read] "+transcriptSamplePath)
                    
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
                        Print.printing("    "+sampleStr+": Empty")
                        compareSet = set(compareList)
                    elif compareSet != set(compareList):
                        Print.printing("    "+sampleStr+": Same")
                    elif compareSet == set(compareList):
                        Print.printing("    "+sampleStr+": Different")

                    sqlPath = sqlPathStr.format(branch=branchStr,method=methodStr,ant=antStr,trim=trimStr)
                    createCommandStr = """CREATE TABLE TranscriptExpression_{}
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
                        'FPKM'  REAL    NOT NULL);""".format(sampleStr)
                    insertCommandStr = "INSERT INTO TranscriptExpression_{} ('UUID','TranscriptID','Chromosome','Strand','Start','End','TranscriptName','ExonCount','Length','GeneID','GeneName','Coverage','FPKM')\
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)".format(sampleStr)
                    self.expressionInputDict = {
                        "sqlPath" : sqlPath,
                        "count" : countInt,
                        "rowList" : rowList,
                        "createCommand" : createCommandStr,
                        "insertCommand" : insertCommandStr,
                    }
                    self.exportingExpression(Print)

                Print.phraseStr = "-- Summarising for Gene Expression --"
                Print.printTimeStamp()

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
                Print.printing("[SQLite3:CreateTable] "+sqlPath)

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
                for uuid in resultDict.keys():
                    valueList = list()
                    for posInt in range(len(insertColumnList)):
                        valueList.append(resultDict[uuid][insertColumnList[posInt]])

                    insertCommand = insertComStr.format(column=",".join(insertColumnList),value=(("?,"*(len(valueList)-1)))+"?")
                    ReturnMsg = Cursor.execute(insertCommand,valueList)

                Connect.commit()
                Print.printing("[SQLite3:Insert] "+sqlPath)
                Connect.close()
                Print.printing("[SQLite3:Close]\n")

                # Transcript
                Print.phraseStr = "-- Summarising for Gene Expression --"
                Print.printTimeStamp()

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
                Print.printing("[SQLite3:CreateTable] "+sqlPath)

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
                for uuid in resultDict.keys():
                    valueList = list()
                    for posInt in range(len(insertColumnList)):
                        valueList.append(resultDict[uuid][insertColumnList[posInt]])

                    insertCommand = insertComStr.format(column=",".join(insertColumnList),value=(("?,"*(len(valueList)-1)))+"?")
                    ReturnMsg = Cursor.execute(insertCommand,valueList)

                Connect.commit()
                Print.printing("[SQLite3:Insert] "+sqlPath)
                Connect.close()
                Print.printing("[SQLite3:Close]\n")

                Print.stopLog()