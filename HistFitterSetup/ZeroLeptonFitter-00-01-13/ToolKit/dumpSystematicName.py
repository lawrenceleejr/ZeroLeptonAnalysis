#!/usr/bin/env python

import ROOT
from ROOT import *
ROOT.PyConfig.IgnoreCommandLineOptions = True

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)

ftemp=TFile.Open("root://eosatlas.cern.ch//eos/atlas/user/l/lduflot/atlasreadable/ZeroLeptonRun2-00-00-57/filtered/GAMMAMassiveCB.root")


print "===================="
btag_syst_names = ftemp.Get('btag_weights_names')
print btag_syst_names.GetEntries()

for isys in range(btag_syst_names.GetEntries()):
    print btag_syst_names[isys].Print("")


print "===================="
event_syst_names = ftemp.Get('event_weights_names')
print event_syst_names.GetEntries()

for isys in range(event_syst_names.GetEntries()):
    print event_syst_names[isys].Print("")

