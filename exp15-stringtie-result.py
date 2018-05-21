#!/usr/bin/env python3
import librun, libconfig, libtab
import time
global helber
helber="""
   --- README of exp15-stringtie-result.py ---
  Title:
    Batch Processing for StringTie

  Usage:
    python3 exp15-stringtie-result.py -t <TRIBE> --control=<Control Group> -g <GROUP,GROUP,GROUP...>

  Data Structure:
    First : tribe,
        e.g. raw, untrim, trimmed...
    Second: group,
        e.g. control, A, B, 1, 2...
    Third : subgroup/files,
        e.g. foward, reverse, pair, unpair

    Visualise graph: explanation01-dataStructure.svg

  CAUTION:
    Exp15 required libtab
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
Covet = libtab.runno()
# Covet.dicodi = { "files" : ["result.json","basic.json"] }
# Covet.actor()
Confi = libconfig.confi()
class loggo(librun.loggi):
    def pesonai(self):
        # self.testing = True
        self.typesi = 'script'

        self.dicodi = {
            "tribe"   : [],
            "group"   : [],
        }
        self.sync()

        self.tagesi = ""

        self.comali = []
        self.filasi = "exp15-stringtie-result"
        self.libadi = {}
        self.prelogi = Confi.get("result/log")+"/exp15-sr"

    def actor(self):
        tibeli = self.dicodi.get("tribe",[])
        gupoli = self.dicodi.get("group",[])

        self.hedda()

        self.tagesi = Confi.get("result/stringtie")
        self.chkpaf()

        for tibe in tibeli:

            for gupo in metali:

        self.calti()

Runni = loggo()
