import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pathlib

compareSet = set()
antStr = "speciesTestingA"
trimStr = "trimQ20" # ["trimQ20","trimQ30"]:
sampleList = ["Controlr1","T1r1","T2r1","T3r1","T4r1","T5r1"]

for sampleStr in sampleList:
    pathStr = "data/05-stringtie2/testing/{ant}-{trim}/{sample}-expression.tsv"
    samplePath = pathStr.format(ant=antStr,trim=trimStr,sample=sampleStr)
    sampleDF = pd.read_csv(samplePath,delimiter="\t",header=0)
    
    rowList = sampleDF.values.tolist()
    countInt = len(rowList)

    """
    compareList = list()
    for rowInt in range(countInt):
        compareStr = "\t".join([str(x) for x in rowList[rowInt][0:7]])
        compareList.append(compareStr)
    
    if compareSet == set():
        print(sampleStr+": Empty")
        compareSet = set(compareList)
    elif compareSet != set(compareList):
        print(sampleStr+": same")
    elif compareSet == set(compareList):
        print(sampleStr+": different")
    """

    pathlib.Path("data/07-expressionTable-SQLite3/testing/").mkdir(parents=True,exist_ok=True)
    conn = sqlite3.connect('Expression-{ant}-{trim}.db'.format(ant=antStr,trim=trimStr))
    c = conn.cursor()
    a = c.execute("""CREATE TABLE {exp}_Expression
                ('UUID'  TEXT    PRIMARY KEY NOT NULL, 
                'Gene ID'   TEXT    NOT NULL,
                'Gene Name' TEXT    NOT NULL, 
                'Reference' TEXT    NOT NULL, 
                'Strand'    TEXT    NOT NULL, 
                'Start' INTEGER NOT NULL, 
                'End'   INTEGER NOT NULL, 
                'Coverage'  REAL    NOT NULL, 
                'FPKM'  REAL    NOT NULL, 
                'TPM'   REAL    NOT NULL);""".format(exp=sampleStr))
    conn.commit()

    insertComStr = "INSERT INTO {exp}_Expression('UUID','Gene ID','Gene Name','Reference','Strand','Start','End','Coverage','FPKM','TPM')\
                    VALUES (?,?,?,?,?,?,?,?,?,?)".format(exp=sampleStr)
    for rowInt in range(countInt):
        insertList = []
        sourceList = rowList[rowInt]
        if 'MSTRG' in sourceList[0]:
            insertList.append(sourceList[0])
        else:
            insertList.append("UUID."+str(rowInt))
        
        insertList.extend(sourceList)
        a = c.execute(insertComStr,insertList)

    conn.commit()
    conn.close()
