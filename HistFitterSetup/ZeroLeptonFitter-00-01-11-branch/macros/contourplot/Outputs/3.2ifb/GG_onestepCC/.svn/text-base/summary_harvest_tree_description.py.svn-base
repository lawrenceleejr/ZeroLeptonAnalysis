#!/usr/bin/env python

import os, sys, ROOT
#from ROOT import TTree, TString

ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

def treedescription():
  filename = "/data/data1/zp/shadachi/analysis/HistFitter/ZeroLeptonFitter/00-01-11-08_2/ZeroLeptonFitter/macros/contourplot/Outputs/3.2ifb/GG_onestepCC/GG_onestepCC_SR6jt_fixSigXSecDown__mlspNE60_harvest_list"
  description = "expectedUpperLimitMinus1Sig/F:upperLimitEstimatedError/F:mgluino/F:fitstatus/F:p0d2s/F:p0u2s/F:seed/F:CLsexp/F:sigma1/F:failedfit/F:mlsp/F:expectedUpperLimitPlus2Sig/F:nofit/F:nexp/F:sigma0/F:clsd2s/F:expectedUpperLimit/F:failedstatus/F:xsec/F:covqual/F:upperLimit/F:p0d1s/F:mchargino/F:clsd1s/F:failedp0/F:failedcov/F:p0exp/F:p1/F:p0u1s/F:excludedXsec/F:p0/F:clsu1s/F:clsu2s/F:expectedUpperLimitMinus2Sig/F:expectedUpperLimitPlus1Sig/F:mode/F:fID/C:dodgycov/F:CLs/F"
  return filename, description

def harvesttree(textfile='/data/data1/zp/shadachi/analysis/HistFitter/ZeroLeptonFitter/00-01-11-08_2/ZeroLeptonFitter/macros/contourplot/Outputs/3.2ifb/GG_onestepCC/GG_onestepCC_SR6jt_fixSigXSecDown__mlspNE60_harvest_list'):
  filename, description=treedescription()
  tree = ROOT.TTree('tree','data from ascii file')
  if len(textfile)>0:
    nlines = tree.ReadFile(textfile,description)
  elif len(filename)>0:
    nlines = tree.ReadFile(filename,description)
  else:
    print 'WARNING: file name is empty. No tree is read.'

  tree.SetMarkerStyle(8)
  tree.SetMarkerSize(0.5)

  return tree

