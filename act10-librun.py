#!/usr/bin/env python3
import sys, pprint
import libWorkFlow
global helper_msg_block
helper_msg_block="""
   --- README of act10-libWorkFlow ---
 Title:
    Showcase of libWorkFlow

 Usage:
    python3 act10-libWorkFlow.py --hello=waha -h a ba -t ca -hello mow

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
class runno(libWorkFlow.workflow):

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

        self.script_name_str = "libWorkFlow.py"
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
