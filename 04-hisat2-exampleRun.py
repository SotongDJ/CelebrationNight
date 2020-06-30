#!/usr/bin/env python3
import libConfig, libPrint, libHISAT, pathlib

Align = libHISAT.aligner()
Align.queryStr = "speciesTreatment"
Align.aligning()
"""
Align = libHISAT.aligner()
Align.queryStr = "speciesTreatment2"
Align.aligning()

Align = libHISAT.aligner()
Align.queryStr = "speciesTreatment3"
Align.aligning()

Align = libHISAT.aligner()
Align.queryStr = "species2TreatmentPE"
Align.aligning()

Align = libHISAT.aligner()
Align.queryStr = "species2TreatmentSE"
Align.aligning()
"""