#!/usr/bin/env python3
import sys, json, pprint, time
import pyWorkFlow,libConfig
from subprocess import call

helper_msg_block="""
   --- README of act07-trim ---
 Title:
    Batch Processing for Trimmomatic

 Usage:
    python act07-trim \\
        --raw=<TRIBE of Sources> \\
        --pair=<TRIBE for paired seq> \\
        --unpair=<TRIBE for unpaired seq> \\
        -g <GROUP,GROUP,GROUP...>

 Structure:
    First : tribe,
        e.g. raw, untrim, trimmed...
    Second: group,
        e.g. control, A, B, 1, 2...
    Third : subgroup/files,
        e.g. foward, reverse, pair, unpair

    Visualise graph: explanation01-dataStructure.svg

 Original command:
  java -jar <bin>/trimmomatic-0.35.jar PE \\
    -phred33 -threads <threads> \\
    input_forward.fq.gz input_reverse.fq.gz \\
    output_forward_paired.fq.gz output_forward_unpaired.fq.gz \\
    output_reverse_paired.fq.gz output_reverse_unpaired.fq.gz \\
    <ILLUMINACLIP> <LEADING> \\
    <TRAILING> <SLIDINGWINDOW> <MINLEN>

 CAUTION:
    <GROUP> must separate with space
    <GROUP> don't allowed spacing

   --- README ---
""""""
    command split into [ linoli , linuli , linali ]
 Postfix:
  -si: String
  -ho: String(that store dir path)
  -ti: Intiger/Float
  -li: List
  -tu: Tuple
  -di: Dictionary
  -fa: File (with open())
  -so: JSON
"""

ConfigDict = libConfig.config()
class trimmo(pyWorkFlow.workflow):
    def personalize(self):
        # self.testing = True
        self.helper_msg_str = helper_msg_block

        self.requested_argv_dict = {
            "raw"    : "",
            "pair"   : "",
            "unpair" : "",
            "group"  : [],
        }
        self.SynonymDict.input(ConfigDict.get_dict("synom"))
        self.synchornize()

        self.requested_config_dict = {
            "bin/trimmomatic" : ConfigDict.get_str("bin/trimmomatic"),
            "raw/type"        : ConfigDict.get_str("raw/type"),
            "run/phred"       : ConfigDict.get_str("run/phred"),
            "run/thread"      : ConfigDict.get_str("run/thread"),
            "postfix/forward" : ConfigDict.get_str("postfix/forward"),
            "postfix/reverse" : ConfigDict.get_str("postfix/reverse"),
            "trimmo/lead"     : ConfigDict.get_str("trimmo/lead"),
            "trimmo/trail"    : ConfigDict.get_str("trimmo/trail"),
            "trimmo/slide"    : ConfigDict.get_str("trimmo/slide"),
            "trimmo/length"   : ConfigDict.get_str("trimmo/length"),
            "trimmo/adapter"  : ConfigDict.get_str("trimmo/adapter"),
            "data/prefix"     : ConfigDict.get_dict("data/prefix"),
            "result/raw"      : ConfigDict.get_str("result/raw"),
        }

        self.comand_line_list = []
        self.adcoli = [
            'java', '-jar', self.requested_config_dict.get("bin/trimmomatic"),
            'PE', '-phred'+self.requested_config_dict.get("run/phred"),
            '-threads', self.requested_config_dict.get("run/thread")
        ]
        self.adpali = []
        self.adpali.append(self.requested_config_dict.get("trimmo/lead"))
        self.adpali.append(self.requested_config_dict.get("trimmo/trail"))
        self.adpali.append(self.requested_config_dict.get("trimmo/slide"))
        self.adpali.append(self.requested_config_dict.get("trimmo/length"))
        self.adpali.append(self.requested_config_dict.get("trimmo/adapter"))

        self.script_name = "act07-trim"
        self.log_file_prefix_str = ConfigDict.get_str("result/log")+"/act07-trim-"

    def actor(self):
        self.group_list = self.requested_argv_dict.get("group" ,[])
        self.rawusi = self.requested_argv_dict.get("raw"   ,"")
        self.pairsi = self.requested_argv_dict.get("pair"  ,"")
        self.unpasi = self.requested_argv_dict.get("unpair","")

        self.startLog()

        inrasi = self.requested_config_dict.get("result/raw") + "/" + self.rawusi
        otpasi = self.requested_config_dict.get("result/raw") + "/" + self.pairsi
        otunsi = self.requested_config_dict.get("result/raw") + "/" + self.unpasi
        self.target_file_list = [ inrasi, otpasi, otunsi ]
        self.checkPath()

        if self.rawusi != "" and self.pairsi != "" and self.unpasi != "":
            for gupo in self.group_list:
                input_forward = (
                    inrasi + "/" +
                    self.requested_config_dict.get("data/prefix").get(self.rawusi,"") +
                    gupo + "-" + self.requested_config_dict.get("postfix/forward") +
                    "." + self.requested_config_dict.get("raw/type")
                )
                input_reverse = (
                    inrasi + "/" +
                    self.requested_config_dict.get("data/prefix").get(self.rawusi,"") +
                    gupo + "-" + self.requested_config_dict.get("postfix/reverse") +
                    "." + self.requested_config_dict.get("raw/type")
                )
                output_forward_paired   = (
                    otpasi + "/" +
                    self.requested_config_dict.get("data/prefix").get(self.pairsi,"") +
                    gupo + "-" + self.requested_config_dict.get("postfix/forward") +
                    "." + self.requested_config_dict.get("raw/type")
                )
                output_forward_unpaired = (
                    otunsi + "/" +
                    self.requested_config_dict.get("data/prefix").get(self.unpasi,"") +
                    gupo + "-" + self.requested_config_dict.get("postfix/forward") +
                    "." + self.requested_config_dict.get("raw/type")
                )
                output_reverse_paired   = (
                    otpasi + "/" +
                    self.requested_config_dict.get("data/prefix").get(self.pairsi,"") +
                    gupo + "-" + self.requested_config_dict.get("postfix/reverse") +
                    "." + self.requested_config_dict.get("raw/type")
                )
                output_reverse_unpaired = (
                    otunsi + "/" +
                    self.requested_config_dict.get("data/prefix").get(self.unpasi,"") +
                    gupo + "-" + self.requested_config_dict.get("postfix/reverse") +
                    "." + self.requested_config_dict.get("raw/type")
                )

                self.comand_line_list = []
                self.comand_line_list.extend(self.adcoli)
                self.comand_line_list.append(input_forward)
                self.comand_line_list.append(input_reverse)
                self.comand_line_list.append(output_forward_paired)
                self.comand_line_list.append(output_forward_unpaired)
                self.comand_line_list.append(output_reverse_paired)
                self.comand_line_list.append(output_reverse_unpaired)
                self.comand_line_list.extend(self.adpali)

                self.runCommand()

            self.stopLog()

Trimmo = trimmo()
