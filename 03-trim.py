#!/usr/bin/env python3
import libConfig, libPrint
import pathlib
"""
   --- README of 03-trim ---
 Title:
    Batch Processing for Trimmomatic

 Original command:
  java -jar <bin>/trimmomatic-0.35.jar PE \\
    -phred33 -threads <threads> \\
    input_forward.fq.gz input_reverse.fq.gz \\
    output_forward_paired.fq.gz output_forward_unpaired.fq.gz \\
    output_reverse_paired.fq.gz output_reverse_unpaired.fq.gz \\
    <ILLUMINACLIP> <LEADING> \\
    <TRAILING> <SLIDINGWINDOW> <MINLEN>

   --- README ---
"""
# ---- Parameter ----
Trim = libConfig.config()
Trim.queryStr = "binTrimmomatic"
Trim.folderStr = "data/config/"
Trim.modeStr = "UPDATE"
Trim.load()

ExpRep = libConfig.config()
ExpRep.queryStr = "testing"
ExpRep.folderStr = "data/config/"
ExpRep.modeStr = "UPDATE"
ExpRep.load()

# ---- Initialization ----
conditionList = ExpRep.storeDict.get("[trim]condition",[])
groupList = ExpRep.storeDict.get("group",[])
directionList = ExpRep.storeDict.get("direction",[])

branchStr = ExpRep.storeDict.get("branch","")
pairStr = ExpRep.storeDict.get("pairPostfix","")
unpairStr = ExpRep.storeDict.get("unpairPostfix","")

inputFileNameStr = ExpRep.storeDict.get("[trim]inputFileName","")
outputFileNameStr = ExpRep.storeDict.get("[trim]outputFileName","")
fileTypeStr = ExpRep.storeDict.get("[trim]fileType","")
checkFolderList = ExpRep.storeDict.get("[trim]checkFolder",[])
# ---- Action ----
for folderStr in checkFolderList:
    pathlib.Path(folderStr).mkdir(parents=True,exist_ok=True)

if type(conditionList) == type(list()) and conditionList != []:
    for conditionStr in conditionList:
        Print = libPrint.timer()
        Print.logFilenameStr = "03-trim-{branch}-{cond}".format(
            branch=branchStr,
            cond=conditionStr
        )
        Print.folderStr = "data/log/"
        Print.startLog()

        TrimPara = libConfig.config()
        TrimPara.queryStr = conditionStr
        TrimPara.folderStr = "data/config/"
        TrimPara.modeStr = "UPDATE"
        TrimPara.load()

        for groupStr in groupList:
            inputFileList = list()
            outputFileList = list()
            for directionStr in directionList:
                inputStr = inputFileNameStr.format(
                    group=groupStr,
                    direction=directionStr,
                    fileType=fileTypeStr
                )
                inputFileList.append(inputStr)
                outputPairStr = outputFileNameStr.format(
                    condition=conditionStr,
                    direction=directionStr,
                    group=groupStr,
                    pairType=pairStr,
                    fileType=fileTypeStr,
                )
                outputFileList.append(outputPairStr)
                outputUnPairStr = outputFileNameStr.format(
                    condition=conditionStr,
                    direction=directionStr,
                    group=groupStr,
                    pairType=unpairStr,
                    fileType=fileTypeStr,
                )
                outputFileList.append(outputUnPairStr)

            fileList = inputFileList + outputFileList
            fileStr = " ".join(fileList)

            commandDict = dict()
            commandDict.update(TrimPara.storeDict)
            commandDict.update({ 'files' : fileStr })
            proCommandStr = Trim.storeDict["command"].format(**commandDict)
            Print.phraseStr = proCommandStr
            Print.runCommand()

    Print.stopLog()

