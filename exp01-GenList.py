# List generator
import json, subprocess
print("Current path [PWD]:")
subprocess.call(['pwd'])
wanisi = """Required your target directory.
The limitation of Target Directory:
    Need to be absolute path (start from root, '/')
    Space is not allowed (safety concern)
    Can replace "[PWD]" (without quotation marks) with current path
"""
tardir = input("What's the path of your target directory?\n")
print("Target path set as:\n--> "+tardir+" <--")
