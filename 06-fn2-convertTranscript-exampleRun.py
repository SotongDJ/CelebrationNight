#!/usr/bin/env python3
import pathlib
sampleList = [
    {
        "from"     : "userData/06-gr-exportTranscript/speciesTreatment/speciesDatabase-trimQ30-transcript.fn",
        "toFolder" : "userData/06-gr-exportTranscript/speciesTreatment/",
        "toFile"   : "speciesDatabase-trimQ30-transcript.tsv",
    }
]

sampleDict = sampleList[0]
fromStr = sampleDict["from"]
toFolderStr = sampleDict["toFolder"]
toFileStr = sampleDict["toFile"]

pairDict =dict()
keyStr = str()
valueList = list()
for lineStr in open(fromStr).read().splitlines():
    if lineStr[0] == ">" and valueList == list():
        keyStr = lineStr[1:]
    elif lineStr[0] == ">" and valueList != list():
        pairDict[keyStr] = valueList
        keyStr = lineStr[1:]
        valueList = list() 
    else:
        valueList.append(lineStr)

pairDict = { x : "".join(y) for x,y in pairDict.items() }

pathlib.Path( toFolderStr ).mkdir(parents=True,exist_ok=True)
with open( toFolderStr+toFileStr, 'w') as targetHandle:
    targetHandle.write("transcript\tsequence\n")
    for keyStr,valueStr in pairDict.items():
        targetStr=keyStr.split(" ")[0]
        targetHandle.write("{}\t{}\n".format(targetStr,valueStr))