#!/usr/bin/env python

import pprint
import time
import ROOT
import os
import sys

from array import array
from optparse import OptionParser

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

ROOT.gSystem.Load("libSusyFitter.so");
#ROOT.gROOT.LoadMacro("ContourUtils.C");
#ROOT.gROOT.LoadMacro("contourmacros/GetSRName.C");

# Use HistFitter's automatic rejection? 
automaticRejection=False

parser = OptionParser()
parser.add_option("-F", "--inputFile", help="input file", default=None)
parser.add_option("-f", "--format", help="format of input file", default=None)
parser.add_option("-I", "--interpretation", help="interpretation", default=None)
parser.add_option("-c", "--cutstring", help="cut string applied", default=None)
parser.add_option("-d", "--discovery", help="discovery prefix", default=False, action="store_true")

(options, args) = parser.parse_args(sys.argv[1:])

if not options.inputFile or not os.path.isfile(options.inputFile):
    print "Cannot find input file %s" % options.inputFile
    sys.exit()

if not options.format:
    print "No format string specified"
    sys.exit()

if not options.cutstring:
    print "No cut string specified"
    sys.exit()

if not options.interpretation:
    print "No interpretation specified"
    sys.exit()

prefix = ""
if options.discovery:
    prefix = "discovery"

ROOT.CollectAndWriteHypoTestResults( options.inputFile, options.format, options.interpretation, options.cutstring, int(automaticRejection), "Outputs/", prefix ) ;

