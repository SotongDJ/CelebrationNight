import pathlib, json
import pandas, numpy, math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

# testFile is the file that create by 09-ft
# Please replace [testFile] and limitation (fisherBelow and countAbove) before running
sampleList = [
    {
        "testFilename" : "data/09-ft-FisherExactTest/GO-[testFile]{}.{}",
        "checkType" : "biologicalOnly",
        "fisherBelow" : -5.5,
        "countAbove" : 30,
        "title" : "GO Term",
        "type" : "GO",
        "dividend" : "[UP in ratio-D_vs_con]",
        "divisor" : "[UP in ratio-H_vs_N]",
    },
    {
        "testFilename" : "data/09-ft-FisherExactTest/KEGG-[testFile]{}.{}",
        "checkType" : "keggLowLevel",
        "fisherBelow" : -2.3,
        "countAbove" : 10,
        "title" : "KEGG",
        "type" : "KEGG",
        "dividend" : "[UP in ratio-D_vs_con]",
        "divisor" : "[UP in ratio-H_vs_N]",
    },
    {
        "testFilename" : "data/09-ft-FisherExactTest/TF-[testFile]{}.{}",
        "checkType" : "pass",
        "fisherBelow" : -2.3,
        "countAbove" : 5,
        "title" : "Transcription Factor",
        "type" : "TF",
        "dividend" : "[UP in ratio-D_vs_con]",
        "divisor" : "[UP in ratio-H_vs_N]",
    }
]

def idCheck(contentDict,conditionStr):
    result = False
    bioBool = "0008150" in contentDict.get('GO Path','')
    kHighBool = "__" in contentDict.get('KEGG Path','')
    gHighBool = "__" in contentDict.get('GO Path','')
    kLowBool = "__" not in contentDict.get('KEGG Path','')
    gLowBool = "__" not in contentDict.get('GO Path','')
    if conditionStr == "biologicalOnly":
        result = bioBool
    elif conditionStr == "biologicalLow":
        result = bioBool and gLowBool
    elif conditionStr == "biologicalHigh":
        result = bioBool and gHighBool
    elif conditionStr == "keggLowLevel":
        result = kLowBool
    elif conditionStr == "keggHighLevel":
        result = kHighBool
    elif conditionStr == "pass":
        result = True
    return result

