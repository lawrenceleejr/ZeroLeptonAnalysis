#!/usr/bin/env python

import pprint
import time
import ROOT
import os
import sys

from array import array
import argparse

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

ROOT.gSystem.Load("libSusyFitter.so");
#ROOT.gROOT.LoadMacro("ContourUtils.C");
#ROOT.gROOT.LoadMacro("contourmacros/GetSRName.C");

# Use HistFitter's automatic rejection?
automaticRejection=False

parser = argparse.ArgumentParser()
parser.add_argument("-F", "--inputFile", help="input file", default=[], action='append')
parser.add_argument("-f", "--format", help="format of input file", default=None)
parser.add_argument("-I", "--interpretation", help="interpretation", default=None)
parser.add_argument("-c", "--cutstring", help="cut string applied", default=None)
parser.add_argument("-p", "--prefix", help="discovery prefix", default="")
parser.add_argument("-o", "--output-dir", help="output directory", type=str, default="Outputs/")

#(options, args) = parser.parse_args(sys.argv[1:])
args = parser.parse_args()

filenames = args.inputFile
for f in filenames:
    if not f or not os.path.isfile(f):
        print "Cannot find input file %s" % f
        del f

if filenames == []:
    print "No filenames given"
    sys.exit()

if not args.format:
    print "No format string specified"
    sys.exit()

if not args.cutstring:
    print "No cut string specified"
    sys.exit()

if not args.interpretation:
    print "No interpretation specified"
    sys.exit()

for f in filenames:
    ROOT.CollectAndWriteHypoTestResults(f, args.format, args.interpretation, args.cutstring, int(automaticRejection), args.output_dir, args.prefix ) ;

