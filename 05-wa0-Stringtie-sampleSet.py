#!/usr/bin/env python3
import libConfig
# ---- Keyword list ----
"""
large/04-hisat2/testing/speciesTestingA-trimQ30/hisat2ForStringtie-T1r1-sorted.bam
data/05-wa-Stringtie/testing/speciesTestingA-trimQ30/T1r1.gtf
data/05-wa-Stringtie/testing/speciesTestingA-trimQ30-merged.gtf
data/05-wa-Stringtie/testing/speciesTestingA-trimQ30/T1r1-expression.tsv
data/05-wa-ballgown/testing/speciesTestingA-trimQ30-T1r1/
data/05-wa-ballgown/testing/speciesTestingA-trimQ30-T1r1/T1r1-expression.gtf
testing => testing
["Control","T1","T2","T3","T4","T5"] => ["Control","T1","T2","T3","T4","T5"]
["r1","r2","r3"] => ["r1","r2","r3"]
SpeA, speciesTestingA => SpeA, speciesTestingA
SpeB, speciesTestingB => SpeB, speciesTestingB
SpeC, speciesTestingC => SpeC, speciesTestingC
"""
# ---- Configuration of Experiment Design ---- 
expRep = libConfig.config()
expRep.queryStr = "testing"
expRep.folderStr = "config/"
expRep.queryDict = {
    "branch" : "testing",
    "group" : ["Control","T1","T2","T3","T4","T5"],
    "replication" : ["r1","r2","r3"],
    "pairPostfix" : "pair",
    "unpairPostfix" : "unpair",
    "[hisat2]Condition" : "hisat2ForStringtie",
    "conditionList" : [("speciesTestingB",'trimQ30'),("speciesTestingA",'trimQ30'),("speciesTestingC",'trimQ30')],
    "[waStringtie]inputFileName" : "large/04-hisat2/testing/{annotateCondition}-{trimCondition}/{hisat2Condition}-{group}{replication}-sorted.bam",
    # above: large/04-hisat2/testing/speciesTestingA-trimQ30/hisat2ForStringtie-T1r1-sorted.bam
    "[waStringtie]outputFolder" : "data/05-wa-Stringtie/testing/{annotateCondition}-{trimCondition}/",
    "[waStringtie]outputFileName" : "data/05-wa-Stringtie/testing/{annotateCondition}-{trimCondition}/{group}{replication}.gtf",
    # above: data/05-wa-Stringtie/testing/speciesTestingA-trimQ30/T1r1.gtf
    "[waStringtie]mergedFolder" : "data/05-wa-Stringtie/testing/",
    "[waStringtie]mergedFileName" : "data/05-wa-Stringtie/testing/{annotateCondition}-{trimCondition}-merged.gtf",
    # above: data/05-wa-Stringtie/testing/speciesTestingA-trimQ30-merged.gtf
    "[waStringtie]tsvFileName" : "data/05-wa-Stringtie/testing/{annotateCondition}-{trimCondition}/{group}{replication}-expression.tsv",
    # above: data/05-wa-Stringtie/testing/speciesTestingA-trimQ30/T1r1-expression.tsv
    "[waStringtie]ballgownFolder" : "data/05-wa-ballgown/testing/{annotateCondition}-{trimCondition}-{group}{replication}/",
    # above: data/05-wa-ballgown/testing/speciesTestingA-trimQ30-T1r1/
    "[waStringtie]gtfFileName" : "data/05-wa-ballgown/testing/{annotateCondition}-{trimCondition}-{group}{replication}/{group}{replication}-expression.gtf",
    # above: data/05-wa-ballgown/testing/speciesTestingA-trimQ30-T1r1/T1r1-expression.gtf
    "testing" : False,
}
expRep.modeStr = "UPDATE"
expRep.save()

# ---- Configuration of Mapping Conditions ---- 
SpeA = libConfig.config()
SpeA.queryStr = "speciesTestingA"
SpeA.folderStr = "config/"
SpeA.queryDict = {
    "seqPath" : "data/dbgs-GenomeSequence/speciesTestingA/speciesTestingA.fa",
    "antPath" : "data/dbga-GenomeAnnotation/speciesTestingA/speciesTestingA.gff3",
    "indexHeader" : "large/02-hisat2Index/speciesTestingA",
    "checkFolder"    : "large/02-hisat2Index/",
    "thread" : "6",
    "testing" : False,
}
SpeA.modeStr = "UPDATE"
SpeA.save()

SpeB = libConfig.config()
SpeB.queryStr = "speciesTestingB"
SpeB.folderStr = "config/"
SpeB.queryDict = {
    "seqPath" : "data/dbgs-GenomeSequence/speciesTestingB/speciesTestingB.fna",
    "antPath" : "data/dbga-GenomeAnnotation/speciesTestingB/speciesTestingB.gff3",
    "indexHeader" : "large/02-hisat2Index/speciesTestingB",
    "checkFolder"    : "large/02-hisat2Index/",
    "thread" : "6",
    "testing" : False,
}
SpeB.modeStr = "UPDATE"
SpeB.save()

SpeC = libConfig.config()
SpeC.queryStr = "speciesTestingC"
SpeC.folderStr = "config/"
SpeC.queryDict = {
    "seqPath" : "data/dbgs-GenomeSequence/speciesTestingC/speciesTestingC.fasta",
    "antPath" : "data/dbga-GenomeAnnotation/speciesTestingC/speciesTestingC.gff3",
    "indexHeader" : "large/02-hisat2Index/speciesTestingC",
    "checkFolder"    : "large/02-hisat2Index/",
    "thread" : "6",
    "testing" : False,
}
SpeC.modeStr = "UPDATE"
SpeC.save()

# ---- Configuration of Mapping Command ---- 
"""
Original command:
    stringtie [BAM file] -o [Result GTF file]\
        -p [Thread] -G [Reference GFF file] -e
"""

Stringtie = libConfig.config()
Stringtie.queryStr = "binStringTie-RUN"
Stringtie.folderStr = "config/"
Stringtie.queryDict = {
    "command" : 
        "bin/stringtie/stringtie {bamfile} -v -o {outputfile} "+
        "-p {thread} -G {antPath}"
}
Stringtie.modeStr = "UPDATE"
Stringtie.save()

Stringtie = libConfig.config()
Stringtie.queryStr = "binStringTie-RUN-withoutAnnotation"
Stringtie.folderStr = "config/"
Stringtie.queryDict = {
    "command" : 
        "bin/stringtie/stringtie {bamfile} -v -o {outputfile} "+
        "-p {thread}"
}
Stringtie.modeStr = "UPDATE"
Stringtie.save()

StMerge = libConfig.config()
StMerge.queryStr = "binStringTie-MERGE"
StMerge.folderStr = "config/"
StMerge.queryDict = {
    "command" : 
        "bin/stringtie/stringtie {inputfiles} --merge -v -o {outputfile} "+
        "-p {thread}"
}
StMerge.modeStr = "UPDATE"
StMerge.save()

StEstimate = libConfig.config()
StEstimate.queryStr = "binStringTie-ESTIMATE"
StEstimate.folderStr = "config/"
StEstimate.queryDict = {
    "command" : 
        "bin/stringtie/stringtie {bamfile} -v "+
        "-b {ballgownPath} " +
        "-p {thread} -G {mergePath} " +
        "-o {gtffile} "        
        "-e -A {tsvfile}"        
}
StEstimate.modeStr = "UPDATE"
StEstimate.save()
