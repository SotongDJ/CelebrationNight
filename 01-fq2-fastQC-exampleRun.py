import subprocess
bamList = [ n for n in open("hisat2-list.txt").read().splitlines()]
fastqc = "bin/FastQC/fastqc -f fastq -o largeData/04-hisat2/species/speciesDatabase-trimQ30/report"
commandList = list()
commandList.extend(fastqc.split(" "))
commandList.extend(bamList)
subprocess.call(commandList)