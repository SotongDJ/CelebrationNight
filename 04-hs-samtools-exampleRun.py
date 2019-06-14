#!/usr/bin/env python3
import libConfig, libPrint, libHISAT, pathlib

Summarise = libHISAT.summariser()
Summarise.branchStr = "testing"
Summarise.summaring()