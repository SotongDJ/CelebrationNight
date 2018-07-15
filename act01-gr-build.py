#!/usr/bin/env python3
import pyWorkFlow, libConfig, libConvert
global helper_msg_block
helper_msg_block="""
--- README of act01-Genome-Reference-build.py ---
 Title:
  Construct reference from Genome information for further analysis

 Usage:
  python3 act01-gr-build.py -a <codename for reference>\\
    --genome=<Path and Name of GENOME SEQUENCE File>
    --annotation=<Path and Name of GENOME ANNOTATION File>

 CAUTION:
  Genome tag and Annotate tag must set with file name only.

 Original Command of Stage 1 (Build HISAT2 Index):
  hisat2-build -p [THREAD] <Path and Name of GENOME File> \\
    <OUTPUT FOLDER for HISAT2>/<codename>
--- README ---
"""


ConfigDict = libConfig.config()
class genomerefer(pyWorkFlow.workflow):
    def personalize(self):
        # self.testing = True
        self.helper_msg_str = helper_msg_block

        self.requested_argv_dict = {
            "refer": "",
            "genome": "",
            "annotation": ""
        }
        self.SynonymDict.input(ConfigDict.get_dict("synom"))
        self.synchornize()

        self.comand_line_list = []
        self.script_name = "act01-Genome-Reference-build.py"
        ConfigDict.requested_dict = {}
        ConfigDict.requested_dict = {
            "bin/hisat2build": "",
            "result/log": "",
            "result/gff-json": "",
            "index/hisat": "",
            "run/thread": "",
            "refer/annotate": {},
            "refer/genome": {},
            "head/gff": {},
        }
        self.requested_config_dict = ConfigDict.get_batchly()
        self.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act01-gr-build-"

    def actor(self):
        self.refer_codename_str = self.requested_argv_dict.get("refer","")
        self.genome_path = self.requested_argv_dict.get("genome" ,"")
        self.annotation_path = self.requested_argv_dict.get("annotation" ,"")

        self.startLog()

        genome_boolean = False
        annotation_boolean = False
        if self.refer_codename_str != "":
            genome_temp_dict = self.requested_config_dict.get("refer/genome",{})
            genome_temp_path = genome_temp_dict.get(self.refer_codename_str,"")
            if self.genome_path == "" and genome_temp_path != "":
                self.genome_path = genome_temp_path
                genome_boolean = True
            elif self.genome_path != "":
                genome_temp_dict.update({ self.refer_codename_str : self.genome_path })
                ConfigDict.update({ "refer/genome" : genome_temp_dict })
                genome_boolean = True

            annotation_temp_dict = self.requested_config_dict.get("refer/annotate",{})
            annotation_temp_path = annotation_temp_dict.get(self.refer_codename_str,"")
            if self.annotation_path == "" and annotation_temp_path != "":
                self.annotation_path = annotation_temp_path
                annotation_boolean = True
            elif self.annotation_path != "":
                annotation_temp_dict.update({ self.refer_codename_str : self.annotation_path })
                ConfigDict.update({ "refer/annotate" : annotation_temp_dict })
                annotation_boolean = True

        if self.refer_codename_str != "" and genome_boolean and annotation_boolean:
            self.phrase_str = "==========\nStage: Build HISAT2 Index\n=========="
            self.printPhrase()

            self.binary_path = self.requested_config_dict.get("bin/hisat2build")
            self.thread_argv_list = ["-p",self.requested_config_dict.get("run/thread")]
            self.output_path = self.requested_config_dict.get("index/hisat") + "/" + self.refer_codename_str

            self.comand_line_list = []
            self.comand_line_list.append(self.binary_path)
            self.comand_line_list.extend(self.thread_argv_list)
            self.comand_line_list.append(self.genome_path)
            self.comand_line_list.append(self.output_path)
            self.runCommand()

            self.phrase_str = "==========\nStage: Copy Genome FASTA to HISAT2 Index folder\n=========="
            self.printPhrase()

            self.comand_line_list = ["cp",self.genome_path,self.output_path+".fa"]
            self.runCommand()

        else:
            self.phrase_str = (
                "Required codename of [refer], \n"
                +"use \"--help\" argument for further info."
            )
            self.printPhrase()

        self.phrase_str = "==========\nStage: Copy Refer annotation to Result folder\n=========="
        self.printPhrase()

        self.extraction_path = self.requested_config_dict.get("result/gff-json")+"/"+self.refer_codename_str
        self.comand_line_list = ["cp", self.annotation_path, self.extraction_path+".gff"]
        self.runCommand()

        self.phrase_str = "==========\nStage: Convert GFF to JSON\n=========="
        self.printPhrase()

        header_list = self.requested_config_dict.get("head/gff")
        CvtoJSON = libConvert.cvtDSVtoJSON()
        CvtoJSON.requested_argv_dict = {
            "files": [self.extraction_path+".gff"],
            "refer_column": "",
            "prefix": "gff",
            "header": header_list,
            "headless": False,
            "delimiter": "\t"
        }
        CvtoJSON.actor()

        self.phrase_str = "==========\nStage: Extract GFF Information\n=========="
        self.printPhrase()
        # under construction

        Extract = libConvert.attributionExtractor()
        Extract.requested_argv_dict = {
            "gff.json"  : [self.extraction_path+".json"],
        }
        Extract.actor()

        self.printBlankLine()

        self.stopLog()

GeRef = genomerefer()
