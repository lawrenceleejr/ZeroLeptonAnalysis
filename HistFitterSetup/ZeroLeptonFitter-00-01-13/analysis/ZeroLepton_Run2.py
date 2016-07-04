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
from CoefficientsForDatadriven import *

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

    log.info("Waiting 2 seconds to review user args")
    wait(2)

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

    zlFitterConfig.luminosity = 4.0
    log.warning("Forcing optimisation luminosity to {0} fb-1".format(zlFitterConfig.luminosity))

    configMgr.blindSR = True
    configMgr.blindCR = True
    log.warning("Forcing optimisation CRs and SR to be blinded")

if zlFitterConfig.useSplittedNtuples:
    channel.useSplittedNtuples = True
    if "veto==0" in channel.commonCutList:
        # already applied in the filtered ntuples - remove it
        channel.commonCutList.remove("veto==0")

channel.Print()
configMgr.cutsDict = channel.getCutsDict()

anaName = channel.name
if channel.optimisationRegion:
    anaName = channel.fullname

#coefficents for data-driven BG estimation
channelCoefficients = ChannelCoefficients(anaName,zlFitterConfig.meffABCD)
channelCoefficients.Print()
CoefficientsDict = channelCoefficients.getCoefficientsDict()
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
INPUTDIR_MC = inputConfig.background
INPUTDIR_MC_ALTERNATIVE = inputConfig.background_alternative
INPUTDIR_SIGNAL = inputConfig.signal
INPUTDIR_DATA = inputConfig.data

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

        #if not os.path.exists(os.path.join(INPUTDIR_SIGNAL, grid+".root")) and not "eos" in INPUTDIR_SIGNAL:
        #     log.fatal("Input file {0} for signal does not exist!".format(os.path.join(INPUTDIR_SIGNAL, grid+".root")))
        #else:
         # allpoints = sigSamples

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

configMgr.nTOYs = 5000      # number of toys when doing frequentist calculator
configMgr.doExclusion = False
if myFitType == FitType.Exclusion:
    configMgr.doExclusion = True
configMgr.calculatorType = 2 # 2=asymptotic calculator, 0=frequentist calculator
configMgr.testStatType = 3   # 3=one-sided profile likelihood test statistic (LHC default)
configMgr.nPoints = 20       # number of values scanned of signal-strength for upper-limit determination of signal strength.

if configMgr.calculatorType == 2:
    configMgr.nPoints = 30

#######################################################################------
# Now we start to build the data model
#######################################################################------

# Scaling calculated by outputLumi / inputLumi
configMgr.inputLumi = 0.001 # Luminosity of input TTree after weighting
configMgr.outputLumi = zlFitterConfig.luminosity # Luminosity required for output histograms
configMgr.setLumiUnits("fb-1")

# Set the files to read from
bgdFiles = []
topFiles = []
qcdFiles = []
dibosonFiles = []
dataFiles = []
wFiles = []
zFiles = []
gammaFiles = []

if configMgr.readFromTree:



    if zlFitterConfig.useSplittedNtuples:
        for i in range(channel.nJets, 7):
            dibosonFiles.append(os.path.join(INPUTDIR_MC, "DibosonMassiveCB_nJet_{0}.root".format(i)))
            topFiles.append(os.path.join(INPUTDIR_MC, "Top_nJet_{0}.root".format(i)))
            gammaFiles.append(os.path.join(INPUTDIR_MC, "GAMMAMassiveCB_nJet_{0}.root".format(i)))
            wFiles.append(os.path.join(INPUTDIR_MC, "WMassiveCB_nJet_{0}.root".format(i)))
            zFiles.append(os.path.join(INPUTDIR_MC, "ZMassiveCB_nJet_{0}.root".format(i)))

            if zlFitterConfig.useMCQCDsample:
                qcdFiles.append(os.path.join(INPUTDIR_MC, "QCD_nJet_{0}.root".format(i)))
            if not zlFitterConfig.usePrecomputedTopGeneratorSys:
                topFiles.append(os.path.join(INPUTDIR_MC_ALTERNATIVE, "TopaMcAtNloHerwigpp_nJet_{0}.root".format(i)))
            if not zlFitterConfig.usePrecomputedTopFragmentationSys:
                topFiles.append(os.path.join(INPUTDIR_MC_ALTERNATIVE, "TopPowhegHerwigpp_nJet_{0}.root".format(i)))
            if not zlFitterConfig.usePrecomputedZGeneratorSys:
                zFiles.append(os.path.join(INPUTDIR_MC_ALTERNATIVE, "ZMadgraphPythia8_nJet_{0}.root".format(i)))
            if not zlFitterConfig.usePrecomputedWGeneratorSys:
                wFiles.append(os.path.join(INPUTDIR_MC_ALTERNATIVE, "WMadgraphPythia8_nJet_{0}.root".format(i)))


    else:

        # QCD
        if zlFitterConfig.useMCQCDsample:
            qcdFiles.append(os.path.join(INPUTDIR_MC, "QCD.root"))
