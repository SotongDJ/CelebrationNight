#!/usr/bin/env python3
import libConfig
# ---- Configuration of Experiment Design ---- 
Testing = libConfig.config()
Testing.queryStr = "testing"
Testing.folderStr = "data/config/"
# Arguments/Parameters below need to modify depend on 
# your experiment design and naming style
Testing.queryDict = {
    "branch"               : "testing",
    "group"                : ["Control","T1","T2","T3","T4","T5"],
    "direction"            : ["F","R"],
    "replication"          : ["r1"],
    "pairPostfix"          : "pair",
    "unpairPostfix"        : "unpair",
    "[trim]checkFolder"    : ["data/01-raw/","data/03-trimed/testing/"],
    "[trim]condition"      : ["trimQ20","trimQ30"],
    "[trim]inputFileName"  : "data/01-raw/{group}-{replication}-{direction}{fileType}",
    # above: data/tmp/T1-r1-F.fastq
    "[trim]outputFileName" : "data/03-trimed/testing/{condition}-{group}-{replication}-{direction}-{pairType}{fileType}",
    # above: data/03-trimed/testing/trimQ20-T1-r1-F-pair.fastq
    "[trim]fileType"       : ".fastq",
    "testing"              : True,
}
Testing.modeStr = "UPDATE"
Testing.save()

# ---- Configuration of Trimming Conditions ---- 
TrimParA = libConfig.config()
TrimParA.queryStr = "trimQ20"
TrimParA.folderStr = "data/config/"
TrimParA.queryDict = {
    "singlePair" : "PE", # Pair end
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
TrimParB.folderStr = "data/config/"
TrimParB.queryDict = {
    "singlePair" : "PE", # Pair end
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
Trim.folderStr = "data/config/"
Trim.queryDict = {
    "command" : 
        "java -jar bin/trimmomatic/trimmomatic-0.36.jar "+
        "{singlePair} -phred{phred} -threads {thread} {files} "+
        "{adapter} {lead} {trail} {slide} {length}"
}
Trim.modeStr = "OVERWRITE"
Trim.save()