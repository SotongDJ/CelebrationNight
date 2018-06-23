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
    GeneID = libsnm.geneid()
    GeneID.dicodi = {
        "description" : [file of gene description] ,
        "basement" : [result file] ,
        "if" : [column name of gene id in result file],
        "key" : [header of gene id, "gene:"],
        "from" : [column name of gene id in gene description file],
        "to" : [column name of description],
    }
    # GeneID.dicodi.update()
    GeneID.filasi = "libsnm.geneid"
    GeneID.actor()

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
class geneid(librun.workflow):
    def redirek(self):
        """"""
    def pesonai(self):
        # self.testing = True

        self.dicodi = {
            "description" : "" ,
            "basement" : "" ,
            "if" : "",
            "key" : "",
            "from" : "",
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
        frosi = self.dicodi.get("from","")
        tonsi = self.dicodi.get("to","")

        self.head()

        self.frase = pprint.pformat((addasi, socesi, ifasi, keyosi, tonsi))
        self.printimo()

        addafi = open(addasi,"r")
        addaso = json.load(addafi)

        socefi = open(socesi,"r")
        soceso = json.load(socefi)

        blanbo = False

        if ifasi != "" and tonsi != "":
            for id in list(soceso.keys()):
                metadi = soceso.get(id)
                if keyosi in metadi.get(ifasi):
                    refesi = metadi.get(ifasi).replace(keyosi,"")
                    resusi = addaso.get(frosi).get(refesi,"N/A")
                    metadi.update({ tonsi : resusi })
                    soceso.update({ id : metadi })
                    blanbo = True

        if blanbo:
            with open(socesi,"w") as socefi:
                json.dump(soceso,socefi,indent=4,sort_keys=True)

        self.endin()
