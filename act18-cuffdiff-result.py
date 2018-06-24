#!/usr/bin/env python3
import librun, libconfig, libtab, libsnm, libmar
import time, json
global helber
helber="""
--- README of act18-cuffdiff-result.py ---
 Title:
  Batch Processing for StringTie (Summarise)

 Usage:
  python3 act18-cuffdiff-result.py -t <TRIBE> \\
<<<<<<< HEAD:act18-cuffdiff-result.py
    -r [Description JSON file (Act16)]\\
=======
    -r [Description JSON file (Exp16)]\\
>>>>>>> cea885fa61915b43643c8a47a8922db9a5b6c201:act18-cuffdiff-result.py
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
  act18 required libtab, libsnm, libmar
  act18 required result from act17
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
class cuffdiffresult(librun.workflow):
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
        self.filasi = "act18-cuffdiff-result.py"
        self.libadi = {
            "result/cuffdiff" : Confi.siget("result/cuffdiff"),
            "result/cd-result" : Confi.siget("result/cd-result"),
            "data/prefix" : Confi.diget("data/prefix"),
            "target/libsnm" : Confi.diget("target/libsnm"),
            "type/database" : Confi.diget("type/database"),
            "result/log" : Confi.siget("result/log"),
            "libtab/FoldChange" : Confi.liget("libtab/FoldChange"),
        }
        self.prelogi = self.libadi.get("result/log")+"/act18-cufre-"

    def actor(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])
        refesi = self.dicodi.get("refer",[])

        self.head()

        self.tageli = []
        self.tageli.append(self.libadi.get("result/cd-result"))
        self.chkpaf()

        self.frasi = "==========\nStage 1 : Convert TSV/DIFF to JSON\n=========="
        self.printe()

        taboli = []
        for tibe in tibeli:
            for gupo in gupoli:
                socesi = (
                    self.libadi.get("result/cuffdiff") + "/" +
                    self.libadi.get("data/prefix").get(tibe) +
                    gupo + "-Result/gene_exp.diff"
                )
                self.tagesi = socesi
                cetabo = self.chkfal()
                self.tagesi = socesi.replace(".diff",".json")
                jasobo = self.chkfal()

                if cetabo and not jasobo:
                    taboli.append(socesi)

        if taboli != []:
            CoveJos = libtab.tab2json()
            CoveJos.dicodi = { "files" : taboli ,"id" : "test_id" }
            CoveJos.filasi = "libtab.tab2json"
            CoveJos.prelogi = self.libadi.get("result/log")+"/act18-cufre-covejos-"
            CoveJos.actor()

        self.frasi = "==========\nStage 2 : Scanning for Variable Parts\n=========="
        self.printe()

        Cudiski = libmar.miksing()
        Cudiski.dicodi = {
            "tribe"   : tibeli,
            "group"   : gupoli,
            "prefix"  : self.libadi.get("result/cuffdiff") + "/",
            "postfix" : "-Result/gene_exp.json",
            "libtab"  : self.libadi.get("libtab/FoldChange")
        }
        Cudiski.prelogi = self.prelogi + "sca-Cudiski-"
        Cudiski.scanning()

        self.frasi = "==========\nStage 3 : Merging\n=========="
        self.printe()

        if tibeli != []:
            tibesi = tibeli[0]

            Cudiski.prelogi = self.prelogi + "fus-Cudiski-"
            Cudiski.fusion()
            Cudiski.resusi = (
                self.libadi.get("result/cd-result") + "/" +
                self.libadi.get("data/prefix").get(tibesi) + "FoldChange.json"
            )
            with open(Cudiski.resusi,"w") as resufi:
                json.dump(Cudiski.resudi,resufi,indent=4,sort_keys=True)
            Cudiski.prelogi = self.prelogi + "ara-Cudiski-"
            Cudiski.arrange()

        if refesi != "" and tibeli != []:
            self.frasi = "==========\nStage 4 : Combine Description from GFF3\n=========="
            self.printe()

            tibesi = tibeli[0]
            tiposi = self.libadi.get("type/database").get(tibesi)

            GeneID = libsnm.geneid()
            GeneID.dicodi = {
                "description" : refesi ,
                "basement" : Cudiski.resusi ,
            }
            tagadi = self.libadi.get("target/libsnm").get(tiposi+"-foldchange")
            GeneID.dicodi.update(tagadi)
            GeneID.filasi = "libsnm.geneid"
            GeneID.prelogi = self.libadi.get("result/log")+"/act18-cufre-geneid-"
            GeneID.actor()

            self.frasi = "==========\nStage 5 : Convert JSON back to TSV/CTAB\n=========="
            self.printe()
        else:
            self.frasi = "==========\nStage 4 : Convert JSON back to TSV/CTAB\n=========="
            self.printe()

        CoveTab = libtab.json2tab()
        CoveTab.filasi = "libtab.json2tab"
        CoveTab.prelogi = self.libadi.get("result/log")+"/act18-cufre-covetab-"
        CoveTab.dicodi = {
            "files" : [Cudiski.resusi],
            "column" : Cudiski.coluli
        }
        CoveTab.actor()

        self.printbr()

        self.endin()

CufRe = cuffdiffresult()
