#!/usr/bin/env python3
import librun, libconfig, libstm
import sys
global helber
helber="""
   --- README of exp17-stringtie-cuffdiff ---
  Title:
    Batch Processing for StringTie-CuffDiff workflow

  Usage:
    python exp17-sticuf -t <TRIBE> -g <GROUP,GROUP,GROUP...> \\
        --refer=<CODENAME of reference>

  Data Structure:
    First : tribe,
        e.g. raw, untrim, trimmed...
    Second: group,
        e.g. control, A, B, 1, 2...
    Third : subgroup/files,
        e.g. foward, reverse, pair, unpair

    Visualise graph: explanation01-dataStructure.svg

  Original command:
    cuffdiff -o [output folder] -p [thread] \\
      <Merged transcript that created by libstm> \\
      <sample1_hits.sam> <sample2_hits.sam> [... sampleN_hits.sam]

  CAUTION:
   Exp17 required libstm
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
class stiticuffdiff(librun.workflow):
    def pesonai(self):
        # self.testing = True
        self.helb = helber

        self.dicodi = {
            "tribe"   : [],
            "group"   : [],
            "control" : "",
            "refer"   : ""
        }
        self.Synom.input(Confi.diget("synom"))
        self.libadi = {
            "bin/cuffdiff"     : Confi.siget("bin/cuffdiff"),
            "run/thread"       : Confi.siget("run/thread"),
            "data/prefix"      : Confi.diget("data/prefix"),
            "result/stringtie" : Confi.siget("result/stringtie"),
            "result/cuffdiff"  : Confi.siget("result/cuffdiff"),
            "result/hisat"     : Confi.siget("result/hisat"),
            "result/log"       : Confi.siget("result/log"),
        }
        self.sync()

        self.tagesi = ""

        self.comali = []
        self.adcosi = self.libadi.get("bin/cuffdiff")
        self.adlasi = "-L"
        self.adotsi = "-o"
        self.adphli = [ "-p", self.libadi.get("run/thread")]


        self.filasi = "exp17-sticuf"
        self.prelogi = self.libadi.get("result/log")+"/exp17-sticuf-"

    def actor(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])
        cotosi = self.dicodi.get("control","")
        refesi = self.dicodi.get("refer","")

        self.head()

        self.tagesi = self.libadi.get("result/cuffdiff")
        self.chkpaf()
        for tibe in tibeli:
            self.printbr()
            Marge.testing = self.testing
            Marge.prelogi = self.libadi.get("result/log")+"/exp17-StiCuf-Merge-"

            metali = []
            metali.extend(gupoli)
            metali.append(cotosi)
            Marge.dicodi = {
                "tribe" : [tibe],
                "group" : metali,
                "refer" : refesi
            }
            Marge.actor()
            self.printbr()

            self.adrfsi = Marge.outusi
            self.tagesi = self.adrfsi
            self.chkfal()

            if cotosi != "":
                self.cosasi = (
                    self.libadi.get("result/hisat") + "/" +
                    self.libadi.get("data/prefix").get(tibe) +
                    cotosi + "-cufflinks-sorted.bam"
                )
                for gupo in gupoli:
                    adinli = []
                    adinli.append(self.cosasi)
                    adinsi = (
                        self.libadi.get("result/hisat") + "/" +
                        self.libadi.get("data/prefix").get(tibe) +
                        gupo + "-cufflinks-sorted.bam"
                    )
                    adinli.append(adinsi)

                    self.comali = []
                    self.comali.append(self.adcosi)
                    self.comali.append(self.adlasi)
                    self.comali.append(cotosi+","+gupo)
                    self.comali.append(self.adotsi)
                    adotsi = (
                        self.libadi.get("result/cuffdiff") + "/" +
                        self.libadi.get("data/prefix").get(tibe) + gupo + "-Result"
                    )
                    self.comali.append(adotsi)
                    self.comali.extend(self.adphli)
                    self.comali.append(self.adrfsi)
                    self.comali.extend(adinli)

                    self.runit()

        self.endin()

StiCuf = stiticuffdiff()
