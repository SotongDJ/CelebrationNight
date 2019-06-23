#!/usr/bin/env python3
import sqlite3, json
settingList = [
    {
        "reference" : 'data/dbga-GenomeAnnotation/speciesEnsembl/speciesEnsembl-attributes.db',
        "dictionary" : 'data/dbga-GenomeAnnotation/speciesEnsembl/speciesEnsembl-attributes.json',
        "select" : "SELECT ID , description FROM Attributes;",
        "idInt" : 0,
        "descriInt" : 1,
    },
    {
        "reference" : 'data/dbga-GenomeAnnotation/speciesTAIR/gene_descriptions.db',
        "dictionary" : 'data/dbga-GenomeAnnotation/speciesTAIR/speciesTAIR-attributes.json',
        "select" : "SELECT * FROM Attributes;",
        "idInt" : 1,
        "descriInt" : 3,
    }
]
for settingDict in settingList:
    print("[SQL-load] open attribute database")
    Connect = sqlite3.connect(settingDict["reference"])
    Cursor = Connect.cursor()
    # Need change
    descriExc = Cursor.execute(settingDict["select"])

    print("[Convert] generating dictionary from attribute database")
    descriDict = dict()
    countInt = 0
    for rowList in descriExc:
        # Need change
        tempList = list(rowList)
        idStr = tempList[settingDict["idInt"]]
        descriStr = tempList[settingDict["descriInt"]]
        
        if idStr != None and descriStr != None:
            if descriDict.get(idStr,"") == "":
                descriDict.update({ idStr : descriStr })
            else:
                descriDict.update({ idStr : "{}; {}".format(descriDict.get(idStr),descriStr) })
        countInt = countInt + 1
        print(countInt,end='\r')
    print("[Finish] scan throught {} lines".format(str(countInt)))
    Connect.close()

    with open(settingDict["dictionary"],"w") as targetHandle:
        json.dump(descriDict,targetHandle,indent=2)