#!/usr/bin/env python3
import libConfig
# ---- Configuration of Indexing Conditions ---- 
SpeA = libConfig.config()
SpeA.queryStr = "speciesTestingA"
SpeA.folderStr = "data/config/"
SpeA.queryDict = {
    "from" : "binHISAT2-BUILD",
    "seqPath" : "data/GenomeSequence/SpeA.fa",
    "indexHeader" : "large/02-hisat2Index/SpeA",
    "checkFolder"    : "large/02-hisat2Index/",
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
    "indexHeader" : "large/02-hisat2Index/SpeB",
    "checkFolder"    : "large/02-hisat2Index/",
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
    "indexHeader" : "large/02-hisat2Index/SpeC",
    "checkFolder"    : "large/02-hisat2Index/",
    "thread" : "6",
    "testing" : True,
}
SpeC.modeStr = "OVERWRITE"
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
HISAT.folderStr = "data/config/"
HISAT.queryDict = {
    "command" : "bin/hisat2/hisat2-build -p {thread} {seqPath} {indexHeader}"
}
HISAT.modeStr = "OVERWRITE"
HISAT.save()
