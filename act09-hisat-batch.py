#!/usr/bin/env python3
import libWorkFlow, libconfig, sys
global helper_msg_block
helper_msg_block="""
   --- README of act09-hisat-batch ---
  Title:
    Batch Processing for HISAT2

  Usage:
    python act09-hisat-batch \\
      [stringtie|cufflinks] -t <TRIBE> -g <GROUP,GROUP,GROUP...> \\
      -x <GENOME PREFIX that USE in HISAT2-BUILD>

  Data Structure:
    First : tribe,
        e.g. raw, untrim, trimmed...
    Second: group,
        e.g. control, A, B, 1, 2...
    Third : subgroup/files,
        e.g. foward, reverse, pair, unpair

    Visualise graph: explanation01-dataStructure.svg

  Original command:
    hisat2 -q [--dta/--dta-cufflinks] --phred[33] -p [4]
        -x [prefix of HISAT2-build genome index]
        -1 [forward fastq files of]
        -2 [reverse fastq files of]
        -S [output SAM files]
    samtools sort -o [out-sorted.bam] [in.bam]
    samtools view -o [out.bam] -Su [in.sam]
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
class hisatbat(libWorkFlow.workflow):
    def personalize(self):
        # self.testing = True
        self.helper_msg_str = helper_msg_block

        self.requested_argv_dict = {
            "tribe" : [],
            "group" : [],
            "index" : "",
            "INDEPENDED"  : []
        }
        self.SynonymDict.input(ConfigDict.get_dict("synom"))
        self.synchornize()
        self.requested_config_dict = {
            "bin/hisat2"     : ConfigDict.get_str("bin/hisat2")     ,
            "run/phred"      : ConfigDict.get_str("run/phred")      ,
            "run/thread"     : ConfigDict.get_str("run/thread")     ,
            "index/hisat"    : ConfigDict.get_str("index/hisat")    ,
            "result/log"     : ConfigDict.get_str("result/log")     ,
            "result/hisat"   : ConfigDict.get_str("result/hisat")   ,
            "result/raw"     : ConfigDict.get_str("result/raw")     ,
            "data/prefix"    : ConfigDict.get_dict("data/prefix")    ,
            "postfix/forward": ConfigDict.get_str("postfix/forward"),
            "postfix/reverse": ConfigDict.get_str("postfix/reverse"),
        }

        self.target_file_path = ""

        self.adcoli = [self.requested_config_dict.get("bin/hisat2"),"-q"]
        self.adphli = ["--phred"+self.requested_config_dict.get("run/phred")]
        self.adthli = ["-p",self.requested_config_dict.get("run/thread")]
        self.adgnli = ["-x"]
        self.adh1li = ["-1"]
        self.adh2li = ["-2"]
        self.adrsli = ["-S"]

        self.becoli = ["samtools","view","-o"]
        self.beinli = ["-Su"]

        self.cecoli = ["samtools","sort","-o"]

        self.lscoli = ["ls", "-alFh"]
        self.rmcoli = ["rm", "-v"]


        self.script_name = "act09-hisat-batch.py"

        self.comand_line_list = []

        self.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act09-hisat-batch-"

    def actor(self):
        tribe_list = self.requested_argv_dict.get("tribe",[])
        group_list = self.requested_argv_dict.get("group",[])
        indesi = self.requested_argv_dict.get("index","")
        argvli = self.requested_argv_dict.get("INDEPENDED",[])

        self.startLog()

        self.stinli = [ 0 , False ]
        self.pofidi = {0:[]}
        self.argvdi = {0:""}
        timein = 0
        self.timoli = [0]
        self.jecosi = ""

        if indesi != "" and argvli != []:
            self.indesi =  self.requested_config_dict.get("index/hisat") + "/" + indesi
            for argv in argvli:

                if argv == "stringtie":
                    if timein != 0:
                        self.timoli.append(timein)
                    self.stinli = [ timein , True ]
                    self.pofidi.update({ timein : ["--dta"] })
                    self.argvdi.update({ timein : "-stringtie" })
                    timein = timein + 1

                elif argv == "cufflinks":
                    if timein != 0:
                        self.timoli.append(timein)
                    self.stinli = [ timein , True ]
                    self.pofidi.update({ timein : ["--dta-cufflinks"] })
                    self.argvdi.update({ timein : "-cufflinks" })
                    timein = timein + 1

                if argv == "testing":
                    self.testing = True

            self.target_file_path = self.requested_config_dict.get("result/hisat")
            self.checkPath()
            for tribe_name in tribe_list:
                for gupo in group_list:
                    for timo in self.timoli:
                        self.comand_line_list = []
                        self.comand_line_list.extend(self.adcoli)

                        pofili = self.pofidi.get(timo)
                        self.comand_line_list.extend(pofili)

                        self.comand_line_list.extend(self.adphli)
                        self.comand_line_list.extend(self.adthli)
                        self.comand_line_list.extend(self.adgnli)
                        self.comand_line_list.append(self.indesi)
                        self.comand_line_list.extend(self.adh1li)

                        fecosi = (
                            self.requested_config_dict.get("result/raw") + "/" +
                            tribe_name + "/" +
                            self.requested_config_dict.get("data/prefix").get(tribe_name) +
                            gupo + "-" +
                            self.requested_config_dict.get("postfix/forward") + ".fastq"
                        )
                        self.comand_line_list.append(fecosi)

                        self.comand_line_list.extend(self.adh2li)

                        hecosi = (
                            self.requested_config_dict.get("result/raw") + "/" +
                            tribe_name + "/" +
                            self.requested_config_dict.get("data/prefix").get(tribe_name) +
                            gupo + "-" +
                            self.requested_config_dict.get("postfix/reverse") + ".fastq"
                        )
                        self.comand_line_list.append(hecosi)

                        self.comand_line_list.extend(self.adrsli)

                        argvsi = self.argvdi.get(timo)
                        self.jecosi = (
                            self.requested_config_dict.get("result/hisat") + "/" +
                            self.requested_config_dict.get("data/prefix").get(tribe_name) +
                            gupo
                        )
                        self.comand_line_list.append( self.jecosi + argvsi + ".sam" )

                        self.target_file_path = self.jecosi + argvsi + ".sam"
                        abanbo = self.checkFile()
                        self.target_file_path = self.jecosi + argvsi + "-sorted.bam"
                        bababo = self.checkFile()
                        """
                           sam bam hisat samtool
                            0   0   1     1
                            1   0   0     1
                            0   1   0     0
                            1   1   0     1
                        """
                        if not abanbo and not bababo:
                            self.runCommand()

                        if timo == self.stinli[0] and self.stinli[1] and not bababo:
                            self.comand_line_list = []
                            self.comand_line_list.extend( self.rmcoli )
                            self.comand_line_list.append( self.jecosi + argvsi + ".bam" )

                            self.runCommand()

                            self.comand_line_list = []
                            self.comand_line_list.extend( self.becoli )
                            self.comand_line_list.append( self.jecosi + argvsi + ".bam" )
                            self.comand_line_list.extend( self.beinli )
                            self.comand_line_list.append( self.jecosi + argvsi + ".sam" )

                            self.runCommand()

                            self.comand_line_list = []
                            self.comand_line_list.extend( self.cecoli )
                            self.comand_line_list.append( self.jecosi + argvsi + "-sorted" + ".bam" )
                            self.comand_line_list.append( self.jecosi + argvsi + ".bam" )

                            self.runCommand()

                            self.comand_line_list = []
                            self.comand_line_list.extend( self.lscoli )
                            self.comand_line_list.append( self.jecosi + argvsi + ".sam" )
                            self.comand_line_list.append( self.jecosi + argvsi + ".bam" )
                            self.comand_line_list.append( self.jecosi + argvsi + "sorted" + ".bam" )

                            self.runCommand()

                            self.comand_line_list = []
                            self.comand_line_list.extend( self.rmcoli )
                            self.comand_line_list.append( self.jecosi + argvsi + ".bam" )
                            self.comand_line_list.append( self.jecosi + argvsi + ".sam" )

                            self.runCommand()
        self.stopLog()

HiSaB = hisatbat()
