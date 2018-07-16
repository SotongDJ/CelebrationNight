#!/usr/bin/env python3
import json, time
import pyWorkFlow, libConfig
global helper_msg_block
helper_msg_block="""
--- README of act06-fastqc-result-summary ---
 Title:
  FastQC result summary generator

 Usage:
  python act06-frs -t <TRIBE> -g <GROUP> <GROUP> <GROUP>... \\
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
ConfigDict = libConfig.config()
class fasresum(pyWorkFlow.workflow):
    def personalize(self):
        # self.testing = True
        self.helper_msg_str = helper_msg_block

        self.requested_argv_dict = {
            "tribe"   : [],
            "group"   : [],
            "subgroup": []
        }
        self.SynonymDict.input(ConfigDict.get_dict("synom"))
        self.synchornize()

        self.target_file_path = ""

        self.script_name = "act05-gfr"
        self.requested_config_dict = {
            "result/fastqc" : ConfigDict.get_str("result/fastqc"),
            "result/gfr" : ConfigDict.get_str("result/gfr"),
            "result/log" : ConfigDict.get_str("result/log"),
            "data/prefix" : ConfigDict.get_dict("data/prefix"),
            "raw/type" : ConfigDict.get_dict("raw/type"),
            "header/fastqc" : ConfigDict.get_list("header/fastqc"),
        }
        self.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act05-gfr-"

        self.comand_line_list = []

        pnglibfa = open('act06-fsp-png-template.json','r')
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
        tribe_list = self.requested_argv_dict.get("tribe",[])
        group_list = self.requested_argv_dict.get("group",[])
        suguli = self.requested_argv_dict.get("subgroup",[])

        self.startLog()

        self.phrase_str = "==========\nStage 1 : Grab info. from the fastqc results\n=========="
        self.printPhrase()

        self.resudi = {}
        self.resusi = self.requested_config_dict.get("result/gfr") + "/result."

        self.target_file_path = self.requested_config_dict.get("result/gfr")
        self.checkPath()

        for tribe_name in tribe_list:
            for gupo in group_list:
                for sugu in suguli:
                    socesi = (
                        self.requested_config_dict.get("result/fastqc") + "/" +
                        self.requested_config_dict.get("data/prefix").get(tribe_name) +
                        gupo + "-" + sugu + "_fastqc/summary.txt"
                    )
                    self.target_file_path = socesi
                    if self.checkFile():
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

        self.phrase_str = "==========\nStage 2 : Generate HTML\n=========="
        self.printPhrase()
        with open(self.resusi+"json","w") as resufi:
            json.dump(self.resudi,resufi,indent=4,sort_keys=True)

        with open(self.resusi+"html","w") as resufi:
            resufi.write(self.headsi)

            rowlitu = tuple(self.requested_config_dict.get("header/fastqc"))
            for gupo in group_list:
                tribetu = tuple(tribe_list)
                metasi = ""
                metasi = "<table>\n    <caption><h2>" + gupo + "</h2></caption>\n"
                resufi.write(metasi)

                filali = []
                metasi = "    <tr>\n        <th>Types</th>\n"
                resufi.write(metasi)

                for tribe_name in tribetu:

                    colspan = len(suguli)
                    if colspan > 1:
                        metasi = "        <th colspan=\"" + str(colspan) + "\">" + tribe_name + "</th>\n"
                    else:
                        metasi = "        <th>" + tribe_name + "</th>\n"
                    resufi.write(metasi)

                    for sugu in suguli:
                        inpusi = (
                            self.requested_config_dict.get("data/prefix").get(tribe_name)  +
                            gupo + "-" + sugu + "." + self.requested_config_dict.get("raw/type")
                        )
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
        self.stopLog()

FaReS = fasresum()
