#!/usr/bin/env python3
import sys, json, pprint, time
from subprocess import call

helber="""
   --- README of exp07-trim ---
 Title:
    Batch Processing for Trimmomatic

 Usage:
    python exp07-trim <TRIBE> <GROUP,GROUP,GROUP...>

 Structure:
    First : tribe,
        e.g. raw, untrim, trimmed...
    Second: group,
        e.g. control, A, B, 1, 2...
    Third : subgroup/files,
        e.g. foward, reverse, pair, unpair

    Visualise graph: explanation01-dataStructure.svg

 Required variables:
  config.json
    "trimmomatic"/"pair"
    "trimmomatic"/"unpair"
    "bin"/"trimmomatic"
    "bin"/"tmmadapter"
    "var"/"tribe"
    "var"/"group"
    "var"/"subgroup"
    "var"/"file-list"
    "var"/"binding"
    "var"/"thread"
    "var"/"path"/"raw"
    "var"/"path"/"log"
    "var"/"path"/"trimmoresut"
    "var"/"prefix" [value of pair and unpair]

 Original command:
  java -jar <bin>/trimmomatic-0.35.jar PE -phred33
  -threads <threads> -trimlog <logfile>\
  input_forward.fq.gz input_reverse.fq.gz \
  output_forward_paired.fq.gz output_forward_unpaired.fq.gz \
  output_reverse_paired.fq.gz output_reverse_unpaired.fq.gz \
  ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 LEADING:3 \
  TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36

 CAUTION:
    <GROUP> must separate with comma
    <GROUP> don't allowed spacing

   --- README ---
""""""
    command split into [ linoli , linuli , linali ]
 Postfix:
  -si: String
  -ho: String(that store dir path)
  -ti: Intiger/Float
  -li: List
  -tu: Tuple
  -di: Dictionary
  -fa: File (with open())
  -so: JSON
"""
# config- : stand for variables related to config file
configsi = 'data/config.json'
configfa = open(configsi,'r')
configso = json.load(configfa)
configdi = configso.get('var',{})
"""
resuho: path of output directory
tredasi: threads """
binodi = configso.get('bin',{})
trimfa = binodi.get('trimmomatic',"")
trimsi = binodi.get('tmmadapter',"")

pafwadi = configdi.get('path',{})
soroho = pafwadi.get('raw',"")
logoho = pafwadi.get('log',"")
resuho = pafwadi.get('trimmoresut',"")

trimodi = configso.get('trimmomatic',{})
payirsi = trimodi.get('pair',"")
unparsi = trimodi.get('unpair',"")

prefidi = configdi.get('prefix',{})
prepisi = prefidi.get(payirsi,"")
preunsi = prefidi.get(unparsi,"")

tribeli = configdi.get('tribe',[])
grupoli = configdi.get('group',[])
sugrudi = configdi.get('subgroup',{})
fallidi = configdi.get('file-list',{})
bindosi = configdi.get('binding',"")
tredasi = configdi.get('thread',"")

# linose: first part of command
linoli = [ 'java', '-jar', trimfa ,
'PE', '-phred33', '-threads', tredasi ]

linali = [ "ILLUMINACLIP:" + trimsi + "/adapters/TruSeq3-PE.fa:2:30:10",
"LEADING:3", "TRAILING:3", "SLIDINGWINDOW:4:15", "MINLEN:36"]

timmasi = time.strftime("%Y%m%d%H%M%S")

tribesi = ""
metali = []
meseli = []

if len(sys.argv) < 1:
    print(helber)
elif len(sys.argv) == 2:
    # if sys.argv[-1] in tribeli:
    tribesi = sys.argv[-1]
    metali = grupoli
elif len(sys.argv) == 3:
    meseli.extend(sys.argv)
    # if metali[2] in tribeli:
    tribesi = meseli[-2]
    metali = []
    metali = meseli[-1].split(',')
    for n in metali:
        if n not in grupoli:
            metali.pop(metali.index(n))

else:
    print(helber)

for n in ['-h','--help','-help','/?']:
    if n in sys.argv:
        print(helber)

runninlog = ("RUN started at " + timmasi )
scriptlog = ("LOCAL\n" +
"Input:  " + pprint.pformat(sys.argv) + "\n" +
"Tribe:  " + pprint.pformat(tribesi) + "\n" +
"Group:  " + pprint.pformat(metali) + "\n")
configlog = ("FROM config.json\n" +
"\"tribe\"      : " + pprint.pformat(tribeli) + "\n" +
"\"group\"      : " + pprint.pformat(grupoli) + "\n" +
"\"subgroup\"   : " + pprint.pformat(sugrudi) + "\n" +
"\"trimmomatic\": " + pprint.pformat(trimodi) + "\n" +
"\"prefix\"     : " + pprint.pformat(prefidi) + "\n" +
"\"file-list\"  : " + pprint.pformat(fallidi) + "\n" +
"\"binding\"    : " + pprint.pformat(bindosi) + "\n" +
"\"thread\"     : " + pprint.pformat(tredasi) + "\n" +
"\"raw\"        : " + pprint.pformat(soroho) + "\n" +
"\"log\"        : " + pprint.pformat(logoho) + "\n" +
"\"trimmomatic\": " + pprint.pformat(trimfa) + "\n" +
"\"tmmadapter\" : " + pprint.pformat(trimsi) + "\n" +
"\"trimmoresut\": " + pprint.pformat(resuho) + "\n")
print("\n\n" + scriptlog + "\n" + configlog)
logosi = logoho + "/exp07-trim-run-" + timmasi + ".log"
with open(logosi,'w') as logofale:
    logofale.write(scriptlog + "\n" + configlog)
# --- Main ---

fallisi = fallidi.get(tribesi,{})
for grupo in metali:
    runisi = ""
    comasi = ""
    argudi = {
    "forward":"?",
    "reverse":"?"
    }
    for fale in open(fallisi).read().splitlines():
        for argu in list(argudi.keys()):
            compasi = sugrudi.get(argu,'?')
            if compasi == "?":
                print("Error: fixing config.json required")
                print(" 'var'/'sugru'/'" + argu + "' not exist ")
            elif compasi in fale:
                if grupo in fale:
                    argudi.update({ argu : fale })

    if "?" in list(argudi.values()):
        print("Error: something went wrong")

    fofasi = argudi.get("forward","")
    refasi = argudi.get("reverse","")

    call(["mkdir",resuho + "-pr/"])
    call(["mkdir",resuho + "-un/"])

    linuli = [
        soroho + "/" + tribesi + "/" + fofasi,
        soroho + "/" + tribesi + "/" + refasi,
        resuho + "-pr/" + prepisi + "-" + fofasi,
        resuho + "-un/" + preunsi + "-" + fofasi,
        resuho + "-pr/" + prepisi + "-" + refasi,
        resuho + "-un/" + preunsi + "-" + refasi,
    ]

    arguli = linoli + linuli +linali

    print('\n\nCommand: \n  ' + '  \\\n    '.join(arguli))
    runisi = "\n\nRUN started at " + time.strftime("%Y%m%d%H%M%S")
    comasi = "\nCommand: \n  " + " ".join(arguli)
    with open(logosi,'a') as logofale:
        logofale.write(runisi + comasi)
    call(arguli, stdout=open(logosi, 'a'))
