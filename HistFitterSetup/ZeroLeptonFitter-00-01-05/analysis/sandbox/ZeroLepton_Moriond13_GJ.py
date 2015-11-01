################################################################
##
## Moriond 2013 0-lepton analysis
##
################################################################

from configManager import configMgr
from ROOT import kBlack, kWhite, kGray, kRed, kPink, kMagenta, kViolet, kBlue, kAzure, kCyan, kTeal, kGreen, kSpring, kYellow, kOrange
from configWriter import TopLevelXML, Measurement, ChannelXML, Sample
from logger import Logger
from systematic import Systematic
from math import sqrt
import os
import sys
import pickle
import pprint
import time

log = Logger("ZeroLeptonFitter")
log.info("ZeroLeptonFitter says hi!")

#----------------------------------------------
# some useful functions
#----------------------------------------------
def myreplace(l1, l2, element):
    idx = l1.index(element)
    if idx >= 0:
        return l1[:idx] + l2 + l1[idx+1:]
    
    print "WARNING idx negative"
    return l1

def wait(sec):
    os.system('setterm -cursor off')
    while sec > 0:
        sys.stdout.write(str(sec) + '...     \r')
        sys.stdout.flush()
        sec -= 1
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            os.system('setterm -cursor on')
            print
            sys.exit()
    os.system('setterm -cursor on')

#-------------------------------
# Analysis parameters
#-------------------------------

configMgr.blindSR = False    # Blind the SRs only
configMgr.fixSigXSec = True # Run fits with also with up and down theor. uncert.? False: add uncert. as fit parameter
configMgr.runOnlyNominalXSec = True # only run nominal fit if fixSigXSec=True ?

useCRWTY = True             # use control regions for Top, W and Z background
useCRQ = True               # use control region for QCD background
useQCDsample = True         # include QCD sample

# Apply a user-defined errBG to the background errors? (Useful if setting everything to MC pred)
useFlatBkgError = False

# Use shape fit (false=cut&count)?
useShapeFit = True

useQCDMethodSyst = False     # use systematics from sheffield method otherwise use theoSysQCDNumber
useSyst = True              # use systematical uncertainties (jes, jer, theo, ...)
useISRSyst = True           # use ISR syst (effect only for SM* grids)
useStat = True              # use stat uncertainties on MC
useTheoSys = True           # use theoretical systematical uncertainties (jes, jer, theo, ...)
if useSyst == False:
    useTheoSys = False
    useISRSyst = False

# grid, with a default point and a default name
grid = "Gluino_Stop_charm"           
allpoints = ["450_400"] #close to the SM_GG diagonal
anaName = "test" 

theoSysQCDNumber = 0.99     # uncertainty on QCD background estimate

#-------------------------------
# Cuts
#-------------------------------
#default values; overwritten if set through command-line
chn = 0                   #analysis channel 0=A,1=B,..
level = 'loose'           #loose, medium, tight
meff = 00000              # final meff cut
met = 160000

# note that e.g. jet3pt and higher are ignored for SRA, jet4pt for SRB, etc.
jet1pt = 130000
jet2pt = 60000
jet3pt = 60000
jet4pt = 60000
jet5pt = 60000
jet6pt = 60000

metSig = 0
metomeff = 0.3            # final met/meff cut
dPhi = 0.

# final cuts dictionnary
metomeffDefault = (0.4, 0.25, 0.25, 0.20, 0.15)
selections={
    'loose' : [(0.4, 1000000),            None, (0.30, 1000000),            None, (0.30, 1000000)],
    'medium': [(0.4, 1300000), (0.30, 1300000), (0.30, 1300000),            None, (0.25, 1300000)],
    'tight' : [(0.3, 1900000), (0.25, 1900000), (0.25, 1900000), (0.15, 1700000), (0.15, 1400000)]
    }

#theo sys on bkg
#theoSysTopNumber=0.30
#theoSysWNumber=0.30
#theoSysZNumber=0.30
#if myFitType==FitType.Exclusion:
#    useQCD=False

#-------------------------------
# Options
#-------------------------------

# sigSamples is set by the "-g" HistFitter option    
try:
    sigSamples
except NameError:
    sigSamples = None
    
if sigSamples != None:
    if sigSamples[0].find("grid") >= 0: # first entry allowed to specify a grid name
        grid = sigSamples[0].replace("grid", "")
        allpoints = sigSamples[1:]
    else:
        allpoints = sigSamples
        
# pickedSRs is set by the "-r" HistFitter option    
try:
    pickedSRs
except NameError:
    pickedSRs = None
    
if pickedSRs != None and len(pickedSRs) >= 1: 
    if pickedSRs[0] == "SRA": chn = 0
    if pickedSRs[0] == "SRB": chn = 1
    if pickedSRs[0] == "SRC": chn = 2
    if pickedSRs[0] == "SRD": chn = 3
    if pickedSRs[0] == "SRE": chn = 4
    metomeff = metomeffDefault[chn]
    
    if len(pickedSRs) >= 2 and pickedSRs[1] in selections.keys():
        level = pickedSRs[1]
        meff = selections[pickedSRs[1]][chn][1]
        metomeff = selections[pickedSRs[1]][chn][0]
        anaName = pickedSRs[0]+pickedSRs[1]
    else:
        print pickedSRs
        anaName = pickedSRs[0]
        if len(pickedSRs) >= 2:
            meff = int(pickedSRs[1])*1000
            anaName += "-meff"+pickedSRs[1]
            print anaName
        if len(pickedSRs) >= 3:
            metomeff = float(pickedSRs[2])
            anaName += "-metomeff"+pickedSRs[2]
            print anaName
        if len(pickedSRs) >= 4:
            met = int(pickedSRs[3])*1000
            anaName += "-met"+pickedSRs[3]
            print anaName
        if len(pickedSRs) >= 5:
            jet1pt = int(pickedSRs[4])*1000
            anaName += "-jet1pt"+pickedSRs[4]
            print anaName
        if len(pickedSRs) >= 6:
            jet2pt = int(pickedSRs[5])*1000
            anaName += "-jet2pt"+pickedSRs[5] 
            print anaName  
        if len(pickedSRs) >= 7:
            jet3pt = int(pickedSRs[6])*1000
            anaName += "-jet3pt"+pickedSRs[6] 
            print anaName  
        if len(pickedSRs) >= 8:
            jet4pt = int(pickedSRs[7])*1000
            anaName += "-jet4pt"+pickedSRs[7] 
            print anaName    
        if len(pickedSRs) >= 9:
            jet5pt = int(pickedSRs[8])*1000
            anaName += "-jet5pt"+pickedSRs[8]   
        if len(pickedSRs) >= 10:
            jet6pt = int(pickedSRs[9])*1000
            anaName += "-jet6pt"+pickedSRs[9] 
            print anaName 
        if len(pickedSRs) >= 11:
            metSig = int(pickedSRs[10])
            anaName += "-metSig"+pickedSRs[10] 
            print anaName 
        if len(pickedSRs) >= 12:
            dPhi = float(pickedSRs[11])
            anaName += "-dPhi"+pickedSRs[11] 
            print anaName       
        
        # pick up shape fit settings. Note: anaName will get set below for if useShapeFit
        if len(pickedSRs) >= 13:
            minbin = int(pickedSRs[12])*1000
        if len(pickedSRs) >= 14:
            nBins = int(pickedSRs[13])

