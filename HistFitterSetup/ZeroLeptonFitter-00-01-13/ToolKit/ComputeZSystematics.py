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
from ROOT import *

from Utils import *
from ChannelConfig import *
from ChannelsDict import *
from ZLFitterConfig import *

from optparse import OptionParser

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
# Some global variables
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#


weightStr="(normWeight*genWeight)"

gammaSherpaFile=TFile.Open("/afs/cern.ch/user/y/yamanaka/public/v02/GAMMAMassiveCB_TRUTH_filtered.root")
treeGammaSherpa_CRY=gammaSherpaFile.Get("GAMMA_CRY_TRUTH")

gammaMadGraphFile=TFile.Open("/afs/cern.ch/user/y/yamanaka/public/v02/GAMMAMassiveCB_TRUTH_filtered.root")
treeGammaMadGraph_CRY=gammaMadGraphFile.Get("GAMMA_CRY_TRUTH_MadGraph")

zSherpaFile=TFile.Open("root://eosatlas.cern.ch//eos/atlas/user/l/lduflot/atlasreadable/ZeroLeptonRun2-00-00-57/filtered/ZMassiveCB.root")
treeZSherpa_SR=zSherpaFile.Get("Z_SRAll")

zMadGraphFile=TFile.Open("root://eosatlas.cern.ch//eos/atlas/user/l/lduflot/atlasreadable/ZeroLeptonRun2-00-00-57/filtered/ZMadgraphPythia8.root")
treeZMadGraph_SR=zMadGraphFile.Get("Z_SRAll_Madgraph")


h=TH1F("h","h",10,0,10)

for anaName in sorted(finalChannelsDict.keys()):
    #anaName="SR2jl"


    cuts=finalChannelsDict[anaName].getCutsDict()

    cuts_CRY=cuts["CRY"]
    cuts_CRY_truth=cuts_CRY.replace("&& phTight==1 ","")
    cuts_SR=cuts["SR"]
#    print cuts_CRY_truth




    treeGammaSherpa_CRY.Draw("1>>h","("+cuts_CRY_truth+")*"+weightStr)
    nbGammaSherpaCRY=h.Integral()


    treeGammaMadGraph_CRY.Draw("1>>h","("+cuts_CRY_truth+")*"+weightStr)
    nbGammaMadGraphCRY=h.Integral()


    treeZSherpa_SR.Draw("1>>h","("+cuts_SR+")*"+weightStr)
    nbZSherpaSR=h.Integral()


    treeZMadGraph_SR.Draw("1>>h","("+cuts_SR+")*"+weightStr)
    nbZMadGraphSR=h.Integral()


    TFSherpa=nbZSherpaSR/nbGammaSherpaCRY
    TFMadGraph=nbZMadGraphSR/nbGammaMadGraphCRY

    #print nbGammaSherpaCRY,nbGammaMadGraphCRY
    #print nbZSherpaSR*3200#,nbZMadGraphSR

    #print TFSherpa,TFMadGraph
    #print anaName, TFSherpa,TFMadGraph,TFMadGraph/TFSherpa-1
    print "zTheoSysGeneratorDict[(\""+anaName+"\",\"SR\")] =",TFMadGraph/TFSherpa-1
