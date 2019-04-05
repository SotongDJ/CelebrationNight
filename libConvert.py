#!/usr/bin/env python3
import sys, pprint, json
import pyWorkFlow
global helper_msg_block
helper_msg_block="""
   --- README of Conversion Library ---
  Title:
    Conversion tool for JSON and TSV/CTAB

  Usage:
    import libConvert

    CvtoJSON = libConvert.cvtDSVtoJSON()
    CvtoJSON.requested_argv_dict = {
		"files": [],
		"refer_column": "",
		"prefix": "",
		"header": [],
		"headless": True,
		"delimiter": "\t"
	}
    CvtoJSON.actor()

    MakingRelation = makingRelation()
    MakingRelation.inputDict = dict()
    MakingRelation.inputDict.update(idKeyValueDict)
    MakingRelation.log_file_prefix_str = self.log_file_prefix_str
    MakingRelation.actor()
    relationDict = MakingRelation.outputDict

    CvtoTAB = libConvert.cvtJSONtoDSV()
    CvtoTAB.requested_argv_dict = {
        "files" : [<INPUT>,<INPUT>......] ,
        "header": [<NAME>,<NAME>......] # for sorting
        "delimiter": "\t"
    }
    CvtoTAB.actor()

   --- README ---
"""

class cvtDSVtoJSON(pyWorkFlow.workflow):
    def personalize(self):
        # self.testing = True
        self.type = "library"

        self.requested_argv_dict = {
            "files": [],
            "refer_column": "",
            "prefix": "",
            "header": [],
            "headless": True,
            "delimiter": "\t"
        }

        self.target_file_path = ""

        self.comand_line_list=[]

        self.script_name = "libConvert.cvtDSVtoJSON"
        self.requested_config_dict = {}
        self.log_file_prefix_str = "temp/tmp-"

    def actor(self):
        sourceFilesList = self.requested_argv_dict.get("files",[])
        referColumnNameStr = self.requested_argv_dict.get("refer_column","")
        prefixStr = self.requested_argv_dict.get("prefix","")
        headerList = self.requested_argv_dict.get("header",[])
        headlessBoo = self.requested_argv_dict.get("headless",True)
        delimiterStr = self.requested_argv_dict.get("delimiter","\t")
        self.startLog()
        #
        self.phrase_str = "Total files: "+pprint.pformat(sourceFilesList)
        self.printTimeStamp()
        #
        for sourceFilenameStr in sourceFilesList:
            #
            self.phrase_str = "{Now processing} "+sourceFilenameStr
            self.printTimeStamp()
            #
            name_temp_list = sourceFilenameStr.split(".")
            name_temp_list[-1] = "json"
            resultFilenameStr = ".".join(name_temp_list)

            self.target_file_path = resultFilenameStr
            result_file_boolean = self.checkFile()

            if not result_file_boolean:
                #
                self.phrase_str = "{Loading Files} "+sourceFilenameStr
                self.printTimeStamp()
                #
                linesList = open(sourceFilenameStr).read().splitlines()
                first_line_boolean = True
                max_digit_num = len(linesList)
                line_num = 0
                while first_line_boolean and line_num < max_digit_num:
                    lineStr = linesList[0]
                    if lineStr[0] == "#":
                        del linesList[0]
                    else:
                        firstLineStr = linesList[0]
                        first_line_boolean = False
                    line_num = line_num + 1

                positionDict = dict() # {numbering:key}

                idKeyValueDict = dict()
                relationDict = {
                    "{key:{value:[id]}}" : dict(),
                    "{key:{id:[value]}}" : dict()
                }
                #
                self.phrase_str = "{Create Header/Key List} "+sourceFilenameStr
                self.printTimeStamp()
                #
                if not headlessBoo:
                    if headerList == []:
                        tempLineStr = linesList.pop(0)
                        headerList = tempLineStr.split(delimiterStr)
                else:
                    column_temp_list = firstLineStr.split(delimiterStr)
                    max_digit_num = len(str(len(column_temp_list)))
                    for column_num in range(len(column_temp_list)):
                        digit_num = len(str(len(column_num)))
                        if digit_num != max_digit_num:
                            diff_digit_num = max_digit_num - digit_num
                        else:
                            diff_digit_num = 0
                            #
                        headerList.append(
                            "Column_"+("0"*diff_digit_num)+str(column_num)
                        )
                #
                self.phrase_str = "{Assign Key's Position} "+sourceFilenameStr
                self.printTimeStamp()
                #
                for number in range(len(headerList)):
                    if headerList[number] not in positionDict.values():
                        positionDict.update({ number : headerList[number] })
                    if headerList[number] not in relationDict.get("{key:{value:[id]}}").keys():
                        relationDict.get("{key:{value:[id]}}").update({ headerList[number] :{} })
                    if headerList[number] not in relationDict.get("{key:{id:[value]}}").keys():
                        relationDict.get("{key:{id:[value]}}").update({ headerList[number] :{} })

                referColumnExistBoo = False
                if referColumnNameStr != "":
                    referColumnExistBoo = True
                #
                self.phrase_str = "{Start Conversion} "+sourceFilenameStr
                self.printTimeStamp()
                #
                lineIdInt = 0
                CurrentlineCountInt = 0
                TotalLineCountInt = len(linesList)
                for lineStr in linesList:
                    CurrentlineCountInt = CurrentlineCountInt + 1
                    if lineStr[0] != "#":
                        #
                        wordStr = "["+str(CurrentlineCountInt)+"/"+str(TotalLineCountInt)+"]"
                        print(wordStr,end="\r")
                        #
                        tempValueList = lineStr.split(delimiterStr)
                        tempKeyValueDict = dict()
                        idStr = ""
                        #
                        lineIdInt = lineIdInt + 1
                        if not referColumnExistBoo:
                            idStr = prefixStr + str(lineIdInt)
                            #
                        if len(tempValueList) == len(positionDict.keys()):
                            for number in range(len(list(positionDict.keys()))):
                                keyStr = positionDict.get(number)
                                tempKeyValueDict.update({ keyStr : tempValueList[number]})
                                if keyStr == referColumnNameStr and referColumnExistBoo:
                                    idStr = tempValueList[number]
                                    #
                            if idStr != "":
                                targetValueDict = idKeyValueDict.get(idStr,dict())
                                for keyStr in tempKeyValueDict.keys():
                                    tempList = targetValueDict.get(keyStr,list())
                                    tempList.append(tempKeyValueDict[keyStr])
                                    targetValueDict.update({ keyStr : list(set(tempList)) })
                                    #
                                idKeyValueDict.update({ idStr : targetValueDict })
                            else:
                                # print(lineStr)
                                self.phrase_str = "[{}/{}] Line without id".format(str(CurrentlineCountInt),str(TotalLineCountInt))
                                self.printPhrase()
                        else:
                            print('line: '+str(lineIdInt))
                #
                self.phrase_str = "{Rearrange Relation Dict.} "+sourceFilenameStr
                self.printTimeStamp()
                #
                MakingRelation = makingRelation()
                MakingRelation.inputDict = dict()
                MakingRelation.inputDict.update(idKeyValueDict)
                MakingRelation.log_file_prefix_str = self.log_file_prefix_str
                MakingRelation.actor()
                relationDict = MakingRelation.outputDict
                #
                with open(resultFilenameStr,"w") as result_file_handle:
                    json.dump(idKeyValueDict,result_file_handle,indent=4,sort_keys=True)

                filenameStr = resultFilenameStr.replace(".json","-KeyValueIdDict.json")
                with open(filenameStr,"w") as relation_file_handle:
                    json.dump(relationDict["{key:{value:[id]}}"],relation_file_handle,indent=4,sort_keys=True)

                filenameStr = resultFilenameStr.replace(".json","-KeyIdValueDict.json")
                with open(filenameStr,"w") as relation_file_handle:
                    json.dump(relationDict["{key:{id:[value]}}"],relation_file_handle,indent=4,sort_keys=True)

                filenameStr = resultFilenameStr.replace(".json","-KeyMetadata.json")
                with open(filenameStr,"w") as relation_file_handle:
                    json.dump(relationDict["metadata"],relation_file_handle,indent=4,sort_keys=True)



        self.stopLog()

