#!/usr/bin/env python3
import libHISAT
"""
for indexStr in ["speciesDatabase","speciesDatabase2","speciesDatabase3","species2Database"]:
    Index = libHISAT.indexer()
    Index.titleStr = indexStr
    Index.indexing()
"""
Index = libHISAT.indexer()
Index.titleStr = "speciesDatabase"
Index.indexing()
