import pathlib
import sqlite3
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

branchStr = "testing"
antStr = "speciesTestingA"
controlStr = "Controlr1"
sampleList = ["Controlr1","T1r1","T2r1","T3r1","T4r1","T5r1"]
trim20PathStr = 'data/07-sl-expressionTable-SQLite3/{branch}/Expression-{ant}-trimQ20.db'
trim30PathStr = 'data/07-sl-expressionTable-SQLite3/{branch}/Expression-{ant}-trimQ30.db'
sqlFolderStr = "data/07-df-differenceDistribution/{branch}/"
sqlPathStr = 'data/07-df-differenceDistribution/{branch}/Difference-{ant}.db'

trim20Path = trim20PathStr.format(branch=branchStr,ant=antStr)
Connect = sqlite3.connect(trim20Path)
print("[SQLite3]\n    "+trim20Path)
Cursor = Connect.cursor()

geneidDict = dict()
q20Dict = dict()
for sampleStr in sampleList:
    sampleExc = Cursor.execute("SELECT UUID, GeneID, TPM  from {}_Expression".format(sampleStr))
    for rowList in sampleExc:
        uuid, geneid, tpm = rowList
        subDict = q20Dict.get(uuid,dict())
        subDict.update({ sampleStr : tpm })
        q20Dict.update({ uuid : subDict })

        geneidDict.update({ uuid : geneid })

Connect.close()

trim30Path = trim30PathStr.format(branch=branchStr,ant=antStr)
Connect = sqlite3.connect(trim30Path)
print("[SQLite3]\n    "+trim30Path)
Cursor = Connect.cursor()

q30Dict = dict()
for sampleStr in sampleList:
    sampleExc = Cursor.execute("SELECT UUID, GeneID, TPM  from {}_Expression".format(sampleStr))
    for rowList in sampleExc:
        uuid, geneid, tpm = rowList
        subDict = q30Dict.get(uuid,dict())
        subDict.update({ sampleStr : tpm })
        q30Dict.update({ uuid : subDict })

        geneidDict.update({ uuid : geneid })

Connect.close()

diffrDict = dict()
for uuid in q20Dict.keys():
    geneidStr = geneidDict[uuid]
    for sampleStr in sampleList:
        q20Flt = q20Dict[uuid][sampleStr]
        q30Flt = q30Dict[uuid][sampleStr]
        diffFlt = abs(q30Flt-q20Flt)

        minFlt = sorted([q20Flt,q30Flt])[0]
        if minFlt != 0.0:
            ratioFlt = diffFlt/minFlt
        else:
            ratioFlt = 0.0
        
        if (q30Flt-q20Flt) > 0:
            dirStr = "increase"
        elif (q30Flt-q20Flt) < 0:
            dirStr = "decrease"
        else:
            dirStr = "remain"
        
        if diffFlt != 0:
            groupIntStr = str(int(math.ceil(math.log10(diffFlt))))
        else:
            groupIntStr = 'none'
        
        subDict = diffrDict.get(uuid,dict())
        subDict.update({ "Difference_"+sampleStr : diffFlt })
        subDict.update({ "Direction_"+sampleStr : dirStr })
        subDict.update({ "Ratio_"+sampleStr : ratioFlt })
        subDict.update({ "Group_"+sampleStr : groupIntStr })
        subDict.update({ "GeneID" : geneidStr})
        diffrDict.update({ uuid : subDict })

createComStr = "CREATE TABLE Differences_Summary ({})"
createColumnList = [
    "'UUID'  TEXT PRIMARY KEY NOT NULL", 
    "'GeneID'  TEXT", 
]
columnList = ["UUID","GeneID"]
insertColumnList = ["GeneID"]
for sampleStr in sampleList:
    columnStr = "Difference_{} REAL".format(sampleStr)
    createColumnList.append(columnStr)
    columnList.append("Difference_{}".format(sampleStr))
    insertColumnList.append("Difference_{}".format(sampleStr))

    columnStr = "Direction_{} TEXT".format(sampleStr)
    createColumnList.append(columnStr)
    columnList.append("Direction_{}".format(sampleStr))
    insertColumnList.append("Direction_{}".format(sampleStr))

    columnStr = "Ratio_{} REAL".format(sampleStr)
    createColumnList.append(columnStr)
    columnList.append("Ratio_{}".format(sampleStr))
    insertColumnList.append("Ratio_{}".format(sampleStr))

    columnStr = "Group_{} TEXT".format(sampleStr)
    createColumnList.append(columnStr)
    columnList.append("Group_{}".format(sampleStr))
    insertColumnList.append("Group_{}".format(sampleStr))

