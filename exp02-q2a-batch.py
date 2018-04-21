from subprocess import Popen, call

#    ---README---
#
# exp02-q2a-batch
#     batch processing for fastq_to_fasta binary
#
# original command:
#    time <bin>/fastq_to_fasta -v -Q33 -i <fastq file> -o <fasta file>
#
# Note:
#    command split into [linose,lino,linase,lina,lisi]
#
# file list path:
#    ./list.txt
#
#    ---README---

linose = ['time','./fastq_to_fasta','-v','-Q33','-i',]
linase = ['-o']

# lino = fastq filename
for lino in open("list.txt","r").read().splitlines():
    if "#" not in lino:
        # lina = fasta filename (and replace '_' with '-')
        lina = lino.replace('_','-').replace('fastq','fasta')
        # lisi = log file (and replace '_' with '-')
        lisi =  lino.replace('_','-').replace('fastq','log')
        argumase = \
        linose + [lino] + \
        linase + [lina]
        print(argumase)
        call(argumase, stdout=open(lisi, 'w'))
