#!/usr/bin/env python3
import pprint, time, json, sys
from subprocess import call
global helper_msg_block
helper_msg_block="""
   --- README of WorkFlow Framework v2.3 ---
 Title:
    General class for bio-info-misc project

 Usage:
    import libWorkFlow
    class <CLASS_NAME>(libWorkFlow.workflow):

        def personalize(self):
            # self.testing = True

            self.requested_argv_dict = {
                < VAR_NAME_A > : < VAR_VALUE > ,
                < VAR_NAME_B > : < VAR_VALUE > ,
                < VAR_NAME_C > : < VAR_VALUE > ,
            }
            self.synchornize()

            self.target_file_path = ""

            self.comand_line_list=[]

            self.script_name = < Library Name >
            self.requested_config_dict = {}
            self.log_file_prefix_str = < Path of Log Files >

        def actor(self):
            < VAR_A > = self.requested_argv_dict.get(< VAR_NAME_A >,"")
            < VAR_B > = self.requested_argv_dict.get(< VAR_NAME_B >,"")
            < VAR_C > = self.requested_argv_dict.get(< VAR_NAME_C >,"")
            print((< VAR_A >, < VAR_B >, < VAR_C >))

            self.startLog()

            self.target_file_path = < TARGET_FILE >
            self.checkPath()

            self.runCommand()

            self.stopLog()

    Ano = <CLASS_NAME>()
    Ano.actor()

   --- README ---
"""
class refined_dict:
    def input(self,socedi):
        if type(socedi) == type(dict()):
            self.content_dict.update(socedi)

    def list(self):
        return list(self.content_dict.keys())

    def get_str(self,askasi):
        return self.content_dict.get(askasi,"")

    def get_list(self,askasi):
        return self.content_dict.get(askasi,[])

    def vomit(self):
        return self.content_dict

    def __init__(self):
        self.content_dict = {}

