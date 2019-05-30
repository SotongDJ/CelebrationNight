#!/usr/bin/env python3
import pandas as pd
import sqlite3
annotationStr = "speciesTestingA"
conversionBoo = True

gffPath = "data/dbga-GenomeAnnotation/{ant}/{ant}.gff3".format(ant=annotationStr)
gffWHPath = "data/dbga-GenomeAnnotation/{ant}/{ant}-withoutHashtag.gff3".format(ant=annotationStr)
sqlPath = "data/dbga-GenomeAnnotation/{ant}/{ant}-attributes.db".format(ant=annotationStr)

if conversionBoo:
    infoList = open(gffPath).read().splitlines()
    with open(gffWHPath,'w') as targetFile:
        for n in infoList:
            if n[0] != "#":
                targetFile.write(n+"\n")

print("[Load] load DataFrame of gff3")
gffDF = pd.read_csv(gffWHPath,header=None,names=("seqid","source","type","start","end","score","strand","phase","attributes"),low_memory=False,delimiter="\t")
columnSet = set(gffDF.columns)
print("[Finish] load DataFrame of gff3")

print("[Start] Collect data types")
# for rowInt in range(10):
for rowInt in range(len(gffDF)):
    print("[{}/{}]".format(str(rowInt),str(len(gffDF))),end="\r")
    beforeStr = gffDF.xs(rowInt)['attributes']
    columnSet.update(set([ x.split("=")[0] for x in beforeStr.split(";")]))

print("[Finish] Collect data types")

columnList = ['UUID']
columnList.extend(sorted(list(columnSet)))
# attDF = pd.DataFrame(index=range(10), columns=columnList)
attDF = pd.DataFrame(index=range(len(gffDF)), columns=columnList)
print("[Start] Conversion of Attributes")
# for rowInt in range(10):
for rowInt in range(len(gffDF)):
    print("[{}/{}]".format(str(rowInt),str(len(gffDF))),end="\r")
    sourceStr = gffDF.xs(rowInt)['attributes']
    attDF.at[rowInt, 'UUID'] = rowInt
    for titleStr in list(gffDF.columns):
        attDF.at[rowInt, titleStr]= str(gffDF.xs(rowInt)[titleStr])

    for x in sourceStr.split(";"):
        attDF.at[rowInt, x.split("=")[0]] = str(x.split("=")[-1])
    
print("[Finish] Conversion of Attributes")

print("[Write] Generate SQL database for Attributes")
attDF.head()
Connect = sqlite3.connect(sqlPath)
attDF.to_sql(name='Attributes', con=Connect)
Connect.commit()
Connect.close()
print("[Finish] Generate SQL database for Attributes")
