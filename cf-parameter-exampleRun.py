#!/usr/bin/env python3
import libConfig
# ---- Configuration of Indexing Conditions ---- 
SpeDataBase = libConfig.config()
SpeDataBase.queryStr = "speciesDatabase"
SpeDataBase.folderStr = "config/"
SpeDataBase.queryDict = {
    "from" : "binHISAT2-BUILD",
    "dbgaPath" : "userData/dbga-GenomeAnnotation/speciesDatabase/",
    "seqPath" : "userData/dbgs-GenomeSequence/speciesDatabase/speciesDatabase.fn",
    "antPath" : "userData/dbga-GenomeAnnotation/speciesDatabase/speciesDatabase.gff3",
    "gtfPath" : "userData/dbga-GenomeAnnotation/speciesDatabase/speciesDatabase.gtf",
    "indexHeader" : "largeData/02-hisat2Index/speciesDatabase",
    "checkFolder" : "largeData/02-hisat2Index/",
    "thread" : "6",
    "testing" : False,
}
SpeDataBase.modeStr = "UPDATE"
SpeDataBase.save()

SpeDataBaseTwo = libConfig.config()
SpeDataBaseTwo.queryStr = "speciesDatabase2"
SpeDataBaseTwo.folderStr = "config/"
SpeDataBaseTwo.queryDict = {
    "from" : "binHISAT2-BUILD",
    "dbgaPath" : "userData/dbga-GenomeAnnotation/speciesDatabase2/",
    "seqPath" : "userData/dbgs-GenomeSequence/speciesDatabase2/speciesDatabase2.fn",
    "antPath" : "userData/dbga-GenomeAnnotation/speciesDatabase2/speciesDatabase2.gff3",
    "gtfPath" : "userData/dbga-GenomeAnnotation/speciesDatabase2/speciesDatabase2.gtf",
    "indexHeader" : "largeData/02-hisat2Index/speciesDatabase2",
    "checkFolder" : "largeData/02-hisat2Index/",
    "thread" : "6",
    "testing" : False,
}
SpeDataBaseTwo.modeStr = "UPDATE"
SpeDataBaseTwo.save()

SpeDataBaseThree = libConfig.config()
SpeDataBaseThree.queryStr = "speciesDatabase3"
SpeDataBaseThree.folderStr = "config/"
SpeDataBaseThree.queryDict = {
    "from" : "binHISAT2-BUILD",
    "dbgaPath" : "userData/dbga-GenomeAnnotation/speciesDatabase3/",
    "seqPath" : "userData/dbgs-GenomeSequence/speciesDatabase3/speciesDatabase3.fn",
    "antPath" : "userData/dbga-GenomeAnnotation/speciesDatabase3/speciesDatabase3.gff3",
    "gtfPath" : "userData/dbga-GenomeAnnotation/speciesDatabase3/speciesDatabase3.gtf",
    "indexHeader" : "largeData/02-hisat2Index/speciesDatabase3",
    "checkFolder" : "largeData/02-hisat2Index/",
    "thread" : "6",
    "testing" : False,
}
SpeDataBaseThree.modeStr = "UPDATE"
SpeDataBaseThree.save()

SpeTwoDataBase = libConfig.config()
SpeTwoDataBase.queryStr = "species2Database"
SpeTwoDataBase.folderStr = "config/"
SpeTwoDataBase.queryDict = {
    "dbgaPath" : "userData/dbga-GenomeAnnotation/species2Database/",
    "seqPath" : "userData/dbgs-GenomeSequence/species2Database/species2Database.fn",
    "antPath" : "userData/dbga-GenomeAnnotation/species2Database/species2Database.gff3",
    "gtfPath" : "userData/dbga-GenomeAnnotation/species2Database/species2Database.gtf",
    "indexHeader" : "largeData/02-hisat2Index/species2Database",
    "checkFolder" : "largeData/02-hisat2Index/",
    "thread" : "6",
    "testing" : False,
}
SpeTwoDataBase.modeStr = "UPDATE"
SpeTwoDataBase.save()

# ---- Configuration of Trimming Conditions ---- 
TrimParA = libConfig.config()
TrimParA.queryStr = "trimQ20"
TrimParA.folderStr = "config/"
TrimParA.queryDict = {
    "header" : "trimQ20",
    "phred" : "33", # sequencing type, illumina solexa = 33
    "thread" : "6", # cluster server have 8 cores
    "lead" : "LEADING:20",
    "trail" : "TRAILING:20",
    "slide" : "SLIDINGWINDOW:4:20",
    "length" : "MINLEN:36",
    "adapter" : "ILLUMINACLIP:bin/trimmomatic/adapters/TruSeq3-PE.fa:2:30:10",
}
TrimParA.modeStr = "OVERWRITE"
TrimParA.save()

TrimParB = libConfig.config()
TrimParB.queryStr = "trimQ30"
TrimParB.folderStr = "config/"
TrimParB.queryDict = {
    "header" : "trimQ30",
    "phred" : "33", # sequencing type, illumina solexa = 33
    "thread" : "6", # cluster server have 8 cores
    "lead" : "LEADING:30",
    "trail" : "TRAILING:30",
    "slide" : "SLIDINGWINDOW:4:30",
    "length" : "MINLEN:36",
    "adapter" : "ILLUMINACLIP:bin/trimmomatic/adapters/TruSeq3-PE.fa:2:30:10",
}
TrimParB.modeStr = "OVERWRITE"
TrimParB.save()

TrimParC = libConfig.config()
TrimParC.queryStr = "trimQ30-SE"
TrimParC.folderStr = "config/"
TrimParC.queryDict = {
    "header" : "trimQ30",
    "phred" : "33", # sequencing type, illumina solexa = 33
    "thread" : "6", # cluster server have 8 cores
    "lead" : "LEADING:30",
    "trail" : "TRAILING:30",
    "slide" : "SLIDINGWINDOW:4:30",
    "length" : "MINLEN:36",
    "adapter" : "ILLUMINACLIP:bin/trimmomatic/adapters/TruSeq3-SE.fa:2:30:10",
}
TrimParC.modeStr = "OVERWRITE"
TrimParC.save()

# ---- Configuration of Alignment Conditions ---- 
stringtiePara = libConfig.config()
stringtiePara.queryStr = "hisat2ForStringtie"
stringtiePara.folderStr = "config/"
stringtiePara.queryDict = {
    "dta" : "--dta", 
    "phred" : "33", # sequencing type, illumina solexa = 33
    "thread" : "6", # cluster server have 8 cores
}
stringtiePara.modeStr = "OVERWRITE"
stringtiePara.save()

cufflinksPara = libConfig.config()
cufflinksPara.queryStr = "hisat2ForCufflinks"
cufflinksPara.folderStr = "config/"
cufflinksPara.queryDict = {
    "dta" : "--dta-cufflinks", 
    "phred" : "33", # sequencing type, illumina solexa = 33
    "thread" : "6", # cluster server have 8 cores
}
cufflinksPara.modeStr = "OVERWRITE"
cufflinksPara.save()
