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
class stringtie(librun.workflow):
    def pesonai(self):
        # self.testing = True
        self.helb = helber

        self.dicodi = {
            "tribe"   : [],
            "group"   : []
        }
        self.Synom.input(Confi.diget("synom"))
        self.sync()

        self.tagesi = ""

        self.comali = []
        self.adcoli = [ Confi.siget("bin/stringtie") ]
        self.adotli = [ "-o" ]
        self.adphli = [ "-p", Confi.siget("run/thread")]
        self.adrfli = [ "-G", Confi.siget("refer/annotate") ]


        self.filasi = "exp12-stringtie-batch"
        self.libadi = {}
        self.prelogi = Confi.siget("result/log")+"/exp12-stringtie-batch-"

    def actor(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])

        self.head()

        self.tagesi = Confi.siget("result/stringtie")
        self.chkpaf()
        for tibe in tibeli:
            for gupo in gupoli:
                self.comali = []
                self.comali.extend(self.adcoli)
                adinsi = (
                    Confi.siget("result/hisat") + "/" +
                    Confi.siget("data/prefix/"+tibe) + gupo +
                    "-stringtie-sorted.bam"
                )
                self.comali.append(adinsi)
                self.comali.extend(self.adotli)
                adotsi = (
                    Confi.siget("result/stringtie") + "/" +
                    Confi.siget("data/prefix/"+tibe) + gupo +
                    "-stringtie.gtf"
                )
                self.comali.append(adotsi)
                self.comali.extend(self.adphli)
                self.comali.extend(self.adrfli)

                self.runit()

        self.endin()

StiTie = stringtie()
