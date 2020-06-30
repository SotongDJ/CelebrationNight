#!/usr/bin/env python3
import pandas as pd
import numpy as np
import sqlite3, json, pathlib, math
import libPrint
# Declaration of sample-dependent variables
configList = [
    {
        "branch"     : ["speciesTreatment"],
        "method"     : "gffRead",
        "control"    : "control",
        "group"      : ["treat1","treat2","treat3","treat4"], # without control
        "compare"    : [ ["treat2","treat1"],["treat4","treat3"],["treat2","treat3"],["treat1","treat4"] ],
        "note"       : "All",
        "annotate"   : "speciesDatabase",
        "trim"       : "trimQ30",
        "omic" : "transcript",
        "attribute"  : {
            'description' : 'userData/08-an-annotateTranscriptome/speciesTreatment-gffRead/speciesDatabase-transcript-attribute-description.json',
            'homolog' : 'userData/08-an-annotateTranscriptome/speciesTreatment-gffRead/speciesDatabase-transcript-attribute-homolog.json',
            "GO" : "userData/08-an-annotateTranscriptome/speciesTreatment-gffRead/speciesDatabase-transcript-GO-gene2term.json",
            "KO" : "userData/08-an-annotateTranscriptome/speciesTreatment-gffRead/speciesDatabase-transcript-KO-gene2term.json",
            "EC" : "userData/08-an-annotateTranscriptome/speciesTreatment-gffRead/speciesDatabase-transcript-EC-gene2term.json",
            "TF" : "userData/08-an-annotateTranscriptome/speciesTreatment-gffRead/speciesDatabase-transcript-TF-gene2term.json",
            "SR" : "userData/08-an-annotateTranscriptome/speciesTreatment-gffRead/speciesDatabase-transcript-SR-gene2term.json",
        }
    },
    {
        "branch"     : ["speciesTreatment2"],
        "method"     : "gffRead",
        "control"    : "Normal",
        "group"      : ["treatI","treatJ"], # without control
        "compare"    : [["treatI","treatJ"]],
        "note"       : "All",
        "annotate"   : "speciesDatabase",
        "trim"       : "trimQ30",
        "omic" : "transcript",
        "attribute"  : {
            'description' : 'userData/08-an-annotateTranscriptome/speciesTreatment2-gffRead/speciesDatabase-transcript-attribute-description.json',
            'homolog' : 'userData/08-an-annotateTranscriptome/speciesTreatment2-gffRead/speciesDatabase-transcript-attribute-homolog.json',
            "GO" : "userData/08-an-annotateTranscriptome/speciesTreatment2-gffRead/speciesDatabase-transcript-GO-gene2term.json",
            "KO" : "userData/08-an-annotateTranscriptome/speciesTreatment2-gffRead/speciesDatabase-transcript-KO-gene2term.json",
            "EC" : "userData/08-an-annotateTranscriptome/speciesTreatment2-gffRead/speciesDatabase-transcript-EC-gene2term.json",
            "TF" : "userData/08-an-annotateTranscriptome/speciesTreatment2-gffRead/speciesDatabase-transcript-TF-gene2term.json",
            "SR" : "userData/08-an-annotateTranscriptome/speciesTreatment2-gffRead/speciesDatabase-transcript-SR-gene2term.json",
        }
    },
]
# Don't touch the code below if you don't know how it works
sourceFilePathStr = 'userData/09-cd-transcriptomeSummary/{branch}-{method}/{annotate}-{trim}-{omic}Expression.db'
resultFilePathStr = 'userData/09-cd-transcriptomeSummary/{branch}-{method}-{annotate}-{trim}/ExpressionSummary-{note}-{omic}'
namePairFilePathStr = 'userData/09-cd-transcriptomeSummary/{branch}-{method}-{annotate}-{trim}/NamePair-{note}-{omic}.json'
logFolderPathStr = 'userData/09-cd-transcriptomeSummary/{branch}-{method}-{annotate}-{trim}/'
logFilePathStr = 'ExpressionSummary-{note}-{omic}'

