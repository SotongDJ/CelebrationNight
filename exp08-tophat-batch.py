#!/usr/bin/env python3
import sys, json, pprint, time
from subprocess import call

helber="""
   --- README of exp08-tophat-batch ---
Title:
    Batch Processing for TopHat

Usage:
    python exp08-tophat-batch <TRIBE> <GROUP,GROUP,GROUP...>

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
    "var"/"tribe"
    "var"/"group"
    "var"/"subgroup"
    "var"/"file-list"
    "var"/"binding"
    "var"/"thread"
    "var"/"path"/"raw"
    "var"/"path"/"log"
    "var"/"path"/"trimmomatic"
    "var"/"path"/"trimmoresut"

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
binoho: <bin>
resuho: path of output directory
tredasi: threads """
pafwadi = configdi.get('path',{})
soroho = pafwadi.get('raw',"")
logoho = pafwadi.get('log',"")
binoho = pafwadi.get('trimmomatic',"")
resuho = pafwadi.get('trimmoresut',"")

tribeli = configdi.get('tribe',[])
grupoli = configdi.get('group',[])
sugrudi = configdi.get('subgroup',{})
fallidi = configdi.get('file-list',{})
bindosi = configdi.get('binding',"")
tredasi = configdi.get('thread',"")

timmasi = time.strftime("%Y%m%d%H%M%S")



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
"\"file-list\"  : " + pprint.pformat(fallidi) + "\n" +
"\"binding\"    : " + pprint.pformat(bindosi) + "\n" +
"\"thread\"     : " + pprint.pformat(tredasi) + "\n" +
"\"raw\"        : " + pprint.pformat(soroho) + "\n" +
"\"log\"        : " + pprint.pformat(logoho) + "\n" +
"\"trimmomatic\": " + pprint.pformat(binoho) + "\n" +
"\"trimmoresut\": " + pprint.pformat(resuho) + "\n")
print("\n\n" + scriptlog + "\n" + configlog)
logosi = logoho + "/exp07-trim-run-" + timmasi + ".log"
with open(logosi,'w') as logofale:
    logofale.write(scriptlog + "\n" + configlog)
# --- Main ---
