# List generator
import json, subprocess
wanisi = """Required your target directory.
The limitation of Target Directory:
    Space is not allowed (safety concern)
    Target must be under Current Directory

Current directory('s path):"""
print(wanisi)
subprocess.call(['pwd'])
tardir = input("\nWhat's the path of your target directory?\n")
print("Target path set as:\n--> "+tardir+" <--")
