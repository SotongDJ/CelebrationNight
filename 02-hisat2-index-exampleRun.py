#!/usr/bin/env python3
import libHISAT

for indexStr in ["speciesAnnotationA","speciesAnnotationB","speciesAnnotationC"]:
    Index = libHISAT.indexer()
    Index.titleStr = indexStr
    Index.indexing()
