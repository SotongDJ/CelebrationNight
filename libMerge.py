#!/usr/bin/env python3
import pyWorkFlow, libConfig
import time, json, random
global helper_msg_block
helper_msg_block="""
--- README of library-mix-analysis-result.py ---
 Title:
  Library for Mixing analysis result

 Usage: # Replace * with related string
    Miski = libmar.miksing()
    Miski.requested_argv_dict = {
      "tribe"   : tribe_list,
      "group"   : group_list,
      "prefix"  : self.requested_config_dict.get("result/*") + "/",
      "postfix" : "/*.json", OR "postfix" : "-*.json",
      "libconvert"  : self.requested_config_dict.get("libconvert/*")
    }
    Miski.log_file_prefix_str = self.log_file_prefix_str + "Miski-"
    Miski.scanning()

    Miski.fusion()
    Miski.resusi = (
        self.requested_config_dict.get("result/*") + "/" +
        self.requested_config_dict.get("data/prefix").get(tribe_name) + "*.json"
    )
    with open(Miski.resusi,"w") as resufi:
        json.dump(Miski.resudi,resufi,indent=4,sort_keys=True)
    Miski.arrange()

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
ConfigDict = libConfig.config()
class miksing(pyWorkFlow.workflow):
    def redirecting(self):
        """"""
    def personalize(self):
        # self.testing = True
        self.helper_msg_str = helper_msg_block

        self.requested_argv_dict = {
            "tribe"   : [],
            "group"   : [],
            "prefix"  : "",
            "postfix" : "",
            "libconvert"  : []
        }

        self.comand_line_list = []
        self.requested_config_dict = {
            "data/prefix" : ConfigDict.get_dict("data/prefix"),
            "result/log" : ConfigDict.get_str("result/log"),
        }
        self.script_name = "libmar"
        self.log_file_prefix_str = ConfigDict.get_str("result/log")+"/libmar-"

        self.resusi = ""

    def scanning(self):
        tribe_list = self.requested_argv_dict.get("tribe",[])
        group_list = self.requested_argv_dict.get("group",[])
        pifisi = self.requested_argv_dict.get("prefix",[])
        pofisi = self.requested_argv_dict.get("postfix",[])

        self.script_name = "scanning from libmar"
        self.startLog()

        self.tunodi = {}
        self.refedi = {}
        for tribe_name in tribe_list:
            keyoli = []
            for gupo in group_list:
                socesi = (
                    pifisi +
                    self.requested_config_dict.get("data/prefix").get(tribe_name) + gupo +
                    pofisi
                )
                socefi = open(socesi,"r")
                soceso = json.load(socefi)

                numein = 0
                if keyoli == []:
                    keyoli = list(soceso.keys())

                if self.refedi == {}:
                    for id in keyoli:
                        admedi = soceso.get(id)
                        bamedi = {}
                        for colu in list(soceso.get(id).keys()):
                            basi = admedi.get(colu)
                            bamedi.update({ colu : basi})
                            self.refedi.update({ id : bamedi})
                else:
                    for id in keyoli:
                        admedi = soceso.get(id)
                        bamedi = self.refedi.get(id)
                        for colu in list(soceso.get(id).keys()):
                            adsi = admedi.get(colu)
                            basi = bamedi.get(colu)
                            if adsi == basi and not self.tunodi.get(colu,False):
                                self.tunodi.update({ colu : False })
                            else:
                                self.tunodi.update({ colu : True })
        self.stopLog()

    def fusion(self):
        tribe_list = self.requested_argv_dict.get("tribe",[])
        group_list = self.requested_argv_dict.get("group",[])
        pifisi = self.requested_argv_dict.get("prefix",[])
        pofisi = self.requested_argv_dict.get("postfix",[])

        self.script_name = "fusion from libmar"
        self.startLog()

        self.coludi = {}
        self.resudi = {}
        for tribe_name in tribe_list:
            for gupo in group_list:
                socesi = (
                    pifisi +
                    self.requested_config_dict.get("data/prefix").get(tribe_name) + gupo +
                    pofisi
                )
                socefi = open(socesi,"r")
                soceso = json.load(socefi)

                for id in list(soceso.keys()):
                    somedi = soceso.get(id)
                    remedi = self.resudi.get(id,{})
                    for colu in list(somedi.keys()):
                        if self.tunodi.get(colu,False):
                            remedi.update({ colu+"("+gupo+")" : somedi.get(colu) })

                            comeli = self.coludi.get(colu,[])
                            if colu+"("+gupo+")" not in comeli:
                                comeli.append(colu+"("+gupo+")")
                                self.coludi.update({ colu : comeli })
                            comeli = []

                        elif remedi.get(colu,"") == "":
                            remedi.update({ colu : somedi.get(colu) })
                    self.resudi.update({ id : remedi })
        self.stopLog()

    def arrange(self):
        self.script_name = "arrange from libmar"
        self.startLog()

        self.coluli = []
        litali = self.requested_argv_dict.get("libconvert",[])
        if litali == []:
            litali = list(self.tunodi.keys())
        litasi = "*@*"+"*@*".join(litali)+"*@*"
        for colu in list(self.coludi.keys()):
            if "*@*"+colu+"*@*" in litasi:
                metasi = "*@*".join(self.coludi.get(colu))
                litasi = litasi.replace("*@*"+colu+"*@*","*@*"+metasi+"*@*")
        litasi = litasi[3:len(litasi)-3]
        self.coluli = litasi.split("*@*")
        print(list(self.tunodi.keys()))
        print(list(self.coludi.keys()))
        print(self.coluli)
        self.stopLog()
