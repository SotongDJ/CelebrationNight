#!/usr/bin/env python3
import librun, libconfig
global helber
helber="""
--- README of library-stringtie-merge ---
 Title:
  Merge transcriptome for StringTie

 Usage:
  import libstmerge
  Marge = libstmerge.loggo()
  Marge.testing = self.testing
  Marge.prelogi = < Log File Path>
  Marge.dicodi = {
    "tribe"   : <TRIBE>,
    "group"   : [<GROUP>,<GROUP>......]
  }
  Marge.actor()

 Data Structure:
  First : tribe,
    e.g. raw, untrim, trimmed...
  Second: group,
    e.g. control, A, B, 1, 2...
  Third : subgroup/files,
    e.g. foward, reverse, pair, unpair

  Visualise graph: explanation01-dataStructure.svg

 Original command:
  stringtie [gtf files] --merge -o [path for result] \\
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
class loggo(librun.loggi):
    def redirek(self):
        """"""
    def pesonai(self):
        # self.testing = True

        self.dicodi = {
            "tribe"   : [],
            "group"   : []
        }
        self.sync()

        self.tagesi = ""

        self.comali = []
        self.adcoli = [ Confi.siget("bin/stringtie") ]
        self.admgli = [ "--merge" ]
        self.adotli = [ "-o" ]
        self.adphli = [ "-p", Confi.siget("run/thread")]
        self.adrfli = [ "-G", Confi.siget("refer/annotate") ]


        self.filasi = "library-stringtie-merge"
        self.libadi = {}
        self.prelogi = Confi.siget("result/log")+"/exp13-stringtie-merge-"

    def actor(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])

        self.head()

        self.tagesi = Confi.siget("result/stringtie")
        self.chkpaf()
        for tibe in tibeli:
            self.comali = []
            self.comali.extend(self.adcoli)

            for gupo in gupoli:
                guposi = ""
                guposi = (
                    Confi.siget("result/stringtie") + "/" +
                    Confi.siget("data/prefix/"+tibe) + "-" + gupo +
                    "-stringtie.gtf"
                )
                self.comali.append(guposi)

            self.comali.extend(self.admgli)
            self.comali.extend(self.adotli)
            self.outusi = (
                Confi.siget("result/stringtie") + "/" +
                Confi.siget("data/prefix/"+tibe) + "-" + "-".join(sorted(gupoli)) +"-stringtie-merged.gtf"
            )
            self.comali.append(self.outusi)
            self.comali.extend(self.adphli)
            self.comali.extend(self.adrfli)

            self.ranni()
        self.endin()
