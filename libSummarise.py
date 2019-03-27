#!/usr/bin/env python3
import pyWorkFlow, libConfig
import pyBriefer
import time, json, random
global helper_msg_block
helper_msg_block="""
--- README of library-mix-analysis-result.py ---
 Title:
  Library for Mixing analysis result

 Usage: # Replace * with related string
    Miski = libSummarise.miksing()
    Miski.requested_argv_dict = {
      "tribe" : tribe_list,
      "group" : group_list,
      "prefix" : self.requested_config_dict.get("result/*") + "/",
      "postfix" : "/*.json", OR "postfix" : "-*.json",
      "header" : [<sorted column name list>]
    }
    Miski.log_file_prefix_str = self.log_file_prefix_str + "Miski-"
    Miski.scanning()

    Miski.fusion()
    result_file_name = (
        self.requested_config_dict.get("result/*") + "/" + branch_name + "-*.json"
    )
    with open(result_file_name,"w") as result_file_handle:
        json.dump(Miski.result_dict,result_file_handle,indent=4,sort_keys=True)
    Miski.arrange()

--- README ---
"""
ConfigDict = libConfig.config()
class summary(pyWorkFlow.workflow):
    def personalize(self):
        # self.testing = True
        self.type = "library"
        self.helper_msg_str = helper_msg_block

        self.requested_argv_dict = {
            "branch" : "",
            "group" : [],
            "prefix" : "",
            "postfix" : "",
            "header" : []
        }

        self.comand_line_list = []
        ConfigDict.requested_dict = {}
        ConfigDict.requested_dict = {
            "result/log" : "",
            "data/replication" : {},
        }
        self.requested_config_dict = ConfigDict.get_batchly()
        self.script_name = "libSummarise"
        self.log_file_prefix_str = ConfigDict.get_str("result/log")+"/libSummarise-"

        self.repeat_boolean_dict = {}
    """
    def scanning(self):
        branch_name = self.requested_argv_dict.get("branch","")
        group_list = self.requested_argv_dict.get("group",[])
        prefix_path = self.requested_argv_dict.get("prefix","")
        postfix_path = self.requested_argv_dict.get("postfix","")
        head_list = self.requested_argv_dict.get("header",[])

        self.script_name = "Scanning of libSummarise"
        self.startLog()

        self.repeat_boolean_dict = {}
        first_dict = {}
        first_group_boolean = True
        for group_name in group_list:
            replication_list = self.requested_config_dict.get("data/replication").get(group_name)
            id_list = []
            for replication_name in replication_list:
                if replication_name != "":
                    replication_name = "-" + replication_name

                source_file_name = (
                    prefix_path + branch_name + "-"
                    + group_name + replication_name + postfix_path
                )
                source_file_handle = open(source_file_name,"r")
                source_file_dict = json.load(source_file_handle)

                if id_list == []:
                    id_list = list(source_file_dict.keys())

                if first_group_boolean:
                    for id in id_list:
                        key_value_dict = source_file_dict.get(id)
                        first_temp_dict = {}
                        for first_column_name in list(key_value_dict.keys()):
                            first_value_name = key_value_dict.get(first_column_name)
                            first_temp_dict.update({ first_column_name : first_value_name})
                            first_dict.update({ id : first_temp_dict})
                    first_group_boolean = False
                else:
                    for id in id_list:
                        key_value_dict = source_file_dict.get(id)
                        first_temp_dict = first_dict.get(id,{})
                        for column_name in list(key_value_dict.keys()):
                            query_value_name = key_value_dict.get(column_name)
                            first_value_name = first_temp_dict.get(column_name)
                            if query_value_name == first_value_name and self.repeat_boolean_dict.get(column_name, True):
                                    self.repeat_boolean_dict.update({ column_name : True })
                            else:
                                self.repeat_boolean_dict.update({ column_name : False })
                    """"""
                    debugger = pyBriefer.heading()
                    debugger.content_dict = self.repeat_boolean_dict
                    debugger.view()
                    """"""
        self.stopLog()
    """
    def fusion(self):
        branch_name = self.requested_argv_dict.get("branch","")
        group_list = self.requested_argv_dict.get("group",[])
        prefix_path = self.requested_argv_dict.get("prefix","")
        postfix_path = self.requested_argv_dict.get("postfix","")

        self.script_name = "Fusion of libSummarise"
        self.startLog()

        self.column_list_dict = {}
        self.result_dict = {}
        for group_name in group_list:
            replication_list = self.requested_config_dict.get("data/replication").get(group_name)
            for replication_name in replication_list:
                if replication_name != "":
                    replication_name = "-" + replication_name

                source_file_name = (
                    prefix_path + branch_name + "-"
                    + group_name + replication_name + postfix_path
                )
                source_file_handle = open(source_file_name,"r")
                source_file_dict = json.load(source_file_handle)

                for id in list(source_file_dict.keys()):
                    source_temp_dict = source_file_dict.get(id)
                    result_temp_dict = self.result_dict.get(id,{})
                    for column_name in list(source_temp_dict.keys()):
                        if not self.repeat_boolean_dict.get(column_name,False):
                            result_temp_dict.update(
                                { column_name+"("+group_name+")" : source_temp_dict.get(column_name) }
                            )

                            column_temp_list = self.column_list_dict.get(column_name,[])
                            if column_name+"("+group_name+")" not in column_temp_list:
                                column_temp_list.append(column_name+"("+group_name+")")
                                self.column_list_dict.update({ column_name : column_temp_list })
                            column_temp_list = []

                        elif result_temp_dict.get(column_name,"") == "":
                            result_temp_dict.update({ column_name : source_temp_dict.get(column_name) })
                    self.result_dict.update({ id : result_temp_dict })
        self.stopLog()

    def arrange(self):
        self.script_name = "Arrange of libSummarise"
        self.startLog()

        self.column_name_list = []
        sorted_header_list = self.requested_argv_dict.get("header",[])
        if sorted_header_list == []:
            sorted_header_list = list(self.repeat_boolean_dict.keys())

        sorted_header_str = "*@*"+"*@*".join(sorted_header_list)+"*@*"
        for column_name in list(self.column_list_dict.keys()):
            if "*@*"+column_name+"*@*" in sorted_header_str:
                temp_str = "*@*".join(self.column_list_dict.get(column_name))
                sorted_header_str = sorted_header_str.replace("*@*"+column_name+"*@*","*@*"+temp_str+"*@*")

        sorted_header_str = sorted_header_str[3:len(sorted_header_str)-3]
        self.column_name_list = sorted_header_str.split("*@*")
        print(list(self.repeat_boolean_dict.keys()))
        print(list(self.column_list_dict.keys()))
        print(self.column_name_list)
        self.stopLog()
