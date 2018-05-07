import pprint, time, json, sys
from subprocess import call
global helber
helber="""
   --- README of exp00-librun ---
 Title:
    General class for bio-info-misc project

 Usage:
    import this library while running you python scripts

 Structure:
    First : tribe,
        e.g. raw, untrim, trimmed...
    Second: group,
        e.g. control, A, B, 1, 2...
    Third : subgroup/files,
        e.g. foward, reverse, pair, unpair

    Visualise graph: explanation01-dataStructure.png

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

class loggi:

    def pesonai(self):
        self.dicli = {
            "hello" : ""
        }
        self.sync()
        self.filasi = "librun.py"

        self.comali=['echo','wahaha']

        self.libadi = {}
        self.prelogi = "temp/temp-"

    class confi:
        def loadso(self):
            configfi = "data/config.json"
            configfa = open(configfi,'r')
            self.confi = json.load(configfa)
        def get(self,wodsi):
            resut = self.confi.get(wodsi)
            return resut
        def getli(self,wodli):
            resut = ""
            for n in wodli:
                resut = resut + "/" + self.confi.get(wodsi,"")
            return resut
        def check(self,wodsi):
            resut = False
            metali = list(self.confi.keys())
            if wodsi in metali:
                resut = True
            return resut

        def __init__(self):
            self.loadso()

    def hebe(self):
        print('haha')

    def sync(self):
        print('hehe')

    def printe(self):
        print(self.frasi)
        with open(self.logisi,'a') as logifa:
            logifa.write(self.frasi+"\n")

    def maxlen(self):
        metali = []
        for namasi in self.lisli:
            metali.append(len(namasi))
        return max(metali)

    def timme(self):
        yearsi = self.timosi[0:4]
        montsi = self.timosi[4:6]
        dayesi = self.timosi[6:8]
        hoursi = self.timosi[8:10]
        minusi = self.timosi[10:12]
        secosi = self.timosi[12:14]

        if len(self.sepere) != 3:
            self.sepere =  "-_-"
        timaki = (self.sepere[0].join([yearsi,montsi,dayesi]) +
            self.sepere[1] + self.sepere[2].join([hoursi,minusi,secosi]))

        return timaki

    def argv(self):
        metali = self.siarli
        metasi = " ".join(self.siarli)
        while "--" in metasi:
            metali = metasi.split(" ")
            for n in range(len(metali)):
                if "--" == metali[n][0:2]:
                    semesi = metali.pop(n)
                    semesi = semesi.split("--")[1]
                    if "=" in semesi:
                        semeli = semesi.split("=")
                        self.argudi.update({ semeli[0] : [semeli[1]] })
                        metasi = " ".join(metali)
                        break

        self.siarli = metali
        arguli = []

        for nanasi in range(len(self.siarli)):
            if self.siarli[nanasi][0] == '-':
                arguli.append(nanasi)

        for n in arguli:
            metasi = self.siarli[n]
            metasi = metasi.split("-")[1]
            metali = self.argudi.get(metasi,[])

            if arguli.index(n) == 0:
                self.argudi.update({ "argv" : self.siarli[0:n] })
                metali.extend(self.siarli[n+1:arguli[arguli.index(n)+1]])
            elif arguli.index(n) == len(arguli)-1:
                metali.extend(self.siarli[n+1:len(self.siarli)])
            else:
                metali.extend(self.siarli[n+1:arguli[arguli.index(n)+1]])

            self.argudi.update({ metasi : metali })

        metatu = tuple(self.argudi.keys())
        for argu in metatu:
            if len(argu) == 1 and self.Confi.check("synom/"+argu):
                metali = list(self.Confi.confi.keys())
                metadi = {}
                for meta in metali:
                    metasi = ""
                    if "synom/" in meta:
                        metasi = self.Confi.confi.get(meta)
                        metadi.update({
                            meta.replace("synom/","") : metasi
                        })

        for meta in metatu:
            if meta in list(metadi.keys()):
                metali = []
                metasi = metadi.get(meta)
                metali = self.argudi.get(metasi,[])
                metali.extend(self.argudi.get(meta))
                self.argudi.update({ metasi : metali })

    def hedda(self):
        self.begisi = time.strftime("%Y%m%d%H%M%S")

        self.timosi = time.strftime("%Y%m%d%H%M%S")

        self.sepere = "- :"
        runninlog = ("RUN "+self.filasi+", begin at ["
            + self.timme() +"]\n~~~~~~~~~~~~\n" )

        if self.locadi != {}:
            scriptlog = "LOCAL\n"

            self.lisli = []
            self.lisli = list(self.locadi.keys())
            metain = self.maxlen()
            for loca in self.lisli:
                if len(loca) < metain :
                    loca = loca + ' '*(metain-len(loca))

                scriptlog = (scriptlog + "    " + loca + ": " +
                    pprint.pformat(self.locadi.get(loca)) + "\n")

        else:
            scriptlog = ""

        if self.libadi != {}:
            configlog = "FROM config.json\n"

            self.lisli = []
            self.lisli = list(self.libadi.keys())
            metain = self.maxlen()
            for liba in self.lisli:
                if len(loca) < metain :
                    liba = "\"" + liba + "\"" + ' '*(metain-len(liba))
                else:
                    liba = "\"" + liba + "\""

                configlog = (configlog + "    " + liba + ": " +
                    pprint.pformat(self.libadi.get(liba)) + "\n")

        else:
            configlog = ""

        self.sepere = "-_-"
        self.logisi = self.prelogi + self.timme() + '.log'

        self.frasi = runninlog + scriptlog + "\n" + configlog
        self.printe()

        self.timosi = ""
        self.frasi = ""
        self.sepere = ""

    def ranni(self):
        self.timosi = time.strftime("%Y%m%d%H%M%S")

        self.sepere = "- :"
        runisi = "\n[" + self.timme() + "]"
        comasi = " Command: " + " ".join(self.comali)

        self.frasi = runisi + comasi
        self.printe()

        call(self.comali, stdout=open(self.logisi, 'a'))

        self.timosi = ""
        self.frasi = ""
        self.sepere = ""

    def calti(self):
        self.timosi = time.strftime("%Y%m%d%H%M%S")
        yedifi = int(self.timosi[0:4])-int(self.begisi[0:4])
        modifi = int(self.timosi[4:6])-int(self.begisi[4:6])
        dadifi = int(self.timosi[6:8])-int(self.begisi[6:8])
        hodifi = int(self.timosi[8:10])-int(self.begisi[8:10])
        midifi = int(self.timosi[10:12])-int(self.begisi[10:12])
        sedifi = int(self.timosi[12:14])-int(self.begisi[12:14])

        if sedifi < 0 :
            midifi = midifi -1
            sedifi = sedifi + 60
        if midifi < 0 :
            hodifi = hodifi -1
            midifi = midifi + 60
        if hodifi < 0 :
            dadifi = dadifi -1
            hodifi = hodifi + 24

        if dadifi < 0 :
            resut = "More than one month..."
        else:
            resut = (
                str(hodifi) + " hr "+
                str(midifi) + " min "+
                str(sedifi) + " s "
            )

        self.frasi = resut
        self.printe()

        self.frasi = ""
        self.timosi = ""

    def __init__(self):
        self.hebesi = helber
        self.siarli = sys.argv
        self.argudi = {}
        self.begisi=""
        self.logisi=""

        self.timosi = ""
        self.frasi = ""
        self.sepere = ""
        self.lisli = []

        self.Confi = self.confi()
        self.argv()
        self.pesonai()

        self.locadi = {
            'Input' : self.siarli,
            'Argv.' : self.argudi
        }
