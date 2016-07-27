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
from ChannelsDict import *
from ZLFitterConfig import *
from TheoUncertainties import *

from zerolepton.inputs.config import InputConfig

########################################
# Log
########################################

log = Logger("ZeroLeptonFitter")
log.info("ZeroLeptonFitter says hi!")

########################################
# Config Managers
########################################

# ZeroLepton configuration instance
# If you want to overright one of the option, please change ZLFitterConfig.py locally
zlFitterConfig = ZLFitterConfig()

# HistFitter's ConfigManager settings
configMgr.blindSR = zlFitterConfig.blindSR
configMgr.blindCR = zlFitterConfig.blindCR
configMgr.blindVR = zlFitterConfig.blindVR
configMgr.writeXML = zlFitterConfig.writeXML

configMgr.useSignalInBlindedData = zlFitterConfig.useSignalInBlindedData

configMgr.fixSigXSec = zlFitterConfig.fixSigXSec
configMgr.runOnlyNominalXSec = zlFitterConfig.runOnlyNominalXSec

#######################################################################
# Commandline args
#######################################################################

# parse configMgr.userArg to overwrite options above if needed
if configMgr.userArg != "":
    log.info("Found user args %s" % configMgr.userArg)

    # Note: these options should NOT have defaults! Else they will always get that value; we want them to be undefined if not specified
    parser = argparse.ArgumentParser(prog='ZeroLeptonFitter')
    parser.add_argument("-P", "--regionPrefix", type=str, default="")
    parser.add_argument("-R", "--optimisationRegion", type=str, default=None)
    parser.add_argument("-C", "--useBackgroundCache", action="store_true", default=False)

    args = parser.parse_args(configMgr.userArg.split())

    log.info("Parsed user args %s" % str(args))

    if args.useBackgroundCache:
        log.info("Setting useBackgroundCache=True")

        # note: we pass the filename later, depending on SR
        configMgr.useCacheToTreeFallback = True

    log.info("Waiting 5 seconds to review user args")
    #wait(5)

#######################################################################
# Gets cuts
#######################################################################

# pickedSRs gets set by HistFitter from the -r argument
if len(pickedSRs) > 0 and pickedSRs[0] not in finalChannelsDict and (configMgr.userArg == "" or args.optimisationRegion is None):
    # unknown SR, no optimisation flags passed
    log.fatal("UNKNOWN SR %s" % pickedSRs[0])

elif len(pickedSRs) > 0:
    # known SR, use it
    channel = finalChannelsDict[pickedSRs[0]]
    if configMgr.userArg != "" and args.optimisationRegion is not None:
        log.warning("Note: your optimisation SR will be ignored")
elif configMgr.userArg != "" and args.optimisationRegion is not None:
    # optimisation SR passed
    channel = createChannelConfigFromString(args.optimisationRegion, args.regionPrefix)
    channel.regionDict = regionDict
    log.info("Using optimisation region defined from %s" % args.optimisationRegion)

    # zlFitterConfig.luminosity = 4.0
    # log.warning("Forcing optimisation luminosity to {0} fb-1".format(zlFitterConfig.luminosity))

if zlFitterConfig.useFilteredNtuples:
    channel.useFilteredNtuples = True
    if "veto==0" in channel.commonCutList:
        # already applied
        channel.commonCutList.remove("veto==0")

channel.Print()
configMgr.cutsDict = channel.getCutsDict()

anaName = channel.name
if channel.optimisationRegion:
    anaName = channel.fullname

print anaName , anaName

#######################################################################
# Signal configutation
#######################################################################

# grid, with a default point and a default name
grid = "GG_direct"
gridTreeName = grid
allpoints = ["1200_0"]

########################################################################
# Options
########################################################################

# See settings/input.cfg to configure input directories for your site
inputConfig = InputConfig()
INPUTDIR = inputConfig.background
INPUTDIR_SIGNAL = inputConfig.signal
INPUTDIR_DATA = inputConfig.data

print inputConfig

# # INPUTDIR = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v51_Nov07_nosys_pT50/"
# INPUTDIR = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/Systematics/v51_Nov07_sys_pT50/"
# # INPUTDIR = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/"
# # INPUTDIR_SIGNAL = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v51_SIG_nosys_pT50/"
# INPUTDIR_SIGNAL = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/Systematics/v51_Signal_sys_pT50/"
# INPUTDIR_DATA = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v53_Data_pT50/"


# sigSamples is set by the "-g" HistFitter option
try:
    sigSamples
except NameError:
    sigSamples = None

if sigSamples != None:
    if "grid" in sigSamples[0]: # first entry allowed to specify a grid name
        grid = sigSamples[0].replace("grid", "")
        gridTreeName = grid
        allpoints = sigSamples[1:]

        if not os.path.exists(os.path.join(INPUTDIR_SIGNAL, grid+".root")) and not INPUTDIR_SIGNAL.find("eos")>=0:
            log.fatal("Input file {0} for signal does not exist!".format(os.path.join(INPUTDIR_SIGNAL, grid+".root")))
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
if myFitType == FitType.Discovery and not zlFitterConfig.useSignalInBlindedData:
    allpoints = ["Discovery"]
    grid = ""
    gridTreeName = ""

if myFitType == FitType.Background:
    allpoints = ["Background"]
    grid = ""
    gridTreeName = ""

#######################################################################
# Parameters for hypothesis test
#######################################################################

configMgr.nTOYs = 1000      # number of toys when doing frequentist calculator
configMgr.doExclusion = False
if myFitType == FitType.Exclusion:
    configMgr.doExclusion = True
