################################################################
## In principle all you have to setup is defined in this file ##
################################################################
from configManager import configMgr
from ROOT import kBlack,kWhite,kGray,kRed,kPink,kMagenta,kViolet,kBlue,kAzure,kCyan,kTeal,kGreen,kSpring,kYellow,kOrange
from configWriter import fitConfig,Measurement,Channel,Sample
from systematic import Systematic
from math import sqrt

from logger import Logger

import os

######################
# Results data
######################

results = {}

# key=region name => [exp, expUnc, obs]
results["SR2jl"] = [13000, 1000, 12315]
results["SR2jm"] = [760, 50, 715]
results["SR2jt"] = [125, 10, 133]
results["SR2jW"] = [2.1, 0.7, 0]
results["SR3j"] = [5.0, 1.3, 7]
results["SR4jl-"] = [2120, 130, 2169]
results["SR4jl"] = [630, 50, 608]
results["SR4jm"] = [37, 6, 24]
results["SR4jt"] = [2.51, 1.0, 0]
results["SR4jW"] = [14, 4, 16]
results["SR5j"] = [126, 16, 121]
results["SR6jl"] = [111, 15, 121]
results["SR6jm"] = [33, 6, 39]
results["SR6jt"] = [5.2, 1.5, 5]
results["SR6jt+"] = [4.9, 1.7, 6]

##########################

log = Logger('SimpleUL')
try:
    pickedSRs
except NameError:
    log.fatal("No region specified!")    

if len(pickedSRs) == 0:
    log.fatal("No region specified!")    

for SR in pickedSRs:

    if SR not in results:
        log.warning("SR %s not found in results dict!")
        time.sleep(3)

    ##########################

    # Set observed and expected number of events in counting experiment
    ndata     =  float(results[SR][2]) # Number of events observed in data
    if ndata == 0.0:
        ndata = 0.001

    nbkg      =  float(results[SR][0]) # Number of predicted bkg events
    nbkgErr   =  float(results[SR][1]) # (Absolute) Statistical error on bkg estimate

    lumiError = 0.028 	# Relative luminosity uncertainty

    ucb = Systematic("ucb", configMgr.weights, 1 + nbkgErr/nbkg, 1 - nbkgErr/nbkg, "user","userOverallSys")

    ##########################

    # Setting the parameters of the hypothesis test
    #configMgr.nTOYs=5000
    configMgr.calculatorType=2 # 2=asymptotic calculator, 0=frequentist calculator
    configMgr.testStatType=3   # 3=one-sided profile likelihood test statistic (LHC default)
    configMgr.nPoints=20       # number of values scanned of signal-strength for upper-limit determination of signal strength.

    ##########################

    # Give the analysis a name
    configMgr.analysisName = "SimpleUL_%s" % SR
    configMgr.outputFileName = "results/%s_Output.root"%configMgr.analysisName

    # Define cuts
    configMgr.cutsDict["UserRegion"] = "1."

    # Define weights
    configMgr.weights = "1."

    # Define samples
    bkgSample = Sample("Bkg",kGreen-9)
    bkgSample.setStatConfig(False)
    bkgSample.buildHisto([nbkg],"UserRegion","cuts")
    #bkgSample.buildStatErrors([nbkgErr],"UserRegion","cuts")
    #bkgSample.addSystematic(corb)
    bkgSample.addSystematic(ucb)

    dataSample = Sample("Data",kBlack)
    dataSample.setData()
    dataSample.buildHisto([ndata],"UserRegion","cuts")

    # Define top-level
    ana = configMgr.addFitConfig("SPlusB")
    ana.addSamples([bkgSample,dataSample])
    #ana.setSignalSample(sigSample)

    # Define measurement
    meas = ana.addMeasurement(name="NormalMeasurement",lumi=1.0,lumiErr=lumiError)
    meas.addPOI("mu_Sig")
    meas.addParamSetting("Lumi",True,1)

    # Add the channel
    chan = ana.addChannel("cuts",["UserRegion"],1,0.,1.)
    chan.addDiscoverySamples(["SIG"], [1.], [0.], [1000.], [kMagenta])
    ana.setSignalChannels([chan])

    # These lines are needed for the user analysis to run
    # Make sure file is re-made when executing HistFactory
    if configMgr.executeHistFactory:
        if os.path.isfile("data/%s.root" % configMgr.analysisName):
            os.remove("data/%s.root" % configMgr.analysisName) 
