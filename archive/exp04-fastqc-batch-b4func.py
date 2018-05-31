#!/usr/bin/env python3
import sys
from subprocess import call

helber="""
   --- README of exp04-fastqc-batch ---
Title:
    batch processing for FastQC

Usage:
    python exp04-fastqc-batch <TRIBE> <GROUP,GROUP,GROUP...>

Structure:
    First : tribe,
        e.g. raw, untrim, trimmed...
    Second: group,
        e.g. control, A, B, 1, 2...
    Third : subgroup/files,
        e.g. foward, reverse, pair, unpair

Required files:
    <PATH>/list-[source].txt
        # File list
    <bin>/fastqc
        # Binary from SolexaQA++

Original command:
    time <bin>/fastqc -o <output path> --extract <fastq path>

CAUTION:
    You need to replace <PATH> with absolute path
    Because subprocess.call may fail to pass pwd to system

   --- README ---
""""""
    command split into [ linose , lina ]
"""
# patoho: path of <PATH>, format: "/path/to/your/folder"
patoho = 'path'

# binoho: <bin>
binoho = patoho + '/bin/fastqc'

# resuho: path of output directory
resuho = patoho + '/data/fastqc'

# linose: first part of command
linose = ['time', binoho + '/fastqc',\
    '-o', patoho + '/data/fastqc/','--extract']

# dirodi: directory of related [source]
dirodi = {
    'raw' : patoho + "/data/raw",
    'trim' : patoho + "/data/trim/00-fastq",
}

# listadi: list file of fastq files
listadi = {
    'raw' : patoho + "/data/scripts/list-raw.txt",
    'trim' : patoho + "/data/scripts/list-trim.txt",
}

# helber: helper message
helber = """
Usage:
    python fastqc-batch.py <source>
Note:
    [source]: directory of fastq files
Required:
    ./list-[source].txt: file list of fastq files
    [PATH]/fastqc: binary of fastqc
Modify:
    You need to generate list file with following command:
        ls -1 [PATH]/[source] > list-[source].txt
    You need to modify the values of valiable before initialisation.
"""

# --- Initialization ---

if len(sys.argv) == 1:
    print(helber)

# seta: argument on command line
for seta in sys.argv:
    if seta in list(dirodi.keys()):

        # lino: [source]
        for lino in open(listadi[seta],"r").read().splitlines():

            # lina: [path]+[source]
            lina = dirodi[seta] + "/" + lino

            # lisi: log file, [path]+[source].log
            lisi = resuho + '/' + lino.replace('fastq','log')

            # arguli: argument
            arguli = linose + [lina]

            print('Command: ' + ' '.join(arguli))
            print('Log: ' + lisi)
            call(arguli, stdout=open(lisi, 'w'))

    elif seta in ['-h','--help','-help','/?']:
        print(helber)

    else:
        print( 'Ignore: ' + seta )
