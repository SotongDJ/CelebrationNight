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