if meff == None or chn > 5 or chn < 0:
    print "ERROR analysis not defined!!!"
    print chn,meff
    print pickedSRs
    sys.exit()

#-------------------------------
# HistFitter options
#-------------------------------

# No input signal for discovery and bkg fit
# allpoints changed for naming of output files
if myFitType == FitType.Discovery:
    allpoints = ["Discovery"]
if myFitType == FitType.Background:
    allpoints = ["Background"]
    grid = ""

# Location of the ntuples ("Light" has the baseline cut applied already, preferred for speed)
#INPUTDIR = "/afs/cern.ch/atlas/groups/susy/0lepton/ZeroLeptonFitter/ZeroLepton-00-00-36/"
INPUTDIR = "/afs/cern.ch/atlas/groups/susy/0lepton/ZeroLeptonFitter/ZeroLepton-00-00-36_Light/"
INPUTDIR = "/users/staf/gbesjes/work/HistFitterNtuples/ZeroLepton-00-00-36_Light/"
INPUTDIR = "/glusterfs/atlas2/users/gbesjes/ZeroLepton-00-00-36_Light/"

INPUTDIR_SIGNAL = INPUTDIR 
#INPUTDIR_SIGNAL = "/afs/cern.ch/atlas/groups/susy/0lepton/ZeroLeptonFitter/ZeroLepton-00-00-36/"

#-------------------------------
# Parameters for hypothesis test
#-------------------------------
#configMgr.doHypoTest=False
configMgr.nTOYs = 5000      # number of toys when doing frequentist calculator
configMgr.doExclusion = False
if myFitType == FitType.Exclusion:
    configMgr.doExclusion = True 
configMgr.calculatorType = 2 # 2=asymptotic calculator, 0=frequentist calculator
configMgr.testStatType = 3   # 3=one-sided profile likelihood test statistic (LHC default)
configMgr.nPoints = 20       # number of values scanned of signal-strength for upper-limit determination of signal strength.

#-------------------------------------
# Now we start to build the data model
#-------------------------------------

# Scaling calculated by outputLumi / inputLumi
configMgr.inputLumi = 0.001 # Luminosity of input TTree after weighting
configMgr.outputLumi = 14.1 # Luminosity required for output histograms
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
    qcdFiles.append(INPUTDIR+"/QCDdd.root")
    dibosonFiles.append(INPUTDIR+"/Diboson.root")
    topFiles.append(INPUTDIR+"/Top.root")
    topFiles.append(INPUTDIR+"/TopSherpa.root")
    wFiles.append(INPUTDIR+"W.root")
    zFiles.append(INPUTDIR+"/Z.root")
    gammaFiles.append(INPUTDIR+"/GAMMA.root")
    dataFiles.append(INPUTDIR+"/DataJetTauEtmiss.root")
    dataCRWTFiles.append(INPUTDIR+"/DataEgamma.root")
    dataCRWTFiles.append(INPUTDIR+"/DataMuon.root")
     
# Tuples of nominal weights
configMgr.weights = ["genWeight", "pileupWeight", "normWeight"]

########################################
# Analysis description
########################################
base = "(veto==0 && nJet>=2 &&jet1Pt>" + str(jet1pt) + " && jet2Pt>" + str(jet2pt) + ")"

metCR = met
if metCR > 500*1000:
    metCR = 500*1000

metcut_SR = "(met>" + str(met) + " && dPhi>=" + str(dPhi) + " )"
metcut_CR = "(met>" + str(metCR) + ")" # the extra dphi cut is not applied to CR

baselineSR = [base,
            base + "&& (jet3Pt>" + str(jet3pt) + ")",
            base + "&& (jet3Pt>" + str(jet3pt) + " && jet4Pt>" + str(jet4pt) + ")",
            base + "&& (jet3Pt>" + str(jet3pt) + " && jet4Pt>" + str(jet4pt) + " && jet5Pt>" + str(jet5pt) + ")",
            base + "&& (jet3Pt>" + str(jet3pt) + " && jet4Pt>" + str(jet4pt) + " && jet5Pt>" + str(jet5pt) + " && jet6Pt>" + str(jet6pt) + ")"]

dphicut = ["(dPhi>0.4)",
         "(dPhi>0.4)",
         "(dPhi>0.4 && dPhiR>0.2)",
         "(dPhi>0.4 && dPhiR>0.2)",
         "(dPhi>0.4 && dPhiR>0.2)"]

invdphicut = ["(dPhi<0.2)",
            "(dPhi<0.2)",
            "(dPhi<0.2 || dPhiR<0.2)",
            "(dPhi<0.2 || dPhiR<0.2)",
            "(dPhi<0.2 || dPhiR<0.2)"]

metSigcut = "(met/1000/sqrt((meff2Jet-met)/1000)>=" + str(metSig) + ")"

metomeffcut = ["(met/meff2Jet>" + str(metomeff) + " && " + metSigcut + ")",
             "(met/meff3Jet>" + str(metomeff) + " && " + metSigcut + ")",
             "(met/meff4Jet>" + str(metomeff) + " && " + metSigcut + ")",
             "(met/meff5Jet>" + str(metomeff) + " && " + metSigcut + ")",
             "(met/meff6Jet>" + str(metomeff) + " && " + metSigcut + ")"]

metomeff_delta = 0.1
if metomeff >= 0.4:    
    metomeff_delta = 0.15
if metomeff <= 0.15:    
    metomeff_delta = 0.05