class workflow:

    def __init__(self):
        self.system_argv_list = sys.argv
        self.arranged_argv_dict = {}
        self.begin_time_str = ""
        self.log_file_name = ""

        self.current_time_str = ""
        self.phrase_str = ""
        self.delimiter_str = ""
        self.list_list = []

        self.target_file_path = ""
        self.target_file_list = []

        self.testing = False
        self.requested_argv_dict = {}
        self.SynonymDict = refined_dict()
        self.arrangeArgv()
        self.personalize()

        self.redirecting()

    def personalize(self):
        # self.testing = True
        self.helper_msg_str = helper_msg_block

        self.requested_argv_dict = {
            "hello" : ""
        }
        self.synchornize()

        self.comand_line_list = ['echo','wahaha']

        self.script_name = "libWorkFlow.py"
        self.requested_config_dict = {
            "prefix/wawa" : "haha/wulala"
        }
        self.SynonymDict.input({})
        self.log_file_prefix_str = "temp/temp-"

    def actor(self):
        tribe_list = self.requested_argv_dict.get("tribe",[])
        group_list = self.requested_argv_dict.get("group",[])

        self.startLog()

        self.target_file_path = "temp"
        self.checkPath()

        self.runCommand()

        self.stopLog()

    def printTimeStamp(self):
        self.current_time_str = time.strftime("%Y%m%d%H%M%S")
        self.delimiter_str = "- :" # for convertTime()
        time_str = "[" + self.convertTime() + "] "
        print( time_str+self.phrase_str )
        with open( self.log_file_name, 'a' ) as log_file:
            log_file.write( time_str+self.phrase_str+"\n" )

    def printPhrase(self):
        print(self.phrase_str)
        with open(self.log_file_name,'a') as log_file:
            log_file.write(self.phrase_str+"\n")

    def printBlankLine(self):
        print("  ")
        with open(self.log_file_name,'a') as log_file:
            log_file.write("  \n")

    def getMaxLengthValue(self):
        temp_list = []
        for name_str in self.list_list:
            temp_list.append( len(name_str) )
        return max(temp_list)

    def convertTime(self):
        year_str   = self.current_time_str[0:4]
        month_str  = self.current_time_str[4:6]
        day_str    = self.current_time_str[6:8]
        hour_str   = self.current_time_str[8:10]
        minute_str = self.current_time_str[10:12]
        second_str = self.current_time_str[12:14]

        if len(self.delimiter_str) != 3:
            self.delimiter_str =  "-_-"
        converted_time_str = (
            self.delimiter_str[0].join([ year_str, month_str, day_str ])
            + self.delimiter_str[1]
            + self.delimiter_str[2].join([ hour_str, minute_str, second_str ]))

        return converted_time_str

    def checkPath(self):
        if self.target_file_list == []:
            self.target_file_list.append(self.target_file_path)

        for target_file in self.target_file_list:
            comand_line_list = [ "mkdir", "-v", target_file ]

            self.phrase_str= "\n checkPath: " + " ".join(comand_line_list)
            self.printTimeStamp()

            call(comand_line_list, stdout=open(self.log_file_name, 'a'))

        self.target_file_path = ""
        self.target_file_list = []
        self.current_time_str = ""
        self.phrase_str = ""
        self.delimiter_str = ""

    def checkFile(self):
        result_boolean = False

        self.current_time_str = time.strftime("%Y%m%d%H%M%S")
        target_file_list = [ "head", "-v", self.target_file_path ]
        call([ "mkdir", "-v", "temp" ])
        call(target_file_list, stdout=open("temp/head-"+self.current_time_str, 'a'))

        command_line_str = "\n        chkfal: " + " ".join(target_file_list)
        self.phrase_str = command_line_str
        self.printTimeStamp()

        temp_file_handle = open("temp/head-"+self.current_time_str,"ab")
        temp_file_handle.write("-=#".encode("UTF-8"))
        temp_file_handle.close()

        if open("temp/head-"+self.current_time_str,"rb").read() != "-=#".encode("UTF-8"):
            result_boolean = True

        target_file_list = [ "rm", "-v", "temp/head-"+self.current_time_str ]
        call(target_file_list, stdout=open("temp/head-"+self.current_time_str, 'a'))

        command_line_str = "        chkfal: " + " ".join(target_file_list)
        result_str = "\n        result: " + pprint.pformat(result_boolean)
        self.phrase_str = command_line_str + result_str
        self.printPhrase()

        self.current_time_str = ""
        self.phrase_str = ""
        self.delimiter_str = ""

        return result_boolean

    def arrangeArgv(self):
        independed_argv_list = []
        base_temp_list = self.system_argv_list
        base_temp_str  = " ".join(self.system_argv_list)
        while "--" in base_temp_str:
            base_temp_list = base_temp_str.split(" ")
            for n in range(len(base_temp_list)):
                if "--" == base_temp_list[n][0:2]:
                    if "=" in base_temp_list[n]:
                        second_temp_str = base_temp_list.pop(n)
                        second_temp_str = second_temp_str.split("--")[1]
                        second_temp_list = second_temp_str.split("=")
                        self.arranged_argv_dict.update({
                            second_temp_list[0] : [second_temp_list[1]]
                        })
                        base_temp_str = " ".join(base_temp_list)
                        break
                    else:
                        second_temp_str = base_temp_list.pop(n)
                        independed_argv_list.append(second_temp_str.replace("--",""))
                        base_temp_str = " ".join(base_temp_list)
                        break

        self.system_argv_list = base_temp_str.split(" ")
        argument_position_list = []

        for number in range(len(self.system_argv_list)):
            if len(self.system_argv_list[number]) > 0:
                if self.system_argv_list[number][0] == '-':
                    argument_position_list.append(number)

        no_option_boolean = True
        for position_num in argument_position_list:
            value_temp_list = []
            key_temp_str  = ""

            key_temp_str = self.system_argv_list[position_num]
            key_temp_str = key_temp_str.split("-")[1]
            value_temp_list = self.arranged_argv_dict.get(key_temp_str,[])

            start_position_num = position_num+1
            end_position_num = 0

            if argument_position_list.index(position_num) == 0:
                independed_argv_list.extend(self.system_argv_list[1:position_num])
                no_option_boolean = False

            if argument_position_list.index(position_num) == len(argument_position_list)-1:
                end_position_num = len(self.system_argv_list)
            else:
                end_position_num = argument_position_list[argument_position_list.index(position_num)+1]

            if start_position_num > len(self.system_argv_list):
                start_position_num = len(self.system_argv_list)

            if end_position_num > len(self.system_argv_list):
                end_position_num = len(self.system_argv_list)

            value_temp_list.extend( self.system_argv_list[start_position_num:end_position_num] )
            self.arranged_argv_dict.update({ key_temp_str : value_temp_list })

        if no_option_boolean:
            independed_argv_list.extend(self.system_argv_list[1:len(self.system_argv_list)])
        self.arranged_argv_dict.update({ "INDEPENDED" : list(set(independed_argv_list)) })

    def synchornize(self):
        argument_tuple = tuple(self.arranged_argv_dict.keys())
        pair_dict = {}
        for argument in argument_tuple:
            if len(argument) == 1 and self.SynonymDict.get_str(argument) != "":
                pair_dict.update({ argument : self.SynonymDict.get_str(argument) })

        for argument in argument_tuple:
            if argument in list(pair_dict.keys()):
                synonum_temp_str = pair_dict.get(argument)
                value_temp_list = self.arranged_argv_dict.get(synonum_temp_str,[])
                value_temp_list.extend(self.arranged_argv_dict.get(argument))
                self.arranged_argv_dict.update({ synonum_temp_str : value_temp_list })

        for requested_argv in tuple(self.requested_argv_dict.keys()):
            if requested_argv in tuple(self.arranged_argv_dict.keys()):
                requested_argv_type = type(self.requested_argv_dict.get(requested_argv))
                arranged_argv_type = type(self.arranged_argv_dict.get(requested_argv))

                str_type = type(str())
                list_type = type(list())

                if arranged_argv_type == list_type: # if type(b) == list
                    list_count_boolean = len(self.arranged_argv_dict.get(requested_argv)) > 0

                if requested_argv_type == arranged_argv_type: # if type(a) == type(b)
                    self.requested_argv_dict.update({
                        requested_argv : self.arranged_argv_dict.get(requested_argv)
                    })
                elif arranged_argv_type == str_type and requested_argv_type == list_type:
                    self.requested_argv_dict.update({
                        requested_argv : [self.arranged_argv_dict.get(requested_argv)]
                    })
                elif (
                    arranged_argv_type == list_type
                    and requested_argv_type == str_type
                    and list_count_boolean
                ):
                    value_temp_list = sorted(self.arranged_argv_dict.get(requested_argv))
                    self.requested_argv_dict.update({
                        requested_argv : value_temp_list[0]
                    })

    def redirecting(self):
        if 'help' in self.arranged_argv_dict.get('INDEPENDED',[]):
            print(self.helper_msg_str)
        else:
            self.actor()

    def startLog(self):
        self.begin_time_str = time.strftime("%Y%m%d%H%M%S")
        self.current_time_str = time.strftime("%Y%m%d%H%M%S")

        self.delimiter_str = "- :" # for convertTime()
        run_info_line = (
            "==========\n"
            +"RUN "+self.script_name+", begin at ["+self.convertTime()+"]"
            +"\n=========="
        )
        self.log_argv_dict = {
            'Input_Argv' : self.system_argv_list,
            'Arranged_Argv' : self.arranged_argv_dict,
            'Requested_Argv' : self.requested_argv_dict
        }
        argv_info_line = ["[ARGV: Arguments]"]

        self.list_list = []
        self.list_list = list(self.log_argv_dict.keys())
        list_max_length_num = self.getMaxLengthValue()
        for subject_str in self.list_list:
            if len(subject_str) < list_max_length_num :
                subject_final_str = subject_str + ' '*(list_max_length_num-len(subject_str))
            else:
                subject_final_str = subject_str

            argv_info_line.append("    " + subject_final_str + ": " +
                pprint.pformat(self.log_argv_dict.get(subject_str),compact=True,width=150))

        if self.requested_config_dict != {}:
            config_info_line = ["\n[CONFIG: From config.json]"]

            self.list_list = []
            self.list_list = list(self.requested_config_dict.keys())
            list_max_length_num = self.getMaxLengthValue()
            for config_str in self.list_list:
                if len(config_str) < list_max_length_num :
                    space_count_num = list_max_length_num-len(config_str)
                else:
                    space_count_num = 0

                config_info_line.append(
                    "    \"" + config_str + "\""+ (" "*space_count_num) +": "
                    +pprint.pformat(self.requested_config_dict.get(config_str),compact=True,width=150)
                )

        else:
            config_info_line = []

        self.delimiter_str = "-_-"  # for convertTime()
        self.log_file_name = self.log_file_prefix_str + self.convertTime() + '.log'

        result_list = [run_info_line]
        result_list.extend(argv_info_line)
        result_list.extend(config_info_line)
        self.phrase_str = "\n".join(result_list)+"\n"
        self.printPhrase()

        self.current_time_str = ""
        self.phrase_str = ""
        self.delimiter_str = ""

    def runCommand(self):
        self.current_time_str = time.strftime("%Y%m%d%H%M%S")
        self.delimiter_str = "- :" # for convertTime()
        run_info_line = "[" + self.convertTime() + "]"
        command_line_str = " Command: " + " ".join(self.comand_line_list)

        self.phrase_str = run_info_line + command_line_str
        self.printPhrase()

        if not self.testing:
            call(self.comand_line_list, stdout=open(self.log_file_name, 'a'))

        self.current_time_str = ""
        self.phrase_str = ""
        self.delimiter_str = ""

    def stopLog(self):
        self.current_time_str = time.strftime("%Y%m%d%H%M%S")
        year_diff_num   = int(self.current_time_str[0:4])  -int(self.begin_time_str[0:4])
        month_diff_num  = int(self.current_time_str[4:6])  -int(self.begin_time_str[4:6])
        day_diff_num    = int(self.current_time_str[6:8])  -int(self.begin_time_str[6:8])
        hour_diff_num   = int(self.current_time_str[8:10]) -int(self.begin_time_str[8:10])
        minute_diff_num = int(self.current_time_str[10:12])-int(self.begin_time_str[10:12])
        second_diff_num = int(self.current_time_str[12:14])-int(self.begin_time_str[12:14])

        if second_diff_num < 0 :
            minute_diff_num = minute_diff_num -1
            second_diff_num = second_diff_num + 60

        if minute_diff_num < 0 :
            hour_diff_num = hour_diff_num -1
            minute_diff_num = minute_diff_num + 60

        if hour_diff_num < 0 :
            day_diff_num = day_diff_num -1
            hour_diff_num = hour_diff_num + 24

        if day_diff_num < 0 :
            result_info_str = "More than one month..."
        else:
            result_info_str = (
                str(hour_diff_num) + " hr "+
                str(minute_diff_num) + " min "+
                str(second_diff_num) + " s "
            )

        self.delimiter_str = "- :" #for convertTime()
        run_info_line = (
            "==========\n"
            +self.script_name+", finished on ["+self.convertTime() +"]\n"
            +"     Total time: "+result_info_str+"\n"
            +"=========="
        )

        self.phrase_str = run_info_line
        self.printPhrase()

        self.phrase_str = ""
        self.current_time_str = ""
