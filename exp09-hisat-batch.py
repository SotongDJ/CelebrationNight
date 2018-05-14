#!/usr/bin/env python3
import librun, libconfig, sys
global helber
helber="""
   --- README of exp09-hisat-batch ---
  Title:
    Batch Processing for HISAT2

  Usage:
    python exp09-hisat-batch [stringtie|cufflinks] -t <TRIBE> -g <GROUP,GROUP,GROUP...>

  Data Structure:
    First : tribe,
        e.g. raw, untrim, trimmed...
    Second: group,
        e.g. control, A, B, 1, 2...
    Third : subgroup/files,
        e.g. foward, reverse, pair, unpair

    Visualise graph: explanation01-dataStructure.svg

  Original command:
    hisat2 -q [--dta/--dta-cufflinks] --phred[33] -p [4]
        -x [prefix of HISAT2-build genome index]
        -1 [forward fastq files of]
        -2 [reverse fastq files of]
        -S [output SAM files]
  CAUTION:
    <GROUP> must separate with space
    <GROUP> don't allowed spacing

   --- README ---
""""""
 Postfix of variables:
  -si: String
   -ni: alternative/second string for same Usage
   -fi: string for open()
  -ho: String(that store dir path)
  -ti: Intiger/Float
  -li: List
  -tu: Tuple
  -di: Dictionary
  -fa: File (with open())
  -so: JSON
"""
Confi = libconfig.confi()
class loggo(librun.loggi):
    def pesonai(self):
        self.dicodi = {
            "tribe"   : [],
            "group"   : [],
            "argv" : []
        }
        self.sync()

        self.tagesi = ""

        self.adcoli = [Confi.get("bin/hisat2"),"-q"]
        self.adphli = ["--phred"+Confi.get("run/phred")]
        self.adthli = ["-p",Confi.get("run/thread")]
        self.adgnli = ["-x",Confi.getpaf(["result/hisat", "idx/genome"])]
        self.adh1li = ["-1"]
        self.adh2li = ["-2"]
        self.adrsli = ["-S"]

        self.libadi = {}

        self.filasi = "exp09-hisat-batch.py"

        self.comali = []

        self.prelogi = Confi.get("result/log")+"/exp09-hisat-batch-"

    def actor(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])
        argvli = self.dicodi.get("argv",[])
        self.calti()

Runni = loggo()