if (chn == 4 and metomeff >= 0.3):#sre,loose
    metomeff_delta = 0.15
    
metomeffcutqcd = ["(met/meff2Jet<" + str(metomeff) + ")&&(met/meff2Jet>" + str(metomeff-metomeff_delta) + ")",
                "(met/meff3Jet<" + str(metomeff) + ")&&(met/meff3Jet>" + str(metomeff-metomeff_delta) + ")",
                "(met/meff4Jet<" + str(metomeff) + ")&&(met/meff4Jet>" + str(metomeff-metomeff_delta) + ")",
                "(met/meff5Jet<" + str(metomeff) + ")&&(met/meff5Jet>" + str(metomeff-metomeff_delta) + ")",
                "(met/meff6Jet<" + str(metomeff) + ")&&(met/meff6Jet>" + str(metomeff-metomeff_delta) + ")"]

if metomeff == 0: 
    metomeffcutqcd = ["(1)"]*5

if useShapeFit:
    # Define the number of bins for the shape fit, and its range
    binVar = "meffInc"
   
    # use try/catch to see if nBins or minbin were set in the pickedSRs string
    try:
        nBins
    except NameError:
        nBins = 5
    
    try:
        minbin
    except NameError:
        minbin = meff-300000
        if pickedSRs[0] == "SRA": minbin = 1400000
        if pickedSRs[0] == "SRB": minbin = 1200000
        if pickedSRs[0] == "SRC": minbin = 1200000
        if pickedSRs[0] == "SRD": minbin = 1000000
        if pickedSRs[0] == "SRE": minbin = 900000

    maxbin = 1000000 + minbin ##meff + nbin*100000-300000 

    anaName += "-meffInc-nBins%d-%d-%d" % (nBins, minbin, maxbin)

    # needed for projection strings
    meffcut = "(meffInc>" + str(minbin) + ")"
else:
    #cut&count cuts
    binVar = "cuts" # for setNormRegions calls
    meffcut = "(meffInc>" + str(meff) + ")"

# Signal regions
configMgr.cutsDict["SR"]    = baselineSR[chn] + " && " + dphicut[chn] + " && " + metomeffcut[chn] + " && " + meffcut + " && " + metcut_SR

# Control regions
bjetveto="(nBJet==0)"
leptonVeto = "(nLep == 0)"
bjetcut ="(nBJet>0)"
photonSelection="(phQuality == 2 && phIso < 5000.)"

configMgr.cutsDict["CRW"]   = baselineSR[chn] + " && " + metcut_CR + " && " + meffcut + " && " + bjetveto
configMgr.cutsDict["CRT"] = baselineSR[chn] + " && " + metcut_CR + " && " + meffcut + " && " + bjetcut
configMgr.cutsDict["CRY"]  = baselineSR[chn] + " && " + metcut_CR + " && " + dphicut[chn] + " && " + metomeffcut[chn] + " && " + meffcut + "  &&  " + photonSelection  +  " && "  +  leptonVeto
configMgr.cutsDict["CRQCD"] = baselineSR[chn] + " && " + metcut_CR + " && jet1Pt>400000 &&" + invdphicut[chn] + " && " + metomeffcutqcd[chn] + " && " + meffcut

# Validation regions
configMgr.cutsDict["VRQ1"] = baselineSR[chn] + " && " + metcut_CR + " && " + invdphicut[chn] + " &&  " + metomeffcut[chn] + " && " + meffcut
configMgr.cutsDict["VRQ2"] = baselineSR[chn] + " && " + metcut_CR + " && " + dphicut[chn] + " && " + metomeffcutqcd[chn] + " && " + meffcut
configMgr.cutsDict["VRZ"]  = baselineSR[chn] + " && " + metcut_CR + " && " + meffcut
configMgr.cutsDict["VRT2L"] = configMgr.cutsDict["VRZ"] + " && mll>116000 &&  lep1Pt<200000 && lep2Pt<100000"
configMgr.cutsDict["VRZ_1c"] = configMgr.cutsDict["VRZ"]

configMgr.cutsDict["VRWT_P"]  = baselineSR[chn] + " && " + metcut_CR + " && " + meffcut + " && " + " lep1sign>0"
configMgr.cutsDict["VRWT_M"]  = baselineSR[chn] + " && " + metcut_CR + " && " + meffcut + " && " + " lep1sign<0"

# Similar to CRW,CRT and VRZ but with dphicut and met/meff cut applied
configMgr.cutsDict["VRZ1"] = configMgr.cutsDict["VRZ"] + " && " + dphicut[chn] + " && " + metomeffcut[chn]
configMgr.cutsDict["VRW1"] = configMgr.cutsDict["CRW"] + " && " + dphicut[chn] + " && " + metomeffcut[chn]
configMgr.cutsDict["VRT1"] = configMgr.cutsDict["CRT"] + " && " + dphicut[chn] + " && " + metomeffcut[chn]

# Lepton treated as a neutrino
extra_Cuts_For_VRWT = "(sqrt(pow(met*cos(metPhi)-lep1Pt*cos(lep1Phi),2) + pow(met*sin(metPhi)-lep1Pt*sin(lep1Phi),2))>50000) && ((mt>50000 && abs(lep1sign)==11) || (abs(lep1sign)!=11))" #extra_Cuts_For_VRWT
configMgr.cutsDict["VRW2"] = configMgr.cutsDict["CRW"] + " && " + extra_Cuts_For_VRWT
configMgr.cutsDict["VRT2"] = configMgr.cutsDict["CRT"] + " && " + extra_Cuts_For_VRWT

# Similar to VRW2 and VRT2 but with dphicut and met/meff cut applied
configMgr.cutsDict["VRW3"] = configMgr.cutsDict["VRW2"] + " && " + dphicut[chn] + " && " + metomeffcut[chn]
configMgr.cutsDict["VRT3"] = configMgr.cutsDict["VRT2"] + " && " + dphicut[chn] + " && " + metomeffcut[chn]

