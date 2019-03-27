#!/usr/bin/env python3
import pyWorkFlow, libConfig, libConvert
global helper_msg_block
helper_msg_block="""
--- README of act02-Attribution.py ---
 Title:
  Construct reference from Genome information for further analysis

 Usage:
  python3 act02-attribution.py -a <codename for reference>\\
    --genome=<Path and Name of GENOME SEQUENCE File>
    --annotation=<Path and Name of GENOME ANNOTATION File>

 CAUTION:
  Genome tag and Annotate tag must set with file name only.

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
        self.script_name = "act02-attribution.py"
        ConfigDict.requested_dict = {}
        ConfigDict.requested_dict = {
            "bin/hisat2build": "",
            "result/log": "",
            "result/gff-json": "",
            "index/hisat": "",
            "run/thread": "",
            "refer/annotate": {},
            "refer/genome": {},
            "header/gff3": {},
        }
        self.requested_config_dict = ConfigDict.get_batchly()
        self.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act02-attribution-"

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

        self.phrase_str = "==========\nStage: Copy Refer annotation to Result folder\n=========="
        self.printPhrase()

        self.extraction_path = self.requested_config_dict.get("result/gff-json")+"/"+self.refer_codename_str
        self.comand_line_list = ["cp", self.annotation_path, self.extraction_path+".gff"]
        self.runCommand()

        self.phrase_str = "==========\nStage: Convert GFF to JSON\n=========="
        self.printPhrase()

        header_list = self.requested_config_dict.get("header/gff3")
        CvtoJSON = libConvert.cvtDSVtoJSON()
        CvtoJSON.log_file_name = self.log_file_name
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
        Extract.log_file_name = self.log_file_name
        Extract.requested_argv_dict = {
            "gff.json"  : [self.extraction_path+".json"],
        }
        Extract.actor()

        self.printBlankLine()

        self.stopLog()

GeRef = genomerefer()
