#!/usr/bin/env python3
import sys, pprint
import librun

class runno(librun.loggi):

    def pesonai(self):
        # self.testing = True
        self.typesi = 'script'

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

Ano = runno()
print("Ano.dicodi:\n"+pprint.pformat(Ano.dicodi,compact=True))
print("Ano.locadi:\n"+pprint.pformat(Ano.locadi,compact=True))
print("Ano.libadi:\n"+pprint.pformat(Ano.libadi,compact=True))