#                qcdFiles.append(os.path.join(INPUTDIR_MC, "JetSmearing_2016.root"))#for now, only use 2016 JetSmearing



        # Diboson
        dibosonFiles.append(os.path.join(INPUTDIR_MC, "DibosonMassiveCB.root"))

        # Top
        topFiles.append(os.path.join(INPUTDIR_MC, "Top.root"))
        if not zlFitterConfig.usePrecomputedTopGeneratorSys:
            topFiles.append(os.path.join(INPUTDIR_MC_ALTERNATIVE, "TopaMcAtNloHerwigpp.root"))
        if not zlFitterConfig.usePrecomputedTopFragmentationSys:
            topFiles.append(os.path.join(INPUTDIR_MC_ALTERNATIVE, "TopPowhegHerwigpp.root"))

        # W
        wFiles.append(os.path.join(INPUTDIR_MC, "WMassiveCB.root"))
        if not zlFitterConfig.usePrecomputedWGeneratorSys:
            wFiles.append(os.path.join(INPUTDIR_MC_ALTERNATIVE, "WMadgraphPythia8.root"))

        # Z
        zFiles.append(os.path.join(INPUTDIR_MC, "ZMassiveCB.root"))
        if not zlFitterConfig.usePrecomputedZGeneratorSys:
            zFiles.append(os.path.join(INPUTDIR_MC_ALTERNATIVE, "ZMadgraphPythia8.root"))

        # gamma
        gammaFiles.append(os.path.join(INPUTDIR_MC, "GAMMAMassiveCB.root"))
        gammaFiles.append(os.path.join(INPUTDIR_MC, "GAMMAMassiveCB_TRUTH_filtered.root"))






    # data
    dataFiles.append(os.path.join(INPUTDIR_DATA, "DataMain.root"))

    log.info("Using the following inputs:")
    log.info("topFiles = %s" % topFiles)
    log.info("qcdFiles = %s" % qcdFiles)
    log.info("dibosonFiles = %s" % dibosonFiles)
    log.info("dataFiles = %s" % dataFiles)
    log.info("wFiles = %s" % wFiles)
    log.info("zFiles = %s" % zFiles)
    log.info("gammaFiles = %s" % gammaFiles)

    for list in [dibosonFiles, topFiles, gammaFiles, wFiles, zFiles, dataFiles]:
        for f in list:
            if not "eos" in f and not os.path.exists(f):
                log.fatal("Input file {0} does not exist!".format(f))

# Tuples of nominal weights
weights = ["eventWeight", "normWeight"] #"pileupWeight",
if zlFitterConfig.applyKappaCorrection:
    weights.append("gammaCorWeight(RunNumber)")
configMgr.weights = weights

#######################################################################
# Dump our options to user
#######################################################################

if zlFitterConfig.useStat and zlFitterConfig.useStatPerSample:
    log.fatal("You have turned on both useStat and useStatPerSample: not possible!")
    sys.exit()

log.info("Will run with the following settings:")
log.info("INPUTDIR_MC = %s" % INPUTDIR_MC)
if INPUTDIR_MC != INPUTDIR_SIGNAL:
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
dibosonSample.setNormFactor("mu_"+zlFitterConfig.dibosonSampleName, 1., 0., 500.)

#--------------------------
# QCD
#--------------------------
qcdSample = Sample(zlFitterConfig.qcdSampleName, kOrange+2)
qcdSample.setTreeName("QCDdd_SRAll")
if zlFitterConfig.useMCQCDsample:
    qcdSample.setTreeName("QCD_SRAll")
qcdSample.setNormFactor("mu_"+zlFitterConfig.qcdSampleName, 1., 0., 500.)
qcdSample.setFileList(qcdFiles)
qcdSample.setStatConfig(zlFitterConfig.useStat)

qcdWeight = 1
nJets = channel.nJets
if nJets > 0 and nJets < len(zlFitterConfig.qcdWeightList):
    qcdWeight = zlFitterConfig.qcdWeightList[nJets-1]/ (zlFitterConfig.luminosity*1000)
    if zlFitterConfig.useMCQCDsample:
        qcdWeight = 1
    qcdSample.addWeight(str(qcdWeight))

    for w in configMgr.weights: #ATT: there is a bug in HistFitter, I have to add the other weight by hand
        qcdSample.addWeight(w)

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
if zlFitterConfig.datadriven:
    #For Loose Control Region
    topLooseSample = Sample(zlFitterConfig.topLooseSampleName, kGreen-9)
    topLooseSample.setTreeName("Top_SRAll")
    topLooseSample.setNormFactor("mu_"+zlFitterConfig.topLooseSampleName, 1., 0., 500.)
    topLooseSample.setFileList(topFiles)
    topLooseSample.setStatConfig(zlFitterConfig.useStat)

    #For Very Loose Control Region
    topVeryLooseSample = Sample(zlFitterConfig.topVeryLooseSampleName, kGreen-9)
    topVeryLooseSample.setTreeName("Top_SRAll")
    topVeryLooseSample.setNormFactor("mu_"+zlFitterConfig.topVeryLooseSampleName, 1., 0., 500.)
    topVeryLooseSample.setFileList(topFiles)
    topVeryLooseSample.setStatConfig(zlFitterConfig.useStat)

    #For Top Constraint Region
if zlFitterConfig.doSetNormRegion:
    if "CRT" in zlFitterConfig.constrainingRegionsList and "CRW" in zlFitterConfig.constrainingRegionsList:
        topSample.setNormRegions([("CRT", zlFitterConfig.binVar),("CRW", zlFitterConfig.binVar)])
    if "CRTL" in zlFitterConfig.constrainingRegionsList:
        topLooseSample.setNormRegions([("CRTL", zlFitterConfig.binVar)])
    if "CRTVL" in zlFitterConfig.constrainingRegionsList:
        topVeryLooseSample.setNormRegions([("CRTVL", zlFitterConfig.binVar)])

    #For Top Systematics
if not zlFitterConfig.usePrecomputedTopGeneratorSys:
    topSample.addSystematic(Systematic("generatorTop", "", "_aMcAtNloHerwigpp", "", "tree", "overallNormHistoSysOneSide"))
    if zlFitterConfig.datadriven:
        topLooseSample.addSystematic(Systematic("generatorTop","" , "_aMcAtNloHerwigpp", "", "tree", "overallNormHistoSysOneSide"))
        topVeryLooseSample.addSystematic(Systematic("generatorTop","" , "_aMcAtNloHerwigpp", "", "tree", "overallNormHistoSysOneSide"))

if not zlFitterConfig.usePrecomputedTopFragmentationSys:
    topSample.addSystematic(Systematic("fragmentationTop", "", "_PowhegHerwigpp", "", "tree", "overallNormHistoSysOneSide"))
    if zlFitterConfig.datadriven:
        topLooseSample.addSystematic(Systematic("fragmentationTop","" , "_PowhegHerwigpp", "", "tree", "overallNormHistoSysOneSide"))
        topVeryLooseSample.addSystematic(Systematic("fragmentationTop","" , "_PowhegHerwigpp", "", "tree", "overallNormHistoSysOneSide"))

