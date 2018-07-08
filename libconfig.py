#!/usr/bin/env python3
import json
class config:
    def __init__(self):
        self.load_json()

    def load_json(self):
        global_config_file_str = "config.json"
        global_config_file_handle = open(global_config_file_str,'a+')
        global_config_file_handle.close()

        if open(global_config_file_str).read() == "":
            self.content_dict = {}
            with open(global_config_file_str,'w') as global_config_file_handle:
                global_config_file_handle.write("{}")
        else:
            global_config_file_handle = open(global_config_file_str,'r')
            self.content_dict = json.load(global_config_file_handle)

        local_config_file_str = "data/config.json"
        local_config_file_handle = open(local_config_file_str,'a+')
        local_config_file_handle.close()

        if open(local_config_file_str).read() == "":
            with open(local_config_file_str,'w') as local_config_file_handle:
                local_config_file_handle.write("{}")
        else:
            local_config_file_handle = open(local_config_file_str,'r')
            self.content_dict.update(json.load(local_config_file_handle))

    def refresh(self):
        self.load_json()

        global_config_file_str = "config.json"
        global_config_file_handle = open(global_config_file_str,'r')
        metaso = json.load(global_config_file_handle)
        with open(global_config_file_str,'w') as configfa:
            json.dump(metaso,configfa,indent=4,sort_keys=True)

        local_config_file_str = "data/config.json"
        local_config_file_handle = open(local_config_file_str,'r')
        metaso = json.load(local_config_file_handle)
        with open(local_config_file_str,'w') as configfa:
            json.dump(metaso,configfa,indent=4,sort_keys=True)

    def get_str(self,keyword_str):
        resut = self.content_dict.get(keyword_str)
        return resut

    def get_list(self,keyword_str):
        resut = self.content_dict.get(keyword_str,[])
        return resut

    def get_dict(self,keyword_str):
        resut = self.content_dict.get(keyword_str,{})
        return resut

    def get_path(self,keyword_list):
        resut = []
        for keyword_str in keyword_list:
            resut.append(self.content_dict.get(keyword_str,""))
        return "/".join(resut)

    def check(self,keyword_str):
        resut = False
        metali = list(self.content_dict.keys())
        if keyword_str in metali:
            resut = True
        return resut
