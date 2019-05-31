#!/usr/bin/env python3
import libConfig
# ---- Keyword list ----
"""
large/04-hisat2/testing/speciesTestingA-trimQ30/hisat2ForStringtie-T1r1.sam
large/03-trimed/testing/trimQ30-T1r1-F-pair.fastq
testing
["Control","T1","T2","T3","T4","T5"]
"F"
"R"
["r1"]
SpeA, speciesTestingA
SpeB, speciesTestingB
SpeC, speciesTestingC
"""
# ---- Configuration of Experiment Design ---- 
expRep = libConfig.config()
expRep.queryStr = "testing"
expRep.folderStr = "config/"
# Arguments/Parameters below need to modify depend on 
# your experiment design and naming style
expRep.queryDict = {
    "branch" : "testing",
    "group" : ["Control","T1","T2","T3","T4","T5"],
    "replication" : ["r1"],
    "pairPostfix" : "pair",
    "unpairPostfix" : "unpair",
    "[trim]fileType" : ".fastq",
    "[hisat2]direction" : {
        '1' : "F",
        '2' : "R",
    },
    "[hisat2]inputFileName" : "large/03-trimed/testing/{trimCondition}-{group}{replication}-{direction}-{pairType}{fileType}",
    # above: large/03-trimed/testing/trimQ30-T1r1-F-pair.fastq
    # "[hisat2]Condition" : ["hisat2ForStringtie","hisat2ForCufflinks"],
    "[hisat2]Condition" : ["hisat2ForStringtie"],
    "conditionList" : [("speciesTestingA","trimQ30"),("speciesTestingB","trimQ30"),("speciesTestingC","trimQ30")],
    "[hisat2]outputFolder" : "large/04-hisat2/tripleRep/{annotateCondition}-{trimCondition}/",
    "[hisat2]outputFileName" : "large/04-hisat2/tripleRep/{annotateCondition}-{trimCondition}/{hisat2Condition}-{group}{replication}{fileType}",
    # above: large/04-hisat2/testing/speciesTestingA-trimQ30/hisat2ForStringtie-T1r1.sam
    "testing" : False,
}
expRep.modeStr = "UPDATE"
expRep.save()

# ---- Configuration of Alignment Conditions ---- 
stringtiePara = libConfig.config()
stringtiePara.queryStr = "hisat2ForStringtie"
stringtiePara.folderStr = "config/"
stringtiePara.queryDict = {
    "dta"     : "--dta", 
    "phred"   : "33", # sequencing type, illumina solexa = 33
    "thread"  : "6", # cluster server have 8 cores
}
stringtiePara.modeStr = "OVERWRITE"
stringtiePara.save()

cufflinksPara = libConfig.config()
cufflinksPara.queryStr = "hisat2ForCufflinks"
cufflinksPara.folderStr = "config/"
cufflinksPara.queryDict = {
    "dta"     : "--dta-cufflinks", 
    "phred"   : "33", # sequencing type, illumina solexa = 33
    "thread"  : "6", # cluster server have 8 cores
}
cufflinksPara.modeStr = "OVERWRITE"
cufflinksPara.save()

# ---- Configuration of Alignment Command ---- 
"""
  Original command:
    hisat2 -q [--dta/--dta-cufflinks] --phred[33] -p [4]
        -x [prefix of HISAT2-build genome index]
        -1 [forward fastq files]
        -2 [reverse fastq files]
        -U [unpair fastq files]
        -S [output SAM files]
    samtools view -o [out.bam] -Su [in.sam]
    samtools sort -o [out-sorted.bam] [in.bam]
"""

HISAT2 = libConfig.config()
HISAT2.queryStr = "binHISAT2-RUN"
HISAT2.folderStr = "config/"
HISAT2.queryDict = {
    "command-PE" : 
        "bin/hisat2/hisat2 -q {dta} --phred{phred} -p {thread} " +
        "-x {indexHeader} " +
        "-1 {pairForwardFASTQ} " +
        "-2 {pairReverseFASTQ} " +
        "-U {unpairForwardFASTQ},{unpairReverseFASTQ} " +
        "-S {outputSAM}",
    "command-SE" : 
        "bin/hisat2/hisat2 -q {dta} --phred{phred} -p {thread} " +
        "-x {indexHeader} " +
        "-U {unpairFASTQ} " +
        "-S {outputSAM}",
}
HISAT2.modeStr = "OVERWRITE"
HISAT2.save()

SAMconvert = libConfig.config()
SAMconvert.queryStr = "binSAMtools-CONVERT"
SAMconvert.folderStr = "config/"
SAMconvert.queryDict = {
    "command" : 
        "bin/samtools/samtools view -o {outputBAM} -Su {inputSAM}"
}
SAMconvert.modeStr = "OVERWRITE"
SAMconvert.save()

SAMsort = libConfig.config()
SAMsort.queryStr = "binSAMtools-SORT"
SAMsort.folderStr = "config/"
SAMsort.queryDict = {
    "command" : 
        "bin/samtools/samtools sort -o {outputBAM} {inputBAM}"
}
SAMsort.modeStr = "OVERWRITE"
SAMsort.save()

FLAGstat = libConfig.config()
FLAGstat.queryStr = "binSAMtools-FLAGSTAT"
FLAGstat.folderStr = "config/"
FLAGstat.queryDict = {
    "command" : 
        "bin/samtools/samtools flagstat {BAMfile}"
}
FLAGstat.modeStr = "OVERWRITE"
FLAGstat.save()

Remove = libConfig.config()
Remove.queryStr = "commandRM"
Remove.folderStr = "config/"
Remove.queryDict = {
    "command" : 
        "rm -vf {target}"
}
Remove.modeStr = "OVERWRITE"
Remove.save()