# configMgr.useCLs = True #LL
# configMgr.cppMgr.doUpperLimitAll()
configMgr.calculatorType = 2 # 2=asymptotic calculator, 0=frequentist calculator
# configMgr.calculatorType = 0 # 2=asymptotic calculator, 0=frequentist calculator
configMgr.testStatType = 3   # 3=one-sided profile likelihood test statistic (LHC default)
configMgr.nPoints = 20       # number of values scanned of signal-strength for upper-limit determination of signal strength.
#configMgr.nPoints = 20       # number of values scanned of signal-strength for upper-limit determination of signal strength.

if configMgr.calculatorType == 2:
    configMgr.nPoints = 30
    #configMgr.nPoints = 10

#######################################################################------
# Now we start to build the data model
#######################################################################------

# Scaling calculated by outputLumi / inputLumi
configMgr.inputLumi = 1 # Luminosity of input TTree after weighting
configMgr.outputLumi = zlFitterConfig.luminosity # Luminosity required for output histograms
configMgr.setLumiUnits("fb-1")

# Set the files to read from
bgdFiles = []
topFiles = []
qcdFiles = []
qcdGammaFakeFiles = []
dibosonFiles = []
dataFiles = []
wFiles = []
zFiles = []
gammaFiles = []

if configMgr.readFromTree:

    if zlFitterConfig.useFilteredNtuples:
        for i in range(channel.nJets, 7):
            dibosonFiles.append(os.path.join(INPUTDIR, "DibosonMassiveCB_nJet_{0}.root".format(i)))
            topFiles.append(os.path.join(INPUTDIR, "Top_nJet_{0}.root".format(i)))
            if not zlFitterConfig.usePreComputedTopGeneratorSys:
                topFiles.append(os.path.join(INPUTDIR, "TopaMcAtNloHerwigpp_nJet_{0}.root".format(i)))
            if not zlFitterConfig.usePreComputedTopFragmentationSys:
                topFiles.append(os.path.join(INPUTDIR, "TopPowhegHerwigpp_nJet_{0}.root".format(i)))
            gammaFiles.append(os.path.join(INPUTDIR, "GAMMAMassiveCB_nJet_{0}.root".format(i)))
            wFiles.append(os.path.join(INPUTDIR, "WMassiveCB_nJet_{0}.root".format(i)))
            if not zlFitterConfig.usePreComputedWGeneratorSys:
                wFiles.append(os.path.join(INPUTDIR, "WMadgraphPythia8_nJet_{0}.root".format(i)))
            zFiles.append(os.path.join(INPUTDIR, "ZMassiveCB_nJet_{0}.root".format(i)))
            if not zlFitterConfig.usePreComputedZGeneratorSys:
                zFiles.append(os.path.join(INPUTDIR, "ZMadgraphPythia8_nJet_{0}.root".format(i)))

    else:
        # Diboson
        dibosonFiles.append(INPUTDIR+ "/DibosonMassiveCB.root" )


        if zlFitterConfig.useDDQCDsample:
            qcdFiles.append(os.path.join(INPUTDIR, "JetSmearing_2015.root"))
            qcdFiles.append(os.path.join(INPUTDIR, "JetSmearing_2016.root"))
        else :
            qcdFiles.append( INPUTDIR+"/QCD.root")

        qcdGammaFakeFiles.append( INPUTDIR+"/QCD.root" )


        # Topa
        topFiles.append(INPUTDIR+ "/Top.root")
        if not zlFitterConfig.usePreComputedTopGeneratorSys:
            pass
#            topFiles.append(INPUTDIR + "TopMCatNLO.root")
        if not zlFitterConfig.usePreComputedTopFragmentationSys:
            topFiles.append(INPUTDIR + "TopPowhegPythia8.root")
            topFiles.append(INPUTDIR + "TopPowhegHerwig.root")
        if not zlFitterConfig.usePreComputedTopRadiationSys:
            topFiles.append(INPUTDIR + "TopRadLo.root")
            topFiles.append(INPUTDIR + "TopRadHi.root")


        # W
        wFiles.append(INPUTDIR+ "/WMassiveCB.root")
        if not zlFitterConfig.usePreComputedWGeneratorSys:
            wFiles.append(INPUTDIR+ "/WMadgraphPythia8.root")

        # Z
        zFiles.append(INPUTDIR+ "/ZMassiveCB.root")
        # zFiles.append(INPUTDIR+ "/Zjets.root")
        if not zlFitterConfig.usePreComputedZGeneratorSys:
            zFiles.append(INPUTDIR+ "/ZMadgraphPythia8.root")

        # gamma
        gammaFiles.append(INPUTDIR+ "/GAMMAMassiveCB.root")
        # gammaFiles.append(INPUTDIR+ "/GAMMAMassiveCB_TRUTH_filtered.root"))
        # gammaFiles.append(INPUTDIR+ "/GAMMAMadgraph_TRUTH.root"))

    #data
    # dataFiles.append(INPUTDIR_DATA, "/DataMain_Nov01.root")
    # dataFiles.append(INPUTDIR_DATA+ "/Data_Nov07.root")
    # dataFiles.append(INPUTDIR_DATA+ "/DataMain_data15_13TeV.root")
    # dataFiles.append(INPUTDIR_DATA+ "/DataMain_data16_13TeV.root")
    dataFiles.append(INPUTDIR_DATA+ "/DataMain.root")

    log.info("Using the following inputs:")
    log.info("topFiles = %s" % topFiles)
    log.info("qcdFiles = %s" % qcdFiles)
    log.info("qcdGammaFakeFiles = %s" % qcdGammaFakeFiles)
    log.info("dibosonFiles = %s" % dibosonFiles)
    log.info("dataFiles = %s" % dataFiles)
    log.info("wFiles = %s" % wFiles)
    log.info("zFiles = %s" % zFiles)
    log.info("gammaFiles = %s" % gammaFiles)

