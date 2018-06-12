#!/usr/bin/env python3
import librun, libconfig, libtab, libsnm
import time, json
global helber
helber="""
--- README of library-mix-analysis-result.py ---
 Title:
  Library for Mixing analysis result

 Usage:

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
class miksing(librun.workflow):
    def redirek(self):
        """"""
    def pesonai(self):
        # self.testing = True
        self.helb = helber

        self.dicodi = {
            "tribe"   : [],
            "group"   : [],
            "prefix"  : "",
            "postfix" : "",
        }

        self.comali = []
        self.libadi = {
            "data/prefix" : Confi.diget("data/prefix"),
            "result/log" : Confi.siget("result/log"),
        }
        self.prelogi = Confi.siget("result/log")+"/libmar-"

        self.result = {}

    def scanning(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])
        pifisi = self.dicodi.get("prefix",[])
        pofisi = self.dicodi.get("postfix",[])

        self.filasi = "scanning from libmar"
        self.head()

        self.tunodi = {}
        self.refedi = {}
        for tibe in tibeli:
            for gupo in gupoli:
                socesi = (
                    pifisi +
                    self.libadi.get("data/prefix").get(tibe) + gupo +
                    pofisi
                )
                socefi = open(socesi,"r")
                soceso = json.load(socefi)

                numein = 0
                if self.refedi == {}:
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
                else:
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
        self.endin()

    def fusion(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])

        self.filasi = "scanning from libmar"
        self.head()

        self.resudi = {}
        for tibe in tibeli:
            for gupo in gupoli:
                socesi = (
                    pifisi +
                    self.libadi.get("data/prefix").get(tibe) + gupo +
                    pofisi
                )
                socefi = open(socesi,"r")
                soceso = json.load(socefi)

                for id in list(soceso.keys()):
                    somedi = soceso.get(id)
                    remedi = self.resudi.get(id,{})
                    for colu in list(somedi.keys()):
                        if self.tunodi.get(colu,False):
                            remedi.update({ colu+"("+gupo+")" : somedi.get(colu) })
                        elif remedi.get(colu,"") == "":
                            remedi.update({ colu : somedi.get(colu) })
                    self.resudi.update({ id : remedi })
        self.endin()
