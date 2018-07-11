import pprint,json
class heading:
    def __init__(self):
        self.content_dict = {}
        self.input_file = ""

    def load(self):
        if self.input_file != "" and ".json" in self.input_file:
            file_handle = open(self.input_file,'r')
            self.content_dict = json.load(file_handle)

    def generate(self):
        self.content_str = "<First Layer>,"
        first_key_list = list(self.content_dict.keys())
        first_count_num = len(first_key_list)

        first_content_str = ""

        first_end_num = first_count_num
        first_end_str = ""
        if first_count_num >= 10:
            first_end_num = 10
            first_end_str = "......"
        self.content_str = (
            self.content_str
            # +"content: \n"
            +str(type(self.content_dict))+",<Count: "+str(first_count_num)+">:\n"
        )
        first_target_list = first_key_list[0:first_end_num]
        for first_key in first_target_list:
            first_value = self.content_dict.get(first_key)

            first_content_str = (
                first_content_str
                # +" # <Second Layer: "+str(first_key)+" "+str(type(first_key))+" ==\n"
                +pprint.pformat(first_key)+" # <Second Layer>,"
            )

            second_count_str = ""
            second_content_str = ""
            if type(first_value) in [type(list),type(tuple),type(set)]:
                second_count_str = ",<Count: "+str(len(first_value))+">:\n"
                second_content_str = ""
                if len(first_value) <= 10:
                    second_content_str = (
                        second_content_str
                        #+"content: \n"+str(type(second_target))+"\n"+pprint.pformat(second_target,compact=True,width=1000)
                        +str(type(second_target))+":\n"+pprint.pformat(first_value,compact=True,width=1000)
                    )
                else:
                    second_target = first_value[0:10]
                    second_content_str = (
                        second_content_str
                        # +"content: \n"+str(type(second_target))+"\n"+pprint.pformat(second_target,compact=True,width=1000)
                        +str(type(second_target))+":\n"+pprint.pformat(second_target,compact=True,width=1000)+"\n......"
                    )
            elif type(first_value) in [type(dict())]:
                second_key_list = list(first_value.keys())
                second_count_num = len(second_key_list)

                second_count_str = ",<Count: "+str(second_count_num)+">:\n"
                second_content_str = ""

                second_end_num = second_count_num
                second_end_str = ""
                if second_count_num >= 10:
                    second_end_num = 10
                    second_end_str = "......"

                first_content_str = (
                    first_content_str
                    # +"content: \n"+str(type(first_value))+"\n"
                    +str(type(first_value))
                )
                second_target_list = second_key_list[0:second_end_num]
                for second_key in second_target_list:
                    second_value = first_value.get(second_key)

                    second_content_str = (
                        second_content_str
                        # +" # <Third Layer: "+str(second_key)+" "+str(type(second_key))+" ==\n"
                        +pprint.pformat(second_key)+" # <Third Layer>,"
                    )

                    third_count_str = ""
                    third_content_str = ""

                    if type(second_value) in [type(list),type(tuple),type(set)]:
                        third_count_str = ",<Count: "+str(len(second_value))+">:\n"
                        third_content_str = ""
                        if len(second_value) <= 10:
                            third_target = second_value
                            third_content_str = (
                                third_content_str
                                # +"content: \n"+str(type(third_target))+"\n"+pprint.pformat(third_target,compact=True,width=1000)
                                +str(type(third_target))+":\n"+pprint.pformat(third_target,compact=True,width=1000)
                            )
                        else:
                            third_target = second_value[0:10]
                            third_content_str = (
                                third_content_str
                                # +"content: \n"+str(type(third_target))+"\n"+pprint.pformat(third_target,compact=True,width=1000)
                                +str(type(third_target))+":\n"+pprint.pformat(third_target,compact=True,width=1000)+"\n......"
                            )
                    elif type(second_value) in [type(dict())]:
                        third_key_list = list(second_value.keys())
                        third_count_num = len(third_key_list)

                        third_count_str = ",<Count: "+str(third_count_num)+">:\n"
                        third_content_str = ""

                        third_end_num = third_count_num
                        third_end_str = ""
                        if third_count_num >= 10:
                            third_end_num = 10
                            third_end_str = "......"
                        second_content_str = (
                            second_content_str
                            # +"content: \n"+str(type(second_value))+"\n"
                            +str(type(second_value))
                        )
                        third_target_list = third_key_list[0:third_end_num]
                        for third_key in third_target_list:
                            third_value = second_value.get(third_key)

                            third_content_str = (
                                third_content_str
                                # +" # <Forth Layer: "+str(third_key)+" "+str(type(second_key))+" ==\n"
                                +pprint.pformat(third_key)+" # <Forth Layer>,"
                            )

                            forth_value_str = pprint.pformat(third_value,compact=True,width=1000)
                            if len(forth_value_str) >= 1000:
                                forth_value_str = forth_value_str[0:1000]+"\n......"
                            # forth_content_str = "content: \n"+str(type(third_value))+"\n"+forth_value_str
                            forth_content_str = str(type(third_value))+":\n"+forth_value_str

                            third_content_str = (
                                third_content_str
                                +third_count_str
                                +"    "
                                +forth_content_str.replace("\n","\n    ")+"\n"
                            )

                        third_content_str = third_content_str + third_end_str + "\n"

                    else:
                        second_value_str = pprint.pformat(second_value,compact=True,width=1000)
                        if len(second_value_str) >= 1000:
                            second_value_str = second_value_str[0:1000]+"\n......"
                        # third_content_str = "content: \n"+str(type(second_value))+"\n"+second_value_str
                        third_content_str = str(type(second_value))+":\n"+second_value_str

                    second_content_str = (
                        second_content_str
                        +third_count_str
                        +"    "
                        +third_content_str.replace("\n","\n    ")+"\n"
                    )

                second_content_str = second_content_str + second_end_str + "\n"

            else:
                first_value_str = pprint.pformat(first_value,compact=True,width=1000)
                if len(first_value_str) >= 1000:
                    first_value_str = first_value_str[0:1000]+"\n......"
                # second_content_str = "content: \n"+str(type(first_value))+"\n"+first_value_str
                second_content_str = str(type(first_value))+":\n"+first_value_str

            first_content_str = (
                first_content_str
                +second_count_str
                +"    "
                +second_content_str.replace("\n","\n    ")+"\n"
            )

        first_content_str = first_content_str + first_end_str + "\n"

        self.content_str = (
            self.content_str
            +"    "
            +first_content_str.replace("\n","\n    ")+"\n"
        )
        self.content_str = self.content_str.replace(" Layer>,    <class "," Layer>,<class ")

    def view(self):
        self.load()
        self.generate()
        print(self.content_str)
