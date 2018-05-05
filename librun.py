import pprint, time
from subprocess import call

def datuse(numein=0):
    if len(str(numein)) < 2:
        return '0'+str(numein)
    else:
        return str(numein)

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

def calti(begi='0', endi='360', modde=1):
    numein = int(endi) - int(begi)
    numesi = str(numein)
    return numesi

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
                scriptlog = (scriptlog + loca + ' '*(metain-len(loca)) + ": " +
                    pprint.pformat(locadi.get(loca)) + "\n")

    else:
        scriptlog = ""

    if libadi != {}:
        configlog = "FROM config.json\n"

        metali = list(libadi.keys())
        metain = maxlen(metali)
        for liba in metali:
            if len(loca) < metain :
                configlog = (configlog + "\"" + liba + "\"" +
                    ' '*(metain-len(liba)) + ": " +
                    pprint.pformat(libadi.get(liba)) + "\n")

    else:
        configlog = ""

    if prelogi == "":
        logisi = 'temp/temp-' + timme(timasi=timani,sepere="-_-") + '.log'
    else:
        logisi = prelogi + timme(timasi=timani,sepere="-_-") + '.log'

    print(runninlog + scriptlog + "\n" + configlog)
    with open(logisi,"w") as logifa:
        logifa.write(runninlog + scriptlog + "\n" + configlog)

    return timani,logisi

def ranni(comali=[], logini='', modde='a'):
    comman = []
    logisi = ''
    timani = ''
    modden = ''

    if comali == []:
        comman = ['echo','wahaha']

    if logini == '':
        timani = time.strftime("%Y%m%d%H%M%S")
        timme(modde=2)
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
        logifa.write(runisi + comasi)

    call(comman, stdout=open(logisi, 'a'))