pathlib.Path(sqlFolderStr.format(branch=branchStr)).mkdir(parents=True,exist_ok=True)
sqlPath = sqlPathStr.format(branch=branchStr,ant=antStr)
Connect = sqlite3.connect(sqlPath)
print("[SQLite3]\n    "+sqlPath)
Cursor = Connect.cursor()
ReturnMsg = Cursor.execute(createComStr.format(",".join(createColumnList)))
Connect.commit()

insertComStr = "INSERT INTO Differences_Summary ({column}) VALUES ({value})"
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

for sampleStr in sampleList:
    sampleCreateComStr = "CREATE TABLE Differences_{} ({})"
    sampleCreateColumnList = [
        "'UUID'  TEXT PRIMARY KEY NOT NULL", 
        "'GeneID'  TEXT", 
    ]
    sampleInsertList = ["UUID","GeneID"]

    columnStr = "TPM_{}_Q20 REAL".format(sampleStr)
    sampleCreateColumnList.append(columnStr)
    sampleInsertList.append("TPM_{}_Q20".format(sampleStr))

    columnStr = "TPM_{}_Q30 REAL".format(sampleStr)
    sampleCreateColumnList.append(columnStr)
    sampleInsertList.append("TPM_{}_Q30".format(sampleStr))

    columnStr = "Difference_{} REAL".format(sampleStr)
    sampleCreateColumnList.append(columnStr)
    sampleInsertList.append("Difference_{}".format(sampleStr))

    columnStr = "Direction_{} TEXT".format(sampleStr)
    sampleCreateColumnList.append(columnStr)
    sampleInsertList.append("Direction_{}".format(sampleStr))

    columnStr = "Ratio_{} REAL".format(sampleStr)
    sampleCreateColumnList.append(columnStr)
    sampleInsertList.append("Ratio_{}".format(sampleStr))

    columnStr = "Group_{} TEXT".format(sampleStr)
    sampleCreateColumnList.append(columnStr)
    sampleInsertList.append("Group_{}".format(sampleStr))

    sampleDict = dict()
    for uuid in diffrDict.keys():
        subDict = dict()
        subDict.update({ 'UUID' : uuid })
        subDict.update({ 'GeneID' : geneidDict[uuid] })
        subDict.update({ 'TPM_{}_Q20'.format(sampleStr) : q20Dict[uuid][sampleStr] })
        subDict.update({ 'TPM_{}_Q30'.format(sampleStr) : q30Dict[uuid][sampleStr] })
        subDict.update({ 'Difference_{}'.format(sampleStr) : diffrDict[uuid]["Difference_{}".format(sampleStr)] })
        subDict.update({ 'Direction_{}'.format(sampleStr) : diffrDict[uuid]["Direction_{}".format(sampleStr)] })
        subDict.update({ 'Ratio_{}'.format(sampleStr) : diffrDict[uuid]["Ratio_{}".format(sampleStr)] })
        subDict.update({ 'Group_{}'.format(sampleStr) : diffrDict[uuid]["Group_{}".format(sampleStr)] })
        sampleDict.update({ uuid : subDict })

    sqlPath = sqlPathStr.format(branch=branchStr,ant=antStr)
    Connect = sqlite3.connect(sqlPath)
    print("[SQLite3]\n    "+sqlPath)
    Cursor = Connect.cursor()
    ReturnMsg = Cursor.execute(sampleCreateComStr.format(sampleStr,",".join(sampleCreateColumnList)))
    Connect.commit()

    for uuid in diffrDict.keys():
        valueList = list()
        for posInt in range(len(sampleInsertList)):
            valueList.append(sampleDict[uuid][sampleInsertList[posInt]])

        sampleInsertComStr = "INSERT INTO Differences_{sample} ({column}) VALUES ({value})"
        insertCommand = sampleInsertComStr.format(sample=sampleStr, column=",".join(sampleInsertList),value=(("?,"*(len(valueList)-1)))+"?")
        ReturnMsg = Cursor.execute(insertCommand,valueList)

    Connect.commit()
    Connect.close()
        