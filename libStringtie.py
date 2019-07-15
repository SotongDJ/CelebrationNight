#!/usr/bin/env python3
import libConfig, libPrint
import pathlib
"""
    --- README of Stringtie related actions ---
Original Command:
    # Stringtie assembling
    stringtie [BAM file] -o [Result GTF file] \
        -p [Thread] -G [Reference GFF file] -e


    --- README ---
"""
class assembler:
    def __init__(self):
        self.branchStr = ""
        self.testingBool = True
        self.withoutAnnotation = False
        self.headerStr = "Stringtie"

    def assembling(self):
        # ---- Parameter for Assembling ----
        if self.withoutAnnotation:
            BinMap = libConfig.config()
            BinMap.queryStr = "binStringTie-RUN-withoutAnnotation"
            BinMap.folderStr = "config/"
            BinMap.modeStr = "UPDATE"
            BinMap.load()
        else:
            BinMap = libConfig.config()
            BinMap.queryStr = "binStringTie-RUN"
            BinMap.folderStr = "config/"
            BinMap.modeStr = "UPDATE"
            BinMap.load()

        commandStr = BinMap.storeDict["command"]

        # ---- Initialization for Assembling ----
        Target = libConfig.config()
        Target.queryStr = self.branchStr
        Target.folderStr = "config/"
        Target.modeStr = "UPDATE"
        Target.load()

        branchStr = Target.storeDict.get("branch","")
        groupList = Target.storeDict.get("group",[])
        replicationList = Target.storeDict.get("replication",[])
        hisat2ConditionStr = Target.storeDict.get("[hisat2]Condition","")
        conditionList = Target.storeDict.get("conditionList",[])
        inputFileNameStr = Target.storeDict.get("[{}]inputFileName".format(self.headerStr),"")
        outputFileNameStr = Target.storeDict.get("[{}]outputFileName".format(self.headerStr),"")
        outputFolderStr = Target.storeDict.get("[{}]outputFolder".format(self.headerStr),"")
        
        if not Target.storeDict.get("testing",True):
            self.testingBool = False
        else:
            self.testingBool = True

        for conditionTup in conditionList:
            antCondStr = conditionTup[0]
            trimCondStr = conditionTup[1]

            Annotate = libConfig.config()
            Annotate.queryStr = antCondStr
            Annotate.folderStr = "config/"
            Annotate.modeStr = "UPDATE"
            Annotate.load()

            threadStr = Annotate.storeDict.get("thread","")
            antPathStr = Annotate.storeDict.get("antPath","")

            # ---- Action ----
            Print = libPrint.timer()
            Print.logFilenameStr = "05-{stringtie}-assembling-{branch}-{annotate}-{trim}".format(
                stringtie=self.headerStr,
                branch=branchStr,
                annotate=antCondStr,
                trim=trimCondStr,
            )
            Print.folderStr = "log/"
            Print.testingBool = self.testingBool
            Print.startLog()
            
            for groupStr in groupList:
                for repliStr in replicationList:
                    outputFolderStr = outputFolderStr.format(
                        annotateCondition=antCondStr,
                        trimCondition=trimCondStr
                    )
                    pathlib.Path(outputFolderStr).mkdir(parents=True,exist_ok=True)

                    outputFilenameStr = outputFileNameStr.format(
                        annotateCondition=antCondStr,
                        trimCondition=trimCondStr,
                        group=groupStr,
                        replication=repliStr
                    )

                    inputFilenameStr = inputFileNameStr.format(
                        annotateCondition=antCondStr,
                        hisat2Condition=hisat2ConditionStr,
                        trimCondition=trimCondStr,
                        group=groupStr,
                        replication=repliStr
                    )

                    CommandStr = commandStr.format(
                        bamfile=inputFilenameStr,
                        outputfile=outputFilenameStr,
                        thread=threadStr,
                        antPath=antPathStr
                    )
                    
                    Print.phraseStr = CommandStr
                    Print.runCommand()

            Print.stopLog()

class merger:
    def __init__(self):
        self.branchStr = ""
        self.testingBool = True
        self.headerStr = "Stringtie"

    def merging(self):
        # ---- Parameter for Assembling ----
        BinMap = libConfig.config()
        BinMap.queryStr = "binStringTie-MERGE"
        BinMap.folderStr = "config/"
        BinMap.modeStr = "UPDATE"
        BinMap.load()

        commandStr = BinMap.storeDict["command"]

        # ---- Initialization for Assembling ----
        Target = libConfig.config()
        Target.queryStr = self.branchStr
        Target.folderStr = "config/"
        Target.modeStr = "UPDATE"
        Target.load()

        branchStr = Target.storeDict.get("branch","")
        groupList = Target.storeDict.get("group",[])
        replicationList = Target.storeDict.get("replication",[])
        conditionList = Target.storeDict.get("conditionList",[])
        inputFileNameStr = Target.storeDict.get("[{}]outputFileName".format(self.headerStr),"")
        outputFileNameStr = Target.storeDict.get("[{}]mergedFileName".format(self.headerStr),"")
        outputFolderStr = Target.storeDict.get("[{}]mergedFolder".format(self.headerStr),"")
        
        if not Target.storeDict.get("testing",True):
            self.testingBool = False
        else:
            self.testingBool = True

        for conditionTup in conditionList:
            antCondStr = conditionTup[0]
            trimCondStr = conditionTup[1]

            Annotate = libConfig.config()
            Annotate.queryStr = antCondStr
            Annotate.folderStr = "config/"
            Annotate.modeStr = "UPDATE"
            Annotate.load()

            threadStr = Annotate.storeDict.get("thread","")
            antPathStr = Annotate.storeDict.get("antPath","")

            # ---- Action ----
            Print = libPrint.timer()
            Print.logFilenameStr = "05-{stringtie}-merging-{branch}-{annotate}-{trim}".format(
                stringtie=self.headerStr,
                branch=branchStr,
                annotate=antCondStr,
                trim=trimCondStr,
            )
            Print.folderStr = "log/"
            Print.testingBool = self.testingBool
            Print.startLog()

            gtfFileList = list()
            
            for groupStr in groupList:
                for repliStr in replicationList:
                    outputFolderStr = outputFolderStr.format(
                        annotateCondition=antCondStr,
                        trimCondition=trimCondStr
                    )
                    pathlib.Path(outputFolderStr).mkdir(parents=True,exist_ok=True)

                    inputFileName = inputFileNameStr.format(
                        annotateCondition=antCondStr,
                        trimCondition=trimCondStr,
                        group=groupStr,
                        replication=repliStr
                    )
                    gtfFileList.append(inputFileName)

            outputFilename = outputFileNameStr.format(
                annotateCondition=antCondStr,
                trimCondition=trimCondStr,
            )

            inputFilesStr = " ".join(gtfFileList)
            CommandStr = commandStr.format(
                inputfiles=inputFilesStr,
                outputfile=outputFilename,
                thread=threadStr,
                antPath=antPathStr
            )
                    
            Print.phraseStr = CommandStr
            Print.runCommand()

            Print.stopLog()

