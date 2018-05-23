#!/usr/bin/env python3
import librun, libconfig, sys
global helber
helber="""
   --- README of exp12-stringtie-batch ---
  Title:
    Batch Processing for StringTie (Assembly)

  Usage:
    python exp12-stringtie-batch -t <TRIBE> -g <GROUP,GROUP,GROUP...>

  Data Structure:
    First : tribe,
        e.g. raw, untrim, trimmed...
    Second: group,
        e.g. control, A, B, 1, 2...
    Third : subgroup/files,
        e.g. foward, reverse, pair, unpair

    Visualise graph: explanation01-dataStructure.svg

  Original command:
    stringtie [BAM file] -o [Result GTF file]\
        -p [Thread] -G [Reference GFF file] -e

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

        self.dicodi = {
            "tribe"   : [],
            "group"   : []
        }
        self.sync()

        self.tagesi = ""

        self.comali = []
        self.adcoli = [ Confi.get("bin/stringtie") ]
        self.adotli = [ "-o" ]
        self.adphli = [ "-p", Confi.get("run/thread")]
        self.adrfli = [ "-G", Confi.get("refer/annotate") ]


        self.filasi = "exp12-stringtie-batch"
        self.libadi = {}
        self.prelogi = Confi.get("result/log")+"/exp12-stringtie-batch-"

    def actor(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])

        self.hedda()

        self.tagesi = Confi.get("result/stringtie")
        self.chkpaf()
        for tibe in tibeli:
            for gupo in gupoli:
                self.comali = []
                self.comali.extend(self.adcoli)
                adinsi = (
                    Confi.get("result/hisat") + "/" +
                    Confi.get("data/prefix/"+tibe) + "-" + gupo +
                    "-stringtie-sorted.bam"
                )
                self.comali.append(adinsi)
                self.comali.extend(self.adotli)
                adotsi = (
                    Confi.get("result/stringtie") + "/" +
                    Confi.get("data/prefix/"+tibe) + "-" + gupo +
                    "-stringtie.gtf"
                )
                self.comali.append(adotsi)
                self.comali.extend(self.adphli)
                self.comali.extend(self.adrfli)

                self.ranni()

        self.calti()

Runni = loggo()