#--------------------------
# W
#--------------------------
wSample = Sample(zlFitterConfig.wSampleName, kAzure+1)
wSample.setTreeName("W_SRAll")
wSample.setNormFactor("mu_"+zlFitterConfig.wSampleName, 1., 0., 500.)
wSample.setFileList(wFiles)
wSample.setStatConfig(zlFitterConfig.useStat)
if zlFitterConfig.datadriven:
    #For Loose Top Control Region
    wLooseSample = Sample(zlFitterConfig.wLooseSampleName, kAzure+1)
    wLooseSample.setTreeName("W_SRAll")
    wLooseSample.setNormFactor("mu_"+zlFitterConfig.wLooseSampleName, 1., 0., 500.)
    wLooseSample.setFileList(wFiles)
    wLooseSample.setStatConfig(zlFitterConfig.useStat)
    #For Very Loose Top Control Region
    wVeryLooseSample = Sample(zlFitterConfig.wVeryLooseSampleName, kAzure+1)
    wVeryLooseSample.setTreeName("W_SRAll")
    wVeryLooseSample.setNormFactor("mu_"+zlFitterConfig.wVeryLooseSampleName, 1., 0., 500.)
    wVeryLooseSample.setFileList(wFiles)
    wVeryLooseSample.setStatConfig(zlFitterConfig.useStat)

    #For W in Very Loose W Control Region
    CRWVLSample = Sample("W_CRWVL",kAzure+1)
    CRWVLSample.buildHisto([1],"CRWVL","cuts")
    CRWVLSample.addNormFactor("mu_Z",1,10000,0,False)
    CRWVLSample.addNormFactor("eff_WL",CoefficientsDict["CRWL"].Value,CoefficientsDict["CRWL"].Maxval ,CoefficientsDict["CRWL"].Minval,False)
    CRWVLSample.addNormFactor("eff_YtmtA",CoefficientsDict["CRYtmtA"].Value,CoefficientsDict["CRYtmtA"].Maxval ,CoefficientsDict["CRYtmtA"].Minval,False)
    CRWVLSample.addNormFactor("eff_ZllVL",CoefficientsDict["CRZllVL"].Value,CoefficientsDict["CRZllVL"].Maxval ,CoefficientsDict["CRZllVL"].Minval,False)

    if not zlFitterConfig.meffABCD:
        #For W in Loose W Control Region
        CRWLSample = Sample("W_CRWL",kAzure+1)
        CRWLSample.buildHisto([1],"CRWL","cuts")
        CRWLSample.addNormFactor("mu_Z",1,10000,0,False)
        CRWLSample.addNormFactor("eff_WL",CoefficientsDict["CRWL"].Value,CoefficientsDict["CRWL"].Maxval ,CoefficientsDict["CRWL"].Minval,False)
        CRWLSample.addNormFactor("eff_YL",CoefficientsDict["CRYL"].Value,CoefficientsDict["CRYL"].Maxval ,CoefficientsDict["CRYL"].Minval,False)
        CRWLSample.addNormFactor("eff_YtmtA",CoefficientsDict["CRYtmtA"].Value,CoefficientsDict["CRYtmtA"].Maxval ,CoefficientsDict["CRYtmtA"].Minval,False)
        CRWLSample.addNormFactor("R_ZperW",CoefficientsDict["R_ZperW"].Value,CoefficientsDict["R_ZperW"].Maxval ,CoefficientsDict["R_ZperW"].Minval,False)
        #CRWLSample.addNormFactor("eff_YlmlA",CoefficientsDict["CRYlmlA"].Value,CoefficientsDict["CRYlmlA"].Maxval ,CoefficientsDict["CRYlmlA"].Minval,False)
    else:
        #For W in Loose W Control Region
        CRWLSample = Sample("W_CRWL",kAzure+1)
        CRWLSample.buildHisto([1],"CRWL","cuts")
        CRWLSample.addNormFactor("mu_Z",1,10000,0,False)
        CRWLSample.addNormFactor("eff_WL",CoefficientsDict["CRWL"].Value,CoefficientsDict["CRWL"].Maxval ,CoefficientsDict["CRWL"].Minval,False)
        CRWLSample.addNormFactor("eff_YL",CoefficientsDict["CRYL"].Value,CoefficientsDict["CRYL"].Maxval ,CoefficientsDict["CRYL"].Minval,False)
        CRWLSample.addNormFactor("eff_YtmtA",CoefficientsDict["CRYtmtA"].Value,CoefficientsDict["CRYtmtA"].Maxval ,CoefficientsDict["CRYtmtA"].Minval,False)
        CRWLSample.addNormFactor("R_ZperW",CoefficientsDict["R_ZperW"].Value,CoefficientsDict["R_ZperW"].Maxval ,CoefficientsDict["R_ZperW"].Minval,False)
        """
        CRWLSample.addNormFactor("eff_YtmtA",CoefficientsDict["CRYtmtA"].Value,CoefficientsDict["CRYtmtA"].Maxval ,CoefficientsDict["CRYtmtA"].Minval,False)
        CRWLSample.addNormFactor("eff_YtmlA",CoefficientsDict["CRYtmlA"].Value,CoefficientsDict["CRYtmlA"].Maxval ,CoefficientsDict["CRYtmlA"].Minval,False)
        CRWLSample.addNormFactor("eff_YlmtA",CoefficientsDict["CRYlmtA"].Value,CoefficientsDict["CRYlmtA"].Maxval ,CoefficientsDict["CRYlmtA"].Minval,False)
        """
    #For W Constraint Region
