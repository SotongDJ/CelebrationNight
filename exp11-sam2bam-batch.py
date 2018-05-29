#!/usr/bin/env python3
import librun, libconfig, sys
global helber
helber="""
   --- README of exp11-sam2bam-batch ---
  Title:
    Batch Processing for SAM to BAM conversion

  Usage:
    python exp11-stringtie-batch -t <TRIBE> -g <GROUP,GROUP,GROUP...>

  Data Structure:
    First : tribe,
        e.g. raw, untrim, trimmed...
    Second: group,
        e.g. control, A, B, 1, 2...
    Third : subgroup/files,
        e.g. foward, reverse, pair, unpair

    Visualise graph: explanation01-dataStructure.svg

  Original command:
    samtools view -o [out.bam] -Su [in.sam]
    samtools sort -o [out-sorted.bam] [in.bam]

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

        self.dicodi = {
            "tribe" : [],
            "group" : [],
            "method" : []
        }
        self.sync()

        self.tagesi = ""

        self.becoli = ["samtools","view","-o"]
        self.beinli = ["-Su"]

        self.cecoli = ["samtools","sort","-o"]

        self.lscoli = ["ls", "-alFh"]
        self.rmcoli = ["rm", "-v"]

        self.filasi = "exp11-sam2bam-batch"
        self.libadi = {}
        self.prelogi = Confi.siget("result/log")+"/exp11-sam2bam-batch-"
        # self.prelogi = "temp/temp-"

    def actor(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])

        self.head()

        self.tagesi = Confi.siget("result/hisat")
        self.chkpaf()
        for tibe in tibeli:
            for gupo in gupoli:
                self.filesi = (
                    Confi.siget("result/hisat") + "/" +
                    Confi.siget("data/prefix/"+tibe) + "-" +
                    gupo
                )

                self.comali = []
                self.comali.extend( self.rmcoli )
                self.comali.append( self.filesi + argvsi + ".bam" )

                self.ranni()

                self.comali = []
                self.comali.extend( self.becoli )
                self.comali.append( self.filesi + argvsi + ".bam" )
                self.comali.extend( self.beinli )
                self.comali.append( self.filesi + argvsi + ".sam" )

                self.ranni()

                self.comali = []
                self.comali.extend( self.cecoli )
                self.comali.append( self.filesi + argvsi + "-sorted" + ".bam" )
                self.comali.append( self.filesi + argvsi + ".bam" )

                self.ranni()

                self.comali = []
                self.comali.extend( self.lscoli )
                self.comali.append( self.filesi + argvsi + ".sam" )
                self.comali.append( self.filesi + argvsi + ".bam" )
                self.comali.append( self.filesi + "sorted" + ".bam" )

                self.ranni()

                self.comali = []
                self.comali.extend( self.rmcoli )
                self.comali.append( self.filesi + argvsi + ".bam" )
                self.comali.append( self.filesi + argvsi + ".sam" )

                self.ranni()

        self.endin()
Runni = loggo()
