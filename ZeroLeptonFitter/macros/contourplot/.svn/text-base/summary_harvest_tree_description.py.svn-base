#!/usr/bin/env python

import os, sys, ROOT
from ROOT import TTree, TString

def treedescription():
  filename = '/afs/cern.ch/work/n/nakahama/Run2/ZL/ZL_trunk_new/macros/contourplot/ZL_SROpt_nJets-6_dPhi-0.4_Ap-0.04_Meff-1800_metomeffNj-0.2_pt12-200_pt34-150_Gtt_1300_100_Output_fixSigXSecNominal_hypotest__1_harvest_list'
  description = "p0:p1:CLs:mode:nexp:seed:CLsexp:fID:sigma0:sigma1:clsu1s:clsd1s:clsu2s:clsd2s:p0exp:p0u1s:p0d1s:p0u2s:p0d2s:upperLimit:upperLimitEstimatedError:expectedUpperLimit:expectedUpperLimitPlus1Sig:expectedUpperLimitPlus2Sig:expectedUpperLimitMinus1Sig:expectedUpperLimitMinus2Sig:xsec:excludedXsec:covqual:dodgycov:failedcov:failedfit:failedp0:failedstatus:fitstatus:m0:m12:nofit"
  return filename, description

def harvesttree(textfile=''):
  filename, description=treedescription()
  tree = TTree('tree','data from ascii file')
  if len(textfile)>0:
    nlines = tree.ReadFile(textfile,description)
  elif len(filename)>0:
    nlines = tree.ReadFile(filename,description)
  else:
    print 'WARNING: file name is empty. No tree is read.'

  tree.SetMarkerStyle(8)
  tree.SetMarkerSize(0.5)

  return tree