#-------------------------------
# Dump our options to user 
#-------------------------------
log.info("Will run with the following settings:")
log.info("configMgr.blindSR = %s" % configMgr.blindSR)
log.info("configMgr.fixSigXSec = %s" % configMgr.fixSigXSec)
log.info("configMgr.runOnlyNominalXSec = %s" % configMgr.runOnlyNominalXSec)
log.info("useCRWTY = %s" % useCRWTY)
log.info("useCRQ = %s" % useCRQ)
log.info("useQCDsample = %s" % useQCDsample)
log.info("useFlatBkgError = %s" % useFlatBkgError)
log.info("useShapeFit = %s" % useShapeFit)
log.info("useQCDMethodSyst = %s" % useQCDMethodSyst)
log.info("useSyst = %s" % useSyst)
log.info("useISRSyst = %s" % useISRSyst)
log.info("useStat = %s" % useStat)
log.info("useTheoSys = %s" % useTheoSys)
log.info("grid = %s" % grid)
log.info("allpoints = %s" % allpoints)
log.info("theoSysQCDNumber = %f" % theoSysQCDNumber)
log.info("jet1pt = %f" % jet1pt)
log.info("jet2pt = %f" % jet2pt)
log.info("jet3pt = %f" % jet3pt)
log.info("jet4pt = %f" % jet4pt)
log.info("jet5pt = %f" % jet5pt)
log.info("jet6pt = %f" % jet6pt)
log.info("metSig = %f" % metSig)
log.info("metomeff = %f" % metomeff)
log.info("dPhi = %f" % dPhi)
log.info("Full cutsDict can be printed with -L DEBUG")
log.debug(pprint.pformat(configMgr.cutsDict, width=60))

log.info("Wait 3 seconds for you to panic if these settings are wrong")
wait(3)
log.info("No panicking detected, continuing...")

#--------------------------------------------------------------------------
# List of systematics
#--------------------------------------------------------------------------
configMgr.nomName = ""

# JES (tree-based)
jes = Systematic("JES","","_JESUP","_JESDOWN","tree","overallNormHistoSys") 

# JER (tree-based)a
jer = Systematic("JER", "", "_JER", "_JER", "tree", "overallNormHistoSysOneSideSym") 

# SCALEST (tree-based)
scalest = Systematic("SCALEST", "", "_SCALESTUP", "_SCALESTDOWN", "tree", "overallSys")

# RESOST (tree-based)
resost = Systematic("RESOST", "", "_RESOST", "_RESOST", "tree", "overallNormHistoSysOneSideSym")

# PU
sysWeight_pileupUp=myreplace(configMgr.weights, ["pileupWeightUp"], "pileupWeight")
sysWeight_pileupDown=myreplace(configMgr.weights, ["pileupWeightDown"], "pileupWeight")
pileup = Systematic("pileup", configMgr.weights, sysWeight_pileupUp, sysWeight_pileupDown, "weight", "overallSys")

# b-tag systematics
bTagWeights = configMgr.weights + ["bTagWeight"]
bTagSystWeightsUp = myreplace(bTagWeights, ["bTagWeightBUp", "bTagWeightCUp", "bTagWeightLUp"] , "bTagWeight")
bTagSystWeightsDown = myreplace(bTagWeights, ["bTagWeightBDown", "bTagWeightCDown", "bTagWeightLDown"] , "bTagWeight")

bTagTop = Systematic("bTag",  bTagWeights , bTagSystWeightsUp, bTagSystWeightsDown, "weight", "overallNormHistoSys") 
bTagW = Systematic("bTag", bTagWeights, bTagSystWeightsUp, bTagSystWeightsDown, "weight", "overallNormHistoSys") 

# photon systematics
photonWeights = configMgr.weights + ["photonWeight", "triggerWeight"]
photonSystWeightsUp = myreplace(photonWeights, ["photonWeightUp"] , "photonWeight")
photonSystWeightsDown = myreplace(photonWeights, ["photonWeightDown"] , "photonWeight")
photonSys = Systematic("photonSys", photonWeights, photonSystWeightsUp, photonSystWeightsDown, "weight", "overallSys")

# trigger scaling
triggerSystWeightsUp = myreplace(photonWeights, ["triggerWeightUp"] , "triggerWeight")
triggerSystWeightsDown = myreplace(photonWeights, ["triggerWeightDown"] , "triggerWeight")
triggerSys = Systematic("triggerSys", photonWeights, triggerSystWeightsUp, triggerSystWeightsDown, "weight", "overallSys")

#--------------------------------------------------------------------------
# List of theo systematics
#--------------------------------------------------------------------------

# signal
sysWeight_theoSysSigUp = myreplace(configMgr.weights, ["normWeightUp"], "normWeight")
sysWeight_theoSysSigDown = myreplace(configMgr.weights, ["normWeightDown"], "normWeight")
theoSysSig = Systematic("SigXSec", configMgr.weights, sysWeight_theoSysSigUp, sysWeight_theoSysSigDown, "weight", "overallSys") 

# MC theo systematics
theoSysTop = Systematic("theoSysTop", "", "_Sherpa", "_Sherpa", "tree", "normHistoSysOneSide") 

mu1ScaleSysTop = Systematic("mu1ScaleSys", configMgr.weights, 
                            configMgr.weights + ["mu1ScaleWeightUp"], 
                            configMgr.weights + ["mu1ScaleWeightDown"], 
                            "weight", "overallNormHistoSys") 

mu2ScaleSysTop = Systematic("mu2ScaleSys", configMgr.weights, 
                            configMgr.weights+["mu2ScaleWeightUp"], 
                            configMgr.weights+["mu2ScaleWeightDown"], 
                            "weight", "overallNormHistoSys") 

matchScaleSysTop = Systematic("matchScaleSys", configMgr.weights, 
                              configMgr.weights + ["matchScaleWeightUp"], 
                              configMgr.weights + ["matchScaleWeightDown"], 
                              "weight", "overallNormHistoSys") 

# W MC
mu1ScaleSysW = Systematic("mu1ScaleSys", configMgr.weights, 
                            configMgr.weights + ["mu1ScaleWeightUp"], 
                            configMgr.weights + ["mu1ScaleWeightDown"], 
                            "weight", "overallNormHistoSys") 

mu2ScaleSysW = Systematic("mu2ScaleSys", configMgr.weights, 
                            configMgr.weights + ["mu2ScaleWeightUp"], 
                            configMgr.weights + ["mu2ScaleWeightDown"], 
                            "weight", "overallNormHistoSys") 

matchScaleSysW = Systematic("matchScaleSys", configMgr.weights, 
                              configMgr.weights + ["matchScaleWeightUp"], 
                              configMgr.weights + ["matchScaleWeightDown"], 
                              "weight", "overallNormHistoSys") 

