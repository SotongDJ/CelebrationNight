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

    CoveJos = libtab.tab2json()
    CoveJos.dicodi = {
        "files" : [<INPUT>,<INPUT>......] ,
        "id" : "" ,
        "column": < Column separate by tab >
    }
    CoveJos.actor()

    CoveTab = libtab.json2tab()
    CoveTab.dicodi = { "files" : [<INPUT>,<INPUT>......] }
    CoveTab.actor()

   --- README ---
"""
"""
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
    def redirek(self):
        """"""
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
        self.prelogi = "temp/tmp-"

    def actor(self):
        soceli = self.dicodi.get("files",[])
        tagesi = self.dicodi.get("id","")
        comusi = self.dicodi.get("column","")
        self.head()

        self.frasi = pprint.pformat((soceli,tagesi,len(comusi)))
        self.printimo()

        for socesi in soceli:
            self.frasi = pprint.pformat(socesi)
            self.printimo()

            metali = socesi.split(".")
            metali[-1] = "json"
            resusi = ".".join(metali)
            remasi = resusi.replace(".json","-column.json")

            self.tagesi = resusi
            resubo = self.chkfal()
            self.tagesi = remasi
            remabo = self.chkfal()

            if not resubo or not remabo :
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


                with open(resusi,"w") as resufi:
                    json.dump(resudi,resufi,indent=4,sort_keys=True)

                with open(remasi,"w") as remafi:
                    json.dump(remadi,remafi,indent=4,sort_keys=True)
        self.endin()

class json2tab(librun.loggi):
    def redirek(self):
        """"""

    def pesonai(self):
        # self.testing = True

        self.dicodi = {
            "files" : [],
            "column" : []
        }
        self.sync()

        self.tagesi = ""

        self.comali=[]

        self.filasi = "libtab.py"
        self.libadi = {}
        self.prelogi = "temp/tmp-"

    def actor(self):
        soceli = self.dicodi.get("files",[])
        coluli = self.dicodi.get("column",[])
        self.head()

        self.frasi = pprint.pformat(soceli)
        self.printimo()

        for socesi in soceli:
            socefi = open(socesi,'r')
            soceso = json.load(socefi)

            if coluli == []:
                coluse = set()
                metadi = dict()
                for id in list(soceso.keys()):
                    metadi = soceso.get(id,{})
                    coluse.update(set(metadi.keys()))
                colutu = tuple(sorted(coluse))
            else:
                colutu = tuple(coluli)

            with open(socesi.replace(".json",".tsv"),"w") as resufi:
                resufi.write("id"+"	"+"	".join(colutu)+"\n")
                for id in list(soceso.keys()):
                    line = id
                    metadi = dict()
                    metadi = soceso.get(id,{})
                    for meta in colutu:
                        line = line + "	" + metadi.get(meta,"")
                    resufi.write(line+"\n")

        self.endin()
