#!/usr/bin/env python3
import librun, libconfig
global helber
helber="""
   --- README of exp13-stringtie-merge ---
  Title:
    Merge transcriptome for StringTie

  Usage:
    python exp13-stringtie-merge -t <TRIBE> -g <GROUP,GROUP,GROUP...>

  Data Structure:
    First : tribe,
        e.g. raw, untrim, trimmed...
    Second: group,
        e.g. control, A, B, 1, 2...
    Third : subgroup/files,
        e.g. foward, reverse, pair, unpair

    Visualise graph: explanation01-dataStructure.svg

  Original command:
    stringtie [gtf files] --merge -o [path for result]\
        -p [thread] -G [reference gff file]

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
class stitiemerge(librun.workflow):
    def pesonai(self):
        # self.testing = True
        self.helb = helber

        self.dicodi = {
            "tribe"   : [],
            "group"   : []
        }
        self.Synom.input(Confi.diget("synom"))
        self.sync()
        self.libadi = {
            "bin/stringtie"    : Confi.siget("bin/stringtie"),
            "run/thread"       : Confi.siget("run/thread"),
            "refer/annotate"   : Confi.siget("refer/annotate"),
            "result/log"       : Confi.siget("result/log"),
            "result/stringtie" : Confi.siget("result/stringtie"),
            "data/prefix"      : Confi.diget("data/prefix"),
        }

        self.tagesi = ""

        self.comali = []
        self.adcoli = [ self.libadi.get("bin/stringtie") ]
        self.admgli = [ "--merge" ]
        self.adotli = [ "-o" ]
        self.adphli = [ "-p", self.libadi.get("run/thread")]
        self.adrfli = [ "-G", self.libadi.get("refer/annotate") ]


        self.filasi  = "exp13-stringtie-merge"
        self.prelogi = self.libadi.get("result/log")+"/exp13-stringtie-merge-"

    def actor(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])

        self.head()

        self.tagesi = self.libadi.get("result/stringtie")
        self.chkpaf()
        for tibe in tibeli:
            self.comali = []
            self.comali.extend(self.adcoli)

            for gupo in gupoli:
                guposi = ""
                guposi = (
                    self.libadi.get("result/stringtie") + "/" +
                    self.libadi.get("data/prefix").get(tibe) + gupo +
                    "-stringtie.gtf"
                )
                self.comali.append(guposi)

            self.comali.extend(self.admgli)
            self.comali.extend(self.adotli)
            self.outusi = (
                self.libadi.get("result/stringtie") + "/" +
                self.libadi.get("data/prefix").get(tibe) + "-".join(sorted(gupoli)) +"-stringtie-merged.gtf"
            )
            self.comali.append(self.outusi)
            self.comali.extend(self.adphli)
            self.comali.extend(self.adrfli)

            self.runit()
        self.endin()

StiTim = stitiemerge()