if zlFitterConfig.doSetNormRegion:
    if "CRT" in zlFitterConfig.constrainingRegionsList and "CRW" in zlFitterConfig.constrainingRegionsList:
        wSample.setNormRegions([("CRT", zlFitterConfig.binVar),("CRW", zlFitterConfig.binVar)])

    #For W Systematics
if not zlFitterConfig.usePrecomputedWGeneratorSys:
    wSample.addSystematic(Systematic("generatorW", "", "_Madgraph", "", "tree", "overallNormHistoSysOneSide"))
    if zlFitterConfig.datadriven:
        wLooseSample.addSystematic(Systematic("generatorW", "", "_Madgraph", "", "tree", "overallNormHistoSysOneSide"))
        wVeryLooseSample.addSystematic(Systematic("generatorW", "", "_Madgraph", "", "tree", "overallNormHistoSysOneSide"))

#--------------------------
# Gamma
#--------------------------
gammaSample = Sample(zlFitterConfig.gammaSampleName,kYellow)
gammaSample.setTreeName("GAMMA_SRAll")
gammaSample.setNormFactor("mu_"+zlFitterConfig.zSampleName,1.,0.,500.)
gammaSample.setFileList(gammaFiles)
gammaSample.setStatConfig(zlFitterConfig.useStat)
if not zlFitterConfig.usePrecomputedZGeneratorSys:
    gammaSample.addSystematic(Systematic("generatorZ", "_TRUTH", "_TRUTH_MadGraph", "", "tree", "overallNormHistoSysOneSide"))



if zlFitterConfig.doSetNormRegion:
    if "CRY" in zlFitterConfig.constrainingRegionsList:
        gammaSample.setNormRegions([("CRY", zlFitterConfig.binVar)])
if zlFitterConfig.datadriven:
    #sample for photon CR similar to SR cut
    CRYtmtASample = Sample("GAMMA_CRYtmtA",kYellow)
    CRYtmtASample.buildHisto([1],"CRYtmtA","cuts",0.5)
    CRYtmtASample.addNormFactor("mu_Z",1,10000,0,False)
    CRYtmtASample.addNormFactor("eff_YtmtA",CoefficientsDict["CRYtmtA"].Value,CoefficientsDict["CRYtmtA"].Maxval ,CoefficientsDict["CRYtmtA"].Minval,False)

    CRYLSample = Sample("GAMMA_CRYL",kYellow)
    CRYLSample.buildHisto([1],"CRYL","cuts")
    CRYLSample.addNormFactor("mu_Z",1,10000,0,False)
    CRYLSample.addNormFactor("eff_YtmtA",CoefficientsDict["CRYtmtA"].Value,CoefficientsDict["CRYtmtA"].Maxval ,CoefficientsDict["CRYtmtA"].Minval,False)
    CRYLSample.addNormFactor("eff_YL",CoefficientsDict["CRYL"].Value,CoefficientsDict["CRYL"].Maxval ,CoefficientsDict["CRYL"].Minval,False)
    CRYLSample.addNormFactor("R_YperZ",CoefficientsDict["R_YperZ"].Value,CoefficientsDict["R_YperZ"].Maxval ,CoefficientsDict["R_YperZ"].Minval,False)

    if not zlFitterConfig.meffABCD:
        #sample for loose meff loose Ap region
        CRYlmlASample = Sample("GAMMA_CRYlmlA",kYellow)
        CRYlmlASample.buildHisto([1],"CRYlmlA","cuts",0.5)
        CRYlmlASample.addNormFactor("mu_Z",1,10000,0,False)
        CRYlmlASample.addNormFactor("eff_YlmlA",CoefficientsDict["CRYlmlA"].Value,CoefficientsDict["CRYlmlA"].Maxval ,CoefficientsDict["CRYlmlA"].Minval,False)
    else:
        #sample for tight meff loose Ap region
        CRYtmlASample = Sample("GAMMA_CRYtmlA",kYellow)
        CRYtmlASample.buildHisto([1],"CRYtmlA","cuts",0.5)
        CRYtmlASample.addNormFactor("mu_Z",1,10000,0,False)
        CRYtmlASample.addNormFactor("eff_YtmlA",CoefficientsDict["CRYtmlA"].Value,CoefficientsDict["CRYtmlA"].Maxval ,CoefficientsDict["CRYtmlA"].Minval,False)
        CRYtmlASample.addNormFactor("eff_YtmtA",CoefficientsDict["CRYtmtA"].Value,CoefficientsDict["CRYtmtA"].Maxval ,CoefficientsDict["CRYtmtA"].Minval,False)

        #sample for loose meff tight Ap region
        CRYlmtASample = Sample("GAMMA_CRYlmtA",kYellow)
        CRYlmtASample.buildHisto([1],"CRYlmtA","cuts",0.5)
        CRYlmtASample.addNormFactor("mu_Z",1,10000,0,False)
        CRYlmtASample.addNormFactor("eff_YlmtA",CoefficientsDict["CRYlmtA"].Value,CoefficientsDict["CRYlmtA"].Maxval ,CoefficientsDict["CRYlmtA"].Minval,False)
        CRYlmtASample.addNormFactor("eff_YtmtA",CoefficientsDict["CRYtmtA"].Value,CoefficientsDict["CRYtmtA"].Maxval ,CoefficientsDict["CRYtmtA"].Minval,False)

        #sample for loose meff loose Ap region
        CRYlmlASample = Sample("GAMMA_CRYlmlA",kYellow)
        CRYlmlASample.buildHisto([1],"CRYlmlA","cuts",0.5)
        CRYlmlASample.addNormFactor("mu_Z",1,10000,0,False)
        CRYlmlASample.addNormFactor("eff_YlmtA",CoefficientsDict["CRYlmtA"].Value,CoefficientsDict["CRYlmtA"].Maxval ,CoefficientsDict["CRYlmtA"].Minval,False)
        CRYlmlASample.addNormFactor("eff_YtmlA",CoefficientsDict["CRYtmlA"].Value,CoefficientsDict["CRYtmlA"].Maxval ,CoefficientsDict["CRYtmlA"].Minval,False)
        CRYlmlASample.addNormFactor("eff_YtmtA",CoefficientsDict["CRYtmtA"].Value,CoefficientsDict["CRYtmtA"].Maxval ,CoefficientsDict["CRYtmtA"].Minval,False)


