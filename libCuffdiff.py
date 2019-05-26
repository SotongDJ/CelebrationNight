#!/usr/bin/env python3
import libConfig, libPrint
import pathlib
"""
    --- README of CuffDiff related actions ---
Original command:
    cuffdiff \
        -p <int> \
        -o <string> \
        -L <label1,label2,…,labelN> \
        <transcripts.gtf> \
        [sampleN_replicate1.sam[,…,sample2_replicateM.sam]]

    --- README ---
"""
class assembler:
    def __init__(self):
        self.branchStr = ""
        self.testingBool = True

    def assembling(self):
        # ---- Parameter for Assembling ----
        BinMap = libConfig.config()
        BinMap.queryStr = "binCuffDiff-RUN"
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
        threadStr = Target.storeDict.get("thread","1")
        hisat2ConditionStr = Target.storeDict.get("[hisat2]Condition","")
        conditionList = Target.storeDict.get("conditionList",[])
        methodList = Target.storeDict.get("methodList",[])
        sourceDict = Target.storeDict.get("[CuffDiff]sourceDict",dict())
        bamFileNameStr = Target.storeDict.get("[CuffDiff]bamFileName","")
        gtfFileNameStr = Target.storeDict.get("[CuffDiff]gtfFileName","")
        resultFolderStr = Target.storeDict.get("[CuffDiff]resultFolder","")
        
        if not Target.storeDict.get("testing",True):
            self.testingBool = False
        else:
            self.testingBool = True

        for methodStr in methodList:
            sourceFolderStr = sourceDict.get(methodStr,"")
            for conditionTup in conditionList:
                antCondStr = conditionTup[0]
                trimCondStr = conditionTup[1]

                # ---- Action ----
                Print = libPrint.timer()
                Print.logFilenameStr = "06-CuffDiff-{branch}-from({method})-{annotate}-{trim}".format(
                    branch=branchStr,
                    method=methodStr,
                    annotate=antCondStr,
                    trim=trimCondStr,
                )
                Print.folderStr = "log/"
                Print.testingBool = self.testingBool
                Print.startLog()
                
                resultPathStr = resultFolderStr.format(
                    branch=branchStr,
                    method=methodStr,
                    annotateCondition=antCondStr,
                    trimCondition=trimCondStr,
                )
                pathlib.Path(resultPathStr).mkdir(parents=True,exist_ok=True)
                
                gtfFileStr = gtfFileNameStr.format(
                    sourceFolder=sourceFolderStr,
                    batch=branchStr,
                    annotateCondition=antCondStr,
                    trimCondition=trimCondStr,
                )

                bamGroupList = list()
                for groupStr in groupList:
                    bamFileList = list()
                    for repliStr in replicationList:

                        bamFileStr = bamFileNameStr.format(
                            batch=branchStr,
                            annotateCondition=antCondStr,
                            trimCondition=trimCondStr,
                            hisat2Condition=hisat2ConditionStr,
                            group=groupStr,
                            replication=repliStr,
                        )
                        bamFileList.append(bamFileStr)

                    bamGroupList.append(",".join(bamFileList))
                bamSampleStr = " ".join(bamGroupList)

                CommandStr = commandStr.format(
                    thread=threadStr,
                    outputFolder=resultPathStr,
                    labelList=",".join(groupList),
                    mergedGTF=gtfFileStr,
                    bamFiles=bamSampleStr,
                )
                
                Print.phraseStr = CommandStr
                Print.runCommand()

                Print.stopLog()
