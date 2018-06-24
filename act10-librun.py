#!/usr/bin/env python3
import sys, pprint
import librun
global helber
helber="""
   --- README of act10-librun ---
 Title:
    Showcase of librun

 Usage:
    python3 act10-librun.py --hello=waha -h a ba -t ca -hello mow

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
class runno(librun.workflow):

    def pesonai(self):
        # self.testing = True
        self.helb = helber
        
        self.dicodi = {
            "hello" : ""
        }
        self.Synom.input({"h":"hello"})
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

        self.runit()

        self.frasi = "Ano.dicodi:\n"+pprint.pformat(self.dicodi,compact=True)
        self.printe()
        self.frasi = "Ano.locadi:\n"+pprint.pformat(self.locadi,compact=True)
        self.printe()
        self.frasi = "Ano.libadi:\n"+pprint.pformat(self.libadi,compact=True)
        self.printe()

        self.endin()
Ano = runno()
