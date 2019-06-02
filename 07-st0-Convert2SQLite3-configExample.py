#!/usr/bin/env python3
import libConfig
# ---- Keyword list ----
"""
testing
["Control","T1","T2","T3","T4","T5"]
["r1","r2","r3"]
"ControlT1"
speciesAnnotationA
speciesAnnotationB
speciesAnnotationC
"""
# ---- Configuration of Experiment Design ---- 
expRep = libConfig.config()
expRep.queryStr = "testing"
expRep.folderStr = "config/"
# Arguments/Parameters below need to modify depend on 
# your experiment design and naming style
expRep.queryDict = {
    "branch" : "testing",
    "group" : ["Control","T1","T2","T3","T4","T5"],
    "replication" : ["r1","r2","r3"],
    "samplePattern" : "{group}{replication}",
    "controlSample" : "ControlT1",
    "pairPostfix" : "pair",
    "unpairPostfix" : "unpair",
    "hisat2Condition" : "hisat2ForStringtie",
    "conditionList" : [("speciesAnnotationB",'trimQ30'),("speciesAnnotationA",'trimQ30'),("speciesAnnotationC",'trimQ30')],
    "methodList" : ["Stringtie","dsStringtie","waStringtie"],
    "[sqlite]geneSourceDict" : {
        "Stringtie" : "05-st-Stringtie",
        "dsStringtie" : "05-ds-Stringtie",
        "waStringtie" : "05-wa-Stringtie"
    },
    "[sqlite]transcriptSourceDict" : {
        "Stringtie" : "05-st-ballgown",
        "dsStringtie" : "05-ds-ballgown",
        "waStringtie" : "05-ds-ballgown"
    },
    "[sqlite]geneSourcePathStr" : "data/{folder}/{branch}/{ant}-{trim}/{sample}-expression.tsv",
    "[sqlite]transcriptSourcePathStr" : "data/{folder}/{branch}/{ant}-{trim}-{sample}/t_data.ctab",
    "[sqlite]logFilename" : 'Expression-{ant}-{trim}',
    "sqlFolderStr" : "data/07-st-expressionTable-SQLite3/{branch}-{method}/",
    "sqlPathStr" : 'data/07-st-expressionTable-SQLite3/{branch}-{method}/Expression-{ant}-{trim}.db',
    "testing" : False,
}
expRep.modeStr = "UPDATE"
expRep.save()