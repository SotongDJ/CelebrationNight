#!/usr/bin/env python3
import libWorkFlow, libconfig, libconvert
import time, json, pprint
global helper_msg_block
helper_msg_block="""
  --- README of library-gff-extract.py ---
 Title:
  Library for GFF information extraction

 Usage:
  import libgext
  Gekta = libgext.gffextract()
  Gekta.testing = self.testing
  Gekta.log_file_prefix_str = < Log File Path>
  Gekta.requested_argv_dict = {
    "input"  : <GFF file>
    "tribe"  : <tribe>
    "output" : <OUTPUT JSON file name>
  }
  Gekta.actor()

 CAUTION:
  libgext required libconvert

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
ConfigDict = libconfig.config()
class gffextract(libWorkFlow.workflow):
    def redirecting(self):
        """"""
    def personalize(self):
        # self.testing = True
        self.helper_msg_str = helper_msg_block

        self.requested_argv_dict = {
            "input"  : [],
            "output" : "",
            "tribe"  : "",
        }

        self.comand_line_list = []
        self.script_name = "library-gff-extract.py"
        self.requested_config_dict = {
            "result/stringtie" : ConfigDict.get_str("result/stringtie"),
            "result/ge"        : ConfigDict.get_str("result/ge"),
            "type/database"   : ConfigDict.get_dict("type/database"),
            "target/libgext"   : ConfigDict.get_dict("target/libgext")
        }
        self.log_file_prefix_str = ConfigDict.get_str("result/log")+"/libgext-"

    def actor(self):
        self.input_list      = self.requested_argv_dict.get("input",[])
        self.output_filename = (
            self.requested_config_dict.get("result/ge") + "/" + self.requested_argv_dict.get("output","")
        )
        tribe_name = self.requested_argv_dict.get("tribe","")
        type_name  = self.requested_config_dict.get("type/database").get(tribe_name)
        self.column_name = self.requested_config_dict.get("target/libgext").get(type_name)

        self.startLog()

        self.target_file_list = []
        self.target_file_list.append(self.requested_config_dict.get("result/stringtie"))
        self.target_file_list.append(self.requested_config_dict.get("result/ge"))
        self.checkPath()

        self.printBlankLine()
        self.phrase_str = "==========\nStage 1 : Convert GFF(v3) to JSON\n=========="
        self.printPhrase()

        comusi = (
            "sequence	source	feature	start	end	"
            + "score	srefed	phase	Attributes"
        )

        CvtoJSON = libconvert.cvtTABtoJSON()
        CvtoJSON.requested_argv_dict = {
            "files"  : self.input_list,
            "id"     : "",
            "prefix" : "gff",
            "column" : comusi
        }
        CvtoJSON.actor()

        self.printBlankLine()
        self.phrase_str = "==========\nStage 2 : Grab Attributes from JSON\n=========="
        self.printPhrase()

        self.source_s_dict = dict()
        for inpu in self.input_list:
            metali = inpu.split(".")
            metali[-1] = "json"
            resusi = ".".join(metali)
            remasi = resusi.replace(".json","-column.json")
            filafi = open(remasi,"r")
            filaso = json.load(filafi)
            self.source_s_dict.update(filaso.get("Attributes",{}))

        self.phrase_str = pprint.pformat(( len(self.source_s_dict)))
        self.printTimeStamp()

        self.printBlankLine()
        self.phrase_str = "==========\nStage 3 : Extract Attributes into Dictionaries\n=========="
        self.printPhrase()

        self.gffid_x_value_dict   = {}
        self.name_x_value_dict = {}

        for record in list(self.source_s_dict.keys()):
            ids_list   = []
            value_list = []
            value_dict = {}

            value_list = record.split(";")
            for value in value_list:
                temp_list = []

                temp_list = value.split("=")
                if len(temp_list) == 2:
                    value_dict.update({ temp_list[0] : temp_list[1] })

            ids_list   = self.source_s_dict.get(record)
            for id in ids_list:
                self.gffid_x_value_dict.update({ id : value_dict })

        for id in list(self.gffid_x_value_dict.keys()):
            temp_dict = {}
            name_str  = ""

            temp_dict = self.gffid_x_value_dict.get( id, {})
            temp_dict.update({ "gff_id" : id })

            if "ID" in temp_dict.keys():
                name_str = temp_dict.get("ID")
            elif "Name" in temp_dict.keys():
                name_str = temp_dict.get("Name")

            if name_str != "":
                self.name_x_value_dict.update({ name_str : temp_dict })

        self.phrase_str = pprint.pformat((
            len(self.gffid_x_value_dict),
            len(self.name_x_value_dict)
        ))
        self.printTimeStamp()

        self.printBlankLine()
        self.phrase_str = "==========\nStage 4 : Generate Refer. Dictionary for Result\n=========="
        self.printPhrase()

        self.resudi = {}
        self.desidi = {}

        for nama in list(self.refedi.keys()):
            refesi = self.refedi.get(nama)
            refeli = refesi.replace("=",";").split(";")
            semadi = {}
            for n in range(len(refeli)):
                keyosi = ""
                valusi = ""
                if n+1 != len(refeli):
                    if "_id" in refeli[n] or refeli[n] in ["gene","transcript","protein"]:
                        metadi = self.resudi.get(refeli[n],{})
                        keyosi = refeli[n]
                        valusi = refeli[n+1]
                        semadi.update({ keyosi : valusi })
                        metadi.update({  valusi : refesi })
                        self.resudi.update({ keyosi : metadi })

            for n in range(len(refeli)):
                if refeli[n] == self.column_name:
                    for keyosi in list(semadi.keys()):
                        valusi = semadi.get(keyosi)
                        metadi = self.desidi.get(keyosi,{})
                        metadi.update({  valusi : refeli[n+1] })
                        self.desidi.update({ keyosi : metadi })

        self.phrase_str = pprint.pformat( list(self.resudi.keys()) )
        self.printTimeStamp()

        self.phrase_str = pprint.pformat( list(self.desidi.keys()) )
        self.printTimeStamp()

        self.printBlankLine()
        self.phrase_str = "==========\nStage 5 : Export Dictionaries into JSON\n=========="
        self.printPhrase()

        setosi = "json"
        if "." in self.output_filename:
            metali = []
            metali = self.output_filename.split(".")
            if metali[-1] == "json":
                setosi = metali.pop(-1)
            elif metali[-1] in ["ctab","tsv","diff","tab"]:
                setosi = metali.pop(-1)
                self.output_filename = ".".join(metali).replace("."+setosi,".json")
            else:
                metasi = metali.pop(-1)
                setosi = "json"
                self.output_filename = ".".join(metali).replace("."+metasi,".json")
        else:
            setosi = "json"
            self.output_filename = self.output_filename +".json"

        self.refesi = self.output_filename.replace(".json","-refer.json")
        self.valesi = self.output_filename.replace(".json","-value.json")
        self.desisi = self.output_filename.replace(".json","-"+self.column_name+".json")

        with open(self.refesi,"w") as refefi:
            json.dump(self.refedi,refefi,indent=4,sort_keys=True)

        with open(self.valesi,"w") as valefi:
            json.dump(self.valedi,valefi,indent=4,sort_keys=True)

        with open(self.desisi,"w") as desifi:
            json.dump(self.desidi,desifi,indent=4,sort_keys=True)

        with open(self.output_filename,"w") as oupufi:
            json.dump(self.resudi,oupufi,indent=4,sort_keys=True)

        if setosi != "json":
            self.printBlankLine()
            self.phrase_str = "==========\nStage 6 : Convert JSON back to TSV/CTAB\n=========="
            self.printPhrase()

            CvtoTAB = libConvert.cvtJSONtoDSV()
            CvtoTAB.requested_argv_dict = { "files" : [self.output_filename] }
            CvtoTAB.actor()

        self.stopLog()
