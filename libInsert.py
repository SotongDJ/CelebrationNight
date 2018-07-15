#!/usr/bin/env python3
import sys, pprint, json
import pyWorkFlow
global helper_msg_block
helper_msg_block="""
   --- README of library-search-and-merge ---
  Title:
    Searching and Pairing Tool for Transcript Info. and StringTie Result

  Usage:
    import libsnm
    GeneID = libsnm.geneid()
    GeneID.requested_argv_dict = {
        "description" : [file of gene description] ,
        "basement" : [result file] ,
        "if" : [column name of gene id in result file],
        "key" : [header of gene id, "gene:"],
        "from" : [column name of gene id in gene description file],
        "to" : [column name of description],
    }
    # GeneID.requested_argv_dict.update()
    GeneID.filasi = "libsnm.geneid"
    GeneID.actor()

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
class geneid(pyWorkFlow.workflow):
    def redirecting(self):
        """"""
    def personalize(self):
        # self.testing = True

        self.requested_argv_dict = {
            "description" : "" ,
            "basement" : "" ,
            "if" : "",
            "key" : "",
            "from" : "",
            "to" : "",
        }
        self.synchornize()

        self.target_file_path = ""

        self.comand_line_list=[]

        self.script_name = "library-search-and-merge"
        self.requested_config_dict = {}
        self.log_file_prefix_str = "temp/tmp-"

    def actor(self):
        addasi = self.requested_argv_dict.get("description","")
        socesi = self.requested_argv_dict.get("basement","")
        ifasi = self.requested_argv_dict.get("if","")
        keyosi = self.requested_argv_dict.get("key","")
        frosi = self.requested_argv_dict.get("from","")
        tonsi = self.requested_argv_dict.get("to","")

        self.startLog()

        self.frase = pprint.pformat((addasi, socesi, ifasi, keyosi, tonsi))
        self.printTimeStamp()

        addafi = open(addasi,"r")
        addaso = json.load(addafi)

        socefi = open(socesi,"r")
        soceso = json.load(socefi)

        blanbo = False

        if ifasi != "" and tonsi != "":
            for id in list(soceso.keys()):
                metadi = soceso.get(id)
                if keyosi in metadi.get(ifasi):
                    refesi = metadi.get(ifasi).replace(keyosi,"")
                    resusi = addaso.get(frosi).get(refesi,"N/A")
                    metadi.update({ tonsi : resusi })
                    soceso.update({ id : metadi })
                    blanbo = True

        if blanbo:
            with open(socesi,"w") as socefi:
                json.dump(soceso,socefi,indent=4,sort_keys=True)

        self.stopLog()
