#!/usr/bin/env python3
import librun, libconfig, sys
global helber
helber="""
--- README of exp04-fastqc ---
 Title:
  Batch Processing for FastQC

 Usage:
  python exp04-fastqc -t <TRIBE> -g <GROUP> <GROUP> <GROUP>... \\
    -s <SUBGROUP> <SUBGROUP> <SUBGROUP>...

 Data Structure:
  First : tribe,
    e.g. raw, untrim, trimmed...
  Second: group,
    e.g. control, A, B, 1, 2...
  Third : subgroup/files,
    e.g. foward, reverse, pair, unpair

 Visualise graph: explanation01-dataStructure.svg

 Original command:
  fastqc -o [Result Folder] [FASTQ files]

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
            "subgroup": []
        }
        self.Synom.input(Confi.diget("synom"))
        self.sync()

        self.tagesi = ""

        self.filasi = "exp04-fastqc"
        self.libadi = {
            "bin/fastqc" : Confi.siget("bin/fastqc"),
            "result/raw" : Confi.siget("result/raw"),
            "result/fastqc" : Confi.siget("result/fastqc"),
            "result/log" : Confi.siget("result/log"),
            "data/prefix" : Confi.diget("data/prefix"),
            "raw/type" : Confi.siget("raw/type"),
        }
        self.prelogi = self.libadi.get("result/log")+"/exp04-fastqc-"

        self.comali = []
        self.adcoli = [
            self.libadi.get("bin/fastqc") , "-o",
            self.libadi.get("result/fastqc"), "--extract",
        ]

    def actor(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])
        suguli = self.dicodi.get("subgroup",[])

        self.head()

        self.tagesi = self.libadi.get("result/fastqc")
        self.chkpaf()
        for tibe in tibeli:
            for gupo in gupoli:
                for sugu in suguli:
                    self.comali = []
                    self.comali.extend(self.adcoli)

                    inpusi = (
                        self.libadi.get("result/raw") + "/" + tibe + "/" +
                        self.libadi.get("data/prefix").get(tibe) + "-" +
                        gupo + "-" + sugu + "." + self.libadi.get("raw/type")
                    )
                    self.comali.append(inpusi)

                    self.tagesi = oputsi
                    self.chkpaf()

                    self.ranni()

        self.endin()

Runni = loggo()
