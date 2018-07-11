#!/usr/bin/env python3
import sys, pprint, json
import libWorkFlow
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
class cvtDSVtoJSON(libWorkFlow.workflow):
    def redirecting(self):
        """"""
    def personalize(self):
        # self.testing = True

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

        self.script_name = "libConvert.py"
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
            column_file_name = result_file_name.replace(".json","-column.json")

            self.target_file_path = result_file_name
            result_file_boolean = self.check_file()
            self.target_file_path = column_file_name
            column_file_boolean = self.check_file()

            if not result_file_boolean or not column_file_boolean :
                lines_list = open(source_file_name).read().splitlines()
                first_line_str = lines_list[0]

                position_x_column_dict = {}

                id_x_value_dict = {}
                column_x_value_dict = {}

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
                    if header_list[number] not in position_x_column_dict.values():
                        position_x_column_dict.update({ number : header_list[number] })
                    if header_list[number] not in column_x_value_dict.keys():
                        column_x_value_dict.update({ header_list[number] :{} })

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

                        for number in range(len(list(position_x_column_dict.keys()))):
                            header_list_str = position_x_column_dict.get(number)
                            value_temp_dict.update({ header_list_str : value_temp_list[number]})

                            if header_list_str == refer_column_name and refer_column_exist_boolean:
                                id_name = value_temp_list[number]

                        id_x_value_dict.update({ id_name : value_temp_dict })

                        for number in range(len(list(position_x_column_dict.keys()))):
                            header_list_str = position_x_column_dict.get(number)

                            column_temp_dict = column_x_value_dict.get(header_list_str,{})
                            id_list = column_temp_dict.get(value_temp_list[number],[])

                            id_list.append(id_name)

                            column_temp_dict.update({ value_temp_list[number] : id_list })
                            column_x_value_dict.update({ header_list_str : column_temp_dict })


                with open(result_file_name,"w") as result_file_handle:
                    json.dump(id_x_value_dict,result_file_handle,indent=4,sort_keys=True)

                with open(column_file_name,"w") as column_file_handle:
                    json.dump(column_x_value_dict,column_file_handle,indent=4,sort_keys=True)

        self.stopLog()

class cvtJSONtoDSV(libWorkFlow.workflow):
    def redirecting(self):
        """"""

    def personalize(self):
        # self.testing = True

        self.requested_argv_dict = {
            "files" : [],
            "header" : [],
            "delimiter": "\t"
        }
        self.synchornize()

        self.target_file_path = ""

        self.comand_line_list=[]

        self.script_name = "libConvert.py"
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

            with open(source_file_name.replace(".json",".tsv"),"w") as result_file_handle:
                result_file_handle.write("id"+delimiter_str+delimiter_str.join(header_tuple)+"\n")
                for id_name in list(source_json_dict.keys()):
                    line_str = id_name
                    value_temp_dict = dict()
                    value_temp_dict = source_json_dict.get(id_name,{})
                    for column_name in header_tuple:
                        line_str = line_str + delimiter_str + value_temp_dict.get(column_name,"")
                    result_file_handle.write(line_str+"\n")

        self.stopLog()

class attributionExtractor(libWorkFlow.workflow):
    def redirecting(self):
        """"""

    def personalize(self):
        # self.testing = True
        self.helper_msg_str = helper_msg_block

        self.requested_argv_dict = {
            "gff.json": [],
            "refer": "",
        }

        self.comand_line_list = []
        self.script_name = "libConvert.py"
        self.requested_config_dict = {}
        self.log_file_prefix_str = "temp/tmp-"

    def actor(self):
        """"""
