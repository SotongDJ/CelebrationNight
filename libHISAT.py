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

        self.testingBool = True

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
