import pathlib
import sqlite3
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

branchStr = "testing"
antStr = "speciesTestingA"
controlStr = "Controlr1"
sampleList = ["Controlr1","T1r1","T2r1","T3r1","T4r1","T5r1"]
trim20PathStr = 'data/07-sl-expressionTable-SQLite3/{branch}/Expression-{ant}-trimQ20.db'
trim30PathStr = 'data/07-sl-expressionTable-SQLite3/{branch}/Expression-{ant}-trimQ30.db'

trim20Path = trim20PathStr.format(branch=branchStr,ant=antStr)
Connect = sqlite3.connect(trim20Path)
print("[SQLite3]\n    "+trim20Path)
Cursor = Connect.cursor()

q20Dict = dict()
for sampleStr in sampleList:
    sampleExc = Cursor.execute("SELECT UUID, TPM  from {}_Expression".format(sampleStr))
    for rowList in sampleExc:
        uuid, tpm = rowList
        subDict = q20Dict.get(uuid,dict())
        subDict.update({ sampleStr : tpm })
        q20Dict.update({ uuid : subDict })

Connect.close()

trim30Path = trim30PathStr.format(branch=branchStr,ant=antStr)
Connect = sqlite3.connect(trim30Path)
print("[SQLite3]\n    "+trim30Path)
Cursor = Connect.cursor()

q30Dict = dict()
for sampleStr in sampleList:
    sampleExc = Cursor.execute("SELECT UUID, TPM  from {}_Expression".format(sampleStr))
    for rowList in sampleExc:
        uuid, tpm = rowList
        subDict = q30Dict.get(uuid,dict())
        subDict.update({ sampleStr : tpm })
        q30Dict.update({ uuid : subDict })

Connect.close()

columnList = list()
arrayList = list()
for sampleStr in sampleList:
    columnList.append("Difference_{}".format(sampleStr))
    arrayList.append(list())

diffrDict = dict()
for uuid in q20Dict.keys():
    for sampleInt in range(len(sampleList)):
        q20Flt = q20Dict[uuid][sampleList[sampleInt]]
        q30Flt = q30Dict[uuid][sampleList[sampleInt]]
        difFlt = abs(q30Flt-q20Flt)
        if (q30Flt-q20Flt) > 0:
            dirStr = "increase"
        elif (q30Flt-q20Flt) < 0:
            dirStr = "decrease"
        else:
            dirStr = "remain"
        
        subDict = diffrDict.get(uuid,dict())
        subDict.update({ "Difference_"+sampleList[sampleInt] : difFlt })
        if difFlt != 0.0:
            arrayList[sampleInt].append(difFlt)
        subDict.update({ "Direction_"+sampleList[sampleInt] : dirStr })
        diffrDict.update({ uuid : subDict })

# difAy = np.array(arrayList)
# data = np.array(arrayList[0])
# Choose how many bins you want here
num_bins = 10
fig, axs = plt.subplots(1, 5, sharey=True, sharex=True, tight_layout=True)

for sampleInt in range(len(sampleList)):
    # data = np.array(arrayList[sampleInt])
    data = np.log10(np.array(arrayList[sampleInt]))
    axs[sampleInt].set_title(sampleList[sampleInt])
    N, bins, patches = axs[sampleInt].hist(data, bins=num_bins)
    fracs = N / N.max()
    norm = matplotlib.colors.Normalize(fracs.min(), fracs.max())

    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.plasma(norm(thisfrac))
        thispatch.set_facecolor(color)

# plt.xticks(np.arange(-2, 4, step=1))
plt.show()