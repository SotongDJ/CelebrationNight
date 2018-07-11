#!/usr/bin/env python3
import libWorkFlow, libconfig, libConvert, libsnm, libmar
import time, json
global helper_msg_block
helper_msg_block="""
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
  Act15 required libConvert, libsnm, libmar
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
ConfigDict = libconfig.config()
class stitieresult(libWorkFlow.workflow):
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
        self.script_name = "act15-stringtie-result"
        self.requested_config_dict = {
            "result/stringtie" : ConfigDict.get_str("result/stringtie"),
            "result/ballgown" : ConfigDict.get_str("result/ballgown"),
            "result/st-result" : ConfigDict.get_str("result/st-result"),
            "result/DESeq2" : ConfigDict.get_str("result/DESeq2"),
            "bin/prepDE" : ConfigDict.get_str("bin/prepDE"),
            "data/prefix" : ConfigDict.get_dict("data/prefix"),
            "target/libsnm" : ConfigDict.get_dict("target/libsnm"),
            "type/database" : ConfigDict.get_dict("type/database"),
            "result/log" : ConfigDict.get_str("result/log"),
            "libconvert/TranscriptExpression" : ConfigDict.get_list("libconvert/TranscriptExpression"),
            "libconvert/GeneExpression" : ConfigDict.get_list("libconvert/GeneExpression"),
        }
        self.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act15-stire-"

    def actor(self):
        tribe_list = self.requested_argv_dict.get("tribe",[])
        group_list = self.requested_argv_dict.get("group",[])
        refesi = self.requested_argv_dict.get("refer",[])

        self.startLog()

        self.target_file_list = []
        self.target_file_list.append(self.requested_config_dict.get("result/stringtie"))
        self.target_file_list.append(self.requested_config_dict.get("result/ballgown"))
        self.target_file_list.append(self.requested_config_dict.get("result/st-result"))
        self.target_file_list.append(self.requested_config_dict.get("result/DESeq2"))
        self.checkPath()

        self.phrase_str = "==========\nStage 1 : Convert TSV/CTAB to JSON\n=========="
        self.printPhrase()

        taboli = []
        for tribe_name in tribe_list:
            for gupo in group_list:
                socesi = (
                    self.requested_config_dict.get("result/ballgown") + "/" +
                    self.requested_config_dict.get("data/prefix").get(tribe_name) +
                    gupo + "/t_data.ctab"
                )
                self.target_file_path = socesi
                cetabo = self.checkFile()
                self.target_file_path = socesi.replace(".ctab",".json")
                jasobo = self.checkFile()

                if cetabo and not jasobo:
                    taboli.append(socesi)

        if taboli != []:
            CvtoJSON = libConvert.cvtDSVtoJSON()
            CvtoJSON.requested_argv_dict = { "files" : taboli ,"id" : "t_id" }
            CvtoJSON.filasi = "libConvert.cvtDSVtoJSON"
            CvtoJSON.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act15-stire-covejos-"
            CvtoJSON.actor()

        taboli = []
        for tribe_name in tribe_list:
            for gupo in group_list:
                socesi = (
                    self.requested_config_dict.get("result/stringtie") + "/" +
                    self.requested_config_dict.get("data/prefix").get(tribe_name) +
                    gupo + "-gene.tsv"
                )
                self.target_file_path = socesi
                cetabo = self.checkFile()
                self.target_file_path = socesi.replace(".tsv",".json")
                jasobo = self.checkFile()

                if cetabo and not jasobo:
                    taboli.append(socesi)

        if taboli != []:
            CvtoJSON = libConvert.cvtDSVtoJSON()
            CvtoJSON.requested_argv_dict = { "files" : taboli ,"id" : "Gene ID" }
            CvtoJSON.filasi = "libConvert.cvtDSVtoJSON"
            CvtoJSON.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act15-stire-covejos-"
            CvtoJSON.actor()

        self.phrase_str = "==========\nStage 2 : Scanning for Variable Parts\n=========="
        self.printPhrase()

        Transki = libmar.miksing()
        Transki.requested_argv_dict = {
            "tribe"   : tribe_list,
            "group"   : group_list,
            "prefix"  : self.requested_config_dict.get("result/ballgown") + "/",
            "postfix" : "/t_data.json",
            "libconvert"  : self.requested_config_dict.get("libconvert/TranscriptExpression")
        }
        Transki.log_file_prefix_str = self.log_file_prefix_str + "sca-Transki-"
        Transki.scanning()

        Geniski = libmar.miksing()
        Geniski.requested_argv_dict = {
            "tribe"   : tribe_list,
            "group"   : group_list,
            "prefix"  : self.requested_config_dict.get("result/stringtie") + "/",
            "postfix" : "-gene.json",
            "libconvert"  : self.requested_config_dict.get("libconvert/GeneExpression")
        }
        Geniski.log_file_prefix_str = self.log_file_prefix_str + "sca-Geniski-"
        Geniski.scanning()

        if tribe_list != []:
            tribe_str = tribe_list[0]

            self.phrase_str = "==========\nStage 3 : Merging\n=========="
            self.printPhrase()

            Transki.log_file_prefix_str = self.log_file_prefix_str + "fus-Transki-"
            Transki.fusion()
            Transki.resusi = (
                self.requested_config_dict.get("result/st-result") + "/" +
                self.requested_config_dict.get("data/prefix").get(tribe_str) + "TranscriptExpression.json"
            )
            with open(Transki.resusi,"w") as resufi:
                json.dump(Transki.resudi,resufi,indent=4,sort_keys=True)
            Transki.log_file_prefix_str = self.log_file_prefix_str + "ara-Transki-"
            Transki.arrange()

            Geniski.log_file_prefix_str = self.log_file_prefix_str + "fus-Geniski-"
            Geniski.fusion()
            Geniski.resusi = (
                self.requested_config_dict.get("result/st-result") + "/" +
                self.requested_config_dict.get("data/prefix").get(tribe_str) + "GeneExpression.json"
            )
            with open(Geniski.resusi,"w") as resufi:
                json.dump(Geniski.resudi,resufi,indent=4,sort_keys=True)
            Geniski.log_file_prefix_str = self.log_file_prefix_str + "ara-Geniski-"
            Geniski.arrange()

        self.phrase_str = "==========\nStage 4 : Extract Data for DESeq\n=========="
        self.printPhrase()

        filani = self.requested_config_dict.get("result/DESeq2") + "/" + "stringtie-list.txt"
        filafi = open(filani,"w")
        filafi.write("")
        filafi.close()

        for tribe_name in tribe_list:
            for gupo in group_list:
                linosi = (
                    gupo + " " +
                    self.requested_config_dict.get("result/ballgown") + "/" +
                    self.requested_config_dict.get("data/prefix").get(tribe_name) +
                    gupo + "-ballgown.gtf" +
                    "\n"
                )

                with open(filani,"a") as filafi:
                    filafi.write(linosi)

        self.comand_line_list = [
            "python2", self.requested_config_dict.get("bin/prepDE"),
            "-i", filani
        ]
        self.runCommand()

        self.comand_line_list = [
            "mv", "gene_count_matrix.csv", self.requested_config_dict.get("result/DESeq2") + "/"
        ]
        self.runCommand()

        self.comand_line_list = [
            "mv", "transcript_count_matrix.csv", self.requested_config_dict.get("result/DESeq2") + "/"
        ]
        self.runCommand()

        self.comand_line_list = []

        if refesi != "" and tribe_list != []:
            self.phrase_str = "==========\nStage 5 : Combine Description from GFF3\n=========="
            self.printPhrase()

            tribe_str = tribe_list[0]
            tiposi = self.requested_config_dict.get("type/database").get(tribe_str)

            GeneID = libsnm.geneid()
            GeneID.requested_argv_dict = {
                "description" : refesi ,
                "basement" : Transki.resusi ,
            }
            tagadi = self.requested_config_dict.get("target/libsnm").get(tiposi+"-transcript")
            GeneID.requested_argv_dict.update(tagadi)
            GeneID.filasi = "libsnm.geneid"
            GeneID.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act15-stire-geneid-"
            GeneID.actor()

            GeneID.requested_argv_dict = {
                "description" : refesi ,
                "basement" : Geniski.resusi ,
            }
            tagadi = self.requested_config_dict.get("target/libsnm").get(tiposi+"-gene")
            GeneID.requested_argv_dict.update(tagadi)
            GeneID.filasi = "libsnm.geneid"
            GeneID.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act15-stire-geneid-"
            GeneID.actor()

            self.phrase_str = "==========\nStage 6 : Convert JSON back to TSV/CTAB\n=========="
            self.printPhrase()
        else:
            self.phrase_str = "==========\nStage 5 : Convert JSON back to TSV/CTAB\n=========="
            self.printPhrase()

        CvtoTAB = libConvert.cvtJSONtoDSV()
        CvtoTAB.filasi = "libConvert.cvtJSONtoDSV"
        CvtoTAB.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act15-stire-covetab-"
        CvtoTAB.requested_argv_dict = {
            "files" : [Transki.resusi],
            "column" : Transki.coluli
        }
        CvtoTAB.actor()

        CvtoTAB.requested_argv_dict = {
            "files" : [Geniski.resusi],
            "column" : Geniski.coluli
        }
        CvtoTAB.actor()

        self.printBlankLine()

        self.stopLog()

        self.phrase_str = "\n\n"
        self.printPhrase()

StiRes = stitieresult()
