#!/usr/bin/env python3
import sys, pprint, json
import librun

class tab2json(librun.loggi):

    def pesonai(self):
        # self.testing = True

        self.dicodi = {
            "files" : [],
            "id" : ""
        }
        self.sync()

        self.tagesi = ""

        self.comali=[]

        self.filasi = "libtab.py"
        self.libadi = {}
        self.prelogi = "tmp/tmp-"

    def actor(self):
        soceli = self.dicodi.get("files",[])
        tagesi = self.dicodi.get("id","")
        print((soceli,tagesi))

        for socesi in soceli:
            print(socesi)
            lineli = open(socesi).read().splitlines()
            adnubo = True
            namedi = {}

            resudi = {}
            remadi = {}

            for line in lineli:
                if adnubo:
                    metali = line.split("	")
                    for n in range(len(metali)):
                        if metali[n] not in namedi.values():
                            namedi.update({ n : metali[n] })
                        if metali[n] not in remadi.keys():
                            remadi.update({ metali[n] :{} })
                    adnubo = False
                else:
                    metali = line.split("	")
                    metadi = {}
                    idisi = ""

                    for n in range(len(list(namedi.keys()))):
                        colusi = namedi.get(n)
                        metadi.update({ colusi : metali[n]})

                        if colusi == tagesi:
                            idisi = metali[n]

                    resudi.update({ idisi : metadi })

                    for n in range(len(list(namedi.keys()))):
                        colusi = namedi.get(n)

                        almedi = remadi.get(colusi,{})
                        almeli = almedi.get(metali[n],[])

                        almeli.append(idisi)

                        almedi.update({ metali[n] : almeli })
                        remadi.update({ colusi : almedi })


            with open(socesi.split(".")[0]+".json","w") as resufi:
                json.dump(resudi,resufi,indent=4,sort_keys=True)

            with open(socesi.split(".")[0]+"-column.json","w") as resufi:
                json.dump(remadi,resufi,indent=4,sort_keys=True)

class json2tab(librun.loggi):

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
