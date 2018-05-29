#!/usr/bin/env python3
import sys, pprint
import librun
global helber
helber="""
   --- README of exp10-librun ---
 Title:
    Showcase of librun

 Usage:
    python3 exp10-librun.py --hello=waha -h a ba -t ca -hello mow

   --- README ---
"""
"""
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
class runno(librun.loggi):

    def pesonai(self):
        # self.testing = True

        self.dicodi = {
            "hello" : ""
        }
        self.sync()

        self.tagesi = ""

        self.comali=['echo','wahaha']

        self.filasi = "librun.py"
        self.libadi = {
            "prefix/wawa" : "haha/wulala"
        }
        self.prelogi = "temp/temp-"

    def actor(self):
        self.head()

        self.tagesi = "temp"
        self.chkpaf()

        self.ranni()

        self.frasi = "Ano.dicodi:\n"+pprint.pformat(Ano.dicodi,compact=True)
        self.printe()
        self.frasi = "Ano.locadi:\n"+pprint.pformat(Ano.locadi,compact=True)
        self.printe()
        self.frasi = "Ano.libadi:\n"+pprint.pformat(Ano.libadi,compact=True)
        self.printe()

        self.endin()
Ano = runno()
