#!/usr/bin/env python3
import json, pathlib
class config:
    def __init__(self):
        self.queryStr = ""
        self.folderStr = "data/config/"
        self.storeDict = dict()
        self.queryDict = dict()
        self.modeStr = "OVERWRITE"

    def load(self):
        pathStr = "{}{}.json".format(
            self.folderStr,self.queryStr
        )
        pathlib.Path(self.folderStr).mkdir(parents=True,exist_ok=True)
        if not pathlib.Path(pathStr).exists():
            with open(pathStr,"w") as targetHandle:
                json.dump(dict(),targetHandle)
            
            print("[libConfig]Create new config dictionary: "+self.queryStr)
            self.storeDict = dict()
        else:
            self.storeDict = json.load(open(pathStr))
            print("[libConfig]Finish loading: "+self.queryStr)

    def save(self):
        pathStr = "{}{}.json".format(
            self.folderStr,self.queryStr
        )
        if self.modeStr == "UPDATE":
            if pathlib.Path(pathStr).exists():
                print("[libConfig]Update json: "+self.queryStr)
                sourceDict = json.load(open(pathStr))
                print("[libConfig]Finish loading: "+self.queryStr)
            else:
                print("[libConfig]Create new config dictionary: "+self.queryStr)
                sourceDict = dict()
            
        else:
            print("[libConfig]Overwrite json: "+self.queryStr)
            sourceDict = dict()
            
        sourceDict.update(self.queryDict)


        pathlib.Path(self.folderStr).mkdir(parents=True,exist_ok=True)
        with open(pathStr,"w") as targetHandle:
            json.dump(sourceDict,targetHandle,indent=2,sort_keys=True)

        print("[libConfig]Finish writing json: "+self.queryStr)

if __name__ == "__main__":
    print("__name__ == "+__name__)
    Config = config()

    Config.queryStr = "testing"
    Config.folderStr = "data/config/"
    Config.queryDict = {
        "haha" : "ha",
        "ho" : "hohoho",
    }
    Config.modeStr = "OVERWRITE"
    Config.save()

    Config.load()
    tempDict = Config.storeDict
    tempDict.update({ "hoha" : "wahahaha"})
    Config.modeStr = "UPDATE"
    Config.save()
    Config.load()