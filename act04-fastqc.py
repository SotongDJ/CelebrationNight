#!/usr/bin/env python3
import libWorkFlow, libConfig, sys
global helper_msg_block
helper_msg_block="""
--- README of act04-fastqc ---
 Title:
  Batch Processing for FastQC

 Usage:
  python act04-fastqc -t <TRIBE> -g <GROUP> <GROUP> <GROUP>... \\
    -s <SUBGROUP> <SUBGROUP> <SUBGROUP>...

 Data Structure:
  First : tribe,
    e.g. raw, untrim, trimmed...
  Second: group,
    e.g. control, A, B, 1, 2...
  Third : subgroup/files,
    e.g. foward, reverse, pair, unpair

 Visualise graph: explanation01-dataStructure.svg

 Original command:
  fastqc -o [Result Folder] [FASTQ files]

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
class fasquacon(libWorkFlow.workflow):
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

        self.script_name = "act04-fastqc"
        self.requested_config_dict = {
            "bin/fastqc" : ConfigDict.get_str("bin/fastqc"),
            "result/raw" : ConfigDict.get_str("result/raw"),
            "result/fastqc" : ConfigDict.get_str("result/fastqc"),
            "result/log" : ConfigDict.get_str("result/log"),
            "data/prefix" : ConfigDict.get_dict("data/prefix"),
            "raw/type" : ConfigDict.get_str("raw/type"),
        }
        self.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act04-fastqc-"

        self.comand_line_list = []
        self.adcoli = [
            self.requested_config_dict.get("bin/fastqc") , "-o",
            self.requested_config_dict.get("result/fastqc"), "--extract",
        ]

    def actor(self):
        tribe_list = self.requested_argv_dict.get("tribe",[])
        group_list = self.requested_argv_dict.get("group",[])
        suguli = self.requested_argv_dict.get("subgroup",[])

        self.startLog()

        self.target_file_path = self.requested_config_dict.get("result/fastqc")
        self.checkPath()
        for tribe_name in tribe_list:
            for gupo in group_list:
                for sugu in suguli:
                    self.comand_line_list = []
                    self.comand_line_list.extend(self.adcoli)

                    inpusi = (
                        self.requested_config_dict.get("result/raw") + "/" + tribe_name + "/" +
                        self.requested_config_dict.get("data/prefix").get(tribe_name) +
                        gupo + "-" + sugu + "." + self.requested_config_dict.get("raw/type")
                    )
                    self.comand_line_list.append(inpusi)

                    self.runCommand()

        self.stopLog()

FaQaC = fasquacon()
