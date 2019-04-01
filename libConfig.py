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
            
            print("[libConfig]Create new config dictionary")
            self.storeDict = dict()
        else:
            self.storeDict = json.load(open(pathStr))
            print("[libConfig]Finish loading")

    def save(self):
        pathStr = "{}{}.json".format(
            self.folderStr,self.queryStr
        )
        if self.modeStr == "UPDATE":
            print("[libConfig]Update json")
            sourceDict = json.load(open(pathStr))
        elif self.modeStr == "OVERWRITE":
            print("[libConfig]Overwrite json")
            sourceDict = dict()
        else:
            print("[libConfig]Overwrite json")
            sourceDict = dict()
            
        sourceDict.update(self.queryDict)

        pathlib.Path(self.folderStr).mkdir(parents=True,exist_ok=True)
        with open(pathStr,"w") as targetHandle:
            json.dump(self.queryDict,targetHandle,indent=2,sort_keys=True)

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