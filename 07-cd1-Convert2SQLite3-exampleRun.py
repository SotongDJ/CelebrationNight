#!/usr/bin/env python3
import pandas as pd
import sqlite3, pathlib

configList = [
    {
        "branch"   : ["testing1","testing2"],
        "method"   : ["dsStringtie"],
        "annotate" : ["speciesAAnotationA"],
        "trim"     : ["trimQ30"]
    },
    {
        "branch"   : ["testing3","testing4"],
        "method"   : ["dsStringtie","waStringtie"],
        "annotate" : ["speciesBAnotationA","speciesBAnotationB","speciesBAnotationC"],
        "trim"     : ["trimQ30"]
    }
]

# Don't touch the code below if you don't how it works
typeList = [
    ["gene_exp", "geneExpression"],
    ["isoform_exp", "transcriptExpression"]
]
diffFilePathStr = "data/06-cd-CuffDiff/{branch}-{method}/{annotate}-{trim}/{source}.diff"
sqlFilePathStr = 'data/07-cd-CuffDiff/{branch}-{method}/{annotate}-{trim}-{target}.db'
sqlFolderPathStr = 'data/07-cd-CuffDiff/{branch}-{method}/'

for combinationList in typeList:
    sourceStr = combinationList[0]
    targetStr = combinationList[1]
    for configDict in configList:
        branchList = configDict.get("branch",[])
        methodList = configDict.get("method",[])
        annotateList = configDict.get("annotate",[])
        trimList = configDict.get("trim",[])
        for branchStr in branchList:
            for methodStr in methodList:
                for annotateStr in annotateList:
                    for trimStr in trimList:
                        parameterDict = {
                            "branch"   : branchStr,
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

                        countInt = len(rowList)
                        insertStr = """INSERT INTO Expression 
                            ('UUID','test_id' ,'gene_id' ,'gene' ,
                            'locus' ,'sample_1' ,'sample_2' ,'status' ,
                            'FPKM_1' ,'FPKM_2' ,'log2(fold_change)' ,'test_stat' ,
                            'p_value' ,'q_value' ,'significant') 
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
                        for rowInt in range(countInt):
                            tempList = list()
                            tempList.append(rowInt)
                            tempList.extend(rowList[rowInt])
                            msg = Cursor.execute(insertStr,tempList) 

                        Connect.commit()
