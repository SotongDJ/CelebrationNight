#!/usr/bin/env python3
import librun, libconfig
import time, json, random
global helber
helber="""
--- README of library-mix-analysis-result.py ---
 Title:
  Library for Mixing analysis result

 Usage: # Replace * with related string
    Miski = libmar.miksing()
    Miski.dicodi = {
      "tribe"   : tibeli,
      "group"   : gupoli,
      "prefix"  : self.libadi.get("result/*") + "/",
      "postfix" : "/*.json", OR "postfix" : "-*.json",
      "libtab"  : self.libadi.get("libtab/*")
    }
    Miski.prelogi = self.prelogi + "Miski-"
    Miski.scanning()

    Miski.fusion()
    Miski.resusi = (
        self.libadi.get("result/*") + "/" +
        self.libadi.get("data/prefix").get(tibe) + "*.json"
    )
    with open(Miski.resusi,"w") as resufi:
        json.dump(Miski.resudi,resufi,indent=4,sort_keys=True)
    Miski.arrange()

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
            "libtab"  : []
        }

        self.comali = []
        self.libadi = {
            "data/prefix" : Confi.diget("data/prefix"),
            "result/log" : Confi.siget("result/log"),
        }
        self.filasi = "libmar"
        self.prelogi = Confi.siget("result/log")+"/libmar-"

        self.resusi = ""

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
            keyoli = []
            for gupo in gupoli:
                socesi = (
                    pifisi +
                    self.libadi.get("data/prefix").get(tibe) + gupo +
                    pofisi
                )
                socefi = open(socesi,"r")
                soceso = json.load(socefi)

                numein = 0
                if keyoli == []:
                    keyoli = list(soceso.keys())
                """
                if keyoli == []:
                    if len(list(soceso.keys())) >= 20:
                        keyoli = random.sample(list(soceso.keys()), 20)
                    else:
                        keyoli = list(soceso.keys())
                """

                if self.refedi == {}:
                    for id in keyoli:
                        admedi = soceso.get(id)
                        bamedi = {}
                        for colu in list(soceso.get(id).keys()):
                            basi = admedi.get(colu)
                            bamedi.update({ colu : basi})
                            self.refedi.update({ id : bamedi})
                else:
                    for id in keyoli:
                        admedi = soceso.get(id)
                        bamedi = self.refedi.get(id)
                        for colu in list(soceso.get(id).keys()):
                            adsi = admedi.get(colu)
                            basi = bamedi.get(colu)
                            if adsi == basi and not self.tunodi.get(colu,False):
                                self.tunodi.update({ colu : False })
                            else:
                                self.tunodi.update({ colu : True })
        self.endin()

    def fusion(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])
        pifisi = self.dicodi.get("prefix",[])
        pofisi = self.dicodi.get("postfix",[])

        self.filasi = "fusion from libmar"
        self.head()

        self.coludi = {}
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

                            comeli = self.coludi.get(colu,[])
                            if colu+"("+gupo+")" not in comeli:
                                comeli.append(colu+"("+gupo+")")
                                self.coludi.update({ colu : comeli })
                            comeli = []

                        elif remedi.get(colu,"") == "":
                            remedi.update({ colu : somedi.get(colu) })
                    self.resudi.update({ id : remedi })
        self.endin()

    def arrange(self):
        self.filasi = "arrange from libmar"
        self.head()

        self.coluli = []
        litali = self.dicodi.get("libtab",[])
        if litali == []:
            litali = list(self.tunodi.keys())
        litasi = "*@*"+"*@*".join(litali)+"*@*"
        for colu in list(self.coludi.keys()):
            if "*@*"+colu+"*@*" in litasi:
                metasi = "*@*".join(self.coludi.get(colu))
                litasi = litasi.replace("*@*"+colu+"*@*","*@*"+metasi+"*@*")
        litasi = litasi[3:len(litasi)-3]
        self.coluli = litasi.split("*@*")
        print(list(self.tunodi.keys()))
        print(list(self.coludi.keys()))
        print(self.coluli)
        self.endin()
