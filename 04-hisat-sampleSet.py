import libConfig
Testing = libConfig.config()
# ---- Configuration of Experiment Design ---- 
Testing.queryStr = "testing"
Testing.folderStr = "data/config/"
# Arguments/Parameters below need to modify depend on 
# your experiment design and naming style
Testing.queryDict = {
    "branch" : "testing",
    "group" : ["Control","T1","T2","T3","T4","T5"],
    "direction" : ["F","R"],
    "pairPostfix" : "pair",
    "unpairPostfix" : "unpair",
    "[trim]checkFolder" : ["data/tmp/"],
    "[trim]condition" : ["trimQ20","trimQ30"],
    "[trim]inputFileName" : "data/tmp/{group}-{direction}{fileType}",
    # above: data/tmp/A-R1.fastq
    "[trim]outputFileName" : "data/tmp/{condition}-{group}-{direction}-{pairType}{fileType}",
    # above: data/tmp/A-R1-pair.fastq
    "[trim]fileType" : ".fastq",
    "testing" : True,
}
Testing.modeStr = "UPDATE"
Testing.save()

# ---- Configuration of Trimming Conditions ---- 
TrimParA = libConfig.config()
TrimParA.queryStr = "trimQ20"
TrimParA.folderStr = "data/config/"
TrimParA.queryDict = {
    "singlePair" : "PE", # Pair end
    "phred"   : "33", # sequencing type, illumina solexa = 33
    "thread"  : "6", # cluster server have 8 cores
    "lead"    : "LEADING:20",
    "trail"   : "TRAILING:20",
    "slide"   : "SLIDINGWINDOW:4:20",
    "length"  : "MINLEN:36",
    "adapter" : "ILLUMINACLIP:bin/trimmomatic/adapters/TruSeq3-PE.fa:2:30:10",
}
TrimParA.modeStr = "OVERWRITE"
TrimParA.save()

TrimParB = libConfig.config()
TrimParB.queryStr = "trimQ30"
TrimParB.folderStr = "data/config/"
TrimParB.queryDict = {
    "singlePair" : "PE", # Pair end
    "phred"   : "33", # sequencing type, illumina solexa = 33
    "thread"  : "6", # cluster server have 8 cores
    "lead"    : "LEADING:30",
    "trail"   : "TRAILING:30",
    "slide"   : "SLIDINGWINDOW:4:30",
    "length"  : "MINLEN:36",
    "adapter" : "ILLUMINACLIP:bin/trimmomatic/adapters/TruSeq3-PE.fa:2:30:10",
}
TrimParB.modeStr = "OVERWRITE"
TrimParB.save()

# ---- Configuration of Trimming Command ---- 
"""

"""

Trim = libConfig.config()
Trim.queryStr = "binHISAT2-RUN"
Trim.folderStr = "data/config/"
Trim.queryDict = {
    "command" : 
        "hisat2 -q {dta} --phred{phred} -p {thread}" +
        "-x {indexHeader}" +
        "-1 {fowardFASTQ}" +
        "-2 {reverseFASTQ}" +
        "-S {outputSAM}"
}
Trim.modeStr = "OVERWRITE"
Trim.save()