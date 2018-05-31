#!/usr/bin/env python3
from subprocess import Popen, call
"""
--- README of exp03-solexqa ---
Title:
    batch processing for SolexaQA++
Original command:
    time <bin>/SolexaQA++ analysis <fastq path>/<fastq file> -d <solexqa path>
Note:
    command split into [linoli,lina,linali]
Required files:
    ./list-<type>.txt
        # Path of File list
    ./SolexaQA++
        # Binary from SolexaQA++

CAUTION:
    You need to replace <PATH> with absolute path
    Because subprocess.call may fail to pass pwd to system

--- README ---
"""
linoli = ['time','<PATH>/bin/solexqa/Linux_x64/SolexaQA++','analysis']
linali = ['-d','<PATH>/data/solexqa/']

# dirodi = directory path of related fastq source
dirodi = {
    'raw' : "<PATH>/data/raw/",
    'trim' : "<PATH>/data/trim/00-fastq/",
}

# listadi = file list of related fastq file
listadi = {
    'raw' : "<PATH>/data/scripts/list-raw.txt",
    'trim' : "<PATH>/data/scripts/list-trim.txt",
}

# seta = source of fastq (from dirodi)
for seta in list(dirodi.keys()):

    # lino = fastq filename
    for lino in open(listadi[seta],"r").read().splitlines():

        # lina = <fastq path> + <fastq file>
        lina = dirodi[seta] + lino

        # lisi = log file
        lisi = '<PATH>/data/solexqa/' + lino.replace('fastq','log')

        # arguli = final command line in list type
        arguli = linoli + [lina] + linali
        print('command: '+' '.join(arguli))
        print('log: ' + lisi)
        call(arguli, stdout=open(lisi, 'w'))