for sampleDict in sampleList:
    testFilenameStr = sampleDict["testFilename"].format("","json")
    testDict = json.load(open(testFilenameStr,"r"))
    checkTypeStr = sampleDict["checkType"]
    fisherBelowFlt = sampleDict["fisherBelow"]
    countAboveInt = sampleDict["countAbove"]
    titleStr = sampleDict["title"]
    typeStr = sampleDict["type"]
    dividendStr = sampleDict["dividend"]
    divisorStr = sampleDict["divisor"]

    idTup = tuple([ n for n in testDict.keys() if testDict[n]["dividendCountInt"] != 0 and idCheck(testDict[n],checkTypeStr) ])
    x = [ testDict[n]["dividendCountInt"] for n in idTup ]
    y = [ testDict[n]["Fisher's Exact Test (in log10)"] for n in idTup ]
    area = [ (3.14*200*(testDict[n]["dividendCountInt"]/testDict[n]["dividendSumInt"]))**2 for n in idTup ]
    colors = [ testDict[n]["dividendCountInt"]/testDict[n]["dividendSumInt"] for n in idTup]

    figure(num=None, figsize=(10, 8), dpi=300, facecolor='w', edgecolor='k')
    plt.scatter(x, y, s=area, c=colors, alpha=0.5)

    for i,idStr in enumerate(idTup):
        if testDict[idStr]["Fisher's Exact Test (in log10)"] < fisherBelowFlt or testDict[idStr]["dividendCountInt"] > countAboveInt:
            xNum = x[i]
            yNum = y[i]
            # height = 4*(testDict[idStr]["dividendCountInt"]/testDict[idStr]["dividendSumInt"])
            plt.text(xNum, yNum, "{} ({}/{})".format(idStr,testDict[idStr]["dividendCountInt"],testDict[idStr]["dividendSumInt"]), fontsize=10)

    plt.colorbar(label='Rich Factor')
    plt.xlabel('Genes count')
    plt.ylabel("Fisher's Exact Test (in log$_{10}$ scale)")
    # plt.title('{} Enrichment Analysis'.format(titleStr))

    savePathStr = sampleDict["testFilename"].format("-scatter","svg")
    plt.savefig(savePathStr)
    plt.clf()

    figure(num=None, figsize=(12, 24), dpi=300, facecolor='w', edgecolor='k')
    fig, (ax1, ax2) = plt.subplots(2, sharex=True)
    
    if typeStr == "GO":
        fig.subplots_adjust(left=0.3)
    else:
        fig.subplots_adjust(left=0.2)
    
    labelTup = tuple([ "{} ({})".format(n,testDict[n]["dividendCountInt"]) for n in idTup ])
    nomiBarDF = pandas.DataFrame(index=labelTup, columns=["Count"])
    for idStr in idTup:
        labelStr = "{} ({})".format(idStr,testDict[idStr]["dividendCountInt"])
        nomiBarDF.at[labelStr, "Count"] = testDict[idStr]["dividendCountInt"]
    nomiBarSplitDF = nomiBarDF.sort_values(by="Count").tail(15)
    nomiBarPlt = nomiBarSplitDF.plot(kind='barh', figsize=(9, 8), color='#e26732', zorder=2, width=0.85, legend=False, ax=ax1)
    nomiBarPlt.title.set_text(dividendStr)
    # Despine
    nomiBarPlt.spines['right'].set_visible(False)
    nomiBarPlt.spines['top'].set_visible(False)
    nomiBarPlt.spines['left'].set_visible(False)
    nomiBarPlt.spines['bottom'].set_visible(False)
    # Switch off ticks
    nomiBarPlt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")
    # Draw vertical axis lines
    vals = nomiBarPlt.get_xticks()
    for tick in vals:
        nomiBarPlt.axvline(x=tick, linestyle='dashed', alpha=1, color='#eeeeee', zorder=1)
    # Set x-axis label
    nomiBarPlt.set_xlabel("Genes count", labelpad=20, weight='bold', size=12)
    # Set y-axis label
    nomiBarPlt.set_ylabel("{}".format(titleStr), labelpad=20, weight='bold', size=12)

    domiIDTup = tuple([ n for n in testDict.keys() if testDict[n]["divisorCountInt"] != 0 and idCheck(testDict[n],checkTypeStr) ])
    labelTup = tuple([ "{} ({})".format(n,testDict[n]["divisorCountInt"]) for n in idTup ])
    domiBarDF = pandas.DataFrame(index=labelTup, columns=["Count"])
    for idStr in idTup:
        labelStr = "{} ({})".format(idStr,testDict[idStr]["divisorCountInt"])
        domiBarDF.at[labelStr, "Count"] = testDict[idStr]["divisorCountInt"]
    domiBarSplitDF = domiBarDF.sort_values(by="Count").tail(15)
    domiBarPlt = domiBarSplitDF.plot(kind='barh', figsize=(9, 8), color='#e26732', zorder=2, width=0.85, legend=False, ax=ax2)
    domiBarPlt.title.set_text(divisorStr)
    # Despine
    domiBarPlt.spines['right'].set_visible(False)
    domiBarPlt.spines['top'].set_visible(False)
    domiBarPlt.spines['left'].set_visible(False)
    domiBarPlt.spines['bottom'].set_visible(False)
    # Switch off ticks
    domiBarPlt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")
    # Draw vertical axis lines
    vals = domiBarPlt.get_xticks()
    for tick in vals:
        domiBarPlt.axvline(x=tick, linestyle='dashed', alpha=1, color='#eeeeee', zorder=1)
    # Set x-axis label
    domiBarPlt.set_xlabel("Genes count", labelpad=20, weight='bold', size=12)
    # Set y-axis label
    domiBarPlt.set_ylabel("{}".format(titleStr), labelpad=20, weight='bold', size=12)

    savePathStr = sampleDict["testFilename"].format("-barh","svg")
    plt.savefig(savePathStr)
    plt.clf()