# Tuples of nominal weights
#weights = ["genWeight", "pileupWeight", "normWeight"]
# weights = ["eventWeight", "pileupWeight", "normWeight"]
def anaNameEnum (anaName) :
    if "SRG" in anaName : return 1
    if "SRC" in anaName : return 2
    if "SRS" in anaName : return 3
    else : return 0

weights = ["weight", "WZweight"]
if zlFitterConfig.applyKappaCorrection:
    weights.append("gammaCorWeight(RunNumber, "+str(anaNameEnum(anaName))+")")
    # weights.append("1./1.6")
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

log.info("Wait 3 seconds for you to panic if these settings are wrong")
wait(3)
log.info("No panicking detected, continuing...")

#######################################################################
# List of samples and their plotting colours
#######################################################################

#--------------------------
# Diboson
#--------------------------
# NB: note that theoSys on diboson are applied on the level of the region definitions,
# since we have one for the SR and one for the CR
dibosonSample = Sample(zlFitterConfig.dibosonSampleName, kRed+3)
dibosonSample.setTreeName("Diboson_SRAll")
dibosonSample.setFileList(dibosonFiles)
dibosonSample.setStatConfig(zlFitterConfig.useStat)

#--------------------------
# QCD
#--------------------------
qcdSample = Sample(zlFitterConfig.qcdSampleName, kOrange+2)
if zlFitterConfig.useDDQCDsample:#normWeight is 0 => remove it
    qcdSample.setTreeName("Data_SRAll")
else :
    qcdSample.setTreeName("QCD_SRAll")
qcdSample.setNormFactor("mu_"+zlFitterConfig.qcdSampleName, 1., 0., 5000.)
qcdSample.setFileList(qcdFiles)
qcdSample.setStatConfig(zlFitterConfig.useStat)

qcdWeight = 1
nJets = channel.nJets
if nJets > 0 and nJets < len(zlFitterConfig.qcdWeightList)+1:
    qcdWeight = zlFitterConfig.qcdWeightList[nJets-1]/ (zlFitterConfig.luminosity)
    if zlFitterConfig.useMCQCDsample:
        qcdWeight = 1

    qcdSample.addWeight(str(qcdWeight))
    for w in configMgr.weights: #add all other weights but not normWeight
        qcdSample.addWeight(w)
    if zlFitterConfig.useDDQCDsample:#normWeight is 0 => remove it
        qcdSample.removeWeight("weight")
        qcdSample.addWeight("0.01")


#--------------------------
# QCD Gamma Fakes - for CRY
#--------------------------
qcdGammaFakeSample = Sample(zlFitterConfig.qcdSampleName+"GammaFakes", kOrange+2)
qcdGammaFakeSample.setTreeName("QCD_SRAll")
qcdGammaFakeSample.setNormFactor("mu_"+zlFitterConfig.qcdSampleName+"GammaFakes", 1., 0., 500.)
qcdGammaFakeSample.setFileList(qcdGammaFakeFiles)
qcdGammaFakeSample.setStatConfig(zlFitterConfig.useStat)
# qcdGammaFakeSample.setStatConfig(False)
qcdGammaFakeSample.addSampleSpecificWeight("(phTruthOrigin!=38)")


if zlFitterConfig.doSetNormRegion:
    if "CRYQ" in zlFitterConfig.constrainingRegionsList:
        qcdGammaFakeSample.setNormRegions([("CRYQ", zlFitterConfig.binVar)])


# Define samples
#FakePhotonSample = Sample("Bkg",kGreen-9)
#FakePhotonSample.setStatConfig(False)
#FakePhotonSample.buildHisto([nbkg],"UserRegion","cuts")
# ucb = Systematic("ucb", configMgr.weights, 1 + nbkgErr/nbkg, 1 - nbkgErr/nbkg, "user","userOverallSys")
#FakePhotonSample.addSystematic(ucb)


#--------------------------
# Top
#--------------------------

topSample = Sample(zlFitterConfig.topSampleName, kGreen-9)
topSample.setTreeName("Top_SRAll")
topSample.setNormFactor("mu_"+zlFitterConfig.topSampleName, 1., 0., 500.)
topSample.setFileList(topFiles)
topSample.setStatConfig(zlFitterConfig.useStat)
if zlFitterConfig.doSetNormRegion:
    if "CRT" in zlFitterConfig.constrainingRegionsList and "CRW" in zlFitterConfig.constrainingRegionsList:
        topSample.setNormRegions([("CRT", zlFitterConfig.binVar),("CRW", zlFitterConfig.binVar)])
    if "CRTZL" in zlFitterConfig.constrainingRegionsList and "CRW" in zlFitterConfig.constrainingRegionsList:
        topSample.setNormRegions([("CRTZL", zlFitterConfig.binVar),("CRW", zlFitterConfig.binVar)])

if not zlFitterConfig.usePreComputedTopGeneratorSys:
    topSample.addSystematic(Systematic("generatorTop", "", "_aMcAtNloHerwigpp", "", "tree", "overallNormHistoSysOneSide"))
if not zlFitterConfig.usePreComputedTopFragmentationSys:
    topSample.addSystematic(Systematic("Pythia8Top", "" , "_PowhegPythia8", "" , "tree", "overallNormHistoSysOneSide"))
