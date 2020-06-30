#!/usr/bin/env python3
import pandas as pd
import sqlite3, pathlib

configList = [
    {
        "branch"   : {"speciesTreatment" : "Treatment on Species"},
        "method"   : ["gffRead"],
        "annotate" : ["speciesDatabase"],
        "trim"     : ["trimQ30"],
        "sampleRename" : {
            "control" : "ControlTreatment",
            "treat1" : "TreatmentOne",
            "treat2" : "TreatmentTwo",
            "treat3" : "TreatmentThree",
            "treat4" : "TreatmentFour"
        }
    },
    {
        "branch"   : {"speciesTreatment2" : "Second Treatment on Species"},
        "method"   : ["gffRead"],
        "annotate" : ["speciesDatabase"],
        "trim"     : ["trimQ30"],
        "sampleRename" : {
            "Normal" : "NormalTreatment",
            "treatI" : "TreatmentI",
            "treatJ" : "TreatmentJ",
        }
    },
]
# Don't touch the code below if you don't how it works

typeList = [
    ["gene_exp", "gene"],
    ["isoform_exp", "transcript"]
]

diffFilePathStr = "userData/07-cd-estimateExpression/{branch}-{method}/{annotate}-{trim}/{source}.diff"
sqlFilePathStr = 'userData/09-cd-transcriptomeSummary/{renameBranch}-{method}/{annotate}-{trim}-{target}Expression.db'
sqlFolderPathStr = 'userData/09-cd-transcriptomeSummary/{renameBranch}-{method}/'

for combinationList in typeList:
    """
    sourceStr = "gene_exp"
    targetStr = "geneExpression"
    """
    sourceStr,targetStr = combinationList
    for configDict in configList:
        branchDict = configDict.get("branch",dict())
        methodList = configDict.get("method",list())
        annotateList = configDict.get("annotate",list())
        trimList = configDict.get("trim",list())
        renameDict = configDict.get("sampleRename",dict())
        for branchStr in list(branchDict.keys()):
            renameBranchStr = branchDict[branchStr]
            for methodStr in methodList:
                for annotateStr in annotateList:
                    for trimStr in trimList:
                        parameterDict = {
                            "branch"   : branchStr,
                            "renameBranch" : renameBranchStr,
                            "method"   : methodStr,
                            "annotate" : annotateStr,
                            "trim"     : trimStr,
                            "source"   : sourceStr,
                            "target"   : targetStr
                        }
                        pathStr = diffFilePathStr.format(**parameterDict)
                        sqlPathStr = sqlFilePathStr.format(**parameterDict)
                        sqlFolderStr = sqlFolderPathStr.format(**parameterDict)
                        pathlib.Path( sqlFolderStr ).mkdir(parents=True,exist_ok=True)
                        if pathlib.Path(sqlPathStr).exists():
                            pathlib.Path(sqlPathStr).unlink()

                        diffDF = pd.read_csv(pathStr,delimiter="\t",header=0)
                        rowList = diffDF.values.tolist()
                        Connect = sqlite3.connect(sqlPathStr)
                        Cursor = Connect.cursor()
                        createStr = """CREATE  TABLE  Expression 
                                ('UUID' INTEGER PRIMARY KEY  NOT NULL,
                                'test_id'  TEXT ,  
                                'gene_id'  TEXT,  
                                'gene'  TEXT,  
                                'locus'  TEXT,  
                                'sample_1'  TEXT,  
                                'sample_2'  TEXT,  
                                'status'  TEXT,  
                                'FPKM_1'  REAL,  
                                'FPKM_2'  REAL,  
                                'log2(fold_change)'  REAL,  
                                'test_stat'  REAL,  
                                'p_value'  REAL,  
                                'q_value'   REAL,  
                                'significant'   TEXT);"""
                        msg = Cursor.execute(createStr)
                        Connect.commit()

                        columnTup = tuple(['test_id' ,'gene_id' ,'gene' ,
                            'locus' ,'sample_1' ,'sample_2' ,'status' ,
                            'FPKM_1' ,'FPKM_2' ,'log2(fold_change)' ,'test_stat' ,
                            'p_value' ,'q_value' ,'significant'])
                        insertStr = """INSERT INTO Expression 
                            ('UUID','test_id' ,'gene_id' ,'gene' ,
                            'locus' ,'sample_1' ,'sample_2' ,'status' ,
                            'FPKM_1' ,'FPKM_2' ,'log2(fold_change)' ,'test_stat' ,
                            'p_value' ,'q_value' ,'significant') 
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
                        testList =list()
                        totalCountInt = len(rowList)
                        currentCountInt = 0
                        for rowInt, eachRowList in enumerate(rowList):
                            currentCountInt = currentCountInt + 1
                            print("[{}/{}]".format(currentCountInt,totalCountInt),end="\r")
                            columnDict = dict()
                            for columnInt,columnStr in enumerate(columnTup):
                                contentEle = eachRowList[columnInt]
                                if type(contentEle) == type(str()) and contentEle in renameDict.keys():
                                    contentEle = renameDict[contentEle]
                                columnDict[columnStr] = contentEle
                            contentList = [ rowInt ]
                            contentList.extend([ columnDict[n] for n in columnTup ])
                            msg = Cursor.execute(insertStr,contentList) 
                            
                            testList.append(columnDict['test_id'])
                        
                        print("")
                        print(len(testList),len(set(testList)))
                        Connect.commit()
