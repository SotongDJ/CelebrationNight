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
            "source" : ""
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
        self.refer_dict = {}
        self.output_dict = {}

    def actor(self):
        self.startLog()

        branch_name = self.requested_argv_dict.get("branch")
        target_name = self.requested_argv_dict.get("target")
        source_name = self.requested_argv_dict.get("source")

        refer_name_dict = self.requested_config_dict.get("data/refer")
        refer_name = refer_name_dict.get(branch_name)

        database_dict = self.requested_config_dict.get("refer/database")
        db_type_name = database_dict.get(refer_name)

        annotate_source_dict = self.requested_config_dict.get("database/annotation-source")
        source_pair_dict = annotate_source_dict.get(source_name+"-"+db_type_name)
        source_key_str = source_pair_dict.get("key")
        source_value_str = source_pair_dict.get("value")
        source_replace_list = source_pair_dict.get("replace")
        source_remove_front_list = source_pair_dict.get("delimiter(front-remove)")
        source_remove_back_list = source_pair_dict.get("delimiter(back-remove)")

        annotate_target_dict = self.requested_config_dict.get("database/annotation-target")
        target_pair_dict = annotate_target_dict.get(target_name+"-"+db_type_name)
        target_key_str = target_pair_dict.get("key")
        target_value_str = target_pair_dict.get("value")
        target_replace_list = target_pair_dict.get("replace")
        target_remove_front_list = target_pair_dict.get("delimiter(front-remove)")
        target_remove_back_list = target_pair_dict.get("delimiter(back-remove)")

        source_value_dict = self.refer_dict.get("{key:{value:[id]}}").get(source_key_str,{})
        source_id_dict = self.refer_dict.get("{key:{id:value}}").get(source_value_str,{})
        """
        debugger = pyBriefer.heading()
        debugger.content_dict = self.input_dict
        debugger.view()

        debugger.content_dict = self.refer_dict
        debugger.view()
        """
        if branch_name != "" and target_name != "" and source_name !="":
            for id_str in list(self.input_dict.keys()): # {id:{key:value}}
                target_key_value_dict = self.input_dict.get(id_str)

                if target_key_str in list(target_key_value_dict.keys()):
                    query_str = target_key_value_dict.get(target_key_str)

                    if target_replace_list != []:
                        for replace_str in target_replace_list:
                            query_str = query_str.replace(replace_str,"")

                    if target_remove_front_list != []:
                        for remove_front_str in target_remove_front_list:
                            if remove_front_str in query_str:
                                query_list = query_str.split(remove_front_str)
                                garbage_str = query_list.pop(0)
                                query_str = remove_front_str.join(query_list)

                    if target_remove_back_list != []:
                        for remove_back_str in target_remove_back_list:
                            if remove_back_str in query_str:
                                query_list = query_str.split(remove_back_str)
                                garbage_str = query_list.pop(-1)
                                query_str = remove_back_str.join(query_list)

                    if source_key_str == source_value_str:
                        result_str = query_str
                    else:
                        intermediate_id_name = source_value_dict.get(query_str,[""])[0]
                        result_str = source_id_dict.get(intermediate_id_name,"N/A")

                    write_boolean = False
                    if result_str == "N/A":
                        if len(target_key_value_dict.get(target_value_str,"")) < 3:
                            write_boolean = True
                    else:
                        write_boolean = True

                    if write_boolean:
                        if source_replace_list != []:
                            for replace_str in source_replace_list:
                                result_str = result_str.replace(replace_str,"")

                        if source_remove_front_list != []:
                            for remove_front_str in source_remove_front_list:
                                if remove_front_str in result_str:
                                    result_list = result_str.split(remove_front_str)
                                    garbage_str = result_list.pop(0)
                                    result_str = remove_front_str.join(result_list)

                        if source_remove_back_list != []:
                            for remove_back_str in source_remove_back_list:
                                if remove_back_str in result_str:
                                    result_list = result_str.split(remove_back_str)
                                    garbage_str = result_list.pop(-1)
                                    result_str = remove_back_str.join(result_list)

                        target_key_value_dict.update({ target_value_str : result_str })
                        self.input_dict.update({ id_str : target_key_value_dict })

        self.output_dict = self.input_dict
        self.stopLog()
