#!/usr/bin/env python3
import libConfig
# ---- Keyword list ----
"""
SpeA, speciesAnnotationA
SpeB, speciesAnnotationB
SpeC, speciesAnnotationC
"""
# ---- Configuration of Indexing Conditions ---- 
SpeA = libConfig.config()
SpeA.queryStr = "speciesAnnotationA"
SpeA.folderStr = "config/"
SpeA.queryDict = {
    "from" : "binHISAT2-BUILD",
    "seqPath" : "data/dbgs-GenomeSequence/speciesAnnotationA/speciesAnnotationA.fa",
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
    "from" : "binHISAT2-BUILD",
    "seqPath" : "data/dbgs-GenomeSequence/speciesAnnotationB/speciesAnnotationB.fna",
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
    "from" : "binHISAT2-BUILD",
    "seqPath" : "data/dbgs-GenomeSequence/speciesAnnotationC/speciesAnnotationC.fasta",
    "indexHeader" : "large/02-hisat2Index/speciesAnnotationC",
    "checkFolder"    : "large/02-hisat2Index/",
    "thread" : "6",
    "testing" : False,
}
SpeC.modeStr = "UPDATE"
SpeC.save()
# ---- Configuration of Indexing Command ---- 
"""
Usage:
    hisat2-build [options]* <reference_in> <ht2_base>

Main arguments
    <reference_in>
        A comma-separated list of FASTA files containing the reference sequences to be 
        aligned to, or, if -c is specified, the sequences themselves. 
        E.g., <reference_in> might be chr1.fa,chr2.fa,chrX.fa,chrY.fa, or, 
        if -c is specified, this might be GGTCATCCT,ACGGGTCGT,CCGTTCTATGCGGCTTA.

    <ht2_base>
        The basename of the index files to write. 
        By default, hisat2-build writes files named NAME.1.ht2, NAME.2.ht2, NAME.3.ht2, NAME.4.ht2, 
        NAME.5.ht2, NAME.6.ht2, NAME.7.ht2, and NAME.8.ht2 where NAME is <ht2_base>.
"""

HISAT = libConfig.config()
HISAT.queryStr = "binHISAT2-BUILD"
HISAT.folderStr = "config/"
HISAT.queryDict = {
    "command" : "bin/hisat2/hisat2-build -p {thread} {seqPath} {indexHeader}"
}
HISAT.modeStr = "OVERWRITE"
HISAT.save()
