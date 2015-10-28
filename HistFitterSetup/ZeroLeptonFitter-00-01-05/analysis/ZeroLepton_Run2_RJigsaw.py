###############################################################
##
## Run 2 0-lepton analysis
##
################################################################

########################################
# Imports
########################################

# python import
import socket
import os, sys, pickle, pprint, string, time, argparse

# root import
from configManager import configMgr
from ROOT import kBlack, kWhite, kGray, kRed, kPink, kMagenta, kViolet, kBlue, kAzure, kCyan, kTeal, kGreen, kSpring, kYellow, kOrange
from ROOT import TMath
from configWriter import fitConfig, Measurement, Channel, Sample
from logger import Logger
from systematic import Systematic
from math import sqrt
from copy import deepcopy

# ZL import

from Utils import *
from ChannelConfig import *
from allChannelsDict import *
from ZLFitterConfig import *

########################################
# Log
########################################

log = Logger("ZeroLeptonFitter")

log.info("ZeroLeptonFitter says hi!")

########################################
# Config Managers
########################################

#ZeroLepton
zlFitterConfig = ZLFitterConfig()

# LL - Reinserting deprecated flat error
flatError = 0.2

#HisftFitter


configMgr.blindSR = zlFitterConfig.blindSR              
configMgr.blindCR = zlFitterConfig.blindCR              
configMgr.blindVR = zlFitterConfig.blindVR              
configMgr.useSignalInBlindedData = zlFitterConfig.useSignalInBlindedData

configMgr.fixSigXSec = zlFitterConfig.fixSigXSec        
configMgr.runOnlyNominalXSec = zlFitterConfig.runOnlyNominalXSec 



#######################################################################
# Gets cuts
#######################################################################

print configMgr.cutsDict



allChannelsDict[pickedSRs[0]].Print()#getCutsDict()
configMgr.cutsDict = allChannelsDict[pickedSRs[0]].getCutsDict()
anaName      = allChannelsDict[pickedSRs[0]].name





#######################################################################
# Signal configutation
#######################################################################

# grid, with a default point and a default name
grid = "SM_GG_direct"
gridTreeName = grid 
allpoints = ["1200_0"]


#######################################################################
# Commandline args
#######################################################################

# parse configMgr.userArg to overwrite options above if needed
if configMgr.userArg != "":
    log.info("Found user args %s" % configMgr.userArg)

    # Note: these options should NOT have defaults! Else they will always get that value; we want them to be undefined if not specified
    parser = argparse.ArgumentParser()
    parser.add_argument("-C", "--useBackgroundCache", action="store_true", default=False)

    args = parser.parse_args(configMgr.userArg.split())

    log.info("Parsed user args %s" % str(args))
   
    if args.useBackgroundCache:
        log.info("Setting useBackgroundCache=True")

        # note: we pass the filename later, depending on SR
        configMgr.useCacheToTreeFallback = True

    log.info("Waiting 5 seconds to review user args")
    wait(5)

########################################################################
# Options
########################################################################

# sigSamples is set by the "-g" HistFitter option    
try:
    sigSamples
except NameError:
    sigSamples = None
    
if sigSamples != None:
    if sigSamples[0].find("grid") >= 0: # first entry allowed to specify a grid name
        grid = sigSamples[0].replace("grid", "")
        gridTreeName = grid
        allpoints = sigSamples[1:]
    else:
        allpoints = sigSamples

# rename the default option for the sq-sq compressed points
if grid == "SM_SS_direct_compressedPoints":
    gridTreeName = "SM_SS_direct"

########################################################################
# HistFitter options
########################################################################

# No input signal for discovery and bkg fit
# allpoints changed for naming of output files
if myFitType == FitType.Discovery and  not zlFitterConfig.useSignalInBlindedData:
    allpoints = ["Discovery"]
    grid = ""
    gridTreeName = ""

if myFitType == FitType.Background:
    allpoints = ["Background"]
    grid = ""
    gridTreeName = ""


