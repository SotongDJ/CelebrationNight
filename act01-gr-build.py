#!/usr/bin/env python3
import libWorkFlow, libconfig, libgext
global helper_msg_block
helper_msg_block="""
--- README of act01-Genome-Reference-build.py ---
 Title:
  Construct reference from Genome information for further analysis

 Usage:
  python3 act01-gr-build.py -t <tribe>\\
    --genome=<Path and Name of GENOME File>
    --prefix=<Prefix for HISAT2 index and GFF Info file>

 CAUTION:
  Genome tag and Annotate tag must set with file name only.

 Original Command of Stage 1 (Build HISAT2 Index):
  hisat2-build -p [THREAD] <Path and Name of GENOME File> \\
    <OUTPUT FOLDER for HISAT2>/<codename>
--- README ---
"""
ConfigDict = libconfig.config()
class genomerefer(libWorkFlow.workflow):
    def personalize(self):
        # self.testing = True
        self.helper_msg_str = helper_msg_block

        self.requested_argv_dict = {
            "genome" : "",
            "prefix" : "",
            "tribe"  : "",
        }
        self.SynonymDict.input(ConfigDict.get_dict("synom"))
        self.synchornize()

        self.comand_line_list = []
        self.script_name_str = "act01-Genome-Reference-build.py"
        self.requested_config_dict = {
            "bin/hisat2build" : ConfigDict.get_str("bin/hisat2build"),
            "index/hisat"     : ConfigDict.get_str("index/hisat"),
            "result/log"      : ConfigDict.get_str("result/log"),
            "run/thread"      : ConfigDict.get_str("run/thread"),
            "refer/annotate"  : ConfigDict.get_dict("refer/annotate"),
        }
        self.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act01-gr-build-"

    def actor(self):
        self.genome_file_path = self.requested_argv_dict.get("genome","")
        self.prefix_str = self.requested_argv_dict.get("prefix" ,"")
        self.tribe_str = self.requested_argv_dict.get("tribe" ,"")

        self.startLog()

        self.phrase_str = "==========\nStage 1 : Build HISAT2 Index\n=========="
        self.printPhrase()

        self.binary_path = self.requested_config_dict.get("bin/hisat2build")
        self.thread_argv_list = ["-p",self.requested_config_dict.get("run/thread")]
        self.output_path = self.requested_config_dict.get("index/hisat") + "/" + self.prefix_str

        self.comand_line_list = []
        self.comand_line_list.append(self.binary_path)
        self.comand_line_list.extend(self.thread_argv_list)
        self.comand_line_list.append(self.genome_file_path)
        self.comand_line_list.append(self.output_path)
        self.runCommand()

        self.phrase_str = "==========\nStage 2 : Copy Genome FASTA to HISAT2 Index folder\n=========="
        self.printPhrase()

        self.comand_line_list = ["cp",self.genome_file_path,self.output_path+".fa"]
        self.runCommand()

        self.phrase_str = "==========\nStage 3 : Extract GFF Information\n=========="
        self.printPhrase()
        # under construction
        """
        Gekta = libgext.gffextract()
        Gekta.testing = self.testing
        Gekta.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act01-grb-libgext-"
        Gekta.requested_argv_dict = {
            "input"  : [self.requested_config_dict.get("refer/annotate").get(self.tribe_str)],
            "tribe"  : self.tribe_str,
            "output" : self.prefix_str+"-gff-info.json"
        }
        Gekta.actor()
        """
        self.printBlankLine()

        self.stopLog()

GeRef = genomerefer()
