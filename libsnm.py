#!/usr/bin/env python3
import sys, pprint, json
import librun
global helber
helber="""
   --- README of library-search-and-merge ---
  Title:
    Searching and Pairing Tool for Transcript Info. and StringTie Result

  Usage:
    import libsnm


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
class geneid(librun.loggi):

    def pesonai(self):
        # self.testing = True

        self.dicodi = {
            "description" : "" ,
            "basement" : "" ,
            "if" : "",
            "key" : "",
            "to" : "",
        }
        self.sync()

        self.tagesi = ""

        self.comali=[]

        self.filasi = "library-search-and-merge"
        self.libadi = {}
        self.prelogi = "temp/tmp-"

    def actor(self):
        addasi = self.dicodi.get("description","")
        socesi = self.dicodi.get("basement","")
        ifasi = self.dicodi.get("if","")
        keyosi = self.dicodi.get("key","")
        tonsi = self.dicodi.get("to","")

        self.head()

        self.frase = pprint.pformat((addasi, socesi, ifasi, keyosi, tonsi))
        self.printimo()

        addafi = open(addasi,"r")
        addaso = json.load(addafi)

        socefi = open(socesi,"r")
        soceso = json.load(socefi)

        blanbo = False

        if ifasi != "" and keyosi != "" and tonsi != "":
            for id in list(soceso.keys()):
                metadi = soceso.get(id)
                if keyosi in metadi.get(ifasi):
                    refesi = metadi.get(ifasi).replace(keyosi,"")
                    resusi = addaso.get(ifasi).get(refesi,"N/A")
                    metadi.update({ tonsi : resusi })
                    soceso.update({ id : metadi })
                    blanbo = True

        if blanbo:
            with open(socesi,"w") as socefi:
                json.dump(soceso,socefi,indent=4,sort_keys=True)

        self.endin()
