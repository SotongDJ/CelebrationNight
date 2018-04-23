from subprocess import Popen, call
"""
--- README of exp02-q2a-batch ---
Title:
    batch processing for fastq_to_fasta binary
Original command:
    time <bin>/fastq_to_fasta -v -Q33 -i <fastq file> -o <fasta file>
Note:
    command split into [linoli,lino,linali,lina,lisi]
Required files:
    ./list.txt
        # Path of File list
    ./fastq_to_fasta
        # Binary from fastx toolkit

--- README ---
"""
linoli = ['time','./fastq_to_fasta','-v','-Q33','-i',]
linali = ['-o']

# lino = fastq filename
for lino in open("list.txt","r").read().splitlines():
    if "#" not in lino:

        # lina = fasta filename (and replace '_' with '-')
        lina = lino.replace('_','-').replace('fastq','fasta')

        # lisi = log file (and replace '_' with '-')
        lisi =  lino.replace('_','-').replace('fastq','log')

        # arguli = final command line in list type
        arguli = \
        linoli + [lino] + \
        linali + [lina]

        print(arguli)
        call(arguli, stdout=open(lisi, 'w'))
