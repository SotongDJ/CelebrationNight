#!/usr/bin/env python3
import libConfig
# ---- Keyword list ----
"""
large/04-hisat2/testing/speciesAnnotationA-trimQ30/hisat2ForStringtie-T1r1-sorted.bam
data/05-st-Stringtie/testing/speciesAnnotationA-trimQ30/T1r1.gtf
data/05-st-Stringtie/testing/speciesAnnotationA-trimQ30-merged.gtf
data/05-st-Stringtie/testing/speciesAnnotationA-trimQ30/T1r1-expression.tsv
data/05-st-ballgown/testing/speciesAnnotationA-trimQ30-T1r1/
data/05-st-ballgown/testing/speciesAnnotationA-trimQ30-T1r1/T1r1-expression.gtf
testing =>
["Control","T1","T2","T3","T4","T5"]
["r1","r2","r3"]
SpeA, speciesAnnotationA
SpeB, speciesAnnotationB
SpeC, speciesAnnotationC
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
    "[hisat2]Condition" : "hisat2ForStringtie",
    "conditionList" : [("speciesAnnotationB",'trimQ30'),("speciesAnnotationA",'trimQ30'),("speciesAnnotationC",'trimQ30')],
    "[Stringtie]inputFileName" : "large/04-hisat2/testing/{annotateCondition}-{trimCondition}/{hisat2Condition}-{group}{replication}-sorted.bam",
    # above: large/04-hisat2/testing/speciesAnnotationA-trimQ30/hisat2ForStringtie-T1r1-sorted.bam
    "[Stringtie]outputFolder" : "data/05-st-Stringtie/testing/{annotateCondition}-{trimCondition}/",
    "[Stringtie]outputFileName" : "data/05-st-Stringtie/testing/{annotateCondition}-{trimCondition}/{group}{replication}.gtf",
    # above: data/05-st-Stringtie/testing/speciesAnnotationA-trimQ30/T1r1.gtf
    "[Stringtie]mergedFolder" : "data/05-st-Stringtie/testing/",
    "[Stringtie]mergedFileName" : "data/05-st-Stringtie/testing/{annotateCondition}-{trimCondition}-merged.gtf",
    # above: data/05-st-Stringtie/testing/speciesAnnotationA-trimQ30-merged.gtf
    "[Stringtie]tsvFileName" : "data/05-st-Stringtie/testing/{annotateCondition}-{trimCondition}/{group}{replication}-expression.tsv",
    # above: data/05-st-Stringtie/testing/speciesAnnotationA-trimQ30/T1r1-expression.tsv
    "[Stringtie]ballgownFolder" : "data/05-st-ballgown/testing/{annotateCondition}-{trimCondition}-{group}{replication}/",
    # above: data/05-st-ballgown/testing/speciesAnnotationA-trimQ30-T1r1/
    "[Stringtie]gtfFileName" : "data/05-st-ballgown/testing/{annotateCondition}-{trimCondition}-{group}{replication}/{group}{replication}-expression.gtf",
    # above: data/05-st-ballgown/testing/speciesAnnotationA-trimQ30-T1r1/T1r1-expression.gtf
    "testing" : False,
}
expRep.modeStr = "UPDATE"
expRep.save()

# ---- Configuration of Mapping Conditions ---- 
SpeA = libConfig.config()
SpeA.queryStr = "speciesAnnotationA"
SpeA.folderStr = "config/"
SpeA.queryDict = {
    "seqPath" : "data/dbgs-GenomeSequence/speciesAnnotationA/speciesAnnotationA.fa",
    "antPath" : "data/dbga-GenomeAnnotation/speciesAnnotationA/speciesAnnotationA.gff3",
    "indexHeader" : "large/02-hisat2Index/speciesAnnotationA",
    "checkFolder"    : "large/02-hisat2Index/",
    "thread" : "6",
    "testing" : False,
}
SpeA.modeStr = "UPDATE"
SpeA.save()

SpeB = libConfig.config()
SpeB.queryStr = "speciesAnnotationB"
SpeB.folderStr = "config/"
SpeB.queryDict = {
    "seqPath" : "data/dbgs-GenomeSequence/speciesAnnotationB/speciesAnnotationB.fna",
    "antPath" : "data/dbga-GenomeAnnotation/speciesAnnotationB/speciesAnnotationB.gff3",
    "indexHeader" : "large/02-hisat2Index/speciesAnnotationB",
    "checkFolder"    : "large/02-hisat2Index/",
    "thread" : "6",
    "testing" : False,
}
SpeB.modeStr = "UPDATE"
SpeB.save()

SpeC = libConfig.config()
SpeC.queryStr = "speciesAnnotationC"
SpeC.folderStr = "config/"
SpeC.queryDict = {
    "seqPath" : "data/dbgs-GenomeSequence/speciesAnnotationC/speciesAnnotationC.fasta",
    "antPath" : "data/dbga-GenomeAnnotation/speciesAnnotationC/speciesAnnotationC.gff3",
    "indexHeader" : "large/02-hisat2Index/speciesAnnotationC",
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
