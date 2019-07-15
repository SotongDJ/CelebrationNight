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

  java -jar <bin>/trimmomatic-0.35.jar SE \\
    -phred33 -threads <threads> \\
    input.fq.gz output.fq.gz \\
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
        BinTrim.folderStr = "config/"
        BinTrim.modeStr = "UPDATE"
        BinTrim.load()

        ExpRep = libConfig.config()
        ExpRep.queryStr = self.queryStr
        ExpRep.folderStr = "config/"
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
        modeStr = ExpRep.storeDict.get("mode","")

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
                Print.folderStr = "log/"
                Print.testingBool = testingBool
                Print.startLog()

                TrimPara = libConfig.config()
                TrimPara.queryStr = conditionStr
                TrimPara.folderStr = "config/"
                TrimPara.modeStr = "UPDATE"
                TrimPara.load()
                headerStr = TrimPara.storeDict.get('header',"")

                for groupStr in groupList:
                    for replicationStr in replicationList:
                        if modeStr == "pairEnd":
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
                                    condition=headerStr,
                                    direction=directionStr,
                                    group=groupStr,
                                    replication=replicationStr,
                                    pairType=pairStr,
                                    fileType=fileTypeStr,
                                )
                                outputFileList.append(outputPairStr)
                                outputUnPairStr = outputFileNameStr.format(
                                    condition=headerStr,
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
                            commandDict.update({ 
                                'files' : fileStr,
                                'mode'  : "PE",
                            })
                            CommandStr = commandStr.format(**commandDict)
                            Print.phraseStr = CommandStr
                            Print.runCommand()

                        elif modeStr == "singleEnd":
                            inputStr = inputFileNameStr.format(
                                group=groupStr,
                                replication=replicationStr,
                                fileType=fileTypeStr
                            )
                            outputStr = outputFileNameStr.format(
                                condition=headerStr,
                                group=groupStr,
                                replication=replicationStr,
                                fileType=fileTypeStr,
                            )

                            fileStr = "{} {}".format(inputStr,outputStr)

                            commandDict = dict()
                            commandDict.update(TrimPara.storeDict)
                            commandDict.update({ 
                                'files' : fileStr,
                                'mode'  : "SE",
                            })
                            CommandStr = commandStr.format(**commandDict)
                            Print.phraseStr = CommandStr
                            Print.runCommand()

                Print.stopLog()

if __name__ == "__main__":
    print("__name__ == "+__name__)
    Trim = trimmer()
    Trim.queryStr = "testing"
    Trim.trimming()
