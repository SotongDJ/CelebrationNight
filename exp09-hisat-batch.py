#!/usr/bin/env python3
import librun, libconfig, sys
global helber
helber="""
   --- README of exp09-hisat-batch ---
  Title:
    Batch Processing for HISAT2

  Usage:
    python exp09-hisat-batch [stringtie|cufflinks] -t <TRIBE> -g <GROUP,GROUP,GROUP...>

  Data Structure:
    First : tribe,
        e.g. raw, untrim, trimmed...
    Second: group,
        e.g. control, A, B, 1, 2...
    Third : subgroup/files,
        e.g. foward, reverse, pair, unpair

    Visualise graph: explanation01-dataStructure.svg

  Original command:
    hisat2 -q [--dta/--dta-cufflinks] --phred[33] -p [4]
        -x [prefix of HISAT2-build genome index]
        -1 [forward fastq files of]
        -2 [reverse fastq files of]
        -S [output SAM files]
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
            "tribe" : [],
            "group" : [],
            "index" : "",
            "argv"  : []
        }
        self.Synom.input(Confi.diget("synom"))
        self.sync()
        self.libadi = {
            "bin/hisat2"     : Confi.siget("bin/hisat2")     ,
            "run/phred"      : Confi.siget("run/phred")      ,
            "run/thread"     : Confi.siget("run/thread")     ,
            "index/hisat"    : Confi.siget("index/hisat")    ,
            "result/log"     : Confi.siget("result/log")     ,
            "result/hisat"   : Confi.siget("result/hisat")   ,
            "result/raw"     : Confi.siget("result/raw")     ,
            "data/prefix"    : Confi.diget("data/prefix")    ,
            "postfix/forward": Confi.siget("postfix/forward"),
            "postfix/reverse": Confi.siget("postfix/reverse"),
        }

        self.tagesi = ""

        self.adcoli = [self.libadi.get("bin/hisat2"),"-q"]
        self.adphli = ["--phred"+self.libadi.get("run/phred")]
        self.adthli = ["-p",self.libadi.get("run/thread")]
        self.adgnli = ["-x"]
        self.adh1li = ["-1"]
        self.adh2li = ["-2"]
        self.adrsli = ["-S"]

        self.becoli = ["samtools","view","-o"]
        self.beinli = ["-Su"]

        self.cecoli = ["samtools","sort","-o"]

        self.lscoli = ["ls", "-alFh"]
        self.rmcoli = ["rm", "-v"]


        self.filasi = "exp09-hisat-batch.py"

        self.comali = []

        self.prelogi = self.libadi.get("result/log")+"/exp09-hisat-batch-"

    def actor(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])
        indesi = self.dicodi.get("index","")
        argvli = self.dicodi.get("argv",[])

        self.stinli = [ 0 , False ]
        self.pofidi = {0:[]}
        self.argvdi = {0:""}
        timein = 0
        self.timoli = [0]
        self.jecosi = ""

        if indesi != "" and argvli != []:
            self.indesi =  self.libadi.get("index/hisat") + "/" + indesi
            for argv in argvli:

                if argv == "stringtie":
                    if timein != 0:
                        self.timoli.append(timein)
                    self.stinli = [ timein , True ]
                    self.pofidi.update({ timein : ["--dta"] })
                    self.argvdi.update({ timein : "-stringtie" })
                    timein = timein + 1

                elif argv == "cufflinks":
                    if timein != 0:
                        self.timoli.append(timein)
                    self.pofidi.update({ timein : ["--dta-cufflinks"] })
                    self.argvdi.update({ timein : "-cufflinks" })
                    timein = timein + 1

                if argv == "testing":
                    self.testing = True

            self.head()

            self.tagesi = self.libadi.get("result/hisat")
            self.chkpaf()
            for tibe in tibeli:
                for gupo in gupoli:
                    for timo in self.timoli:
                        self.comali = []
                        self.comali.extend(self.adcoli)

                        pofili = self.pofidi.get(timo)
                        self.comali.extend(pofili)

                        self.comali.extend(self.adphli)
                        self.comali.extend(self.adthli)
                        self.comali.extend(self.adgnli)
                        self.comali.append(self.indesi)
                        self.comali.extend(self.adh1li)

                        fecosi = (
                            self.libadi.get("result/raw") + "/" +
                            tibe + "/" +
                            self.libadi.get("data/prefix").get(tibe) + "-" +
                            gupo + "-" +
                            self.libadi.get("postfix/forward") + ".fastq"
                        )
                        self.comali.append(fecosi)

                        self.comali.extend(self.adh2li)

                        hecosi = (
                            self.libadi.get("result/raw") + "/" +
                            tibe + "/" +
                            self.libadi.get("data/prefix").get(tibe) + "-" +
                            gupo + "-" +
                            self.libadi.get("postfix/reverse") + ".fastq"
                        )
                        self.comali.append(hecosi)

                        self.comali.extend(self.adrsli)

                        argvsi = self.argvdi.get(timo)
                        self.jecosi = (
                            self.libadi.get("result/hisat") + "/" +
                            self.libadi.get("data/prefix").get(tibe) + "-" +
                            gupo
                        )
                        self.comali.append( self.jecosi + argvsi + ".sam" )

                        self.tagesi = self.jecosi + argvsi + ".sam"
                        abanbo = self.chkfal()
                        self.tagesi = self.jecosi + argvsi + "-sorted.bam"
                        bababo = self.chkfal()
                        """
                           sam bam hisat samtool
                            0   0   1     1
                            1   0   0     1
                            0   1   0     0
                            1   1   0     1
                        """
                        if not abanbo and not bababo:
                            self.ranni()

                        if timo == self.stinli[0] and self.stinli[1] and not bababo:
                            self.comali = []
                            self.comali.extend( self.rmcoli )
                            self.comali.append( self.jecosi + argvsi + ".bam" )

                            self.ranni()

                            self.comali = []
                            self.comali.extend( self.becoli )
                            self.comali.append( self.jecosi + argvsi + ".bam" )
                            self.comali.extend( self.beinli )
                            self.comali.append( self.jecosi + argvsi + ".sam" )

                            self.ranni()

                            self.comali = []
                            self.comali.extend( self.cecoli )
                            self.comali.append( self.jecosi + argvsi + "-sorted" + ".bam" )
                            self.comali.append( self.jecosi + argvsi + ".bam" )

                            self.ranni()

                            self.comali = []
                            self.comali.extend( self.lscoli )
                            self.comali.append( self.jecosi + argvsi + ".sam" )
                            self.comali.append( self.jecosi + argvsi + ".bam" )
                            self.comali.append( self.jecosi + argvsi + "sorted" + ".bam" )

                            self.ranni()

                            self.comali = []
                            self.comali.extend( self.rmcoli )
                            self.comali.append( self.jecosi + argvsi + ".bam" )
                            self.comali.append( self.jecosi + argvsi + ".sam" )

                            self.ranni()
            self.endin()

Runni = loggo()