# Location of the ntuples ("Light" has the baseline cut applied already, preferred for speed)
###INPUTDIR = "/afs/cern.ch/atlas/groups/susy/0lepton/ZeroLeptonFitter/ZeroLepton-00-00-53_Light/"
#INPUTDIR = "/afs/cern.ch/atlas/groups/susy/0lepton/ZeroLeptonFitter/ZeroLeptonRun2-00-00-19/13TeV/"
#INPUTDIR = "/afs/cern.ch/user/l/leejr/work/public/Merged0LNtuples/082715a_40GeVTest/"
#INPUTDIR = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v44/"

INPUTDIR = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v51_Oct17_pT50/"
INPUTDIR_SIGNAL = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v51_SIG_pT50/"
INPUTDIR_DATA = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v53_Data_pT50/"


# Location of the signal inputs (default is the normal INPUTDIR)
# INPUTDIR_SIGNAL = INPUTDIR 
    

#######################################################################
# Parameters for hypothesis test
#######################################################################

#configMgr.nTOYs = 5000      # number of toys when doing frequentist calculator
configMgr.nTOYs = 10      # number of toys when doing frequentist calculator
configMgr.doExclusion = False
if myFitType == FitType.Exclusion:
    configMgr.doExclusion = True 
configMgr.calculatorType = 2 # 2=asymptotic calculator, 0=frequentist calculator
configMgr.testStatType = 3   # 3=one-sided profile likelihood test statistic (LHC default)
configMgr.nPoints = 20       # number of values scanned of signal-strength for upper-limit determination of signal strength.

if configMgr.calculatorType == 2:
    # configMgr.nPoints = 30 
    configMgr.nPoints = 5 


#######################################################################------
# Now we start to build the data model
#######################################################################------

# Scaling calculated by outputLumi / inputLumi
configMgr.inputLumi = 1.0 ##0.001 # Luminosity of input TTree after weighting
configMgr.outputLumi = zlFitterConfig.luminosity # Luminosity required for output histograms
configMgr.setLumiUnits("fb-1")

# Set the files to read from
bgdFiles = []
topFiles = []
qcdFiles = []
dibosonFiles = []
dataFiles = []
dataCRWTFiles = []
wFiles = []
zFiles = []
gammaFiles = []

if configMgr.readFromTree:

    #QCD
    qcdFiles.append(INPUTDIR+"/BKG/QCD.root")

    #Diboson
    dibosonFiles.append(INPUTDIR+"/BKG/Diboson.root")

    #Top
    topFiles.append(INPUTDIR+"/BKG/Top.root")      
            
    #W
    wFiles.append(INPUTDIR+"/BKG/Wjets.root")

    #Z
    zFiles.append(INPUTDIR+"/BKG/Zjets.root")

    #gamma
    gammaFiles.append(INPUTDIR+"/GammaJet.root")
    
    #data
    dataFiles.append(INPUTDIR_DATA+"/Data_Oct10.root")
    dataCRWTFiles.append(INPUTDIR_DATA+"/Data_Oct10.root")
    dataCRWTFiles.append(INPUTDIR_DATA+"/Data_Oct10.root")

    log.info("Using the following inputs:")
    log.info("topFiles = %s" % topFiles) 
    log.info("qcdFiles = %s" % qcdFiles)
    log.info("dibosonFiles = %s" % dibosonFiles)
    log.info("dataFiles = %s" % dataFiles)
    log.info("dataCRWTFiles = %s" % dataCRWTFiles)
    log.info("wFiles = %s" % wFiles)
    log.info("zFiles = %s" % zFiles)
    log.info("gammaFiles = %s" % gammaFiles)

     
# Tuples of nominal weights
#weights = ["genWeight", "pileupWeight", "normWeight"]
weights = ["weight"]

configMgr.weights = weights

#######################################################################
# Dump our options to user 
#######################################################################

if zlFitterConfig.useStat and zlFitterConfig.useStatPerSample:
    log.fatal("You have turned on both useStat and useStatPerSample: not possible!")
    sys.exit()

log.info("Will run with the following settings:")
log.info("INPUTDIR = %s" % INPUTDIR)
if INPUTDIR != INPUTDIR_SIGNAL:
    log.info("INPUTDIR_SIGNAL = %s" % INPUTDIR_SIGNAL)
