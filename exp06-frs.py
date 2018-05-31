#!/usr/bin/env python3
import json, time
import librun, libconfig
global helber
helber="""
--- README of exp06-fastqc-result-summary ---
 Title:
  FastQC result summary generator

 Usage:
  python exp06-frs -t <TRIBE> -g <GROUP> <GROUP> <GROUP>... \\
    -s <SUBGROUP> <SUBGROUP> <SUBGROUP>...

 Data Structure:
  First : tribe,
    e.g. raw, untrim, trimmed...
  Second: group,
    e.g. control, A, B, 1, 2...
  Third : subgroup/files,
    e.g. foward, reverse, pair, unpair

  Visualise graph: explanation01-dataStructure.svg

 CAUTION:
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
            "tribe"   : [],
            "group"   : [],
            "subgroup": []
        }
        self.Synom.input(Confi.diget("synom"))
        self.sync()

        self.tagesi = ""

        self.filasi = "exp05-gfr"
        self.libadi = {
            "result/fastqc" : Confi.siget("result/fastqc"),
            "result/gfr" : Confi.siget("result/gfr"),
            "result/log" : Confi.siget("result/log"),
            "data/prefix" : Confi.diget("data/prefix"),
            "raw/type" : Confi.diget("raw/type"),
            "fql/row" : Confi.liget("fql/row"),
        }
        self.prelogi = self.libadi.get("result/log")+"/exp05-gfr-"

        self.comali = []

        pnglibfa = open('exp06-fsp-png-template.json','r')
        self.pcondi = json.load(pnglibfa)

        self.headsi = """<!DOCTYPE html>
        <html>
        <head>
        <style>
        h2 {
            text-align: center
        }
        table, th, td {
            border: 2px solid black;
            border-collapse: collapse;
            background-color: #EDF7F9;
            margin: auto;
            text-align: center;
        }
        th, td {
            padding: 15px;
        }
        </style>
        </head>
        <body>
        """
        self.endsi = """</body>
        </html>
        """
    def actor(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])
        suguli = self.dicodi.get("subgroup",[])

        self.head()

        self.frasi = "==========\nStage 1 : Grab info. from the fastqc results\n=========="
        self.printe()

        self.resudi = {}
        self.resusi = self.libadi.get("result/gfr") + "/result."

        self.tagesi = self.libadi.get("result/gfr")
        self.chkpaf()

        for tibe in tibeli:
            for gupo in gupoli:
                for sugu in suguli:
                    if self.libadi.get("data/prefix").get(tibe) == "":
                        socesi = (
                            self.libadi.get("result/fastqc") + "/" +
                            gupo + "-" + sugu + "_fastqc/summary.txt"
                        )
                    else:
                        socesi = (
                            self.libadi.get("result/fastqc") + "/" +
                            self.libadi.get("data/prefix").get(tibe) + "-" +
                            gupo + "-" + sugu + "_fastqc/summary.txt"
                        )
                    self.tagesi = socesi
                    if self.chkfal():
                        for lino in open(socesi).read().splitlines():
                            metali = []
                            metali = lino.split("	")

                            recosi = ""
                            catesi = ""
                            falesi = ""
                            recosi,catesi,falesi = metali

                            metadi = {}
                            metadi = self.resudi.get('cate',{})
                            semedi = {}
                            semedi = metadi.get(catesi,{})
                            semedi.update({ falesi : recosi })
                            metadi.update({ catesi : semedi })
                            self.resudi.update({ 'cate' : metadi })

                            metadi = {}
                            metadi = self.resudi.get('fale',{})
                            semedi = {}
                            semedi = metadi.get(falesi,{})
                            semedi.update({ catesi : recosi })
                            metadi.update({ falesi : semedi })
                            self.resudi.update({ 'fale' : metadi })

        self.frasi = "==========\nStage 2 : Generate HTML\n=========="
        self.printe()
        with open(self.resusi+"json","w") as resufi:
            json.dump(self.resudi,resufi,indent=4,sort_keys=True)

        with open(self.resusi+"html","w") as resufi:
            resufi.write(self.headsi)

            rowlitu = tuple(self.libadi.get("fql/row"))
            for gupo in gupoli:
                tibetu = tuple(tibeli)
                metasi = ""
                metasi = "<table>\n    <caption><h2>" + gupo + "</h2></caption>\n"
                resufi.write(metasi)

                filali = []
                metasi = "    <tr>\n        <th>Types</th>\n"
                resufi.write(metasi)

                for tibe in tibetu:

                    colspan = len(suguli)
                    if colspan > 1:
                        metasi = "        <th colspan=\"" + str(colspan) + "\">" + tibe + "</th>\n"
                    else:
                        metasi = "        <th>" + tibe + "</th>\n"
                    resufi.write(metasi)

                    for sugu in suguli:
                        if self.libadi.get("data/prefix").get(tibe) != "":
                            inpusi = (
                                self.libadi.get("data/prefix").get(tibe) + "-" +
                                gupo + "-" + sugu + "." + self.libadi.get("raw/type")
                            )
                        else:
                            inpusi = gupo + "-" + sugu + "." + self.libadi.get("raw/type")
                        filali.append(inpusi)

                metasi = "    </tr>\n"
                resufi.write(metasi)

                filatu = tuple(filali)
                metasi = "    <tr>\n        <th>Files</th>\n"
                resufi.write(metasi)

                for fila in filatu:
                    metasi = "        <th>" + fila + "</th>\n"
                    resufi.write(metasi)

                metasi = "    </tr>\n"
                resufi.write(metasi)

                for rowu in rowlitu:
                    time.sleep(0.01)
                    metasi = "    <tr>\n        <th>" + rowu + "</th>\n"
                    resufi.write(metasi)

                    for fila in filatu:
                        valusi = self.resudi.get("cate").get(rowu,{}).get(fila,'')
                        metasi = "        <td>" + self.pcondi.get(valusi,"") + "</td>\n"
                        resufi.write(metasi)

                    metasi = "    </tr>\n"
                    resufi.write(metasi)

                metasi = "</table>\n<br>"
                resufi.write(metasi)

            resufi.write(self.endsi)
        self.endin()

Runni = loggo()
