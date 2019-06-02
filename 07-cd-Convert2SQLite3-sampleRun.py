import pandas as pd
import sqlite3
pathStr = "data/06-cd-CuffDiff/testing-dsStringtie/arathTAIR-trimQ30/gene_exp.diff"
diffDF = pd.read_csv(pathStr,delimiter="\t",header=0)
rowList = diffDF.values.tolist()
pathStr
sqlPathStr = 'data/06-cd-CuffDiff/testing-dsStringtie/arathTAIR-trimQ30/gene.db'

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
'value_1'  REAL,  
'value_2'  REAL,  
'log2(fold_change)'  REAL,  
'test_stat'  REAL,  
'p_value'  REAL,  
'q_value'   REAL,  
'significant'   TEXT);"""
msg = Cursor.execute(createStr)
Connect.commit()

countInt = len(rowList)
insertStr = """INSERT INTO Expression ('UUID','test_id' ,'gene_id' ,'gene' ,'locus' ,'sample_1' ,'sample_2' ,'status' ,'value_1' ,'value_2' ,'log2(fold_change)' ,'test_stat' ,'p_value' ,'q_value' ,'significant') VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
for rowInt in range(countInt):
    tempList = list()
    tempList.append(rowInt)
    tempList.extend(rowList[rowInt])
    msg = Cursor.execute(insertStr,tempList) 

Connect.commit()