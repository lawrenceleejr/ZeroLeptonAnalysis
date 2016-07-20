#!/usr/bin/env python

import os, sys, ROOT
#from ROOT import TTree, TString

ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

def treedescription():
  filename = "/imports/rcs5_data/larryl/ZeroLeptonAnalysis/HistFitterSetup/ZeroLeptonFitter-00-01-11-branch/macros/contourplot/Outputs/11.3ifb_RJigsaw/GG_direct/GG_direct_SRJigsawSRG1a_fixSigXSecNominal__1_harvest_list"
  description = "expectedUpperLimitMinus1Sig/F:upperLimitEstimatedError/F:fitstatus/F:p0d2s/F:p0u2s/F:m12/F:CLsexp/F:sigma1/F:failedfit/F:expectedUpperLimitPlus2Sig/F:nofit/F:nexp/F:sigma0/F:clsd2s/F:m0/F:expectedUpperLimit/F:failedstatus/F:xsec/F:covqual/F:upperLimit/F:p0d1s/F:clsd1s/F:failedp0/F:failedcov/F:p0exp/F:p1/F:p0u1s/F:excludedXsec/F:p0/F:clsu1s/F:clsu2s/F:expectedUpperLimitMinus2Sig/F:expectedUpperLimitPlus1Sig/F:seed/F:mode/F:fID/F:dodgycov/F:CLs/F"
  return filename, description

def harvesttree(textfile='/imports/rcs5_data/larryl/ZeroLeptonAnalysis/HistFitterSetup/ZeroLeptonFitter-00-01-11-branch/macros/contourplot/Outputs/11.3ifb_RJigsaw/GG_direct/GG_direct_SRJigsawSRG1a_fixSigXSecNominal__1_harvest_list'):
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

