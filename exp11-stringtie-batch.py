#!/usr/bin/env python3
import librun, libconfig, sys
global helber
helber="""
   --- README of exp11-stringtie-batch ---
  Title:
    Batch Processing for StringTie

  Usage:
    python exp11-stringtie-batch -t <TRIBE> -g <GROUP,GROUP,GROUP...>

  Data Structure:
    First : tribe,
        e.g. raw, untrim, trimmed...
    Second: group,
        e.g. control, A, B, 1, 2...
    Third : subgroup/files,
        e.g. foward, reverse, pair, unpair

    Visualise graph: explanation01-dataStructure.svg

  Original command:


  CAUTION:
    <GROUP> must separate with space
    <GROUP> don't allowed spacing

   --- README ---
""""""
 Postfix of variables:
  -si: String
   -ni: alternative/second string for same Usage
   -fi: string for open()
  -ho: String(that store dir path)
  -ti: Intiger/Float
  -li: List
  -tu: Tuple
  -di: Dictionary
  -fa: File (with open())
  -so: JSON
"""
Confi = libconfig.confi()
class loggo(librun.loggi):
    def pesonai(self):
        self.dicodi = {
            "tribe"   : [],
            "group"   : []
        }
        self.sync()

        self.tagesi = ""

        self.adcoli = []
        self.comali = []

        self.filasi = "exp11-stringtie-batch.py"
        self.libadi = {}
        self.prelogi = Confi.get("result/log")+"/exp11-stringtie-batch-"

    def actor(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])

Runni = loggo()
