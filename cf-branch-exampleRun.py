#!/usr/bin/env python3
import libConfig
# ---- Configuration of Experiment Design ---- 
expRep = libConfig.config()
expRep.queryStr = "speciesTreatment"
expRep.folderStr = "config/"
# Arguments/Parameters below need to modify depend on 
# your experiment design and naming style
expRep.queryDict = {
    "branch" : "speciesTreatment",
    "group" : ["control","treat1","treat2","treat3","treat4"],
    "direction" : ["R1","R2"],
    "replication" : ["1","2","3"],
    "pairPostfix" : "pair",
    "unpairPostfix" : "unpair",
    "mode" : "pairEnd",
    "thread" : "6",
    "conditionsList" : [
        {
            "genome" : "speciesDatabase",
            "trim" : "trimQ30",
            "transcriptome" : "dsStringtie",
            "map" : "hisat2ForStringtie",
        },
        {
            "genome" : "speciesDatabase",
            "trim" : "trimQ30",
            "transcriptome" : "gffRead",
            "map" : "hisat2ForCufflinks",
        }
    ],
    "gtfDict" : {
        "Stringtie" : {
            "folder" : "05-st-Stringtie",
            "balgown" : "05-st-ballgown",
        },
        "dsStringtie" : {
            "folder" : "05-ds-Stringtie",
            "balgown" : "05-ds-ballgown",
        },
        "waStringtie" : {
            "folder" : "05-wa-Stringtie",
            "balgown" : "05-wa-ballgown",
        },
        "gffRead" : {
            "folder" : "05-gr-transcriptomeConstruction",
            "balgown" : "",
        }
    },
    "checkFolder" : ["largeData/01-raw/","largeData/03-trimed/speciesTreatment/"],
    "[trim]inputFileName" : "largeData/01-raw/speciesTreatment/{group}{replication}-{direction}{fileType}",
    "[trim]outputFileName" : "largeData/03-trimed/speciesTreatment/{condition}-{group}{replication}-{direction}-{pairType}{fileType}",
    "[trim]fileType" : ".fastq",
    "[hisat2]direction" : { '1' : "R1",'2' : "R2" },
    "[hisat2]inputFileName" : "largeData/03-trimed/speciesTreatment/{trim}-{group}{replication}-{direction}-{pairType}{fileType}",
    "[hisat2]outputFolder" : "largeData/04-hisat2/speciesTreatment/{annotate}-{trim}/",
    "[hisat2]outputFileName" : "largeData/04-hisat2/speciesTreatment/{annotate}-{trim}/{hisat2Condition}-{group}{replication}{fileType}",
    "[CuffDiff]resultFolder" : "userData/07-cd-estimateExpression/{branch}-{method}/{annotate}-{trim}/",
    "stringtieFolder" : "userData/{folder}/{branch}/{annotate}-{trim}/",
    "stringtieGTF" : "userData/{folder}/{branch}/{annotate}-{trim}/{group}{replication}.gtf",
    "stringtieTSV" : "userData/{transcriptome}/{branch}/{annotate}-{trim}/{group}{replication}-expression.tsv",
    "transcriptomeFolder" : "userData/{folder}/{branch}/",
    "transcriptomeGTF" : "userData/{folder}/{branch}/{annotate}-{trim}-final.gtf",
    "ballgownFolder" : "userData/{folder}/{branch}/{annotate}-{trim}-{group}{replication}/",
    "ballgownGTF" : "userData/{folder}/{branch}/{annotate}-{trim}-{group}{replication}/{group}{replication}-expression.gtf",
    "testing" : False,
}
expRep.modeStr = "UPDATE"
expRep.save()

# ---- Configuration of Experiment Design ---- 
expRep = libConfig.config()
expRep.queryStr = "speciesTreatment2"
expRep.folderStr = "config/"
# Arguments/Parameters below need to modify depend on 
# your experiment design and naming style
expRep.queryDict = {
    "branch" : "speciesTreatment2",
    "group" : ["Normal","treatI","treatJ"],
    "direction" : ["R1","R2"],
    "replication" : ["1","2","3"],
    "pairPostfix" : "pair",
    "unpairPostfix" : "unpair",
    "mode" : "pairEnd",
    "thread" : "6",
    "conditionsList" : [
        {
            "genome" : "speciesDatabase",
            "trim" : "trimQ30",
            "transcriptome" : "dsStringtie",
            "map" : "hisat2ForStringtie",
        },
        {
            "genome" : "speciesDatabase",
            "trim" : "trimQ30",
            "transcriptome" : "gffRead",
            "map" : "hisat2ForCufflinks",
        }
    ],
    "gtfDict" : {
        "Stringtie" : {
            "folder" : "05-st-Stringtie",
            "balgown" : "05-st-ballgown",
        },
        "dsStringtie" : {
            "folder" : "05-ds-Stringtie",
            "balgown" : "05-ds-ballgown",
        },
        "waStringtie" : {
            "folder" : "05-wa-Stringtie",
            "balgown" : "05-wa-ballgown",
        },
        "gffRead" : {
            "folder" : "05-gr-transcriptomeConstruction",
            "balgown" : "",
        }
    },
    "checkFolder" : ["largeData/01-raw/","largeData/03-trimed/speciesTreatment2/"], # H_S1_R1_001.fastq
    "[trim]inputFileName" : "largeData/01-raw/speciesTreatment/{group}_S{replication}_{direction}_001{fileType}",
    "[trim]outputFileName" : "largeData/03-trimed/speciesTreatment2/{condition}-{group}{replication}-{direction}-{pairType}{fileType}",
    "[trim]fileType" : ".fastq",
    "[hisat2]direction" : { '1' : "R1",'2' : "R2" },
    "[hisat2]inputFileName" : "largeData/03-trimed/speciesTreatment2/{trim}-{group}{replication}-{direction}-{pairType}{fileType}",
    "[hisat2]outputFolder" : "largeData/04-hisat2/speciesTreatment2/{annotate}-{trim}/",
    "[hisat2]outputFileName" : "largeData/04-hisat2/speciesTreatment2/{annotate}-{trim}/{hisat2Condition}-{group}{replication}{fileType}",
    "[CuffDiff]resultFolder" : "userData/07-cd-estimateExpression/{branch}-{method}/{annotate}-{trim}/",
    "stringtieFolder" : "userData/{folder}/{branch}/{annotate}-{trim}/",
    "stringtieGTF" : "userData/{folder}/{branch}/{annotate}-{trim}/{group}{replication}.gtf",
    "stringtieTSV" : "userData/{transcriptome}/{branch}/{annotate}-{trim}/{group}{replication}-expression.tsv",
    "transcriptomeFolder" : "userData/{folder}/{branch}/",
    "transcriptomeGTF" : "userData/{folder}/{branch}/{annotate}-{trim}-final.gtf",
    "ballgownFolder" : "userData/{folder}/{branch}/{annotate}-{trim}-{group}{replication}/",
    "ballgownGTF" : "userData/{folder}/{branch}/{annotate}-{trim}-{group}{replication}/{group}{replication}-expression.gtf",
    "testing" : False,
}
expRep.modeStr = "UPDATE"
expRep.save()
