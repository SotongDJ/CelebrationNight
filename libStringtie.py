#!/usr/bin/env python3
import libConfig, libPrint
import pathlib
"""
    --- README of Stringtie 2 related actions ---
Original Command:
    # Stringtie 2 assembling
    stringtie [BAM file] -o [Result GTF file] \
        -p [Thread] -G [Reference GFF file] -e


    --- README ---
"""
class assembler:
    def __init__(self):
        self.branchStr = ""
        self.testingBool = True

    def assembling(self):
        # ---- Parameter for Assembling ----
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

        groupList = Target.storeDict.get("group",[])
        replicationList = Target.storeDict.get("replication",[])
        hisat2ConditionStr = Target.storeDict.get("[stringtie2]hisat2Condition","")
        conditionList = Target.storeDict.get("[stringtie2]conditionList",[])
        inputFileNameStr = Target.storeDict.get("[stringtie2]inputFileName","")
        outputFileNameStr = Target.storeDict.get("[stringtie2]outputFileName","")
        outputFolderStr = Target.storeDict.get("[stringtie2]outputFolder","")
        
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
            Print.logFilenameStr = "05-stringtie-assembling-{annotate}-{trim}".format(
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

        groupList = Target.storeDict.get("group",[])
        replicationList = Target.storeDict.get("replication",[])
        conditionList = Target.storeDict.get("[stringtie2]conditionList",[])
        inputFileNameStr = Target.storeDict.get("[stringtie2]outputFileName","")
        outputFileNameStr = Target.storeDict.get("[stringtie2]mergedFileName","")
        outputFolderStr = Target.storeDict.get("[stringtie2]mergedFolder","")
        
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
            Print.logFilenameStr = "05-stringtie-merging-{annotate}-{trim}".format(
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

                    inputFileNameStr = inputFileNameStr.format(
                        annotateCondition=antCondStr,
                        trimCondition=trimCondStr,
                        group=groupStr,
                        replication=repliStr
                    )
                    gtfFileList.append(inputFileNameStr)

            outputFilenameStr = outputFileNameStr.format(
                annotateCondition=antCondStr,
                trimCondition=trimCondStr,
            )
            gtfFileList.append(inputFileNameStr)

            inputFilesStr = " ".join(gtfFileList)
            CommandStr = commandStr.format(
                inputfiles=inputFilesStr,
                outputfile=outputFilenameStr,
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

        groupList = Target.storeDict.get("group",[])
        replicationList = Target.storeDict.get("replication",[])
        hisat2ConditionStr = Target.storeDict.get("[stringtie2]hisat2Condition","")
        conditionList = Target.storeDict.get("[stringtie2]conditionList",[])
        inputFileNameStr = Target.storeDict.get("[stringtie2]inputFileName","")
        mergedFileNameStr = Target.storeDict.get("[stringtie2]mergedFileName","")
        balgownFolderStr = Target.storeDict.get("[stringtie2]ballgownFolder","")
        gtfFileNameStr = Target.storeDict.get("[stringtie2]gtfFileName","")
        tsvFileNameStr = Target.storeDict.get("[stringtie2]tsvFileName","")
        
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

            # ---- Action ----
            Print = libPrint.timer()
            Print.logFilenameStr = "05-stringtie-estimating-{annotate}-{trim}".format(
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

class directEstimator:
    def __init__(self):
        self.branchStr = ""
        self.testingBool = True

    def directEstimating(self):
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

        groupList = Target.storeDict.get("group",[])
        replicationList = Target.storeDict.get("replication",[])
        hisat2ConditionStr = Target.storeDict.get("[stringtie2]hisat2Condition","")
        conditionList = Target.storeDict.get("[stringtie2]conditionList",[])
        inputFileNameStr = Target.storeDict.get("[stringtie2]inputFileName","")
        balgownFolderStr = Target.storeDict.get("[dsStringtie2]ballgownFolder","")
        gtfFileNameStr = Target.storeDict.get("[dsStringtie2]gtfFileName","")
        tsvFileNameStr = Target.storeDict.get("[dsStringtie2]tsvFileName","")
        
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
            Print.logFilenameStr = "05-stringtie-directEstimating-{annotate}-{trim}".format(
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

                    CommandStr = commandStr.format(
                        thread=threadStr,
                        mergePath=antPathStr,
                        bamfile=bamPathStr,
                        ballgownPath=ballgownPathStr,
                        gtffile=gtfPathStr,
                        tsvfile=tsvPathStr
                    )
                    
                    Print.phraseStr = CommandStr
                    Print.runCommand()

            Print.stopLog()