nPartonsSysW = Systematic("nPartonsSysW", configMgr.weights, 
                          configMgr.weights + ["nPartonsWeight"], 
                          configMgr.weights + ["nPartonsWeight"], 
                          "weight", "overallNormHistoSysOneSideSym") 

# Z MC
mu1ScaleSysZ = Systematic("mu1ScaleSys", configMgr.weights, 
                            configMgr.weights + ["mu1ScaleWeightUp"], 
                            configMgr.weights + ["mu1ScaleWeightDown"], 
                            "weight", "overallNormHistoSys") 

mu2ScaleSysZ = Systematic("mu2ScaleSys", configMgr.weights, 
                            configMgr.weights + ["mu2ScaleWeightUp"], 
                            configMgr.weights + ["mu2ScaleWeightDown"], 
                            "weight", "overallNormHistoSys") 

matchScaleSysZ = Systematic("matchScaleSys", configMgr.weights, 
                              configMgr.weights + ["matchScaleWeightUp"], 
                              configMgr.weights + ["matchScaleWeightDown"], 
                              "weight", "overallNormHistoSys") 

# QCD
theoSysQCD = Systematic("theoSysQCD", configMgr.weights, 1.0 + theoSysQCDNumber,1.0-theoSysQCDNumber, "user", "userOverallSys")
QCDGausSys = Systematic("QCDGausSys", "", "_ghi", "_glo", "tree", "overallNormHistoSys")
QCDTailSys = Systematic("QCDTailSys", "", "_thi", "_tlo", "tree", "overallNormHistoSys")

# Diboson
theoSysDiboson = Systematic("theoSysDiboson",  configMgr.weights,  1.5, 0.5,  "user", "userOverallSys")

#-------------------------------------------
# List of samples and their plotting colours
#-------------------------------------------
# Diboson
dibosonSample = Sample("Diboson", kRed+3)
dibosonSample.setTreeName("Diboson_SRAll")
dibosonSample.setFileList(dibosonFiles)
dibosonSample.setStatConfig(useStat)

# Top
topSample = Sample("ttbar", kGreen-9)
topSample.setTreeName("Top_SRAll")
topSample.setNormFactor("mu_Top", 1., 0., 500.)
topSample.setFileList(topFiles)
topSample.setStatConfig(useStat) 

if useTheoSys:
    topSample.addSystematic(theoSysTop)

if useSyst :
    topSample.addSystematic(pileup)
    topSample.addSystematic(jes)
    topSample.addSystematic(jer)
    topSample.addSystematic(scalest)
    topSample.addSystematic(resost)  

if useSyst and useCRWTY:
    #topSample.setNormRegions([("CRT","cuts"),("CRW","cuts")])
    topSample.setNormRegions([("CRT", binVar)])

# QCD
qcdSample = Sample("Multijets", kOrange+2)
qcdSample.setTreeName("QCDdd")
qcdSample.setNormFactor("mu_Multijets", 1., 0., 500.)
qcdSample.setFileList(qcdFiles)
qcdSample.setStatConfig(useStat)
qcdSample.addWeight("0.0000013")#ATT: qcd prenormalisation
## if useSyst :
##     if useQCDMethodSyst:
##         qcdSample.addSystematic(QCDTailSys )
##         qcdSample.addSystematic(QCDGausSys )
##     else:
##         qcdSample.addSystematic(theoSysQCD)

#qcdSample.addSystematic(QCDGausSys)
#qcdSample.addSystematic(QCDTailSys)

if useSyst and useCRQ:
    qcdSample.setNormRegions([("CRQCD", binVar)])

# W 
wSample = Sample("Wjets", kAzure+1)
wSample.setTreeName("W_SRAll")
wSample.setNormFactor("mu_W", 1., 0., 500.)
wSample.setFileList(wFiles)
wSample.setStatConfig(useStat)

if useTheoSys:
    wSample.addSystematic(mu1ScaleSysW)
    wSample.addSystematic(mu2ScaleSysW)
    wSample.addSystematic(matchScaleSysW)
    wSample.addSystematic(nPartonsSysW)

if useSyst:
    wSample.addSystematic(pileup)
    wSample.addSystematic(jes)
    wSample.addSystematic(jer)
    wSample.addSystematic(scalest)
    wSample.addSystematic(resost)  

if useSyst and useCRWTY:
    #wSample.setNormRegions([("CRT","cuts"),("CRW","cuts")])
    wSample.setNormRegions([("CRW", binVar)])

# Gamma
gammaSample = Sample("GAMMAjets",kYellow)
gammaSample.setTreeName("GAMMA_SRAll")
gammaSample.setNormFactor("mu_Z",1.,0.,500.)
gammaSample.setFileList(gammaFiles)
gammaSample.setStatConfig(useStat)

if useTheoSys:
    gammaSample.addSystematic(mu1ScaleSysZ)
    gammaSample.addSystematic(mu2ScaleSysZ)
    gammaSample.addSystematic(matchScaleSysZ)

if useSyst :
    gammaSample.addSystematic(pileup)
    gammaSample.addSystematic(jes)
    gammaSample.addSystematic(jer)
    gammaSample.addSystematic(scalest)
    gammaSample.addSystematic(resost)        

if useSyst and useCRWTY:
    gammaSample.setNormRegions([("CRY", binVar)])
    
#gammaSample.noRenormSys = True

# Z
zSample = Sample("Zjets", kBlue)
zSample.setTreeName("Z_SRAll")
zSample.setNormFactor("mu_Z", 1., 0., 500.)
zSample.setFileList(zFiles)
zSample.setStatConfig(useStat)

if useTheoSys:
    zSample.addSystematic(mu1ScaleSysZ)
    zSample.addSystematic(mu2ScaleSysZ)
    zSample.addSystematic(matchScaleSysZ)

if useSyst :
    zSample.addSystematic(pileup)
    zSample.addSystematic(jes)
    zSample.addSystematic(jer)
    zSample.addSystematic(scalest)
    zSample.addSystematic(resost)  

if useSyst and useCRWTY:
    zSample.setNormRegions([("CRY", binVar)]) 
#zSample.setNormRegions([("CRT","cuts"),("CRW","cuts"),("CRY","cuts")])
zSample.normSampleRemap = "GAMMAjets"

# Data
dataSample = Sample("Data", kBlack)
dataSample.setTreeName("Data_SRAll")
dataSample.setData()
dataSample.setFileList(dataFiles)

