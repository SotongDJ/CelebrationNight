#!/usr/bin/env python3
import libConfig, libPrint
import pathlib
"""
--- README of HISAT2 related actions ---
Original Command of Building HISAT2 Index:
  hisat2-build -p [THREAD] <Path and Name of GENOME File> \\
    <OUTPUT FOLDER for HISAT2>/<codename>

--- README ---
"""
class indexer:
    def __init__(self):
        # ---- Initialization ----
        self.commandStr = str()

        self.titleStr = ""
        self.folderStr = ""
        self.seqPathStr = ""
        self.indexHeaderStr = ""
        self.threadStr = ""

        self.testingBool = False

    def indexing(self):
        # ---- Action ----
        pathlib.Path(self.folderStr).mkdir(parents=True,exist_ok=True)

        Print = libPrint.timer()
        Print.logFilenameStr = "02-hisat2-index-{title}".format(
            title=self.titleStr
        )
        Print.folderStr = "data/log/"
        Print.testingBool = self.testingBool
        Print.startLog()

        CommandStr = self.commandStr.format(
            seqPath=self.seqPathStr,
            indexHeader=self.indexHeaderStr,
            thread=self.threadStr
        )
        Print.phraseStr = CommandStr
        Print.runCommand()

        Print.stopLog()
        
class aligner:
    def __init__(self):
        self.branchStr = ""
        self.testingBool = False
    
    def aligning(self):
        HISAT2 = libConfig.config()
        HISAT2.queryStr = "binHISAT2-RUN"
        HISAT2.folderStr = "data/config/"
        HISAT2.modeStr = "UPDATE"
        HISAT2.load()

        commandStr = HISAT2.storeDict.get("command","")

        expRep = libConfig.config()
        expRep.queryStr = self.branchStr
        expRep.folderStr = "data/config/"
        expRep.modeStr = "UPDATE"
        expRep.load()

        trimConditionList = expRep.storeDict.get("[trim]condition",[])
        hisat2ConditionList = expRep.storeDict.get("[hisat2]hisat2Condition",[])
        annotateConditionList = expRep.storeDict.get("[hisat2]annotateCondition",[])
        groupList = expRep.storeDict.get("group",[])
        replicationList = expRep.storeDict.get("replication",[])

        directionDict = expRep.storeDict.get("[hisat2]direction",dict())

        pairPostfixStr = expRep.storeDict.get("pairPostfix","")
        fileTypeStr = expRep.storeDict.get("[trim]fileType","")
        inputFileNameStr = expRep.storeDict.get("[hisat2]inputFileName","")
        outputFolderStr = expRep.storeDict.get("[hisat2]outputFolder","")
        outputFileNameStr = expRep.storeDict.get("[hisat2]outputFileName","")

        if not expRep.storeDict.get("testing",True):
            self.testingBool = False
        else:
            self.testingBool = True

        for trimConditionStr in trimConditionList:
            for annotateConditionStr in annotateConditionList:
                finalOutputFolderStr = outputFolderStr.format(
                    annotateCondition=annotateConditionStr,
                    trimCondition=trimConditionStr
                )
                pathlib.Path(finalOutputFolderStr).mkdir(parents=True,exist_ok=True)
                for hisat2ConditionStr in hisat2ConditionList:
                    Print = libPrint.timer()
                    Print.logFilenameStr = "04-hisat2-{hisat2cond}-{annotateCon}-{trimCon}".format(
                        hisat2cond=hisat2ConditionStr,
                        annotateCon=annotateConditionStr,
                        trimCon=trimConditionStr,
                    )
                    Print.folderStr = "data/log/"
                    Print.testingBool = self.testingBool
                    Print.startLog()
                    for groupStr in groupList:
                        for replicationStr in replicationList:
                            finalDict = dict()

                            Para = libConfig.config() #parameters
                            Para.queryStr = hisat2ConditionStr
                            Para.folderStr = "data/config/"
                            Para.modeStr = "UPDATE"
                            Para.load()
                            finalDict.update(Para.storeDict)

                            Spec = libConfig.config() #parameters
                            Spec.queryStr = annotateConditionStr
                            Spec.folderStr = "data/config/"
                            Spec.modeStr = "UPDATE"
                            Spec.load()
                            finalDict.update({
                                "indexHeader" : Spec.storeDict.get("indexHeader","")
                            })

                            forwardDict = {
                                "trimCondition" : trimConditionStr,
                                "group" : groupStr,
                                "replication": replicationStr,
                                "direction" : directionDict['1'],
                                "pairType" : pairPostfixStr,
                                "fileType" : fileTypeStr,
                            }
                            reverseDict = {
                                "trimCondition" : trimConditionStr,
                                "group" : groupStr,
                                "replication": replicationStr,
                                "direction" : directionDict['2'],
                                "pairType" : pairPostfixStr,
                                "fileType" : fileTypeStr,
                            }
                            outputDict = {
                                "annotateCondition": annotateConditionStr,
                                "trimCondition": trimConditionStr,
                                "hisat2Condition": hisat2ConditionStr,
                                "group": groupStr,
                                "replication": replicationStr,
                                "fileType": ".sam",
                            }
                            
                            finalDict.update({
                                "forwardFASTQ" : inputFileNameStr.format(**forwardDict),
                                "reverseFASTQ" : inputFileNameStr.format(**reverseDict),
                                "outputSAM"    : outputFileNameStr.format(**outputDict)
                            })

                            finalCommandStr = commandStr.format(**finalDict)
                            Print.phraseStr = finalCommandStr
                            Print.runCommand()
                    Print.stopLog()

if __name__ == "__main__":
    print("__name__ == "+__name__)
    # ---- Parameter for Indexing ----
    BinIndex = libConfig.config()
    BinIndex.queryStr = "binHISAT2-BUILD"
    BinIndex.folderStr = "data/config/"
    BinIndex.modeStr = "UPDATE"
    BinIndex.load()

    for indexStr in ["speciesTestingA","speciesTestingB","speciesTestingC"]:
        # ---- Initialization for Indexing ----
        Target = libConfig.config()
        Target.queryStr = indexStr
        Target.folderStr = "data/config/"
        Target.modeStr = "UPDATE"
        Target.load()

        Index = indexer()
        Index.commandStr = BinIndex.storeDict["command"]

        Index.titleStr = indexStr
        Index.folderStr = Target.storeDict.get("checkFolder","")
        Index.seqPathStr = Target.storeDict.get("seqPath","")
        Index.indexHeaderStr = Target.storeDict.get("indexHeader","")
        Index.threadStr = Target.storeDict.get("thread","")

        if Target.storeDict.get("testing",False):
            Index.testingBool = True

        Index.indexing()
