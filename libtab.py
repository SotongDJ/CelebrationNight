#!/usr/bin/env python3
import sys, pprint, json
import librun
global helber
helber="""
   --- README of library-tab ---
  Title:
    Conversion tool for JSON and TSV/CTAB

  Usage:
    import libtab

    class covejos(libtab.tab2json):
        def redirek(self):
            """"""
    CoveJos = covejos()
    CoveJos.dicodi = {
        "files" : [<INPUT>,<INPUT>......] ,
        "id" : "" ,
        "column": < Column separate by tab >
    }
    CoveJos.actor()

    class covetab(libtab.json2tab):
        def redirek(self):
            """"""
    CoveTab = covetab()
    CoveTab.dicodi = { "files" : [<INPUT>,<INPUT>......] }
    CoveTab.actor()

   --- README ---
""""""
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
class tab2json(librun.loggi):

    def pesonai(self):
        # self.testing = True

        self.dicodi = {
            "files" : [],
            "id" : "",
            "column" : ""
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
        comusi = self.dicodi.get("column","")
        print((soceli,tagesi,len(comusi)))


        for socesi in soceli:
            print(socesi)
            lineli = open(socesi).read().splitlines()

            namedi = {}

            resudi = {}
            remadi = {}


            if comusi != "":
                metali = comusi.split("	")
                for n in range(len(metali)):
                    if metali[n] not in namedi.values():
                        namedi.update({ n : metali[n] })
                    if metali[n] not in remadi.keys():
                        remadi.update({ metali[n] :{} })
                colubo = False
            else:
                colubo = True

            if tagesi != "":
                tagebo = True
            else:
                tagebo = False

            numein = 0
            for line in lineli:
                if colubo:
                    metali = line.split("	")
                    for n in range(len(metali)):
                        if metali[n] not in namedi.values():
                            namedi.update({ n : metali[n] })
                        if metali[n] not in remadi.keys():
                            remadi.update({ metali[n] :{} })
                    colubo = False
                elif "#" not in line:
                    metali = line.split("	")
                    metadi = {}
                    idisi = ""

                    if not tagebo:
                        numein = numein + 1
                        idisi = str(numein)

                    for n in range(len(list(namedi.keys()))):
                        colusi = namedi.get(n)
                        metadi.update({ colusi : metali[n]})

                        if colusi == tagesi and tagebo:
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