#    topSample.addSystematic(Systematic("HerwigppTop", "", "_PowhegHerwigpp", "", "tree", "overallNormHistoSysOneSide"))

if not zlFitterConfig.usePreComputedTopRadiationSys:
    topSample.addSystematic(Systematic("radiationTop", "", "_RadLo", "_RadHi", "tree", "overallNormHistoSys"))



#--------------------------
# W
#--------------------------
wSample = Sample(zlFitterConfig.wSampleName, kAzure+1)
wSample.setTreeName("W_SRAll")
wSample.setNormFactor("mu_"+zlFitterConfig.wSampleName, 1., 0., 500.)
wSample.setFileList(wFiles)
wSample.setStatConfig(zlFitterConfig.useStat)
if not zlFitterConfig.usePreComputedWGeneratorSys:
    wSample.addSystematic(Systematic("generatorW", "", "_Madgraph", "", "tree", "overallNormHistoSysOneSide"))

if zlFitterConfig.doSetNormRegion:
    if "CRT" in zlFitterConfig.constrainingRegionsList and "CRW" in zlFitterConfig.constrainingRegionsList:
        wSample.setNormRegions([("CRT", zlFitterConfig.binVar),("CRW", zlFitterConfig.binVar)])



#--------------------------
# Gamma
#--------------------------
gammaSample = Sample(zlFitterConfig.gammaSampleName,kYellow)
gammaSample.setTreeName("GAMMA_SRAll")
gammaSample.setNormFactor("mu_"+zlFitterConfig.zSampleName,1.,0.,500.)
gammaSample.setFileList(gammaFiles)
gammaSample.setStatConfig(zlFitterConfig.useStat)
if zlFitterConfig.doSetNormRegion:
    if "CRY" in zlFitterConfig.constrainingRegionsList:
        gammaSample.setNormRegions([("CRY", zlFitterConfig.binVar)])

# gammaSyst = Systematic("generatorZ", "", "", "", "tree", "overallNormHistoSysOneSide")
# truthGammaList = [INPUTDIR+ "/GAMMAMassiveCB_TRUTH_filtered.root",
#                         INPUTDIR+ "/GAMMAMadgraph_TRUTH.root"]
# gammaSyst.setFileList(gammaSample,
#                       truthGammaList
#                       )
# gammaSample.addSystematic(gammaSyst)

#--------------------------
# Z
#--------------------------
zSample = Sample(zlFitterConfig.zSampleName, kBlue)
zSample.setTreeName("Z_SRAll")
zSample.setNormFactor("mu_"+zlFitterConfig.zSampleName, 1., 0., 500.)
zSample.setFileList(zFiles)
zSample.setStatConfig(zlFitterConfig.useStat)
if zlFitterConfig.doSetNormRegion:
    if "CRZ" in zlFitterConfig.constrainingRegionsList:
        zSample.setNormRegions([("CRZ", zlFitterConfig.binVar)])
        # zSample.normSampleRemap = "GAMMAjets"
    if "CRY" in zlFitterConfig.constrainingRegionsList:
        zSample.setNormRegions([("CRY", zlFitterConfig.binVar)])
        zSample.normSampleRemap = "GAMMAjets"
if not zlFitterConfig.usePreComputedZGeneratorSys:
    zSample.addSystematic(Systematic("generatorZ", "", "_Madgraph", "", "tree", "overallNormHistoSysOneSide"))


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

# Here be systematics. Sometime in future.
# sysWeight_theoSysSigUp = myreplace(configMgr.weights, ["normWeightUp"], "normWeight")
# sysWeight_theoSysSigDown = myreplace(configMgr.weights, ["normWeightDown"], "normWeight")
# theoSysSig = Systematic("SigXSec", configMgr.weights, sysWeight_theoSysSigUp, sysWeight_theoSysSigDown, "weight", "overallSys")



#######################################################################
# Set up fit
#######################################################################

# First define HistFactory attributes
prefix = "ZL"
if grid == "":
    configMgr.analysisName =  "%s_%s_%s" % (prefix, anaName, allpoints[0])
else:
    configMgr.analysisName =  "%s_%s_%s_%s" % (prefix, anaName, grid, allpoints[0])

# store everything in its own directory - except when optimising, we want to recycle the final cut
configMgr.histCacheFile = "data/%s/%s.root" % (configMgr.analysisName, configMgr.analysisName)
configMgr.outputFileName = "results/%s/%s_Output.root " % (configMgr.analysisName, configMgr.analysisName)

