#!/usr/bin/env python3
import pyWorkFlow, libConfig
import pyBriefer
import sys, pprint, json
global helper_msg_block
helper_msg_block="""
   --- README of library-search-and-merge ---
  Title:
    Inserting Tool for Annotation

  Usage:
    import libInsert
    Insert = libInsert.inserting()
    Insert.log_file_name = self.log_file_name # follow host
    Insert.requested_argv_dict = {
        "branch" : < BRANCH >,
        "target" : < PATTERN >,
        # "database/annotation-target" in global config.json
        "refer" : < PATH of REFERENCE >
    }
    Insert.input_dict = < INPUT DICTIONARY >
    Insert.actor()
   --- README ---
"""
class inserting(pyWorkFlow.workflow):
    def personalize(self):
        # self.testing = True
        self.type = "library"
        self.helper_msg_str = helper_msg_block

        self.requested_argv_dict = {
            "branch" : "",
            "target" : "",
            "refer" : ""
        }

        ConfigDict = libConfig.config()
        self.comand_line_list=[]
        ConfigDict.requested_dict = {}
        ConfigDict.requested_dict = {
            "result/log" : "",
            "result/gff-json" : "",
            "data/refer" : {},
            "refer/database" : {},
            "database/annotation-source" : {},
            "database/annotation-target" : {},
        }
        self.requested_config_dict = ConfigDict.get_batchly()

        self.script_name = "library-search-and-merge"
        self.log_file_prefix_str = "temp/tmp-"

        self.input_dict = {} # {id:{key:value}}
        self.output_dict = {}

    def actor(self):
        self.startLog()

        branch_name = self.requested_argv_dict.get("branch")
        target_name = self.requested_argv_dict.get("target")
        refer_file_path = self.requested_argv_dict.get("refer")

        refer_name_dict = self.requested_config_dict.get("data/refer")
        refer_name = refer_name_dict.get(branch_name)

        database_dict = self.requested_config_dict.get("refer/database")
        db_type_name = database_dict.get(refer_name)

        annotate_source_dict = self.requested_config_dict.get("database/annotation-source")
        source_pair_dict = annotate_source_dict.get(db_type_name)
        source_key_str = source_pair_dict.get("key")
        source_value_str = source_pair_dict.get("value")

        annotate_target_dict = self.requested_config_dict.get("database/annotation-target")
        target_set_dict = annotate_target_dict.get(target_name+"-"+db_type_name)
        target_key_str = target_set_dict.get("key")
        target_value_str = target_set_dict.get("value")
        target_replace_str = target_set_dict.get("replace")

        refer_file_handle = open(refer_file_path,"r")
        refer_file_dict = json.load(refer_file_handle)

        value_temp_dict = refer_file_dict.get("{key:{value:[id]}}").get(source_key_str)
        id_temp_dict = refer_file_dict.get("{key:{id:value}}").get(source_value_str)
        """
        debugger = pyBriefer.heading()
        debugger.content_dict = self.input_dict
        debugger.view()
        """
        if branch_name != "" and target_name != "":
            for id in list(self.input_dict.keys()): # {id:{key:value}}
                key_value_dict = self.input_dict.get(id)
                if target_key_str in list(key_value_dict.keys()):
                    value_temp_str = key_value_dict.get(target_key_str)
                    value_temp_str = value_temp_str.replace(target_replace_str,"")

                    convert_id_name = value_temp_dict.get(value_temp_str,"")
                    final_str = id_temp_dict.get(convert_id_name,"N/A")

                    key_value_dict.update({ target_value_str : final_str })
                    self.input_dict.update({ id : key_value_dict })

        self.output_dict = self.input_dict
        self.stopLog()
