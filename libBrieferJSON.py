import pprint,json
import libWorkFlow
class heading(libWorkFlow.workflow):
    def redirecting(self):
        """"""
    def actor(self):
        """"""
    def personalize(self):
        # self.testing = True
        self.helper_msg_str = "libJsonHeader.heading"

        self.requested_argv_dict = {}

        self.target_file_path = ""

        self.comand_line_list=[]

        self.script_name = "libJsonHeader.heading"
        self.requested_config_dict = {}
        self.log_file_prefix_str = "temp/temp-"

        self.initiation()

    def set(self,file_name):
        self.input_file = file_name

    def initiation(self):
        self.content_dict = {}
        self.input_file = ""
        self.output_file = ""

    def load(self):
        if self.input_file != "" and ".json" in self.input_file:
            file_handle = open(self.input_file,'r')
            self.content_dict = json.load(file_handle)

        if self.input_file == "":
            print("required the string \'input_file\'")

        if ".json" not in self.input_file:
            print("\'input_file\' must be JSON file")

        self.input_file = ""

    def generate(self):
        self.content_str = "target_dict = {\n"
        first_key_list = list(self.content_dict.keys())
        first_count_num = len(first_key_list)

        first_end_num = first_count_num
        first_end_str = "},"
        if first_count_num >= 10:
            first_end_num = 10
            first_end_str = "<......>\n},"
        self.content_str = (
            self.content_str+"    # First Layer\n    # Count: "+str(first_count_num)+"\n"
        )
        first_target_list = first_key_list[0:first_end_num]

        first_content_str = ""

        for first_key in first_target_list:
            first_value = self.content_dict.get(first_key)

            first_content_str = (
                first_content_str
                +pprint.pformat(first_key)+": \n"
            )

            second_count_str = ""
            second_content_str = ""
            if type(first_value) in [type(list),type(tuple),type(set)]:
                second_count_str = "    # Second Layer\n    # Count: "+str(len(first_value))+" (list/tuple/set)\n[\n"
                second_content_str = ""
                if len(first_value) <= 10:
                    second_content_str = pprint.pformat(first_value,compact=True,width=1000)+"\n],"
                else:
                    second_target = first_value[0:10]
                    second_content_str = pprint.pformat(second_target,compact=True,width=1000)+"\n<......>\n],"
            elif type(first_value) in [type(dict())]:
                second_key_list = list(first_value.keys())
                second_count_num = len(second_key_list)

                second_count_str = "{\n"+"    # Second Layer\n    # Count: "+str(second_count_num)+" (dict)\n"
                second_content_str = ""

                second_end_num = second_count_num
                second_end_str = "},"
                if second_count_num >= 10:
                    second_end_num = 10
                    second_end_str = "<......>\n},"

                second_target_list = second_key_list[0:second_end_num]
                for second_key in second_target_list:
                    second_value = first_value.get(second_key)

                    second_content_str = (
                        second_content_str
                        +pprint.pformat(second_key)+": \n"
                    )

                    third_count_str = ""
                    third_content_str = ""

                    if type(second_value) in [type(list),type(tuple),type(set)]:
                        third_count_str = "[\n"+"    # Third Layer\n    # Count: "+str(len(second_value))+" (list/tuple/set)\n"
                        third_content_str = third_count_str
                        if len(second_value) <= 10:
                            third_target = second_value
                            third_content_str = pprint.pformat(third_target,compact=True,width=1000)+"\n],"
                        else:
                            third_target = second_value[0:10]
                            third_content_str = pprint.pformat(third_target,compact=True,width=1000)+"\n<......>\n],"
                    elif type(second_value) in [type(dict())]:
                        third_key_list = list(second_value.keys())
                        third_count_num = len(third_key_list)

                        third_count_str = "{\n"+"    # Third Layer\n    # Count: "+str(third_count_num)+" (dict)\n"
                        third_content_str = third_count_str

                        third_end_num = third_count_num
                        third_end_str = "},"
                        if third_count_num >= 10:
                            third_end_num = 10
                            third_end_str = "<......>},"
                        third_target_list = third_key_list[0:third_end_num]
                        for third_key in third_target_list:
                            third_value = second_value.get(third_key)

                            third_content_str = (
                                third_content_str
                                +pprint.pformat(third_key)+": \n"
                            )

                            forth_value_str = pprint.pformat(third_value,compact=True,width=1000)
                            if len(forth_value_str) >= 1000:
                                forth_value_str = forth_value_str[0:1000]+"\n<......>\n"
                            forth_content_str = forth_value_str+", # Forth Layer;"+str(type(third_value))

                            third_content_str = (
                                third_content_str+"    "+forth_content_str.replace("\n","\n    ")+"\n"
                            )

                        third_content_str = third_content_str + third_end_str + "\n"

                    else:
                        second_value_str = pprint.pformat(second_value,compact=True,width=1000)
                        if len(second_value_str) >= 1000:
                            second_value_str = second_value_str[0:1000]+"\n<......>\n"
                        third_content_str = second_value_str+", # Third Layer;"+str(type(second_value))

                    second_content_str = (
                        second_content_str
                        +"    "+third_content_str.replace("\n","\n    ")+"\n"
                    )

                second_content_str = second_content_str + second_end_str + "\n"

            else:
                first_value_str = pprint.pformat(first_value,compact=True,width=1000)
                if len(first_value_str) >= 1000:
                    first_value_str = first_value_str[0:1000]+"\n<......>\n"
                second_content_str = first_value_str+", # Second Layer;"+str(type(first_value))+"\n"

            first_content_str = (
                first_content_str
                +second_count_str
                +"    "+second_content_str.replace("\n","\n    ")+"\n"
            )

        first_content_str = first_content_str + first_end_str + "\n"

        self.content_str = (
            self.content_str
            +"    "+first_content_str.replace("\n","\n    ")+",\n},"
        )

    def view(self):
        self.phrase_str = "Start loading"
        self.printTimeStamp()
        self.load()

        self.phrase_str = "Start generating"
        self.printTimeStamp()
        self.generate()

        print(self.content_str)
        self.stopLog()

    def output(self):
        self.startLog()
        if self.output_file == "" and self.input_file != "":
            self.output_file = self.input_file.replace(".json",".py")

        if self.input_file != "":

            self.phrase_str = "Start loading"
            self.printTimeStamp()
            self.load()

            self.phrase_str = "Start generating"
            self.printTimeStamp()
            self.generate()

            self.phrase_str = "Start outputing"
            self.printTimeStamp()
            with open(self.output_file,"w") as output_file_handle:
                output_file_handle.write(self.content_str)

        self.input_file = ""
        self.output_file = ""
        self.stopLog()
