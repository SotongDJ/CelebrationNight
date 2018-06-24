#!/usr/bin/env python3
import sys, json, pprint, time
import librun,libconfig
from subprocess import call

helber="""
   --- README of act07-trim ---
 Title:
    Batch Processing for Trimmomatic

 Usage:
    python act07-trim \\
        --raw=<TRIBE of Sources> \\
        --pair=<TRIBE for paired seq> \\
        --unpair=<TRIBE for unpaired seq> \\
        -g <GROUP,GROUP,GROUP...>

 Structure:
    First : tribe,
        e.g. raw, untrim, trimmed...
    Second: group,
        e.g. control, A, B, 1, 2...
    Third : subgroup/files,
        e.g. foward, reverse, pair, unpair

    Visualise graph: explanation01-dataStructure.svg

 Original command:
  java -jar <bin>/trimmomatic-0.35.jar PE \\
    -phred33 -threads <threads> \\
    input_forward.fq.gz input_reverse.fq.gz \\
    output_forward_paired.fq.gz output_forward_unpaired.fq.gz \\
    output_reverse_paired.fq.gz output_reverse_unpaired.fq.gz \\
    <ILLUMINACLIP> <LEADING> \\
    <TRAILING> <SLIDINGWINDOW> <MINLEN>

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
class trimmo(librun.workflow):
    def pesonai(self):
        # self.testing = True
        self.helb = helber

        self.dicodi = {
            "raw"    : "",
            "pair"   : "",
            "unpair" : "",
            "group"  : [],
        }
        self.Synom.input(Confi.diget("synom"))
        self.sync()

        self.libadi = {
            "bin/trimmomatic" : Confi.siget("bin/trimmomatic"),
            "raw/type"        : Confi.siget("raw/type"),
            "run/phred"       : Confi.siget("run/phred"),
            "run/thread"      : Confi.siget("run/thread"),
            "postfix/forward" : Confi.siget("postfix/forward"),
            "postfix/reverse" : Confi.siget("postfix/reverse"),
            "trimmo/lead"     : Confi.siget("trimmo/lead"),
            "trimmo/trail"    : Confi.siget("trimmo/trail"),
            "trimmo/slide"    : Confi.siget("trimmo/slide"),
            "trimmo/length"   : Confi.siget("trimmo/length"),
            "trimmo/adapter"  : Confi.siget("trimmo/adapter"),
            "data/prefix"     : Confi.diget("data/prefix"),
            "result/raw"      : Confi.siget("result/raw"),
        }

        self.comali = []
        self.adcoli = [
            'java', '-jar', self.libadi.get("bin/trimmomatic"),
            'PE', '-phred'+self.libadi.get("run/phred"),
            '-threads', self.libadi.get("run/thread")
        ]
        self.adpali = []
        self.adpali.append(self.libadi.get("trimmo/lead"))
        self.adpali.append(self.libadi.get("trimmo/trail"))
        self.adpali.append(self.libadi.get("trimmo/slide"))
        self.adpali.append(self.libadi.get("trimmo/length"))
        self.adpali.append(self.libadi.get("trimmo/adapter"))

        self.filasi = "act07-trim"
        self.prelogi = Confi.siget("result/log")+"/act07-trim-"

    def actor(self):
        self.gupoli = self.dicodi.get("group" ,[])
        self.rawusi = self.dicodi.get("raw"   ,"")
        self.pairsi = self.dicodi.get("pair"  ,"")
        self.unpasi = self.dicodi.get("unpair","")

        self.head()

        inrasi = self.libadi.get("result/raw") + "/" + self.rawusi
        otpasi = self.libadi.get("result/raw") + "/" + self.pairsi
        otunsi = self.libadi.get("result/raw") + "/" + self.unpasi
        self.tageli = [ inrasi, otpasi, otunsi ]
        self.chkpaf()

        if self.rawusi != "" and self.pairsi != "" and self.unpasi != "":
            for gupo in self.gupoli:
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

                self.comali = []
                self.comali.extend(self.adcoli)
                self.comali.append(input_forward)
                self.comali.append(input_reverse)
                self.comali.append(output_forward_paired)
                self.comali.append(output_forward_unpaired)
                self.comali.append(output_reverse_paired)
                self.comali.append(output_reverse_unpaired)
                self.comali.extend(self.adpali)

                self.runit()

            self.endin()

Trimmo = trimmo()
