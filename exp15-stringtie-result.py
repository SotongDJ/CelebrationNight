#!/usr/bin/env python3
import librun, libconfig, libtab, libsnm
import time, json
global helber
helber="""
   --- README of exp15-stringtie-result.py ---
  Title:
    Batch Processing for StringTie (Summarise)

  Usage:
    python3 exp15-stringtie-result.py -t <TRIBE> \
        -r [Description JSON file (Exp16)]\
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
class covejos(libtab.tab2json):
    def redirek(self):
        """"""
class covetab(libtab.json2tab):
    def redirek(self):
        """"""
class geneid(libsnm.geneid):
    def redirek(self):
        """"""
Confi = libconfig.confi()
class loggo(librun.loggi):
    def pesonai(self):
        # self.testing = True

        self.dicodi = {
            "tribe" : [],
            "group" : [],
            "refer" : ""
        }
        self.sync()

        self.tagesi = ""

        self.comali = []
        self.filasi = "exp15-stringtie-result"
        self.libadi = {}
        self.prelogi = Confi.siget("result/log")+"/exp15-sr-"

    def actor(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])
        refesi = self.dicodi.get("refer",[])

        self.head()

        self.tagesi = Confi.siget("result/stringtie")
        self.chkpaf()

        self.frasi = "==========\nStage 1 : Convert TSV/CTAB to JSON\n=========="
        self.printe()

        taboli = []
        for tibe in tibeli:
            for gupo in gupoli:
                socesi = (
                    Confi.siget("result/stringtie") + "/" +
                    Confi.siget("data/prefix/"+tibe) + "-" +
                    gupo + "/t_data.ctab"
                )
                self.tagesi = socesi
                cetabo = self.chkfal()
                self.tagesi = socesi.replace(".ctab",".json")
                jasobo = self.chkfal()

                if cetabo and not jasobo:
                    taboli.append(socesi)

        if taboli != []:
            CoveJos = covejos()
            CoveJos.dicodi = { "files" : taboli ,"id" : "t_id" }
            CoveJos.filasi = "libtab.tab2json"
            CoveJos.prelogi = Confi.siget("result/log")+"/exp15-sr-covejos-"
            CoveJos.actor()

        taboli = []
        for tibe in tibeli:
            for gupo in gupoli:
                socesi = (
                    Confi.siget("result/stringtie") + "/" +
                    Confi.siget("data/prefix/"+tibe) + "-" +
                    gupo + "-gene.tsv"
                )
                self.tagesi = socesi
                cetabo = self.chkfal()
                self.tagesi = socesi.replace(".tsv",".json")
                jasobo = self.chkfal()

                if cetabo and not jasobo:
                    taboli.append(socesi)

        if taboli != []:
            CoveJos = covejos()
            CoveJos.dicodi = { "files" : taboli ,"id" : "Gene ID" }
            CoveJos.filasi = "libtab.tab2json"
            CoveJos.prelogi = Confi.siget("result/log")+"/exp15-sr-covejos-"
            CoveJos.actor()

        self.frasi = "==========\nStage 2 : Scanning for Variable Parts\n=========="
        self.printe()

        self.adtunodi = {}
        self.adrefedi = {}
        for tibe in tibeli:
            for gupo in gupoli:
                socesi = (
                    Confi.siget("result/stringtie") + "/" +
                    Confi.siget("data/prefix/"+tibe) + "-" +
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
                    Confi.siget("result/stringtie") + "/" +
                    Confi.siget("data/prefix/"+tibe) + "-" +
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
                    Confi.siget("result/stringtie") + "/" +
                    Confi.siget("data/prefix/"+tibe) + "-" +
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
            Confi.siget("result/stringtie") + "/" +
            Confi.siget("data/prefix/"+tibe) + "-trsp-result.json"
        )
        with open(adresusi,"w") as adresufi:
            json.dump(self.adresudi,adresufi,indent=4,sort_keys=True)

        self.baresudi = {}
        for tibe in tibeli:
            for gupo in gupoli:
                socesi = (
                    Confi.siget("result/stringtie") + "/" +
                    Confi.siget("data/prefix/"+tibe) + "-" +
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
            Confi.siget("result/stringtie") + "/" +
            Confi.siget("data/prefix/"+tibe) + "-gene-result.json"
        )
        with open(baresusi,"w") as baresufi:
            json.dump(self.baresudi,baresufi,indent=4,sort_keys=True)

        if refesi != "":
            self.frasi = "==========\nStage 4 : Combine Description from GFF3\n=========="
            self.printe()

            GeneID = geneid()
            GeneID.dicodi = {
                "description" : refesi ,
                "basement" : adresusi ,
                "if" : "gene_id",
                "key" : "gene:",
                "from" : "gene_id",
                "to" : "Description",
            }
            GeneID.filasi = "libsnm.geneid"
            GeneID.prelogi = Confi.siget("result/log")+"/exp15-sr-geneid-"
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
            GeneID.prelogi = Confi.siget("result/log")+"/exp15-sr-geneid-"
            GeneID.actor()

            self.frasi = "==========\nStage 5 : Convert JSON back to TSV/CTAB\n=========="
            self.printe()
        else:
            self.frasi = "==========\nStage 4 : Convert JSON back to TSV/CTAB\n=========="
            self.printe()

        CoveTab = covetab()
        CoveTab.filasi = "libtab.json2tab"
        CoveTab.prelogi = Confi.siget("result/log")+"/exp15-sr-covetab-"
        CoveTab.dicodi = {
            "files" : [adresusi],
            "column" : Confi.liget("libtab/case1")
        }
        CoveTab.actor()

        CoveTab.dicodi = {
            "files" : [baresusi],
            "column" : Confi.liget("libtab/case2")
        }
        CoveTab.actor()

        self.printbr()

        self.endin()

Runni = loggo()
