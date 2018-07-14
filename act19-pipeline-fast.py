#!/usr/bin/env python3
import libWorkFlow, libConfig, libstm
import time
global helper_msg_block
helper_msg_block="""
--- README of act19-pipeline-fast ---
 Title:
  Batch Processing for StringTie (Compare)

 Usage:
  python act19-pipeline-fast -t <TRIBE> -g <GROUP,GROUP,GROUP...>

 Data Structure:
  First : tribe,
    e.g. raw, untrim, trimmed...
  Second: group,
    e.g. control, A, B, 1, 2...
  Third : subgroup/files,
    e.g. foward, reverse, pair, unpair

  Visualise graph: explanation01-dataStructure.svg

 Original command:
  stringtie [GROUP BAM file] -B \\
    -G [Merged GTF file] -p [thread] -b [Result PATH]

 CAUTION:
  Act14 required libstm
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
Marge = libstm.marge()
ConfigDict = libConfig.config()
class stititobago(libWorkFlow.workflow):
    def personalize(self):
        # self.testing = True
        self.helper_msg_str = helper_msg_block

        self.requested_argv_dict = {
            "tribe"   : [],
            "group"   : [],
            # "control" : ""
        }
        self.SynonymDict.input(ConfigDict.get_dict("synom"))
        self.synchornize()

        self.script_name = "act19-pipeline-fast"
        self.requested_config_dict = {
            "bin/stringtie" : ConfigDict.get_str("bin/stringtie"),
            "result/stringtie" : ConfigDict.get_str("result/stringtie"),
            "result/ballgown" : ConfigDict.get_str("result/ballgown"),
            "result/hisat" : ConfigDict.get_str("result/hisat"),
            "result/log" : ConfigDict.get_str("result/log"),
            "run/thread" : ConfigDict.get_str("run/thread"),
            "data/prefix" : ConfigDict.get_dict("data/prefix"),
            "refer/annotate" : ConfigDict.get_dict("refer/annotate"),
        }
        self.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act19-pipeline-fast-"

        self.comand_line_list = []
        self.adcoli = [ self.requested_config_dict.get("bin/stringtie") ]
        self.adrfli = [ "-eG" ]
        self.adphli = [ "-p", self.requested_config_dict.get("run/thread")]
        self.adfoli = [ "-b" ]
        self.adotli = [ "-o" ]
        self.adagli = [ "-eA" ]

    def actor(self):
        tribe_list = self.requested_argv_dict.get("tribe",[])
        group_list = self.requested_argv_dict.get("group",[])
        # cotosi = self.requested_argv_dict.get("control","")

        self.startLog()

        self.target_file_list = []
        self.target_file_list.append(self.requested_config_dict.get("result/stringtie"))
        self.target_file_list.append(self.requested_config_dict.get("result/hisat"))
        self.target_file_list.append(self.requested_config_dict.get("result/ballgown")+"-fast")
        self.checkPath()

        for tribe_name in tribe_list:
            for gupo in group_list:
                self.adinsi = self.requested_config_dict.get("refer/annotate").get(tribe_name)
                self.comand_line_list = []
                self.comand_line_list.extend(self.adcoli)

                adsbsi = (
                    self.requested_config_dict.get("result/hisat") + "/" +
                    self.requested_config_dict.get("data/prefix").get(tribe_name) +
                    gupo + "-stringtie-sorted.bam"
                )
                self.comand_line_list.append(adsbsi)

                self.comand_line_list.extend(self.adrfli)
                self.comand_line_list.append(self.adinsi)

                self.comand_line_list.extend(self.adphli)

                self.comand_line_list.extend(self.adfoli)
                adresi = (
                    self.requested_config_dict.get("result/ballgown") + "-fast/" +
                    self.requested_config_dict.get("data/prefix").get(tribe_name) +
                    gupo
                )
                self.comand_line_list.append(adresi)

                self.comand_line_list.extend(self.adotli)
                adresi = (
                    self.requested_config_dict.get("result/ballgown") + "-fast/" +
                    self.requested_config_dict.get("data/prefix").get(tribe_name) +
                    gupo + "-ballgown.gtf"
                )
                self.comand_line_list.append(adresi)

                self.comand_line_list.extend(self.adagli)
                adgesi = (
                    self.requested_config_dict.get("result/ballgown") + "-fast/" +
                    self.requested_config_dict.get("data/prefix").get(tribe_name) +
                    gupo + "-gene.tsv"
                )
                self.comand_line_list.append(adgesi)

                self.runCommand()

        self.stopLog()

StiToB = stititobago()
