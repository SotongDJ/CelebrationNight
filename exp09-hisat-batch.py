#!/usr/bin/env python3
import librun, libconfig, sys
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
    <GROUP> must separate with comma
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
        self.dicodi = {
            "tribe"   : [],
            "group"   : [],
            "argv" : []
        }
        self.sync()

        self.tagesi = ""

        self.adcoli = ["hisat2","-q"]
        self.becoli = ["--phred"+Confi.get("run/phred")]
        self.cecoli = ["-p",Confi.get("run/thread")]
        self.decoli = ["-x",Confi.getpaf(["result/hisat", "idx/genome"])]
        self.edcoli = ["-1"]
        self.gecoli = ["-2"]
        self.idcoli = ["-S"]

        self.libadi = {}

        self.filasi = "exp09-hisat-batch.py"

        self.comali = []

        self.prelogi = Confi.get("result/log")+"/exp09-hisat-batch-"

Runni = loggo()

tibeli = Runni.dicodi.get("tribe",[])
gupoli = Runni.dicodi.get("group",[])
argvli = Runni.dicodi.get("argv",[])

stinbo = false
pofidi = {0:[]}
argvdi = {0:""}
timein = 0
timoli = [0]
for argv in argvli:

    if argv == "stringtie":
        if timein != 0:
            timoli.append(timein)
        pofidi.update({ timein : ["--dta"] })
        argvdi.update({ timein : "-stringtie" })
        stinbo = True
        timein = timein + 1
    elif argv == "cufflinks":
        if timein != 0:
            timoli.append(timein)
        pofidi.update({ timein : ["--dta-cufflinks"] })
        argvdi.update({ timein : "-cufflinks" })
        timein = timein + 1

Runni.hedda()
for tibe in tibeli:
    for gupo in gupoli:
        for timo in timoli:
            Runni.comali = []
            Runni.comali.extend(Runni.adcoli)
            pofisi = pofidi.get(timo)
            Runni.comali.extend(pofisi)
            Runni.comali.extend(Runni.becoli)
            Runni.comali.extend(Runni.cecoli)
            Runni.comali.extend(Runni.decoli)
            Runni.comali.extend(Runni.edcoli)

            fecoli = [
                Confi.get("result/raw") + "/" +
                tibe + "/" +
                Confi.get("data/prefix/"+tibe) + "-" +
                gupo + "-" +
                Confi.get("string/postfix/forward") + ".fastq"
            ]

            Runni.comali.extend(fecoli)
            Runni.comali.extend(Runni.gecoli)

            hecoli = [
                Confi.get("result/raw") + "/" +
                tibe + "/" +
                Confi.get("data/prefix/"+tibe) + "-" +
                gupo + "-" +
                Confi.get("string/postfix/reverse") + ".fastq"
            ]

            Runni.comali.extend(hecoli)
            Runni.comali.extend(Runni.idcoli)

            argvsi = argvdi.get(timo)
            jecoli = [
                Confi.get("result/hisat") + "/" +
                Confi.get("data/prefix/"+tibe) + "-" +
                gupo + argvsi + ".sam"
            ]

            Runni.comali.extend(jecoli)

            Runni.tagesi = Confi.get("result/hisat")
            Runni.chkpaf()

            # Runni.test()
            Runni.ranni()

            if stinbo:
                Runni.comali = []
Runni.calti()
