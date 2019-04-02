#!/usr/bin/env python3
import libConfig, libPrint, libTrim
import pathlib
"""
   --- README of 03-trim ---
 Title:
    Batch Processing for Trimmomatic

 Original command:
  java -jar <bin>/trimmomatic-0.35.jar PE \\
    -phred33 -threads <threads> \\
    input_forward.fq.gz input_reverse.fq.gz \\
    output_forward_paired.fq.gz output_forward_unpaired.fq.gz \\
    output_reverse_paired.fq.gz output_reverse_unpaired.fq.gz \\
    <ILLUMINACLIP> <LEADING> \\
    <TRAILING> <SLIDINGWINDOW> <MINLEN>

   --- README ---
"""
# ---- Parameter ----
BinTrim = libConfig.config()
BinTrim.queryStr = "binTrimmomatic"
BinTrim.folderStr = "data/config/"
BinTrim.modeStr = "UPDATE"
BinTrim.load()

ExpRep = libConfig.config()
ExpRep.queryStr = "testing"    # ATTENTION: change query name
ExpRep.folderStr = "data/config/"
ExpRep.modeStr = "UPDATE"
ExpRep.load()

# ---- Initialization ----
Trim = libTrim.trimmer()
Trim.commandStr = BinTrim.storeDict["command"]

Trim.conditionList = ExpRep.storeDict.get("[trim]condition",[])
Trim.groupList = ExpRep.storeDict.get("group",[])
Trim.directionList = ExpRep.storeDict.get("direction",[])

Trim.branchStr = ExpRep.storeDict.get("branch","")
Trim.pairStr = ExpRep.storeDict.get("pairPostfix","")
Trim.unpairStr = ExpRep.storeDict.get("unpairPostfix","")

Trim.inputFileNameStr = ExpRep.storeDict.get("[trim]inputFileName","")
Trim.outputFileNameStr = ExpRep.storeDict.get("[trim]outputFileName","")
Trim.fileTypeStr = ExpRep.storeDict.get("[trim]fileType","")
Trim.checkFolderList = ExpRep.storeDict.get("[trim]checkFolder",[])

Trim.trimming()
