#!/usr/bin/env python3
import libConfig
# ---- Keyword list ----
"""
large/04-hisat2/testing/speciesTestingA-trimQ30/hisat2ForStringtie-T1r1-sorted.bam
data/05-st-Stringtie/testing/speciesTestingA-trimQ30-merged.gtf
data/06-cd-CuffDiff/testing-Stringtie/speciesTestingA-trimQ30/
testing
["Control","T1","T2","T3","T4","T5"]
["r1","r2","r3"]
speciesTestingA
speciesTestingB
speciesTestingC
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
    "replication" : ["r1","r2","r3"],
    "pairPostfix" : "pair",
    "unpairPostfix" : "unpair",
    "thread" : "6",
    "[hisat2]Condition" : "hisat2ForStringtie",
    "conditionList" : [("speciesTestingB",'trimQ30'),("speciesTestingA",'trimQ30'),("speciesTestingC",'trimQ30')],
    "methodList" : ["Stringtie","dsStringtie","waStringtie"],
    "[CuffDiff]sourceDict" : {
        "Stringtie" : "05-st-Stringtie",
        "dsStringtie" : "05-ds-Stringtie",
        "waStringtie" : "05-wa-Stringtie"
    },
    "[CuffDiff]bamFileName" : "large/04-hisat2/{branch}/{annotateCondition}-{trimCondition}/{hisat2Condition}-{group}{replication}-sorted.bam",
    # above: large/04-hisat2/testing/speciesTestingA-trimQ30/hisat2ForStringtie-T1r1-sorted.bam
    "[CuffDiff]gtfFileName" : "data/{sourceFolder}/{branch}/{annotateCondition}-{trimCondition}-merged.gtf",
    # above: data/05-st-Stringtie/testing/speciesTestingA-trimQ30-merged.gtf
    "[CuffDiff]resultFolder" : "data/06-cd-CuffDiff/{branch}-{method}/{annotateCondition}-{trimCondition}/",
    # above: data/06-cd-CuffDiff/testing-Stringtie/speciesTestingA-trimQ30/
    "testing" : False,
}
expRep.modeStr = "UPDATE"
expRep.save()
# ---- Configuration of cuffdiff Command ---- 
"""
Original command:
    cuffdiff \
        -p <int> \
        -o <string> \
        -L <label1,label2,…,labelN> \
        <transcripts.gtf> \
        [sampleN_replicate1.sam[,…,sample2_replicateM.sam]]

"""

CuffDiff = libConfig.config()
CuffDiff.queryStr = "binCuffDiff-RUN"
CuffDiff.folderStr = "config/"
CuffDiff.queryDict = {
    "command" : 
        "bin/cufflinks/cuffdiff "+
        "-p {thread} "+
        "-o {outputFolder} "+
        "-L {labelList} "+
        "{mergedGTF} {bamFiles}"
}
CuffDiff.modeStr = "UPDATE"
CuffDiff.save()
