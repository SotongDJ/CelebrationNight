import pprint, time, json, sys
import libconfig
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
        # self.testing = True
        self.typesi = 'library'

        self.dicodi = {
            "hello" : ""
        }
        self.sync()

        self.tagesi = ""

        self.comali=['echo','wahaha']

        self.filasi = "librun.py"
        self.libadi = {
            "prefix/wawa" : "haha/wulala"
        }
        self.prelogi = "temp/temp-"

    def actor(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])

        self.hedda()

        self.tagesi = "temp"
        self.chkpaf()

        self.ranni()

        self.calti()

    def redirek(self):
        if self.typesi == "script":
            self.actor()

    def sync(self):
        for dico in tuple(self.dicodi.keys()):
            if dico in tuple(self.argudi.keys()):
                arti = type(self.dicodi.get(dico))
                bati = type(self.argudi.get(dico))

                siti = type(str())
                liti = type(list())

                if bati == liti: # if type(b) == list
                    babo = len(self.argudi.get(dico)) > 0

                if arti == bati: # if type(a) == type(b)
                    self.dicodi.update({ dico : self.argudi.get(dico) })
                elif bati == siti and arti == liti:
                    self.dicodi.update({ dico : [self.argudi.get(dico)] })
                elif bati == liti and arti == siti and babo:
                    metali = sorted(self.argudi.get(dico))
                    self.dicodi.update({ dico : metali[0] })

    def printe(self):
        print(self.frasi)
        with open(self.logisi,'a') as logifa:
            logifa.write(self.frasi+"\n")

    def printbr(self):
            print("  ")
            with open(self.logisi,'a') as logifa:
                logifa.write("  \n")

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
        arbeli = []
        metali = self.siarli
        metasi = " ".join(self.siarli)
        while "--" in metasi:
            metali = metasi.split(" ")
            for n in range(len(metali)):
                if "--" == metali[n][0:2]:
                    if "=" in metali[n]:
                        semesi = metali.pop(n)
                        semesi = semesi.split("--")[1]
                        semeli = semesi.split("=")
                        self.argudi.update({ semeli[0] : [semeli[1]] })
                        metasi = " ".join(metali)
                        break
                    else:
                        semesi = metali.pop(n)
                        arbeli.append(semesi.replace("--",""))
                        metasi = " ".join(metali)
                        break

        self.siarli = metasi.split(" ")
        arguli = []

        for nanasi in range(len(self.siarli)):
            if self.siarli[nanasi][0] == '-':
                arguli.append(nanasi)

        begibo = True
        for n in arguli:
            metasi = self.siarli[n]
            metasi = metasi.split("-")[1]
            metali = self.argudi.get(metasi,[])

            begoin = n+1

            endoin = 0
            if arguli.index(n) == 0:
                arbeli.extend(self.siarli[1:n])
                begibo = False

            if arguli.index(n) == len(arguli)-1:
                endoin = len(self.siarli)
            else:
                endoin = arguli[arguli.index(n)+1]

            if begoin > len(self.siarli):
                begoin = len(self.siarli)
            if endoin > len(self.siarli):
                endoin = len(self.siarli)

            metali.extend(self.siarli[begoin:endoin])
            self.argudi.update({ metasi : metali })

        if begibo:
            arbeli.extend(self.siarli[1:len(self.siarli)])
        self.argudi.update({ "argv" : list(set(arbeli)) })

        metatu = tuple(self.argudi.keys())
        metadi = {}
        for argu in metatu:
            if len(argu) == 1 and self.Confi.check("synom/"+argu):
                metali = list(self.Confi.confi.keys())
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
            + self.timme() +"]\n~~~~~~~~~~~~" )

        self.locadi = {
            'Input' : self.siarli,
            'Argv.' : self.argudi,
            'Para.' : self.dicodi
        }

        scriptlog = ["LOCAL"]

        self.lisli = []
        self.lisli = list(self.locadi.keys())
        metain = self.maxlen()
        for loca in self.lisli:
            if len(loca) < metain :
                loca = loca + ' '*(metain-len(loca))

            scriptlog.append("    " + loca + ": " +
                pprint.pformat(self.locadi.get(loca),compact=True,width=150))

        if self.libadi != {}:
            configlog = ["FROM config.json"]

            self.lisli = []
            self.lisli = list(self.libadi.keys())
            metain = self.maxlen()
            for liba in self.lisli:
                if len(liba) < metain :
                    semein = metain-len(liba)
                else:
                    semein = 0

                configlog.append("    \"" + liba + "\""+ (" "*semein) +": "+
                    pprint.pformat(self.libadi.get(liba)))

        else:
            configlog = []

        self.sepere = "-_-"
        self.logisi = self.prelogi + self.timme() + '.log'

        metali = [runninlog]
        metali.extend(scriptlog)
        metali.extend(configlog)
        self.frasi = "\n".join(metali)
        self.printe()

        self.timosi = ""
        self.frasi = ""
        self.sepere = ""

    def chkpaf(self):
        self.timosi = time.strftime("%Y%m%d%H%M%S")

        tageli = [ "mkdir", "-v", self.tagesi ]

        self.sepere = "- :"
        runisi = "[" + self.timme() + "]"
        comasi = " chkpaf: " + " ".join(tageli)

        self.frasi = runisi + comasi
        self.printe()

        call(tageli, stdout=open(self.logisi, 'a'))

        self.timosi = ""
        self.frasi = ""
        self.sepere = ""

    def chkfal(self):
        resut = False

        self.timosi = time.strftime("%Y%m%d%H%M%S")
        tageli = [ "head", "-v", self.tagesi ]
        call(tageli, stdout=open("temp/head-"+self.timosi, 'a'))

        self.sepere = "- :"
        runisi = "[" + self.timme() + "]"
        comasi = " chkfal: " + " ".join(tageli)
        self.frasi = runisi + comasi
        self.printe()

        filafi = open("temp/head-"+self.timosi,"ab")
        filafi.close()
        if open("temp/head-"+self.timosi).read() != "":
            resut = True

        tageli = [ "rm", "-v", "temp/head-"+self.timosi ]
        call(tageli, stdout=open("temp/head-"+self.timosi, 'a'))

        self.timosi = time.strftime("%Y%m%d%H%M%S")
        self.sepere = "- :"
        runisi = "[" + self.timme() + "]"
        comasi = "\n        chkfal: " + " ".join(tageli)
        resusi = "\n        result: " + pprint.pformat(resut)
        self.frasi = runisi + resusi + comasi
        self.printe()

        self.timosi = ""
        self.frasi = ""
        self.sepere = ""

        return resut

    def ranni(self):
        self.timosi = time.strftime("%Y%m%d%H%M%S")
        self.sepere = "- :"
        runisi = "[" + self.timme() + "]"
        comasi = " Command: " + " ".join(self.comali)

        self.frasi = runisi + comasi
        self.printe()

        if not self.testing:
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

        self.sepere = "- :"
        runisi = "[" + self.timme() + "] Total time: "

        self.frasi = runisi + resut
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

        self.testing = False
        self.typesi = 'library'
        self.dicodi = {}

        self.Confi = libconfig.confi()
        self.argv()
        self.pesonai()

        self.redirek()
