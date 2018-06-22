#!/usr/bin/env python3
import librun, libconfig, libstm
import time
global helber
helber="""
--- README of exp19-pipeline-fast ---
 Title:
  Batch Processing for StringTie (Compare)

 Usage:
  python exp19-pipeline-fast -t <TRIBE> -g <GROUP,GROUP,GROUP...>

 Data Structure:
  First : tribe,
    e.g. raw, untrim, trimmed...
  Second: group,
    e.g. control, A, B, 1, 2...
  Third : subgroup/files,
    e.g. foward, reverse, pair, unpair

  Visualise graph: explanation01-dataStructure.svg

 Original command:
  stringtie [GROUP BAM file] -B \\
    -G [Merged GTF file] -p [thread] -b [Result PATH]

 CAUTION:
  Exp14 required libstm
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
Marge = libstm.marge()
Confi = libconfig.confi()
class stititobago(librun.workflow):
    def pesonai(self):
        # self.testing = True
        self.helb = helber

        self.dicodi = {
            "tribe"   : [],
            "group"   : [],
            # "control" : ""
        }
        self.Synom.input(Confi.diget("synom"))
        self.sync()

        self.filasi = "exp19-pipeline-fast"
        self.libadi = {
            "bin/stringtie" : Confi.siget("bin/stringtie"),
            "result/stringtie" : Confi.siget("result/stringtie"),
            "result/ballgown" : Confi.siget("result/ballgown"),
            "result/hisat" : Confi.siget("result/hisat"),
            "result/log" : Confi.siget("result/log"),
            "run/thread" : Confi.siget("run/thread"),
            "data/prefix" : Confi.diget("data/prefix"),
            "refer/annotate" : Confi.diget("refer/annotate"),
        }
        self.prelogi = self.libadi.get("result/log")+"/exp19-pipeline-fast-"

        self.comali = []
        self.adcoli = [ self.libadi.get("bin/stringtie") ]
        self.adrfli = [ "-eG" ]
        self.adphli = [ "-p", self.libadi.get("run/thread")]
        self.adfoli = [ "-b" ]
        self.adotli = [ "-o" ]
        self.adagli = [ "-eA" ]

    def actor(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])
        # cotosi = self.dicodi.get("control","")

        self.head()

        self.tageli = []
        self.tageli.append(self.libadi.get("result/stringtie"))
        self.tageli.append(self.libadi.get("result/hisat"))
        self.tageli.append(self.libadi.get("result/ballgown")+"-fast")
        self.chkpaf()

        for tibe in tibeli:
            for gupo in gupoli:
                self.adinsi = self.libadi.get("refer/annotate").get(tibe)
                self.comali = []
                self.comali.extend(self.adcoli)

                adsbsi = (
                    self.libadi.get("result/hisat") + "/" +
                    self.libadi.get("data/prefix").get(tibe) +
                    gupo + "-stringtie-sorted.bam"
                )
                self.comali.append(adsbsi)

                self.comali.extend(self.adrfli)
                self.comali.append(self.adinsi)

                self.comali.extend(self.adphli)

                self.comali.extend(self.adfoli)
                adresi = (
                    self.libadi.get("result/ballgown") + "-fast/" +
                    self.libadi.get("data/prefix").get(tibe) +
                    gupo
                )
                self.comali.append(adresi)

                self.comali.extend(self.adotli)
                adresi = (
                    self.libadi.get("result/ballgown") + "-fast/" +
                    self.libadi.get("data/prefix").get(tibe) +
                    gupo + "-ballgown.gtf"
                )
                self.comali.append(adresi)

                self.comali.extend(self.adagli)
                adgesi = (
                    self.libadi.get("result/ballgown") + "-fast/" +
                    self.libadi.get("data/prefix").get(tibe) +
                    gupo + "-gene.tsv"
                )
                self.comali.append(adgesi)

                self.runit()

        self.endin()

StiToB = stititobago()
