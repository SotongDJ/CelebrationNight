#!/usr/bin/env python3
import libCuffdiff

DiffEA = libCuffdiff.differ()
DiffEA.branchStr = "testing"
DiffEA.diffing()