import pathlib
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

branchStr = "testing"
antStr = "speciesTestingA"
controlStr = "Controlr1"
sampleList = ["Controlr1","T1r1","T2r1","T3r1","T4r1","T5r1"]

fileStr = 'data/07-sl-expressionTable-SQLite3/{branch}/Expression-{ant}-trimQ20.db'
filePath = fileStr.format(branch=branchStr,ant=antStr)
Connect = sqlite3.connect(filePath)
print("[SQLite3]\n    "+filePath)
Cursor = Connect.cursor()

q20Dict = dict()
for sampleStr in sampleList:
    sampleExc = Cursor.execute("SELECT UUID, TPM  from {}_Expression".format(sampleStr))
    for rowList in sampleExc:
        uuid, tpm = rowList
        subDict = q20Dict.get(uuid,dict())
        subDict.update({ sampleStr : tpm })
        q20Dict.update({ uuid : subDict })

Connect.close()

fileStr = 'data/07-sl-expressionTable-SQLite3/{branch}/Expression-{ant}-trimQ30.db'
filePath = fileStr.format(branch=branchStr,ant=antStr)
Connect = sqlite3.connect(filePath)
print("[SQLite3]\n    "+filePath)
Cursor = Connect.cursor()

q30Dict = dict()
for sampleStr in sampleList:
    sampleExc = Cursor.execute("SELECT UUID, TPM  from {}_Expression".format(sampleStr))
    for rowList in sampleExc:
        uuid, tpm = rowList
        subDict = q30Dict.get(uuid,dict())
        subDict.update({ sampleStr : tpm })
        q30Dict.update({ uuid : subDict })

Connect.close()

diffrDict = dict()
for uuid in q20Dict.keys():
    for sampleStr in sampleList:
        q20Flt = q20Dict[uuid][sampleStr]
        q30Flt = q30Dict[uuid][sampleStr]
        difFlt = abs(q30Flt-q20Flt)
        if (q30Flt-q20Flt) > 0:
            dirStr = "increase"
        elif (q30Flt-q20Flt) < 0:
            dirStr = "decrease"
        else:
            dirStr = "remain"
        
        subDict = diffrDict.get(uuid,dict())
        subDict.update({ "Difference_"+sampleStr : difFlt })
        subDict.update({ "Direction_"+sampleStr : dirStr })
        diffrDict.update({ uuid : subDict })

createComStr = "CREATE TABLE ExpressionSummary ({})"
createColumnList = [
    "'UUID'  TEXT PRIMARY KEY NOT NULL", 
]
columnList = ["UUID"]
insertColumnList = []
for sampleStr in sampleList:
    columnStr = "Difference_{} REAL".format(sampleStr)
    createColumnList.append(columnStr)
    columnList.append("Difference_{}".format(sampleStr))
    insertColumnList.append("Difference_{}".format(sampleStr))

    columnStr = "Direction_{} REAL".format(sampleStr)
    createColumnList.append(columnStr)
    columnList.append("Direction_{}".format(sampleStr))
    insertColumnList.append("Direction_{}".format(sampleStr))

pathlib.Path("data/07-df-differenceDistribution/{branch}/".format(branch=branchStr)).mkdir(parents=True,exist_ok=True)
fileStr = 'data/07-df-differenceDistribution/{branch}/Difference-{ant}.db'
filePath = fileStr.format(branch=branchStr,ant=antStr)
Connect = sqlite3.connect(filePath)
print("[SQLite3]\n    "+filePath)
Cursor = Connect.cursor()
ReturnMsg = Cursor.execute(createComStr.format(",".join(createColumnList)))
Connect.commit()

insertComStr = "INSERT INTO ExpressionSummary ({column}) VALUES ({value})"
a = 0
for uuid in diffrDict.keys():
    valueList = list()
    valueList.append(uuid)
    for posInt in range(len(insertColumnList)):
        valueList.append(diffrDict[uuid][insertColumnList[posInt]])

    insertCommand = insertComStr.format(column=",".join(columnList),value=(("?,"*(len(valueList)-1)))+"?")
    ReturnMsg = Cursor.execute(insertCommand,valueList)

Connect.commit()

Connect.close()