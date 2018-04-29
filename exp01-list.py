import sys, json, pprint, time
from subprocess import call

helber="""
   --- README of exp01-list ---
Title:
    List Generator
    (Actually, this exp. is Exp08 or Exp07.5
    But I decide to remove Exp01 and rename Exp08 to Exp01)

Usage:
    python exp01-trim <TRIBE> [-data=<DATA>]*

    <TRIBE>: Name of tribe
    <DATA>* : Path of Data dir. (default is "./data")

    * concept of work, but haven't work

Structure:
    First : tribe,
        e.g. raw, untrim, trimmed...
    Second: group,
        e.g. control, A, B, 1, 2...
    Third : subgroup/files,
        e.g. foward, reverse, pair, unpair

Required variables:
  config.json
    "var"/"list-format"
    "var"/"path"/"raw"
    "var"/"path"/"log"

Modify variables:
  config.json
    "var"/"file-list"

Original command:
  ls -1

   --- README ---
""""""
Postfix:
 -bo: boolean
 -si: String
 -ho: String(that store dir path)
 -ti: Intiger/Float
 -li: List
 -tu: Tuple
 -di: Dictionary
 -fa: File (with open())
 -so: Something (with json.dump(), mostly dictionary)
"""
#    ---- Processing received argument----
tribesi = ""
if len(sys.argv) < 1:
    print(helber)
elif len(sys.argv) == 2:
    tribesi = sys.argv[-1]
else:
    print(helber)

for n in ['-h','--help','-help','/?']:
    if n in sys.argv:
        print(helber)


# config- : stand for variables related to config file
configsi = 'data/config.json'
configfa = open(configsi,'r')
configso = json.load(configfa)
configdi = configso.get('var',{})

lifomasi = configdi.get('list-format',[])

pafwadi = configdi.get('path',{})
soroho = pafwadi.get('raw',"")
logoho = pafwadi.get('log',"")

patoho = soroho + "/" + tribesi
tempasi = "temp/" + tribesi + ".list"
listasi = "data/" + tribesi + ".list"

if tribesi !="" :
    arguli = ["ls","-1",patoho]
    print('\nCommand: \n  ' + '  \\\n    '.join(arguli))
    call(arguli, stdout=open(tempasi, 'w'))

    with open(listasi,'w') as listafa:

        for lino in open(tempasi).read().splitlines():
            valubo = False
            linoli = lino.split('.')
            for nata in lifomasi:
                if nata in linoli[-1]:
                    valubo = True
            if valubo == True:
                listafa.write(lino+"\n")

    listadi = configdi.get("file-list",{})
    listadi.update({ tribesi : listasi })
    configdi.update({ 'file-list' : listadi })
    configso.update({ 'var' : configdi })

    with open(configsi,'w') as configfa:
        json.dump(configso,configfa,indent=4,sort_keys=True)
