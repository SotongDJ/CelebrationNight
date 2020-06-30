#!/usr/bin/env python3
import pathlib, json

sampleList = [
    {
        'times' : 2,
        0 : "userData/08-an-annotateTranscriptome/speciesTreatment-gffRead/speciesDatabase-trimQ30-transcriptNamePair.json",
        1 : "userData/dbga-GenomeAnnotation/speciesDatabase/speciesDatabase-homolog.json",
        'database' : {
            "GO" : "userData/dbgo-GOdatabase/prefix-{type}.json",
            "KO" : "userData/dbkg-KEGG-hirTree/prefix1-{type}.json",
            "EC" : "userData/dbkg-KEGG-hirTree/prefix2-{type}.json",
            "TF" : "userData/dbtf-TFdb/prefix-{type}.json",
            "SR" : "userData/dbsr-stressRegulation/prefix-{type}.json"
        },
        'attribute' : {
            'description' : 'userData/dbga-GenomeAnnotation/speciesDatabase/speciesDatabase-attributes.json',
            'homolog' : 'userData/dbga-GenomeAnnotation/speciesDatabase/speciesDatabase-homolog.json',
        },
        'output folder' : "userData/08-an-annotateTranscriptome/speciesTreatment-gffRead/",
        'output file' : "speciesDatabase-transcript-{database}-{type}.json",
    },
]

