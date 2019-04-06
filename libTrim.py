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
        self.commandStr = str()

        self.conditionList = list()
        self.groupList = list()
        self.replicationList = list()
        self.directionList = list()

        self.branchStr = str()
        self.pairStr = str()
        self.unpairStr = str()

        self.inputFileNameStr = str()
        self.outputFileNameStr = str()
        self.fileTypeStr = str()
        self.checkFolderList = str()

        self.testingBool = True

    def trimming(self):
        # ---- Action ----
        for folderStr in self.checkFolderList:
            pathlib.Path(folderStr).mkdir(parents=True,exist_ok=True)

        if type(self.conditionList) == type(list()) and self.conditionList != []:
            for conditionStr in self.conditionList:
                Print = libPrint.timer()
                Print.logFilenameStr = "03-trim-{branch}-{cond}".format(
                    branch=self.branchStr,
                    cond=conditionStr
                )
                Print.folderStr = "data/log/"
                Print.testingBool = self.testingBool
                Print.startLog()

                TrimPara = libConfig.config()
                TrimPara.queryStr = conditionStr
                TrimPara.folderStr = "data/config/"
                TrimPara.modeStr = "UPDATE"
                TrimPara.load()

                for groupStr in self.groupList:
                    for replicationStr in self.replicationList:
                        inputFileList = list()
                        outputFileList = list()
                        for directionStr in self.directionList:
                            inputStr = self.inputFileNameStr.format(
                                group=groupStr,
                                replication=replicationStr,
                                direction=directionStr,
                                fileType=self.fileTypeStr
                            )
                            inputFileList.append(inputStr)
                            outputPairStr = self.outputFileNameStr.format(
                                condition=conditionStr,
                                direction=directionStr,
                                group=groupStr,
                                replication=replicationStr,
                                pairType=self.pairStr,
                                fileType=self.fileTypeStr,
                            )
                            outputFileList.append(outputPairStr)
                            outputUnPairStr = self.outputFileNameStr.format(
                                condition=conditionStr,
                                direction=directionStr,
                                group=groupStr,
                                replication=replicationStr,
                                pairType=self.unpairStr,
                                fileType=self.fileTypeStr,
                            )
                            outputFileList.append(outputUnPairStr)

                        fileList = inputFileList + outputFileList
                        fileStr = " ".join(fileList)

                        commandDict = dict()
                        commandDict.update(TrimPara.storeDict)
                        commandDict.update({ 'files' : fileStr })
                        CommandStr = self.commandStr.format(**commandDict)
                        Print.phraseStr = CommandStr
                        Print.runCommand()

                Print.stopLog()

if __name__ == "__main__":
    print("__name__ == "+__name__)
    # ---- Parameter ----
    BinTrim = libConfig.config()
    BinTrim.queryStr = "binTrimmomatic"
    BinTrim.folderStr = "data/config/"
    BinTrim.modeStr = "UPDATE"
    BinTrim.load()

    ExpRep = libConfig.config()
    ExpRep.queryStr = "testing"
    ExpRep.folderStr = "data/config/"
    ExpRep.modeStr = "UPDATE"
    ExpRep.load()

    # ---- Initialization ----
    Trim = trimmer()
    Trim.commandStr = BinTrim.storeDict["command"]

    Trim.conditionList = ExpRep.storeDict.get("[trim]condition",[])
    Trim.groupList = ExpRep.storeDict.get("group",[])
    Trim.replicationList = ExpRep.storeDict.get("replication",[])
    Trim.directionList = ExpRep.storeDict.get("direction",[])

    Trim.branchStr = ExpRep.storeDict.get("branch","")
    Trim.pairStr = ExpRep.storeDict.get("pairPostfix","")
    Trim.unpairStr = ExpRep.storeDict.get("unpairPostfix","")

    Trim.inputFileNameStr = ExpRep.storeDict.get("[trim]inputFileName","")
    Trim.outputFileNameStr = ExpRep.storeDict.get("[trim]outputFileName","")
    Trim.fileTypeStr = ExpRep.storeDict.get("[trim]fileType","")
    Trim.checkFolderList = ExpRep.storeDict.get("[trim]checkFolder",[])

    if ExpRep.storeDict.get("testing",False):
        Trim.testingBool = True

    Trim.trimming()
