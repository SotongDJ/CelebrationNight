import json, pprint

configsi = 'data/config.json'

configfi = open(configsi,'r')

configdi = json.load(configfi).get('var',{})
pafwasi = configdi.get('path',{}).get('fastqc-comb',"")
grupoli = configdi.get('group',[])
tribeli = configdi.get('tribe',[])
prefisdi = configdi.get('prefix',{})
blanksi = configdi.get('blank-prefix',{})

faslidi = json.load(configfi).get('fastqc-list',{})
rowlidi = faslidi.get("row",{})
colspan = faslidi.get("colspan",{})

inputsi = pafwasi + '/result.json'
inputfa = open(inputsi,'r')
inputli = json.load(inputfa)

faledi = inputli.get('fale',{})

resutdi = {}
resutsi = pafwasi + '/result.html'
resutfa = open(resutsi,'w')

"""
resutdi={
group:{ # primadi
tribe:[ # seconli / blankli
fale,
fale
]
},
group:{
tribe:[
fale,
fale
]
}
}
"""

for grupo in grupoli:
    primadi = {}
    primadi = resutdi.get(grupo,{})

    for tribe in tribeli:
        seconli = {}
        seconli = primadi.get(tribe,[])

        blankli = {}
        blankli = primadi.get(blanksi,[])

        for fale in faledi:
            if grupo in fale:

                prefis = prefisdi.get(tribe,"")
                if prefis != "":
                    if prefis in fale:
                        seconli.append(fale)
                    else:
                        blankli.append(fale)

        primadi.update({ tribe : seconli })
        primadi.update({ blanksi : blankli })

    resutdi.update({ grupo : primadi })

# pprint.pprint(resutdi)

resutfa.close()