log.info("myFitType = %s" % myFitType)
log.info("doValidation = %s" % doValidation)
log.info("configMgr.useCacheToTreeFallback = %s" % configMgr.useCacheToTreeFallback)
log.info("configMgr.fixSigXSec = %s" % configMgr.fixSigXSec)
log.info("configMgr.runOnlyNominalXSec = %s" % configMgr.runOnlyNominalXSec)
log.info("grid = %s" % grid)
log.info("gridTreeName = %s" % gridTreeName)

log.info("allpoints = %s" % allpoints)

log.info("Full cutsDict can be printed with -L DEBUG")
log.debug(pprint.pformat(configMgr.cutsDict, width=60))

#log.info("Wait 3 seconds for you to panic if these settings are wrong")
#wait(3)
#log.info("No panicking detected, continuing...")





#######################################################################
# List of samples and their plotting colours
#######################################################################

#--------------------------
# Diboson
#--------------------------
# NB: note that theoSys on diboson are applied on the level of the region definitions,
# since we have one for the SR and one for the CR 
dibosonSample = Sample("Diboson", kRed+3)
dibosonSample.setTreeName("Diboson_SRAll")
dibosonSample.setFileList(dibosonFiles)
dibosonSample.setStatConfig(zlFitterConfig.useStat)

#--------------------------             
# QCD
#--------------------------
qcdSample = Sample("Multijets", kOrange+2)
qcdSample.setTreeName("QCD_SRAll")
qcdSample.setNormFactor("mu_Multijets", 1., 0., 500.)
qcdSample.setFileList(qcdFiles)
qcdSample.setStatConfig(zlFitterConfig.useStat)




qcdWeight=1
nJet=allChannelsDict[pickedSRs[0]].nJet
if nJet>0 and nJet<len(zlFitterConfig.qcdWeightList):
    qcdWeight=zlFitterConfig.qcdWeightList[nJet-1]/ (zlFitterConfig.luminosity*1000)
    qcdSample.addWeight(str(qcdWeight))
    for w in configMgr.weights:#ATT: there is a bug in HistFitter, I have to add the other weight by hand
        qcdSample.addWeight(w)

        
#--------------------------
# Top
#--------------------------
topSample = Sample("Top", kGreen-9)
topSample.setTreeName("Top_SRAll")
topSample.setNormFactor("mu_Top", 1., 0., 500.)
topSample.setFileList(topFiles)
topSample.setStatConfig(zlFitterConfig.useStat) 


#--------------------------
# W 
#--------------------------
wSample = Sample("Wjets", kAzure+1)
wSample.setTreeName("W_SRAll")
wSample.setNormFactor("mu_W", 1., 0., 500.)
wSample.setFileList(wFiles)
wSample.setStatConfig(zlFitterConfig.useStat)


#--------------------------  
# Gamma
#--------------------------
gammaSample = Sample("GAMMAjets",kYellow)
gammaSample.setTreeName("GAMMA_SRAll")
gammaSample.setNormFactor("mu_Z",1.,0.,500.)
gammaSample.setFileList(gammaFiles)
gammaSample.setStatConfig(zlFitterConfig.useStat)

#--------------------------
# Z
#--------------------------
zSample = Sample("Zjets", kBlue)
zSample.setTreeName("Z_SRAll")
zSample.setNormFactor("mu_Z", 1., 0., 500.)
zSample.setFileList(zFiles)
zSample.setStatConfig(zlFitterConfig.useStat)

#--------------------------
# Data
#--------------------------

dataSample = Sample("Data", kBlack)
dataSample.setTreeName("Data_SRAll")
dataSample.setData()
dataSample.setFileList(dataFiles)

#######################################################################
# Shape Factor
#######################################################################
if zlFitterConfig.useShapeFit and zlFitterConfig.useShapeFactor:
    topSample.addShapeFactor("topShape")
    wSample.addShapeFactor("wShape")
    zSample.addShapeFactor("zShape")
    gammaSample.addShapeFactor("gammaShape")
    qcdSample.addShapeFactor("qcdShape")



