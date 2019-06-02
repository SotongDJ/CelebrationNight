import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pathlib
import libPrint

branshStr = "testing"
trimList = ["trimQ20","trimQ30"]
antStr = "speciesAnnotationA"
sampleList = ["Controlr1","T1r1","T2r1","T3r1","T4r1","T5r1"]
testingBool = True
saveFolderStr = "data/07-da-DitributionAnalysis/{branch}/"
savePathStr = "data/07-da-DitributionAnalysis/{branch}/{ant}-boxplot.png"
summaryPathStr = "data/07-da-DitributionAnalysis/{branch}/{ant}-{trim}.tsv"
expressionPathStr = "data/05-stringtie2/{branch}/{ant}-{trim}/{sample}-expression.tsv"
logFileNamehStr = "{ant}-{trim}-{sample}"

fig, axs = plt.subplots(1,10, sharex=True, sharey=True)
yInt = 0
pathlib.Path(saveFolderStr.format(branch=branshStr)).mkdir(parents=True,exist_ok=True)
for trimStr in trimList:
    summaryPath = summaryPathStr.format(branch=branshStr,ant=antStr,trim=trimStr)
    with open(summaryPath,'w') as summaryHandle:
        summaryColumnList = list()
        summaryColumnList.extend(["Sample","Total Count","Masked Count"])
        summaryColumnList.extend(["Max","Q3","Q2","Q1","Min"])
        summaryColumnList.extend(["log10(Max)","log10(Q3)","log10(Q2)","log10(Q1)","log10(Min)"])
        summaryHandle.write("\t".join(summaryColumnList)+"\n")

    for sampleStr in sampleList:
        summaryList = list()

        logFileName = logFileNamehStr.format(branch=branshStr,ant=antStr,trim=trimStr,sample=sampleStr)
        Print = libPrint.timer()
        Print.logFilenameStr = logFileName
        Print.folderStr = saveFolderStr.format(branch=branshStr)
        Print.testingBool = testingBool
        Print.startLog()

        Print.printing("Trim  : "+trimStr)
        Print.printing("Sample: "+sampleStr)
        summaryList.append(sampleStr)

        samplePath = expressionPathStr.format(branch=branshStr,ant=antStr,trim=trimStr,sample=sampleStr)
        sampleDF = pd.read_csv(samplePath,delimiter="\t",header=0)
        # sampleDF.columns.values
        # sampleDF.head(10)

        sampleAy = sampleDF['TPM'].values
        Print.printing("  Gene Count: "+str(sampleAy.size)+" #Total")
        summaryList.append(str(sampleAy.size))

        # sampleAy[:10]

        # noZeroAy = np.where(sampleAy < 10**-10 , 10**-10 , sampleAy)
        # ( noZeroAy <= 10**-10 ).sum()
        noZeroAy = np.ma.masked_equal(sampleAy,0)
        Print.printing("  Gene Count: "+str(noZeroAy.count())+" # Non-zero")
        summaryList.append(str(noZeroAy.count()))
        Print.printing("  Max  : "+str(noZeroAy.max()))
        summaryList.append(str(noZeroAy.max()))
        Print.printing("  Q3   : "+str(np.quantile(noZeroAy,0.75)))
        summaryList.append(str(np.quantile(noZeroAy,0.75)))
        Print.printing("  Q2   : "+str(np.quantile(noZeroAy,0.50)))
        summaryList.append(str(np.quantile(noZeroAy,0.50)))
        Print.printing("  Q1   : "+str(np.quantile(noZeroAy,0.25)))
        summaryList.append(str(np.quantile(noZeroAy,0.25)))
        Print.printing("  Min  : "+str(noZeroAy.min()))
        summaryList.append(str(noZeroAy.min()))

        l10ScaAy = np.log10(noZeroAy)
        Print.printing("  Max in log scale: "+str(l10ScaAy.max()))
        summaryList.append(str(l10ScaAy.max()))
        Print.printing("   Q3 in log scale: "+str(np.quantile(l10ScaAy,0.75)))
        summaryList.append(str(np.quantile(l10ScaAy,0.75)))
        Print.printing("   Q2 in log scale: "+str(np.quantile(l10ScaAy,0.50)))
        summaryList.append(str(np.quantile(l10ScaAy,0.50)))
        Print.printing("   Q1 in log scale: "+str(np.quantile(l10ScaAy,0.25)))
        summaryList.append(str(np.quantile(l10ScaAy,0.25)))
        Print.printing("  Min in log scale: "+str(l10ScaAy.min()))
        summaryList.append(str(l10ScaAy.min()))

        with open(summaryPath,'a') as summaryHandle:
            summaryHandle.write("\t".join(summaryList)+"\n")

        axs[yInt].set_title(sampleStr+"("+trimStr+")")
        axs[yInt].boxplot(l10ScaAy, showfliers=False, whis='range')
        Print.stopLog()
        yInt = yInt + 1

savePath = savePathStr.format(branch=branshStr,ant=antStr)
# plt.xticks([1],[sampleStr+"("+trimStr+")"])
plt.ylim((-5,5))
# plt.savefig(savePath, bbox_inches='tight')
plt.show()
plt.close()
# Print.printing("  BoxPlot drawed and saved in "+savePath)
# Print.printing("\n")
