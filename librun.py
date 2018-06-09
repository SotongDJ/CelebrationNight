#!/usr/bin/env python3
import pprint, time, json, sys
from subprocess import call
global helber
helber="""
   --- README of library-run ---
 Title:
    General class for bio-info-misc project

 Usage:
    import librun
    class <CLASS_NAME>(librun.workflow):

        def pesonai(self):
            # self.testing = True

            self.dicodi = {
                < VAR_NAME_A > : < VAR_VALUE > ,
                < VAR_NAME_B > : < VAR_VALUE > ,
                < VAR_NAME_C > : < VAR_VALUE > ,
            }
            self.sync()

            self.tagesi = ""

            self.comali=[]

            self.filasi = < Library Name >
            self.libadi = {}
            self.prelogi = < Path of Log Files >

        def actor(self):
            < VAR_A > = self.dicodi.get(< VAR_NAME_A >,"")
            < VAR_B > = self.dicodi.get(< VAR_NAME_B >,"")
            < VAR_C > = self.dicodi.get(< VAR_NAME_C >,"")
            print((< VAR_A >, < VAR_B >, < VAR_C >))

            self.head()

            self.tagesi = < TARGET_FILE >
            self.chkpaf()

            self.runit()

            self.endin()

    Ano = <CLASS_NAME>()
    Ano.actor()

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
class dicto:
    def input(self,socedi):
        if type(socedi) == type(dict()):
            self.cotedi.update(socedi)

    def list(self):
        return list(self.cotedi.keys())

    def siget(self,askasi):
        return self.cotedi.get(askasi,"")

    def liget(self,askasi):
        return self.cotedi.get(askasi,[])

    def vomit(self):
        return self.cotedi

    def __init__(self):
        self.cotedi = {}

class workflow:

    def pesonai(self):
        # self.testing = True
        self.helb = helber

        self.dicodi = {
            "hello" : ""
        }
        self.sync()

        self.comali=['echo','wahaha']

        self.filasi = "librun.py"
        self.libadi = {
            "prefix/wawa" : "haha/wulala"
        }
        self.Synom.input({})
        self.prelogi = "temp/temp-"

    def actor(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])

        self.head()

        self.tagesi = "temp"
        self.chkpaf()

        self.runit()

        self.endin()

    def printimo(self):
        self.timosi = time.strftime("%Y%m%d%H%M%S")
        self.sepere = "- :"
        timisi = "[" + self.timme() + "] "
        print(timisi+self.frasi)
        with open(self.logisi,'a') as logifa:
            logifa.write(timisi+self.frasi+"\n")

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

    def chkpaf(self):
        if self.tageli == []:
            self.tageli.append(self.tagesi)
        for tage in self.tageli:
            comali = [ "mkdir", "-v", tage ]
            comasi = "\n chkpaf: " + " ".join(comali)

            self.frasi = comasi
            self.printimo()

            call(comali, stdout=open(self.logisi, 'a'))

        self.tagesi = ""
        self.tageli = []
        self.timosi = ""
        self.frasi = ""
        self.sepere = ""

    def chkfal(self):
        resut = False

        self.timosi = time.strftime("%Y%m%d%H%M%S")
        tageli = [ "head", "-v", self.tagesi ]
        call(tageli, stdout=open("temp/head-"+self.timosi, 'a'))

        comasi = "\n        chkfal: " + " ".join(tageli)
        self.frasi = comasi
        self.printimo()

        filafi = open("temp/head-"+self.timosi,"ab")
        filafi.write("-=#".encode("UTF-8"))
        filafi.close()
        if open("temp/head-"+self.timosi,"rb").read() != "-=#".encode("UTF-8"):
            resut = True

        tageli = [ "rm", "-v", "temp/head-"+self.timosi ]
        call(tageli, stdout=open("temp/head-"+self.timosi, 'a'))

        comasi = "        chkfal: " + " ".join(tageli)
        resusi = "\n        result: " + pprint.pformat(resut)
        self.frasi = comasi + resusi
        self.printe()

        self.timosi = ""
        self.frasi = ""
        self.sepere = ""

        return resut

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

        self.tagesi = ""
        self.tageli = []

        self.testing = False
        self.dicodi = {}
        self.Synom = dicto()
        self.argv()
        self.pesonai()

        self.redirek()

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
            if len(self.siarli[nanasi]) > 0:
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

    def sync(self):
        argutu = tuple(self.argudi.keys())
        sinodi = {}
        for argu in argutu:
            if len(argu) == 1 and self.Synom.siget(argu) != "":
                sinodi.update({ argu : self.Synom.siget(argu) })

        for argu in argutu:
            if argu in list(sinodi.keys()):
                metasi = sinodi.get(argu)
                metali = self.argudi.get(metasi,[])
                metali.extend(self.argudi.get(argu))
                self.argudi.update({ metasi : metali })

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

    def redirek(self):
        if self.argudi.get('argv',[]) == ['help']:
            print(self.helb)
        else:
            self.actor()

    def head(self):
        self.begisi = time.strftime("%Y%m%d%H%M%S")

        self.timosi = time.strftime("%Y%m%d%H%M%S")

        self.sepere = "- :"
        runninlog = ("==========\nRUN "+self.filasi+", begin at ["
            + self.timme() +"]\n==========" )

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
            configlog = ["\nFROM config.json"]

            self.lisli = []
            self.lisli = list(self.libadi.keys())
            metain = self.maxlen()
            for liba in self.lisli:
                if len(liba) < metain :
                    semein = metain-len(liba)
                else:
                    semein = 0

                configlog.append("    \"" + liba + "\""+ (" "*semein) +": "+
                    pprint.pformat(self.libadi.get(liba),compact=True,width=150))

        else:
            configlog = []

        self.sepere = "-_-"
        self.logisi = self.prelogi + self.timme() + '.log'

        metali = [runninlog]
        metali.extend(scriptlog)
        metali.extend(configlog)
        self.frasi = "\n".join(metali)+"\n"
        self.printe()

        self.timosi = ""
        self.frasi = ""
        self.sepere = ""

    def runit(self):
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

    def endin(self):
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
        runisi = ("==========\n"+self.filasi+", finished on ["
            + self.timme() +"]\n     Total time: "+resut+"\n==========" )

        self.frasi = runisi
        self.printe()

        self.frasi = ""
        self.timosi = ""
