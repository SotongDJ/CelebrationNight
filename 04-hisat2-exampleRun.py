#!/usr/bin/env python3
import libConfig, libPrint, libHISAT, pathlib

Align = libHISAT.aligner()
Align.queryStr = "testing"
Align.aligning()