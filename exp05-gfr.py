#!/usr/bin/env python3
import json
import librun, libconfig
global helber
helber="""
--- README of exp05-grab-fastqc-result ---
 Title:
  Grab FastQC result and generate related JSON database

 Usage:
  python exp05-gfr -t <TRIBE> -g <GROUP> <GROUP> <GROUP>... \\
    -s <SUBGROUP> <SUBGROUP> <SUBGROUP>...

 Data Structure:
  First : tribe,
    e.g. raw, untrim, trimmed...
  Second: group,
    e.g. control, A, B, 1, 2...
  Third : subgroup/files,
    e.g. foward, reverse, pair, unpair

  Visualise graph: explanation01-dataStructure.svg

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
            "tribe"   : [],
            "group"   : [],
            "subgroup": []
        }
        self.Synom.input(Confi.diget("synom"))
        self.sync()

        self.tagesi = ""

        self.filasi = "exp05-gfr"
        self.libadi = {
            "result/fastqc" : Confi.siget("result/fastqc"),
            "result/gfr" : Confi.siget("result/gfr"),
            "result/log" : Confi.siget("result/log"),
            "data/prefix" : Confi.diget("data/prefix"),
        }
        self.prelogi = self.libadi.get("result/log")+"/exp05-gfr-"

        self.comali = []

    def actor(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])
        suguli = self.dicodi.get("subgroup",[])

        self.head()

        self.resudi = {}
        resusi = self.libadi.get("result/gfr") + "/result.json"

        self.tagesi = self.libadi.get("result/gfr")
        self.chkpaf()

        for tibe in tibeli:
            for gupo in gupoli:
                for sugu in suguli:
                    socesi = (
                        self.libadi.get("result/fastqc") + "/" +
                        self.libadi.get("data/prefix").get(tibe) +
                        gupo + "-" + sugu + "_fastqc/summary.txt"
                    )
                    self.tagesi = socesi
                    if self.chkfal():
                        for lino in open(socesi).read().splitlines():
                            metali = []
                            metali = lino.split("	")

                            recosi = ""
                            catesi = ""
                            falesi = ""
                            recosi,catesi,falesi = metali

                            metadi = {}
                            metadi = self.resudi.get('cate',{})
                            semedi = {}
                            semedi = metadi.get(catesi,{})
                            semedi.update({ falesi : recosi })
                            metadi.update({ catesi : semedi })
                            self.resudi.update({ 'cate' : metadi })

                            metadi = {}
                            metadi = self.resudi.get('fale',{})
                            semedi = {}
                            semedi = metadi.get(falesi,{})
                            semedi.update({ catesi : recosi })
                            metadi.update({ falesi : semedi })
                            self.resudi.update({ 'fale' : metadi })

        with open(resusi,"w") as resufi:
            json.dump(self.resudi,resufi,indent=4,sort_keys=True)

        self.endin()

Runni = loggo()