# TODO: this needs fixing to store an intermediate histogram before the final selection
#if channel.optimisationRegion:
#    dataDirName =  "%s_%s_%s_%s" % (prefix, channel.fullnameForData, grid, allpoints[0])
#    if not os.path.exists("data/%s" % dataDirName):
#        os.makedirs("data/%s" % dataDirName) # HistFitter doesn't realize we want something other than analysisName
#
#    configMgr.histCacheFile = "data/%s/%s.root" % (dataDirName, configMgr.analysisName)

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
    meas.addParamSetting("mu_"+zlFitterConfig.dibosonSampleName, True, 1)

    # fix Lumi if not exclusion fit
    if myFitType != FitType.Exclusion:
        meas.addParamSetting("Lumi", True, zlFitterConfig.luminosity)

    # fix error on signal
    if configMgr.fixSigXSec:
        meas.addParamSetting("alpha_SigXSec", True, 1)

    if "CRYQ" not in zlFitterConfig.constrainingRegionsList:
        meas.addParamSetting("mu_"+zlFitterConfig.qcdSampleName+"GammaFakes", True, 1) # fix QCD
    if "CRQ" not in zlFitterConfig.constrainingRegionsList:
        meas.addParamSetting("mu_"+zlFitterConfig.qcdSampleName, True, 1) # fix QCD
    if "CRY" not in zlFitterConfig.constrainingRegionsList and "CRZ" not in zlFitterConfig.constrainingRegionsList:
        meas.addParamSetting("mu_"+zlFitterConfig.zSampleName, True, 1)
    if "CRW" not in zlFitterConfig.constrainingRegionsList:
        meas.addParamSetting("mu_"+zlFitterConfig.wSampleName, True, 1)
    if "CRT" not in zlFitterConfig.constrainingRegionsList:
        meas.addParamSetting("mu_"+zlFitterConfig.topSampleName, True, 1)

    #-------------------------------------------------
    # add Samples to the configuration
    #-------------------------------------------------
    allSamplesList = [topSample, wSample, zSample, dataSample]
    if zlFitterConfig.useDIBOSONsample:
        allSamplesList += [dibosonSample]
    myFitConfig.addSamples(allSamplesList)

    #-------------------------------------------------
    # Signal sample
    #-------------------------------------------------
    sigSampleName = "%s_%s" % (grid, point)

    if myFitType == FitType.Exclusion or (myFitType == FitType.Discovery and zlFitterConfig.useSignalInBlindedData==True):

        sigSample = Sample(sigSampleName, kRed)
        sigSample.setFileList([os.path.join(INPUTDIR_SIGNAL, grid+("_fastsim" if grid=="GG_onestepCC" else "")+".root")]) # tentative hack. Will change the file name soon.
        sigSample.setTreeName("%s_%s_SRAll" % (gridTreeName, point) )
        sigSample.setNormByTheory()
        sigSample.setNormFactor("mu_SIG", 1, 0., 100.)
