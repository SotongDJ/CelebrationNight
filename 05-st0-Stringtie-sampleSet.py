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
    "[stringtie2]trimCondition" : ["trimQ20"],
    "[stringtie2]hisat2Condition" : "hisat2ForStringtie",
    "[stringtie2]annotateCondition" : ["speciesTestingA","speciesTestingB","speciesTestingC"],
    "[stringtie2]inputFileName" : "data/04-hisat2/testing/{annotateCondition}-{trimCondition}/{hisat2Condition}-{group}{replication}-sorted.bam",
    # above: data/04-hisat2/testing/speciesTestingA-trimQ20/hisat2ForStringtie-T1r1-sorted.bam
    "[stringtie2]outputFileName" : "data/05-stringtie2/testing/{annotateCondition}-{trimCondition}/{group}{replication}.gtf",
    # above: data/05-stringtie2/testing/speciesTestingA-trimQ20/T1r1.gtf
    "[stringtie2]outputFolder" : "data/05-stringtie2/testing/{annotateCondition}-{trimCondition}/",
    "[stringtie2]mergedFileName" : "data/05-stringtie2/testing/{annotateCondition}-{trimCondition}-merged.gtf",
    # above: data/05-stringtie2/testing/speciesTestingA-trimQ20-merged.gtf
    "[stringtie2]mergedFolder" : "data/05-stringtie2/singRep/",
    "testing" : False,
}
expRep.modeStr = "UPDATE"
expRep.save()

# ---- Configuration of Mapping Conditions ---- 
SpeA = libConfig.config()
SpeA.queryStr = "speciesTestingA"
SpeA.folderStr = "data/config/"
SpeA.queryDict = {
    "from" : "binHISAT2-BUILD",
    "seqPath" : "data/GenomeSequence/SpeA.fa",
    "antPath" : "data/GenomeSequence/SpeA.gff3",
    "indexHeader" : "data/02-hisat2Index/SpeA",
    "checkFolder"    : "data/02-hisat2Index/",
    "thread" : "6",
    "testing" : True,
}
SpeA.modeStr = "OVERWRITE"
SpeA.save()

SpeB = libConfig.config()
SpeB.queryStr = "speciesTestingB"
SpeB.folderStr = "data/config/"
SpeB.queryDict = {
    "from" : "binHISAT2-BUILD",
    "seqPath" : "data/GenomeSequence/SpeB.fna",
    "antPath" : "data/GenomeSequence/SpeB.gff3",
    "indexHeader" : "data/02-hisat2Index/SpeB",
    "checkFolder"    : "data/02-hisat2Index/",
    "thread" : "6",
    "testing" : True,
}
SpeB.modeStr = "OVERWRITE"
SpeB.save()

SpeC = libConfig.config()
SpeC.queryStr = "speciesTestingC"
SpeC.folderStr = "data/config/"
SpeC.queryDict = {
    "from" : "binHISAT2-BUILD",
    "seqPath" : "data/GenomeSequence/SpeC.fasta",
    "antPath" : "data/GenomeSequence/SpeC.gff3",
    "indexHeader" : "data/02-hisat2Index/SpeC",
    "checkFolder"    : "data/02-hisat2Index/",
    "thread" : "6",
    "testing" : True,
}
SpeC.modeStr = "OVERWRITE"
SpeC.save()

# ---- Configuration of Mapping Command ---- 
"""
Original command:
    stringtie [BAM file] -o [Result GTF file]\
        -p [Thread] -G [Reference GFF file] -e
"""

Stringtie = libConfig.config()
Stringtie.queryStr = "binStringTie-RUN"
Stringtie.folderStr = "data/config/"
Stringtie.queryDict = {
    "command" : 
        "bin/stringtie/stringtie {bamfile} -o {outputfile} "+
        "-p {thread} -G {antPath} -e"
}
Stringtie.modeStr = "UPDATE"
Stringtie.save()

StMerge = libConfig.config()
StMerge.queryStr = "binStringTie-MERGE"
StMerge.folderStr = "data/config/"
StMerge.queryDict = {
    "command" : 
        "bin/stringtie/stringtie {inputfiles} --merge -o {outputfile} "+
        "-p {thread} -G {antPath}"
}
StMerge.modeStr = "UPDATE"
StMerge.save()
