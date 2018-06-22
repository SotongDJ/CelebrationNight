#!/usr/bin/env python3
import librun, libconfig, libtab
import time, json, pprint
global helber
helber="""
  --- README of library-gff-extract.py ---
 Title:
  Library for GFF information extraction

 Usage:
  import libgext
  Gekta = libgext.gffextract()
  Gekta.testing = self.testing
  Gekta.prelogi = < Log File Path>
  Gekta.dicodi = {
    "input"  : <GFF file>
    "tribe"  : <tribe>
    "output" : <OUTPUT JSON file name>
  }
  Gekta.actor()

 CAUTION:
  libgext required libtab

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
class gffextract(librun.workflow):
    def redirek(self):
        """"""
    def pesonai(self):
        # self.testing = True
        self.helb = helber

        self.dicodi = {
            "input"  : [],
            "output" : "",
            "tribe"  : "",
        }

        self.comali = []
        self.filasi = "library-gff-extract.py"
        self.libadi = {
            "result/stringtie" : Confi.siget("result/stringtie"),
            "result/ge"        : Confi.siget("result/ge"),
            "target/extract"   : Confi.diget("target/extract")
        }
        self.prelogi = Confi.siget("result/log")+"/libgext-"

    def actor(self):
        self.inpuli = self.dicodi.get("input",[])
        self.oupusi = self.libadi.get("result/ge") + "/" +self.dicodi.get("output","")
        self.colusi = self.libadi.get("target/extract").get(self.dicodi.get("tribe",""))

        self.head()

        self.tageli = []
        self.tageli.append(self.libadi.get("result/stringtie"))
        self.tageli.append(self.libadi.get("result/ge"))
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
            elif metali[-1] in ["ctab","tsv","diff","tab"]:
                setosi = metali.pop(-1)
                self.oupusi = ".".join(metali).replace("."+setosi,".json")
            else:
                metasi = metali.pop(-1)
                setosi = "json"
                self.oupusi = ".".join(metali).replace("."+metasi,".json")
        else:
            setosi = "json"
            self.oupusi = self.oupusi +".json"

        self.refesi = self.oupusi.replace(".json","-refer.json")
        self.valesi = self.oupusi.replace(".json","-value.json")
        self.desisi = self.oupusi.replace(".json","-"+self.colusi+".json")

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
