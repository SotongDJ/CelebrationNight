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
class converter:
    def __init__(self):
        self.branchStr = ""
        self.testingBool = True

    def converting(self):
        # ---- Parameter ----
        BinGFF = libConfig.config()
        BinGFF.queryStr = "binCufflinks-gffread"
        BinGFF.folderStr = "config/"
        BinGFF.modeStr = "UPDATE"
        BinGFF.load()

        Copying = libConfig.config()
        Copying.queryStr = "commandCP"
        Copying.folderStr = "config/"
        Copying.modeStr = "UPDATE"
        Copying.load()

        # ---- Initialization for Assembling ----
        Target = libConfig.config()
        Target.queryStr = self.branchStr
        Target.folderStr = "config/"
        Target.modeStr = "UPDATE"
        Target.load()

        if not Target.storeDict.get("testing",True):
            self.testingBool = False
        else:
            self.testingBool = True

        gffreadStr = BinGFF.storeDict["command"]
        copyStr = Copying.storeDict["command"]

        branchStr = self.branchStr
        conditionsList = [ n for n in Target.storeDict["conditionsList"] if n["transcriptome"] == "gffRead" ]
        gtfDict = Target.storeDict["gtfDict"]

        for conditionDict in conditionsList:
            genomeStr = conditionDict["genome"]
            trimStr = conditionDict["trim"]
            transcriptomeStr = conditionDict["transcriptome"]

            folderStr = gtfDict[transcriptomeStr]['folder']
            infoDict = {
                "branch" : self.branchStr,
                "annotate" : genomeStr,
                "trim" : trimStr,
                "folder" : folderStr,
            }
            targetFolderStr = Target.storeDict["transcriptomeFolder"]
            targetStr = Target.storeDict["transcriptomeGTF"]

            Spec = libConfig.config() #parameters
            Spec.queryStr = genomeStr
            Spec.folderStr = "config/"
            Spec.modeStr = "UPDATE"
            Spec.load()

            inputStr = Spec.storeDict["antPath"]
            outputStr = Spec.storeDict["gtfPath"]
            outputFolderStr = Spec.storeDict["dbgaPath"]

            Print = libPrint.timer()
            Print.logFilenameStr = "05-gffConversion-{branch}-{annotate}".format(
                branch=branchStr,
                annotate=genomeStr,
            )
            Print.folderStr = outputFolderStr
            Print.testingBool = self.testingBool
            Print.startLog()
            
            targetPath = targetStr.format(**infoDict)

            if not pathlib.Path(outputStr).exists():
                CommandStr = gffreadStr.format(inputFile=inputStr,outputFile=outputStr)
                Print.phraseStr = CommandStr
                Print.runCommand()

            folderPath = targetFolderStr.format(**infoDict)
            pathlib.Path(folderPath).mkdir(parents=True,exist_ok=True)
            
            CommandStr = copyStr.format(output=outputStr,target=targetPath)
            Print.phraseStr = CommandStr
            Print.runCommand()

            Print.stopLog()

class differ:
    def __init__(self):
        self.branchStr = ""
        self.testingBool = True

    def diffing(self):
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

        groupList = Target.storeDict["group"]
        replicationList = Target.storeDict["replication"]
        threadStr = Target.storeDict["thread"]
        bamFileNameStr = Target.storeDict["[hisat2]outputFileName"]
        gtfFileNameStr = Target.storeDict["transcriptomeGTF"]
        gtfDict = Target.storeDict["gtfDict"]
        resultFolderStr = Target.storeDict["[CuffDiff]resultFolder"]

        conditionsList = Target.storeDict["conditionsList"]
        for conditionDict in conditionsList:
            genomeStr = conditionDict["genome"]
            trimStr = conditionDict["trim"]
            transcriptomeStr = conditionDict["transcriptome"]
            folderStr = gtfDict[transcriptomeStr]['folder']
            hisat2ConditionStr = conditionDict["map"]

            if not Target.storeDict.get("testing",True):
                self.testingBool = False
            else:
                self.testingBool = True

            infoDict = {
                "branch" : self.branchStr,
                "method" : transcriptomeStr,
                "annotate" : genomeStr,
                "trim" : trimStr,
                "folder" : folderStr,
                "hisat2Condition" : hisat2ConditionStr,
                "fileType" : "-sorted.bam",
            }

            # ---- Action ----
            Print = libPrint.timer()
            Print.logFilenameStr = "07-CuffDiff-{branch}-from({method})-{annotate}-{trim}".format(**infoDict)
            Print.folderStr = "log/"
            Print.testingBool = self.testingBool
            Print.startLog()
            
            resultPathStr = resultFolderStr.format(**infoDict)
            pathlib.Path(resultPathStr).mkdir(parents=True,exist_ok=True)
            
            gtfFileStr = gtfFileNameStr.format(**infoDict)

            bamGroupList = list()
            for groupStr in groupList:
                bamFileList = list()
                for repliStr in replicationList:
                    bamFileDict = dict()
                    bamFileDict.update(infoDict)
                    bamFileDict.update({
                        "group" : groupStr,
                        "replication" : repliStr,
                    })

                    bamFileStr = bamFileNameStr.format(**bamFileDict)
                    bamFileList.append(bamFileStr)

                bamGroupList.append(",".join(bamFileList))
            bamSampleStr = " ".join(bamGroupList)

            infoDict.update({
                "thread" : threadStr,
                "outputFolder" : resultPathStr,
                "labelList" : ",".join(groupList),
                "mergedGTF" : gtfFileStr,
                "bamFiles" : bamSampleStr,
            })
            CommandStr = commandStr.format(**infoDict)
            
            Print.phraseStr = CommandStr
            Print.runCommand()

            Print.stopLog()
