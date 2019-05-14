#!/usr/bin/env python3
import sys, pprint, json, pathlib
import libPrint
global helper_msg_block
helper_msg_block="""
   --- README of Conversion Library ---
  Title:
    Conversion tool for JSON and TSV/CTAB

  Usage:
    import libConvert

    CvtoJSON = libConvert.convertDSVtoJSON()
    CvtoJSON.argumentDict = {
		"files": [],
		"refer_column": "",
		"prefix": "",
		"header": [],
		"headless": True,
		"delimiter": "\t"
	}
    CvtoJSON.converting()

    MakingRelation = relationGeneration()
    MakingRelation.inputDict = dict()
    MakingRelation.inputDict.update(idKeyValueDict)
    MakingRelation.logFilenameStr = self.logFilenameStr+"-relation"
    MakingRelation.generating()
    relationDict = MakingRelation.outputDict

   --- README ---
"""

class convertDSVtoJSON:
    def __init__(self):
        self.testingBool = False
        self.logFilenameStr = ""
        self.folderStr = "data/log/"

        self.argumentDict = {
            "files": [],
            "refer_column": "",
            "prefix": "",
            "header": [],
            "headless": True,
            "delimiter": "\t"
        }

    def converting(self):
        sourceFilesList = self.argumentDict.get("files",[])
        referColumnNameStr = self.argumentDict.get("refer_column","")
        prefixStr = self.argumentDict.get("prefix","")
        headerList = self.argumentDict.get("header",[])
        headlessBoo = self.argumentDict.get("headless",True)
        delimiterStr = self.argumentDict.get("delimiter","\t")

        Print = libPrint.timer()
        Print.logFilenameStr = self.logFilenameStr
        Print.folderStr = self.folderStr
        Print.testingBool = self.testingBool
        Print.startLog()

        Print.phraseStr = "Total files: "+pprint.pformat(sourceFilesList)
        Print.printTimeStamp()
        #
        for sourceFilenameStr in sourceFilesList:
            #
            Print.phraseStr = "{Now processing} "+sourceFilenameStr
            Print.printTimeStamp()
            #
            tempFilenamelist = sourceFilenameStr.split(".")
            tempFilenamelist[-1] = "json"
            resultFilenameStr = ".".join(tempFilenamelist)

            resultFileBo = pathlib.Path(resultFilenameStr).exists()

            if not resultFileBo:
                #
                Print.phraseStr = "{Loading Files} "+sourceFilenameStr
                Print.printTimeStamp()
                #
                linesList = open(sourceFilenameStr).read().splitlines()
                firstLineBo = True
                maxDigitInt = len(linesList)
                lineNumInt = 0
                while firstLineBo and lineNumInt < maxDigitInt:
                    lineStr = linesList[0]
                    if lineStr[0] == "#":
                        del linesList[0]
                    else:
                        firstLineStr = linesList[0]
                        firstLineBo = False
                    lineNumInt = lineNumInt + 1

                positionDict = dict() # {numbering:key}

                idKeyValueDict = dict()
                relationDict = {
                    "{key:{value:[id]}}" : dict(),
                    "{key:{id:[value]}}" : dict()
                }
                #
                Print.phraseStr = "{Create Header/Key List} "+sourceFilenameStr
                Print.printTimeStamp()
                #
                if not headlessBoo:
                    if headerList == []:
                        tempLineStr = linesList.pop(0)
                        headerList = tempLineStr.split(delimiterStr)
                else:
                    column_temp_list = firstLineStr.split(delimiterStr)
                    maxDigitInt = len(str(len(column_temp_list)))
                    for column_num in range(len(column_temp_list)):
                        digit_num = len(str(len(column_num)))
                        if digit_num != maxDigitInt:
                            diff_digit_num = maxDigitInt - digit_num
                        else:
                            diff_digit_num = 0
                            #
                        headerList.append(
                            "Column_"+("0"*diff_digit_num)+str(column_num)
                        )
                #
                Print.phraseStr = "{Assign Key's Position} "+sourceFilenameStr
                Print.printTimeStamp()
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
                Print.phraseStr = "{Start Conversion} "+sourceFilenameStr
                Print.printTimeStamp()
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
                                Print.phraseStr = "[{}/{}] Line without id".format(str(CurrentlineCountInt),str(TotalLineCountInt))
                                Print.printPhrase()
                        else:
                            print('line: '+str(lineIdInt))
                #
                Print.phraseStr = "{Rearrange Relation Dict.} "+sourceFilenameStr
                Print.printTimeStamp()
                #
                MakingRelation = relationGeneration()
                MakingRelation.inputDict = dict()
                MakingRelation.inputDict.update(idKeyValueDict)
                MakingRelation.logFilenameStr = self.logFilenameStr+"-relation"
                MakingRelation.generating()
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



        Print.stopLog()

class relationGeneration:
    def __init__(self):
        self.testingBool = False
        self.logFilenameStr = ""
        self.folderStr = "data/log/"

        self.argumentDict = dict()
        self.inputDict = dict()
        self.outputDict = dict()

    def generating(self):
        Print = libPrint.timer()
        Print.logFilenameStr = self.logFilenameStr
        Print.folderStr = self.folderStr
        Print.testingBool = self.testingBool
        Print.startLog()

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

        Print.stopLog()
