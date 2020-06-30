#!/usr/bin/env python3
import libConfig, libPrint, pathlib
import libCuffdiff

DiffEA = libCuffdiff.differ()
DiffEA.branchStr = "speciesTreatment"
DiffEA.diffing()
"""
DiffEA = libCuffdiff.differ()
DiffEA.branchStr = "speciesTreatment2"
DiffEA.diffing()
"""