#        sigSample.addSystematic(theoSysSig)
        sigSample.setStatConfig(zlFitterConfig.useStat)
        myFitConfig.addSamples(sigSample)
        myFitConfig.setSignalSample(sigSample)


    ######################################################################
    # CR photon
    ######################################################################

    for regionName in zlFitterConfig.allRegionsList():
        treeBaseName = regionDict[regionName].suffixTreeName

        # skip validation regions
        if not doValidation and regionName not in zlFitterConfig.constrainingRegionsList:
            continue

        #select only regions with leptons
        if treeBaseName not in ["CRY"]:
            continue

        extraWeightList = regionDict[regionName].extraWeightList

        # Gamma control region
        if not zlFitterConfig.useShapeFit:
            REGION = myFitConfig.addChannel("cuts", [regionName], 1, 0.5, 1.5)
        else:
            REGION = myFitConfig.addChannel(zlFitterConfig.binVar, [regionName], zlFitterConfig.nBins, zlFitterConfig.minbin, zlFitterConfig.maxbin)
            REGION.useOverflowBin = True
            REGION.useUnderflowBin = False

        # if regionName=="CRY":
        #     qcdGammaFakeSample.addSystematic(Systematic("PhFakeRateUncertainty", configMgr.weights, 1.+.6, 1-.6, "user", "userOverallSys"))

        # REGION.addSample(qcdGammaFakeSample )
        REGION.addSample(gammaSample, 0) ##order is important!!!!
        REGION.addSample(qcdGammaFakeSample ,1)

        # print REGION.sampleList
        for sam in REGION.sampleList:

            sam.setTreeName(sam.treeName.replace("SRAll", treeBaseName))
            if sam.treeName.find("Data") >= 0:
                sam.setFileList(dataFiles)
            if sam.name.find("GAMMA") >= 0: #ATT: should define to which samples the extra-weight should be applied
                for extraWeight in extraWeightList:
                    sam.addWeight(extraWeight)

        # set region type
        if regionName in zlFitterConfig.constrainingRegionsList:
            # add as a constraining region
            myFitConfig.setBkgConstrainChannels(REGION)
        else:
            myFitConfig.setValidationChannels(REGION)


    ######################################################################
    # Signal Regions
    ######################################################################
    if not zlFitterConfig.useShapeFit:
        #SR_loose = myFitConfig.addChannel("cuts", ["SR_meffcut_relaxed"], 1, 0.5, 1.5)

        SR = myFitConfig.addChannel("cuts", [zlFitterConfig.SRName], 1, 0.5, 1.5)
        # myFitConfig.addChannel("Meff", [zlFitterConfig.SRName], 50, 0, 3000)
        # myFitConfig.addChannel("MET", [zlFitterConfig.SRName], 50, 0, 3000)
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

    # Dummy sample for discovery tests
    if myFitType == FitType.Discovery:
        SR.addDiscoverySamples(["SIG"], [1.], [0.], [1000.], [kMagenta])

    if zlFitterConfig.useDDQCDsample or zlFitterConfig.useMCQCDsample:
        SR.addSample(qcdSample)

    ######################################################################
    # Regions with leptons
    ######################################################################

    for regionName in zlFitterConfig.allRegionsList():
        treeBaseName = regionDict[regionName].suffixTreeName

        # select only regions with leptons
        if treeBaseName not in ["CRWT","VRWT","CRZ","CRZ_VR1b"]:
            continue

        # skip validation regions
        if not doValidation and regionName not in zlFitterConfig.constrainingRegionsList:
            continue

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
            if "Data" in sam.treeName:
                sam.setFileList(dataFiles)
                pass

        # extra weights
        extraWeightList = regionDict[regionName].extraWeightList
        for extraWeight in extraWeightList:
            REGION.addWeight(extraWeight)

        # lepton uncertainties
        if zlFitterConfig.useLeptonUncertainties and "systWeights[0]" in regionDict[regionName].extraWeightList:

            leptonSystematicList = []

            EL_EFFSystWeightsDown = myreplace(REGION.weights, ["systWeights[1]"] , "systWeights[0]")
            EL_EFFSystWeightsUp = myreplace(REGION.weights, ["systWeights[2]"] , "systWeights[0]")
            leptonSystematicList.append(Systematic("EL_EFF", REGION.weights  , EL_EFFSystWeightsUp, EL_EFFSystWeightsDown, "weight", "overallNormHistoSys"))

            MUON_EFF_STATSystWeightsDown = myreplace(REGION.weights, ["systWeights[3]"] , "systWeights[0]")
            MUON_EFF_STATSystWeightsUp = myreplace(REGION.weights, ["systWeights[4]"] , "systWeights[0]")
            leptonSystematicList.append(Systematic("MUON_EFF_STAT", REGION.weights  , MUON_EFF_STATSystWeightsUp, MUON_EFF_STATSystWeightsDown, "weight", "overallNormHistoSys"))

            MUON_EFF_SYSSystWeightsDown = myreplace(REGION.weights, ["systWeights[5]"] , "systWeights[0]")
            MUON_EFF_SYSSystWeightsUp = myreplace(REGION.weights, ["systWeights[6]"] , "systWeights[0]")
            leptonSystematicList.append(Systematic("MUON_EFF_SYS", REGION.weights  , MUON_EFF_SYSSystWeightsUp, MUON_EFF_SYSSystWeightsDown, "weight", "overallNormHistoSys"))

            MUON_EFF_TrigStatSystWeightsDown = myreplace(REGION.weights, ["systWeights[7]"] , "systWeights[0]")
            MUON_EFF_TrigStatSystWeightsUp = myreplace(REGION.weights, ["systWeights[7]"] , "systWeights[0]")
            leptonSystematicList.append(Systematic("MUON_EFF_TrigStat", REGION.weights  , MUON_EFF_TrigStatSystWeightsUp, MUON_EFF_TrigStatSystWeightsDown, "weight", "overallNormHistoSys"))

            MUON_EFF_TrigSystSystWeightsDown = myreplace(REGION.weights, ["systWeights[8]"] , "systWeights[0]")
            MUON_EFF_TrigSystSystWeightsUp = myreplace(REGION.weights, ["systWeights[8]"] , "systWeights[0]")
            leptonSystematicList.append(Systematic("MUON_EFF_TrigSyst", REGION.weights  , MUON_EFF_TrigSystSystWeightsUp, MUON_EFF_TrigSystSystWeightsDown, "weight", "overallNormHistoSys"))

            for sys in leptonSystematicList:
                sam.addSystematic(sys)

        #bTagging uncertainties
        if zlFitterConfig.useBTagUncertainties and "btagSystWeights[0]" in regionDict[regionName].extraWeightList:

            btagSystematicList = []

            bTagSystWeightsBUp = myreplace(REGION.weights, ["btagSystWeights[1]"] , "btagSystWeights[0]")
            bTagSystWeightsBDown = myreplace(REGION.weights, ["btagSystWeights[2]"] , "btagSystWeights[0]")
            btagSystematicList.append(Systematic("EFF_B", REGION.weights  , bTagSystWeightsBUp, bTagSystWeightsBDown, "weight", "overallNormHistoSys"))

            bTagSystWeightsCUp = myreplace(REGION.weights, ["btagSystWeights[3]"] , "btagSystWeights[0]")
            bTagSystWeightsCDown = myreplace(REGION.weights, ["btagSystWeights[4]"] , "btagSystWeights[0]")
            btagSystematicList.append(Systematic("EFF_C", REGION.weights  , bTagSystWeightsCUp, bTagSystWeightsCDown, "weight", "overallNormHistoSys"))

            bTagSystWeightsLUp = myreplace(REGION.weights, ["btagSystWeights[5]"] , "btagSystWeights[0]")
            bTagSystWeightsLDown = myreplace(REGION.weights, ["btagSystWeights[6]"] , "btagSystWeights[0]")
            btagSystematicList.append(Systematic("EFF_Light", REGION.weights  , bTagSystWeightsLUp, bTagSystWeightsLDown, "weight", "overallNormHistoSys"))


            bTagSystWeightsExtrapolationUp = myreplace(REGION.weights, ["btagSystWeights[7]"] , "btagSystWeights[0]")
            bTagSystWeightsExtrapolationDown = myreplace(REGION.weights, ["btagSystWeights[8]"] , "btagSystWeights[0]")
            btagSystematicList.append(Systematic("EFF_extrapolation", REGION.weights  , bTagSystWeightsExtrapolationUp, bTagSystWeightsExtrapolationDown, "weight", "overallNormHistoSys"))


            bTagSystWeightsExtrapolationFromCharmUp = myreplace(REGION.weights, ["btagSystWeights[9]"] , "btagSystWeights[0]")
            bTagSystWeightsExtrapolationFromCharmDown = myreplace(REGION.weights, ["btagSystWeights[10]"] , "btagSystWeights[0]")
            btagSystematicList.append(Systematic("EFF_extrapolation_from_charm", REGION.weights  , bTagSystWeightsExtrapolationFromCharmUp, bTagSystWeightsExtrapolationFromCharmDown, "weight", "overallNormHistoSys"))


            for sam in REGION.sampleList:
                if sam.name==zlFitterConfig.zSampleName: continue #ATT : prb with Z samples!!!!!
                for sys in btagSystematicList:
                    sam.addSystematic(sys)

        # set region type
        if regionName in zlFitterConfig.constrainingRegionsList:
            myFitConfig.setBkgConstrainChannels(REGION)
        else:
            myFitConfig.setValidationChannels(REGION)



