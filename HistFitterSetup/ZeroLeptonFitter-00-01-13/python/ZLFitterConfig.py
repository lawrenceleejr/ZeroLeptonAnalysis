#!/usr/bin/env python

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.Reset()
ROOT.gROOT.SetBatch(True)
ROOT.gSystem.Load("libSusyFitter.so")

from optparse import OptionParser
import sys, os, string, shutil, pickle, subprocess, copy
from YieldsTable import latexfitresults

from logger import Logger

ROOT.gROOT.LoadMacro("python/Functions.C")

class ZLFitterConfig:

    def __init__(self):

        self.log =  Logger("ZLFitterConfig")

        ##############################################
        # Fit config
        ##############################################

        # blinding
        self.blindSR = False
        self.blindCR = False
        self.blindVR = False
        self.useSignalInBlindedData = False

        #Run hypotests with also with up and down theor. uncert.? False: add uncert. as fit parameter
        self.fixSigXSec = True

        # only run nominal fit if fixSigXSec=True ?
        self.runOnlyNominalXSec = False

        # Use files split by nJet ?
        self.useFilteredNtuples = False

        ##############################################
        # Basic fit setup
        ##############################################

        # Use a shape factor when using shape fits?
        self.useShapeFactor = False

        # do shape fits
        self.useShapeFit = False

        #parameters for shape fits
        self.minbin      = 1000
        self.maxbin      = 2000
        self.nBins       = 5
        self.binVar      = "cuts"

        ##############################################
        # Sample Name
        ##############################################

        self.qcdSampleName = "Multijets"
        self.gammaSampleName = "GAMMAjets"
        self.zSampleName = "Zjets"
        self.wSampleName = "Wjets"
        self.topSampleName = "Top"
        self.dibosonSampleName = "Diboson"
        self.sampleNameList = []

        self.sampleNameList.append(self.qcdSampleName)
        self.sampleNameList.append(self.wSampleName)
        self.sampleNameList.append(self.zSampleName)
        self.sampleNameList.append(self.gammaSampleName)
        self.sampleNameList.append(self.topSampleName)
        self.sampleNameList.append(self.dibosonSampleName)

        ##############################################
        # Systematics
        ##############################################

        # Apply a user-defined error to the background and signal errors? (Useful if setting everything to MC pred)
        self.usePrecomputedError = True
        self.flatErrorSignal=0.0  #this number is only used for the signal, see TheoUncertainties.py for the background
        self.usePreComputedWGeneratorSys=False
        self.usePreComputedTopGeneratorSys=True
        self.usePreComputedTopFragmentationSys=True
        self.usePreComputedTopRadiationSys=False
        self.usePreComputedZGeneratorSys=True

#jet smearing
        self.useDDQCDsample = True

        # JES,JER,...
        self.useJETUncertainties = True

        # MET
        self.useMETUncertainties = True

        # Btag
        self.useBTagUncertainties = True

        # Leptons
        self.useLeptonUncertainties = True

        ##############################################
        # Kappa correction for gamma+jets
        ##############################################
        self.applyKappaCorrection = True

        ##############################################
        # Statistical error
        ##############################################

        # use stat uncertainties on MC - globally
        self.useStat = True

        # use MC stat per sample
        self.useStatPerSample = False
        self.statErrThreshold = 0.01

        ##############################################
        # Luminosity
        ##############################################

        self.luminosity = 13.28 # 2.674#unit is fb-1
        self.luminosityEr = 0.029 # style the run1 error ####################

        ##############################################
        # samples
        ##############################################

        self.useMCQCDsample =True
        self.useDIBOSONsample = True

        # QCD weight- one number per jet multiplicity starting with the monojet channel
        self.qcdWeightList = [0.006727*float(self.luminosity)]*6

        ##############################################
        # Signal and control region
        ##############################################

        self.doSetNormRegion=True

        self.SRName = "SR"

        # list of constraining regions
        self.constrainingRegionsList = []
        self.constrainingRegionsList += ["CRT","CRW"]
        #self.constrainingRegionsList += ["CRTZL","CRW","CRT"]
        # self.constrainingRegionsList += ["CRZ"]
        self.constrainingRegionsList += ["CRY"]
        self.constrainingRegionsList += ["CRQ"]
        # self.constrainingRegionsList += ["CRYQ"]


        # list of validation regions
        self.validationRegionsList = []


        # # # self.validationRegionsList+=["VRYf"]
        self.validationRegionsList += ["VRZ","VRW","VRT"]
