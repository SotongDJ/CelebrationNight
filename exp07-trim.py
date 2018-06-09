#!/usr/bin/env python3
import sys, json, pprint, time
from subprocess import call

helber="""
   --- README of exp07-trim ---
 Title:
    Batch Processing for Trimmomatic

 Usage:
    python exp07-trim <TRIBE> <GROUP,GROUP,GROUP...>

 Structure:
    First : tribe,
        e.g. raw, untrim, trimmed...
    Second: group,
        e.g. control, A, B, 1, 2...
    Third : subgroup/files,
        e.g. foward, reverse, pair, unpair

    Visualise graph: explanation01-dataStructure.svg

 Original command:
  java -jar <bin>/trimmomatic-0.35.jar PE -phred33
  -threads <threads> -trimlog <logfile>\
  input_forward.fq.gz input_reverse.fq.gz \
  output_forward_paired.fq.gz output_forward_unpaired.fq.gz \
  output_reverse_paired.fq.gz output_reverse_unpaired.fq.gz \
  ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 LEADING:3 \
  TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36

 CAUTION:
    <GROUP> must separate with space
    <GROUP> don't allowed spacing

   --- README ---
""""""
    command split into [ linoli , linuli , linali ]
 Postfix:
  -si: String
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
            "raw"    : "",
            "Pair"   : "",
            "unPair" : "",
            "group"  : [],
        }
        self.Synom.input(Confi.diget("synom"))
        self.sync()

        self.libadi = {
            "bin/trimmomatic" : Confi.siget("bin/trimmomatic")
            "raw/type"        : Confi.siget("raw/type")
            "run/phred"       : Confi.siget("run/phred")
            "run/thread"      : Confi.siget("run/thread")
            "postfix/forward" : Confi.siget("postfix/forward")
            "postfix/reverse" : Confi.siget("postfix/reverse")
            "trimmo/lead"     : Confi.siget("trimmo/lead")
            "trimmo/trail"    : Confi.siget("trimmo/trail")
            "trimmo/slide"    : Confi.siget("trimmo/slide")
            "trimmo/length"   : Confi.siget("trimmo/length")
            "trimmo/adapter"  : Confi.siget("trimmo/adapter")
            "data/prefix"     : Confi.diget("data/prefix")
            "result/raw"      : Confi.siget("result/raw")
        }

        self.comali = []
        self.adcoli = [
            'java', '-jar', self.libadi.get("bin/trimmomatic"),
            'PE', '-phred'+self.libadi.get("trimmo/phred"),
            '-threads', self.libadi.get("trimmo/thread")
        ]
        self.adpali = []
        self.adpali.append(self.libadi.get("trimmo/lead"))
        self.adpali.append(self.libadi.get("trimmo/trail"))
        self.adpali.append(self.libadi.get("trimmo/slide"))
        self.adpali.append(self.libadi.get("trimmo/length"))
        self.adpali.append(self.libadi.get("trimmo/adapter"))

        self.filasi = "exp07-trim"
        self.prelogi = Confi.siget("result/log")+"/exp07-trim-"

    def actor(self):
        self.gupoli = self.dicodi.get("group" ,[])
        self.rawusi = self.dicodi.get("raw"   ,"")
        self.pairsi = self.dicodi.get("Pair"  ,"")
        self.unpasi = self.dicodi.get("unPair","")

        inrasi = self.libadi.get("result/raw") + "/" + self.rawusi
        otpasi = self.libadi.get("result/raw") + "/" + self.pairsi
        otunsi = self.libadi.get("result/raw") + "/" + self.unpasi
        self.tageli = [ inrasi, otpasi, otunsi ]
        self.chkpaf()

        for gupo in gupoli:
            input_forward = (
                inrasi + "/" +
                self.libadi.get("data/prefix").get(self.rawusi,"") +
                gupo + "-" + self.libadi.get("postfix/forward") +
                "." + self.libadi.get("raw/type")
            )
            input_reverse = (
                inrasi + "/" +
                self.libadi.get("data/prefix").get(self.rawusi,"") +
                gupo + "-" + self.libadi.get("postfix/reverse") +
                "." + self.libadi.get("raw/type")
            )
            output_forward_paired   = (
                otpasi + "/" +
                self.libadi.get("data/prefix").get(self.pairsi,"") +
                gupo + "-" + self.libadi.get("postfix/forward") +
                "." + self.libadi.get("raw/type")
            )
            output_forward_unpaired = (
                otunsi + "/" +
                self.libadi.get("data/prefix").get(self.unpasi,"") +
                gupo + "-" + self.libadi.get("postfix/forward") +
                "." + self.libadi.get("raw/type")
            )
            output_reverse_paired   = (
                otpasi + "/" +
                self.libadi.get("data/prefix").get(self.pairsi,"") +
                gupo + "-" + self.libadi.get("postfix/reverse") +
                "." + self.libadi.get("raw/type")
            )
            output_reverse_unpaired = (
                otunsi + "/" +
                self.libadi.get("data/prefix").get(self.unpasi,"") +
                gupo + "-" + self.libadi.get("postfix/reverse") +
                "." + self.libadi.get("raw/type")
            )

fallisi = fallidi.get(tribesi,{})
for grupo in metali:
    runisi = ""
    comasi = ""
    argudi = {
    "forward":"?",
    "reverse":"?"
    }
    for fale in open(fallisi).read().splitlines():
        for argu in list(argudi.keys()):
            compasi = sugrudi.get(argu,'?')
            if compasi == "?":
                print("Error: fixing config.json required")
                print(" 'var'/'sugru'/'" + argu + "' not exist ")
            elif compasi in fale:
                if grupo in fale:
                    argudi.update({ argu : fale })

    if "?" in list(argudi.values()):
        print("Error: something went wrong")

    fofasi = argudi.get("forward","")
    refasi = argudi.get("reverse","")

    call(["mkdir",resuho + "-pr/"])
    call(["mkdir",resuho + "-un/"])

    linuli = [
        soroho + "/" + tribesi + "/" + fofasi,
        soroho + "/" + tribesi + "/" + refasi,
        resuho + "-pr/" + prepisi + "-" + fofasi,
        resuho + "-un/" + preunsi + "-" + fofasi,
        resuho + "-pr/" + prepisi + "-" + refasi,
        resuho + "-un/" + preunsi + "-" + refasi,
    ]

    arguli = linoli + linuli +linali

    print('\n\nCommand: \n  ' + '  \\\n    '.join(arguli))
    runisi = "\n\nRUN started at " + time.strftime("%Y%m%d%H%M%S")
    comasi = "\nCommand: \n  " + " ".join(arguli)
    with open(logosi,'a') as logofale:
        logofale.write(runisi + comasi)
    call(arguli, stdout=open(logosi, 'a'))