#        if zlFitterConfig.useQCDsample:
#            REGION.addSample(qcdSample)


    ######################################################################
    # Hadronic CRs - LL
    ######################################################################

    for regionName in zlFitterConfig.allRegionsList():


        # skip validation regions
        if not doValidation and regionName not in zlFitterConfig.constrainingRegionsList:
            continue

        if not( regionName in ["VRZc","VRZca"]):
            continue

        treeBaseName = regionDict[regionName].suffixTreeName


    #     # select only regions with leptons
        if treeBaseName not in ["SRAll"]:
            continue
    #     if "CR" not in regionName:
    #         continue

    #     #setup region
    #     if not zlFitterConfig.useShapeFit:
    #         REGION = myFitConfig.addChannel("cuts", [regionName], 1, 0.5, 1.5)
    #     else:
        REGION = myFitConfig.addChannel(zlFitterConfig.binVar, [regionName], zlFitterConfig.nBins, zlFitterConfig.minbin, zlFitterConfig.maxbin)
        REGION.useOverflowBin = True
        REGION.useUnderflowBin = False

    #     #set the treename
    #     for sam in REGION.sampleList:
    #         sam.setTreeName(sam.treeName.replace("SRAll", treeBaseName))
    #         if "Data" in sam.treeName:
    #             sam.setFileList(dataFiles)
    #             pass

    #     # extra weights
    #     extraWeightList = regionDict[regionName].extraWeightList
    #     for extraWeight in extraWeightList:
    #         REGION.addWeight(extraWeight)

    #     #bTagging uncertainties
    #     if zlFitterConfig.useBTagUncertainties and "bTagWeight" in regionDict[regionName].extraWeightList:

    #         btagSystematicList = []

    #         bTagSystWeightsBUp = myreplace(REGION.weights, ["bTagWeightBUp"] , "bTagWeight")
    #         bTagSystWeightsBDown = myreplace(REGION.weights, ["bTagWeightBDown"] , "bTagWeight")
    #         btagSystematicList.append(Systematic("bTagSysB", REGION.weights  , bTagSystWeightsBUp, bTagSystWeightsBDown, "weight", "overallNormHistoSys"))

    #         bTagSystWeightsCUp = myreplace(REGION.weights, ["bTagWeightCUp"] , "bTagWeight")
    #         bTagSystWeightsCDown = myreplace(REGION.weights, ["bTagWeightCDown"] , "bTagWeight")
    #         btagSystematicList.append(Systematic("bTagSysC", REGION.weights  , bTagSystWeightsCUp, bTagSystWeightsCDown, "weight", "overallNormHistoSys"))

    #         bTagSystWeightsLUp = myreplace(REGION.weights, ["bTagWeightLUp"] , "bTagWeight")
    #         bTagSystWeightsLDown = myreplace(REGION.weights, ["bTagWeightLDown"] , "bTagWeight")
    #         btagSystematicList.append(Systematic("bTagSysL", REGION.weights  , bTagSystWeightsLUp, bTagSystWeightsLDown, "weight", "overallNormHistoSys"))

    #         for sys in btagSystematicList:
    #             sam.addSystematic(sys)

    #     # set region type
    #     if regionName in zlFitterConfig.constrainingRegionsList:
    #         myFitConfig.setBkgConstrainChannels(REGION)
    #     else:
        myFitConfig.setValidationChannels(REGION)


    #     if zlFitterConfig.useQCDsample:
    #         REGION.addSample(qcdSample)


    ######################################################################
    # Regions for QCD
    ######################################################################


    for regionName in zlFitterConfig.allRegionsList():

        #select region for QCD
        if not "RQ" in regionName:
            continue

        treeBaseName = regionDict[regionName].suffixTreeName

        if treeBaseName not in ["SRAll"]:
            continue

        # skip validation regions when not needed
        if not doValidation and regionName not in zlFitterConfig.constrainingRegionsList:
            continue

        # setup region
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
        if zlFitterConfig.useDDQCDsample or zlFitterConfig.useMCQCDsample:
            REGION.addSample(qcdSample)

    ###############################################################
    # add precomputed error in all VR and SR
    # These uncertainties correspond to the uncertainty on the TF
    # That's why they are not added in the control regions
    ###############################################################

    if zlFitterConfig.usePrecomputedError:
        for REGION in myFitConfig.channels:
            if REGION.regionString in zlFitterConfig.constrainingRegionsList:
                continue


            for sam in REGION.sampleList:

                # if sam.name == zlFitterConfig.qcdSampleName+"GammaFakes":
                #     sam.addSystematic(Systematic("FlatDiboson", configMgr.weights, 1.+error, 1-error, "user", "userOverallSys"))

                #signal
                if sam.name == sigSampleName:
                    #Needs to add theory uncertainty on signal acceptance for low-dM points
                    nameSys = "FlatSig"
                    #sam.addSystematic(Systematic(nameSys, configMgr.weights, 1.+zlFitterConfig.flatErrorSignal, 1-zlFitterConfig.flatErrorSignal, "user", "userOverallSys"))
                #Z background
                elif sam.name==zlFitterConfig.zSampleName:
                    #generator
                    if zlFitterConfig.usePreComputedZGeneratorSys:
                        print "adding Z THEO UNCERTAINTIES"
                        errorGenerator=getError(channel.name,REGION.name.replace("cuts_",""),zTheoSysGeneratorDict)
                        sam.addSystematic(Systematic("GeneratorZ", configMgr.weights, 1.+errorGenerator, 1-errorGenerator, "user", "userOverallSys"))
                    #Kappa
                    if zlFitterConfig.applyKappaCorrection:
