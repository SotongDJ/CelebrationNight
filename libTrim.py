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
class trimmer:
    def __init__(self):
        # ---- Initialization ----
        self.queryStr = str()

    def trimming(self):
        # ---- Parameter ----
        BinTrim = libConfig.config()
        BinTrim.queryStr = "binTrimmomatic"
        BinTrim.folderStr = "data/config/"
        BinTrim.modeStr = "UPDATE"
        BinTrim.load()

        ExpRep = libConfig.config()
        ExpRep.queryStr = self.queryStr
        ExpRep.folderStr = "data/config/"
        ExpRep.modeStr = "UPDATE"
        ExpRep.load()

        # ---- Initialization ----
        commandStr = BinTrim.storeDict["command"]

        conditionList = ExpRep.storeDict.get("[trim]condition",[])
        groupList = ExpRep.storeDict.get("group",[])
        replicationList = ExpRep.storeDict.get("replication",[])
        directionList = ExpRep.storeDict.get("direction",[])

        branchStr = ExpRep.storeDict.get("branch","")
        pairStr = ExpRep.storeDict.get("pairPostfix","")
        unpairStr = ExpRep.storeDict.get("unpairPostfix","")

        inputFileNameStr = ExpRep.storeDict.get("[trim]inputFileName","")
        outputFileNameStr = ExpRep.storeDict.get("[trim]outputFileName","")
        fileTypeStr = ExpRep.storeDict.get("[trim]fileType","")
        checkFolderList = ExpRep.storeDict.get("[trim]checkFolder",[])

        if not ExpRep.storeDict.get("testing",True):
            testingBool = False
        else:
            testingBool = True

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
                Print.testingBool = testingBool
                Print.startLog()

                TrimPara = libConfig.config()
                TrimPara.queryStr = conditionStr
                TrimPara.folderStr = "data/config/"
                TrimPara.modeStr = "UPDATE"
                TrimPara.load()

                for groupStr in groupList:
                    for replicationStr in replicationList:
                        inputFileList = list()
                        outputFileList = list()
                        for directionStr in directionList:
                            inputStr = inputFileNameStr.format(
                                group=groupStr,
                                replication=replicationStr,
                                direction=directionStr,
                                fileType=fileTypeStr
                            )
                            inputFileList.append(inputStr)
                            outputPairStr = outputFileNameStr.format(
                                condition=conditionStr,
                                direction=directionStr,
                                group=groupStr,
                                replication=replicationStr,
                                pairType=pairStr,
                                fileType=fileTypeStr,
                            )
                            outputFileList.append(outputPairStr)
                            outputUnPairStr = outputFileNameStr.format(
                                condition=conditionStr,
                                direction=directionStr,
                                group=groupStr,
                                replication=replicationStr,
                                pairType=unpairStr,
                                fileType=fileTypeStr,
                            )
                            outputFileList.append(outputUnPairStr)

                        fileList = inputFileList + outputFileList
                        fileStr = " ".join(fileList)

                        commandDict = dict()
                        commandDict.update(TrimPara.storeDict)
                        commandDict.update({ 'files' : fileStr })
                        CommandStr = commandStr.format(**commandDict)
                        Print.phraseStr = CommandStr
                        Print.runCommand()

                Print.stopLog()

if __name__ == "__main__":
    print("__name__ == "+__name__)
    Trim = trimmer()
    Trim.queryStr = "testing"
    Trim.trimming()
