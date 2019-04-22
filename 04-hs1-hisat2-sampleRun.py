#!/usr/bin/env python3
import libConfig, libPrint, libHISAT, pathlib

Align = libHISAT.aligner()
Align.branchStr = "testing"
Align.aligning()