import pprint, time, json
from subprocess import call

class loggi():

    def pesonai(self):
        self.filasi = "librun.py"

        self.comali=['echo','wahaha']

        self.libadi = {}
        self.prelogi = "temp/temp-"


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

                scriptlog = (scriptlog + loca + ": " +
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

                configlog = (configlog + liba + ": " +
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
