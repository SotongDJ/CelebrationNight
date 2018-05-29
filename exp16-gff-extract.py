#!/usr/bin/env python3
import librun, libconfig, libtab
import time, json, pprint
global helber
helber="""
   --- README of exp16-gff-extract.py ---
  Title:
    Batch Processing for StringTie

  Usage:
    python3 exp16-gff-extract.py -i <GFF files> -o <OUTPUT JSON file>

  CAUTION:
    Exp16 required libtab

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

        self.dicodi = {
            "input"   : [],
            "output"   : "",
        }
        self.Synom.input(Confi.diget("synom"))
        self.sync()

        self.tagesi = ""

        self.comali = []
        self.filasi = "exp15-stringtie-result"
        self.libadi = {}
        self.prelogi = Confi.siget("result/log")+"/exp15-sr-"

    def actor(self):
        self.inpuli = self.dicodi.get("input",[])
        self.oupusi = self.dicodi.get("output","")
        self.refesi = self.oupusi.replace(".json","-refer.json")
        self.valesi = self.oupusi.replace(".json","-value.json")
        self.desisi = self.oupusi.replace(".json","-description.json")

        self.head()

        self.tagesi = Confi.siget("result/stringtie")
        self.chkpaf()

        self.printbr()
        self.frasi = "==========\nStage 1 : Convert GFF(v3) to JSON\n=========="
        self.printe()

        comusi = (
            "sequence	source	feature	start	end	"+
            "score	srefed	phase	Attributes"
        )

        CoveJos = libtab.tab2json()
        CoveJos.dicodi = { "files" : self.inpuli ,"id" : "" ,"column":comusi}
        CoveJos.actor()

        self.printbr()
        self.frasi = "==========\nStage 2 : Grab Attributes from JSON\n=========="
        self.printe()

        self.socedi = dict()
        for inpu in self.inpuli:
            metali = inpu.split(".")
            metali[-1] = "json"
            resusi = ".".join(metali)
            remasi = resusi.replace(".json","-column.json")
            filafi = open(remasi,"r")
            filaso = json.load(filafi)
            self.socedi.update(filaso.get("Attributes",{}))

        self.frasi = pprint.pformat(( len(self.socedi)))
        self.printimo()

        self.printbr()
        self.frasi = "==========\nStage 3 : Extract Attributes into Dictionaries\n=========="
        self.printe()

        self.refedi = {}
        self.valedi = {}
        for reco in list(self.socedi.keys()):
            metali = []
            metali = reco.split(";")
            numeli = self.socedi.get(reco)
            namasi = ""
            for meta in metali:
                if "ID=" in meta:
                    namasi = meta.split("=")[1]
                    self.refedi.update({ namasi : reco })
                    self.valedi.update({ namasi : numeli })
                elif "Name=" in meta:
                    namasi = meta.split("=")[1]
                    self.refedi.update({ namasi : reco })
                    self.valedi.update({ namasi : numeli })

        self.frasi = pprint.pformat(( len(self.refedi) , len(self.valedi) ))
        self.printimo()

        self.printbr()
        self.frasi = "==========\nStage 4 : Generate Refer. Dictionary for Result\n=========="
        self.printe()

        self.resudi = {}
        self.desidi = {}

        for nama in list(self.refedi.keys()):
            refesi = self.refedi.get(nama)
            refeli = refesi.replace("=",";").split(";")
            keyosi = ""
            valusi = ""
            for n in range(len(refeli)):
                if "_id" in refeli[n]:
                    metadi = self.resudi.get(refeli[n],{})
                    keyosi = refeli[n]
                    valusi = refeli[n+1]
                    metadi.update({  valusi : refesi })
                    self.resudi.update({ keyosi : metadi })

            for n in range(len(refeli)):
                if refeli[n] == "description" and keyosi != "" and valusi != "":
                    metadi = self.desidi.get(keyosi,{})
                    metadi.update({  valusi : refeli[n+1] })
                    self.desidi.update({ keyosi : metadi })

        self.frasi = pprint.pformat( list(self.resudi.keys()) )
        self.printimo()

        self.frasi = pprint.pformat( list(self.desidi.keys()) )
        self.printimo()

        self.printbr()
        self.frasi = "==========\nStage 5 : Export Dictionaries into JSON\n=========="
        self.printe()

        setosi = "json"
        if "." in self.oupusi:
            metali = []
            metali = self.oupusi.split(".")
            if metali[-1] == "json":
                setosi = metali.pop(-1)
            elif metali[-1] in ["ctab","tsv"]:
                setosi = metali.pop(-1)
                self.oupusi = setosi.replace("."+setosi,".json")
            else:
                metasi = metali.pop(-1)
                setosi = "json"
                self.oupusi = setosi.replace("."+metasi,".json")
        else:
            setosi = "json"
            self.oupusi = setosi+".json"

        with open(self.refesi,"w") as refefi:
            json.dump(self.refedi,refefi,indent=4,sort_keys=True)

        with open(self.valesi,"w") as valefi:
            json.dump(self.valedi,valefi,indent=4,sort_keys=True)

        with open(self.desisi,"w") as desifi:
            json.dump(self.desidi,desifi,indent=4,sort_keys=True)

        with open(self.oupusi,"w") as oupufi:
            json.dump(self.resudi,oupufi,indent=4,sort_keys=True)

        if setosi != "json":
            self.printbr()
            self.frasi = "==========\nStage 6 : Convert JSON back to TSV/CTAB\n=========="
            self.printe()

            CoveTab = libtab.json2tab()
            CoveTab.dicodi = { "files" : [self.oupusi] }
            CoveTab.actor()

        self.endin()

Runni = loggo()
