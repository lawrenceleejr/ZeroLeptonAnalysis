#!/usr/bin/env python

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
# Import Modules                                                             # 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
ROOT.gSystem.Load("libSusyFitter.so")
import sys, os, string, shutil,pickle,subprocess
from ROOT import TMsgLogger

from Utils import *
from ChannelConfig import *
from ChannelsDict import *
from ZLFitterConfig import *

from optparse import OptionParser

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
# Some global variables
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#




#WARNING: need to add protection in the code
parser = OptionParser()
parser.add_option("-a", "--anaShortName", help="specify anaShortName (default SR6jm)", default = "SR2jl")
parser.add_option("-r", "--region", help="specify region (default SR)", default = "SR")
(options, args) = parser.parse_args()


cuts=finalChannelsDict[options.anaShortName].getCutsDict()





print "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
print "Cut string for %s in %s" % (options.region, options.anaShortName) 
print cuts[options.region]
print "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"

for cut in cuts[options.region].split("&&"):
    print cut
