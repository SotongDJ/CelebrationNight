#!/usr/bin/env python3
import sys, pprint
import pyWorkFlow
global helper_msg_block
helper_msg_block="""
   --- README of act10-pyWorkFlow ---
 Title:
    Showcase of pyWorkFlow

 Usage:
    python3 act10-librun.py --hello=waha -h a ba -t ca -hello mow

   --- README ---
"""
class runno(pyWorkFlow.workflow):

    def personalize(self):
        # self.testing = True
        self.helper_msg_str = helper_msg_block

        self.requested_argv_dict = {
            "hello" : ""
        }
        self.SynonymDict.input({"h":"hello"})
        self.synchornize()

        self.target_file_path = ""

        self.comand_line_list=['echo','wahaha']

        self.script_name = "pyWorkFlow.py"
        self.requested_config_dict = {
            "prefix/wawa" : "haha/wulala"
        }
        self.log_file_prefix_str = "temp/temp-"

    def actor(self):
        self.startLog()

        self.target_file_path = "temp"
        self.checkPath()

        self.runCommand()

        self.phrase_str = "Ano.requested_argv_dict:\n"+pprint.pformat(self.requested_argv_dict,compact=True)
        self.printPhrase()
        self.phrase_str = "Ano.locadi:\n"+pprint.pformat(self.locadi,compact=True)
        self.printPhrase()
        self.phrase_str = "Ano.requested_config_dict:\n"+pprint.pformat(self.requested_config_dict,compact=True)
        self.printPhrase()

        self.stopLog()
Ano = runno()
