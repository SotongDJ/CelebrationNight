#!/usr/bin/env python3
import libConfig
# ---- Keyword list ----
"""
SpeA, speciesTestingA
SpeB, speciesTestingB
SpeC, speciesTestingC
"""
# ---- Configuration of Indexing Conditions ---- 
SpeA = libConfig.config()
SpeA.queryStr = "speciesTestingA"
SpeA.folderStr = "config/"
SpeA.queryDict = {
    "from" : "binHISAT2-BUILD",
    "seqPath" : "large/dbgs-GenomeSequence/speciesTestingA/speciesTestingA.fa",
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
    "from" : "binHISAT2-BUILD",
    "seqPath" : "large/dbgs-GenomeSequence/speciesTestingB/speciesTestingB.fna",
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
    "from" : "binHISAT2-BUILD",
    "seqPath" : "large/dbgs-GenomeSequence/speciesTestingC/speciesTestingC.fasta",
    "indexHeader" : "large/02-hisat2Index/speciesTestingC",
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
