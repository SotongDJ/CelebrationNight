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
        eopusi = oupusi.replace(".json","-extra.json")
        reopsi = oupusi.replace(".json","-refer.json")

        self.head()

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

        self.resudi = {}
        self.copedi = {}
        for reco in self.socese:
            metali = reco.split(";")
            idisi = ""
            metadi = {}
            for meta in metali:
                if "Name=" in meta:
                    idisi = meta.split("=")[1]
                    metadi.update({ meta.split("=")[0] : meta.split("=")[1] })
                elif "=" in meta:
                    metadi.update({ meta.split("=")[0] : meta.split("=")[1] })

            metali = []
            metali = list(self.copedi.keys())
            numein = 0
            if idisi != "" and idisi not in metali:
                self.resudi.update({ idisi : metadi })
            elif idisi != "" and idisi in metali:
                self.copedi.update({ str(numein)+"|"+idisi : metadi })
                numein = numein + 1

        print(( len(self.resudi) , len(self.copedi) ))

        self.frasi = "Stage 4 : Generate Refer. Dictionary for Result"
        self.printe()

        self.refedi = {}
        self.ekfedi = {}


        self.frasi = "Stage 5 : Export Dictionaries into JSON"
        self.printe()

        setosi = "json"
        if "." in oupusi:
            metali = []
            metali = oupusi.split(".")
            if metali[-1] == "json":
                setosi = metali.pop(-1)
            elif metali[-1] in ["ctab","tsv"]:
                setosi = metali.pop(-1)
                oupusi = setosi.replace("."+setosi,".json")
            else:
                metasi = metali.pop(-1)
                setosi = "json"
                oupusi = setosi.replace("."+metasi,".json")
        else:
            setosi = "json"
            oupusi = setosi+".json"

        with open(oupusi,"w") as resufi:
            json.dump(self.resudi,resufi,indent=4,sort_keys=True)

        with open(eopusi,"w") as resufi:
            json.dump(self.copedi,resufi,indent=4,sort_keys=True)

        if setosi != "json":
            self.frasi = "Stage 6 : Convert JSON back to TSV/CTAB"
            self.printe()

            CoveTab = covetab()
            CoveTab.dicodi = { "files" : [oupusi] }
            CoveTab.actor()

        self.endin()

Runni = loggo()
