import sys, json, pprint
from subprocess import call

helber="""
   --- README of exp07-trim ---
Title:
    batch processing for Trimmomatic
Usage:
    python exp07-trim <source>
Note:
    command split into [ linoli , linuli , linali ]
Required variables:
  config.json
    "var"
      "thread"
      "path"
        "pwd"
        "trimmomatic"
        "trimmoresut"

CAUTION:
    You need to set <PATH> ("var"/"path"/"pwd" in config.json)
      with absolute path
    Because subprocess.call may fail to pass pwd to system

Original command:
  java -jar <bin>/trimmomatic-0.35.jar PE -phred33
    -threads <threads> -trimlog <logfile>\
    input_forward.fq.gz input_reverse.fq.gz \
    output_forward_paired.fq.gz output_forward_unpaired.fq.gz \
    output_reverse_paired.fq.gz output_reverse_unpaired.fq.gz \
    ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 LEADING:3 \
    TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36
   --- README ---
""""""
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
patoho: path of fastq directory
binoho: <bin>
resuho: path of output directory
tredasi: threads """
pafwadi = configdi.get('path',{})
patoho = pafwadi.get('pwd',"")
soroho = patoho + "/" + pafwadi.get('raw',"")
binoho = patoho + "/" + pafwadi.get('trimmomatic',"")
resuho = patoho + "/" + pafwadi.get('trimmoresut',"")

tribeli = configdi.get('tribe',[])
fallidi = configdi.get('file-list',{})
tredasi = configdi.get('thread',"")

# linose: first part of command
linoli = [ 'java', '-jar', binoho+'trimmomatic-0.35.jar', 'PE',
'-phred33', '-threads', tredasi, '-trimlog']

linali = [ "ILLUMINACLIP:TruSeq3-PE.fa:2:30:10", "LEADING:3",
"TRAILING:3", "SLIDINGWINDOW:4:15", "MINLEN:36"]

if len(sys.argv) == 1:
    print(helber)

# --- Main ---
for seta in sys.argv:
    if seta in tribeli:
        fallisi = fallidi.get(fallisi,{})
        for lino in open(fallisi).read().splitlines():
            linuli = []
            inputsi = soroho + "/" + lino
            inputsi = soroho + "/" + lino



    elif seta in ['-h','--help','-help','/?']:
        print(helber)

    else:
        print( 'Ignore: ' + seta )
