#!/usr/bin/env python3
import json, pprint

configsi = 'data/config.json'

configfi = open(configsi,'r')
configdi = json.load(configfi).get('var',{})

tribeli = configdi.get('tribe',[])
falisdi = configdi.get('file-list',{})
pafwasi = configdi.get('path',{}).get('fastqc',"")
pafcosi = configdi.get('path',{}).get('fastqc-comb',"")

resutsi = pafcosi + '/result.json'
resutdi = {}

for tribe in tribeli:
    falis = falisdi.get(tribe,"")
    for fal in open(falis).read().splitlines():
        tafasi = pafwasi + "/" + fal.replace('.fastq','_fastqc') + "/summary.txt"
        for lino in open(tafasi).read().splitlines():

            metali = []
            metali = lino.split("	")

            recosi = ""
            catesi = ""
            falesi = ""
            recosi,catesi,falesi = metali

            primadi = {}
            primadi = resutdi.get('cate',{})
            secondi = {}
            secondi = primadi.get(catesi,{})
            secondi.update({ falesi : recosi })
            primadi.update({ catesi : secondi })
            resutdi.update({ 'cate' : primadi })

            primadi = {}
            primadi = resutdi.get('fale',{})
            secondi = {}
            secondi = primadi.get(falesi,{})
            secondi.update({ catesi : recosi })
            primadi.update({ falesi : secondi })
            resutdi.update({ 'fale' : primadi })

# pprint.pprint(resutdi)
resutfa = open(resutsi,'w')
json.dump(resutdi,resutfa,indent=4,sort_keys=True)
resutfa.close()
