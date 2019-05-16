#!/usr/bin/env python3
import libConfig, libPrint, pathlib
import libStringtie

Assembling = libStringtie.assembler()
Assembling.branchStr = "testing"
Assembling.withoutAnnotation = True
Assembling.headerStr = "waStringtie"
Assembling.assembling()
