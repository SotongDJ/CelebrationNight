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

resutdi={
    group:{
        tribe:[
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
