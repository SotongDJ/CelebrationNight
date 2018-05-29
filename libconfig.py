#!/usr/bin/env python3
import json
class confi:

    def loadso(self):
        primoconfigfi = "config.json"
        primoconfigfa = open(primoconfigfi,'a+')
        primoconfigfa.close()

        if open(primoconfigfi).read() == "":
            self.confi = {}
            with open(primoconfigfi,'w') as primoconfigfa:
                primoconfigfa.write("{}")
        else:
            primoconfigfa = open(primoconfigfi,'r')
            self.confi = json.load(primoconfigfa)

        seconconfigfi = "data/config.json"
        seconconfigfa = open(seconconfigfi,'a+')
        seconconfigfa.close()

        if open(seconconfigfi).read() == "":
            with open(seconconfigfi,'w') as seconconfigfa:
                seconconfigfa.write("{}")
        else:
            seconconfigfa = open(seconconfigfi,'r')
            self.confi.update(json.load(seconconfigfa))

    def refes(self):
        self.loadso()

        primoconfigfi = "config.json"
        primoconfigfa = open(primoconfigfi,'r')
        metaso = json.load(primoconfigfa)
        with open(primoconfigfi,'w') as configfa:
            json.dump(metaso,configfa,indent=4,sort_keys=True)

        seconconfigfi = "data/config.json"
        seconconfigfa = open(seconconfigfi,'r')
        metaso = json.load(seconconfigfa)
        with open(seconconfigfi,'w') as configfa:
            json.dump(metaso,configfa,indent=4,sort_keys=True)

    def siget(self,wodsi):
        resut = self.confi.get(wodsi)
        return resut

    def liget(self,wodsi):
        resut = self.confi.get(wodsi,[])
        return resut

    def diget(self,wodsi):
        resut = self.confi.get(wodsi,{})
        return resut

    def hoget(self,wodli):
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