#**************
# Set up fit 
#**************

# First define HistFactory attributes
if grid == "":
    configMgr.analysisName =  "ZL2013_%s_%s" % (anaName, allpoints[0])
else:
    configMgr.analysisName =  "ZL2013_%s_%s_%s" % (anaName, grid, allpoints[0])
configMgr.histCacheFile = "data/%s.root" % configMgr.analysisName
configMgr.outputFileName = "results/%s_Output.root " % configMgr.analysisName

# Note that we do not create fitConfigClones from som basic fitConfig with only the backgrounds
# As a consequence, memory usage goes through the roof for more than ~10 points.
# This NEEDS to be rewritten, but initial attempts caused different results, so for the draft INT
# we leave the code as is. On my TODO list. --GJ, 16/12/12 

for point in allpoints:
    if point == "":
        continue
        
    # Fit config instance
    name = "Fit_%s" % point
    myFitConfig = configMgr.addFitConfig(name)
 
    meas = myFitConfig.addMeasurement(name="NormalMeasurement", lumi=1.0, lumiErr=0.039)
    meas.addPOI("mu_SIG")

    meas.addParamSetting("mu_Diboson", True, 1) # fix diboson to MC prediction

    if not useCRQ:
        meas.addParamSetting("mu_Multijets", True, 1) # fix QCD

    if not useCRWTY:
        meas.addParamSetting("mu_Z", True, 1) # fix diboson to MC prediction
        meas.addParamSetting("mu_W", True, 1) # fix diboson to MC prediction
        meas.addParamSetting("mu_Top", True, 1) # fix diboson to MC prediction

    if useFlatBkgError:
        dibosonSample.addSystematic(Systematic("errBG", configMgr.weights, 1.3, 0.7, "user", "userOverallSys"))
        topSample.addSystematic(Systematic("errBG", configMgr.weights, 1.3, 0.7, "user", "userOverallSys")) 
        qcdSample.addSystematic(Systematic("errBG", configMgr.weights, 1.3, 0.7, "user", "userOverallSys"))
        wSample.addSystematic(Systematic("errBG", configMgr.weights, 1.3, 0.7, "user", "userOverallSys"))
        gammaSample.addSystematic(Systematic("errBG", configMgr.weights, 1.3, 0.7, "user", "userOverallSys"))
        zSample.addSystematic(Systematic("errBG", configMgr.weights, 1.3, 0.7, "user", "userOverallSys"))

    myFitConfig.addSamples([dibosonSample, topSample, wSample, zSample, dataSample])
        
    #-------------------------------------------------
    # Signal sample
    #-------------------------------------------------
    sigSampleName = "%s_%s" % (grid, point)
    if myFitType == FitType.Exclusion:
        if not os.path.exists("%s%s.root" % (INPUTDIR_SIGNAL, grid) ):
            log.fatal("Signal input file %s does not exist!" % ("%s%s.root" % (INPUTDIR_SIGNAL, grid) ) )

        sigSample = Sample(sigSampleName, kRed)
        sigSample.setFileList([INPUTDIR_SIGNAL+grid+".root"])
        sigSample.setTreeName("%s_%s_SRAll" % (grid, point) )
        sigSample.setNormByTheory()
        sigSample.setNormFactor("mu_SIG", 1, 0., 100.)
        sigSample.addSystematic(theoSysSig) ##keep error on signal
        sigSample.setStatConfig(useStat)

        if sigSampleName.startswith("SM") and useISRSyst:
            from SystematicsUtils import getISRSyst
            isrSyst = getISRSyst(sigSampleName)
            sigSample.addSystematic(isrSyst)

        myFitConfig.addSamples(sigSample)
        myFitConfig.setSignalSample(sigSample)

    #-------------------------------------------------
    # CR
    #-------------------------------------------------

    if useCRWTY or (useCRWTY==False and myFitType == FitType.Background):
        
        # Gamma control region
        if not useShapeFit:
            CRGAMMA = myFitConfig.addChannel("cuts", ["CRY"], 1, 0.5, 1.5)
        else:
            CRGAMMA = myFitConfig.addChannel(binVar, ["CRY"], nBins, minbin, maxbin)
            CRGAMMA.useOverflowBin = True
            CRGAMMA.useUnderflowBin = False

        CRGAMMA.addSample(gammaSample, 0) ##order is important!!!!
        for sam in CRGAMMA.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll", "CRY"))
            
            if sam.name.find("GAMMA") >= 0:
                sam.addWeight("photonWeight")
                sam.addWeight("triggerWeight") 

            if sam.treeName.find("Data") >= 0:
                sam.setFileList(dataCRWTFiles)
            pass
        
        if not useCRWTY and myFitType == FitType.Background:            
            myFitConfig.setValidationChannels(CRGAMMA)
        else:
            myFitConfig.setBkgConstrainChannels(CRGAMMA)

        # Top control region
        if not useShapeFit:
            CRT = myFitConfig.addChannel("cuts", ["CRT"], 1, 0.5, 1.5)
        else:
            CRT = myFitConfig.addChannel(binVar, ["CRT"], nBins, minbin, maxbin)
            CRT.useOverflowBin = True
            CRT.useUnderflowBin = False

        CRT.addWeight("bTagWeight")    
        for sam in CRT.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll", "CRWT"))
            if useSyst:
                if sam.name.find("ttbar") >= 0:
                    sam.addSystematic(bTagTop)
                    pass

                if sam.name.find("W") >= 0:
                    sam.addSystematic(bTagW)
                    pass

            if sam.treeName.find("Data") >= 0:
                sam.setFileList(dataCRWTFiles)
                pass

            pass
        
        if not useCRWTY and myFitType == FitType.Background:            
            myFitConfig.setValidationChannels(CRT)
        else:
            myFitConfig.setBkgConstrainChannels(CRT)

        # W control region
        if not useShapeFit:
            CRW = myFitConfig.addChannel("cuts", ["CRW"], 1, 0.5, 1.5)
        else:
            CRW = myFitConfig.addChannel(binVar, ["CRW"], nBins, minbin, maxbin)
            CRW.useOverflowBin = True
            CRW.useUnderflowBin = False

        CRW.addWeight("bTagWeight")
        for sam in CRW.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll", "CRWT"))
            if useSyst:
                if sam.name.find("ttbar") >= 0:
                    sam.addSystematic(bTagTop)
                    pass
                
                if sam.name.find("W") >= 0:                       
                    sam.addSystematic(bTagW)
                    pass    
            
            if sam.treeName.find("Data") >= 0:
                sam.setFileList(dataCRWTFiles)
            
            pass
        
        if not useCRWTY and myFitType==FitType.Background:            
            myFitConfig.setValidationChannels(CRW)
        else:
            myFitConfig.setBkgConstrainChannels(CRW)

    # QCD control region
    if useCRQ or (not useCRQ and myFitType == FitType.Background):
        if not useShapeFit:
            CRQCD = myFitConfig.addChannel("cuts", ["CRQCD"], 1, 0.5, 1.5)
        else:
            CRQCD = myFitConfig.addChannel(binVar, ["CRQCD"], nBins, minbin, maxbin)
            CRQCD.useOverflowBin = True
            CRQCD.useUnderflowBin = False

        if useCRQ == False and myFitType == FitType.Background:
            myFitConfig.setValidationChannels(CRQCD) 
        else:
            myFitConfig.setBkgConstrainChannels(CRQCD)
        
        if useQCDsample:
            CRQCD.addSample(qcdSample)
            CRQCD.addWeight("(genWeight < 400)")    #reject events with large weights

    #-------------------------------------------------
    # SR
    #-------------------------------------------------    
    if not useShapeFit:        
        SR = myFitConfig.addChannel("cuts", ["SR"], 1, 0.5, 1.5)
    else:
        SR = myFitConfig.addChannel(binVar, ["SR"], nBins, minbin, maxbin)
        SR.useOverflowBin = True
        SR.useUnderflowBin = False

    if useQCDsample:
        SR.addSample(qcdSample)

    if useSyst:                
        for sam in SR.sampleList:       
            if sam.name.find("Diboson") >= 0:             
                sam.addSystematic(theoSysDiboson)
            if sam.name.find("Multijets") >= 0:                       
                if useQCDMethodSyst:
                    sam.addSystematic(QCDTailSys )
                    sam.addSystematic(QCDGausSys )
                else:
                    sam.addSystematic(theoSysQCD)

    # Use the SR as validation region in the background fit, so that we can extract info from PDF in SR
    if myFitType == FitType.Background: 
        myFitConfig.setValidationChannels(SR)
    else:
        myFitConfig.setSignalChannels([SR])
            
    if myFitType == FitType.Discovery:
        SR.addDiscoverySamples(["SIG"], [1.], [0.], [100.], [kMagenta])

    #-------------------------------------------------
    # VR
    #-------------------------------------------------  
    if doValidation:
        if not (len(pickedSRs) >= 2 and pickedSRs[1].find("tight") >= 0 and pickedSRs[0] == "SRD"): #no stat in SRD,tight
            if not useShapeFit:
                VRZ = myFitConfig.addChannel("cuts",["VRZ"],1,0.5,1.5)
            else:
                VRZ = myFitConfig.addChannel(binVar, ["VRZ"], nBins, minbin, maxbin)
                VRZ.useOverflowBin = True
                VRZ.useUnderflowBin = False

            for sam in VRZ.sampleList:
                sam.setTreeName(sam.treeName.replace("SRAll","CRZ"))
                if sam.treeName.find("Data") >= 0:
                    sam.setFileList(dataCRWTFiles)
                    pass

            myFitConfig.setValidationChannels(VRZ)
 
        if len(pickedSRs)>=2 and pickedSRs[1].find("tight")<0:
            if not useShapeFit:
                VRZ_1b = myFitConfig.addChannel("cuts",["VRT2L"],1,0.5,1.5)
            else:
                VRZ_1b = myFitConfig.addChannel(binVar, ["VRT2L"], nBins, minbin, maxbin)
                VRZ_1b.useOverflowBin = True
                VRZ_1b.useUnderflowBin = False
                
            for sam in VRZ_1b.sampleList:
                sam.setTreeName(sam.treeName.replace("SRAll","CRZ_VR1b"))
                if sam.treeName.find("Data") >= 0:
                    sam.setFileList(dataCRWTFiles)
                    pass

            myFitConfig.setValidationChannels(VRZ_1b)

            
