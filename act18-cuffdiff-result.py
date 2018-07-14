#!/usr/bin/env python3
import libWorkFlow, libConfig, libConvert, libsnm, libmar
import time, json
global helper_msg_block
helper_msg_block="""
--- README of act18-cuffdiff-result.py ---
 Title:
  Batch Processing for StringTie (Summarise)

 Usage:
  python3 act18-cuffdiff-result.py -t <TRIBE> \\
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
  act18 required libConvert, libsnm, libmar
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
ConfigDict = libConfig.config()
class cuffdiffresult(libWorkFlow.workflow):
    def personalize(self):
        # self.testing = True
        self.helper_msg_str = helper_msg_block

        self.requested_argv_dict = {
            "tribe" : [],
            "group" : [],
            "refer" : ""
        }
        self.SynonymDict.input(ConfigDict.get_dict("synom"))
        self.synchornize()

        self.comand_line_list = []
        self.script_name = "act18-cuffdiff-result.py"
        self.requested_config_dict = {
            "result/cuffdiff" : ConfigDict.get_str("result/cuffdiff"),
            "result/cd-result" : ConfigDict.get_str("result/cd-result"),
            "data/prefix" : ConfigDict.get_dict("data/prefix"),
            "target/libsnm" : ConfigDict.get_dict("target/libsnm"),
            "type/database" : ConfigDict.get_dict("type/database"),
            "result/log" : ConfigDict.get_str("result/log"),
            "libconvert/FoldChange" : ConfigDict.get_list("libconvert/FoldChange"),
        }
        self.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act18-cufre-"

    def actor(self):
        tribe_list = self.requested_argv_dict.get("tribe",[])
        group_list = self.requested_argv_dict.get("group",[])
        refesi = self.requested_argv_dict.get("refer",[])

        self.startLog()

        self.target_file_list = []
        self.target_file_list.append(self.requested_config_dict.get("result/cd-result"))
        self.checkPath()

        self.phrase_str = "==========\nStage 1 : Convert TSV/DIFF to JSON\n=========="
        self.printPhrase()

        taboli = []
        for tribe_name in tribe_list:
            for gupo in group_list:
                socesi = (
                    self.requested_config_dict.get("result/cuffdiff") + "/" +
                    self.requested_config_dict.get("data/prefix").get(tribe_name) +
                    gupo + "-Result/gene_exp.diff"
                )
                self.target_file_path = socesi
                cetabo = self.checkFile()
                self.target_file_path = socesi.replace(".diff",".json")
                jasobo = self.checkFile()

                if cetabo and not jasobo:
                    taboli.append(socesi)

        if taboli != []:
            CvtoJSON = libConvert.cvtDSVtoJSON()
            CvtoJSON.requested_argv_dict = { "files" : taboli ,"id" : "test_id" }
            CvtoJSON.filasi = "libConvert.cvtDSVtoJSON"
            CvtoJSON.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act18-cufre-covejos-"
            CvtoJSON.actor()

        self.phrase_str = "==========\nStage 2 : Scanning for Variable Parts\n=========="
        self.printPhrase()

        Cudiski = libmar.miksing()
        Cudiski.requested_argv_dict = {
            "tribe"   : tribe_list,
            "group"   : group_list,
            "prefix"  : self.requested_config_dict.get("result/cuffdiff") + "/",
            "postfix" : "-Result/gene_exp.json",
            "libconvert"  : self.requested_config_dict.get("libconvert/FoldChange")
        }
        Cudiski.log_file_prefix_str = self.log_file_prefix_str + "sca-Cudiski-"
        Cudiski.scanning()

        self.phrase_str = "==========\nStage 3 : Merging\n=========="
        self.printPhrase()

        if tribe_list != []:
            tribe_str = tribe_list[0]

            Cudiski.log_file_prefix_str = self.log_file_prefix_str + "fus-Cudiski-"
            Cudiski.fusion()
            Cudiski.resusi = (
                self.requested_config_dict.get("result/cd-result") + "/" +
                self.requested_config_dict.get("data/prefix").get(tribe_str) + "FoldChange.json"
            )
            with open(Cudiski.resusi,"w") as resufi:
                json.dump(Cudiski.resudi,resufi,indent=4,sort_keys=True)
            Cudiski.log_file_prefix_str = self.log_file_prefix_str + "ara-Cudiski-"
            Cudiski.arrange()

        if refesi != "" and tribe_list != []:
            self.phrase_str = "==========\nStage 4 : Combine Description from GFF3\n=========="
            self.printPhrase()

            tribe_str = tribe_list[0]
            tiposi = self.requested_config_dict.get("type/database").get(tribe_str)

            GeneID = libsnm.geneid()
            GeneID.requested_argv_dict = {
                "description" : refesi ,
                "basement" : Cudiski.resusi ,
            }
            tagadi = self.requested_config_dict.get("target/libsnm").get(tiposi+"-foldchange")
            GeneID.requested_argv_dict.update(tagadi)
            GeneID.filasi = "libsnm.geneid"
            GeneID.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act18-cufre-geneid-"
            GeneID.actor()

            self.phrase_str = "==========\nStage 5 : Convert JSON back to TSV/CTAB\n=========="
            self.printPhrase()
        else:
            self.phrase_str = "==========\nStage 4 : Convert JSON back to TSV/CTAB\n=========="
            self.printPhrase()

        CvtoTAB = libConvert.cvtJSONtoDSV()
        CvtoTAB.filasi = "libConvert.cvtJSONtoDSV"
        CvtoTAB.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act18-cufre-covetab-"
        CvtoTAB.requested_argv_dict = {
            "files" : [Cudiski.resusi],
            "column" : Cudiski.coluli
        }
        CvtoTAB.actor()

        self.printBlankLine()

        self.stopLog()

CufRe = cuffdiffresult()
