#!/usr/bin/env python3
import librun, libconfig, libtab, libsnm, libmar
import time, json
global helber
helber="""
--- README of act15-stringtie-result.py ---
 Title:
  Batch Processing for StringTie (Summarise)

 Usage:
  python3 act15-stringtie-result.py -t <TRIBE> \\
    -r [Description JSON file (Act16)]\\
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
  Act15 required libtab, libsnm, libmar
  Act15 required result from Act16
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
        self.filasi = "act15-stringtie-result"
        self.libadi = {
            "result/stringtie" : Confi.siget("result/stringtie"),
            "result/ballgown" : Confi.siget("result/ballgown"),
            "result/st-result" : Confi.siget("result/st-result"),
            "result/DESeq2" : Confi.siget("result/DESeq2"),
            "bin/prepDE" : Confi.siget("bin/prepDE"),
            "data/prefix" : Confi.diget("data/prefix"),
            "target/libsnm" : Confi.diget("target/libsnm"),
            "type/database" : Confi.diget("type/database"),
            "result/log" : Confi.siget("result/log"),
            "libtab/TranscriptExpression" : Confi.liget("libtab/TranscriptExpression"),
            "libtab/GeneExpression" : Confi.liget("libtab/GeneExpression"),
        }
        self.prelogi = self.libadi.get("result/log")+"/act15-stire-"

    def actor(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])
        refesi = self.dicodi.get("refer",[])

        self.head()

        self.tageli = []
        self.tageli.append(self.libadi.get("result/stringtie"))
        self.tageli.append(self.libadi.get("result/ballgown"))
        self.tageli.append(self.libadi.get("result/st-result"))
        self.tageli.append(self.libadi.get("result/DESeq2"))
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
            CoveJos.prelogi = self.libadi.get("result/log")+"/act15-stire-covejos-"
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
            CoveJos.prelogi = self.libadi.get("result/log")+"/act15-stire-covejos-"
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
        Transki.prelogi = self.prelogi + "sca-Transki-"
        Transki.scanning()

        Geniski = libmar.miksing()
        Geniski.dicodi = {
            "tribe"   : tibeli,
            "group"   : gupoli,
            "prefix"  : self.libadi.get("result/stringtie") + "/",
            "postfix" : "-gene.json",
            "libtab"  : self.libadi.get("libtab/GeneExpression")
        }
        Geniski.prelogi = self.prelogi + "sca-Geniski-"
        Geniski.scanning()

        if tibeli != []:
            tibesi = tibeli[0]

            self.frasi = "==========\nStage 3 : Merging\n=========="
            self.printe()

            Transki.prelogi = self.prelogi + "fus-Transki-"
            Transki.fusion()
            Transki.resusi = (
                self.libadi.get("result/st-result") + "/" +
                self.libadi.get("data/prefix").get(tibesi) + "TranscriptExpression.json"
            )
            with open(Transki.resusi,"w") as resufi:
                json.dump(Transki.resudi,resufi,indent=4,sort_keys=True)
            Transki.prelogi = self.prelogi + "ara-Transki-"
            Transki.arrange()

            Geniski.prelogi = self.prelogi + "fus-Geniski-"
            Geniski.fusion()
            Geniski.resusi = (
                self.libadi.get("result/st-result") + "/" +
                self.libadi.get("data/prefix").get(tibesi) + "GeneExpression.json"
            )
            with open(Geniski.resusi,"w") as resufi:
                json.dump(Geniski.resudi,resufi,indent=4,sort_keys=True)
            Geniski.prelogi = self.prelogi + "ara-Geniski-"
            Geniski.arrange()

        self.frasi = "==========\nStage 4 : Extract Data for DESeq\n=========="
        self.printe()

        filani = self.libadi.get("result/DESeq2") + "/" + "stringtie-list.txt"
        filafi = open(filani,"w")
        filafi.write("")
        filafi.close()

        for tibe in tibeli:
            for gupo in gupoli:
                linosi = (
                    gupo + " " +
                    self.libadi.get("result/ballgown") + "/" +
                    self.libadi.get("data/prefix").get(tibe) +
                    gupo + "-ballgown.gtf" +
                    "\n"
                )

                with open(filani,"a") as filafi:
                    filafi.write(linosi)

        self.comali = [
            "python2", self.libadi.get("bin/prepDE"),
            "-i", filani
        ]
        self.runit()

        self.comali = [
            "mv", "gene_count_matrix.csv", self.libadi.get("result/DESeq2") + "/"
        ]
        self.runit()

        self.comali = [
            "mv", "transcript_count_matrix.csv", self.libadi.get("result/DESeq2") + "/"
        ]
        self.runit()

        self.comali = []

        if refesi != "" and tibeli != []:
            self.frasi = "==========\nStage 5 : Combine Description from GFF3\n=========="
            self.printe()

            tibesi = tibeli[0]
            tiposi = self.libadi.get("type/database").get(tibesi)

            GeneID = libsnm.geneid()
            GeneID.dicodi = {
                "description" : refesi ,
                "basement" : Transki.resusi ,
            }
            tagadi = self.libadi.get("target/libsnm").get(tiposi+"-transcript")
            GeneID.dicodi.update(tagadi)
            GeneID.filasi = "libsnm.geneid"
            GeneID.prelogi = self.libadi.get("result/log")+"/act15-stire-geneid-"
            GeneID.actor()

            GeneID.dicodi = {
                "description" : refesi ,
                "basement" : Geniski.resusi ,
            }
            tagadi = self.libadi.get("target/libsnm").get(tiposi+"-gene")
            GeneID.dicodi.update(tagadi)
            GeneID.filasi = "libsnm.geneid"
            GeneID.prelogi = self.libadi.get("result/log")+"/act15-stire-geneid-"
            GeneID.actor()

            self.frasi = "==========\nStage 6 : Convert JSON back to TSV/CTAB\n=========="
            self.printe()
        else:
            self.frasi = "==========\nStage 5 : Convert JSON back to TSV/CTAB\n=========="
            self.printe()

        CoveTab = libtab.json2tab()
        CoveTab.filasi = "libtab.json2tab"
        CoveTab.prelogi = self.libadi.get("result/log")+"/act15-stire-covetab-"
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

        self.frasi = "\n\n"
        self.printe()

StiRes = stitieresult()
