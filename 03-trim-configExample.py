#!/usr/bin/env python3
import libConfig
# ---- Keyword list ----
"""
large/01-raw/T1r1-F.fastq
large/03-trimed/testing/trimQ30-T1r1-F-pair.fastq
testing
["Control","T1","T2","T3","T4","T5"]
["F","R"]
["r1"]
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
    "branch"               : "testing",
    "group"                : ["Control","T1","T2","T3","T4","T5"],
    "direction"            : ["F","R"],
    "replication"          : ["r1"],
    "pairPostfix"          : "pair",
    "unpairPostfix"        : "unpair",
    "mode"                 : "pairEnd",
    "[trim]checkFolder"    : ["large/01-raw/","large/03-trimed/testing/"],
    "[trim]condition"      : ["trimQ30"],
    "[trim]inputFileName"  : "large/01-raw/{group}{replication}-{direction}{fileType}",
    # above: large/01-raw/T1r1-F.fastq
    "[trim]outputFileName" : "large/03-trimed/testing/{condition}-{group}{replication}-{direction}-{pairType}{fileType}",
    # above: large/03-trimed/testing/trimQ30-T1r1-F-pair.fastq
    "[trim]fileType"       : ".fastq",
    "testing"              : False,
}
expRep.modeStr = "UPDATE"
expRep.save()

expRep = libConfig.config()
expRep.queryStr = "testing-singleEnd-{direction}-{pairType}"
expRep.folderStr = "config/"
expRep.queryDict = {
    "branch"               : "testing-singleEnd",
    "group"                : ["Control","T1","T2","T3","T4","T5"],
    "direction"            : ["F","R"],
    "replication"          : ["r1"],
    "pairPostfix"          : "pair",
    "unpairPostfix"        : "unpair",
    "mode"                 : "singleEnd",
    "[trim]checkFolder"    : ["large/01-raw/","large/03-trimed/testing/"],
    "[trim]condition"      : ["trimQ30-SE"],
    "[trim]inputFileName"  : "large/01-raw/{group}{replication}{fileType}",
    # above: large/01-raw/T1r1.fastq
    "[trim]outputFileName" : "large/03-trimed/testing/{condition}-{group}{replication}{fileType}",
    # above: large/03-trimed/testing/trimQ30-T1r1.fastq
    "[trim]fileType"       : ".fastq",
    "testing"              : False,
}
expRep.modeStr = "UPDATE"
expRep.save()

# ---- Configuration of Trimming Conditions ---- 
TrimParA = libConfig.config()
TrimParA.queryStr = "trimQ20"
TrimParA.folderStr = "config/"
TrimParA.queryDict = {
    "header"     : "trimQ20",
    "phred"      : "33", # sequencing type, illumina solexa = 33
    "thread"     : "6", # cluster server have 8 cores
    "lead"       : "LEADING:20",
    "trail"      : "TRAILING:20",
    "slide"      : "SLIDINGWINDOW:4:20",
    "length"     : "MINLEN:36",
    "adapter"    : "ILLUMINACLIP:bin/trimmomatic/adapters/TruSeq3-PE.fa:2:30:10",
}
TrimParA.modeStr = "OVERWRITE"
TrimParA.save()

TrimParB = libConfig.config()
TrimParB.queryStr = "trimQ30"
TrimParB.folderStr = "config/"
TrimParB.queryDict = {
    "header"     : "trimQ30",
    "phred"      : "33", # sequencing type, illumina solexa = 33
    "thread"     : "6", # cluster server have 8 cores
    "lead"       : "LEADING:30",
    "trail"      : "TRAILING:30",
    "slide"      : "SLIDINGWINDOW:4:30",
    "length"     : "MINLEN:36",
    "adapter"    : "ILLUMINACLIP:bin/trimmomatic/adapters/TruSeq3-PE.fa:2:30:10",
}
TrimParB.modeStr = "OVERWRITE"
TrimParB.save()

TrimParC = libConfig.config()
TrimParC.queryStr = "trimQ30-SE"
TrimParC.folderStr = "config/"
TrimParC.queryDict = {
    "header"     : "trimQ30",
    "phred"      : "33", # sequencing type, illumina solexa = 33
    "thread"     : "6", # cluster server have 8 cores
    "lead"       : "LEADING:30",
    "trail"      : "TRAILING:30",
    "slide"      : "SLIDINGWINDOW:4:30",
    "length"     : "MINLEN:36",
    "adapter"    : "ILLUMINACLIP:bin/trimmomatic/adapters/TruSeq3-SE.fa:2:30:10",
}
TrimParC.modeStr = "OVERWRITE"
TrimParC.save()
# ---- Configuration of Trimming Command ---- 
"""
FROM: http://www.usadellab.org/cms/?page=trimmomatic

java -jar <path to trimmomatic.jar> PE [-threads <threads] [-phred33 | -phred64] [-trimlog <logFile>] \
    <input 1> <input 2> <paired output 1> <unpaired output 1> <paired output 2> <unpaired output 2> \
    <step 1> ...

java -jar trimmomatic-0.35.jar PE -phred33 input_forward.fq.gz input_reverse.fq.gz \
    output_forward_paired.fq.gz output_forward_unpaired.fq.gz output_reverse_paired.fq.gz \
    output_reverse_unpaired.fq.gz ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 \
    SLIDINGWINDOW:4:15 MINLEN:36

Step options:
* ILLUMINACLIP:<fastaWithAdaptersEtc>:<seed mismatches>:<palindrome clip threshold>:<simple clip threshold>
    * fastaWithAdaptersEtc: 
        specifies the path to a fasta file containing all the adapters, PCR sequences etc. 
        The naming of the various sequences within this file determines how they are used. 
        See below.
    * seedMismatches: 
        specifies the maximum mismatch count which will still allow a full match to be performed
    * palindromeClipThreshold: 
        specifies how accurate the match between the two 'adapter ligated' reads must be for PE palindrome read alignment.
    * simpleClipThreshold: 
        specifies how accurate the match between any adapter etc. 
        sequence must be against a read.
* SLIDINGWINDOW:<windowSize>:<requiredQuality>
    * windowSize: specifies the number of bases to average across
    * requiredQuality: specifies the average quality required.
* LEADING:<quality>
    * quality: Specifies the minimum quality required to keep a base.
* TRAILING:<quality>
    * quality: Specifies the minimum quality required to keep a base.
* CROP:<length>
    * length: The number of bases to keep, from the start of the read.
* HEADCROP:<length>
    * length: The number of bases to remove from the start of the read.
* MINLEN:<length>
    * length: Specifies the minimum length of reads to be kept.
"""

Trim = libConfig.config()
Trim.queryStr = "binTrimmomatic"
Trim.folderStr = "config/"
Trim.queryDict = {
    "command" : 
        "java -jar bin/trimmomatic/trimmomatic-0.36.jar "+
        "{mode} -phred{phred} -threads {thread} {files} "+
        "{adapter} {lead} {trail} {slide} {length}"
}
Trim.modeStr = "OVERWRITE"
Trim.save()