class makingRelation(pyWorkFlow.workflow):
    def personalize(self):
        # self.testing = True
        self.type = "library"

        self.requested_argv_dict = dict()
        self.inputDict = dict()
        self.outputDict = dict()

        self.target_file_path = ""

        self.comand_line_list = list()

        self.script_name = "libConvert.makingRelation"
        self.requested_config_dict = dict()
        self.log_file_prefix_str = "temp/tmp-"

    def actor(self):
        self.startLog()

        valueIdDict = dict()
        idValueDict = dict()
        metaDict = dict()

        for idStr in list(self.inputDict.keys()):
            keyValueDict = self.inputDict.get(idStr)

            for keyStr in list(keyValueDict.keys()):
                sourceValueList = keyValueDict.get(keyStr)
                for valueStr in sourceValueList:
                    tempValueIdDict = valueIdDict.get(keyStr,{})
                    tempIdValueDict = idValueDict.get(keyStr,{})

                    valueList = tempIdValueDict.get(idStr,[])
                    valueList.append(valueStr)
                    tempIdValueDict.update({ idStr : valueList })

                    idList = tempValueIdDict.get(valueStr,[])
                    idList.append(idStr)
                    tempValueIdDict.update({ valueStr : idList })

                    valueIdDict.update({ keyStr : tempValueIdDict })
                    idValueDict.update({ keyStr : tempIdValueDict })

        targetValueIdDict = dict()
        keyValueCountDict = dict()
        for keyStr in valueIdDict.keys():
            targetValueDict = dict()
            valueIdCountDict = dict()
            for valueStr in valueIdDict[keyStr].keys():
                idList = valueIdDict[keyStr][valueStr]
                targetSet = sorted(list(set(idList)))
                if targetSet != [""] and idList != []:
                    targetValueDict.update({ valueStr : targetSet })
                    #
                    valueCountInt = valueIdCountDict.get(len(targetSet),0)
                    valueCountInt = valueCountInt + 1
                    valueIdCountDict.update({ len(targetSet) : valueCountInt })
            targetValueIdDict.update({ keyStr : targetValueDict })
            keyValueCountDict.update({ keyStr : valueIdCountDict })

        targetIdValueDict = dict()
        keyIdCountDict = dict()
        for keyStr in idValueDict.keys():
            targetIdDict = dict()
            idValueCountDict = dict()
            for idStr in idValueDict[keyStr].keys():
                valueList = idValueDict[keyStr][idStr]
                targetSet = sorted(list(set(valueList)))
                if targetSet != [""] and valueList != []:
                    targetIdDict.update({ idStr : targetSet })
                    #
                    idCountInt = idValueCountDict.get(len(targetSet),0)
                    idCountInt = idCountInt + 1
                    idValueCountDict.update({ len(targetSet) : idCountInt })
            targetIdValueDict.update({ keyStr : targetIdDict })
            keyIdCountDict.update({ keyStr : idValueCountDict })

        metaDict.update({ "count(id):valueAmount" : keyValueCountDict })
        metaDict.update({ "count(value):idAmount" : keyIdCountDict })
        self.outputDict = {
            "{key:{value:[id]}}" : targetValueIdDict,
            "{key:{id:[value]}}" : targetIdValueDict,
            "metadata" : metaDict,
        }

        self.stopLog()

