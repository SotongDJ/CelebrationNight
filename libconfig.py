import json
class confi:
    def loadso(self):
        configfi = "data/config.json"
        configfa = open(configfi,'r')
        self.confi = json.load(configfa)
    def get(self,wodsi):
        resut = self.confi.get(wodsi)
        return resut
    def getli(self,wodli):
        resut = []
        for wodsi in wodli:
            resut.append(self.confi.get(wodsi,""))
        return "/".join(resut)
    def check(self,wodsi):
        resut = False
        metali = list(self.confi.keys())
        if wodsi in metali:
            resut = True
        return resut

    def __init__(self):
        self.loadso()
