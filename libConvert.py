#!/usr/bin/env python3
import sys, pprint, json
import pyWorkFlow
global helper_msg_block
helper_msg_block="""
   --- README of library-tab ---
  Title:
    Conversion tool for JSON and TSV/CTAB

  Usage:
    import libconvert

    CvtoJSON = libConvert.cvtDSVtoJSON()
    CvtoJSON.requested_argv_dict = {
        "files" : [<INPUT>,<INPUT>......] ,
        "id" : "" ,
        "column": < Column separate by tab > # for headless file
    }
    CvtoJSON.actor()

    CvtoTAB = libConvert.cvtJSONtoDSV()
    CvtoTAB.requested_argv_dict = {
        "files" : [<INPUT>,<INPUT>......] ,
        "column": [<NAME>,<NAME>......] # for sorting
    }
    CvtoTAB.actor()

   --- README ---
"""
class cvtDSVtoJSON(pyWorkFlow.workflow):
    def personalize(self):
        # self.testing = True
        self.type = "library"

        self.requested_argv_dict = {
            "files": [],
            "refer_column": "",
            "prefix": "",
            "header": [],
            "headless": True,
            "delimiter": "\t"
        }
        self.synchornize()

        self.target_file_path = ""

        self.comand_line_list=[]

        self.script_name = "libConvert.cvtDSVtoJSON"
        self.requested_config_dict = {}
        self.log_file_prefix_str = "temp/tmp-"

    def actor(self):
        source_files_list = self.requested_argv_dict.get("files",[])
        refer_column_name = self.requested_argv_dict.get("refer_column","")
        prefix_str = self.requested_argv_dict.get("prefix","")
        header_list = self.requested_argv_dict.get("header",[])
        headless_boolean = self.requested_argv_dict.get("headless",True)
        delimiter_str = self.requested_argv_dict.get("delimiter","\t")
        self.startLog()

        for source_file_name in source_files_list:
            self.phrase_str = pprint.pformat(source_file_name)
            self.printTimeStamp()

            name_temp_list = source_file_name.split(".")
            name_temp_list[-1] = "json"
            result_file_name = ".".join(name_temp_list)
            relation_file_name = result_file_name.replace(".json","-related.json")

            self.target_file_path = result_file_name
            result_file_boolean = self.checkFile()
            self.target_file_path = relation_file_name
            relation_file_boolean = self.checkFile()

            if not result_file_boolean or not relation_file_boolean :
                lines_list = open(source_file_name).read().splitlines()
                first_line_str = lines_list[0]

                position_dict = {} # {numbering:key}

                id_dict = {} # {id:{key:value}}
                relation_dict = {
                    "{key:{value:[id]}}" : {},
                    "{key:{id:value}}" : {}
                }

                if not headless_boolean:
                    if header_list == []:
                        header_list = first_line_str.split(delimiter_str)
                else:
                    column_temp_list = first_line_str.split(delimiter_str)
                    max_digit_num = len(str(len(column_temp_list)))
                    for column_num in range(len(column_temp_list)):
                        digit_num = len(str(len(column_num)))
                        if digit_num != max_digit_num:
                            diff_digit_num = max_digit_num - digit_num
                        else:
                            diff_digit_num = 0

                        header_list.append(
                            "Column_"+("0"*diff_digit_num)+str(column_num)
                        )

                for number in range(len(header_list)):
                    if header_list[number] not in position_dict.values():
                        position_dict.update({ number : header_list[number] })
                    if header_list[number] not in relation_dict.get("{key:{value:[id]}}").keys():
                        relation_dict.get("{key:{value:[id]}}").update({ header_list[number] :{} })
                    if header_list[number] not in relation_dict.get("{key:{id:value}}").keys():
                        relation_dict.get("{key:{id:value}}").update({ header_list[number] :{} })

                refer_column_exist_boolean = False
                if refer_column_name != "":
                    refer_column_exist_boolean = True

                line_id_num = 0
                for line_str in lines_list:
                    if "#" not in line_str:
                        value_temp_list = line_str.split(delimiter_str)
                        value_temp_dict = {}
                        id_name = ""

                        if not refer_column_exist_boolean:
                            line_id_num = line_id_num + 1
                            id_name = prefix_str + str(line_id_num)

                        for number in range(len(list(position_dict.keys()))):
                            header_list_str = position_dict.get(number)
                            value_temp_dict.update({ header_list_str : value_temp_list[number]})

                            if header_list_str == refer_column_name and refer_column_exist_boolean:
                                id_name = value_temp_list[number]

                        id_dict.update({ id_name : value_temp_dict })

                        value_temp_dict = {} # {key:{value:[id]}}
                        id_temp_dict = {} # {key:{id:value}}

                        for number in range(len(list(position_dict.keys()))):
                            header_list_str = position_dict.get(number) # key
                            value_str = value_temp_list[number] # value

                            value_temp_dict = relation_dict.get("{key:{value:[id]}}").get(header_list_str,{})
                            id_temp_dict = relation_dict.get("{key:{id:value}}").get(header_list_str,{})

                            id_list = value_temp_dict.get(value_temp_list[number],[])
                            id_list.append(id_name)

                            value_temp_dict.update({ value_temp_list[number] : id_list })
                            id_temp_dict.update({ id_name : value_str })

                            relation_dict.get("{key:{value:[id]}}").update({ header_list_str : value_temp_dict })
                            relation_dict.get("{key:{id:value}}").update({ header_list_str : id_temp_dict })


                with open(result_file_name,"w") as result_file_handle:
                    json.dump(id_dict,result_file_handle,indent=4,sort_keys=True)

                with open(relation_file_name,"w") as relation_file_handle:
                    json.dump(relation_dict,relation_file_handle,indent=4,sort_keys=True)

        self.stopLog()

