#!/usr/bin/env python3
import pathlib, json

sampleList = [
    {
        'times' : 2,
        0 : "data/06-ba-blat/speciesaEnsembl/T??Q**-testing-trimQ30-nameList-gene.json",
        1 : "data/dbga-GenomeAnnotation/speciesaEnsembl/speciesaEnsembl-homolog.json",
        'database' : {
            "GO" : "data/dbgo-GOdatabase/tair-{type}.json",
            "KEGG" : "data/dbkg-KEGG-hirTree/ath00001-{type}.json",
            "TF" : "data/dbtf-TFdb/at-tf-{type}.json",
        },
        'output folder' : "data/09-an-annotation/speciesaEnsembl/",
        'output file' : "T??Q**-testing-trimQ30-{database}-{type}.json",
    },
]

for sampleDict in sampleList:
    # sampleDict = sampleList[0]
    timesInt = sampleDict['times']
    databaseDict = sampleDict['database']
    outputFolderStr = sampleDict['output folder']
    outputFileStr = sampleDict['output file']
    id2HmDict = dict()
    hm2IdDict = dict()
    for targetInt in range(timesInt):
        inputStr = sampleDict[targetInt]
        inputDict = json.load(open(inputStr,'r'))
        if targetInt == 0:
            for idStr in list(inputDict.keys()):
                if type(inputDict[idStr]) == type(str()):
                    id2HmDict.update({ idStr : [inputDict[idStr]] })
                elif type(inputDict[idStr]) == type(list()):
                    id2HmDict.update({ idStr : inputDict[idStr] })
            print(targetInt)
        else:
            inputKeyList = list(inputDict.keys())
            hm2IdKeyList = list(hm2IdDict.keys())
            #
            initCountInt = 1
            totalCountInt = len(inputKeyList)
            #
            hmDict = dict()
            for hmStr in inputKeyList:
                #
                print("[{}/{}]".format(initCountInt,totalCountInt), end="\r")
                #
                if hmStr in hm2IdKeyList:
                    if type(inputDict[hmStr]) == type(str()):
                        for idStr in hm2IdDict[hmStr]:
                            tempSet = set(hmDict.get(idStr,list()))
                            tempSet.update({inputDict[hmStr]})
                            hmDict.update({ idStr : list(tempSet) })
                    elif type(inputDict[hmStr]) == type(list()):
                        for targetStr in inputDict[hmStr]:
                            for idStr in hm2IdDict[hmStr]:
                                tempSet = set(hmDict.get(idStr,list()))
                                tempSet.update({targetStr})
                                hmDict.update({ idStr : list(tempSet) })
                #
                initCountInt = initCountInt + 1
                #
            id2HmDict = dict()
            id2HmDict.update(hmDict)

            print("")

        hm2IdDict = dict()
        #
        initCountInt = 1
        totalCountInt = len(list(id2HmDict.keys()))
        #
        for idStr in list(id2HmDict.keys()):
            #
            print("[{}/{}]".format(initCountInt,totalCountInt), end="\r")
            #
            for hmStr in id2HmDict[idStr]:
                tempSet = set(hm2IdDict.get(hmStr,list()))
                tempSet.update({idStr})
                hm2IdDict.update({ hmStr : list(tempSet) })
            #
            initCountInt = initCountInt + 1
            #
        print("")
    # The following codes fuse with some older but still unpublish codes
    #     that related to gene2term/term2gene/count generation.
    for databaseStr in list(databaseDict.keys()):
        targetPathStr = databaseDict[databaseStr]
        pathlib.Path( outputFolderStr ).mkdir(parents=True,exist_ok=True)
        initDict = json.load(open(targetPathStr.format(type="gene2term"),'r'))
        gene2TermDict = dict()
        term2GeneDict = dict()
        countDict = dict()
        #
        initCountInt = 1
        totalCountInt = len(list(id2HmDict.keys()))
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
        
        for gene in list(gene2TermDict.keys()):
            gene2TermList = gene2TermDict.get(gene,[])
            if len(gene2TermList) > 0 :
                for go in gene2TermList:
                    tempList = term2GeneDict.get(go,[])
                    tempList.append(gene)
                    term2GeneDict.update({ go : tempList})

        countList = []
        sumList = []
        for go in term2GeneDict.keys():
            countList.append( go+"\t"+str(len(term2GeneDict[go])))
            countDict.update({ go : len(term2GeneDict[go]) })

            sumList.extend(term2GeneDict[go])
            sumList = list(set(sumList))

        countDict.update({ "#SUM" : len(sumList) })

        with open(outputFolderStr+outputFileStr.format(database=databaseStr,type="count"),'w') as dictFile:
            json.dump(countDict, dictFile, indent=4, sort_keys=True)

        with open(outputFolderStr+outputFileStr.format(database=databaseStr,type="term2gene"),'w') as dictFile:
            json.dump(term2GeneDict, dictFile, indent=4, sort_keys=True)

        with open(outputFolderStr+outputFileStr.format(database=databaseStr,type="gene2term"),'w') as dictFile:
            json.dump(gene2TermDict, dictFile, indent=4, sort_keys=True)

