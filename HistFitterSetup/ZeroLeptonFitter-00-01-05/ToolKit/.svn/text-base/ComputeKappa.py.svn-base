#!/usr/bin/env python
"""
This python script is plotting event counts in all SRs

Usage:
python ToolKit/MakePullPlots.py
python ToolKit/PlotSRs.py
"""
import sys
import math
import copy
import pickle
import ROOT
import os
from ROOT import *

ROOT.gROOT.SetBatch(True) # Turn off online histogram drawing



channelName="VLForKappa"

########################################################



try:
    fYield = open('yield_%s_all.pickle' % channelName,'r')
except:
    print "Could not open yield_%s_all.pickl" % channelName
    sys.exit()

theMap = pickle.load(fYield)


###########################################
# Look for CRY and VRZ index 
###########################################

CRYIndex=-1
VRZIndex=-1
for iname,name in enumerate(theMap["names"]):
    if name=="CRY_cuts":
        CRYIndex=iname
    if name=="VRZ_cuts":
        VRZIndex=iname
print CRYIndex
print VRZIndex



###########################################
# Get the number of events
###########################################

#print theMap

#Number of predicted gamma events in CRY
print theMap["MC_exp_events_GAMMAjets"]
NMCGammaInCRY=theMap["MC_exp_events_GAMMAjets"][CRYIndex]

#Number of predicted Z events in VRZ
NMCZInVRZ=theMap["MC_exp_events_Zjets"][VRZIndex]


#Number of events in data
NDataInCRY=theMap["nobs"][CRYIndex]
NDataInVRZ=theMap["nobs"][VRZIndex]

#Number of background events (different from gamma+jets) in CRY
NBkgInCRY=theMap["TOTAL_FITTED_bkg_events"][CRYIndex]-theMap["Fitted_events_GAMMAjets"][CRYIndex]
#Number of background events (different from Z+jets) in VRZ
NBkgInVRZ=theMap["TOTAL_FITTED_bkg_events"][VRZIndex]-theMap["Fitted_events_Zjets"][VRZIndex]

#Number of fitted gamma events in CRY
NFittedGammaInCRY=theMap["Fitted_events_GAMMAjets"][CRYIndex]

#Number of fitted Z events in VRZ
NFittedZInVRZ=theMap["Fitted_events_Zjets"][VRZIndex]



if NFittedZInVRZ!=NMCZInVRZ:
    print "=============================================="
    print "WARNING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print "WARNING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print "WARNING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print "WARNING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print "The number of fitted and predicted are not the same for Z+jets"
    print "This is suspicious!!!!"
    print "Please check that VRZ is set a validation region in fit"
    print "=============================================="

if NMCGammaInCRY!=NFittedGammaInCRY:
    print "=============================================="
    print "WARNING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print "WARNING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print "WARNING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print "WARNING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print "The number of fitted and predicted are not the same for gamma+jets"
    print "This is suspicious!!!!"
    print "Please check that CRY is set a validation region in fit"
    print "=============================================="
    

kappa=(NDataInCRY-NBkgInCRY)/NMCGammaInCRY*NMCZInVRZ/(NDataInVRZ-NBkgInVRZ)

print "=============================================="
print "Nb of events in CRY:",NDataInCRY
print "Nb of events in VRZ:",NDataInVRZ
print "Nb of MC expected gamma events in CRY after background substraction:",NMCGammaInCRY
print "Nb of MC expected Zll events in VRZ after background substraction:",NMCZInVRZ
print "Nb of bkg events other than gamma events in CRY:",NBkgInCRY
print "Nb of bkg events other than Z in VRZ:",NBkgInVRZ
print "===> kappa: ",kappa
