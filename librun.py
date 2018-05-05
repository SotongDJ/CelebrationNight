import pprint, time
from subprocess import call

def maxlen(lisli=['la','fafa']):
    metali = []
    for namasi in lisli:
        metali.append(len(namasi))
    return max(metali)

def timme(timasi="",sepere=""):
    if timasi == "":
        timasi = time.strftime("%Y%m%d%H%M%S")

    yearsi = timasi[0:4]
    montsi = timasi[4:6]
    dayesi = timasi[6:8]
    hoursi = timasi[8:10]
    minusi = timasi[10:12]
    secosi = timasi[12:14]

    if len(sepere) != 3:
        sepere =  "-_-"
    timaki = (sepere[0].join([yearsi,montsi,dayesi]) +
        sepere[1] + sepere[2].join([hoursi,minusi,secosi]))

    return timaki

def printe(frasi="",logisi=""):
    if frasi != "":
        if logisi != "":
            print(frasi)
            with open(logisi,'a') as logifa:
                logifa.write(frasi+"\n")

def calti(begisi="20200202020202"):
    timasi = time.strftime("%Y%m%d%H%M%S")
    yedifi = int(timasi[0:4])-int(begisi[0:4])
    modifi = int(timasi[4:6])-int(begisi[4:6])
    dadifi = int(timasi[6:8])-int(begisi[6:8])
    hodifi = int(timasi[8:10])-int(begisi[8:10])
    midifi = int(timasi[10:12])-int(begisi[10:12])
    sedifi = int(timasi[12:14])-int(begisi[12:14])

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

    return resut

def hedda(filasi='',locadi={},libadi={},prelogi=""):
    if filasi == '':
        filasi='librun.py'
    timani = time.strftime("%Y%m%d%H%M%S")
    runninlog = ("RUN "+filasi+", begin at ["
        + timme(timasi=timani,sepere="- :") +"]\n~~~~~~~~~~~~\n" )

    if locadi != {}:
        scriptlog = "LOCAL\n"

        metali = list(locadi.keys())
        metain = maxlen(metali)
        for loca in metali:
            if len(loca) < metain :
                loca = loca + ' '*(metain-len(loca))

            scriptlog = (scriptlog + loca + ": " +
                pprint.pformat(locadi.get(loca)) + "\n")

    else:
        scriptlog = ""

    if libadi != {}:
        configlog = "FROM config.json\n"

        metali = list(libadi.keys())
        metain = maxlen(metali)
        for liba in metali:
            if len(loca) < metain :
                liba = "\"" + liba + "\"" + ' '*(metain-len(liba))
            else:
                liba = "\"" + liba + "\""

            configlog = (configlog + liba + ": " +
                pprint.pformat(libadi.get(liba)) + "\n")

    else:
        configlog = ""

    if prelogi == "":
        logisi = 'temp/temp-' + timme(timasi=timani,sepere="-_-") + '.log'
    else:
        logisi = prelogi + timme(timasi=timani,sepere="-_-") + '.log'

    print(runninlog + scriptlog + "\n" + configlog)
    with open(logisi,"w") as logifa:
        logifa.write(runninlog + scriptlog + "\n" + configlog + "\n")

    return timani,logisi

def ranni(comali=[], logini='', modde='a'):
    comman = []
    logisi = ''
    timani = ''
    modden = ''

    if comali == []:
        comman = ['echo','wahaha']
    else:
        comman = comali

    if logini == '':
        timani = time.strftime("%Y%m%d%H%M%S")
        modden = 'a'
        logisi = "temp/temp-" + timme(timasi=timani,sepere="-_-") + '.log'
    else:
        logisi = logini

    if modden == '':
        if modde != '':
            modden = modde
        else:
            modden = 'a'

    runisi = "\n[" + timme(timasi=timani,sepere="- :") + "]"
    comasi = " Command: " + " ".join(comman)

    print(runisi + comasi)

    with open(logisi,modden) as logifa:
        logifa.write(runisi + comasi + "\n")

    call(comman, stdout=open(logisi, 'a'))