#--------------------------
# Z
#--------------------------
zSample = Sample(zlFitterConfig.zSampleName, kBlue)
zSample.setTreeName("Z_SRAll")
zSample.setNormFactor("mu_"+zlFitterConfig.zSampleName, 1., 0., 500.)
zSample.setFileList(zFiles)
zSample.setStatConfig(zlFitterConfig.useStat)

if zlFitterConfig.datadriven:
    zLooseSample = Sample(zlFitterConfig.zLooseSampleName, kBlue)
    zLooseSample.setTreeName("Z_SRAll")
    zLooseSample.setNormFactor("mu_"+zlFitterConfig.zLooseSampleName, 1., 0., 500.)
    zLooseSample.setFileList(zFiles)
    zLooseSample.setStatConfig(zlFitterConfig.useStat)

    zVeryLooseSample = Sample(zlFitterConfig.zVeryLooseSampleName, kBlue)
    zVeryLooseSample.setTreeName("Z_SRAll")
    zVeryLooseSample.setNormFactor("mu_"+zlFitterConfig.zLooseSampleName, 1., 0., 500.)
    zVeryLooseSample.setFileList(zFiles)
    zVeryLooseSample.setStatConfig(zlFitterConfig.useStat)

    #for SR Znunu BG events
    zSRSample  = Sample("Z_SR",kBlue)
    zSRSample.buildHisto([1],"SR","cuts")
    zSRSample.setNormFactor("mu_Z",1,0,10000)

    #for Very Loose Zll events
    CRZllVLSample = Sample("Z_CRZllVL",kBlue)
    CRZllVLSample.buildHisto([1],"CRZllVL","cuts")
    CRZllVLSample.addNormFactor("mu_Z",1,10000,0,False)
    CRZllVLSample.addNormFactor("eff_ZllVL",CoefficientsDict["CRZllVL"].Value,CoefficientsDict["CRZllVL"].Maxval ,CoefficientsDict["CRZllVL"].Minval,False)
    CRZllVLSample.addNormFactor("SF_llpernunu",CoefficientsDict["SF_llpernunu"].Value,CoefficientsDict["SF_llpernunu"].Maxval ,CoefficientsDict["SF_llpernunu"].Minval,False)

    #for validation region
    if "VRZf" in zlFitterConfig.datadrivenValidationRegionsList:
        VRZfSample = Sample("Z_VRZf",kBlue)
        VRZfSample.buildHisto([1],"VRZf","cuts")
        VRZfSample.addNormFactor("mu_Z",1,10000,0,False)
        VRZfSample.addNormFactor("SF_llpernunu",CoefficientsDict["SF_llpernunu"].Value,CoefficientsDict["SF_llpernunu"].Maxval ,CoefficientsDict["SF_llpernunu"].Minval,False)
    if "VRZVL" in zlFitterConfig.datadrivenValidationRegionsList:
        VRZVLSample = Sample("Z_VRZVL",kBlue)
        VRZVLSample.buildHisto([1],"VRZVL","cuts")
        VRZVLSample.addNormFactor("mu_Z",1,10000,0,False)
        VRZVLSample.addNormFactor("eff_ZllVL",CoefficientsDict["CRZllVL"].Value,CoefficientsDict["CRZllVL"].Maxval ,CoefficientsDict["CRZllVL"].Minval,False)
    if "VRZL" in zlFitterConfig.datadrivenValidationRegionsList:
        VRZLSample = Sample("Z_VRZL",kBlue)
        VRZLSample.buildHisto([1],"VRZL","cuts")
        VRZLSample.addNormFactor("mu_Z",1,10000,0,False)
        VRZLSample.addNormFactor("eff_YL",CoefficientsDict["CRYL"].Value,CoefficientsDict["CRYL"].Maxval ,CoefficientsDict["CRYL"].Minval,False)
    if zlFitterConfig.meffABCD:
        if "VRZlmlA" in zlFitterConfig.datadrivenValidationRegionsList:
            VRZlmlASample = Sample("Z_VRZlmlA",kBlue)
            VRZlmlASample.buildHisto([1],"VRZlmlA","cuts")
            VRZlmlASample.addNormFactor("mu_Z",1,10000,0,False)
            VRZlmlASample.addNormFactor("eff_YlmtA",CoefficientsDict["CRYlmtA"].Value,CoefficientsDict["CRYlmtA"].Maxval ,CoefficientsDict["CRYlmtA"].Minval,False)
            VRZlmlASample.addNormFactor("eff_YtmlA",CoefficientsDict["CRYtmlA"].Value,CoefficientsDict["CRYtmlA"].Maxval ,CoefficientsDict["CRYtmlA"].Minval,False)

if zlFitterConfig.doSetNormRegion:
    if "CRY" in zlFitterConfig.constrainingRegionsList:
        zSample.setNormRegions([("CRY", zlFitterConfig.binVar)])
        zSample.normSampleRemap = "GAMMAjets"
    if "CRZllL" in zlFitterConfig.constrainingRegionsList:
        zLooseSample.setNormRegions([("CRZllL", zlFitterConfig.binVar)])
if not zlFitterConfig.usePrecomputedZGeneratorSys:
    zSample.addSystematic(Systematic("generatorZ", "", "_Madgraph", "", "tree", "overallNormHistoSysOneSide"))
    if zlFitterConfig.datadriven:
        ZLooseSample.addSystematic(Systematic("generatorZ","" , "_Madgraph", "", "tree", "overallNormHistoSysOneSide"))
        ZVeryLooseSample.addSystematic(Systematic("generatorZ","" , "_Madgraph", "", "tree", "overallNormHistoSysOneSide"))


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
if zlFitterConfig.useShapeFit and zlFitterConfig.useShapeFactor and not zlFitterConfig.datadriven:
    topSample.addShapeFactor("topShape")
    wSample.addShapeFactor("wShape")
    zSample.addShapeFactor("zShape")
    gammaSample.addShapeFactor("gammaShape")
    qcdSample.addShapeFactor("qcdShape")