#######################################################################
# Apply systematics
#######################################################################






#######################################################################
# Set up fit 
#######################################################################

# First define HistFactory attributes
prefix = "ZL"



if grid == "":
    configMgr.analysisName =  "%s_%s_%s" % (prefix, anaName, allpoints[0])
else:
    configMgr.analysisName =  "%s_%s_%s_%s" % (prefix, anaName, grid, allpoints[0])

# store everything in its own directory
configMgr.histCacheFile = "data/%s/%s.root" % (configMgr.analysisName, configMgr.analysisName)
configMgr.outputFileName = "results/%s/%s_Output.root " % (configMgr.analysisName, configMgr.analysisName)

# this is set using -u="-C" on the commandline
if configMgr.useCacheToTreeFallback:
    # The idea is the following: let the HistoPrepare be used, but use TreePrepare() internally
    # as fallback option. So we read the backgrounds from histograms, and for signal we
    # fall back to the tree. This saves a lot of time!

    # fallback cache file is the file normally created for backgrounds!

    # NOTE: should be identical to the normal filename (in the case grid == ""), or the file will not be found
    configMgr.histBackupCacheFile =  "data/ZL_%s_Background/ZL_%s_Background.root" % (anaName, anaName)
    configMgr.useHistBackupCacheFile = True

    log.info("setting configMgr.histBackupCacheFile to %s" % configMgr.histBackupCacheFile)


