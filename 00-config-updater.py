import json,pathlib
# ---- Don't edit thing above this line ----

queryStr = "brapaEnseQ20"
folderStr = "data/config/"
queryDict = {
    "type" : "branch",
    "reference" : "brapaEnsembl",
    "branch" : "trimQ20",
}
modeStr = "OVERWRITE" # UPDATE or OVERWRITE

# ---- Don't edit thing below this line ----
pathStr = "{}{}.json".format(
    folderStr,queryStr
)
pathlib.Path(folderStr).mkdir(parents=True,exist_ok=True)
if not pathlib.Path(pathStr).exists():
    with open(pathStr,"w") as targetHandle:
        json.dump(dict(),targetHandle)

if modeStr == "UPDATE":
    sourceDict = json.load(open(pathStr,"r"))
elif modeStr == "OVERWRITE":
    sourceDict = dict()
else:
    print("OVERWRITE")
    sourceDict = dict()
sourceDict.update()

with open(pathStr,"w") as targetHandle:
    json.dump(queryDict,targetHandle,indent=2,sort_keys=True)