class estimator:
    def __init__(self):
        self.branchStr = ""
        self.testingBool = True
        self.directEstimating = False
        self.headerStr = "Stringtie"

    def estimating(self):
        # ---- Parameter for Assembling ----
        BinMap = libConfig.config()
        BinMap.queryStr = "binStringTie-ESTIMATE"
        BinMap.folderStr = "config/"
        BinMap.modeStr = "UPDATE"
        BinMap.load()

        commandStr = BinMap.storeDict["command"]

        # ---- Initialization for Assembling ----
        Target = libConfig.config()
        Target.queryStr = self.branchStr
        Target.folderStr = "config/"
        Target.modeStr = "UPDATE"
        Target.load()

        branchStr = Target.storeDict.get("branch","")
        groupList = Target.storeDict.get("group",[])
        replicationList = Target.storeDict.get("replication",[])
        hisat2ConditionStr = Target.storeDict.get("[hisat2]Condition","")
        conditionList = Target.storeDict.get("conditionList",[])
        inputFileNameStr = Target.storeDict.get("[{}]inputFileName".format(self.headerStr),"")
        mergedFileNameStr = Target.storeDict.get("[{}]mergedFileName".format(self.headerStr),"")
        balgownFolderStr = Target.storeDict.get("[{}]ballgownFolder".format(self.headerStr),"")
        gtfFileNameStr = Target.storeDict.get("[{}]gtfFileName".format(self.headerStr),"")
        tsvFileNameStr = Target.storeDict.get("[{}]tsvFileName".format(self.headerStr),"")
        
        if not Target.storeDict.get("testing",True):
            self.testingBool = False
        else:
            self.testingBool = True

        for conditionTup in conditionList:
            antCondStr = conditionTup[0]
            trimCondStr = conditionTup[1]

            Annotate = libConfig.config()
            Annotate.queryStr = antCondStr
            Annotate.folderStr = "config/"
            Annotate.modeStr = "UPDATE"
            Annotate.load()

            threadStr = Annotate.storeDict.get("thread","")
            antPathStr = Annotate.storeDict.get("antPath","")

            # ---- Action ----
            Print = libPrint.timer()
            Print.logFilenameStr = "05-{stringtie}-estimating-{branch}-{annotate}-{trim}".format(
                stringtie=self.headerStr,
                branch=branchStr,
                annotate=antCondStr,
                trim=trimCondStr,
            )
            Print.folderStr = "log/"
            Print.testingBool = self.testingBool
            Print.startLog()
            
            for groupStr in groupList:
                for repliStr in replicationList:
                    ballgownPathStr = balgownFolderStr.format(
                        annotateCondition=antCondStr,
                        trimCondition=trimCondStr,
                        group=groupStr,
                        replication=repliStr
                    )
                    pathlib.Path(ballgownPathStr).mkdir(parents=True,exist_ok=True)

                    bamPathStr = inputFileNameStr.format(
                        annotateCondition=antCondStr,
                        hisat2Condition=hisat2ConditionStr,
                        trimCondition=trimCondStr,
                        group=groupStr,
                        replication=repliStr
                    )

                    mergeFileNameStr = mergedFileNameStr.format(
                        annotateCondition=antCondStr,
                        trimCondition=trimCondStr
                    )

                    gtfPathStr = gtfFileNameStr.format(
                        annotateCondition=antCondStr,
                        trimCondition=trimCondStr,
                        group=groupStr,
                        replication=repliStr
                    )

                    tsvPathStr = tsvFileNameStr.format(
                        annotateCondition=antCondStr,
                        trimCondition=trimCondStr,
                        group=groupStr,
                        replication=repliStr
                    )

                    if self.directEstimating:
                        CommandStr = commandStr.format(
                            thread=threadStr,
                            mergePath=antPathStr,
                            bamfile=bamPathStr,
                            ballgownPath=ballgownPathStr,
                            gtffile=gtfPathStr,
                            tsvfile=tsvPathStr
                        )
                    else:
                        CommandStr = commandStr.format(
                            thread=threadStr,
                            mergePath=mergeFileNameStr,
                            bamfile=bamPathStr,
                            ballgownPath=ballgownPathStr,
                            gtffile=gtfPathStr,
                            tsvfile=tsvPathStr
                        )

                    Print.phraseStr = CommandStr
                    Print.runCommand()

            Print.stopLog()
