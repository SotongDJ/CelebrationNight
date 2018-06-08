#!/usr/bin/env python3
import librun, libconfig, libtab, libsnm
import time, json
global helber
helber="""
--- README of exp15-stringtie-result.py ---
 Title:
  Batch Processing for StringTie (Summarise)

 Usage:
  python3 exp15-stringtie-result.py -t <TRIBE> \\
    -r [Description JSON file (Exp16)]\\
    -g <GROUP,GROUP,GROUP...>

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
  Exp15 required result from Exp16
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
            "tribe" : [],
            "group" : [],
            "refer" : ""
        }
        self.Synom.input(Confi.diget("synom"))
        self.sync()

        self.comali = []
        self.filasi = "exp15-stringtie-result"
        self.libadi = {
            "result/stringtie" : Confi.siget("result/stringtie"),
            "result/ballgown" : Confi.siget("result/ballgown"),
            "result/st-result" : Confi.siget("result/st-result"),
            "data/prefix" : Confi.diget("data/prefix"),
            "result/log" : Confi.siget("result/log"),
            "libtab/case1" : Confi.liget("libtab/case1"),
            "libtab/case2" : Confi.liget("libtab/case2"),
        }
        self.prelogi = self.libadi.get("result/log")+"/exp15-sr-"

    def actor(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])
        refesi = self.dicodi.get("refer",[])

        self.head()

        self.tageli = []
        self.tageli.append(self.libadi.get("result/stringtie"))
        self.tageli.append(self.libadi.get("result/ballgown"))
        self.tageli.append(self.libadi.get("result/st-result"))
        self.chkpaf()

        self.frasi = "==========\nStage 1 : Convert TSV/CTAB to JSON\n=========="
        self.printe()

        taboli = []
        for tibe in tibeli:
            for gupo in gupoli:
                socesi = (
                    self.libadi.get("result/ballgown") + "/" +
                    self.libadi.get("data/prefix").get(tibe) + "-" +
                    gupo + "/t_data.ctab"
                )
                self.tagesi = socesi
                cetabo = self.chkfal()
                self.tagesi = socesi.replace(".ctab",".json")
                jasobo = self.chkfal()

                if cetabo and not jasobo:
                    taboli.append(socesi)

        if taboli != []:
            CoveJos = libtab.tab2json()
            CoveJos.dicodi = { "files" : taboli ,"id" : "t_id" }
            CoveJos.filasi = "libtab.tab2json"
            CoveJos.prelogi = self.libadi.get("result/log")+"/exp15-sr-covejos-"
            CoveJos.actor()

        taboli = []
        for tibe in tibeli:
            for gupo in gupoli:
                socesi = (
                    self.libadi.get("result/stringtie") + "/" +
                    self.libadi.get("data/prefix").get(tibe) + "-" +
                    gupo + "-gene.tsv"
                )
                self.tagesi = socesi
                cetabo = self.chkfal()
                self.tagesi = socesi.replace(".tsv",".json")
                jasobo = self.chkfal()

                if cetabo and not jasobo:
                    taboli.append(socesi)

        if taboli != []:
            CoveJos = libtab.tab2json()
            CoveJos.dicodi = { "files" : taboli ,"id" : "Gene ID" }
            CoveJos.filasi = "libtab.tab2json"
            CoveJos.prelogi = self.libadi.get("result/log")+"/exp15-sr-covejos-"
            CoveJos.actor()

        self.frasi = "==========\nStage 2 : Scanning for Variable Parts\n=========="
        self.printe()

        self.adtunodi = {}
        self.adrefedi = {}
        for tibe in tibeli:
            for gupo in gupoli:
                socesi = (
                    self.libadi.get("result/ballgown") + "/" +
                    self.libadi.get("data/prefix").get(tibe) + "-" +
                    gupo + "/t_data.json"
                )
                socefi = open(socesi,"r")
                soceso = json.load(socefi)

                numein = 0
                if self.adrefedi != {}:
                    for id in list(soceso.keys()):
                        admedi = soceso.get(id)
                        bamedi = self.adrefedi.get(id)
                        numein = numein + 1
                        if numein <= 10:
                            for colu in list(soceso.get(id).keys()):
                                adsi = admedi.get(colu)
                                basi = bamedi.get(colu)
                                if adsi == basi:
                                    self.adtunodi.update({ colu : False })
                                else:
                                    self.adtunodi.update({ colu : True })
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

                            self.adrefedi.update({ id : bamedi})
                        else:
                            break
        print(self.adtunodi)

        self.batunodi = {}
        self.barefedi = {}
        for tibe in tibeli:
            for gupo in gupoli:
                socesi = (
                    self.libadi.get("result/stringtie") + "/" +
                    self.libadi.get("data/prefix").get(tibe) + "-" +
                    gupo + "-gene.json"
                )
                socefi = open(socesi,"r")
                soceso = json.load(socefi)

                numein = 0
                if self.barefedi != {}:
                    for id in list(soceso.keys()):
                        admedi = soceso.get(id)
                        bamedi = self.barefedi.get(id)
                        numein = numein + 1
                        if numein <= 10:
                            for colu in list(soceso.get(id).keys()):
                                adsi = admedi.get(colu)
                                basi = bamedi.get(colu)
                                if adsi == basi:
                                    self.batunodi.update({ colu : False })
                                else:
                                    self.batunodi.update({ colu : True })
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

                            self.barefedi.update({ id : bamedi})
                        else:
                            break
        print(self.batunodi)

        self.frasi = "==========\nStage 3 : Merging\n=========="
        self.printe()

        self.adresudi = {}
        for tibe in tibeli:
            for gupo in gupoli:
                socesi = (
                    self.libadi.get("result/ballgown") + "/" +
                    self.libadi.get("data/prefix").get(tibe) + "-" +
                    gupo + "/t_data.json"
                )
                socefi = open(socesi,"r")
                soceso = json.load(socefi)

                numein = 0
                for id in list(soceso.keys()):
                    somedi = soceso.get(id)
                    remedi = self.adresudi.get(id,{})
                    for colu in list(somedi.keys()):
                        if self.adtunodi.get(colu,False):
                            remedi.update({ colu+"("+gupo+")" : somedi.get(colu) })
                        elif remedi.get(colu,"") == "":
                            remedi.update({ colu : somedi.get(colu) })
                    self.adresudi.update({ id : remedi })

        adresusi = (
            self.libadi.get("result/st-result") + "/" +
            self.libadi.get("data/prefix").get(tibe) + "-TranscriptExpression.json"
        )
        with open(adresusi,"w") as adresufi:
            json.dump(self.adresudi,adresufi,indent=4,sort_keys=True)

        self.baresudi = {}
        for tibe in tibeli:
            for gupo in gupoli:
                socesi = (
                    self.libadi.get("result/stringtie") + "/" +
                    self.libadi.get("data/prefix").get(tibe) + "-" +
                    gupo + "-gene.json"
                )
                socefi = open(socesi,"r")
                soceso = json.load(socefi)

                numein = 0
                for id in list(soceso.keys()):
                    somedi = soceso.get(id)
                    remedi = self.baresudi.get(id,{})
                    for colu in list(somedi.keys()):
                        if self.batunodi.get(colu,False):
                            remedi.update({ colu+"("+gupo+")" : somedi.get(colu) })
                        elif remedi.get(colu,"") == "":
                            remedi.update({ colu : somedi.get(colu) })
                    self.baresudi.update({ id : remedi })

        baresusi = (
            self.libadi.get("result/st-result") + "/" +
            self.libadi.get("data/prefix").get(tibe) + "-GeneExpression.json"
        )
        with open(baresusi,"w") as baresufi:
            json.dump(self.baresudi,baresufi,indent=4,sort_keys=True)

        if refesi != "":
            self.frasi = "==========\nStage 4 : Combine Description from GFF3\n=========="
            self.printe()

            GeneID = libsnm.geneid()
            GeneID.dicodi = {
                "description" : refesi ,
                "basement" : adresusi ,
                "if" : "gene_id",
                "key" : "gene:",
                "from" : "gene_id",
                "to" : "Description",
            }
            GeneID.filasi = "libsnm.geneid"
            GeneID.prelogi = self.libadi.get("result/log")+"/exp15-sr-geneid-"
            GeneID.actor()

            GeneID.dicodi = {
                "description" : refesi ,
                "basement" : baresusi ,
                "if" : "Gene ID",
                "key" : "gene:",
                "from" : "gene_id",
                "to" : "Description",
            }
            GeneID.filasi = "libsnm.geneid"
            GeneID.prelogi = self.libadi.get("result/log")+"/exp15-sr-geneid-"
            GeneID.actor()

            self.frasi = "==========\nStage 5 : Convert JSON back to TSV/CTAB\n=========="
            self.printe()
        else:
            self.frasi = "==========\nStage 4 : Convert JSON back to TSV/CTAB\n=========="
            self.printe()

        CoveTab = libtab.json2tab()
        CoveTab.filasi = "libtab.json2tab"
        CoveTab.prelogi = self.libadi.get("result/log")+"/exp15-sr-covetab-"
        CoveTab.dicodi = {
            "files" : [adresusi],
            "column" : self.libadi.get("libtab/case1")
        }
        CoveTab.actor()

        CoveTab.dicodi = {
            "files" : [baresusi],
            "column" : self.libadi.get("libtab/case2")
        }
        CoveTab.actor()

        self.printbr()

        self.endin()

Runni = loggo()