#######################################################################
# Apply systematics
#######################################################################

# Here be systematics. Sometime in future.
sysWeight_theoSysSigUp = myreplace(configMgr.weights, ["normWeightUp"], "normWeight")
sysWeight_theoSysSigDown = myreplace(configMgr.weights, ["normWeightDown"], "normWeight")
theoSysSig = Systematic("SigXSec", configMgr.weights, sysWeight_theoSysSigUp, sysWeight_theoSysSigDown, "weight", "overallSys")


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
    """
    if zlFitterConfig.datadriven:
        meas.addPOI("mu_Z")
    """

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

    if "CRQ" not in zlFitterConfig.constrainingRegionsList:
        meas.addParamSetting("mu_"+zlFitterConfig.qcdSampleName, True, 1) # fix QCD
    if "CRY" not in zlFitterConfig.constrainingRegionsList:
        meas.addParamSetting("mu_"+zlFitterConfig.zSampleName, True, 1)
    if "CRW" not in zlFitterConfig.constrainingRegionsList:
        meas.addParamSetting("mu_"+zlFitterConfig.wSampleName, True, 1)
    if "CRT" not in zlFitterConfig.constrainingRegionsList:
        meas.addParamSetting("mu_"+zlFitterConfig.topSampleName, True, 1)
    if "CRWL" in zlFitterConfig.constrainingRegionsList:
        meas.addParamSetting("mu_"+zlFitterConfig.wLooseSampleName, True, 1)
    if "CRWVL" in zlFitterConfig.constrainingRegionsList:
        meas.addParamSetting("mu_"+zlFitterConfig.wVeryLooseSampleName, True, 1)
    """
    if "CRZllL" in zlFitterConfig.constrainingRegionsList:
        meas.addParamSetting("mu_"+zlFitterConfig.zLooseSampleName, True, 1)
    """
    if "CRZllVL" in zlFitterConfig.constrainingRegionsList:
        meas.addParamSetting("mu_"+zlFitterConfig.zVeryLooseSampleName, True, 1)
    """
    if zlFitterConfig.datadriven:
        for regionName in zlFitterConfig.datadrivenRegionsList:
            meas.addParamSetting("mu_dummy_"+regionName,True,1)
    """
    #-------------------------------------------------
    # add Samples to the configuration
    #-------------------------------------------------
    if not zlFitterConfig.datadriven:
        allSamplesList = [topSample, wSample, zSample, dataSample]
        if zlFitterConfig.useDIBOSONsample:
            allSamplesList += [dibosonSample]
        myFitConfig.addSamples(allSamplesList)
    else:
        allSamplesList = [dataSample]
        if zlFitterConfig.useDIBOSONsample:
            allSamplesList += [dibosonSample]
        myFitConfig.addSamples(allSamplesList)


    #-------------------------------------------------
    # Signal sample
    #-------------------------------------------------
    sigSampleName = "%s_%s" % (grid, point)

    if myFitType == FitType.Exclusion or (myFitType == FitType.Discovery and zlFitterConfig.useSignalInBlindedData==True):

        sigSample = Sample(sigSampleName, kRed)
        sigSample.setFileList([os.path.join(INPUTDIR_SIGNAL, grid+".root")])
        sigSample.setTreeName("%s_%s_SRAll" % (gridTreeName, point) )
        sigSample.setNormByTheory()
        sigSample.setNormFactor("mu_SIG", 1, 0., 100.)
        sigSample.addSystematic(theoSysSig)
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

        #select only regions with photons
        if treeBaseName not in ["CRY"]:
            continue

        extraWeightList = regionDict[regionName].extraWeightList

        # Gamma control region
        if (not zlFitterConfig.useShapeFit) or zlFitterConfig.datadriven :
            REGION = myFitConfig.addChannel("cuts", [regionName], 1, 0.5, 1.5)
        else:
            REGION = myFitConfig.addChannel(zlFitterConfig.binVar, [regionName], zlFitterConfig.nBins, zlFitterConfig.minbin, zlFitterConfig.maxbin)
            REGION.useOverflowBin = True
            REGION.useUnderflowBin = False
        if not zlFitterConfig.datadriven:
            REGION.addSample(gammaSample, 0) ##order is important!!!!
        else:
            if regionName in ["CRYtmtA","CRYtmlA"]:
                REGION.addSample(wSample)
                REGION.addSample(topSample)
            elif regionName in ["CRYlmlA","CRYlmtA","CRYL"]:
                REGION.addSample(wLooseSample)
                REGION.addSample(topLooseSample)
        for sam in REGION.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll", treeBaseName))
            if "Data" in sam.treeName:
                #sam.setFileList(dataFiles)
                pass
            if "GAMMA" in sam.name: #ATT: should define to which samples the extra-weight should be applied
                for extraWeight in extraWeightList:
                    sam.addWeight(extraWeight)
        #for datadriven
        if zlFitterConfig.datadriven:
            if regionName in zlFitterConfig.datadrivenRegionsList:
                if "CRYL" == regionName:
                    REGION.addSample(CRYLSample)
                if not zlFitterConfig.meffABCD:
                    #this region become CR for not ABCD
                    if "CRYtmtA" == regionName:
                        REGION.addSample(CRYtmtASample)
                    if "CRYlmlA" == regionName:
                        REGION.addSample(CRYlmlASample)
                else:
                    if "CRYlmtA" == regionName:
                        REGION.addSample(CRYlmtASample)
                    if "CRYtmlA" == regionName:
                        REGION.addSample(CRYtmlASample)
                    if "CRYlmlA" == regionName:
                        REGION.addSample(CRYlmlASample)
            if doValidation and regionName in zlFitterConfig.datadrivenValidationRegionsList:
                #this region become validation region if  ABCD
                if "CRYtmtA" == regionName:
                    REGION.addSample(CRYtmtASample)

        # set region type
        if regionName in zlFitterConfig.constrainingRegionsList:
            # add as a constraining region
            myFitConfig.setBkgConstrainChannels(REGION)
        else:
            myFitConfig.setValidationChannels(REGION)

    ######################################################################
    # Signal Regions
    ######################################################################
    if not zlFitterConfig.useShapeFit or zlFitterConfig.datadriven:
        #SR_loose = myFitConfig.addChannel("cuts", ["SR_meffcut_relaxed"], 1, 0.5, 1.5)

        SR = myFitConfig.addChannel("cuts", [zlFitterConfig.SRName], 1, 0.5, 1.5)
        #SR.remapSystChanName = "cuts_SR_meffcut_relaxed"
    else:
        SR = myFitConfig.addChannel(zlFitterConfig.binVar, [zlFitterConfig.SRName], zlFitterConfig.nBins, zlFitterConfig.minbin, zlFitterConfig.maxbin)
        SR.useOverflowBin = True
        SR.useUnderflowBin = False

    #for datadriven BG estimation
    if zlFitterConfig.datadriven:
        SR.addSample(zSRSample)
        SR.addSample(topSample)
        SR.addSample(wSample)
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
        if regionName in ["VRWtmtA","VRWtmlA","VRWlmtA","VRWlmlA"]:
            continue

        #setup region
        if (not zlFitterConfig.useShapeFit ) or zlFitterConfig.datadriven:
            REGION = myFitConfig.addChannel("cuts", [regionName], 1, 0.5, 1.5)
        else:
            REGION = myFitConfig.addChannel(zlFitterConfig.binVar, [regionName], zlFitterConfig.nBins, zlFitterConfig.minbin, zlFitterConfig.maxbin)
            REGION.useOverflowBin = True
            REGION.useUnderflowBin = False

        #add monte carlo samples for datadriven
        if zlFitterConfig.datadriven:
            if regionName in ["CRW","CRT","VRWf","VRTf","VRWM","VRTM","VRWMf","VRTMf","VRZ"]:
                REGION.addSample(topSample)
                REGION.addSample(wSample)
                REGION.addSample(zSample)
            if regionName in ["VRZf"]:
                REGION.addSample(topSample)
                REGION.addSample(wSample)
            if regionName in ["CRWL","CRTL","CRZllL"]:
                REGION.addSample(topLooseSample)
                REGION.addSample(zLooseSample)
                if regionName in ["CRTL","CRZllL"]:
                    REGION.addSample(wLooseSample)
            if regionName in ["CRWVL","CRTVL","CRZllVL"]:
                REGION.addSample(topVeryLooseSample)
                if regionName in ["CRWVL","CRTVL"]:
                    REGION.addSample(zVeryLooseSample)
                if regionName in ["CRZllVL","CRTVL"]:
                    REGION.addSample(wVeryLooseSample)


        #set the treename
        for sam in REGION.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll", treeBaseName))
            if "Data" in sam.treeName:
                #sam.setFileList(dataFiles)
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

            for sam in REGION.sampleList:
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



        #add monte carlo samples for datadriven
        if zlFitterConfig.datadriven:
            if regionName in zlFitterConfig.datadrivenRegionsList:
                if "CRZllVL" == regionName:
                    REGION.addSample(CRZllVLSample)
                if "CRWVL" == regionName:
                    REGION.addSample(CRWVLSample)
                if "CRWL" == regionName:
                    REGION.addSample(CRWLSample)
            #add validation region for datadriven method
            if regionName=="VRZf" and regionName in zlFitterConfig.datadrivenValidationRegionsList:
                REGION.addSample(VRZfSample)

        # set region type
        if regionName in zlFitterConfig.constrainingRegionsList:
            myFitConfig.setBkgConstrainChannels(REGION)
        else:
            myFitConfig.setValidationChannels(REGION)


    ######################################################################
    # Regions for QCD
    ######################################################################

    for regionName in zlFitterConfig.allRegionsList():

        #select region for QCD
        if not "RQ" in regionName:
            continue

        treeBaseName = regionDict[regionName].suffixTreeName

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
        if zlFitterConfig.useDDQCDsample and zlFitterConfig.useMCQCDsample:
            REGION.addSample(qcdSample)


    ######################################################################
    # Validation Regions for 0-lepton
    ######################################################################
    for regionName in zlFitterConfig.allRegionsList():
        if not zlFitterConfig.datadriven:
            break
        if not regionName in zlFitterConfig.datadrivenValidationRegionsList:
            continue
        if not regionName in ["VRZVL","VRZL","VRZlmlA"]:
            continue
        REGION = myFitConfig.addChannel("cuts", [regionName], 1, 0.5, 1.5)
        if regionName in ["VRZVL"]:
            REGION.addSample(topVeryLooseSample)
            REGION.addSample(wVeryLooseSample)
            REGION.addSample(VRZVLSample)
        if regionName in ["VRZL"] and zlFitterConfig.meffABCD:
            REGION.addSample(topLooseSample)
            REGION.addSample(wLooseSample)
            REGION.addSample(VRZLSample)
        if regionName in ["VRZlmlA"] and zlFitterConfig.meffABCD:
            REGION.addSample(topLooseSample)
            REGION.addSample(wLooseSample)
            REGION.addSample(VRZlmlASample)
        myFitConfig.setValidationChannels(REGION)

    ###############################################################
    # add Precomputed error in all VR and SR
    # These uncertainties correspond to the uncertainty on the TF
    # That's why they are not added in the control regions
    ###############################################################

    if zlFitterConfig.usePrecomputedError:
        for REGION in myFitConfig.channels:
            if REGION.regionString in zlFitterConfig.constrainingRegionsList:
                continue

            for sam in REGION.sampleList:
                if sam.name == sigSampleName:
                    #signal
                    #Needs to add theory uncertainty on signal acceptance for low-dM points
                    nameSys = "FlatSig"
                    #sam.addSystematic(Systematic(nameSys, configMgr.weights, 1+zlFitterConfig.flatErrorSignal, 1-zlFitterConfig.flatErrorSignal, "user", "userOverallSys"))
                elif sam.name == zlFitterConfig.zSampleName or sam.name == zlFitterConfig.zLooseSampleName or sam.name == zlFitterConfig.zVeryLooseSampleName:
                    # Z background
                    # generator
                    if zlFitterConfig.usePrecomputedZGeneratorSys:
                        errorGenerator = getError(channel.name, REGION.name.replace("cuts_", ""), zTheoSysGeneratorDict)
                        sam.addSystematic(Systematic("GeneratorZ", configMgr.weights, 1+errorGenerator, 1-errorGenerator, "user", "userOverallSys"))
                    #Kappa
                        if zlFitterConfig.applyKappaCorrection:
                            kappaError=0.066
                            sam.addSystematic(Systematic("Kappa", configMgr.weights, 1+kappaError, 1-kappaError, "user", "userOverallSys"))

                elif sam.name == zlFitterConfig.wSampleName or sam.name == zlFitterConfig.wLooseSampleName or sam.name == zlFitterConfig.wVeryLooseSampleName:
                    # W background
                    # generator
                    if zlFitterConfig.usePrecomputedWGeneratorSys:
                        errorGenerator = getError(channel.name, REGION.name.replace("cuts_", ""), wTheoSysGeneratorDict)
                        sam.addSystematic(Systematic("GeneratorW", configMgr.weights, 1+errorGenerator, 1-errorGenerator, "user", "userOverallSys"))
                elif sam.name == zlFitterConfig.topSampleName or sam.name == zlFitterConfig.topLooseSampleName or sam.name == zlFitterConfig.topVeryLooseSampleName:
                    # Top background
                    # generator
                    if zlFitterConfig.usePrecomputedTopGeneratorSys:
                        errorGenerator = getError(channel.name, REGION.name.replace("cuts_", ""), topTheoSysGeneratorDict)
                        sam.addSystematic(Systematic("GeneratorTop", configMgr.weights, 1+errorGenerator, 1-errorGenerator, "user", "userOverallSys"))

                    # A14 uncertainty
                    errorA14 = getError(channel.name, REGION.name.replace("cuts_", ""), topTheoSysA14Dict)
                    sam.addSystematic(Systematic("TopTuneA14", configMgr.weights, 1+errorA14, 1-errorA14, "user", "userOverallSys"))

                    # PowhegHerwig
                    if zlFitterConfig.usePrecomputedTopFragmentationSys:
                        errorPowhegHerwig = getError(channel.name, REGION.name.replace("cuts_", ""), topTheoSysPowhegHerwigDict)
                        sam.addSystematic(Systematic("FragmentationTop", configMgr.weights, 1+errorPowhegHerwig, 1-errorPowhegHerwig, "user", "userOverallSys"))
                    # radiation
                    errorRad = getError(channel.name, REGION.name.replace("cuts_", ""), topTheoSysRadDict)
                    sam.addSystematic(Systematic("TopRadiation", configMgr.weights, 1+errorRad[0], 1-errorRad[1], "user", "userOverallSys"))
                # diboson
                elif sam.name == zlFitterConfig.dibosonSampleName:
                    error = 0
                    if (channel.name, REGION.name.replace("cuts_", "")) in dibosonFlatSysDict.keys():
                        error = dibosonFlatSysDict[(channel.name,REGION.name.replace("cuts_",""))]
                    elif ("default", "default") in dibosonFlatSysDict.keys():
                        error = dibosonFlatSysDict[("default","default")]
                    sam.addSystematic(Systematic("FlatDiboson", configMgr.weights, 1+error, 1-error, "user", "userOverallSys"))

                    #continue

    ###############################################################
    # Add systematics
    ###############################################################

    # JET systematics
    jetSystematicList = []

    # JER systematics
    # ATT: Not sure that it should be symmetrized
    jetSystematicList.append(Systematic("JER", "", "_JET_JER_SINGLE_NP_1up", "", "tree", "overallNormHistoSysOneSide"))

    # JES systematics
    jesSystematicStrList = [
        "JET_GroupedNP_1",
        "JET_GroupedNP_2",
        "JET_GroupedNP_3",
        ]

    for jesSysStr in jesSystematicStrList:
        jetSystematicList.append(Systematic(jesSysStr, "", "_"+jesSysStr+"_1up", "_"+jesSysStr+"_1down", "tree", "overallNormHistoSys"))

    # MET systematics
    metSystematicList = []
    metSystematicList.append(Systematic("MET_SoftTrk_ResoPara", "", "_MET_SoftTrk_ResoPara", "", "tree", "overallNormHistoSysOneSide"))
    metSystematicList.append(Systematic("MET_SoftTrk_ResoPerp", "", "_MET_SoftTrk_ResoPerp", "", "tree", "overallNormHistoSysOneSide"))
    metSystematicList.append(Systematic("MET_SoftTrk_Scale", "", "_MET_SoftTrk_ScaleUp", "_MET_SoftTrk_ScaleDown", "tree", "overallNormHistoSys"))

    for REGION in myFitConfig.channels:
        for sam in REGION.sampleList:
            if  sam.name in zlFitterConfig.datadrivenSampleNameList:
                continue
            if  sam.name == "Z_VRZf":
                continue
            if zlFitterConfig.useJETUncertainties:
                for sys in jetSystematicList:
                    sam.addSystematic(sys)
            if zlFitterConfig.useMETUncertainties:
                for sys in metSystematicList:
                    sam.addSystematic(sys)

    ###############################################################
    # This is the end
    ###############################################################

