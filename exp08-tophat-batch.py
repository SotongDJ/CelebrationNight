#!/usr/bin/env python3
import librun, libconfig, sys
helber="""
   --- README of exp08-tophat-batch ---
  Title:
    Batch Processing for TopHat2

  Usage:
    python exp08-tophat-batch -t <TRIBE> -g <GROUP,GROUP,GROUP...>

  Data Structure:
    First : tribe,
        e.g. raw, untrim, trimmed...
    Second: group,
        e.g. control, A, B, 1, 2...
    Third : subgroup/files,
        e.g. foward, reverse, pair, unpair

    Visualise graph: explanation01-dataStructure.svg

  Original command:
  tophat2
        -p [4]
        -o [output folder]
        [prefix of bowtie2-build genome index]
        [forward fastq files]
        [reverse fastq files]
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
        # self.testing = True
        self.typesi = 'script'
        
        self.dicodi = {
            "tribe"   : [],
            "group"   : [],
        }
        self.sync()

        self.tagesi = ""

        self.adcoli = ["tophat2"]
        self.becoli = ["-p",Confi.get("run/thread")]
        self.cecoli = ["-o"]
        self.edcoli = [Confi.getpaf(["result/bowtie", "idx/genome"])]

        self.libadi = {}

        self.filasi = "exp08-tophat-batch.py"

        self.comali = []

        self.prelogi = Confi.get("result/log")+"/exp08-tophat-batch-"

Runni = loggo()

tibeli = Runni.dicodi.get("tribe",[])
gupoli = Runni.dicodi.get("group",[])
Runni.hedda()
for tibe in tibeli:
    for gupo in gupoli:
        Runni.comali = []
        Runni.comali.extend(Runni.adcoli)
        Runni.comali.extend(Runni.becoli)
        Runni.comali.extend(Runni.cecoli)

        decoli = [
            Confi.get("result/tophat") + "/" +
            Confi.get("data/prefix/"+tibe) + "-" + gupo
        ]
        Runni.comali.extend(decoli)

        Runni.comali.extend(Runni.edcoli)

        fecoli = [
            Confi.get("result/raw") + "/" +
            tibe + "/" +
            Confi.get("data/prefix/"+tibe) + "-" +
            gupo + "-" +
            Confi.get("postfix/forward") + ".fastq"
        ]
        Runni.comali.extend(fecoli)

        gecoli = [
            Confi.get("result/raw") + "/" +
            tibe + "/" +
            Confi.get("data/prefix/"+tibe) + "-" +
            gupo + "-" +
            Confi.get("postfix/reverse") + ".fastq"
        ]
        Runni.comali.extend(gecoli)

        Runni.tagesi = Confi.get("result/tophat")
        Runni.chkpaf()

        # Runni.test()
        Runni.ranni()
Runni.calti()
