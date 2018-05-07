#!/usr/bin/env python3
import sys, json, pprint, time
from subprocess import call

helber="""
   --- README of exp08-tophat-batch ---
 Title:
    Batch Processing for TopHat

 Usage:
    python exp08-tophat-batch <TRIBE> <GROUP,GROUP,GROUP...>

 Structure:
    First : tribe,
        e.g. raw, untrim, trimmed...
    Second: group,
        e.g. control, A, B, 1, 2...
    Third : subgroup/files,
        e.g. foward, reverse, pair, unpair

    Visualise graph: explanation01-dataStructure.svg

 Original command:

 CAUTION:
    <GROUP> must separate with comma
    <GROUP> don't allowed spacing

   --- README ---
""""""
 Postfix of variables:
  -si: String
   -ni: alternative/second string for same Usage
   -fi: string for open()
  -ho: String(that store dir path)
  -ti: Intiger/Float
  -li: List
  -tu: Tuple
  -di: Dictionary
  -fa: File (with open())
  -so: JSON
"""
