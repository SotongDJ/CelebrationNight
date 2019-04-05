#!/usr/bin/env python3
import libConfig, libPrint, libHISAT
import pathlib
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

    Index = libHISAT.indexer()
    Index.commandStr = BinIndex.storeDict["command"]

    Index.titleStr = indexStr
    Index.folderStr = Target.storeDict.get("checkFolder","")
    Index.seqPathStr = Target.storeDict.get("seqPath","")
    Index.indexHeaderStr = Target.storeDict.get("indexHeader","")
    Index.threadStr = Target.storeDict.get("thread","")

    if Target.storeDict.get("testing",False):
        Index.testingBool = True

    Index.indexing()
