# data/06-ba-blat/speciesEnsembl/T??Q**-testing-trimQ30.psl
pathStr = "data/06-ba-blat/speciesEnsembl/T??Q**-testing-trimQ30"

linesList = []
linesList = open("{}.psl".format(pathStr)).read().splitlines()
oldHeaderList = []
for n in [0,1,2,3,4]:
    oldHeaderList.append(linesList.pop(0))

newHeaderList = []
firstLineLst = oldHeaderList[2].split("\t")
secondLineLst = oldHeaderList[3].split("\t")

for n in range(21):
    if n < len(firstLineLst) and n < len(secondLineLst):
        headerStr = firstLineLst[n] + " " +secondLineLst[n]
    elif n < len(firstLineLst) and n >= len(secondLineLst):
        headerStr = firstLineLst[n]
    elif n >= len(firstLineLst) and n < len(secondLineLst):
        headerStr = secondLineLst[n]
    newHeaderList.append(headerStr)

for n in range(len(newHeaderList)):
    headerStr = newHeaderList[n]
    timesInt = 0
    while timesInt < 6:
        headerStr = headerStr.replace("  "," ")
        timesInt = timesInt + 1
    
    newHeaderList[n] = headerStr

resultList = []
resultList.append("\t".join(newHeaderList))
resultList.extend(linesList)

with open("{}.tsv".format(pathStr),'w') as target:
    target.write("\n".join(resultList))
