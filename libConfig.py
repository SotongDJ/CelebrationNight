#!/usr/bin/env python3
import json, pathlib
class config:
    def __init__(self):
        self.parentStr = "results/config/"
        self.configStr = str()
        self.configDict = dict()

    def load(self):
        pathlib.Path(self.parentStr).mkdir(parents=True,exist_ok=True)
        pathStr = "{parent}{child}.json".format(
            parent=self.parentStr,
            child=self.configStr
        )
        self.configDict = json.load(pathStr)

    def save(self):
        pathlib.Path(self.parentStr).mkdir(parents=True,exist_ok=True)
        pathStr = "{parent}{child}.json".format(
            parent=self.parentStr,
            child=self.configStr
        )
        with open(pathStr,"w") as targetHandle:
            json.dump(self.configDict,targetHandle,indent=2,sort_keys=True)

if __name__ == "__main__":
    print("__name__ == "+__name__)
    Config = config()
    Config.configStr = "testing"
    Config.save()