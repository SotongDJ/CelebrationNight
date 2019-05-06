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
        BinMap.folderStr = "data/config/"
        BinMap.modeStr = "UPDATE"
        BinMap.load()

        self.commandStr = BinMap.storeDict["command"]

        # ---- Initialization for Assembling ----
        Target = libConfig.config()
        Target.queryStr = self.branchStr
        Target.folderStr = "data/config/"
        Target.modeStr = "UPDATE"
        Target.load()

        self.groupList = Target.storeDict.get("group",[])
        self.replicationList = Target.storeDict.get("replication",[])
        self.hisat2ConditionStr = Target.storeDict.get("[stringtie2]hisat2Condition","")
        self.annotateConditionList = Target.storeDict.get("[stringtie2]annotateCondition",[])
        self.trimConditionList = Target.storeDict.get("[stringtie2]trimCondition",[])
        self.inputFileNameStr = Target.storeDict.get("[stringtie2]inputFileName","")
        self.outputFileNameStr = Target.storeDict.get("[stringtie2]outputFileName","")
        self.outputFolderStr = Target.storeDict.get("[stringtie2]outputFolder","")
        
        if not Target.storeDict.get("testing",True):
            self.testingBool = False
        else:
            self.testingBool = True

        for antCondStr in self.annotateConditionList:
            Annotate = libConfig.config()
            Annotate.queryStr = antCondStr
            Annotate.folderStr = "data/config/"
            Annotate.modeStr = "UPDATE"
            Annotate.load()

            threadStr = Annotate.storeDict.get("thread","")
            antPathStr = Annotate.storeDict.get("antPath","")

            for trimCondStr in self.trimConditionList:
                # ---- Action ----
                Print = libPrint.timer()
                Print.logFilenameStr = "05-stringtie-assembling-{annotate}-{trim}".format(
                    annotate=antCondStr,
                    trim=trimCondStr,
                )
                Print.folderStr = "data/log/"
                Print.testingBool = self.testingBool
                Print.startLog()
                
                for groupStr in self.groupList:
                    for repliStr in self.replicationList:
                        outputFolderStr = self.outputFolderStr.format(
                            annotateCondition=antCondStr,
                            trimCondition=trimCondStr
                        )
                        pathlib.Path(outputFolderStr).mkdir(parents=True,exist_ok=True)

                        outputFilenameStr = self.outputFileNameStr.format(
                            annotateCondition=antCondStr,
                            trimCondition=trimCondStr,
                            group=groupStr,
                            replication=repliStr
                        )

                        inputFilenameStr = self.inputFileNameStr.format(
                            annotateCondition=antCondStr,
                            hisat2Condition=self.hisat2ConditionStr,
                            trimCondition=trimCondStr,
                            group=groupStr,
                            replication=repliStr
                        )

                        CommandStr = self.commandStr.format(
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
        BinMap.folderStr = "data/config/"
        BinMap.modeStr = "UPDATE"
        BinMap.load()

        self.commandStr = BinMap.storeDict["command"]

        # ---- Initialization for Assembling ----
        Target = libConfig.config()
        Target.queryStr = self.branchStr
        Target.folderStr = "data/config/"
        Target.modeStr = "UPDATE"
        Target.load()

        self.groupList = Target.storeDict.get("group",[])
        self.replicationList = Target.storeDict.get("replication",[])
        self.annotateConditionList = Target.storeDict.get("[stringtie2]annotateCondition",[])
        self.trimConditionList = Target.storeDict.get("[stringtie2]trimCondition",[])
        self.inputFileNameStr = Target.storeDict.get("[stringtie2]outputFileName","")
        self.outputFileNameStr = Target.storeDict.get("[stringtie2]mergedFileName","")
        self.outputFolderStr = Target.storeDict.get("[stringtie2]mergedFolder","")
        
        if not Target.storeDict.get("testing",True):
            self.testingBool = False
        else:
            self.testingBool = True

        for antCondStr in self.annotateConditionList:
            Annotate = libConfig.config()
            Annotate.queryStr = antCondStr
            Annotate.folderStr = "data/config/"
            Annotate.modeStr = "UPDATE"
            Annotate.load()

            threadStr = Annotate.storeDict.get("thread","")
            antPathStr = Annotate.storeDict.get("antPath","")

            for trimCondStr in self.trimConditionList:
                # ---- Action ----
                Print = libPrint.timer()
                Print.logFilenameStr = "05-stringtie-merging-{annotate}-{trim}".format(
                    annotate=antCondStr,
                    trim=trimCondStr,
                )
                Print.folderStr = "data/log/"
                Print.testingBool = self.testingBool
                Print.startLog()

                self.gtfFileList = list()
                
                for groupStr in self.groupList:
                    for repliStr in self.replicationList:
                        outputFolderStr = self.outputFolderStr.format(
                            annotateCondition=antCondStr,
                            trimCondition=trimCondStr
                        )
                        pathlib.Path(outputFolderStr).mkdir(parents=True,exist_ok=True)

                        inputFileNameStr = self.inputFileNameStr.format(
                            annotateCondition=antCondStr,
                            trimCondition=trimCondStr,
                            group=groupStr,
                            replication=repliStr
                        )
                        self.gtfFileList.append(inputFileNameStr)

                outputFilenameStr = self.outputFileNameStr.format(
                    annotateCondition=antCondStr,
                    trimCondition=trimCondStr,
                )
                self.gtfFileList.append(inputFileNameStr)

                inputFilesStr = " ".join(self.gtfFileList)
                CommandStr = self.commandStr.format(
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
        BinMap.folderStr = "data/config/"
        BinMap.modeStr = "UPDATE"
        BinMap.load()

        self.commandStr = BinMap.storeDict["command"]

        # ---- Initialization for Assembling ----
        Target = libConfig.config()
        Target.queryStr = self.branchStr
        Target.folderStr = "data/config/"
        Target.modeStr = "UPDATE"
        Target.load()

        self.groupList = Target.storeDict.get("group",[])
        self.replicationList = Target.storeDict.get("replication",[])
        self.hisat2ConditionStr = Target.storeDict.get("[stringtie2]hisat2Condition","")
        self.annotateConditionList = Target.storeDict.get("[stringtie2]annotateCondition",[])
        self.trimConditionList = Target.storeDict.get("[stringtie2]trimCondition",[])
        self.inputFileNameStr = Target.storeDict.get("[stringtie2]inputFileName","")
        self.mergedFileNameStr = Target.storeDict.get("[stringtie2]mergedFileName","")
        self.balgownFolderStr = Target.storeDict.get("[stringtie2]ballgownFolder","")
        self.gtfFileNameStr = Target.storeDict.get("[stringtie2]gtfFileName","")
        self.tsvFileNameStr = Target.storeDict.get("[stringtie2]tsvFileName","")
        
        if not Target.storeDict.get("testing",True):
            self.testingBool = False
        else:
            self.testingBool = True

        for antCondStr in self.annotateConditionList:
            Annotate = libConfig.config()
            Annotate.queryStr = antCondStr
            Annotate.folderStr = "data/config/"
            Annotate.modeStr = "UPDATE"
            Annotate.load()

            threadStr = Annotate.storeDict.get("thread","")

            for trimCondStr in self.trimConditionList:
                # ---- Action ----
                Print = libPrint.timer()
                Print.logFilenameStr = "05-stringtie-estimating-{annotate}-{trim}".format(
                    annotate=antCondStr,
                    trim=trimCondStr,
                )
                Print.folderStr = "data/log/"
                Print.testingBool = self.testingBool
                Print.startLog()
                
                for groupStr in self.groupList:
                    for repliStr in self.replicationList:
                        ballgownPathStr = self.balgownFolderStr.format(
                            annotateCondition=antCondStr,
                            trimCondition=trimCondStr,
                            group=groupStr,
                            replication=repliStr
                        )
                        pathlib.Path(ballgownPathStr).mkdir(parents=True,exist_ok=True)

                        bamPathStr = self.inputFileNameStr.format(
                            annotateCondition=antCondStr,
                            hisat2Condition=self.hisat2ConditionStr,
                            trimCondition=trimCondStr,
                            group=groupStr,
                            replication=repliStr
                        )

                        mergeFileNameStr = self.mergedFileNameStr.format(
                            annotateCondition=antCondStr,
                            trimCondition=trimCondStr
                        )

                        gtfPathStr = self.gtfFileNameStr.format(
                            annotateCondition=antCondStr,
                            trimCondition=trimCondStr,
                            group=groupStr,
                            replication=repliStr
                        )

                        tsvPathStr = self.tsvFileNameStr.format(
                            annotateCondition=antCondStr,
                            trimCondition=trimCondStr,
                            group=groupStr,
                            replication=repliStr
                        )

                        CommandStr = self.commandStr.format(
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
        BinMap.folderStr = "data/config/"
        BinMap.modeStr = "UPDATE"
        BinMap.load()

        self.commandStr = BinMap.storeDict["command"]

        # ---- Initialization for Assembling ----
        Target = libConfig.config()
        Target.queryStr = self.branchStr
        Target.folderStr = "data/config/"
        Target.modeStr = "UPDATE"
        Target.load()

        self.groupList = Target.storeDict.get("group",[])
        self.replicationList = Target.storeDict.get("replication",[])
        self.hisat2ConditionStr = Target.storeDict.get("[stringtie2]hisat2Condition","")
        self.annotateConditionList = Target.storeDict.get("[stringtie2]annotateCondition",[])
        self.trimConditionList = Target.storeDict.get("[stringtie2]trimCondition",[])
        self.inputFileNameStr = Target.storeDict.get("[stringtie2]inputFileName","")
        self.balgownFolderStr = Target.storeDict.get("[dsStringtie2]ballgownFolder","")
        self.gtfFileNameStr = Target.storeDict.get("[dsStringtie2]gtfFileName","")
        self.tsvFileNameStr = Target.storeDict.get("[dsStringtie2]tsvFileName","")
        
        if not Target.storeDict.get("testing",True):
            self.testingBool = False
        else:
            self.testingBool = True

        for antCondStr in self.annotateConditionList:
            Annotate = libConfig.config()
            Annotate.queryStr = antCondStr
            Annotate.folderStr = "data/config/"
            Annotate.modeStr = "UPDATE"
            Annotate.load()

            threadStr = Annotate.storeDict.get("thread","")
            antPathStr = Annotate.storeDict.get("antPath","")

            for trimCondStr in self.trimConditionList:
                # ---- Action ----
                Print = libPrint.timer()
                Print.logFilenameStr = "05-stringtie-directEstimating-{annotate}-{trim}".format(
                    annotate=antCondStr,
                    trim=trimCondStr,
                )
                Print.folderStr = "data/log/"
                Print.testingBool = self.testingBool
                Print.startLog()
                
                for groupStr in self.groupList:
                    for repliStr in self.replicationList:
                        ballgownPathStr = self.balgownFolderStr.format(
                            annotateCondition=antCondStr,
                            trimCondition=trimCondStr,
                            group=groupStr,
                            replication=repliStr
                        )
                        pathlib.Path(ballgownPathStr).mkdir(parents=True,exist_ok=True)

                        bamPathStr = self.inputFileNameStr.format(
                            annotateCondition=antCondStr,
                            hisat2Condition=self.hisat2ConditionStr,
                            trimCondition=trimCondStr,
                            group=groupStr,
                            replication=repliStr
                        )

                        gtfPathStr = self.gtfFileNameStr.format(
                            annotateCondition=antCondStr,
                            trimCondition=trimCondStr,
                            group=groupStr,
                            replication=repliStr
                        )

                        tsvPathStr = self.tsvFileNameStr.format(
                            annotateCondition=antCondStr,
                            trimCondition=trimCondStr,
                            group=groupStr,
                            replication=repliStr
                        )

                        CommandStr = self.commandStr.format(
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
