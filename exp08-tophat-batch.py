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

        self.libadi = {
            "result/tophat"   : Confi.siget("result/tophat"),
            "result/log"      : Confi.siget("result/log"),
            "run/thread"      : Confi.siget("run/thread"),
            "data/prefix"     : Confi.diget("data/prefix"),
            "result/raw"      : Confi.siget("result/raw"),
            "postfix/forward" : Confi.siget("postfix/forward"),
            "postfix/reverse" : Confi.siget("postfix/reverse")
        }

        self.tagesi = ""

        self.adcoli = ["tophat2"]
        self.becoli = ["-p",self.libadi.get("run/thread")]
        self.cecoli = ["-o"]

        self.filasi = "exp08-tophat-batch.py"

        self.comali = []

        self.prelogi = self.libadi.get("result/log")+"/exp08-tophat-batch-"

    def actor(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])
        indesi = self.dicodi.get("index","")

        self.head()

        if indesi != "":
            for tibe in tibeli:
                for gupo in gupoli:
                    self.comali = []
                    self.comali.extend(self.adcoli)
                    self.comali.extend(self.becoli)
                    self.comali.extend(self.cecoli)

                    decoli = [
                        self.libadi.get("result/tophat") + "/" +
                        self.libadi.get("data/prefix").get(tibe) + gupo
                    ]
                    self.comali.extend(decoli)

                    self.comali.append(indesi)

                    fecoli = [
                        self.libadi.get("result/raw") + "/" +
                        tibe + "/" +
                        self.libadi.get("data/prefix").get(tibe) +
                        gupo + "-" +
                        self.libadi.get("postfix/forward") + ".fastq"
                    ]
                    self.comali.extend(fecoli)

                    gecoli = [
                        self.libadi.get("result/raw") + "/" +
                        tibe + "/" +
                        self.libadi.get("data/prefix").get(tibe) +
                        gupo + "-" +
                        self.libadi.get("postfix/reverse") + ".fastq"
                    ]
                    self.comali.extend(gecoli)

                    self.tagesi = self.libadi.get("result/tophat")
                    self.chkpaf()

                    self.ranni()
        self.endin()

Runni = loggo()
