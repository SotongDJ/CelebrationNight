#!/usr/bin/env python3
import librun, libconfig, libtab
import time, json
global helber
helber="""
   --- README of exp15-stringtie-result.py ---
  Title:
    Batch Processing for StringTie

  Usage:
    python3 exp15-stringtie-result.py -t <TRIBE> --control=<Control Group> -g <GROUP,GROUP,GROUP...>

  Data Structure:
    First : tribe,
        e.g. raw, untrim, trimmed...
    Second: group,
        e.g. control, A, B, 1, 2...
    Third : subgroup/files,
        e.g. foward, reverse, pair, unpair

    Visualise graph: explanation01-dataStructure.svg

  CAUTION:
    Exp15 required libtab
    <GROUP> must separate with space
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
class covejos(libtab.tab2json):
    def redirek(self):
        """"""
class covetab(libtab.json2tab):
    def redirek(self):
        """"""
Confi = libconfig.confi()
class loggo(librun.loggi):
    def pesonai(self):
        # self.testing = True

        self.dicodi = {
            "tribe"   : [],
            "group"   : [],
        }
        self.sync()

        self.tagesi = ""

        self.comali = []
        self.filasi = "exp15-stringtie-result"
        self.libadi = {}
        self.prelogi = Confi.get("result/log")+"/exp15-sr-"

    def actor(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])

        self.hedda()

        self.tagesi = Confi.get("result/stringtie")
        self.chkpaf()

        self.frasi = "Stage 1 : Convert TSV/CTAB to JSON"
        self.printe()

        taboli = []
        for tibe in tibeli:
            for gupo in gupoli:
                socesi = (
                    Confi.get("result/stringtie") + "/" +
                    Confi.get("data/prefix/"+tibe) + "-" +
                    gupo + "/t_data.ctab"
                )
                self.tagesi = socesi
                cetabo = self.chkfal()
                self.tagesi = socesi.replace(".ctab",".json")
                jasobo = self.chkfal()

                if cetabo and not jasobo:
                    taboli.append(socesi)

        CoveJos = covejos()
        CoveJos.dicodi = { "files" : taboli ,"id" : "t_id" }
        CoveJos.actor()

        self.frasi = "Stage 2 : Scanning for Variable Parts"
        self.printe()

        self.tunodi = {}
        self.refedi = {}
        for tibe in tibeli:
            for gupo in gupoli:
                socesi = (
                    Confi.get("result/stringtie") + "/" +
                    Confi.get("data/prefix/"+tibe) + "-" +
                    gupo + "/t_data.json"
                )
                socefi = open(socesi,"r")
                soceso = json.load(socefi)

                numein = 0
                if self.refedi != {}:
                    for id in list(soceso.keys()):
                        admedi = soceso.get(id)
                        bamedi = self.refedi.get(id)
                        numein = numein + 1
                        if numein <= 10:
                            for colu in list(soceso.get(id).keys()):
                                adsi = admedi.get(colu)
                                basi = bamedi.get(colu)
                                if adsi == basi:
                                    self.tunodi.update({ colu : False })
                                else:
                                    self.tunodi.update({ colu : True })
                        else:
                            break
                else:
                    for id in list(soceso.keys()):
                        admedi = soceso.get(id)
                        bamedi = {}
                        numein = numein + 1
                        if numein <= 10:
                            for colu in list(soceso.get(id).keys()):
                                basi = admedi.get(colu)
                                bamedi.update({ colu : basi})

                            self.refedi.update({ id : bamedi})
                        else:
                            break
        print(self.tunodi)

        self.frasi = "Stage 3 : Merging"
        self.printe()

        self.resudi = {}
        for tibe in tibeli:
            for gupo in gupoli:
                socesi = (
                    Confi.get("result/stringtie") + "/" +
                    Confi.get("data/prefix/"+tibe) + "-" +
                    gupo + "/t_data.json"
                )
                socefi = open(socesi,"r")
                soceso = json.load(socefi)

                numein = 0
                for id in list(soceso.keys()):
                    somedi = soceso.get(id)
                    remedi = self.resudi.get(id,{})
                    for colu in list(somedi.keys()):
                        if self.tunodi.get(colu,False):
                            remedi.update({ colu+"("+gupo+")" : somedi.get(colu) })
                        elif remedi.get(colu,"") == "":
                            remedi.update({ colu : somedi.get(colu) })
                    self.resudi.update({ id : remedi })

        resusi = (
            Confi.get("result/stringtie") + "/" +
            Confi.get("data/prefix/"+tibe) + "-result.json"
        )
        with open(resusi,"w") as resufi:
            json.dump(self.resudi,resufi,indent=4,sort_keys=True)

        self.frasi = "Stage 4 : Convert JSON back to TSV/CTAB"
        self.printe()

        CoveTab = covetab()
        CoveTab.dicodi = { "files" : [resusi] }
        CoveTab.actor()

        self.calti()

Runni = loggo()
