#!/usr/bin/env python3
import libConfig
# ---- Keyword list ----
"""
large/04-hisat2/testing/speciesAnnotationA-trimQ30/hisat2ForStringtie-T1r1-sorted.bam
data/05-st-Stringtie/testing/speciesAnnotationA-trimQ30-merged.gtf
data/06-cd-CuffDiff/testing-Stringtie/speciesAnnotationA-trimQ30/
testing
["Control","T1","T2","T3","T4","T5"]
["r1","r2","r3"]
speciesAnnotationA
speciesAnnotationB
speciesAnnotationC
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
    "conditionList" : [("speciesAnnotationB",'trimQ30'),("speciesAnnotationA",'trimQ30'),("speciesAnnotationC",'trimQ30')],
    "methodList" : ["Stringtie","dsStringtie","waStringtie"],
    "[CuffDiff]sourceDict" : {
        "Stringtie" : "05-st-Stringtie",
        "dsStringtie" : "05-ds-Stringtie",
        "waStringtie" : "05-wa-Stringtie"
    },
    "[CuffDiff]bamFileName" : "large/04-hisat2/{branch}/{annotateCondition}-{trimCondition}/{hisat2Condition}-{group}{replication}-sorted.bam",
    # above: large/04-hisat2/testing/speciesAnnotationA-trimQ30/hisat2ForStringtie-T1r1-sorted.bam
    "[CuffDiff]gtfFileName" : "data/{sourceFolder}/{branch}/{annotateCondition}-{trimCondition}-merged.gtf",
    # above: data/05-st-Stringtie/testing/speciesAnnotationA-trimQ30-merged.gtf
    # NOTE:
    #     If you want to use cuffdiff to estimate without transcriptome assembly, use gffread convert gff3 file (genome annotation) to gtf file (transcriptome annotation)
    #     After that, copy the gtf file to the path above and rename as mimic of merged transcriptome annotation
    #
    "[CuffDiff]resultFolder" : "data/06-cd-CuffDiff/{branch}-{method}/{annotateCondition}-{trimCondition}/",
    # above: data/06-cd-CuffDiff/testing-Stringtie/speciesAnnotationA-trimQ30/

    "gtfFolder" : "data/05-ds-Stringtie/{branch}/",
    "gtfFile" : "data/05-ds-Stringtie/{branch}/{annotation}-{trimCondition}-merged.gtf",
    "testing" : False,
}
expRep.modeStr = "UPDATE"
expRep.save()

# ---- Configuration of Mapping Conditions ---- 
SpeA = libConfig.config()
SpeA.queryStr = "speciesAnnotationA"
SpeA.folderStr = "config/"
SpeA.queryDict = {
    "dbgaPath" : "data/dbga-GenomeAnnotation/speciesAnnotationA/",
    "seqPath" : "data/dbgs-GenomeSequence/speciesAnnotationA/speciesAnnotationA.fa",
    "antPath" : "data/dbga-GenomeAnnotation/speciesAnnotationA/speciesAnnotationA.gff3",
    "gtfPath" : "data/dbga-GenomeAnnotation/speciesAnnotationA/speciesAnnotationA.gtf",
    "indexHeader" : "large/02-hisat2Index/speciesAnnotationA",
    "checkFolder"    : "large/02-hisat2Index/",
    "thread" : "6",
    "testing" : False,
}
SpeA.modeStr = "UPDATE"
SpeA.save()

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

gffReader = libConfig.config()
gffReader.queryStr = "binCufflinks-gffread"
gffReader.folderStr = "config/"
gffReader.queryDict = {
    "command" : "bin/cufflinks/gffread {inputFile} -T -o {outputFile}"
}
gffReader.modeStr = "UPDATE"
gffReader.save()

Copying = libConfig.config()
Copying.queryStr = "commandCP"
Copying.folderStr = "config/"
Copying.queryDict = {
    "command" : "cp -vf {output} {target}"
}
Copying.modeStr = "OVERWRITE"
Copying.save()