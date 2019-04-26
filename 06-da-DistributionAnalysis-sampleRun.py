import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pathlib

for trimStr in ["trimQ20","trimQ30"]:
   for sampleStr in ["Controlr1","T1r1","T2r1","T3r1","T4r1","T5r1"]:
         antStr = "speciesTestingA"
         pathStr = "data/05-stringtie2/testing/{ant}-{trim}/{sample}-expression.tsv"
         samplePath = pathStr.format(ant=antStr,trim=trimStr,sample=sampleStr)
         sampleDF = pd.read_csv(samplePath,delimiter="\t",header=0)
         # sampleDF.columns.values
         # sampleDF.head(10)

         sampleAy = sampleDF['TPM'].values
         # sampleAy[:10]

         # noZeroAy = np.where(sampleAy < 10**-10 , 10**-10 , sampleAy)
         # ( noZeroAy <= 10**-10 ).sum()
         noZeroAy = np.ma.masked_equal(sampleAy,0)
         l10ScaAy = np.log10(noZeroAy)
         # lnScalAy = np.log(noZeroAy)
         # l2ScalAy = np.log2(noZeroAy)

         fig1, ax1 = plt.subplots()
         ax1.set_title(sampleStr+"("+trimStr+")")
         # ax1.boxplot(l10ScaAy, showfliers=False)
         ax1.boxplot(l10ScaAy, showfliers=False, whis='range')
         # ax1.boxplot(sampleAy)
         # plt.xticks(xNumList,xNameList)
         pathlib.Path("data/05-stringtie2/testing/BoxPlot/").mkdir(parents=True,exist_ok=True)
         savePathStr = "data/05-stringtie2/testing/BoxPlot/{ant}-{trim}-{sample}-boxplot.png"
         savePath = savePathStr.format(ant=antStr,trim=trimStr,sample=sampleStr)
         plt.ylim((-5,5))
         plt.savefig(savePath, bbox_inches='tight')
         # plt.show()
         plt.close()