##         VRZfull = myFitConfig.addChannel("cuts",["VRZfull"],1,0.5,1.5)
##         for sam in VRZfull.sampleList:
##             sam.setTreeName(sam.treeName.replace("SRAll","CRZ"))
##             if sam.treeName.find("Data") >= 0:
##                 sam.setFileList(dataCRWTFiles)
##                 pass
##         myFitConfig.setValidationChannels(VRZfull)
        
##         VRZ_1b = myFitConfig.addChannel("cuts",["VRZ_1b"],1,0.5,1.5)
##         for sam in VRZ_1b.sampleList:
##             sam.setTreeName(sam.treeName.replace("SRAll","CRZ_VR1b"))
##             if sam.treeName.find("Data") >= 0:
##                 sam.setFileList(dataCRWTFiles)
##                 pass
##         myFitConfig.setValidationChannels(VRZ_1b)

##         VRZ_1c = myFitConfig.addChannel("cuts",["VRZ_1c"],1,0.5,1.5)
##         for sam in VRZ_1c.sampleList:
##             sam.setTreeName(sam.treeName.replace("SRAll","CRZ_VR1c"))
##             if sam.treeName.find("Data") >= 0:
##                 sam.setFileList(dataCRWTFiles)
##                 pass
##         myFitConfig.setValidationChannels(VRZ_1c)


        # VRWT_P
        if not useShapeFit:
            VRWT_P = myFitConfig.addChannel("cuts", ["VRWT_P"], 1, 0.5, 1.5)
        else:
            VRWT_P = myFitConfig.addChannel(binVar, ["VRWT_P"], nBins, minbin, maxbin)
            VRWT_P.useOverflowBin = True
            VRWT_P.useUnderflowBin = False
        
        for sam in VRWT_P.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll","CRWT"))
            if sam.treeName.find("Data") >= 0:
                sam.setFileList(dataCRWTFiles)
                pass
        myFitConfig.setValidationChannels(VRWT_P)

        # VRWT_M
        if not useShapeFit:
            VRWT_M = myFitConfig.addChannel("cuts", ["VRWT_M"], 1, 0.5, 1.5)
        else:
            VRWT_M = myFitConfig.addChannel(binVar, ["VRWT_M"], nBins, minbin, maxbin)
            VRWT_M.useOverflowBin = True
            VRWT_M.useUnderflowBin = False
        
        for sam in VRWT_M.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll", "CRWT"))
            if sam.treeName.find("Data") >= 0:
                sam.setFileList(dataCRWTFiles)
                pass
        myFitConfig.setValidationChannels(VRWT_M)

        # VRW1
        if not useShapeFit:
            VRW1 = myFitConfig.addChannel("cuts", ["VRW1"], 1, 0.5, 1.5)
        else:
            VRW1 = myFitConfig.addChannel(binVar, ["VRW1"], nBins, minbin, maxbin)
            VRW1.useOverflowBin = True
            VRW1.useUnderflowBin = False

        for sam in VRW1.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll", "CRWT"))
            if sam.treeName.find("Data") >= 0:
                sam.setFileList(dataCRWTFiles)
                pass
        myFitConfig.setValidationChannels(VRW1)

        # VRT1
        if not useShapeFit:
            VRT1 = myFitConfig.addChannel("cuts", ["VRT1"], 1, 0.5, 1.5)
        else:
            VRT1 = myFitConfig.addChannel(binVar, ["VRT1"], nBins, minbin, maxbin)
            VRT1.useOverflowBin = True
            VRT1.useUnderflowBin = False

        for sam in VRT1.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll", "CRWT"))
            if sam.treeName.find("Data") >= 0:
                sam.setFileList(dataCRWTFiles)
                pass

        myFitConfig.setValidationChannels(VRT1)

        # VRW2
        if not useShapeFit:
            VRW2 = myFitConfig.addChannel("cuts", ["VRW2"], 1, 0.5, 1.5)
        else:
            VRW2 = myFitConfig.addChannel(binVar, ["VRW2"], nBins, minbin, maxbin)
            VRW2.useOverflowBin = True
            VRW2.useUnderflowBin = False

        for sam in VRW2.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll", "VRWT_SRAll"))
            if sam.treeName.find("Data") >= 0:
                sam.setFileList(dataCRWTFiles)
                pass

        myFitConfig.setValidationChannels(VRW2)

        # VRT2
        if not useShapeFit:
            VRT2 = myFitConfig.addChannel("cuts", ["VRT2"], 1, 0.5, 1.5)
        else:
            VRT2 = myFitConfig.addChannel(binVar, ["VRT2"], nBins, minbin, maxbin)
            VRT2.useOverflowBin = True
            VRT2.useUnderflowBin = False

        for sam in VRT2.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll", "VRWT_SRAll"))
            if sam.treeName.find("Data") >= 0:
                sam.setFileList(dataCRWTFiles)
                pass

        myFitConfig.setValidationChannels(VRT2)

        # VRW3
        if not useShapeFit:
            VRW3 = myFitConfig.addChannel("cuts", ["VRW3"], 1, 0.5, 1.5)
        else:
            VRW3 = myFitConfig.addChannel(binVar, ["VRW3"], nBins, minbin, maxbin)
            VRW3.useOverflowBin = True
            VRW3.useUnderflowBin = False

        for sam in VRW3.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll", "VRWT_SRAll"))
            if sam.treeName.find("Data") >= 0:
                sam.setFileList(dataCRWTFiles)
                pass

        myFitConfig.setValidationChannels(VRW3)

        # VRT3
        if not useShapeFit:
            VRT3 = myFitConfig.addChannel("cuts", ["VRT3"], 1, 0.5, 1.5)
        else:
            VRT3 = myFitConfig.addChannel(binVar, ["VRT3"], nBins, minbin, maxbin)
            VRT3.useOverflowBin = True
            VRT3.useUnderflowBin = False

        for sam in VRT3.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll", "VRWT_SRAll"))
            if sam.treeName.find("Data") >= 0:
                sam.setFileList(dataCRWTFiles)
                pass

        myFitConfig.setValidationChannels(VRT3)

        # VRQCD1
        if not useShapeFit:
            VRQCD1 = myFitConfig.addChannel("cuts", ["VRQ1"], 1, 0.5, 1.5)
        else:
            VRQCD1 = myFitConfig.addChannel(binVar, ["VRQ1"], nBins, minbin, maxbin)
            VRQCD1.useOverflowBin = True
            VRQCD1.useUnderflowBin = False

        myFitConfig.setValidationChannels(VRQCD1)
        VRQCD1.addSample(qcdSample)
        VRQCD1.addWeight("(genWeight<400)")  

        if useSyst:                
            for sam in VRQCD1.sampleList:       
                #if sam.name.find("Multijets") >= 0:                       
                if useQCDMethodSyst:
                    sam.addSystematic(QCDTailSys )
                    sam.addSystematic(QCDGausSys )
                else:
                    sam.addSystematic(theoSysQCD) 
       ##  if useSyst:
    ##             for sam in VRQCD1.sampleList:        
    ##                 ##if sam.name.find("Multijets") >= 0: 
    ##                 if not useQCDMethodSyst:
    ##                     sam.addSystematic(theoSysQCD)
    ##                 else:
    ##                     sam.addSystematic(QCDTailSys )
    ##                     sam.addSystematic(QCDGausSys )                    
    ##                     pass

        # VRQCD2
        if not useShapeFit:
            VRQCD2 = myFitConfig.addChannel("cuts", ["VRQ2"], 1, 0.5, 1.5)
        else:
            VRQCD2 = myFitConfig.addChannel(binVar, ["VRQ2"], nBins, minbin, maxbin)
            VRQCD2.useOverflowBin = True
            VRQCD2.useUnderflowBin = False

        myFitConfig.setValidationChannels(VRQCD2)
        VRQCD2.addSample(qcdSample)
        VRQCD2.addWeight("(genWeight<400)")

        if useSyst:                
            for sam in VRQCD2.sampleList:       
                #if sam.name.find("Multijets") >= 0:                       
                if useQCDMethodSyst:
                    sam.addSystematic(QCDTailSys)
                    sam.addSystematic(QCDGausSys)
                else:
                    sam.addSystematic(theoSysQCD)

    ##         if useSyst:
    ##             for sam in VRQCD2.sampleList:        
    ##                 ###if sam.name.find("Multijets") >= 0 : 
    ##                 if not useQCDMethodSyst:
    ##                     sam.addSystematic(theoSysQCD)
    ##                 else:
    ##                     sam.addSystematic(QCDTailSys )
    ##                     sam.addSystematic(QCDGausSys )                    
    ##                     pass
