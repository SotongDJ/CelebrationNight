import pathlib, json
configDict = {
    "from" : "userData/07-cd-estimateExpression/speciesTreatment-gffRead/speciesDatabase-trimQ30/isoform_exp.diff",
    "toFolder" : "userData/08-an-annotateTranscriptome/speciesTreatment-gffRead/",
    "toFile" : "speciesDatabase-trimQ30-transcriptNamePair.json"
}

sourceStr = configDict["from"]
outputFolderStr = configDict["toFolder"]
outputFleStr = outputFolderStr+configDict["toFile"]
pathlib.Path( outputFolderStr ).mkdir(parents=True,exist_ok=True)
skipBool = False
resultDict = dict()
for lineStr in open(sourceStr).read().splitlines():
    if not skipBool:
        skipBool = True
    else:
        lineList = lineStr.split("\t")
        transcript = lineList[0]
        gene = lineList[1]
        resultDict[transcript] = gene

with open(outputFleStr,'w') as target:
    json.dump(resultDict,target,indent=2,sort_keys=True)