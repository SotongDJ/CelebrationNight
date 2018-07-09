#!/usr/bin/env python3
import json
class config:
    def __init__(self):
        self.global_dict = {}
        self.local_dict = {}
        self.requested_dict = {}

        self.load()

    def refresh(self):
        self.load()
        self.save()

    def load(self):
        self.load_global_json()
        self.load_local_json()

    def save(self):
        self.save_global_json()
        self.save_local_json()

    def load_global_json(self):
        global_config_file_str = "config.json"
        global_config_file_handle = open(global_config_file_str,'a+')
        global_config_file_handle.close()

        if open(global_config_file_str).read() == "":
            with open(global_config_file_str,'w') as global_config_file_handle:
                global_config_file_handle.write("{}")
        else:
            global_config_file_handle = open(global_config_file_str,'r')
            self.global_dict = json.load(global_config_file_handle)

    def load_local_json(self):
        local_config_file_str = "data/config.json"
        local_config_file_handle = open(local_config_file_str,'a+')
        local_config_file_handle.close()

        if open(local_config_file_str).read() == "":
            with open(local_config_file_str,'w') as local_config_file_handle:
                local_config_file_handle.write("{}")
        else:
            local_config_file_handle = open(local_config_file_str,'r')
            self.local_dict.update(json.load(local_config_file_handle))

    def save_global_json(self):
        global_config_file_str = "config.json"
        global_config_file_handle = open(global_config_file_str,'r')
        with open(global_config_file_str,'w') as configfa:
            json.dump(self.global_dict,configfa,indent=4,sort_keys=True)

    def save_local_json(self):
        local_config_file_str = "data/config.json"
        local_config_file_handle = open(local_config_file_str,'r')
        metaso = json.load(local_config_file_handle)
        with open(local_config_file_str,'w') as configfa:
            json.dump(self.local_dict,configfa,indent=4,sort_keys=True)

    def get_str(self,keyword_str):
        result_str = ""
        if keyword_str in list(self.global_dict.keys()):
            result_str = self.global_dict.get(keyword_str)
        elif keyword_str in list(self.local_dict.keys()):
            result_str = self.local_dict.get(keyword_str)

        return result_str

    def get_list(self,keyword_str):
        result_list = []
        if keyword_str in list(self.global_dict.keys()):
            result_list = self.global_dict.get(keyword_str)
        elif keyword_str in list(self.local_dict.keys()):
            result_list = self.local_dict.get(keyword_str)

        return result_list

    def get_dict(self,keyword_str):
        result_dict = {}
        if keyword_str in list(self.global_dict.keys()):
            result_dict = self.global_dict.get(keyword_str)
        elif keyword_str in list(self.local_dict.keys()):
            result_dict = self.local_dict.get(keyword_str)

        return result_dict

    def get_batchly(self):
        for keyword_name in list(self.requested_dict.keys()):
            if keyword_name in list(self.global_dict.keys()):
                self.requested_dict.update({ keyword_name : self.global_dict.get(keyword_name)})
            elif keyword_name in list(self.local_dict.keys()):
                self.requested_dict.update({ keyword_name : self.local_dict.get(keyword_name)})

        return self.requested_dict

    def update(self,keyword_dict):
        for keyword_name in list(keyword_dict.keys()):
            if keyword_name in list(self.global_dict.keys()):
                self.global_dict.update({ keyword_name : keyword_dict.get(keyword_name)})
            elif keyword_name in list(self.local_dict.keys()):
                self.local_dict.update({ keyword_name : keyword_dict.get(keyword_name)})
        self.save()