class cvtJSONtoDSV(pyWorkFlow.workflow):
    def personalize(self):
        # self.testing = True
        self.type = "library"

        self.requested_argv_dict = {
            "files" : [],
            "header" : [],
            "delimiter": "\t"
        }
        self.synchornize()

        self.target_file_path = ""

        self.comand_line_list=[]

        self.script_name = "libConvert.cvtJSONtoDSV"
        self.requested_config_dict = {}
        self.log_file_prefix_str = "temp/tmp-"

    def actor(self):
        source_files_list = self.requested_argv_dict.get("files",[])
        header_list = self.requested_argv_dict.get("header",[])
        delimiter_str = self.requested_argv_dict.get("delimiter","\t")
        self.startLog()

        for source_file_name in source_files_list:
            source_file_handle = open(source_file_name,'r')
            source_json_dict = json.load(source_file_handle)

            if header_list == []:
                column_name_set = set()
                value_temp_dict = dict()
                for id_name in list(source_json_dict.keys()):
                    value_temp_dict = source_json_dict.get(id_name,{})
                    column_name_set.update(set(value_temp_dict.keys()))
                header_tuple = tuple(sorted(column_name_set))
            else:
                header_tuple = tuple(header_list)

            with open(source_file_name.replace(".json",".dsv"),"w") as result_file_handle:
                result_file_handle.write("id"+delimiter_str+delimiter_str.join(header_tuple)+"\n")
                for id_name in list(source_json_dict.keys()):
                    line_str = id_name
                    value_temp_dict = dict()
                    value_temp_dict = source_json_dict.get(id_name,{})
                    for column_name in header_tuple:
                        line_str = line_str + delimiter_str + value_temp_dict.get(column_name,"")
                    result_file_handle.write(line_str+"\n")

        self.stopLog()

class attributionExtractor(pyWorkFlow.workflow):
    def personalize(self):
        # self.testing = True
        self.type = "library"

        self.helper_msg_str = helper_msg_block

        self.requested_argv_dict = {
            "gff.json": [],
        }

        self.comand_line_list = []
        self.script_name = "libConvert.attributionExtractor"
        self.requested_config_dict = {}
        self.log_file_prefix_str = "temp/tmp-"

    def actor(self):
        source_files_list = self.requested_argv_dict.get("gff.json",[])
        self.startLog()

        for source_file_name in source_files_list:
            target_file_name = source_file_name.replace("-related.json",".json")
            target_file_name = target_file_name.replace(".json","-related.json")

            self.target_file_path = target_file_name
            target_file_boolean = self.checkFile()

            if target_file_boolean:
                self.phrase_str = "Extracting "+target_file_name
                self.printTimeStamp()

                target_file_handle = open(target_file_name,'r')
                target_json_dict = json.load(target_file_handle)

                key_id_value_dict = target_json_dict.get('{key:{id:value}}')
                raw_temp_dict = key_id_value_dict.get('Attributes')
                result_dict = {} # id=[key:value]
                relation_dict = {
                    "{key:{value:[id]}}" : {},
                    "{key:{id:value}}" : {}
                }

                for gffid_name in list(raw_temp_dict.keys()):
                    attribution_str = raw_temp_dict.get(gffid_name)[0]
                    attribution_temp_dict = {}

                    for paired_set_str in attribution_str.split(";"):
                        paired_set_list = paired_set_str.split("=")
                        key_str = paired_set_list[0]
                        value_str = paired_set_list[1]
                        attribution_temp_dict.update({ key_str : value_str })

                        value_temp_dict = relation_dict.get("{key:{value:[id]}}").get(key_str,{})
                        value_temp_dict.update({ value_str : gffid_name })
                        relation_dict.get("{key:{value:[id]}}").update({ key_str : value_temp_dict })

                        gffid_temp_dict = relation_dict.get("{key:{id:value}}").get(key_str,{})
                        gffid_temp_dict.update({ gffid_name : value_str })
                        relation_dict.get("{key:{id:value}}").update({ key_str : gffid_temp_dict })

                    result_dict.update({ gffid_name : attribution_temp_dict })


                result_file_name = target_file_name.replace("-related.json","-attribution.json")
                with open(result_file_name,"w") as result_file_handle:
                    json.dump(result_dict,result_file_handle)

                relation_file_name = target_file_name.replace("-related.json","-attribution-related.json")
                with open(relation_file_name,"w") as relation_file_handle:
                    json.dump(relation_dict,relation_file_handle)

                """
                attribution_file_name = target_file_name.replace("-related.json","-atr-gffid[key-value].json")
                with open(attribution_file_name,"w") as attribution_file_handle:
                    json.dump(result_dict.get("id=[key:value]"),attribution_file_handle)

                value_file_name = target_file_name.replace("-related.json","-atr-key[value-gffid].json")
                with open(value_file_name,"w") as value_file_handle:
                    json.dump(result_dict.get("{key:{value:[id]}}"),value_file_handle)

                gffid_file_name = target_file_name.replace("-related.json","-atr-key[gffid-value].json")
                with open(gffid_file_name,"w") as gffid_file_handle:
                    json.dump(result_dict.get("{key:{id:value}}"),gffid_file_handle)
                """

        self.stopLog()
