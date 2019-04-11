#!/usr/bin/env python3
import libConfig
# ---- Configuration of Experiment Design ---- 
expRep = libConfig.config()
expRep.queryStr = "testing"
expRep.folderStr = "data/config/"
# Arguments/Parameters below need to modify depend on 
# your experiment design and naming style
expRep.queryDict = {
    "branch" : "testing",
    "group" : ["Control","T1","T2","T3","T4","T5"],
    "replication" : ["r1"],
    "pairPostfix" : "pair",
    "unpairPostfix" : "unpair",
    "[trim]fileType" : ".fastq",
    "[trim]condition" : ["trimQ20","trimQ30"],
    "[hisat2]direction" : {
        '1' : "F",
        '2' : "R",
    },
    "[hisat2]inputFileName" : "data/03-trimed/testing/{trimCondition}-{group}-{replication}-{direction}-{pairType}{fileType}",
    # above: data/tmp/trimQ20-T1-r1-F-pair.fastq
    "[hisat2]hisat2Condition" : ["hisat2ForStringtie","hisat2ForCufflinks"],
    "[hisat2]annotateCondition" : ["speciesTestingA","speciesTestingB","speciesTestingC"],
    "[hisat2]outputFolder" : "data/04-hisat2/testing/{annotateCondition}-{trimCondition}/",
    "[hisat2]outputFileName" : "data/04-hisat2/testing/{annotateCondition}-{trimCondition}/{hisat2Condition}-{group}-{replication}{fileType}",
    # above: date/04-hisat2/testing/speciesTestingA-trimQ20/hisat2ForStringtie-T1-r1.sam
    "testing" : True,
}
expRep.modeStr = "UPDATE"
expRep.save()

# ---- Configuration of Trimming Conditions ---- 
stringtiePara = libConfig.config()
stringtiePara.queryStr = "hisat2ForStringtie"
stringtiePara.folderStr = "data/config/"
stringtiePara.queryDict = {
    "dta"     : "--dta", 
    "phred"   : "33", # sequencing type, illumina solexa = 33
    "thread"  : "6", # cluster server have 8 cores
}
stringtiePara.modeStr = "OVERWRITE"
stringtiePara.save()

cufflinksPara = libConfig.config()
cufflinksPara.queryStr = "hisat2ForCufflinks"
cufflinksPara.folderStr = "data/config/"
cufflinksPara.queryDict = {
    "dta"     : "--dta-cufflinks", 
    "phred"   : "33", # sequencing type, illumina solexa = 33
    "thread"  : "6", # cluster server have 8 cores
}
cufflinksPara.modeStr = "OVERWRITE"
cufflinksPara.save()

# ---- Configuration of Trimming Command ---- 
"""
  Original command:
    hisat2 -q [--dta/--dta-cufflinks] --phred[33] -p [4]
        -x [prefix of HISAT2-build genome index]
        -1 [forward fastq files]
        -2 [reverse fastq files]
        -S [output SAM files]
    samtools view -o [out.bam] -Su [in.sam]
    samtools sort -o [out-sorted.bam] [in.bam]
"""

HISAT2 = libConfig.config()
HISAT2.queryStr = "binHISAT2-RUN"
HISAT2.folderStr = "data/config/"
HISAT2.queryDict = {
    "command" : 
        "bin/hisat2/hisat2 -q {dta} --phred{phred} -p {thread} " +
        "-x {indexHeader} " +
        "-1 {forwardFASTQ} " +
        "-2 {reverseFASTQ} " +
        "-S {outputSAM}"
}
HISAT2.modeStr = "OVERWRITE"
HISAT2.save()

SAMconvert = libConfig.config()
SAMconvert.queryStr = "binSAMtools-CONVERT"
SAMconvert.folderStr = "data/config/"
SAMconvert.queryDict = {
    "command" : 
        "bin/samtools/samtools view -o {outputBAM} -Su {inputSAM}"
}
SAMconvert.modeStr = "OVERWRITE"
SAMconvert.save()

SAMsort = libConfig.config()
SAMsort.queryStr = "binSAMtools-SORT"
SAMsort.folderStr = "data/config/"
SAMsort.queryDict = {
    "command" : 
        "bin/samtools/samtools sort -o {outputBAM} {inputBAM}"
}
SAMsort.modeStr = "OVERWRITE"
SAMsort.save()

Remove = libConfig.config()
Remove.queryStr = "commandRM"
Remove.folderStr = "data/config/"
Remove.queryDict = {
    "command" : 
        "rm -vf {target}"
}
Remove.modeStr = "OVERWRITE"
Remove.save()
