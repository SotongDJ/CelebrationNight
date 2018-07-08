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

    CoveJos = libconvert.tab2json()
    CoveJos.requested_argv_dict = {
        "files" : [<INPUT>,<INPUT>......] ,
        "id" : "" ,
        "column": < Column separate by tab > # for headless file
    }
    CoveJos.actor()

    CoveTab = libconvert.json2tab()
    CoveTab.requested_argv_dict = {
        "files" : [<INPUT>,<INPUT>......] ,
        "column": [<NAME>,<NAME>......] # for sorting
    }
    CoveTab.actor()

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
class tab2json(libWorkFlow.workflow):
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
        soceli        = self.requested_argv_dict.get("files" ,[])
        target_file_path        = self.requested_argv_dict.get("id"    ,"")
        prefix_str = self.requested_argv_dict.get("prefix","")
        comusi        = self.requested_argv_dict.get("column","")
        self.startLog()

        self.phrase_str = pprint.pformat((soceli,target_file_path,len(comusi)))
        self.printTimeStamp()

        for socesi in soceli:
            self.phrase_str = pprint.pformat(socesi)
            self.printTimeStamp()

            metali = socesi.split(".")
            metali[-1] = "json"
            resusi = ".".join(metali)
            remasi = resusi.replace(".json","-column.json")

            self.target_file_path = resusi
            resubo = self.check_file()
            self.target_file_path = remasi
            remabo = self.check_file()

            if not resubo or not remabo :
                lineli = open(socesi).read().splitlines()

                namedi = {}

                resudi = {}
                remadi = {}

                if comusi != "":
                    metali = comusi.split("	")
                    for n in range(len(metali)):
                        if metali[n] not in namedi.values():
                            namedi.update({ n : metali[n] })
                        if metali[n] not in remadi.keys():
                            remadi.update({ metali[n] :{} })
                    colubo = False
                else:
                    colubo = True

                if target_file_path != "":
                    tagebo = True
                else:
                    tagebo = False

                numein = 0
                for line in lineli:
                    if colubo:
                        metali = line.split("	")
                        for n in range(len(metali)):
                            if metali[n] not in namedi.values():
                                namedi.update({ n : metali[n] })
                            if metali[n] not in remadi.keys():
                                remadi.update({ metali[n] :{} })
                        colubo = False
                    elif "#" not in line:
                        metali = line.split("	")
                        metadi = {}
                        idisi = ""

                        if not tagebo:
                            numein = numein + 1
                            idisi = prefix_str + str(numein)

                        for n in range(len(list(namedi.keys()))):
                            colusi = namedi.get(n)
                            metadi.update({ colusi : metali[n]})

                            if colusi == target_file_path and tagebo:
                                idisi = prefix_str + metali[n]

                        resudi.update({ idisi : metadi })

                        for n in range(len(list(namedi.keys()))):
                            colusi = namedi.get(n)

                            almedi = remadi.get(colusi,{})
                            almeli = almedi.get(metali[n],[])

                            almeli.append(idisi)

                            almedi.update({ metali[n] : almeli })
                            remadi.update({ colusi : almedi })


                with open(resusi,"w") as resufi:
                    json.dump(resudi,resufi,indent=4,sort_keys=True)

                with open(remasi,"w") as remafi:
                    json.dump(remadi,remafi,indent=4,sort_keys=True)
        self.stopLog()

class json2tab(libWorkFlow.workflow):
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
        soceli = self.requested_argv_dict.get("files",[])
        coluli = self.requested_argv_dict.get("column",[])
        self.startLog()

        self.phrase_str = pprint.pformat(soceli)
        self.printTimeStamp()

        for socesi in soceli:
            socefi = open(socesi,'r')
            soceso = json.load(socefi)

            if coluli == []:
                coluse = set()
                metadi = dict()
                for id in list(soceso.keys()):
                    metadi = soceso.get(id,{})
                    coluse.update(set(metadi.keys()))
                colutu = tuple(sorted(coluse))
            else:
                colutu = tuple(coluli)

            with open(socesi.replace(".json",".tsv"),"w") as resufi:
                resufi.write("id"+"	"+"	".join(colutu)+"\n")
                for id in list(soceso.keys()):
                    line = id
                    metadi = dict()
                    metadi = soceso.get(id,{})
                    for meta in colutu:
                        line = line + "	" + metadi.get(meta,"")
                    resufi.write(line+"\n")

        self.stopLog()
