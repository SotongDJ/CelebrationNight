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

    CvtoJSON = libconvert.cvtTABtoJSON()
    CvtoJSON.requested_argv_dict = {
        "files" : [<INPUT>,<INPUT>......] ,
        "id" : "" ,
        "column": < Column separate by tab > # for headless file
    }
    CvtoJSON.actor()

    CvtoTAB = libconvert.cvtJSONtoTAB()
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
class cvtTABtoJSON(libWorkFlow.workflow):
    def redirecting(self):
        """"""
    def personalize(self):
        # self.testing = True

        self.requested_argv_dict = {
            "files"  : [],
            "id"     : "",
            "prefix" : "",
            "column" : ""
        }
        self.synchornize()

        self.target_file_path = ""

        self.comand_line_list=[]

        self.script_name_str = "libconvert.py"
        self.requested_config_dict = {}
        self.log_file_prefix_str = "temp/tmp-"

    def actor(self):
        source_files_list = self.requested_argv_dict.get("files" ,[])
        column_id_name = self.requested_argv_dict.get("id"    ,"")
        prefix_str = self.requested_argv_dict.get("prefix","")
        column_name_str = self.requested_argv_dict.get("column","")
        self.startLog()

        self.phrase_str = pprint.pformat((
            source_files_list,column_id_name,prefix_str,column_name_str
        ))
        self.printTimeStamp()

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

                name_dict = {}

                id_x_value_dict = {}
                column_x_value_dict = {}

                if column_name_str != "":
                    column_temp_list = column_name_str.split("	")
                    for number in range(len(metali)):
                        if column_temp_list[number] not in name_dict.values():
                            name_dict.update({ number : column_temp_list[number] })
                        if column_temp_list[number] not in column_x_value_dict.keys():
                            column_x_value_dict.update({ column_temp_list[number] :{} })
                    header_boolean = False
                else:
                    header_boolean = True

                if column_id_name != "":
                    column_id_exist_boolean = True
                else:
                    column_id_exist_boolean = False

                line_id_num = 0
                for line_str in lines_list:
                    if header_boolean:
                        column_temp_list = line_str.split("	")
                        for column_num in range(len(column_temp_list)):
                            if column_temp_list[column_num] not in name_dict.values():
                                name_dict.update({ column_num : column_temp_list[column_num] })
                            if column_temp_list[column_num] not in column_x_value_dict.keys():
                                column_x_value_dict.update({ column_temp_list[column_num] :{} })
                        header_boolean = False
                    elif "#" not in line_str:
                        value_temp_list = line_str.split("	")
                        value_temp_dict = {}
                        id_name_str = ""

                        if not column_id_exist_boolean:
                            line_id_num = line_id_num + 1
                            id_name_str = prefix_str + str(line_id_num)

                        for number in range(len(list(name_dict.keys()))):
                            column_name_str = name_dict.get(number)
                            value_temp_dict.update({ column_name_str : value_temp_list[number]})

                            if column_name_str == column_id_name and column_id_exist_boolean:
                                id_name_str = value_temp_list[number]

                        id_x_value_dict.update({ id_name_str : value_temp_dict })

                        for number in range(len(list(name_dict.keys()))):
                            column_name_str = name_dict.get(number)

                            column_temp_dict = column_x_value_dict.get(column_name_str,{})
                            id_list = column_temp_dict.get(value_temp_list[number],[])

                            id_list.append(id_name_str)

                            column_temp_dict.update({ value_temp_list[number] : id_list })
                            column_x_value_dict.update({ column_name_str : column_temp_dict })


                with open(result_file_name,"w") as result_file_handle:
                    json.dump(id_x_value_dict,result_file_handle,indent=4,sort_keys=True)

                with open(column_file_name,"w") as column_file_handle:
                    json.dump(column_x_value_dict,column_file_handle,indent=4,sort_keys=True)
        self.stopLog()

class cvtJSONtoTAB(libWorkFlow.workflow):
    def redirecting(self):
        """"""

    def personalize(self):
        # self.testing = True

        self.requested_argv_dict = {
            "files" : [],
            "column" : []
        }
        self.synchornize()

        self.target_file_path = ""

        self.comand_line_list=[]

        self.script_name_str = "libconvert.py"
        self.requested_config_dict = {}
        self.log_file_prefix_str = "temp/tmp-"

    def actor(self):
        source_files_list = self.requested_argv_dict.get("files",[])
        column_name_list = self.requested_argv_dict.get("column",[])
        self.startLog()

        self.phrase_str = pprint.pformat(source_files_list)
        self.printTimeStamp()

        for source_file_name in source_files_list:
            source_file_handle = open(source_file_name,'r')
            source_json_dict = json.load(source_file_handle)

            if column_name_list == []:
                column_name_set = set()
                value_temp_dict = dict()
                for id_name in list(source_json_dict.keys()):
                    value_temp_dict = source_json_dict.get(id_name,{})
                    column_name_set.update(set(value_temp_dict.keys()))
                column_name_tuple = tuple(sorted(column_name_set))
            else:
                column_name_tuple = tuple(column_name_list)

            with open(source_file_name.replace(".json",".tsv"),"w") as result_file_handle:
                result_file_handle.write("id"+"	"+"	".join(column_name_tuple)+"\n")
                for id_name in list(source_json_dict.keys()):
                    line_str = id_name
                    value_temp_dict = dict()
                    value_temp_dict = source_json_dict.get(id_name,{})
                    for column_name in column_name_tuple:
                        line_str = line_str + "	" + value_temp_dict.get(column_name,"")
                    result_file_handle.write(line_str+"\n")

        self.stopLog()
