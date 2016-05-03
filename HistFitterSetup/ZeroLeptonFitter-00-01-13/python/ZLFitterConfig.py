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

        self.log = Logger("ZLFitterConfig")
        
        ##############################################
        # Fit config
        ##############################################

        # blinding
        self.blindSR = True
        self.blindCR = True
        self.blindVR = True
        self.useSignalInBlindedData = False

        #Run hypotests with also with up and down theor. uncert.? False: add uncert. as fit parameter
        self.fixSigXSec = True           

        # only run nominal fit if fixSigXSec=True ?
        self.runOnlyNominalXSec = False

        # Use files split by nJet ?
        self.useSplittedNtuples = False

        self.writeXML = False

        ##############################################
        # Basic fit setup
        ##############################################

        # Use a shape factor when using shape fits?
        self.useShapeFactor = False

        # do shape fits
        self.useShapeFit = False
        
        #do data-driven BG estimation
        self.datadriven = False
        self.meffABCD = True
        self.meffABCD = self.datadriven and self.meffABCD

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
        self.zLooseSampleName = "ZjetsL"
        self.zVeryLooseSampleName = "ZjetsVL"
        self.wSampleName = "Wjets"
        self.wLooseSampleName = "WjetsL"
        self.wVeryLooseSampleName = "WjetsVL"
        self.topSampleName = "Top"
        self.topLooseSampleName = "TopL"
        self.topVeryLooseSampleName = "TopVL"
        self.dibosonSampleName = "Diboson"

        self.CRYtmtASampleName = "GAMMA_CRYtmtA"
        self.CRYtmlASampleName = "GAMMA_CRYtmlA"
        self.CRYlmtASampleName = "GAMMA_CRYlmtA"
        self.CRYlmlASampleName = "GAMMA_CRYlmlA"
        self.CRYLSampleName = "GAMMA_CRYL"
        self.CRWLSampleName = "W_CRWL"
        self.CRWVLSampleName = "W_CRWVL"
        self.CRZllVLSampleName = "Z_CRZllVL"
        self.zSRSampleName = "Z_SR"
        self.VRZlmlASampleName = "Z_VRZlmlA"
        self.VRZLSampleName = "Z_VRZL"
        self.VRZVLSampleName = "Z_VRZVL"


        self.datadrivenSampleNameList = []
        self.sampleNameList = []        
        self.sampleNameList.append(self.qcdSampleName)
        self.sampleNameList.append(self.wSampleName)
        self.sampleNameList.append(self.zSampleName)
        self.sampleNameList.append(self.gammaSampleName)
        self.sampleNameList.append(self.topSampleName)
        self.sampleNameList.append(self.dibosonSampleName)
        self.datadrivenSampleNameList = []
        if self.datadriven:
            self.sampleNameList.append(self.topLooseSampleName)
            self.sampleNameList.append(self.topVeryLooseSampleName)            
            self.sampleNameList.append(self.wLooseSampleName)
            self.sampleNameList.append(self.wVeryLooseSampleName)
            self.sampleNameList.append(self.zLooseSampleName)
            self.sampleNameList.append(self.zVeryLooseSampleName)
            self.sampleNameList.append(self.CRYtmtASampleName)
            self.sampleNameList.append(self.CRYtmlASampleName)
            self.sampleNameList.append(self.CRYlmtASampleName)
            self.sampleNameList.append(self.CRYlmlASampleName)
            self.sampleNameList.append(self.CRYLSampleName)
            self.sampleNameList.append(self.CRWLSampleName)
            self.sampleNameList.append(self.CRWVLSampleName)
            self.sampleNameList.append(self.CRZllVLSampleName)
            self.sampleNameList.append(self.zSRSampleName)
            self.sampleNameList.append(self.VRZlmlASampleName)
            self.sampleNameList.append(self.VRZLSampleName)
            self.sampleNameList.append(self.VRZVLSampleName)

            self.datadrivenSampleNameList.append(self.topLooseSampleName)
            self.datadrivenSampleNameList.append(self.topVeryLooseSampleName)            
            self.datadrivenSampleNameList.append(self.wLooseSampleName)
            self.datadrivenSampleNameList.append(self.wVeryLooseSampleName)
            self.datadrivenSampleNameList.append(self.zLooseSampleName)
            self.datadrivenSampleNameList.append(self.zVeryLooseSampleName)
            self.datadrivenSampleNameList.append(self.CRYtmtASampleName)
            self.datadrivenSampleNameList.append(self.CRYtmlASampleName)
            self.datadrivenSampleNameList.append(self.CRYlmtASampleName)
            self.datadrivenSampleNameList.append(self.CRYlmlASampleName)
            self.datadrivenSampleNameList.append(self.CRYLSampleName)
            self.datadrivenSampleNameList.append(self.CRWLSampleName)
            self.datadrivenSampleNameList.append(self.CRWVLSampleName)
            self.datadrivenSampleNameList.append(self.CRZllVLSampleName)
            self.datadrivenSampleNameList.append(self.zSRSampleName)
            self.datadrivenSampleNameList.append(self.VRZlmlASampleName)
            self.datadrivenSampleNameList.append(self.VRZLSampleName)
            self.datadrivenSampleNameList.append(self.VRZVLSampleName)


        ##############################################
        # Systematics
        ##############################################

        # Apply a user-defined error to the background and signal errors? (Useful if setting everything to MC pred)
        # If the background settings are False, much slower MC-to-MC comparisons will be used!
        self.usePrecomputedError = True
        self.flatErrorSignal = 0.0  # this number is only used for the signal, see TheoUncertainties.py for the background
        
        # The individual settings must can also be controlled. Make sure the analysis script is sane.
        self.usePrecomputedWGeneratorSys = False
        self.usePrecomputedTopGeneratorSys = False
        self.usePrecomputedTopFragmentationSys = False
        self.usePrecomputedZGeneratorSys = False

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

        self.luminosity = 10#unit is fb-1
        self.luminosityEr = 0.05 # style the run1 error

        ##############################################
        # samples
        ##############################################

        self.useDDQCDsample =False
        self.useMCQCDsample =False
        self.useDIBOSONsample = True

        # QCD weight- one number per jet multiplicity starting with the monojet channel
        self.qcdWeightList = [1]*6

        ##############################################
        # Signal and control region
        ##############################################

        self.doSetNormRegion=True

        self.SRName = "SR"
        
        # list of constraining regions
        self.datadrivenRegionsList = []
        self.datadrivenValidationRegionsList = []
        self.constrainingRegionsList = []
        self.constrainingRegionsList += ["CRT","CRW"] 
        #self.constrainingRegionsList += ["CRQ"] 
        if not self.datadriven:
            self.constrainingRegionsList += ["CRY"]
        else:
            if not self.meffABCD:
                #CRY with the same cut as SR
                self.constrainingRegionsList += ["CRYtmtA"]
                self.datadrivenRegionsList += ["CRYtmtA"]
                #Loose Control region
                self.constrainingRegionsList += ["CRYlmlA","CRYL","CRWL","CRTL","CRZllL"]
                self.datadrivenRegionsList += ["CRYlmlA","CRWL","CRYL"]
                #Very Loose Control region
                self.constrainingRegionsList += ["CRWVL","CRZllVL","CRTVL"]
                self.datadrivenRegionsList += ["CRWVL","CRZllVL"]
            else:
                self.constrainingRegionsList += ["CRYtmlA","CRYlmlA","CRYlmtA"]
                self.datadrivenRegionsList += ["CRYtmlA","CRYlmlA","CRYlmtA"]
                self.constrainingRegionsList += ["CRWL","CRYL","CRTL","CRZllL"]
                self.datadrivenRegionsList += ["CRWL","CRYL"]
                self.constrainingRegionsList += ["CRWVL","CRZllVL","CRTVL"]
                self.datadrivenRegionsList += ["CRWVL","CRZllVL"]


        # list of validation regions
        self.validationRegionsList = []

        #self.validationRegionsList+=["VRYf"]
        self.validationRegionsList += ["VRZ"]

        self.validationRegionsList +=["VRZf"]
        self.validationRegionsList+=["VRWf","VRTf"]
        self.validationRegionsList+=["VRWM","VRTM"]
        self.validationRegionsList+=["VRWMf","VRTMf"]
        ##self.validationRegionsList+=["VRWTplus","VRWTminus"]
        ##self.validationRegionsList+=["VRWTfplus","VRWTfminus"]
        ##self.validationRegionsList+=["VRT2L"] 
        #self.validationRegionsList += ["CRQ"]  #CRQ are temporary added as validation     
        self.validationRegionsList+=["VRQ1","VRQ2","VRQ3","VRQ4"] 
        
        if self.datadriven:
            self.datadrivenValidationRegionsList += ["VRZf"]
            self.validationRegionsList += ["VRZL"]
            self.datadrivenValidationRegionsList += ["VRZL"]
            #Very Loose Control region
            self.validationRegionsList += ["VRZVL"]
            self.datadrivenValidationRegionsList += ["VRZVL"]
            if not self.meffABCD:
                #VRW with the same cut as SR
                self.validationRegionsList += ["VRWtmtA"]
                self.datadrivenValidationRegionsList += ["VRWtmtA"]
            else:
                self.validationRegionsList += ["CRYtmtA","VRWtmtA","VRWtmlA","VRWlmtA","VRWlmlA"]
                self.datadrivenValidationRegionsList += ["CRYtmtA","VRWtmtA","VRWtmlA","VRWlmtA","VRWlmlA"]
                self.validationRegionsList += ["VRZlmlA","VRZlmtA","VRZtmlA"]
                self.datadrivenValidationRegionsList += ["VRZlmlA","VRZlmtA","VRZtmlA"]

        self.Print()

        return

    def getSampleColor(self,sample):
        if sample == self.topSampleName:         return ROOT.kGreen-9
        if sample == self.wSampleName:       return ROOT.kAzure - 4
        if sample == self.zSampleName:       return ROOT.kOrange - 4
        if sample == self.qcdSampleName:   return ROOT.kBlue + 3
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
        return self.constrainingRegionsList+self.validationRegionsList+[self.SRName]
    def allDataDrivenRegionsList(self):
        return self.datadrivenRegionsList+self.datadrivenValidationRegionsList+[self.SRName]

    def Print(self):
        self.log.info("blindSR = %s" % self.blindSR)
        self.log.info("blindCR = %s" % self.blindCR)
        self.log.info("blindVR = %s" % self.blindVR)
        self.log.info("useSplittedNtuples = {0}".format(self.useSplittedNtuples))
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
        self.log.info("useMCQCDsample  = %s" % self.useMCQCDsample )
        self.log.info("useDDQCDsample  = %s" % self.useDDQCDsample )
        self.log.info("useDIBOSONsample  = %s" % self.useDIBOSONsample )
        self.log.info("SRName  = %s" % self.SRName )
        self.log.info("ConstrainingRegionsList  = %s" %  self.constrainingRegionsList ) 
        self.log.info("ValidationRegionsList  = %s" %  self.validationRegionsList ) 
        self.log.info("allRegionsList  = %s" %  self.allRegionsList() ) 
        self.log.info("DataDrivenRegionsList  = %s" %  self.datadrivenRegionsList ) 
        self.log.info("DataDrivenValidationRegionsList  = %s" %  self.datadrivenValidationRegionsList ) 

        return
        