#        self.validationRegionsList += ["CRZVL"]
        self.validationRegionsList += ["VRZa","VRWa","VRTa"]
        self.validationRegionsList += ["VRZb","VRWb","VRTb"]
        self.validationRegionsList += ["VRZc","VRZca"]#,"VRQ2"]#,"VRQ3","VRQ4"]

        # # # self.validationRegionsList +=["VRZf"]

        # # # self.validationRegionsList+=["VRWf","VRTf"]
        # # # self.validationRegionsList+=["VRWM","VRTM"]
        # # # self.validationRegionsList+=["VRWMf","VRTMf"]
        # # # ##self.validationRegionsList+=["VRWTplus","VRWTminus"]
        # # # ##self.validationRegionsList+=["VRWTfplus","VRWTfminus"]
        # # # ##self.validationRegionsList+=["VRT2L"]
        # self.validationRegionsList += ["CRQ"]  #CRQ are temporary added as validation
        self.validationRegionsList+=["VRQ","VRQa","VRQb","VRQc"]#,"VRQ2"]#,"VRQ3","VRQ4"]

        self.datadriven = None
        self.writeXML = None
        self.useSplittedNtuples = False

        self.Print()

        return

    def getSampleColor(self,sample):
        if sample == self.topSampleName:         return ROOT.kGreen-9
        if sample == self.wSampleName:       return ROOT.kAzure - 4
        if sample == self.zSampleName:       return ROOT.kBlue + 3
        if sample == self.qcdSampleName:   return ROOT.kOrange
        if sample == self.gammaSampleName:   return ROOT.kYellow
        if sample == self.dibosonSampleName:     return ROOT.kPink-4#ROOT.kRed + 3
        return 1

    def getSampleNiceName(self,sample):
        if sample == self.topSampleName:  return "Top"
        if sample == self.wSampleName:       return "W+jets"
        if sample == self.zSampleName:       return "Z+jets"
        if sample == self.qcdSampleName:   return "Multijet"
        if sample == self.gammaSampleName:   return "GAMMA+jets"
        if sample == self.dibosonSampleName:     return "Diboson"
        return "Unknown"

    def allRegionsList(self):
        allRegionsList = self.constrainingRegionsList+self.validationRegionsList+[self.SRName]
        return allRegionsList

    def Print(self):
        self.log.info("blindSR = %s" % self.blindSR)
        self.log.info("blindCR = %s" % self.blindCR)
        self.log.info("blindVR = %s" % self.blindVR)
        self.log.info("useFilteredNtuples = {0}".format(self.useFilteredNtuples))
        self.log.info("useSignalInBlindedData %s" % self.useSignalInBlindedData)
        self.log.info("fixSigXSec  = %s" % self.fixSigXSec )
        self.log.info("runOnlyNominalXSec  = %s" % self.runOnlyNominalXSec )
        self.log.info("useShapeFactor  = %s" % self.useShapeFactor )
        self.log.info("useShapeFit  = %s" % self.useShapeFit )
        self.log.info("minbin  = %s" % self.minbin )
        self.log.info("maxbin  = %s" % self.maxbin )
        self.log.info("nBins  = %s" % self.nBins )
        self.log.info("binVar  = %s" % self.binVar )
        self.log.info("usePrecomputedError  = %s" % self.usePrecomputedError )
        self.log.info("flatErrorSignal = %s" % self.flatErrorSignal)
        self.log.info("useStat  = %s" % self.useStat )
        self.log.info("useStatPerSample  = %s" % self.useStatPerSample )
        self.log.info("statErrThreshold  = %s" % self.statErrThreshold )
        self.log.info("luminosity  = %s" % self.luminosity )
        self.log.info("luminosityEr  = %s" % self.luminosityEr )
        self.log.info("useDIBOSONsample  = %s" % self.useDIBOSONsample )
        self.log.info("SRName  = %s" % self.SRName )
        self.log.info("ConstrainingRegionsList  = %s" %  self.constrainingRegionsList )
        self.log.info("ValidationRegionsList  = %s" %  self.validationRegionsList )
        self.log.info("allRegionsList  = %s" %  self.allRegionsList() )

        return

