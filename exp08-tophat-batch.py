#!/usr/bin/env python3
import librun, libconfig, sys
global helber
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
  tophat2 -p [4] -o [output folder] \\
    [prefix of bowtie2-build genome index] \\
    [forward fastq files] [reverse fastq files]
  CAUTION:
    <GROUP> must separate with space
    <GROUP> don't allowed spacing

   --- README ---
"""
"""
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
        self.helb = helber

        self.dicodi = {
            "tribe"   : [],
            "group"   : [],
            "index" : ""
        }
        self.Synom.input(Confi.diget("synom"))
        self.sync()

        self.tagesi = ""

        self.adcoli = ["tophat2"]
        self.becoli = ["-p",Confi.siget("run/thread")]
        self.cecoli = ["-o"]

        self.libadi = {
            "result/stringtie" : Confi.siget("result/stringtie")
        }

        self.filasi = "exp08-tophat-batch.py"

        self.comali = []

        self.prelogi = Confi.siget("result/log")+"/exp08-tophat-batch-"

    def actor(self):

Runni = loggo()

tibeli = Runni.dicodi.get("tribe",[])
gupoli = Runni.dicodi.get("group",[])
Runni.head()
for tibe in tibeli:
    for gupo in gupoli:
        Runni.comali = []
        Runni.comali.extend(Runni.adcoli)
        Runni.comali.extend(Runni.becoli)
        Runni.comali.extend(Runni.cecoli)

        decoli = [
            Confi.siget("result/tophat") + "/" +
            Confi.siget("data/prefix/"+tibe) + "-" + gupo
        ]
        Runni.comali.extend(decoli)

        Runni.comali.extend(Runni.edcoli)

        fecoli = [
            Confi.siget("result/raw") + "/" +
            tibe + "/" +
            Confi.siget("data/prefix/"+tibe) + "-" +
            gupo + "-" +
            Confi.siget("postfix/forward") + ".fastq"
        ]
        Runni.comali.extend(fecoli)

        gecoli = [
            Confi.siget("result/raw") + "/" +
            tibe + "/" +
            Confi.siget("data/prefix/"+tibe) + "-" +
            gupo + "-" +
            Confi.siget("postfix/reverse") + ".fastq"
        ]
        Runni.comali.extend(gecoli)

        Runni.tagesi = Confi.siget("result/tophat")
        Runni.chkpaf()

        # Runni.test()
        Runni.ranni()
Runni.endin()
