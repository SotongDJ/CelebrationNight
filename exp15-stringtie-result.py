#!/usr/bin/env python3
import librun, libconfig, libtab, libsnm, libmar
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
class stitieresult(librun.workflow):
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
            "libtab/TranscriptExpression" : Confi.liget("libtab/TranscriptExpression"),
            "libtab/GeneExpression" : Confi.liget("libtab/GeneExpression"),
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
                    self.libadi.get("data/prefix").get(tibe) +
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
                    self.libadi.get("data/prefix").get(tibe) +
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

        Transki = libmar.miksing()
        Transki.dicodi = {
            "tribe"   : tibeli,
            "group"   : gupoli,
            "prefix"  : self.libadi.get("result/ballgown") + "/",
            "postfix" : "/t_data.json",
            "libtab"  : self.libadi.get("libtab/TranscriptExpression")
        }
        Transki.prelogi = self.prelogi + "Transki-"
        Transki.scanning()

        Geniski = libmar.miksing()
        Geniski.dicodi = {
            "tribe"   : tibeli,
            "group"   : gupoli,
            "prefix"  : self.libadi.get("result/stringtie") + "/",
            "postfix" : "-gene.json",
            "libtab"  : self.libadi.get("libtab/GeneExpression")
        }
        Geniski.prelogi = self.prelogi + "Geniski-"
        Geniski.scanning()

        self.frasi = "==========\nStage 3 : Merging\n=========="
        self.printe()

        Transki.fusion()
        Transki.resusi = (
            self.libadi.get("result/st-result") + "/" +
            self.libadi.get("data/prefix").get(tibe) + "TranscriptExpression.json"
        )
        with open(Transki.resusi,"w") as resufi:
            json.dump(Transki.resudi,resufi,indent=4,sort_keys=True)
        Transki.arrange()

        Geniski.fusion()
        Geniski.resusi = (
            self.libadi.get("result/st-result") + "/" +
            self.libadi.get("data/prefix").get(tibe) + "GeneExpression.json"
        )
        with open(Geniski.resusi,"w") as resufi:
            json.dump(Geniski.resudi,resufi,indent=4,sort_keys=True)
        Geniski.arrange()

        if refesi != "":
            self.frasi = "==========\nStage 4 : Combine Description from GFF3\n=========="
            self.printe()

            GeneID = libsnm.geneid()
            GeneID.dicodi = {
                "description" : refesi ,
                "basement" : Transki.resusi ,
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
                "basement" : Geniski.resusi ,
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
            "files" : [Transki.resusi],
            "column" : Transki.coluli
        }
        CoveTab.actor()

        CoveTab.dicodi = {
            "files" : [Geniski.resusi],
            "column" : Geniski.coluli
        }
        CoveTab.actor()

        self.printbr()

        self.endin()

StiRes = stitieresult()