"""
class cvtJSONtoDSV(pyWorkFlow.workflow):
    def personalize(self):
        # self.testing = True
        self.type = "library"

        self.requested_argv_dict = {
            "files" : [],
            "header" : [],
            "delimiter": "\t"
        }

        self.target_file_path = ""

        self.comand_line_list=[]

        self.script_name = "libConvert.cvtJSONtoDSV"
        self.requested_config_dict = {}
        self.log_file_prefix_str = "temp/tmp-"

    def actor(self):
        sourceFilesList = self.requested_argv_dict.get("files",[])
        headerList = self.requested_argv_dict.get("header",[])
        delimiterStr = self.requested_argv_dict.get("delimiter","\t")
        self.startLog()

        for sourceFilenameStr in sourceFilesList:
            source_file_handle = open(sourceFilenameStr,'r')
            source_json_dict = json.load(source_file_handle)

            if headerList == []:
                column_name_set = set()
                value_temp_dict = dict()
                for id_name in list(source_json_dict.keys()):
                    value_temp_dict = source_json_dict.get(id_name,{})
                    column_name_set.update(set(value_temp_dict.keys()))
                header_tuple = tuple(sorted(column_name_set))
            else:
                header_tuple = tuple(headerList)

            with open(sourceFilenameStr.replace(".json",".dsv"),"w") as result_file_handle:
                result_file_handle.write("id"+delimiterStr+delimiterStr.join(header_tuple)+"\n")
                for id_name in list(source_json_dict.keys()):
                    lineStr = id_name
                    value_temp_dict = dict()
                    value_temp_dict = source_json_dict.get(id_name,{})
                    for column_name in header_tuple:
                        lineStr = lineStr + delimiterStr + value_temp_dict.get(column_name,"")
                    result_file_handle.write(lineStr+"\n")

        self.stopLog()

class attributionExtractor(pyWorkFlow.workflow):
    def personalize(self):
        # self.testing = True
        self.type = "library"

        self.helper_msg_str = helper_msg_block

        self.requested_argv_dict = {
            "gff.json": [],
        }

        self.comand_line_list = []
        self.script_name = "libConvert.attributionExtractor"
        self.requested_config_dict = {}
        self.log_file_prefix_str = "temp/tmp-"

    def actor(self):
        sourceFilesList = self.requested_argv_dict.get("gff.json",[])
        self.startLog()

        WordProc = wordProcess()

        for sourceFilenameStr in sourceFilesList:
            target_file_name = sourceFilenameStr.replace("-relation.json",".json")
            target_file_name = target_file_name.replace(".json","-relation.json")

            self.target_file_path = target_file_name
            target_file_boolean = self.checkFile()

            if target_file_boolean:
                self.phrase_str = "Extracting "+target_file_name
                self.printTimeStamp()

                target_file_handle = open(target_file_name,'r')
                target_json_dict = json.load(target_file_handle)

                key_id_value_dict = target_json_dict.get('{key:{id:value}}')
                raw_temp_dict = key_id_value_dict.get('attribute')
                result_dict = {} # id=[key:value]
                relationDict = {
                    "{key:{value:[id]}}" : {},
                    "{key:{id:value}}" : {}
                }

                for gffid_name in list(raw_temp_dict.keys()):
                    attribution_str = raw_temp_dict.get(gffid_name)
                    attribution_temp_dict = {}

                    for paired_set_str in attribution_str.split(";"):
                        paired_set_list = paired_set_str.split("=")
                        key_str = paired_set_list[0]
                        value_str = paired_set_list[1]
                        # value_str = WordProc.changeESC(value_str)
                        attribution_temp_dict.update({ key_str : value_str })

                        value_temp_dict = relationDict.get("{key:{value:[id]}}").get(key_str,{})
                        value_temp_dict.update({ value_str : [gffid_name] })
                        relationDict.get("{key:{value:[id]}}").update({ key_str : value_temp_dict })

                        gffid_temp_dict = relationDict.get("{key:{id:value}}").get(key_str,{})
                        gffid_temp_dict.update({ gffid_name : value_str })
                        relationDict.get("{key:{id:value}}").update({ key_str : gffid_temp_dict })

                    result_dict.update({ gffid_name : attribution_temp_dict })


                resultFilenameStr = target_file_name.replace("-relation.json","-attribution.json")
                with open(resultFilenameStr,"w") as result_file_handle:
                    json.dump(result_dict,result_file_handle,indent=4,sort_keys=True)

                relation_file_name = target_file_name.replace("-relation.json","-attribution-relation.json")
                with open(relation_file_name,"w") as relation_file_handle:
                    json.dump(relationDict,relation_file_handle,indent=4,sort_keys=True)

        self.stopLog()
        
class wordProcess:
    def __init__(self):
        self.input_file_name = ""

    def loadSymbolDict(self):
        library_file_name = 'esc.json'
        library_file_handle = open(library_file_name,'r')
        self.libDict = json.load(library_file_handle)

    def recoverSymbol(self):
        self.input_lines = open(self.input_file_name).read().splitlines()
        self.output_lines = []

        for lineStr in self.input_lines:
            if "%" in lineStr:
                for key_str in set(self.libDict.keys()):
                    value_str = self.libDict.get(key_str)
                    lineStr = lineStr.replace(key_str,value_str)
                self.output_lines.append(lineStr)
            else:
                self.output_lines.append(lineStr)

    def removeTAB(self):
        self.input_lines = open(self.input_file_name).read().splitlines()
        self.output_lines = []

        for lineStr in self.input_lines:
            lineStr = lineStr.replace("\t","")
            self.output_lines.append(lineStr)

    def removeQuotation(self):
        self.input_lines = open(self.input_file_name).read().splitlines()
        self.output_lines = []

        for lineStr in self.input_lines:
            lineStr = lineStr.replace("\"","")
            lineStr = lineStr.replace("\'","")
            self.output_lines.append(lineStr)

    def save(self):
        with open(self.input_file_name,'w') as output_file_handle:
            for lineStr in self.output_lines:
                output_file_handle.write(lineStr+"\n")

"""