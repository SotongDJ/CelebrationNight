#!/usr/bin/env python3
import pyWorkFlow, libConfig, libstm
import sys
global helper_msg_block
helper_msg_block="""
   --- README of act17-stringtie-cuffdiff ---
  Title:
    Batch Processing for StringTie-CuffDiff workflow

  Usage:
    python act17-sticuf -t <TRIBE> --control=<Control Group> \\
      -g <GROUP,GROUP,GROUP...>

  Data Structure:
    First : tribe,
        e.g. raw, untrim, trimmed...
    Second: group,
        e.g. control, A, B, 1, 2...
    Third : subgroup/files,
        e.g. foward, reverse, pair, unpair

    Visualise graph: explanation01-dataStructure.svg

  Original command:
    cuffdiff -o [output folder] -p [thread] \\
      <Merged transcript that created by libstm> \\
      <sample1_hits.sam> <sample2_hits.sam> [... sampleN_hits.sam]

  CAUTION:
   Act17 required libstm
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
class stiticuffdiff(pyWorkFlow.workflow):
    def personalize(self):
        # self.testing = True
        self.helper_msg_str = helper_msg_block

        self.requested_argv_dict = {
            "tribe"   : [],
            "group"   : [],
            "control" : ""
        }
        self.SynonymDict.input(ConfigDict.get_dict("synom"))
        self.requested_config_dict = {
            "bin/cuffdiff"     : ConfigDict.get_str("bin/cuffdiff"),
            "run/thread"       : ConfigDict.get_str("run/thread"),
            "data/prefix"      : ConfigDict.get_dict("data/prefix"),
            "result/stringtie" : ConfigDict.get_str("result/stringtie"),
            "result/cuffdiff"  : ConfigDict.get_str("result/cuffdiff"),
            "result/hisat"     : ConfigDict.get_str("result/hisat"),
            "result/log"       : ConfigDict.get_str("result/log"),
        }
        self.synchornize()

        self.target_file_path = ""

        self.comand_line_list = []
        self.adcosi = self.requested_config_dict.get("bin/cuffdiff")
        self.adlasi = "-L"
        self.adotsi = "-o"
        self.adphli = [ "-p", self.requested_config_dict.get("run/thread")]

        self.script_name = "act17-sticuf"
        self.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act17-sticuf-"

    def actor(self):
        tribe_list = self.requested_argv_dict.get("tribe",[])
        group_list = self.requested_argv_dict.get("group",[])
        cotosi = self.requested_argv_dict.get("control","")

        self.startLog()

        self.target_file_path = self.requested_config_dict.get("result/cuffdiff")
        self.checkPath()
        for tribe_name in tribe_list:
            self.printBlankLine()
            Marge.testing = self.testing
            Marge.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act17-StiCuf-Merge-"

            metali = []
            metali.extend(group_list)
            metali.append(cotosi)
            Marge.requested_argv_dict = {
                "tribe" : [tribe],
                "group" : metali
            }
            Marge.actor()
            self.printBlankLine()

            self.adrfsi = Marge.outusi
            self.target_file_path = self.adrfsi
            self.checkFile()

            if cotosi != "":
                self.cosasi = (
                    self.requested_config_dict.get("result/hisat") + "/" +
                    self.requested_config_dict.get("data/prefix").get(tribe_name) +
                    cotosi + "-cufflinks-sorted.bam"
                )
                adinli = []
                adinli.append(self.cosasi)
                for gupo in group_list:
                    adinsi = (
                        self.requested_config_dict.get("result/hisat") + "/" +
                        self.requested_config_dict.get("data/prefix").get(tribe_name) +
                        gupo + "-cufflinks-sorted.bam"
                    )
                    adinli.append(adinsi)
                    bainli = [
                        self.cosasi, adinsi
                    ]

                    self.comand_line_list = []
                    self.comand_line_list.append(self.adcosi)
                    self.comand_line_list.append(self.adlasi)
                    self.comand_line_list.append(cotosi+","+gupo)
                    self.comand_line_list.append(self.adotsi)
                    adotsi = (
                        self.requested_config_dict.get("result/cuffdiff") + "/" +
                        self.requested_config_dict.get("data/prefix").get(tribe_name) + gupo + "-Result"
                    )
                    self.comand_line_list.append(adotsi)
                    self.comand_line_list.extend(self.adphli)
                    self.comand_line_list.append(self.adrfsi)
                    self.comand_line_list.extend(bainli)

                    self.runCommand()

                self.comand_line_list = []

                self.comand_line_list.append(self.adcosi)
                self.comand_line_list.append(self.adlasi)
                self.comand_line_list.append(cotosi+","+",".join(group_list))
                self.comand_line_list.append(self.adotsi)
                adotsi = (
                    self.requested_config_dict.get("result/cuffdiff") + "/" +
                    self.requested_config_dict.get("data/prefix").get(tribe_name) + "Result"
                )
                self.comand_line_list.append(adotsi)
                self.comand_line_list.extend(self.adphli)
                self.comand_line_list.append(self.adrfsi)
                self.comand_line_list.extend(adinli)

                self.runCommand()

        self.stopLog()

StiCuf = stiticuffdiff()
