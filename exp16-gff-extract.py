#!/usr/bin/env python3
import librun, libconfig, libtab
import time, json
global helber
helber="""
   --- README of exp16-gff-extract.py ---
  Title:
    Batch Processing for StringTie

  Usage:
    python3 exp16-gff-extract.py -i <GFF files> -o <OUTPUT JSON file>

  CAUTION:
    Exp16 required libtab
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
            "input"   : [],
            "output"   : "",
        }
        self.sync()

        self.tagesi = ""

        self.comali = []
        self.filasi = "exp15-stringtie-result"
        self.libadi = {}
        self.prelogi = Confi.get("result/log")+"/exp15-sr-"

    def actor(self):
        inpuli = self.dicodi.get("input",[])
        oupusi = self.dicodi.get("output","")

        self.hedda()

        self.tagesi = Confi.get("result/stringtie")
        self.chkpaf()

        self.frasi = "Stage 1 : Convert GFF(v3) to JSON"
        self.printe()

        comusi = (
            "sequence	source	feature	start	end	"+
            "score	strand	phase	Attributes"
        )

        CoveJos = covejos()
        CoveJos.dicodi = { "files" : inpuli ,"id" : "" ,"column":comusi}
        CoveJos.actor()

        self.frasi = "Stage 2 : Grab Attributes from JSON"
        self.printe()

        self.socese = set()
        for inpu in inpuli:
            filafi = open(inpu.split(".")[0]+"-column.json","r")
            filaso = json.load(filafi)
            self.socese.update(set(filaso.get("Attributes",{}).keys()))

        self.frasi = "Stage 3 : Extract Attributes into Dictionaries"
        self.printe()

        self.frasi = "Stage 4 : Export Dictionaries into JSON"
        self.printe()

        """
        self.frasi = "Stage 5 : Convert JSON back to TSV/CTAB"
        self.printe()


        CoveTab = covetab()
        CoveTab.dicodi = { "files" : [resusi] }
        CoveTab.actor()
        """
        self.calti()

Runni = loggo()