for point in allpoints:
    if point == "":
        continue
        
    # Fit config instance
    name = "Fit_%s_%s" % (grid, point)
    if grid == "SM_SS_direct_compressedPoints":
        name = "Fit_SM_SS_direct_%s" % (point)

    myFitConfig = configMgr.addFitConfig(name)
    myFitConfig.statErrThreshold = zlFitterConfig.statErrThreshold

    meas = myFitConfig.addMeasurement(name="NormalMeasurement", lumi=1.0, lumiErr=zlFitterConfig.luminosityEr)
    meas.addPOI("mu_SIG")

    #-------------------------------------------------
    # Fix parameters
    #-------------------------------------------------

    # fix diboson to MC prediction
    meas.addParamSetting("mu_Diboson", True, 1) 

    # fix Lumi if not exclusion fit
    if myFitType != FitType.Exclusion:
        meas.addParamSetting("Lumi", True, zlFitterConfig.luminosity)

    #fix error on signal
    if configMgr.fixSigXSec: 
        meas.addParamSetting("alpha_SigXSec", True, 1)

    if "CRQ" not in  zlFitterConfig.constrainingRegionsList:
        meas.addParamSetting("mu_Multijets", True, 1) # fix QCD
    if "CRY" not in  zlFitterConfig.constrainingRegionsList:
        meas.addParamSetting("mu_Z", True, 1)
    if "CRW" not in  zlFitterConfig.constrainingRegionsList:
        meas.addParamSetting("mu_W", True, 1) 
    if "CRT" not in  zlFitterConfig.constrainingRegionsList:
        meas.addParamSetting("mu_Top", True, 1)


    #-------------------------------------------------
    # add Samples to the configuration
    #-------------------------------------------------
    allSamplesList=[topSample, wSample, zSample, dataSample]
    #allSamplesList=[topSample, wSample, zSample, qcdSample, dataSample]
    if zlFitterConfig.useDIBOSONsample:
        allSamplesList+=[dibosonSample]
    myFitConfig.addSamples(allSamplesList)

        
    #-------------------------------------------------
    # Signal sample
    #-------------------------------------------------
    sigSampleName = "%s_%s" % (grid, point)

    if myFitType == FitType.Exclusion or (myFitType == FitType.Discovery and zlFitterConfig.useSignalInBlindedData==True):

        sigSample = Sample(sigSampleName, kRed)
        sigSample.setFileList([INPUTDIR_SIGNAL+grid+".root"])
        sigSample.setTreeName("%s_%s_SRAll" % (gridTreeName, point) )
        sigSample.setNormByTheory()
        sigSample.setNormFactor("mu_SIG", 1, 0., 100.)
        sigSample.setStatConfig(zlFitterConfig.useStat)

        myFitConfig.addSamples(sigSample)
        myFitConfig.setSignalSample(sigSample)


    ######################################################################
    # CR photon
    ######################################################################
    
    #check first if CRY can be used
    regionName="CRY"
    if regionName in zlFitterConfig.constrainingRegionsList and regionName in regionDict.keys():

        treeBaseName=regionDict[regionName].suffixTreeName
        extraWeightList=regionDict[regionName].extraWeightList
       
        # Gamma control region
        if not zlFitterConfig.useShapeFit:
            CRGAMMA = myFitConfig.addChannel("cuts", [regionName], 1, 0.5, 1.5)
        else:
            CRGAMMA = myFitConfig.addChannel(zlFitterConfig.binVar, [regionName], zlFitterConfig.nBins, zlFitterConfig.minbin, zlFitterConfig.maxbin)
            CRGAMMA.useOverflowBin = True
            CRGAMMA.useUnderflowBin = False

        CRGAMMA.addSample(gammaSample, 0) ##order is important!!!!
        for sam in CRGAMMA.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll", treeBaseName))               
            if sam.treeName.find("Data") >= 0:
                sam.setFileList(dataCRWTFiles)
            if sam.name.find("GAMMA") >= 0: #ATT: should define to which samples the extra-weight should be applied
                for extraWeight in extraWeightList:
                    sam.addWeight(extraWeight)
         

        #add as a constraining region
        myFitConfig.setBkgConstrainChannels(CRGAMMA)
        

    ######################################################################
    # Signal Regions
    ######################################################################
    if not zlFitterConfig.useShapeFit:        
        #SR_loose = myFitConfig.addChannel("cuts", ["SR_meffcut_relaxed"], 1, 0.5, 1.5)
        
        SR = [myFitConfig.addChannel("cuts", [zlFitterConfig.SRName], 1, 0.5, 1.5)]
        SR += [myFitConfig.addChannel("NJet", [zlFitterConfig.SRName], 20, 0.0, 20.0)]
        SR += [myFitConfig.addChannel("MDR", [zlFitterConfig.SRName], 30, 0.0, 1500.0)]  
        SR += [myFitConfig.addChannel("MET", [zlFitterConfig.SRName], 30, 0.0, 1500.0)]
        SR += [myFitConfig.addChannel("H2PP", [zlFitterConfig.SRName], 30, 0.0, 2000.0)]
        SR += [myFitConfig.addChannel("HT5PP", [zlFitterConfig.SRName], 30, 0.0, 4000.0)]
        #SR.remapSystChanName = "cuts_SR_meffcut_relaxed"
    else:
        SR = myFitConfig.addChannel(zlFitterConfig.binVar, [zlFitterConfig.SRName], zlFitterConfig.nBins, zlFitterConfig.minbin, zlFitterConfig.maxbin)
        SR.useOverflowBin = True
        SR.useUnderflowBin = False




    # Use the SR as validation region in the background fit, so that we can extract info from PDF in SR
    if myFitType == FitType.Background: 
        myFitConfig.setValidationChannels(SR)
    else:
        myFitConfig.setSignalChannels([SR])
            
    if myFitType == FitType.Discovery:
        SR.addDiscoverySamples(["SIG"], [1.], [0.], [1000.], [kMagenta])

    if zlFitterConfig.useQCDsample:
        SR.addSample(qcdSample)




    ######################################################################
    # Regions with leptons
    ######################################################################      


    for regionName in zlFitterConfig.allRegionsList():

        treeBaseName=regionDict[regionName].suffixTreeName

        #select only regions with leptons
        if treeBaseName not in ["CRWT","VRWT","CRZ","CRZ_VR1b"]: continue

        # skip validation regions
        if not doValidation and  regionName not in zlFitterConfig.constrainingRegionsList:
                continue

        """LH mod 
        #setup region
        if not zlFitterConfig.useShapeFit:
            REGION = myFitConfig.addChannel("cuts", [regionName], 1, 0.5, 1.5)
        else:
            REGION = myFitConfig.addChannel(zlFitterConfig.binVar, [regionName], zlFitterConfig.nBins, zlFitterConfig.minbin, zlFitterConfig.maxbin)
            REGION.useOverflowBin = True
            REGION.useUnderflowBin = False

        #set the treename
        for sam in REGION.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll", treeBaseName))
            if sam.treeName.find("Data") >= 0:
                sam.setFileList(dataCRWTFiles)
                pass

        #extra weights
        extraWeightList=regionDict[regionName].extraWeightList
        for extraWeight in extraWeightList:
            REGION.addWeight(extraWeight)
        

        #set region type
        if regionName in zlFitterConfig.constrainingRegionsList:                    
            myFitConfig.setBkgConstrainChannels(REGION)
        else:
            myFitConfig.setValidationChannels(REGION)
        """
        #setup region
        REGION = []
        if not zlFitterConfig.useShapeFit:
            #REGION = myFitConfig.addChannel("cuts", [regionName], 1, 0.5, 1.5)
            REGION += [myFitConfig.addChannel("MDR", [regionName], 40, 0.0, 1600.0)]
            REGION += [myFitConfig.addChannel("NJet", [regionName], 20, 0.0, 20.0)]
        else:
            REGION += [myFitConfig.addChannel(zlFitterConfig.binVar, [regionName], zlFitterConfig.nBins, zlFitterConfig.minbin, zlFitterConfig.maxbin)]
            #LH set REGION.useOverflowBin = True
            #LH set REGION.useUnderflowBin = False

        for reg in REGION:
            #set the treename
            for sam in reg.sampleList:
                sam.setTreeName(sam.treeName.replace("SRAll", treeBaseName))
                if sam.treeName.find("Data") >= 0:
                    sam.setFileList(dataCRWTFiles)
                    pass

            #extra weights
            extraWeightList=regionDict[regionName].extraWeightList
            for extraWeight in extraWeightList:
                reg.addWeight(extraWeight)


        #set region type
        if regionName in zlFitterConfig.constrainingRegionsList:
            myFitConfig.setBkgConstrainChannels(REGION)
        else:
            #allRegions+=[REGION]
            myFitConfig.setValidationChannels(REGION)
            #myFitConfig.setValidationChannels(allRegions)
        


    ######################################################################
    # Regions for QCD
    ######################################################################


    for regionName in zlFitterConfig.allRegionsList():

        #select region for QCD
        if not (regionName.find("CRQ")>=0 or regionName.find("CRQ")>=0): continue

        treeBaseName=regionDict[regionName].suffixTreeName

        # skip validation regions when not needed
        if not doValidation and  regionName not in zlFitterConfig.constrainingRegionsList:
            continue

        #setup region
        if not zlFitterConfig.useShapeFit:
            REGION = myFitConfig.addChannel("cuts", [regionName], 1, 0.5, 1.5)
        else:
            REGION = myFitConfig.addChannel(zlFitterConfig.binVar, [regionName], zlFitterConfig.nBins, zlFitterConfig.minbin, zlFitterConfig.maxbin)
            REGION.useOverflowBin = True
            REGION.useUnderflowBin = False

        if regionName in zlFitterConfig.constrainingRegionsList:  
            myFitConfig.setBkgConstrainChannels(REGION)
        else:
            myFitConfig.setValidationChannels(REGION)

        #add qcd samples
        if zlFitterConfig.useQCDsample:
            REGION.addSample(qcdSample)







    ###############################################################
    # add flat error in all VR and SR
    ###############################################################
#    if zlFitterConfig.useFlatBkgError:
    if zlFitterConfig.usePrecomputedError:
        for REGION in myFitConfig.channels:
            if REGION.regionString not in zlFitterConfig.constrainingRegionsList:
                for sam in REGION.sampleList:     
                    nameSys="errFlatBkg"
                    if sam.name==sigSampleName:
                        nameSys="errFlatSig"

                    sam.addSystematic(Systematic(nameSys, configMgr.weights, 1.+flatError, 1-flatError, "user", "userOverallSys"))
    



