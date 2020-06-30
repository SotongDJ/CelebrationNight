#!/usr/bin/env python3
import libConfig, libPrint, pathlib
import libCuffdiff

ConveTR = libCuffdiff.converter()
ConveTR.branchStr = "speciesTreatment"
ConveTR.converting()
"""
ConveTR = libCuffdiff.converter()
ConveTR.branchStr = "speciesTreatment2"
ConveTR.converting()
"""