for sampleDict in sampleList:
    # sampleDict = sampleList[0]
    timesInt = sampleDict['times']
    databaseDict = sampleDict['database']
    attributeDict = sampleDict['attribute']
    outputFolderStr = sampleDict['output folder']
    outputFileStr = sampleDict['output file']
    id2HmDict = dict()
    hm2IdDict = dict()
    for targetInt in range(timesInt):
        inputStr = sampleDict[targetInt]
        inputDict = json.load(open(inputStr,'r'))
        print(targetInt)
        if targetInt == 0:
            for idStr in list(inputDict.keys()):
                if type(inputDict[idStr]) == type(str()):
                    hmSet = set([inputDict[idStr]])
                    id2HmDict.update({ idStr : hmSet })

                elif type(inputDict[idStr]) == type(list()):
                    hmSet = set(inputDict[idStr])
                    id2HmDict.update({ idStr : hmSet })
                    
                for hmStr in hmSet:
                    tempSet = hm2IdDict.get(hmStr,set())
                    tempSet.update(set([idStr]))
                    hm2IdDict[hmStr] = tempSet
        else:
            inputKeySet = set(inputDict.keys())
            hm2IdKeySet = set(hm2IdDict.keys())
            #
            initCountInt = 1
            totalCountInt = len(inputKeySet)
            #
            for inputIdStr in inputKeySet:
                #
                print("[{}/{}]".format(initCountInt,totalCountInt), end="\r")
                #
                if inputIdStr in hm2IdKeySet:
                    for idStr in hm2IdDict[inputIdStr]:
                        tempSet = id2HmDict.get(idStr,set())
                        inputEle = inputDict[inputIdStr]
                        if type(inputEle) == type(str()):
                            tempSet.update(set([inputEle]))
                        elif type(inputEle) == type(list()):
                            tempSet.update(set(inputEle))
                        id2HmDict.update({ idStr : tempSet })
                #
                initCountInt = initCountInt + 1
                #
            print("")

            #
            initCountInt = 1
            totalCountInt = len(list(id2HmDict.keys()))
            #
            for idStr in list(id2HmDict.keys()):
                #
                print("[{}/{}]".format(initCountInt,totalCountInt), end="\r")
                #
                for hmStr in id2HmDict[idStr]:
                    tempSet = hm2IdDict.get(hmStr,set())
                    tempSet.update({idStr})
                    hm2IdDict.update({ hmStr : tempSet })
                #
                initCountInt = initCountInt + 1
                #
            print("")
        
    id2HmDict = { x : list(y) for x,y in id2HmDict.items() }
    with open(outputFolderStr+outputFileStr.format(database="mapping",type="id2homolog"),'w') as dictFile:
        json.dump(id2HmDict, dictFile, indent=4, sort_keys=True)
    
    hm2IdDict = { x : list(y) for x,y in hm2IdDict.items() }
    with open(outputFolderStr+outputFileStr.format(database="mapping",type="homolog2id"),'w') as dictFile:
        json.dump(hm2IdDict, dictFile, indent=4, sort_keys=True)

    # The following codes fuse with some older but still unpublish codes
    #     that related to gene2term/term2gene/count generation.
    for databaseStr in list(databaseDict.keys()):
        print(databaseStr)
        targetPathStr = databaseDict[databaseStr]
        pathlib.Path( outputFolderStr ).mkdir(parents=True,exist_ok=True)
        initDict = json.load(open(targetPathStr.format(type="gene2term"),'r'))
        gene2TermDict = dict()
        term2GeneDict = dict()
        countDict = dict()
        #
        initCountInt = 1
        totalCountInt = len(list(hm2IdDict.keys()))
        #
        for hmStr in list(hm2IdDict.keys()):
            #
            print("[{}/{}]".format(initCountInt,totalCountInt), end="\r")
            #
            if hmStr in initDict:
                for targetStr in initDict[hmStr]:
                    for idStr in hm2IdDict[hmStr]:
                        tempSet = set(gene2TermDict.get(idStr,list()))
                        tempSet.update({targetStr})
                        gene2TermDict.update({ idStr : list(tempSet) })
            #
            initCountInt = initCountInt + 1
            #
        print("")

        print(databaseStr,"term2gene")
        for gene in list(gene2TermDict.keys()):
            gene2TermList = gene2TermDict.get(gene,[])
            if len(gene2TermList) > 0 :
                for go in gene2TermList:
                    tempList = term2GeneDict.get(go,[])
                    tempList.append(gene)
                    term2GeneDict.update({ go : tempList})

        print(databaseStr,"count")
        countList = []
        sumSet = set()
        #
        initCountInt = 1
        totalCountInt = len(list(term2GeneDict.keys()))
        #
        for term in term2GeneDict.keys():
            print("[{}/{}]".format(initCountInt,totalCountInt), end="\r")
            #
            countList.append( term+"\t"+str(len(term2GeneDict[term])))
            countDict.update({ term : len(term2GeneDict[term]) })

            sumSet.update(set(term2GeneDict[term]))
            #
            initCountInt = initCountInt + 1
            #

        print("")
        countDict.update({ "#SUM" : len(sumSet) })

        with open(outputFolderStr+outputFileStr.format(database=databaseStr,type="count"),'w') as dictFile:
            json.dump(countDict, dictFile, indent=4, sort_keys=True)

        with open(outputFolderStr+outputFileStr.format(database=databaseStr,type="term2gene"),'w') as dictFile:
            json.dump(term2GeneDict, dictFile, indent=4, sort_keys=True)

        with open(outputFolderStr+outputFileStr.format(database=databaseStr,type="gene2term"),'w') as dictFile:
            json.dump(gene2TermDict, dictFile, indent=4, sort_keys=True)
    
    for attributeStr, targetPathStr in attributeDict.items():
        print(attributeStr)
        pathlib.Path( outputFolderStr ).mkdir(parents=True,exist_ok=True)
        initDict = json.load(open(targetPathStr,'r'))
        alterDict = dict()
        #
        initCountInt = 1
        totalCountInt = len(list(hm2IdDict.keys()))
        #
        for hmStr in list(hm2IdDict.keys()):
            #
            print("[{}/{}]".format(initCountInt,totalCountInt), end="\r")
            #
            if hmStr in initDict.keys():
                for idStr in hm2IdDict[hmStr]:
                    alterEle = initDict[hmStr]
                    idSet = alterDict.get(idStr,set())
                    if type(alterEle) == type(list()):
                        idSet.update(set(alterEle))
                    if type(alterEle) == type(str()):
                        alterList = list()
                        alterList.append(alterEle)
                        idSet.update(set(alterList))
                    alterDict.update({ idStr : idSet })
            #
            initCountInt = initCountInt + 1
            #
        print("")
        alterDict = { x: "; ".join(y) for x,y in alterDict.items() }
        with open(outputFolderStr+outputFileStr.format(database="attribute",type=attributeStr),'w') as dictFile:
            json.dump(alterDict, dictFile, indent=4, sort_keys=True)