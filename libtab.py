#!/usr/bin/env python3
import sys, pprint, json
import librun

class runno(librun.loggi):

    def pesonai(self):
        # self.testing = True

        self.dicodi = {
            "files" : []
        }
        self.sync()

        self.tagesi = ""

        self.comali=[]

        self.filasi = "libtab.py"
        self.libadi = {}
        self.prelogi = "tmp/tmp-"

    def actor(self):
        soceli = self.dicodi.get("files",[])
        print(soceli)

        for socesi in soceli:
            socefi = open(socesi,'r')
            soceso = json.load(socefi)

            coluse = set()
            metadi = dict()
            for id in list(soceso.keys()):
                metadi = soceso.get(id,{})
                coluse.update(set(metadi.keys()))

            colutu = tuple(sorted(coluse))
            with open(socesi.replace(".json",".tsv"),"w") as resufi:
                resufi.write("id"+"	"+"	".join(colutu)+"\n")
                for id in list(soceso.keys()):
                    line = id
                    metadi = dict()
                    metadi = soceso.get(id,{})
                    for meta in colutu:
                        line = line + "	" + metadi.get(meta,"")
                    resufi.write(line+"\n")
