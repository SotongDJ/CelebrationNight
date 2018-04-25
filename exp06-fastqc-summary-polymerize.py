import json, pprint

configsi = 'data/config.json'

configfi = open(configsi,'r')
configdi = json.load(configfi).get('var',{})

pafwasi = configdi.get('path',{}).get('fastqc-comb',"")
tribeli = configdi.get('tribe',[])
prefisdi = configdi.get('prefix',{})
grupoli = configdi.get('group',[])

inputsi = pafwasi + '/result.json'
inputfa = open(inputsi,'r')
inputli = json.load(inputfa)

faledi = inputli.get('fale',{})

resutdi = {}
resutsi = pafwasi + '/result.html'
resutfa = open(resutsi,'w')

for grupo in grupoli:
    primadi = {}
    secondi = {}
    for fale in list(faledi.keys()):
        if grupo in fale:

            primadi = resutdi.get(grupo,{})

            for tribe in tribeli:
                prefisi = ""
                prefisi = prefisdi.get(tribe,"")

                if prefisi != "":
                    if prefisi in fale:
                        metali = []
                        metali = secondi.get(tribe,[])
                        metali.append(fale)
                        secondi.update({ tribe : metali })
                else:
                    metali = []
                    metali = secondi.get("",[])
                    metali.append(fale)
                    secondi.update({ "" : metali })
