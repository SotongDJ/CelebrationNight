#!/usr/bin/env python3
import libHISAT

for indexStr in ["speciesTestingA","speciesTestingB","speciesTestingC"]:
    Index = libHISAT.indexer()
    Index.titleStr = indexStr
    Index.indexing()