for configDict in configList:    
    branchList  = configDict.get("branch",[])
    methodStr   = configDict.get("method","")
    annotateStr = configDict.get("annotate","")
    trimStr     = configDict.get("trim","")
    omicStr     = configDict.get("omic","")
    noteStr     = configDict.get("note","")
    controlStr  = configDict.get("control","")
    groupList   = configDict.get("group",[])
    compareList = configDict.get("compare",[])
    compareCStr = "; ".join([ "\t".join(sorted(x)) for x in compareList ])
    attriDict   = configDict.get("attribute",dict())
    
    descriDict = dict()
    descriList = list(attriDict.keys())
    for labelStr in descriList:
        labelDict = json.load(open(attriDict[labelStr]))
        descriDict.update({ labelStr : labelDict })
    
    for branchStr in branchList:
        infoDict = {
            "branch"   : branchStr,
            "method"   : methodStr,
            "annotate" : annotateStr,
            "trim"     : trimStr,
            "omic"     : omicStr,
            "note"     : noteStr
        }
        sourcePathStr = sourceFilePathStr.format(**infoDict)
        resultPathStr = resultFilePathStr.format(**infoDict)
        logFolderPath = logFolderPathStr.format(**infoDict)
        logPathStr = logFilePathStr.format(**infoDict)

        pathlib.Path( logFolderPath ).mkdir(parents=True,exist_ok=True)
        Print = libPrint.timer()
        Print.logFilenameStr = logPathStr
        Print.folderStr = logFolderPath
        Print.testingBool = False
        Print.startLog()

        Print.printing("branch = {branch}\nmethod = {method}\nannotate = {annotate}\ntrim = {trim}\ntype = {omic}".format(**infoDict))
        Print.printing("[SQL-load] open expression database")
        Connect = sqlite3.connect(sourcePathStr)
        Cursor = Connect.cursor()
        selectStr = "SELECT * FROM Expression"
        expExc = Cursor.execute(selectStr)

        Print.printing("[Compare] adjust combination")
        columnSet = {'[Object ID]'}
        resultDict = dict()
        countInt = 0
        for expList in expExc:
            tempList = list(expList)
            testIDStr = tempList[1]
            geneidStr = tempList[2]
            sampleAStr = tempList[5]
            sampleBStr = tempList[6]
            sampleStr = "\t".join(sorted([sampleAStr, sampleBStr]))
            testStr = tempList[7]
            fpkmAFlt = tempList[8]
            fpkmBFlt = tempList[9]
            foldFlt = tempList[10]
            pvFlt = tempList[12]
            qvFlt = tempList[13]
            sigStr = tempList[14]
            
            errorInt = 0
            subDict = resultDict.get(testIDStr,dict())
            # haveSignalBool = (fpkmAFlt > 0) or (fpkmBFlt > 0)
            # if controlStr in sampleStr and haveSignalBool:
            if controlStr in sampleStr:
                if sampleAStr == controlStr:
                    aStr = sampleAStr
                    bStr = sampleBStr
                    faFlt = fpkmAFlt
                    fbFlt = fpkmBFlt
                    fcFlt = foldFlt
                    diFlt = fbFlt - faFlt
                elif sampleBStr == controlStr:
                    aStr = sampleBStr
                    bStr = sampleAStr
                    faFlt = fpkmBFlt
                    fbFlt = fpkmAFlt
                    fcFlt = foldFlt * -1
                    diFlt = fbFlt - faFlt
                else:
                    errorInt = errorInt + 1
                    print("[ERROR{}:A!=Control,B!=Control]".format(str(errorInt)))
                
                if faFlt == 0.0:
                    logaEle = "noSignal"
                else:
                    logaEle = math.log10(faFlt)

                if fbFlt == 0.0:
                    logbEle = "noSignal"
                else:
                    logbEle = math.log10(fbFlt)

                inputDict = {
                    '[Gene ID]' : geneidStr,
                    "[FPKM:{}]".format(aStr) : faFlt,
                    "[FPKM:{}]".format(bStr) : fbFlt,
                    "[log10(FPKM:{})]".format(aStr) : logaEle,
                    "[log10(FPKM:{})]".format(bStr) : logbEle,
                    "[diff:{}-{}]".format(bStr,aStr) : diFlt,
                    "[ratio:{}/{}]".format(bStr,aStr) : fcFlt,
                    "[pass:{}/{}]".format(bStr,aStr) : testStr,
                    "[pVal:{}/{}]".format(bStr,aStr) : pvFlt,
                    "[qVal:{}/{}]".format(bStr,aStr) : qvFlt,
                    "[signi:{}/{}]".format(bStr,aStr) : sigStr,
                }
                subDict.update(inputDict)
                columnSet.update(set(inputDict.keys()))
                resultDict.update({ testIDStr : subDict })

            # elif sampleStr in compareCStr and haveSignalBool:
            elif sampleStr in compareCStr:
                for compareSubList in compareList:
                    baseStr = compareSubList[0]
                    elemStr = compareSubList[1]
                    if (baseStr in sampleStr) and (elemStr in sampleStr):
                        if sampleAStr == baseStr:
                            aStr = sampleAStr
                            bStr = sampleBStr
                            faFlt = fpkmAFlt
                            fbFlt = fpkmBFlt
                            fcFlt = foldFlt
                            diFlt = fbFlt - faFlt
                        elif sampleBStr == baseStr:
                            aStr = sampleBStr
                            bStr = sampleAStr
                            faFlt = fpkmBFlt
                            fbFlt = fpkmAFlt
                            fcFlt = foldFlt * -1
                            diFlt = fbFlt - faFlt
                        else:
                            errorInt = errorInt + 1
                            print("[ERROR{}:A!=Control,B!=Control]".format(str(errorInt)))
                        
                        inputDict = {
                            "[compare:{}/{}]".format(bStr,aStr) : fcFlt,
                            "[diff:{}-{}]".format(bStr,aStr) : diFlt,
                            "[pass:{}/{}]".format(bStr,aStr) : testStr,
                            "[pVal:{}/{}]".format(bStr,aStr) : pvFlt,
                            "[qVal:{}/{}]".format(bStr,aStr) : qvFlt,
                            "[signi:{}/{}]".format(bStr,aStr) : sigStr,
                        }
                        subDict.update(inputDict)
                        columnSet.update(set(inputDict.keys()))
                        resultDict.update({ testIDStr : subDict })

            countInt = countInt + 1
            print("[{}]".format(countInt),end='\r')
        
        print("")
        Print.printing("[Finish] scan throught {} lines (with \"OK\")".format(str(countInt)))
        Connect.close()

        Print.printing("[Organise] create list of column names")
        columnList = ['[Object ID]','[Gene ID]']
        columnList.extend(descriList)
        columnList.append("[FPKM:{}]".format(controlStr))
        columnList.extend(["[FPKM:{}]".format(x) for x in groupList])
        columnList.append("[log10(FPKM:Total)]")
        columnList.append("[log10(FPKM:{})]".format(controlStr))
        sampleSectionList = [
            "[diff:{}-{}]",
            "[ratio:{}/{}]",
            "[pass:{}/{}]",
            "[pVal:{}/{}]",
            "[qVal:{}/{}]",
            "[signi:{}/{}]",
        ]
        for groupStr in groupList:
            columnList.append("[log10(FPKM:{})]".format(groupStr))
            for sampleSectionStr in sampleSectionList:
                columnList.append(sampleSectionStr.format(groupStr,controlStr))
        
        compareSectionList = [
            "[diff:{}-{}]",
            "[compare:{}/{}]",
            "[pass:{}/{}]",
            "[pVal:{}/{}]",
            "[qVal:{}/{}]",
            "[signi:{}/{}]",
        ]
        for compareSubList in compareList:
            for compareSectionStr in compareSectionList:
                baseStr = compareSubList[0]
                elemStr = compareSubList[1]
                columnList.append(compareSectionStr.format(elemStr,baseStr))

        Print.printing("[Arrange] fill the values into DataFrame")
        testList = list(resultDict.keys())
        nameListDict = dict()
        resultDF = pd.DataFrame(index=range(len(testList)), columns=columnList)
        for rowInt in range(len(testList)):
            print("[{}/{}]".format(str(rowInt),str(len(testList))),end="\r")
            testStr = testList[rowInt]
            resultDF.at[rowInt, '[Object ID]'] = testStr
            valueDict = resultDict[testList[rowInt]]

            geneIDStr = valueDict.get(columnList[1],np.NaN)
            if testStr != geneIDStr:
                nameListDict.update({ testStr : geneIDStr })

            for titleStr in [ x for x in columnList if x != '[Object ID]' ]:
                resultDF.at[rowInt, titleStr] = valueDict.get(titleStr,np.NaN)

            sumFlt = 0.0
            fpkmList = [ x for x in columnList if "[FPKM:" in x ]
            for titleStr in fpkmList:
                sumFlt = sumFlt + valueDict.get(titleStr,np.NaN)
            if sumFlt == 0.0:
                resultDF.at[rowInt, "[log10(FPKM:Total)]"] = "noSignal"
            else:
                resultDF.at[rowInt, "[log10(FPKM:Total)]"] = math.log10(sumFlt)
            
            for labelStr in descriList:
                descriEle = descriDict.get(labelStr,dict()).get(testStr,np.NaN)
                if type(descriEle) == type(list()):
                    descriStr = "; ".join(descriEle)
                elif  type(descriEle) == type(str()):
                    descriStr = descriEle
                else:
                    descriStr = np.NaN
                
                resultDF.at[rowInt, labelStr] = descriStr
        
        print("")
        Print.printing("[Export] export as expressionSummary.db")
        if pathlib.Path(resultPathStr+".db").exists():
            pathlib.Path(resultPathStr+".db").unlink()
        Connect = sqlite3.connect(resultPathStr+".db")
        resultDF.to_sql(name='Summary', con=Connect)
        Connect.commit()
        Connect.close()

        Print.printing("[Export] export as expressionSummary.tsv")
        resultDF.to_csv(resultPathStr+".tsv", index=False, sep='\t', encoding='utf-8')
        
        if nameListDict != dict():
            Print.printing("[Export] export namePair.json")
            with open(namePairFilePathStr.format(**infoDict),"w") as targetHandle:
                json.dump(nameListDict,targetHandle,indent=1)

        Print.stopLog()
        print("\n")
