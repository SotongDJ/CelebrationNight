#!/usr/bin/env python3
import pyWorkFlow, libConfig, libConvert, libInsert, libSummarise
import time, json
global helper_msg_block
helper_msg_block="""
--- README of act15-stringtie-summary.py ---
 Title:
  Summarizer of StringTie

 Usage:
  python3 act15-stringtie-result.py -b <BRANCH BRANCH BRANCH ... > \\
    -g <GROUP GROUP GROUP ... >

 CAUTION:
  Act15 required libConvert, libInsert, libSummarise
  Act15 required result from Act01
  Each GROUP must separate with space
  Don't allowed spacing in GROUP name

--- README ---
"""
ConfigDict = libConfig.config()
class stingtieResult(pyWorkFlow.workflow):
    def personalize(self):
        # self.testing = True
        self.type = "script"
        self.helper_msg_str = helper_msg_block

        self.requested_argv_dict = {
            "branch" : [],
            "group" : []
        }
        self.SynonymDict.input(ConfigDict.get_dict("synom"))
        self.synchornize()

        self.comand_line_list = []
        self.script_name = "act15-stringtie-result"
        ConfigDict.requested_dict = {}
        ConfigDict.requested_dict = {
            "result/DESeq2" : "",
            "result/ballgown" : "",
            "result/st-result" : "",
            "result/stringtie" : "",
            "result/gff-json": "",
            "result/log" : "",
            "bin/prepDE" : "",
            "data/refer" : {},
            "data/replication" : {},
            "header/TranscriptExpression" : [],
            "header/GeneExpression" : [],
        }
        self.requested_config_dict = ConfigDict.get_batchly()
        self.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act15-stire-"

    def actor(self):
        branch_list = self.requested_argv_dict.get("branch",[])
        group_list = self.requested_argv_dict.get("group",[])

        refer_dict = {}
        for branch_name in branch_list:
            refer_temp_dict = self.requested_config_dict.get("data/refer",{})
            if branch_name in list(refer_temp_dict.keys()):
                refer_temp_str = refer_temp_dict.get(branch_name)
                gff_json_path = self.requested_config_dict.get("result/gff-json")
                refer_file_name = gff_json_path + "/" + refer_temp_str + "-attribution-related.json"
                refer_dict.update({ refer_temp_str : refer_file_name })

        self.startLog()

        self.target_file_list = []
        self.target_file_list.append(self.requested_config_dict.get("result/stringtie"))
        self.target_file_list.append(self.requested_config_dict.get("result/ballgown"))
        self.target_file_list.append(self.requested_config_dict.get("result/st-result"))
        self.target_file_list.append(self.requested_config_dict.get("result/DESeq2"))
        self.checkPath()

        self.phrase_str = "==========\nStage: Convert TSV/CTAB to JSON\n=========="
        self.printPhrase()

        source_file_list = []
        for branch_name in branch_list:
            for group_name in group_list:
                replication_list = self.requested_config_dict.get("data/replication").get(group_name)
                for replication_name in replication_list:
                    if replication_name != "":
                        replication_name = "-"+replication_name

                    souce_file_temp_name = (
                        self.requested_config_dict.get("result/ballgown")
                        +"/"+branch_name+"-"+group_name+replication_name
                        +"/t_data.ctab"
                    )
                    self.target_file_path = souce_file_temp_name
                    souce_file_temp_boolean = self.checkFile()
                    self.target_file_path = souce_file_temp_name.replace(".ctab",".json")
                    json_file_temp_boolean = self.checkFile()

                    if souce_file_temp_boolean and not json_file_temp_boolean:
                        source_file_list.append(souce_file_temp_name)

        if source_file_list != []:
            CvtoJSON = libConvert.cvtDSVtoJSON()
            CvtoJSON.log_file_name = self.log_file_name
            CvtoJSON.requested_argv_dict = {
                "files": source_file_list,
                "refer_column": "t_id",
                "prefix": "",
                "header": [],
                "headless": False,
                "delimiter": "\t"
            }
            CvtoJSON.filasi = "libConvert.cvtDSVtoJSON"
            CvtoJSON.actor()

        source_file_list = []
        for branch_name in branch_list:
            for group_name in group_list:
                replication_list = self.requested_config_dict.get("data/replication").get(group_name)
                for replication_name in replication_list:
                    if replication_name != "":
                        replication_name = "-"+replication_name

                    souce_file_temp_name = (
                        self.requested_config_dict.get("result/stringtie")
                        +"/"+branch_name+"-"+group_name+replication_name+"-gene.tsv"
                    )
                    self.target_file_path = souce_file_temp_name
                    souce_file_temp_boolean = self.checkFile()
                    self.target_file_path = souce_file_temp_name.replace(".tsv",".json")
                    json_file_temp_boolean = self.checkFile()

                    if souce_file_temp_boolean and not json_file_temp_boolean:
                        source_file_list.append(souce_file_temp_name)

        if source_file_list != []:
            CvtoJSON = libConvert.cvtDSVtoJSON()
            CvtoJSON.log_file_name = self.log_file_name
            CvtoJSON.requested_argv_dict = {
                "files": source_file_list,
                "refer_column": "Gene ID",
                "prefix": "",
                "header": [],
                "headless": False,
                "delimiter": "\t"
            }
            CvtoJSON.filasi = "libConvert.cvtDSVtoJSON"
            CvtoJSON.actor()

        self.phrase_str = "==========\nStage: Scanning for Variable Parts\n=========="
        self.printPhrase()

        Transki = libSummarise.summary()
        Transki.log_file_name = self.log_file_name
        Transki.requested_argv_dict = {
            "branch" : branch_list,
            "group" : group_list,
            "prefix" : self.requested_config_dict.get("result/ballgown") + "/",
            "postfix" : "/t_data.json",
            "header" : self.requested_config_dict.get("libConvert/TranscriptExpression")
        }
        Transki.log_file_prefix_str = self.log_file_prefix_str + "sca-Transki-"
        Transki.scanning()

        Geniski = libSummarise.summary()
        Geniski.log_file_name = self.log_file_name
        Geniski.requested_argv_dict = {
            "branch" : branch_list,
            "group" : group_list,
            "prefix"  : self.requested_config_dict.get("result/stringtie") + "/",
            "postfix" : "-gene.json",
            "header"  : self.requested_config_dict.get("libConvert/GeneExpression")
        }
        Geniski.log_file_prefix_str = self.log_file_prefix_str + "sca-Geniski-"
        Geniski.scanning()

        if branch_list != []:
            for branch_name in branch_list:
                self.phrase_str = "==========\nStage: Merging\n=========="
                self.printPhrase()

                Transki.log_file_prefix_str = self.log_file_prefix_str + "fus-Transki-"
                Transki.fusion()
                result_file_name = (
                    self.requested_config_dict.get("result/st-result") + "/"
                    + branch_name + "-" + "TranscriptExpression.json"
                )
                with open(result_file_name,"w") as result_file_handle:
                    json.dump(Transki.result_dict,result_file_handle,indent=4,sort_keys=True)
                Transki.log_file_prefix_str = self.log_file_prefix_str + "ara-Transki-"
                Transki.arrange()

                Geniski.log_file_prefix_str = self.log_file_prefix_str + "fus-Geniski-"
                Geniski.fusion()
                result_file_name = (
                    self.requested_config_dict.get("result/st-result") + "/"
                    + branch_name + "-" + "GeneExpression.json"
                )
                with open(result_file_name,"w") as result_file_handle:
                    json.dump(Geniski.result_dict,result_file_handle,indent=4,sort_keys=True)
                Geniski.log_file_prefix_str = self.log_file_prefix_str + "ara-Geniski-"
                Geniski.arrange()

        self.phrase_str = "==========\nStage: Extract Data for DESeq\n=========="
        self.printPhrase()

        deseg_file_name = self.requested_config_dict.get("result/DESeq2") + "/stringtie-list.txt"
        deseg_file_handle = open(deseg_file_name,"w")
        deseg_file_handle.write("")
        deseg_file_handle.close()

        for branch_name in branch_list:
            for group_name in group_list:
                ballgown_line_str = (
                    group_name + " "
                    + self.requested_config_dict.get("result/ballgown") + "/"
                    + branch_name + "-" + group_name + "-ballgown.gtf" + "\n"
                )

                with open(deseg_file_name,"a") as deseg_file_handle:
                    deseg_file_handle.write(ballgown_line_str)

        self.comand_line_list = [
            "python2", self.requested_config_dict.get("bin/prepDE"),
            "-i", deseg_file_name
        ]
        self.runCommand()

        self.comand_line_list = [
            "mv", "gene_count_matrix.csv", self.requested_config_dict.get("result/DESeq2") + "/"
        ]
        self.runCommand()

        self.comand_line_list = [
            "mv", "transcript_count_matrix.csv", self.requested_config_dict.get("result/DESeq2") + "/"
        ]
        self.runCommand()

        self.comand_line_list = []

        if refesi != "" and tribe_list != []:
            self.phrase_str = "==========\nStage 5 : Combine Description from GFF3\n=========="
            self.printPhrase()

            tribe_str = tribe_list[0]
            tiposi = self.requested_config_dict.get("type/database").get(tribe_str)

            GeneID = libsnm.geneid()
            GeneID.requested_argv_dict = {
                "description" : refesi ,
                "basement" : Transki.resusi ,
            }
            tagadi = self.requested_config_dict.get("target/libsnm").get(tiposi+"-transcript")
            GeneID.requested_argv_dict.update(tagadi)
            GeneID.filasi = "libsnm.geneid"
            GeneID.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act15-stire-geneid-"
            GeneID.actor()

            GeneID.requested_argv_dict = {
                "description" : refesi ,
                "basement" : Geniski.resusi ,
            }
            tagadi = self.requested_config_dict.get("target/libsnm").get(tiposi+"-gene")
            GeneID.requested_argv_dict.update(tagadi)
            GeneID.filasi = "libsnm.geneid"
            GeneID.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act15-stire-geneid-"
            GeneID.actor()

            self.phrase_str = "==========\nStage 6 : Convert JSON back to TSV/CTAB\n=========="
            self.printPhrase()
        else:
            self.phrase_str = "==========\nStage 5 : Convert JSON back to TSV/CTAB\n=========="
            self.printPhrase()

        CvtoTAB = libConvert.cvtJSONtoDSV()
        CvtoTAB.filasi = "libConvert.cvtJSONtoDSV"
        CvtoTAB.log_file_prefix_str = self.requested_config_dict.get("result/log")+"/act15-stire-covetab-"
        CvtoTAB.requested_argv_dict = {
            "files" : [Transki.resusi],
            "column" : Transki.coluli
        }
        CvtoTAB.actor()

        CvtoTAB.requested_argv_dict = {
            "files" : [Geniski.resusi],
            "column" : Geniski.coluli
        }
        CvtoTAB.actor()

        self.printBlankLine()

        self.stopLog()

        self.phrase_str = "\n\n"
        self.printPhrase()

StingtieResult = stingtieResult()
