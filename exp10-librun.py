#!/usr/bin/env python3
import sys, pprint
import librun

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
        self.hedda()

        self.tagesi = "temp"
        self.chkpaf()

        self.ranni()

        self.frasi = "Ano.dicodi:\n"+pprint.pformat(Ano.dicodi,compact=True)
        self.printe()
        self.frasi = "Ano.locadi:\n"+pprint.pformat(Ano.locadi,compact=True)
        self.printe()
        self.frasi = "Ano.libadi:\n"+pprint.pformat(Ano.libadi,compact=True)
        self.printe()

        self.calti()
Ano = runno()
