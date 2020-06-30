#!/usr/bin/env python3
import libConfig, libPrint
import pathlib
"""
    --- README of HISAT2 related actions ---
Original Command:
    # Building HISAT2 Index
    hisat2-build -p [THREAD] <Path and Name of GENOME File> \\
        < prefix of HISAT2-build genome index (path+header)>
    # Aligning and mapping
    hisat2 \\
        -q [--dta/--dta-cufflinks] --phred[phred] -p [thread] \\
        -x [prefix of HISAT2-build genome index] \\
        -1 [forward fastq files of] \\
        -2 [reverse fastq files of] \\
        -S [output SAM files] \\
    # Convert SAM to BAM
    samtools view -o [out.bam] -Su [in.sam]
    # Sorting BAM for decreasing file size
    samtools sort -o [out-sorted.bam] [in.bam]

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
        # ---- Parameter for Indexing ----
        BinIndex = libConfig.config()
        BinIndex.queryStr = "binHISAT2-BUILD"
        BinIndex.folderStr = "config/"
        BinIndex.modeStr = "UPDATE"
        BinIndex.load()
        # ---- Initialization for Indexing ----

        self.commandStr = BinIndex.storeDict["command"]

        Target = libConfig.config()
        Target.queryStr = self.titleStr
        Target.folderStr = "config/"
        Target.modeStr = "UPDATE"
        Target.load()

        self.folderStr = Target.storeDict["checkFolder"]
        self.seqPathStr = Target.storeDict["seqPath"]
        self.indexHeaderStr = Target.storeDict["indexHeader"]
        self.threadStr = Target.storeDict["thread"]

        if not Target.storeDict.get("testing",True):
            self.testingBool = False
        else:
            self.testingBool = True

        # ---- Action ----
        pathlib.Path(self.folderStr).mkdir(parents=True,exist_ok=True)

        Print = libPrint.timer()
        Print.logFilenameStr = "02-hisat2-index-{title}".format(title=self.titleStr)
        Print.folderStr = "log/"
        Print.testingBool = self.testingBool
        Print.startLog()

        infoDict = {
            'seqPath' : self.seqPathStr,
            'indexHeader' : self.indexHeaderStr,
            'thread' : self.threadStr,
        }
        CommandStr = self.commandStr.format(**infoDict)
        Print.phraseStr = CommandStr
        Print.runCommand()

        Print.stopLog()
   
class aligner:
    def __init__(self):
        self.queryStr = ""
        self.testingBool = False
    
    def aligning(self):
        BinHISAT2 = libConfig.config()
        BinHISAT2.queryStr = "binHISAT2-RUN"
        BinHISAT2.folderStr = "config/"
        BinHISAT2.modeStr = "UPDATE"
        BinHISAT2.load()

        SAMconvert = libConfig.config()
        SAMconvert.queryStr = "binSAMtools-CONVERT"
        SAMconvert.folderStr = "config/"
        SAMconvert.modeStr = "UPDATE"
        SAMconvert.load()

        SAMsort = libConfig.config()
        SAMsort.queryStr = "binSAMtools-SORT"
        SAMsort.folderStr = "config/"
        SAMsort.modeStr = "UPDATE"
        SAMsort.load()

        Remove = libConfig.config()
        Remove.queryStr = "commandRM"
        Remove.folderStr = "config/"
        Remove.modeStr = "UPDATE"
        Remove.load()

        expRep = libConfig.config()
        expRep.queryStr = self.queryStr
        expRep.folderStr = "config/"
        expRep.modeStr = "UPDATE"
        expRep.load()

        branchStr = expRep.storeDict["branch"]
        pairPostfixStr = expRep.storeDict["pairPostfix"]
        unpairPostfixStr = expRep.storeDict["unpairPostfix"]
        groupList = expRep.storeDict["group"]
        modeStr = expRep.storeDict["mode"]
        replicationList = expRep.storeDict["replication"]
        conditionList = expRep.storeDict["conditionsList"]
        for conditionDict in conditionList:
            annotateConditionStr = conditionDict["genome"]
            trimConditionStr = conditionDict["trim"]
            hisat2ConditionStr = conditionDict["map"]
            directionDict = expRep.storeDict["[hisat2]direction"]

            fileTypeStr = expRep.storeDict["[trim]fileType"]
            inputFileNameStr = expRep.storeDict["[hisat2]inputFileName"]
            outputFolderStr = expRep.storeDict["[hisat2]outputFolder"]
            outputFileNameStr = expRep.storeDict["[hisat2]outputFileName"]

            if not expRep.storeDict.get("testing",True):
                self.testingBool = False
            else:
                self.testingBool = True

            finalOutputFolderStr = outputFolderStr.format(
                annotate=annotateConditionStr,
                trim=trimConditionStr
            )
            pathlib.Path(finalOutputFolderStr).mkdir(parents=True,exist_ok=True)

            Print = libPrint.timer()
            Print.logFilenameStr = "04-hs1-hisat2-{branch}-{hisat2cond}-{annotateCon}-{trimCon}".format(
                branch=branchStr,
                hisat2cond=hisat2ConditionStr,
                annotateCon=annotateConditionStr,
                trimCon=trimConditionStr,
            )
            Print.folderStr = "log/"
            Print.testingBool = self.testingBool
            Print.startLog()
            for groupStr in groupList:
                for replicationStr in replicationList:
                    finalDict = dict()

                    Para = libConfig.config() #parameters
                    Para.queryStr = hisat2ConditionStr
                    Para.folderStr = "config/"
                    Para.modeStr = "UPDATE"
                    Para.load()
                    finalDict.update(Para.storeDict)

                    Spec = libConfig.config() #parameters
                    Spec.queryStr = annotateConditionStr
                    Spec.folderStr = "config/"
                    Spec.modeStr = "UPDATE"
                    Spec.load()
                    
                    finalDict.update({ "indexHeader" : Spec.storeDict["indexHeader"] })
                    
                    if modeStr == "pairEnd":
                        pairForwardDict = {
                            "trim" : trimConditionStr,
                            "group" : groupStr,
                            "replication": replicationStr,
                            "direction" : directionDict['1'],
                            "pairType" : pairPostfixStr,
                            "fileType" : fileTypeStr,
                        }
                        pairReverseDict = {
                            "trim" : trimConditionStr,
                            "group" : groupStr,
                            "replication": replicationStr,
                            "direction" : directionDict['2'],
                            "pairType" : pairPostfixStr,
                            "fileType" : fileTypeStr,
                        }
                        unpairForwardDict = {
                            "trim" : trimConditionStr,
                            "group" : groupStr,
                            "replication": replicationStr,
                            "direction" : directionDict['1'],
                            "pairType" : unpairPostfixStr,
                            "fileType" : fileTypeStr,
                        }
                        unpairReverseDict = {
                            "trim" : trimConditionStr,
                            "group" : groupStr,
                            "replication": replicationStr,
                            "direction" : directionDict['2'],
                            "pairType" : unpairPostfixStr,
                            "fileType" : fileTypeStr,
                        }
                    elif modeStr == "singleEnd":
                        unpairDict = {
                            "trim" : trimConditionStr,
                            "group" : groupStr,
                            "replication": replicationStr,
                            "fileType" : fileTypeStr,
                        }

                    samDict = {
                        "annotate": annotateConditionStr,
                        "trim": trimConditionStr,
                        "hisat2Condition": hisat2ConditionStr,
                        "group": groupStr,
                        "replication": replicationStr,
                        "fileType": ".sam",
                    }
                    samFileStr = outputFileNameStr.format(**samDict)
                    bamDict = {
                        "annotate": annotateConditionStr,
                        "trim": trimConditionStr,
                        "hisat2Condition": hisat2ConditionStr,
                        "group": groupStr,
                        "replication": replicationStr,
                        "fileType": ".bam",
                    }
                    bamFileStr = outputFileNameStr.format(**bamDict)
                    sortedBAMDict = {
                        "annotate": annotateConditionStr,
                        "trim": trimConditionStr,
                        "hisat2Condition": hisat2ConditionStr,
                        "group": groupStr,
                        "replication": replicationStr,
                        "fileType": "-sorted.bam",
                    }
                    sortedBAMFileStr = outputFileNameStr.format(**sortedBAMDict)

                    if pathlib.Path(samFileStr).exists():
                        Print.phraseStr = "SAM File existed: "+samFileStr
                        Print.printTimeStamp()
                    elif not pathlib.Path(samFileStr).exists() and not pathlib.Path(bamFileStr).exists() and not pathlib.Path(sortedBAMFileStr).exists():
                        if modeStr == "pairEnd":
                            commandStr = BinHISAT2.storeDict.get("command-PE","")
                            finalDict.update({
                                "pairForwardFASTQ" : inputFileNameStr.format(**pairForwardDict),
                                "pairReverseFASTQ" : inputFileNameStr.format(**pairReverseDict),
                                "unpairForwardFASTQ" : inputFileNameStr.format(**unpairForwardDict),
                                "unpairReverseFASTQ" : inputFileNameStr.format(**unpairReverseDict),
                                "outputSAM"    : samFileStr
                            })
                            finalCommandStr = commandStr.format(**finalDict)
                            Print.phraseStr = finalCommandStr
                            Print.runCommand()
                        elif modeStr == "singleEnd":
                            commandStr = BinHISAT2.storeDict.get("command-SE","")
                            finalDict.update({
                                "unpairFASTQ" : inputFileNameStr.format(**unpairDict),
                                "outputSAM"    : samFileStr
                            })
                            finalCommandStr = commandStr.format(**finalDict)
                            Print.phraseStr = finalCommandStr
                            Print.runCommand()

                    if pathlib.Path(bamFileStr).exists():
                        Print.phraseStr = "BAM File existed: "+bamFileStr
                        Print.printTimeStamp()
                    elif not pathlib.Path(bamFileStr).exists() and not pathlib.Path(sortedBAMFileStr).exists():
                        commandStr = SAMconvert.storeDict.get("command","")
                        finalDict.update({
                            "outputBAM" : bamFileStr,
                            "inputSAM" : samFileStr,
                        })
                        finalCommandStr = commandStr.format(**finalDict)
                        Print.phraseStr = finalCommandStr
                        Print.runCommand()

                    if pathlib.Path(samFileStr).exists() and pathlib.Path(bamFileStr).exists():
                        commandStr = Remove.storeDict.get("command","")
                        finalCommandStr = commandStr.format(target=samFileStr)
                        Print.phraseStr = finalCommandStr
                        Print.runCommand()

                    if pathlib.Path(sortedBAMFileStr).exists():
                        Print.phraseStr = "Sorted BAM File existed: "+sortedBAMFileStr
                        Print.printTimeStamp()
                    else:
                        commandStr = SAMsort.storeDict.get("command","")
                        finalDict.update({
                            "outputBAM" : sortedBAMFileStr,
                            "inputBAM" : bamFileStr,
                        })
                        finalCommandStr = commandStr.format(**finalDict)
                        Print.phraseStr = finalCommandStr
                        Print.runCommand()

                    if pathlib.Path(bamFileStr).exists() and pathlib.Path(sortedBAMFileStr).exists():
                        commandStr = Remove.storeDict.get("command","")
                        finalCommandStr = commandStr.format(target=bamFileStr)
                        Print.phraseStr = finalCommandStr
                        Print.runCommand()


            Print.stopLog()

class summariser: #haven't recheck
    def __init__(self):
        self.branchStr = ""
        self.testingBool = False
    
    def summaring(self):
        FLAGstat = libConfig.config()
        FLAGstat.queryStr = "binSAMtools-FLAGSTAT"
        FLAGstat.folderStr = "config/"
        FLAGstat.modeStr = "UPDATE"
        FLAGstat.load()

        expRep = libConfig.config()
        expRep.queryStr = self.branchStr
        expRep.folderStr = "config/"
        expRep.modeStr = "UPDATE"
        expRep.load()

        trimConditionList = expRep.storeDict.get("[trim]condition",[])
        hisat2ConditionList = expRep.storeDict.get("[hisat2]Condition",[])
        annotateConditionList = expRep.storeDict.get("conditionList",[])
        groupList = expRep.storeDict.get("group",[])
        replicationList = expRep.storeDict.get("replication",[])

        outputFolderStr = expRep.storeDict.get("[hisat2]outputFolder","")
        outputFileNameStr = expRep.storeDict.get("[hisat2]outputFileName","")

        if not expRep.storeDict.get("testing",True):
            self.testingBool = False
        else:
            self.testingBool = True

        for trimConditionStr in trimConditionList:
            for conditionList in annotateConditionList:
                annotateConditionStr = conditionList[0]
                finalOutputFolderStr = outputFolderStr.format(
                    annotateCondition=annotateConditionStr,
                    trimCondition=trimConditionStr
                )
                pathlib.Path(finalOutputFolderStr).mkdir(parents=True,exist_ok=True)

                for hisat2ConditionStr in hisat2ConditionList:
                    Print = libPrint.timer()
                    Print.logFilenameStr = "04-hs2-hisat2-{hisat2cond}-{annotateCon}-{trimCon}".format(
                        hisat2cond=hisat2ConditionStr,
                        annotateCon=annotateConditionStr,
                        trimCon=trimConditionStr,
                    )
                    Print.folderStr = "log/"
                    Print.testingBool = self.testingBool
                    Print.startLog()
                    
                    for groupStr in groupList:
                        for replicationStr in replicationList:
                            sortedBAMDict = {
                                "annotateCondition": annotateConditionStr,
                                "trimCondition": trimConditionStr,
                                "hisat2Condition": hisat2ConditionStr,
                                "group": groupStr,
                                "replication": replicationStr,
                                "fileType": "-sorted.bam",
                            }
                            sortedBAMFileStr = outputFileNameStr.format(**sortedBAMDict)
    
                            if pathlib.Path(sortedBAMFileStr).exists():
                                commandStr = FLAGstat.storeDict.get("command","")
                                finalCommandStr = commandStr.format(BAMfile=sortedBAMFileStr)
                                Print.phraseStr = finalCommandStr
                                Print.runCommand()


                    Print.stopLog()
