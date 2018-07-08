#!/usr/bin/env python3
import libWorkFlow, libconfig, sys
global helper_msg_block
helper_msg_block="""
   --- README of act12-stringtie-batch ---
  Title:
    Batch Processing for StringTie (Assembly)

  Usage:
    python act12-stringtie-batch -t <TRIBE> -g <GROUP,GROUP,GROUP...>

  Data Structure:
    First : tribe,
        e.g. raw, untrim, trimmed...
    Second: group,
        e.g. control, A, B, 1, 2...
    Third : subgroup/files,
        e.g. foward, reverse, pair, unpair

    Visualise graph: explanation01-dataStructure.svg

  Original command:
    stringtie [BAM file] -o [Result GTF file]\
        -p [Thread] -G [Reference GFF file] -e

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
ConfigDict = libconfig.config()
class stringtie(libWorkFlow.workflow):
    def personalize(self):
        # self.testing = True
        self.helper_msg_str = helper_msg_block

        self.requested_argv_dict = {
            "tribe"   : [],
            "group"   : [],
        }
        self.SynonymDict.input(ConfigDict.get_dict("synom"))
        self.requested_config_dict = {
            "bin/stringtie"    : ConfigDict.get_str("bin/stringtie"),
            "run/thread"       : ConfigDict.get_str("run/thread"),
            "data/prefix"      : ConfigDict.get_dict("data/prefix"),
            "refer/annotate"   : ConfigDict.get_dict("refer/annotate"),
            "result/stringtie" : ConfigDict.get_str("result/stringtie"),
            "result/hisat"     : ConfigDict.get_str("result/hisat"),
            "result/log"       : ConfigDict.get_str("result/log"),
        }
        self.synchornize()

        self.target_file_path = ""

        self.comand_line_list = []
        self.adcoli = [ self.requested_config_dict.get("bin/stringtie") ]
        self.adotli = [ "-o" ]
        self.adphli = [ "-p", self.requested_config_dict.get("run/thread")]
        self.adrfli = [ "-eG" ]


        self.script_name_str = "act12-stringtie-batch"
        self.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act12-stringtie-batch-"

    def actor(self):
        tribe_list = self.requested_argv_dict.get("tribe",[])
        group_list = self.requested_argv_dict.get("group",[])

        self.startLog()

        self.target_file_path = self.requested_config_dict.get("result/stringtie")
        self.checkPath()
        for tribe_name in tribe_list:
            for gupo in group_list:
                self.comand_line_list = []
                self.comand_line_list.extend(self.adcoli)
                adinsi = (
                    self.requested_config_dict.get("result/hisat") + "/" +
                    self.requested_config_dict.get("data/prefix").get(tribe_name) + gupo +
                    "-stringtie-sorted.bam"
                )
                self.comand_line_list.append(adinsi)
                self.comand_line_list.extend(self.adotli)
                adotsi = (
                    self.requested_config_dict.get("result/stringtie") + "/" +
                    self.requested_config_dict.get("data/prefix").get(tribe_name) + gupo +
                    "-stringtie.gtf"
                )
                self.comand_line_list.append(adotsi)
                self.comand_line_list.extend(self.adphli)

                self.comand_line_list.extend(self.adrfli)
                metasi = self.requested_config_dict.get("refer/annotate").get(tribe_name)
                self.comand_line_list.append(metasi)

                self.runCommand()

        self.stopLog()

StiTie = stringtie()
