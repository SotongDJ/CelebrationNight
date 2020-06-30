#!/usr/bin/env python3
import libConfig
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

# ---- Configuration of Alignment Command ---- 
"""
  Original command:
    hisat2 -q [--dta/--dta-cufflinks] --phred[33] -p [4]
        -x [prefix of HISAT2-build genome index]
        -1 [forward fastq files]
        -2 [reverse fastq files]
        -U [unpair fastq files]
        -S [output SAM files]
    samtools view -o [out.bam] -Su [in.sam]
    samtools sort -o [out-sorted.bam] [in.bam]
"""

HISAT2 = libConfig.config()
HISAT2.queryStr = "binHISAT2-RUN"
HISAT2.folderStr = "config/"
HISAT2.queryDict = {
    "command-PE" : 
        "bin/hisat2/hisat2 -q {dta} --phred{phred} -p {thread} " +
        "-x {indexHeader} " +
        "-1 {pairForwardFASTQ} " +
        "-2 {pairReverseFASTQ} " +
        "-U {unpairForwardFASTQ},{unpairReverseFASTQ} " +
        "-S {outputSAM}",
    "command-SE" : 
        "bin/hisat2/hisat2 -q {dta} --phred{phred} -p {thread} " +
        "-x {indexHeader} " +
        "-U {unpairFASTQ} " +
        "-S {outputSAM}",
}
HISAT2.modeStr = "OVERWRITE"
HISAT2.save()

SAMconvert = libConfig.config()
SAMconvert.queryStr = "binSAMtools-CONVERT"
SAMconvert.folderStr = "config/"
SAMconvert.queryDict = {
    "command" : 
        "bin/samtools/samtools view -o {outputBAM} -Su {inputSAM}"
}
SAMconvert.modeStr = "OVERWRITE"
SAMconvert.save()

SAMsort = libConfig.config()
SAMsort.queryStr = "binSAMtools-SORT"
SAMsort.folderStr = "config/"
SAMsort.queryDict = {
    "command" : 
        "bin/samtools/samtools sort -o {outputBAM} {inputBAM}"
}
SAMsort.modeStr = "OVERWRITE"
SAMsort.save()

FLAGstat = libConfig.config()
FLAGstat.queryStr = "binSAMtools-FLAGSTAT"
FLAGstat.folderStr = "config/"
FLAGstat.queryDict = {
    "command" : 
        "bin/samtools/samtools flagstat {BAMfile}"
}
FLAGstat.modeStr = "OVERWRITE"
FLAGstat.save()

Remove = libConfig.config()
Remove.queryStr = "commandRM"
Remove.folderStr = "config/"
Remove.queryDict = {
    "command" : 
        "rm -vf {target}"
}
Remove.modeStr = "OVERWRITE"
Remove.save()

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