import sys, json, pprint, time
from subprocess import call

helber="""
   --- README of exp01-list ---
Title:
    List Generator
    (Actually, this exp. is Exp08 or Exp07.5
    But I decide to remove Exp01 and rename Exp08 to Exp01)

Usage:
    python exp01-trim <TRIBE> [-data=<DATA>]

    <TRIBE>: Name of tribe
    <DATA> : Path of Data dir. (default is "./data")
    
Structure:
    First : tribe,
        e.g. raw, untrim, trimmed...
    Second: group,
        e.g. control, A, B, 1, 2...
    Third : subgroup/files,
        e.g. foward, reverse, pair, unpair

Required variables:
  config.json

Original command:
  ls -1

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
 -so: Something (with json.dump(), mostly dictionary)
"""
# config- : stand for variables related to config file
configsi = 'data/config.json'
configfa = open(configsi,'r')
configso = json.load(configfa)
configdi = configso.get('var',{})
"""
resuho: path of output directory"""
pafwadi = configdi.get('path',{})
soroho = pafwadi.get('raw',"")
logoho = pafwadi.get('log',"")

patoho = soroho + "/" + tribe
