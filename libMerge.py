#!/usr/bin/env python3
import pyWorkFlow, libConfig
global helper_msg_block
helper_msg_block="""
--- README of library-stringtie-merge ---
 Title:
  Merge transcriptome for StringTie

 Usage:
  import libstm
  Marge = libstm.marge()
  Marge.testing = self.testing
  Marge.log_file_prefix_str = < Log File Path>
  Marge.requested_argv_dict = {
    "tribe"   : <TRIBE>,
    "group"   : [<GROUP>,<GROUP>......]
  }
  Marge.actor()

 Data Structure:
  First : tribe,
    e.g. raw, untrim, trimmed...
  Second: group,
    e.g. control, A, B, 1, 2...
  Third : subgroup/files,
    e.g. foward, reverse, pair, unpair

  Visualise graph: explanation01-dataStructure.svg

 Original command:
  stringtie [gtf files] --merge -o [path for result] \\
  -p [thread] -G [reference gff file]

 CAUTION:
  <GROUP> must separate with space
  <GROUP> don't allowed spacing

--- README ---
"""
ConfigDict = libConfig.config()
class marge(pyWorkFlow.workflow):
    def redirecting(self):
        """"""
    def personalize(self):
        # self.testing = True

        self.requested_argv_dict = {
            "tribe" : [],
            "group" : []
        }
        # self.synchornize()

        self.script_name = "library-stringtie-merge"
        self.requested_config_dict = {
            "bin/stringtie"    : ConfigDict.get_str("bin/stringtie"),
            "result/stringtie" : ConfigDict.get_str("result/stringtie"),
            "result/hisat"     : ConfigDict.get_str("result/hisat"),
            "result/log"       : ConfigDict.get_str("result/log"),
            "run/thread"       : ConfigDict.get_str("run/thread"),
            "data/prefix"      : ConfigDict.get_dict("data/prefix"),
            "refer/annotate"   : ConfigDict.get_dict("refer/annotate"),
        }
        self.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/exp13-stringtie-merge-"

        self.target_file_path = ""

        self.comand_line_list = []
        self.adcoli = [ self.requested_config_dict.get("bin/stringtie") ]
        self.admgli = [ "--merge" ]
        self.adotli = [ "-o" ]
        self.adphli = [ "-p", self.requested_config_dict.get("run/thread")]
        self.adrfli = [ "-eG" ]

    def actor(self):
        tribe_list = self.requested_argv_dict.get("tribe",[])
        group_list = self.requested_argv_dict.get("group",[])

        self.startLog()

        self.target_file_path = self.requested_config_dict.get("result/stringtie")
        self.checkPath()
        for tribe_name in tribe_list:
            self.comand_line_list = []
            self.comand_line_list.extend(self.adcoli)

            for gupo in group_list:
                group_str = ""
                group_str = (
                    self.requested_config_dict.get("result/stringtie") + "/" +
                    self.requested_config_dict.get("data/prefix").get(tribe_name) + gupo +
                    "-stringtie.gtf"
                )
                self.comand_line_list.append(group_str)

            self.comand_line_list.extend(self.admgli)
            self.comand_line_list.extend(self.adotli)
            self.outusi = (
                self.requested_config_dict.get("result/stringtie") + "/" +
                self.requested_config_dict.get("data/prefix").get(tribe_name) + "-".join(sorted(group_list)) +"-stringtie-merged.gtf"
            )
            self.comand_line_list.append(self.outusi)
            self.comand_line_list.extend(self.adphli)

            self.comand_line_list.extend(self.adrfli)
            metasi = self.requested_config_dict.get("refer/annotate").get(tribe_name)
            self.comand_line_list.append(metasi)

            self.runCommand()
        self.stopLog()