#                        kappaError=0.066 if anaNameEnum(anaName)==3 else 0.080
                        kappaError = 0.058 #.25 if anaNameEnum(anaName)==2 else 0.07
                        sam.addSystematic(Systematic("Kappa", configMgr.weights, 1+kappaError, 1-kappaError, "user", "userOverallSys"))


                #W background
                elif sam.name==zlFitterConfig.wSampleName:
                    #generator
                    if zlFitterConfig.usePreComputedWGeneratorSys:
                        errorGenerator=getError(channel.name,REGION.name.replace("cuts_",""),wTheoSysGeneratorDict)
                        sam.addSystematic(Systematic("GeneratorW", configMgr.weights, 1.+errorGenerator, 1-errorGenerator, "user", "userOverallSys"))
                #Top background
                elif sam.name==zlFitterConfig.topSampleName:
                    #generator
                    if zlFitterConfig.usePreComputedTopGeneratorSys:
                        errorGenerator=getError(channel.name,REGION.name.replace("cuts_",""),topTheoSysGeneratorDict)
                        sam.addSystematic(Systematic("GeneratorTop", configMgr.weights, 1.+errorGenerator, 1-errorGenerator, "user", "userOverallSys"))

                    #A14
#                    errorA14=getError(channel.name,REGION.name.replace("cuts_",""),topTheoSysA14Dict)
#                    sam.addSystematic(Systematic("TopTuneA14", configMgr.weights, 1.+errorA14, 1-errorA14, "user", "userOverallSys"))

                    #PowhegHerwig
                    # if zlFitterConfig.usePreComputedTopFragmentationSys:
                    #     errorPowhegHerwig=getError(channel.name,REGION.name.replace("cuts_",""),topTheoSysPowhegHerwigDict)
                    #     sam.addSystematic(Systematic("FragmentationTop", configMgr.weights, 1.+errorPowhegHerwig, 1-errorPowhegHerwig, "user", "userOverallSys"))
                    #radiation
#                    errorRad=getError(channel.name,REGION.name.replace("cuts_",""),topTheoSysRadDict)
#                    sam.addSystematic(Systematic("TopRadiation", configMgr.weights, 1.+errorRad[0], 1-errorRad[1], "user", "userOverallSys"))



                #diboson
                elif sam.name==zlFitterConfig.dibosonSampleName:
                    error=0
                    if (channel.name,REGION.name.replace("cuts_","")) in dibosonFlatSysDict.keys():
                        error=dibosonFlatSysDict[(channel.name,REGION.name.replace("cuts_",""))]
                    elif ("default","default") in dibosonFlatSysDict.keys():
                        error=dibosonFlatSysDict[("default","default")]
                    sam.addSystematic(Systematic("FlatDiboson", configMgr.weights, 1.+error, 1-error, "user", "userOverallSys"))
                elif sam.name==zlFitterConfig.qcdSampleName:
                    errorQCD = 0.999
                    sam.addSystematic(Systematic("QCDError", configMgr.weights, 1+errorQCD, 1-errorQCD, "user", "userOverallSys"))


                    #continue



    ###############################################################
    # add systematics
    ###############################################################


    #JET systematics
    jetSystematicList = []

    # JER systematics
    # ATT: Not sure that it should be symmetrized
    jetSystematicList.append(Systematic("JER", "", "_JET_JER_SINGLE_NP_1up", "", "tree", "overallNormHistoSysOneSide"))

    #JES systematics
    jesSystematicStrList=[
        "JET_GroupedNP_1",
        "JET_GroupedNP_2",
        "JET_GroupedNP_3",
        ]

    for jesSysStr in jesSystematicStrList:
        jetSystematicList.append(Systematic(jesSysStr,"","_"+jesSysStr+"_1up","_"+jesSysStr+"_1down","tree","overallNormHistoSys"))


    #MET systematics
    metSystematicList = []
    metSystematicList.append(Systematic("MET_SoftTrk_ResoPara", "", "_MET_SoftTrk_ResoPara", "", "tree", "overallNormHistoSysOneSide"))
    metSystematicList.append(Systematic("MET_SoftTrk_ResoPerp", "", "_MET_SoftTrk_ResoPerp", "", "tree", "overallNormHistoSysOneSide"))
    metSystematicList.append(Systematic("MET_SoftTrk_Scale", "", "_MET_SoftTrk_ScaleUp", "_MET_SoftTrk_ScaleDown", "tree", "overallNormHistoSys"))


    for REGION in myFitConfig.channels:
        for sam in REGION.sampleList:
            if zlFitterConfig.qcdSampleName in sam.name: continue
            if zlFitterConfig.useJETUncertainties:
                for sys in jetSystematicList:
                    # if sam.name==zlFitterConfig.qcdSampleName: continue
                    sam.addSystematic(sys)
            if zlFitterConfig.useMETUncertainties:
                for sys in metSystematicList:
                    sam.addSystematic(sys)

    ###############################################################
    # This is the end
    ###############################################################

