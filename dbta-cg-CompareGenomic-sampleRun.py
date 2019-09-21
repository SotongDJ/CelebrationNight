#!/usr/bin/env python3
import pathlib, sqlite3, math, pprint, json
import numpy as np
import pandas as pd
import libPrint

branchList = ["testing"]
methodList = ["dsStringtie","Stringtie","waStringtie"]
conditionList = [("speciesAnnotationA","trimQ30"),("speciesAnnotationB","trimQ30"),("speciesAnnotationC","trimQ30")]
controlStr = "Controlr1"
controlSafeStr = "Controlr1"
sampleList = ["Controlr1","T1r1","T2r1","T3r1","T4r1","T5r1"]

databasePathStr = 'data/07-st-expressionTable-SQLite3/{branch}-{method}/Expression-{ant}-{trim}.db'
resultFolderStr = "data/07-cg-CompareGenomic/{branch}-{method}/"
resultFilenameStr = "geneTranscriptRatio-{ant}-{trim}-{sample}"
jsonFilenameStr = "geneMemberDict-{ant}-{trim}-{sample}.json"

# FPKM
for branchStr in branchList:
    for methodStr in methodList:
        for conditionTup in conditionList:
            antStr = conditionTup[0]
            trimStr = conditionTup[1]
            logFilenameStr = resultFilenameStr.format(ant=antStr,trim=trimStr,sample=controlStr)
            jsonNameStr = jsonFilenameStr.format(ant=antStr,trim=trimStr,sample=controlStr)
            folderStr = resultFolderStr.format(branch=branchStr,method=methodStr)
            
            Print = libPrint.timer()
            Print.logFilenameStr = logFilenameStr
            Print.folderStr = folderStr
            Print.testingBool = False
            Print.startLog()

            Print.printing("# Branch: "+branchStr)
            Print.printing("# -- Calculating FPKM differences --")
            databasePath = databasePathStr.format(branch=branchStr,method=methodStr,ant=antStr,trim=trimStr)
            Connect = sqlite3.connect(databasePath)
            Print.printing("# [SQLite3:Open]"+databasePath)
            Cursor = Connect.cursor()

            infoDict = dict()
            q20Dict = dict()
            geneid2tnameDict = dict()
            g2tQtyDict = dict()
            tname2geneidDict = dict()
            t2gQtyDict = dict()
            annotationDict = dict()

            sampleExc = Cursor.execute("SELECT UUID, TranscriptID, TranscriptName, GeneID, GeneName, FPKM from TranscriptExpression_{}".format(controlSafeStr))
            for rowList in sampleExc:
                uuid, tID, tName, geneID, geneName, fpkm = rowList
                subDict = infoDict.get(uuid,dict())
                subDict.update({ "TranscriptID" : tID })
                subDict.update({ "TranscriptName" : tName })
                subDict.update({ "GeneID" : geneID })
                subDict.update({ "GeneName" : geneName })
                subDict.update({ "FPKM" : fpkm })
                infoDict.update({ uuid : subDict })

            for n in list(infoDict.keys()):
                tnameStr = infoDict[n]['TranscriptName']
                geneidStr = infoDict[n]['GeneID']

                subList = geneid2tnameDict.get(geneidStr,list())
                subList.append(tnameStr)
                geneid2tnameDict.update({ geneidStr : subList })

                subList = tname2geneidDict.get(tnameStr,list())
                subList.append(geneidStr)
                tname2geneidDict.update({ tnameStr : subList })

            for geneidStr in list(geneid2tnameDict.keys()):
                lenInt = len(geneid2tnameDict[geneidStr])

                subList = g2tQtyDict.get(lenInt,list())
                subList.append(geneidStr)
                g2tQtyDict.update({ lenInt : subList })

                geneHeadStr = str()
                if "MSTRG" in geneidStr:
                    geneHeadStr = "UNKNOWN"
                elif ":" in geneidStr:
                    geneHeadStr = "KNOWN"
                elif "rna" in geneidStr:
                    geneHeadStr = "KNOWN"
                elif "gene" in geneidStr:
                    geneHeadStr = "KNOWN"
                elif "BraA" in geneidStr:
                    geneHeadStr = "KNOWN"

                convertList = list()
                for n in geneid2tnameDict[geneidStr]: 
                    if "MST" in n:
                        convertList.append("UNKNOWN")
                    elif "trans" in n:
                        convertList.append("KNOWN")
                    elif "rna" in n:
                        convertList.append("KNOWN")
                    elif "gene" in n:
                        convertList.append("KNOWN")
                    elif "BraA" in n:
                        convertList.append("KNOWN")
                    else:
                        Print.printing("# error: "+n)
                headSet = set(convertList)
                if len(headSet) >= 2:
                    titleStr = "memberHetero-"+geneHeadStr+"".join([ x[0:2] for x in headSet ])
                    subDict = annotationDict.get( titleStr, dict())  
                    subList = subDict.get(lenInt,list())
                    subList.append(geneidStr)
                    subDict.update({ lenInt : subList })
                    annotationDict.update({ titleStr : subDict })
                elif len(headSet) == 1:
                    listHeaderStr = convertList[0]
                    
                    if geneHeadStr == listHeaderStr:
                        subDict = annotationDict.get("memberHomo-"+geneHeadStr,dict())  
                        subList = subDict.get(lenInt,list())
                        subList.append(geneidStr)
                        subDict.update({ lenInt : subList })
                        annotationDict.update({ "memberHomo-"+geneHeadStr : subDict })
                    else:
                        subDict = annotationDict.get("groupMemberHetero-"+geneHeadStr,dict())  
                        subList = subDict.get(lenInt,list())
                        subList.append(geneidStr)
                        subDict.update({ lenInt : subList })
                        annotationDict.update({ "groupMemberHetero-"+geneHeadStr : subDict })
                else:
                    Print.printing("# error: "+pprint.pformat(convertList))
            
            for annotatedTypeStr in annotationDict.keys():
                transCountInt = 0
                geneCountInt = 0
                Print.printing("# Type: "+annotatedTypeStr)
                Print.printing("MemberCount\tGeneCount")
                typeDict = annotationDict[annotatedTypeStr]
                for lenInt in sorted(list(typeDict.keys())):
                    Print.printing("{}\t{}".format(str(lenInt),str(len(typeDict[lenInt]))))
                    geneCountInt = geneCountInt + len(typeDict[lenInt])
                    transCountInt = transCountInt + (len(typeDict[lenInt]) * lenInt)
                
                Print.printing("# Gene Count: "+str(geneCountInt))
                Print.printing("# Transcript Count: "+str(transCountInt))

            for tnameStr in list(tname2geneidDict.keys()):
                lenInt = len(tname2geneidDict[tnameStr])
            
                subList = t2gQtyDict.get(lenInt,list())
                subList.append(tnameStr)
                t2gQtyDict.update({ lenInt : subList })
            
            pathlib.Path( folderStr ).mkdir(parents=True,exist_ok=True)
            with open(folderStr+jsonNameStr,"w") as targetHandle:
                json.dump(annotationDict,targetHandle,indent=2)

            Print.printing("# Finish\n")
