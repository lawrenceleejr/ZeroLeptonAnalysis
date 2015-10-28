###############################################################
##
## Moriond 2013 0-lepton analysis
##
################################################################

from configManager import configMgr
from ROOT import kBlack, kWhite, kGray, kRed, kPink, kMagenta, kViolet, kBlue, kAzure, kCyan, kTeal, kGreen, kSpring, kYellow, kOrange
from ROOT import TMath
from configWriter import TopLevelXML, Measurement, ChannelXML, Sample
from logger import Logger
from systematic import Systematic
from math import sqrt
from copy import deepcopy
import socket
import os
import sys
import pickle
import pprint
import string
import time
import argparse
from AnaList import *

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

def addWeight(oldList, newWeight):
    newList = deepcopy(oldList)
    newList.append(newWeight)
    return newList

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

#nbBJet=0

LUMI = 20.3
LUMI_ERR = 0.028

configMgr.blindSR = False             # Blind the SRs only
configMgr.blindCR = False             # Blind the CRs only

configMgr.fixSigXSec = True          # Run hypotests with also with up and down theor. uncert.? False: add uncert. as fit parameter
configMgr.runOnlyNominalXSec = False # only run nominal fit if fixSigXSec=True ?

useVRWTM = False               #treat lepton as missing particle when constraining W+jets and Top
useChargeAsymmetry = False     #use charge asymmetry to predict W and T

useCRWTY = True             # use control regions for Top, W and Z background
useCRQ = True               # use control region for QCD background
useQCDsample = True         # include QCD sample

# Relax meff cut for SRD/SREt CRT and CRWT?
useRelaxedCutInCRWTForSRDAndSREt = True

# Apply a user-defined errBG to the background errors? (Useful if setting everything to MC pred)
useFlatBkgError = False

# Use shape fit (false=cut&count)?
useShapeFit = False

# Use a shape factor when using shape fits?
useShapeFactor = False

# Fix alpha_SigXSec=0 (for hypothesis tests this goes automatically, this is for exclusion fits without this param)
useFixedXSec = False

# Settings for systematics
useQCDMethodSyst = False    # use systematics from sheffield method otherwise use theoSysQCDNumber
useSyst = True              # use systematical uncertainties (jes, jer, theo, ...)
useISRSyst = True           # use ISR syst (effect only for SM* grids)
useTheoSys = True           # use theoretical systematical uncertainties (jes, jer, theo, ...)
usePreComputedError = True # use theo precomputed error applied only in SR and VR
useTopSherpa = False        # use sherpa for top uncertainty?
useZAlpgen = True          # use Alpgen for Z uncertainty?

useAlternativeBaseline = True # use mcatnlo for top and alpgen for w? (useTopSherpa still works in addition)

# Settings for MC statistics
useStat = True              # use stat uncertainties on MC - globally
useStatPerSample = False    # use MC stat per sample

if useSyst == False:
    useTheoSys = False
    useISRSyst = False

# grid, with a default point and a default name
grid = "SM_GG_direct"
gridTreeName = grid 
allpoints = ["1200_0"]
anaName = "test" 

theoSysQCDNumber = 0.99     # uncertainty on QCD background estimate

# parse configMgr.userArg to overwrite options above if needed
if configMgr.userArg != "":
    log.info("Found user args %s" % configMgr.userArg)

    parser = argparse.ArgumentParser()
    parser.add_argument("-A", "--useAlternativeBaseline", action="store_true", default=False)
    args = parser.parse_args([configMgr.userArg])

    log.info("Parsed user args %s" % str(args))

    if args.useAlternativeBaseline:
        log.info("Setting useAlternativeBaseline=True")
        useAlternativeBaseline = True

    log.info("Waiting 5 seconds to review user args")
    wait(5)

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
metomeffDefault = (0.4, 0.4, 0.25, 0.25, 0.20, 0.15)

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
        gridTreeName = grid
        allpoints = sigSamples[1:]
    else:
        allpoints = sigSamples
        
# pickedSRs is set by the "-r" HistFitter option    
try:
    pickedSRs
except NameError:
    pickedSRs = None

if pickedSRs != None and len(pickedSRs) >= 1:
   
    # If SR is key in cut&count dict, pick it. 
    if len(pickedSRs) == 1 and pickedSRs[0] in anaDictMoriond13:
        pickedSRs = anaDictMoriond13[pickedSRs[0]].split(",")

    anaShortName = "Unknown"
    tmpName = ",".join(pickedSRs)
    if tmpName in anaInvDictMoriond13.keys():
        anaShortName = anaInvDictMoriond13[tmpName]
        
    if pickedSRs[0] == "SRM": chn = 0
    if pickedSRs[0] == "SRA": chn = 1
    if pickedSRs[0] == "SRB": chn = 2
    if pickedSRs[0] == "SRC": chn = 3
    if pickedSRs[0] == "SRD": chn = 4
    if pickedSRs[0] == "SRE": chn = 5
    metomeff = metomeffDefault[chn]
    
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
        useShapeFit = True
        minbin = int(pickedSRs[12])*1000
        meff = int(pickedSRs[12])*1000
    if len(pickedSRs) >= 14:
            nBins = int(pickedSRs[13])

if meff == None or chn > 6 or chn < 0:
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
    grid = ""
    gridTreeName = ""

if myFitType == FitType.Background:
    allpoints = ["Background"]
    grid = ""
    gridTreeName = ""

# grid name not changed beyond this, check if we have the truth Gluino_Stop_charm grids
if grid.find("truth.Gluino_Stop_charm.dM") != -1:
    gridTreeName = "Gluino_Stop_charm"

# Location of the ntuples ("Light" has the baseline cut applied already, preferred for speed)
#INPUTDIR = "/afs/cern.ch/atlas/groups/susy/0lepton/ZeroLeptonFitter/ZeroLepton-00-00-45_Light/"
INPUTDIR = "/afs/cern.ch/work/b/bruneli/public/ZeroLeptonFitter/TREES/ZeroLepton-00-00-47_Light/"

if socket.getfqdn().find("nikhef") != -1:
    INPUTDIR = "/glusterfs/atlas2/users/gbesjes/ZeroLepton-00-00-47_Light/"
elif socket.getfqdn().find("ccage") != -1:
    INPUTDIR = "/afs/in2p3.fr/home/m/makovec/TREES/ZeroLepton-00-00-45_Light/"
elif socket.getfqdn().find("ccwsge") != -1:
    INPUTDIR = "MY_INPUTS/"

#INPUTDIR = "/glusterfs/atlas2/users/gbesjes/ZeroLepton-00-00-45-noJVF_Light"

# Location of the signal inputs (default is the normal INPUTDIR)
INPUTDIR_SIGNAL = INPUTDIR 

# Check if need to use the full ntuples or not. Normally no need to modify this!
useFullNtuples = False
if meff < 700000 or (useShapeFit and minbin < 700000) or chn == 0:
    useFullNtuples = True
    INPUTDIR = "root://eosatlas.cern.ch//eos/atlas/user/m/marijam/ZeroLepton-00-00-45-Inputs/"
    INPUTDIR_SIGNAL = "/afs/cern.ch/work/g/gbesjes/public/ZeroLepton-00-00-45_Light/"
    if socket.getfqdn().find("nikhef") != -1:
        INPUTDIR = "/glusterfs/atlas2/users/gbesjes/ZeroLepton-00-00-45/"
        INPUTDIR_SIGNAL = "/glusterfs/atlas2/users/gbesjes/ZeroLepton-00-00-45_Light/"

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
configMgr.outputLumi = LUMI # Luminosity required for output histograms
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

    if not useAlternativeBaseline:
        # powheg as baseline
        topFiles.append(INPUTDIR+"/Top.root")
        if useTopSherpa:
            topFiles.append(INPUTDIR+"/test.TopSherpa.root")
        else:
            # versus mcatnlo is default
            topFiles.append(INPUTDIR+"/test.TopMcAtNlo.root")
    else:
        # alt. baseline is mcatnlo
        topFiles.append(INPUTDIR+"/TopMcAtNlo.root")
        if useTopSherpa:
            topFiles.append(INPUTDIR+"/test.TopSherpa.root")
        else:
            # normally versus powheg
            topFiles.append(INPUTDIR+"/test.TopPowheg.root")

    if not useAlternativeBaseline:
        # sherpa massive cb as baseline, alpgen for uncertainty
        wFiles.append(INPUTDIR+"/W.root")
        wFiles.append(INPUTDIR+"/test.WAlpgen.root")
    else:
        wFiles.append(INPUTDIR+"/WAlpgen.root")
        wFiles.append(INPUTDIR+"/test.WSherpaMassiveCB.root")

    zFiles.append(INPUTDIR+"/Z.root")
    if useZAlpgen:
        zFiles.append(INPUTDIR+"/test.ZAlpgen.root")

    gammaFiles.append(INPUTDIR+"/GAMMA.root")
    if useZAlpgen:
        gammaFiles.append(INPUTDIR+"/test.GAMMAAlpgen.root")
    
    dataFiles.append(INPUTDIR+"/DataJetTauEtmiss.root")
    dataCRWTFiles.append(INPUTDIR+"/DataEgamma.root")
    dataCRWTFiles.append(INPUTDIR+"/DataMuon.root")

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
configMgr.weights = ["genWeight", "pileupWeight", "normWeight"]

########################################
# Analysis description
########################################
####base = "(veto==0 && nJet>=1 &&jet1Pt>" + str(jet1pt) + ")"
cleaning="!( (abs(jet1Eta)<2. && jet1Chf<0.02) || (abs(jet1Eta)<2. && jet1Chf<0.05 && jet1Emf>0.9) ||  (jet1Eta<-0.1 && jet1Eta>-0.2 && jet1Phi<2.35 && jet1Phi>2.25 && jet1Chf<0.3 && jet1Emf<0.25 )) && abs(timing)<4"
base = "(veto==0 && nJet>=1 &&jet1Pt>" + str(jet1pt) + ") && "+cleaning

#base = "(veto==0 && nJet>=1 &&jet1Pt>" + str(jet1pt) + ")"

metCR = met
if metCR > 500*1000:
    metCR = 500*1000

metcut_SR = "(met>" + str(met) + " && dPhi>=" + str(dPhi) + " )"
metcut_CR = "(met>" + str(metCR) + ")" # the extra dphi cut is not applied to CR

baselineSR = [base,
              base + "&& (jet2Pt>" + str(jet2pt) + ")",
              base + "&& (jet2Pt>" + str(jet2pt) + ")"+ "&& (jet3Pt>" + str(jet3pt) + ")",
              base + "&& (jet2Pt>" + str(jet2pt) + ")"+ "&& (jet3Pt>" + str(jet3pt) + " && jet4Pt>" + str(jet4pt) + ")",
              base + "&& (jet2Pt>" + str(jet2pt) + ")"+ "&& (jet3Pt>" + str(jet3pt) + " && jet4Pt>" + str(jet4pt) + " && jet5Pt>" + str(jet5pt) + ")",
              base + "&& (jet2Pt>" + str(jet2pt) + ")"+ "&& (jet3Pt>" + str(jet3pt) + " && jet4Pt>" + str(jet4pt) + " && jet5Pt>" + str(jet5pt) + " && jet6Pt>" + str(jet6pt) + ")"]

dphicut = ["(dPhi>0.4)",
           "(dPhi>0.4)",
           "(dPhi>0.4)",
           "(dPhi>0.4 && dPhiR>0.2)",
           "(dPhi>0.4 && dPhiR>0.2)",
           "(dPhi>0.4 && dPhiR>0.2)"]

invdphicut = ["(dPhi<0.2)",
              "(dPhi<0.2)",
              "(dPhi<0.2)",
              "(dPhi<0.2 || dPhiR<0.1)",
              "(dPhi<0.2 || dPhiR<0.1)",
              "(dPhi<0.2 || dPhiR<0.1)"]

invdphicut2 = ["(dPhi>0.2 && dPhi<0.4)",
               "(dPhi>0.2 && dPhi<0.4)",
               "(dPhi>0.2 && dPhi<0.4)",
               "((dPhi>0.2 && dPhi<0.4) || (dPhiR>0.1 && dPhiR<0.2))",
               "((dPhi>0.2 && dPhi<0.4) || (dPhiR>0.1 && dPhiR<0.2))",
               "((dPhi>0.2 && dPhi<0.4) || (dPhiR>0.1 && dPhiR<0.2))"]

metSigDefinition="(met/1000/sqrt((meffInc-met)/1000))"

metSigcut = "("+metSigDefinition+">=" + str(metSig) + ")"

metomeffcut = ["(met/jet1Pt>" + str(metomeff) + " && " + metSigcut + ")", 
               "(met/meff2Jet>" + str(metomeff) + " && " + metSigcut + ")",
               "(met/meff3Jet>" + str(metomeff) + " && " + metSigcut + ")",
               "(met/meff4Jet>" + str(metomeff) + " && " + metSigcut + ")",
               "(met/meff5Jet>" + str(metomeff) + " && " + metSigcut + ")",
               "(met/meff6Jet>" + str(metomeff) + " && " + metSigcut + ")"]

metomeff_delta = 0.15
metomeff_delta2 = metomeff_delta+0.05

if metomeff >= 0.4:    
    metomeff_delta = 0.25
    metomeff_delta2 = metomeff_delta+0.05
if metomeff <= 0.2:    
    metomeff_delta = 0.05
    metomeff_delta2 = metomeff_delta+0.05
if metomeff <= 0.15:    
    metomeff_delta = 0.05
    metomeff_delta2 = metomeff_delta+0.05
    

metomeffcutqcd = ["(met/jet1Pt<" + str(metomeff) + ")&&(met/jet1Pt>" + str(metomeff-metomeff_delta) + ")",
                  "(met/meff2Jet<" + str(metomeff) + ")&&(met/meff2Jet>" + str(metomeff-metomeff_delta) + ")",
                  "(met/meff3Jet<" + str(metomeff) + ")&&(met/meff3Jet>" + str(metomeff-metomeff_delta) + ")",
                  "(met/meff4Jet<" + str(metomeff) + ")&&(met/meff4Jet>" + str(metomeff-metomeff_delta) + ")",
                  "(met/meff5Jet<" + str(metomeff) + ")&&(met/meff5Jet>" + str(metomeff-metomeff_delta) + ")",
                  "(met/meff6Jet<" + str(metomeff) + ")&&(met/meff6Jet>" + str(metomeff-metomeff_delta) + ")"]

metomeffcutqcd2 = ["(met/jet1Pt<" + str(metomeff-metomeff_delta) + ")&&(met/jet1Pt>" + str(metomeff-metomeff_delta2) + ")",
                  "(met/meff2Jet<" + str(metomeff-metomeff_delta) + ")&&(met/meff2Jet>" + str(metomeff-metomeff_delta2) + ")",
                  "(met/meff3Jet<" + str(metomeff-metomeff_delta) + ")&&(met/meff3Jet>" + str(metomeff-metomeff_delta2) + ")",
                  "(met/meff4Jet<" + str(metomeff-metomeff_delta) + ")&&(met/meff4Jet>" + str(metomeff-metomeff_delta2) + ")",
                  "(met/meff5Jet<" + str(metomeff-metomeff_delta) + ")&&(met/meff5Jet>" + str(metomeff-metomeff_delta2) + ")",
                  "(met/meff6Jet<" + str(metomeff-metomeff_delta) + ")&&(met/meff6Jet>" + str(metomeff-metomeff_delta2) + ")"]

if metomeff == 0:
    metsig_delta = 6
    metsig_delta2 = metsig_delta+3
    metomeffcutqcd = [ "("+metSigDefinition+">=" + str(metSig-metsig_delta) + ") && ("+metSigDefinition+"<" + str(metSig) + ")"]*6
    metomeffcutqcd2 = [ "("+metSigDefinition+">=" + str(metSig-metsig_delta2) + ") && ("+metSigDefinition+"<" + str(metSig-metsig_delta) + ")"]*6


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
        if pickedSRs[0] == "SRM": minbin = 1400000
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
    meffcut_relaxed = "(meffInc>" + str(meff-200000) + ")"

# Signal regions
configMgr.cutsDict["SR"] = baselineSR[chn] + " && " + dphicut[chn] + " && " + metomeffcut[chn] + " && " + meffcut + " && " + metcut_SR

# Set of relaxed cuts to use if necessary
configMgr.cutsDict["SR_no_dPhicut"] = baselineSR[chn] + " && " + metomeffcut[chn] + " && " + meffcut + " && " + metcut_SR
configMgr.cutsDict["SR_no_metomeffcut"]  = baselineSR[chn] + " && " + dphicut[chn] + " && " + meffcut + " && " + metcut_SR
configMgr.cutsDict["SR_no_dPhicut_no_metomeffcut"] = baselineSR[chn] + " && " + meffcut + " && " + metcut_SR
configMgr.cutsDict["SR_meffcut_relaxed"] = baselineSR[chn] + " && " + metomeffcut[chn] + " && " + meffcut_relaxed + " && " + metcut_SR

#if nbBJet:
#    configMgr.cutsDict["SR"] +=" && (nBJet>="+str(nbBJet)+")"


#configMgr.cutsDict["SR"] +=" && ((RunNumber!=195847 && EventNumber%2!=0) || RunNumber==195847 )"

# Control regions
bjetveto="(nBJet==0)"
leptonVeto = "(nLep == 0)"
bjetcut ="(nBJet>0)"
photonSelection="(phQuality == 2 && phIso < 5000.)"

if (anaShortName == "SRD" or anaShortName == "SREt") and useRelaxedCutInCRWTForSRDAndSREt:
    log.warning("Relaxing meff cut for CRT and CRW for SRD/SREt to >1300")
    # relax meff cut to 1300 for CRT and CRW for SRD
    meffcutCRWT = "(meffInc>1300000)"
    configMgr.cutsDict["CRW"]   = baselineSR[chn] + " && " + metcut_CR + " && " + meffcutCRWT + " && " + bjetveto
    configMgr.cutsDict["CRT"] = baselineSR[chn] + " && " + metcut_CR + " && " + meffcutCRWT + " && " + bjetcut
else:
    configMgr.cutsDict["CRW"]   = baselineSR[chn] + " && " + metcut_CR + " && " + meffcut + " && " + bjetveto
    configMgr.cutsDict["CRT"] = baselineSR[chn] + " && " + metcut_CR + " && " + meffcut + " && " + bjetcut

configMgr.cutsDict["CRY"]  = baselineSR[chn] + " && " + metcut_CR + " && " + dphicut[chn] + " && " + metomeffcut[chn] + " && " + meffcut + "  &&  " + photonSelection  +  " && "  +  leptonVeto
configMgr.cutsDict["CRQ"] = baselineSR[chn]+ " && " + metcut_CR + " && jet1Pt>400000 &&" + invdphicut[chn] + " && " + metomeffcutqcd[chn] + " && " + meffcut

# Validation regions
configMgr.cutsDict["VRQ1"] = baselineSR[chn] + " && " + metcut_CR + " && " + invdphicut[chn] + " &&  " + metomeffcut[chn] + " && " + meffcut
configMgr.cutsDict["VRQ2"] = baselineSR[chn] + " && " + metcut_CR + " && " + dphicut[chn] + " && " + metomeffcutqcd[chn] + " && " + meffcut
configMgr.cutsDict["VRQ3"] = baselineSR[chn] + " && " + metcut_CR + " && " + invdphicut2[chn] + " &&  " + metomeffcut[chn] + " && " + meffcut
configMgr.cutsDict["VRQ4"] = baselineSR[chn] + " && " + metcut_CR + " && " + invdphicut2[chn] + " && " + metomeffcutqcd[chn] + " && " + meffcut
#configMgr.cutsDict["VRQ5"] = baselineSR[chn]+ " && " + metcut_CR + " && jet1Pt>400000 &&" + invdphicut[chn] + " && " + metomeffcutqcd2[chn] + " && " + meffcut
#configMgr.cutsDict["VRQ6"] = baselineSR[chn] + " && " + metcut_CR + " && " + invdphicut2[chn] + " && " + metomeffcutqcd2[chn] + " && " + meffcut
#configMgr.cutsDict["VRQ7"] = baselineSR[chn] + " && " + metcut_CR + " && " + dphicut[chn] + " && " + metomeffcutqcd2[chn] + " && " + meffcut

#remove temporaly tauMt cut since it has beed remove from small tuples
configMgr.cutsDict["VRWTau"] = configMgr.cutsDict["VRQ3"] +" && tauN>=1 && nBJet==0"# && tauMt<100000" # &&tauJetBDTLoose>0"
configMgr.cutsDict["VRttbarTau"] = configMgr.cutsDict["VRQ3"] +" && tauN>=1 && nBJet>0"# && tauMt<100000"# && tauJetBDTLoose>0"

configMgr.cutsDict["VRZ"]  = baselineSR[chn] + " && " + metcut_CR + " && " + meffcut
configMgr.cutsDict["VRT2L"] = configMgr.cutsDict["VRZ"] + " && mll>116000 &&  lep1Pt<200000 && lep2Pt<100000"
configMgr.cutsDict["VRZ_1c"] = configMgr.cutsDict["VRZ"]

configMgr.cutsDict["VRWTPlus"]  = baselineSR[chn] + " && " + metcut_CR + " && " + meffcut + " && " + " lep1sign>0"
configMgr.cutsDict["VRWTMinus"]  = baselineSR[chn] + " && " + metcut_CR + " && " + meffcut + " && " + " lep1sign<0"

# Similar to VRWTMinus and VRWTPlus but with dphicut and met/meff cut applied
configMgr.cutsDict["VRWTPlusf"]  = configMgr.cutsDict["VRWTPlus"]+ " && " + dphicut[chn] + " && " + metomeffcut[chn]
configMgr.cutsDict["VRWTMinusf"]  = configMgr.cutsDict["VRWTMinus"] + " && " + dphicut[chn] + " && " + metomeffcut[chn]

# Similar to CRW,CRT and VRZ but with dphicut and met/meff cut applied
configMgr.cutsDict["VRZf"] = configMgr.cutsDict["VRZ"] + " && " + dphicut[chn] + " && " + metomeffcut[chn]
configMgr.cutsDict["VRWf"] = configMgr.cutsDict["CRW"] + " && " + dphicut[chn] + " && " + metomeffcut[chn]
configMgr.cutsDict["VRTf"] = configMgr.cutsDict["CRT"] + " && " + dphicut[chn] + " && " + metomeffcut[chn]

# Lepton treated as a neutrino
extra_Cuts_For_VRWT = "(sqrt(pow(met*cos(metPhi)-lep1Pt*cos(lep1Phi),2) + pow(met*sin(metPhi)-lep1Pt*sin(lep1Phi),2))>50000) && ((mt>50000 && abs(lep1sign)==11) || (abs(lep1sign)!=11))" #extra_Cuts_For_VRWT
configMgr.cutsDict["VRWM"] = configMgr.cutsDict["CRW"] + " && " + extra_Cuts_For_VRWT
configMgr.cutsDict["VRTM"] = configMgr.cutsDict["CRT"] + " && " + extra_Cuts_For_VRWT

# Similar to VRWM and VRTM but with dphicut and met/meff cut applied
configMgr.cutsDict["VRWMf"] = configMgr.cutsDict["VRWM"] + " && " + dphicut[chn] + " && " + metomeffcut[chn]
configMgr.cutsDict["VRTMf"] = configMgr.cutsDict["VRTM"] + " && " + dphicut[chn] + " && " + metomeffcut[chn]

print configMgr.cutsDict["VRZ"] 
print configMgr.cutsDict["SR"] 
print configMgr.cutsDict["CRY"] 
#toto

#use tighter CR for loose SRA
if meff <= 1000000 and chn <= 1:
    CRW = configMgr.cutsDict["CRW"]    
    CRT = configMgr.cutsDict["CRT"] 
    #CRQ = configMgr.cutsDict["CRQ"]    
    configMgr.cutsDict["CRW"] = configMgr.cutsDict["VRWf"] 
    configMgr.cutsDict["CRT"] = configMgr.cutsDict["VRTf"] 
    #configMgr.cutsDict["CRQ"] = configMgr.cutsDict["VRQ1"] 
    configMgr.cutsDict["VRWf"] = CRW
    configMgr.cutsDict["VRTf"] = CRT
    #configMgr.cutsDict["VRQ1"] = CRQ
    log.info("Replacing CR by tighter ones!!!!!!!!!!!!!!!!!!!!!")
    wait(2)

## if meff>=1500000:
##     newcut=int(meff)-300000
##     configMgr.cutsDict["CRW"]=configMgr.cutsDict["CRW"].replace(str(meff),str(newcut))
##     configMgr.cutsDict["CRT"]=configMgr.cutsDict["CRT"].replace(str(meff),str(newcut))
##     #print configMgr.cutsDict["CRW"]
##     #toto

#Apply looser meff cuts in case of tight SR
if meff >= 2000000:
    configMgr.cutsDict["VRZ"]=configMgr.cutsDict["VRZ"].replace(str(meff),"2000000")
    configMgr.cutsDict["VRZf"]=configMgr.cutsDict["VRZf"].replace(str(meff),"1800000")
    configMgr.cutsDict["VRT2L"]=configMgr.cutsDict["VRT2L"].replace(str(meff),"1700000")
    configMgr.cutsDict["VRTf"]=configMgr.cutsDict["VRTf"].replace(str(meff),"1700000")
    configMgr.cutsDict["VRWTPlusf"]=configMgr.cutsDict["VRWTPlusf"].replace(str(meff),"1700000")
    configMgr.cutsDict["VRWTMinusf"]=configMgr.cutsDict["VRWTMinusf"].replace(str(meff),"1700000")

## #apply looser cuts for VRT2L
## if meff>=1500000:    
##     configMgr.cutsDict["VRT2L"]=configMgr.cutsDict["VRT2L"].replace(str(meff),"1500000")
##     configMgr.cutsDict["VRWTPlusf"]=configMgr.cutsDict["VRWTPlusf"].replace(str(meff),"1500000")
##     configMgr.cutsDict["VRWTMinusf"]=configMgr.cutsDict["VRWTMinusf"].replace(str(meff),"1500000")

#print configMgr.cutsDict["VRT2L"]
#toto
#-------------------------------
# Dump our options to user 
#-------------------------------

if useStat and useStatPerSample:
    log.fatal("You have turned on both useStat and useStatPerSample: not possible!")
    sys.exit()

log.info("Will run with the following settings:")
log.info("INPUTDIR = %s" % INPUTDIR)
if INPUTDIR != INPUTDIR_SIGNAL:
    log.info("INPUTDIR_SIGNAL = %s" % INPUTDIR_SIGNAL)
log.info("doValidation = %s" % doValidation)
log.info("configMgr.blindSR = %s" % configMgr.blindSR)
log.info("configMgr.fixSigXSec = %s" % configMgr.fixSigXSec)
log.info("configMgr.runOnlyNominalXSec = %s" % configMgr.runOnlyNominalXSec)
log.info("useCRWTY = %s" % useCRWTY)
log.info("useCRQ = %s" % useCRQ)
log.info("useQCDsample = %s" % useQCDsample)
log.info("useFlatBkgError = %s" % useFlatBkgError)
log.info("useVRWTM = %s" % useVRWTM)
log.info("useChargeAsymmetry = %s" % useChargeAsymmetry)
log.info("useShapeFit = %s" % useShapeFit)
log.info("useQCDMethodSyst = %s" % useQCDMethodSyst)
log.info("useAlternativeBaseline = %s" % useAlternativeBaseline)
log.info("useTopSherpa = %s" % useTopSherpa)
log.info("useZAlpgen = %s" % useZAlpgen)
log.info("useSyst = %s" % useSyst)
log.info("useISRSyst = %s" % useISRSyst)
log.info("useStat = %s" % useStat)
log.info("useStatPerSample = %s" % useStatPerSample)
log.info("useTheoSys = %s" % useTheoSys)
log.info("useFixedXSec = %s" % useFixedXSec)
log.info("grid = %s" % grid)
log.info("gridTreeName = %s" % gridTreeName)
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
if useShapeFit:
    log.info("nBins = %d" % nBins)
    log.info("minbin = %d" % minbin)
    log.info("maxbin = %d" % maxbin)

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
sysWeight_pileupUp = myreplace(configMgr.weights, ["pileupWeightUp"], "pileupWeight")
sysWeight_pileupDown = myreplace(configMgr.weights, ["pileupWeightDown"], "pileupWeight")
pileup = Systematic("pileup", configMgr.weights, sysWeight_pileupUp, sysWeight_pileupDown, "weight", "overallSys")

# b-tag systematics
bTagWeights = configMgr.weights + ["bTagWeight"]
bTagSystWeightsUp = myreplace(bTagWeights, ["bTagWeightBUp", "bTagWeightCUp", "bTagWeightLUp"] , "bTagWeight")
bTagSystWeightsDown = myreplace(bTagWeights, ["bTagWeightBDown", "bTagWeightCDown", "bTagWeightLDown"] , "bTagWeight")
#bTagSystWeightsUp = myreplace(bTagWeights, ["bTagWeightBUp"] , "bTagWeight")
#bTagSystWeightsDown = myreplace(bTagWeights, ["bTagWeightBDown"] , "bTagWeight")

bTagSys = Systematic("bTagSys",  bTagWeights , bTagSystWeightsUp, bTagSystWeightsDown, "weight", "overallNormHistoSys") 


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
if not useFixedXSec:
    sysWeight_theoSysSigUp = myreplace(configMgr.weights, ["normWeightUp"], "normWeight")
    sysWeight_theoSysSigDown = myreplace(configMgr.weights, ["normWeightDown"], "normWeight")
    theoSysSig = Systematic("SigXSec", configMgr.weights, sysWeight_theoSysSigUp, sysWeight_theoSysSigDown, "weight", "overallSys") 

# MC theo systematics
if useTopSherpa:
    theoSysTop = Systematic("theoSysTop", "", "_Sherpa", "_Sherpa", "tree", "overallNormHistoSysOneSideSym") 
elif useAlternativeBaseline:
    theoSysTop = Systematic("theoSysTop", "", "_Powheg", "_Powheg", "tree", "overallNormHistoSysOneSideSym") 
else:
    # this is the default
    theoSysTop = Systematic("theoSysTop", "", "_McAtNlo", "_McAtNlo", "tree", "overallNormHistoSysOneSideSym") 

# Difference with Alpgen is W systematic; comes from test.WAlpgen.root (copy of WAlpgen but with suffix)
if not useAlternativeBaseline:
    theoSysW = Systematic("theoSysW", "", "_Alpgen", "_Alpgen", "tree", "overallNormHistoSysOneSideSym") 
else:
    theoSysW = Systematic("theoSysW", "", "_Sherpa", "_Sherpa", "tree", "overallNormHistoSysOneSideSym") 

# Z theory uncertaintuy (alpgen)
if useZAlpgen:
    theoSysZ = Systematic("theoSysZ", "", "_Alpgen", "_Alpgen", "tree", "overallNormHistoSysOneSideSym") 

# set usePreComputedError=True for Am, D, El, Em when useAlternativeBaseline
# these regions have issues with profiled nuisance parameters otherwise (5 apr 2013)
## if useAlternativeBaseline and (anaShortName == "SRAm" or anaShortName == "SRBt" or anaShortName == "SRD" or anaShortName == "SREl" or anaShortName == "SREm"):
##     log.warning("useAlternativeBaseline=True and in Am, Bt, D, El or Em, setting usePreComputedError=True")
##     wait(3)
##     usePreComputedError = True

if usePreComputedError:
    # W theory numbers from dict
    from WTheoSys import *

    theoSysWSRNumber = 0.5
    theoSysWVRWTNumber = 0.5

    if anaShortName in wTheoSysErrSRDict.keys():    
        theoSysWSRNumber = wTheoSysErrSRDict[anaShortName]
    theoSysWSR = Systematic("theoSysWSR", configMgr.weights, 1+theoSysWSRNumber, 1-theoSysWSRNumber, "user", "userOverallSys")

    if anaShortName in wTheoSysErrVRWTDict.keys():    
        theoSysWVRWTNumber = wTheoSysErrVRWTDict[anaShortName]
    theoSysWVRWT = Systematic("theoSysWVRWT", configMgr.weights, 1+theoSysWVRWTNumber, 1-theoSysWVRWTNumber, "user", "userOverallSys")

    # Top theory numbers from dict
    from TopTheoSys import *

    theoSysTopSRNumber = 0.5
    theoSysTopVRWTNumber = 0.5

    if anaShortName in topTheoSysErrSRDict.keys():    
        theoSysTopSRNumber = topTheoSysErrSRDict[anaShortName]
    theoSysTopSR = Systematic("theoSysTopSR", configMgr.weights, 1+theoSysTopSRNumber, 1-theoSysTopSRNumber, "user", "userOverallSys")

    if anaShortName in topTheoSysErrVRWTDict.keys():    
        theoSysTopVRWTNumber = topTheoSysErrVRWTDict[anaShortName]
    theoSysTopVRWT = Systematic("theoSysTopVRWT", configMgr.weights, 1+theoSysTopVRWTNumber, 1-theoSysTopVRWTNumber, "user", "userOverallSys")

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
                                     
HFWeightSysW = Systematic("HFWeightSysW", configMgr.weights, 
                          configMgr.weights + ["HFWeight"], 
                          configMgr.weights + ["HFWeight"], 
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
from DiBosonTheoSys import *

theoSysDibosonSRNumber = 0.5
theoSysDibosonCRNumber = 0.5
theoSysDibosonCRWTNumber = 0.5
theoSysDibosonVRWTNumber = 0.5

if anaShortName in dibosonTheoSysErrSRDict.keys():    
    theoSysDibosonSRNumber = dibosonTheoSysErrSRDict[anaShortName]
#print theoSysDibosonSRNumber

if anaShortName in dibosonTheoSysErrCRWTDict.keys():    
    theoSysDibosonCRWTNumber = dibosonTheoSysErrCRWTDict[anaShortName]
#print theoSysDibosonCRWTNumber

if anaShortName in dibosonTheoSysErrVRWTDict.keys():    
    theoSysDibosonVRWTNumber = dibosonTheoSysErrVRWTDict[anaShortName]
#print theoSysDibosonVRWTNumber

theoSysDibosonSR = Systematic("theoSysDibosonSR", configMgr.weights, 1+theoSysDibosonSRNumber, 1-theoSysDibosonSRNumber, "user", "userOverallSys")
theoSysDibosonCR = Systematic("theoSysDibosonCR", configMgr.weights, 1+theoSysDibosonCRNumber, 1-theoSysDibosonCRNumber, "user", "userOverallSys")
theoSysDibosonCRWT = Systematic("theoSysDibosonCRWT", configMgr.weights, 1+theoSysDibosonCRWTNumber, 1-theoSysDibosonCRWTNumber, "user", "userOverallSys")
theoSysDibosonVRWT = Systematic("theoSysDibosonVRWT", configMgr.weights, 1+theoSysDibosonVRWTNumber, 1-theoSysDibosonVRWTNumber, "user", "userOverallSys")

## Setting to have MC per bin, per sample 
#if useStatPerSample:
    #mcstat = Systematic("mcstat", "_NoSys", "_NoSys", "_NoSys", "tree", "shapeStat")

#-------------------------------------------
# List of samples and their plotting colours
#-------------------------------------------

# Diboson
# NB: note that theoSys on diboson are applied on the level of the region definitions,
# since we have one for the SR and one for the CR 
dibosonSample = Sample("Diboson", kRed+3)
dibosonSample.setTreeName("Diboson_SRAll")
dibosonSample.setFileList(dibosonFiles)
dibosonSample.setStatConfig(useStat)
#if useStatPerSample:
    #dibosonSample.addSystematic(mcstat)
                
# QCD
qcdSample = Sample("Multijets", kOrange+2)
#qcdSample.setTreeName("QCD_SRAll")
qcdSample.setTreeName("QCDdd_SRAll")
qcdSample.setNormFactor("mu_Multijets", 1., 0., 500.)
qcdSample.setFileList(qcdFiles)
qcdSample.setStatConfig(useStat)

# Normalise QCD sample to numbers from ZeroLeptonFactory:
qcdWeights = [ 0.00428144, 0.00405194, 0.00378623, 0.00371055, 0.00410402]

if chn != 0:
    # weights made for 20.3 fb-1
    weight = qcdWeights[chn-1] / 20300
    log.info("Setting QCD weight to %.10f" % weight)
    qcdSample.addWeight(str(weight))

#if useStatPerSample:
    #qcdSample.addSystematic(mcstat)

## if useSyst :
##     if useQCDMethodSyst:
##         qcdSample.addSystematic(QCDTailSys )
##         qcdSample.addSystematic(QCDGausSys )
##     else:
##         qcdSample.addSystematic(theoSysQCD)

#qcdSample.addSystematic(QCDGausSys)
#qcdSample.addSystematic(QCDTailSys)

if useSyst and useCRQ:
    qcdSample.setNormRegions([("CRQ", binVar)])
    pass

# Top
topSample = Sample("Top", kGreen-9)
topSample.setTreeName("Top_SRAll")
topSample.setNormFactor("mu_Top", 1., 0., 500.)
topSample.setFileList(topFiles)
topSample.setStatConfig(useStat) 

#if useStatPerSample:
    #topSample.addSystematic(mcstat)

if useTheoSys:
    if not usePreComputedError: 
        topSample.addSystematic(theoSysTop)
    pass

if useSyst :
    topSample.addSystematic(pileup)
    topSample.addSystematic(jes)
    topSample.addSystematic(jer)
    topSample.addSystematic(scalest)
    topSample.addSystematic(resost)
    #topSample.addSystematic(bTagSys)  
    
if useSyst and useCRWTY:
    if useChargeAsymmetry:
        topSample.setNormRegions([("VRWTPlus", binVar),("VRWTPlus", binVar)])
        pass
    elif useVRWTM:
        topSample.setNormRegions([("VRTM", binVar),("VRWM", binVar)])
    else:
        topSample.setNormRegions([("CRT", binVar),("CRW", binVar)])
        pass

# W 
wSample = Sample("Wjets", kAzure+1)
wSample.setTreeName("W_SRAll")
wSample.setNormFactor("mu_W", 1., 0., 500.)
wSample.setFileList(wFiles)
wSample.setStatConfig(useStat)

#if useStatPerSample:
    #wSample.addSystematic(mcstat)

if useTheoSys:
    if not usePreComputedError: wSample.addSystematic(theoSysW)
    wSample.addSystematic(mu1ScaleSysW)
    wSample.addSystematic(mu2ScaleSysW)
    #wSample.addSystematic(matchScaleSysW)
    #wSample.addSystematic(nPartonsSysW)
    wSample.addSystematic(HFWeightSysW)
    pass

if useSyst:
    if( anaShortName != "SRAm"):
        wSample.addSystematic(pileup)#large pu error dur problematic a problematic event in mcid=107693
    
    wSample.addSystematic(jes)
    wSample.addSystematic(jer)
    wSample.addSystematic(scalest)
    wSample.addSystematic(resost)  
    #wSample.addSystematic(bTagSys)  

if useSyst and useCRWTY and not useChargeAsymmetry:
    if useChargeAsymmetry:
        wSample.setNormRegions([("VRWTPlus", binVar),("VRWTPlus", binVar)])
        pass
    elif useVRWTM:
        wSample.setNormRegions([("VRTM", binVar),("VRWM", binVar)])
    else:
        wSample.setNormRegions([("CRT", binVar),("CRW", binVar)])
        #wSample.setNormRegions([("CRW", binVar)])
        pass
    
# Gamma
gammaSample = Sample("GAMMAjets",kYellow)
gammaSample.setTreeName("GAMMA_SRAll")
gammaSample.setNormFactor("mu_Z",1.,0.,500.)
gammaSample.setFileList(gammaFiles)
gammaSample.setStatConfig(useStat)

#if useStatPerSample:
    #gammaSample.addSystematic(mcstat)

if useTheoSys:
    if useZAlpgen:
        gammaSample.addSystematic(theoSysZ)
    gammaSample.addSystematic(mu1ScaleSysZ)
    gammaSample.addSystematic(mu2ScaleSysZ)
    #gammaSample.addSystematic(matchScaleSysZ)

if useSyst :
    gammaSample.addSystematic(pileup)
    gammaSample.addSystematic(jes)
    gammaSample.addSystematic(jer)
    gammaSample.addSystematic(scalest)
    gammaSample.addSystematic(resost)  
    #gammaSample.addSystematic(bTagSys)        

if useSyst and useCRWTY:
    gammaSample.setNormRegions([("CRY", binVar)])
    pass
    
#gammaSample.noRenormSys = True

# Z
zSample = Sample("Zjets", kBlue)
zSample.setTreeName("Z_SRAll")
zSample.setNormFactor("mu_Z", 1., 0., 500.)
zSample.setFileList(zFiles)
zSample.setStatConfig(useStat)

#if useStatPerSample:
    #zSample.addSystematic(mcstat)

if useTheoSys:
    if useZAlpgen:
        zSample.addSystematic(theoSysZ)
    
    zSample.addSystematic(mu1ScaleSysZ)
    zSample.addSystematic(mu2ScaleSysZ)
    #zSample.addSystematic(matchScaleSysZ)

if useSyst :
    zSample.addSystematic(pileup)
    zSample.addSystematic(jes)
    zSample.addSystematic(jer)
    zSample.addSystematic(scalest)
    zSample.addSystematic(resost)  
    #zSample.addSystematic(bTagSys)  

if useSyst and useCRWTY:
    zSample.setNormRegions([("CRY", binVar)])
    zSample.normSampleRemap = "GAMMAjets"
    pass

# Data
dataSample = Sample("Data", kBlack)
dataSample.setTreeName("Data_SRAll")
dataSample.setData()
dataSample.setFileList(dataFiles)

if useShapeFit and useShapeFactor:
    topSample.addShapeFactor("topShape")
    wSample.addShapeFactor("wShape")
    zSample.addShapeFactor("zShape")
    gammaSample.addShapeFactor("gammaShape")
    qcdSample.addShapeFactor("qcdShape")

#**************
# Set up fit 
#**************

# First define HistFactory attributes
prefix = "ZL2013"
if useAlternativeBaseline:
    prefix += "_altBaseline"

if grid == "":
    configMgr.analysisName =  "%s_%s_%s" % (prefix, anaName, allpoints[0])
else:
    configMgr.analysisName =  "%s_%s_%s_%s" % (prefix, anaName, grid, allpoints[0])

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
    name = "Fit_%s_%s" % (grid,point)
    myFitConfig = configMgr.addFitConfig(name)
 
    meas = myFitConfig.addMeasurement(name="NormalMeasurement", lumi=1.0, lumiErr=LUMI_ERR)
    meas.addPOI("mu_SIG")

    if myFitType != FitType.Exclusion:
        meas.addParamSetting("Lumi", True, LUMI) # fix Lumi

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
    #myFitConfig.addSamples([topSample, wSample, zSample, dataSample])
        
    #-------------------------------------------------
    # Signal sample
    #-------------------------------------------------
    sigSampleName = "%s_%s" % (grid, point)
    if myFitType == FitType.Exclusion:
        if INPUTDIR_SIGNAL.find("eosatlas") < 0 and not os.path.exists("%s%s.root" % (INPUTDIR_SIGNAL, grid) ):
            #NB: the test is not done for files in eos
            log.fatal("Signal input file %s does not exist!" % ("%s%s.root" % (INPUTDIR_SIGNAL, grid) ) )

        sigSample = Sample(sigSampleName, kRed)
        sigSample.setFileList([INPUTDIR_SIGNAL+grid+".root"])
        sigSample.setTreeName("%s_%s_SRAll" % (gridTreeName, point) )
        sigSample.setNormByTheory()
        sigSample.setNormFactor("mu_SIG", 1, 0., 100.)
        if not useFixedXSec:
            sigSample.addSystematic(theoSysSig) ##keep error on signal
        
        sigSample.setStatConfig(useStat)
        #if useStatPerSample:
            #sigSample.addSystematic(mcstat)
    
        sigSample.addSystematic(pileup)
        sigSample.addSystematic(jes)
        sigSample.addSystematic(jer)
        sigSample.addSystematic(scalest)
        sigSample.addSystematic(resost)  
        #sigSample.addSystematic(bTagSys)

        #if sigSampleName.startswith("SM") and (grid != "SM_SS_direct" and grid != "SM_SS_onestep" and grid != "SM_GG_onestep") and useISRSyst:
        if (grid == "SM_GG_direct" or grid == "SM_SG_direct") and useISRSyst:
            # channel   |  relative uncertainty
            # --------------------------------------------------
            # A         | (0.1*exp{-dM/100.0})  \oplus (0.15*exp{-dM/250.0})
            # Bm        | (0.45*exp{-dM/100.0}) \oplus (0.15*exp{-dM/240.0} + 0.04)
            # Cm        | (0.2*exp{-dM/100.0})  \oplus (0.3*exp{-dM/180.0})
            # Bt, Ct    | (0.45*exp{-dM/300.0}) \oplus (0.4*exp{-dM/340.0})
            # D         | (0.4*exp{-dM/150.0})  \oplus (0.25*exp{-dM/180.0} + 0.05)
            # El        | (0.2*exp{-dM/100.0})  \oplus (0.15*exp{-dM/200.0} + 0.02)
            # Em        | (0.35*exp{-dM/100.0}) \oplus (0.15*exp{-dM/350.0} + 0.01)
            # Et        | (0.4*exp{-dM/150.0})  \oplus (0.25*exp{-dM/280.0} + 0.03)
            
            # arrays follow coefficients in order of appearance:
            # [mult. factor 1, exponent 1, mult. factor 2, exponent 2, offset]
            coefficients = {}
            coefficients["A"]  = [0.1,  100.0, 0.15, 250.0, 0.0]
            coefficients["Bm"] = [0.45, 100.0, 0.15, 240.0, 0.04]
            coefficients["Cm"] = [0.2,  100.0, 0.3,  180.0, 0.0]
            coefficients["Bt"] = [0.45, 300.0, 0.4,  340.0, 0.0]
            coefficients["Ct"] = coefficients["Bt"]
            coefficients["D"]  = [0.4,  150.0, 0.25, 180.0, 0.05]
            coefficients["El"] = [0.2,  100.0, 0.15, 200.0, 0.02]
            coefficients["Em"] = [0.35, 100.0, 0.15, 350.0, 0.01]
            coefficients["Et"] = [0.4,  150.0, 0.25, 280.0, 0.03]
            
            msq = int(point.split("_")[0]) # first param is msquark for SS grids, mgluino for GG grids 
            mlsp = int(point.split("_")[1])
            mdiff = msq - mlsp

            idx = pickedSRs[0].replace("SR","").upper() 
           
            # TODO: this is dirty and prone to breaking. 
            # We need to fix the selections{} dict above with the Moriond '13 cuts.
            # --GJ 13/03/13

            if not useShapeFit:
                # for cut&count fit
                if idx == "B" and meff == 1800000: # 1800 or 2200
                    idx = "Bm"
                elif idx == "B" and meff == 2200000: # 1800 or 2200
                    idx = "Bt"
                elif idx == "C" and meff == 1200000: # 1200 or 2200
                    idx = "Cm"
                elif idx == "C" and meff == 2200000: # 1200 or 2200
                    idx = "Ct"
                elif idx == "E" and meff == 1000000: # 1000, 1200 or 1500
                    idx = "El"
                elif idx == "E" and meff == 1200000: # 1000, 1200 or 1500
                    idx = "Em"
                elif idx == "E" and meff == 1500000: # 1000, 1200 or 1500
                    idx = "Et"
                elif idx != "A" and idx != "D": 
                    # should not be possible - if you get here, region definitions changed
                    log.fatal("ISR syst needs a non-existing region for B, C or E - bailing out")
                    sys.exit()
            
                errisr_1 = (coefficients[idx][0] * TMath.exp(-1.0*mdiff / coefficients[idx][1]))
                errisr_2 = (coefficients[idx][2] * TMath.exp(-1.0*mdiff / coefficients[idx][3]) + coefficients[idx][4])

                errisr = TMath.sqrt(errisr_1*errisr_1 + errisr_2*errisr_2)
            else:
                # for shape fit, we take the largest one for a given region
                # Note: we could make this hardcoded, but do it dynamically in case the numbers ever change

                # TODO: move this into a function ? 
                if idx == "B":
                    errisr_1 = (coefficients["Bm"][0] * TMath.exp(-1.0*mdiff / coefficients["Bm"][1]))
                    errisr_2 = (coefficients["Bm"][2] * TMath.exp(-1.0*mdiff / coefficients["Bm"][3]) + coefficients["Bm"][4])
                    errisr_Bm = TMath.sqrt(errisr_1*errisr_1 + errisr_2*errisr_2)
                    
                    errisr_1 = (coefficients["Bt"][0] * TMath.exp(-1.0*mdiff / coefficients["Bt"][1]))
                    errisr_2 = (coefficients["Bt"][2] * TMath.exp(-1.0*mdiff / coefficients["Bt"][3]) + coefficients["Bt"][4])
                    errisr_Bt = TMath.sqrt(errisr_1*errisr_1 + errisr_2*errisr_2)

                    errisr = max(errisr_Bm, errisr_Bt)

                elif idx == "C":
                    errisr_1 = (coefficients["Cm"][0] * TMath.exp(-1.0*mdiff / coefficients["Cm"][1]))
                    errisr_2 = (coefficients["Cm"][2] * TMath.exp(-1.0*mdiff / coefficients["Cm"][3]) + coefficients["Cm"][4])
                    errisr_Cm = TMath.sqrt(errisr_1*errisr_1 + errisr_2*errisr_2)
                    
                    errisr_1 = (coefficients["Ct"][0] * TMath.exp(-1.0*mdiff / coefficients["Ct"][1]))
                    errisr_2 = (coefficients["Ct"][2] * TMath.exp(-1.0*mdiff / coefficients["Ct"][3]) + coefficients["Ct"][4])
                    errisr_Ct = TMath.sqrt(errisr_1*errisr_1 + errisr_2*errisr_2)
                    
                    errisr = max(errisr_Cm, errisr_Ct)

                elif idx == "E":
                    errisr_1 = (coefficients["El"][0] * TMath.exp(-1.0*mdiff / coefficients["El"][1]))
                    errisr_2 = (coefficients["El"][2] * TMath.exp(-1.0*mdiff / coefficients["El"][3]) + coefficients["El"][4])
                    errisr_El = TMath.sqrt(errisr_1*errisr_1 + errisr_2*errisr_2)
                    
                    errisr_1 = (coefficients["Em"][0] * TMath.exp(-1.0*mdiff / coefficients["Em"][1]))
                    errisr_2 = (coefficients["Em"][2] * TMath.exp(-1.0*mdiff / coefficients["Em"][3]) + coefficients["Em"][4])
                    errisr_Em = TMath.sqrt(errisr_1*errisr_1 + errisr_2*errisr_2)
                    
                    errisr_1 = (coefficients["Et"][0] * TMath.exp(-1.0*mdiff / coefficients["Et"][1]))
                    errisr_2 = (coefficients["Et"][2] * TMath.exp(-1.0*mdiff / coefficients["Et"][3]) + coefficients["Et"][4])
                    errisr_Et = TMath.sqrt(errisr_1*errisr_1 + errisr_2*errisr_2)
                    
                    errisr = max( max(errisr_El, errisr_Em), errisr_Et)
                else: # A & D have only one ISR uncertainty
                    errisr_1 = (coefficients[idx][0] * TMath.exp(-1.0*mdiff / coefficients[idx][1]))
                    errisr_2 = (coefficients[idx][2] * TMath.exp(-1.0*mdiff / coefficients[idx][3]) + coefficients[idx][4])

                    errisr = TMath.sqrt(errisr_1*errisr_1 + errisr_2*errisr_2)

            isrHighWeights = addWeight(configMgr.weights, str(1 + errisr))
            isrLowWeights = addWeight(configMgr.weights, str(1 - errisr))

            isrUnc = Systematic("ISR", configMgr.weights, isrHighWeights,
                                    isrLowWeights, "weight", "overallSys")
            sigSample.addSystematic(isrUnc)

        elif grid == "SM_SS_direct" and useISRSyst: #special for direct squark production
            msq = int(point.split("_")[0]) 
            mlsp = int(point.split("_")[1])
            mdiff = msq - mlsp

            # See sec4.2 of the note:
            # https://svnweb.cern.ch/trac/atlasphys/browser/Physics/SUSY/Papers/Moriond2013/zero_lepton/INT/INT_0leptonpaper_Moriond2013.pdf
            errisr = TMath.sqrt(0.2*0.2 + 0.15*0.15) * TMath.exp(-1.0*mdiff/250.0)

            isrHighWeights = addWeight(configMgr.weights, str(1 + errisr))
            isrLowWeights = addWeight(configMgr.weights, str(1 - errisr))

            isrUnc = Systematic("ISR", configMgr.weights, isrHighWeights,
                                    isrLowWeights, "weight", "overallSys")
            sigSample.addSystematic(isrUnc)

        elif (grid == "SM_GG_onestep" or grid == "SM_SS_onestep") and useISRSyst: #special for the onestep grids
            # The following formulae have been derived by Zuzana:
            #
            # channel  |  GG-onestep        | SS-onestep
            # --------------------------------------------------
            # 2-jet    | 0.2*exp{-dM/230.7} | 0.1*exp{-dM/360.0}
            # 3-jet    | 0.2*exp{-dM/190.1} | 0.3*exp{-dM/123.1}
            # 4-jet    | 0.3*exp{-dM/144.8} | 0.3*exp{-dM/146.0}
            # 5-jet    | 0.4*exp{-dM/149.3} | 0.3*exp{-dM/238.8}
            # 6-jet    | 0.3*exp{-dM/244.2} | 0.3*exp{-dM/416.3}
            
            if grid == "SM_GG_onestep":
                startingValues = [0.2, 0.2, 0.3, 0.4, 0.3]
                exponentFactors = [230.7, 190.1, 144.8, 149.3, 244.2]
            else:
                startingValues = [0.1, 0.3, 0.3, 0.3, 0.3]
                exponentFactors = [360.0, 123.1, 146.0, 238.8, 416.3]

            # regions are named A-E, so use alphabet position 
            idx = string.lowercase.index(pickedSRs[0].replace("SR","").lower()) 

            msq = int(point.split("_")[0]) # first param is msquark for SS grids, mgluino for GG grids 
            mlsp = int(point.split("_")[2])
            mdiff = msq - mlsp

            errisr = startingValues[idx] * TMath.exp(-1.0*mdiff / exponentFactors[idx])
            
            isrHighWeights = addWeight(configMgr.weights, str(1 + errisr))
            isrLowWeights = addWeight(configMgr.weights, str(1 - errisr))

            isrUnc = Systematic("ISR", configMgr.weights, isrHighWeights,
                                    isrLowWeights, "weight", "overallSys")
            sigSample.addSystematic(isrUnc)
        
        elif (grid == "MUED") and useISRSyst: #special for the mUED grid
            errisr = 0.25   # 25% error everywhere
            isrHighWeights = addWeight(configMgr.weights, str(1 + errisr))
            isrLowWeights = addWeight(configMgr.weights, str(1 - errisr))
            
            isrUnc = Systematic("ISR", configMgr.weights, isrHighWeights,isrLowWeights, "weight", "overallSys")
            sigSample.addSystematic(isrUnc)
    
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
            if sam.name.find("Diboson") >= 0:             
                sam.addSystematic(theoSysDibosonCR)
            if sam.name.find("GAMMA") >= 0:
                if useSyst:
                    sam.addSystematic(photonSys)
                sam.addWeight("photonWeight")
                sam.addWeight("triggerWeight") 

            if sam.treeName.find("Data") >= 0:
                sam.setFileList(dataCRWTFiles)
            pass
        
        if not useCRWTY and myFitType == FitType.Background:            
            myFitConfig.setValidationChannels(CRGAMMA)
        else:
            myFitConfig.setBkgConstrainChannels(CRGAMMA)

        if (not useChargeAsymmetry and not useVRWTM) or (doValidation):
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
                if sam.name.find("Diboson") >= 0 and useSyst:             
                    sam.addSystematic(theoSysDibosonCRWT)
                if useSyst and not useChargeAsymmetry:
                    if sam.name.find("Top") >= 0 or sam.name.find("W") >= 0:
                        sam.addSystematic(bTagSys)
                        pass
                if sam.treeName.find("Data") >= 0:
                    sam.setFileList(dataCRWTFiles)
                    pass
                pass        
            if (not useCRWTY and myFitType == FitType.Background) or useChargeAsymmetry or useVRWTM:
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
                if sam.name.find("Diboson") >= 0 and useSyst:             
                    sam.addSystematic(theoSysDibosonCRWT)
                if useSyst and not useChargeAsymmetry:
                    if sam.name.find("Top") >= 0 or sam.name.find("W") >= 0: 
                        sam.addSystematic(bTagSys)
                        pass                
                if sam.treeName.find("Data") >= 0:
                    sam.setFileList(dataCRWTFiles)            
                pass        
            if (not useCRWTY and myFitType==FitType.Background) or useChargeAsymmetry or useVRWTM:            
                myFitConfig.setValidationChannels(CRW)
            else:
                myFitConfig.setBkgConstrainChannels(CRW)

        if (useVRWTM) or (not useVRWTM and doValidation):
            # Top control region
            if not useShapeFit:
                VRTM = myFitConfig.addChannel("cuts", ["VRTM"], 1, 0.5, 1.5)
            else:
                VRTM = myFitConfig.addChannel(binVar, ["VRTM"], nBins, minbin, maxbin)
                VRTM.useOverflowBin = True
                VRTM.useUnderflowBin = False
            VRTM.addWeight("bTagWeight")    
            for sam in VRTM.sampleList:
                sam.setTreeName(sam.treeName.replace("SRAll", "VRWT_SRAll"))         
                if sam.name.find("Diboson") >= 0 and useSyst:             
                    sam.addSystematic(theoSysDibosonCRWT)
                if useSyst and not useChargeAsymmetry:
                    if sam.name.find("Top") >= 0 or sam.name.find("W") >= 0:
                        sam.addSystematic(bTagSys)
                        pass
                if sam.treeName.find("Data") >= 0:
                    sam.setFileList(dataCRWTFiles)
                    pass
                pass        
            if (not useCRWTY and myFitType == FitType.Background) or useChargeAsymmetry or (not useVRWTM):
                myFitConfig.setValidationChannels(VRTM)
            else:
                myFitConfig.setBkgConstrainChannels(VRTM)

            # W control region
            if not useShapeFit:
                VRWM = myFitConfig.addChannel("cuts", ["VRWM"], 1, 0.5, 1.5)
            else:
                VRWM = myFitConfig.addChannel(binVar, ["VRWM"], nBins, minbin, maxbin)
                VRWM.useOverflowBin = True
                VRWM.useUnderflowBin = False
            VRWM.addWeight("bTagWeight")
            for sam in VRWM.sampleList:
                sam.setTreeName(sam.treeName.replace("SRAll", "VRWT_SRAll"))     
                if sam.name.find("Diboson") >= 0 and useSyst:             
                    sam.addSystematic(theoSysDibosonCRWT)
                if useSyst and not useChargeAsymmetry:
                    if sam.name.find("Top") >= 0 or sam.name.find("W") >= 0: 
                        sam.addSystematic(bTagSys)
                        pass                
                if sam.treeName.find("Data") >= 0:
                    sam.setFileList(dataCRWTFiles)            
                pass        
            if (not useCRWTY and myFitType==FitType.Background) or useChargeAsymmetry or (not useVRWTM):            
                myFitConfig.setValidationChannels(VRWM)
            else:
                myFitConfig.setBkgConstrainChannels(VRWM)

    if useChargeAsymmetry or (not useChargeAsymmetry and doValidation):

        # VRWTPlus
        if not useShapeFit:
            VRWTPlus = myFitConfig.addChannel("cuts", ["VRWTPlus"], 1, 0.5, 1.5)
        else:
            VRWTPlus = myFitConfig.addChannel(binVar, ["VRWTPlus"], nBins, minbin, maxbin)
            VRWTPlus.useOverflowBin = True
            VRWTPlus.useUnderflowBin = False

        for sam in VRWTPlus.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll","CRWT"))
            if sam.treeName.find("Data") >= 0:
                sam.setFileList(dataCRWTFiles)
                pass
        if (not useCRWTY and myFitType==FitType.Background) or not useChargeAsymmetry:
            myFitConfig.setValidationChannels(VRWTPlus)        
        else:
            myFitConfig.setBkgConstrainChannels(VRWTPlus)

        # VRWTMinus
        if not useShapeFit:
            VRWTMinus = myFitConfig.addChannel("cuts", ["VRWTMinus"], 1, 0.5, 1.5)
        else:
            VRWTMinus = myFitConfig.addChannel(binVar, ["VRWTMinus"], nBins, minbin, maxbin)
            VRWTMinus.useOverflowBin = True
            VRWTMinus.useUnderflowBin = False

        for sam in VRWTMinus.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll", "CRWT"))
            if sam.treeName.find("Data") >= 0:
                sam.setFileList(dataCRWTFiles)
                pass
        if (not useCRWTY and myFitType==FitType.Background) or not useChargeAsymmetry:
            myFitConfig.setValidationChannels(VRWTMinus)        
        else:
            myFitConfig.setBkgConstrainChannels(VRWTMinus)

    # QCD control region
    if useCRQ or (not useCRQ and myFitType == FitType.Background):
        if not useShapeFit:
            CRQ = myFitConfig.addChannel("cuts", ["CRQ"], 1, 0.5, 1.5)
        else:
            CRQ = myFitConfig.addChannel(binVar, ["CRQ"], nBins, minbin, maxbin)
            CRQ.useOverflowBin = True
            CRQ.useUnderflowBin = False

        if useCRQ == False and myFitType == FitType.Background:
            myFitConfig.setValidationChannels(CRQ) 
        else:
            myFitConfig.setBkgConstrainChannels(CRQ)

        for sam in CRQ.sampleList:
            if sam.name.find("Diboson") >= 0 and useSyst:             
                sam.addSystematic(theoSysDibosonCR)

        
    if useQCDsample and useCRQ:
        CRQ.addSample(qcdSample)

    #-------------------------------------------------
    # SR
    #-------------------------------------------------    
    if not useShapeFit:        
        #SR_loose = myFitConfig.addChannel("cuts", ["SR_meffcut_relaxed"], 1, 0.5, 1.5)
        
        SR = myFitConfig.addChannel("cuts", ["SR"], 1, 0.5, 1.5)
        #SR.remapSystChanName = "cuts_SR_meffcut_relaxed"
    else:
        SR = myFitConfig.addChannel(binVar, ["SR"], nBins, minbin, maxbin)
        SR.useOverflowBin = True
        SR.useUnderflowBin = False

    #if nbBJet:
    #    SR.addWeight("bTagWeight")
        
    if useQCDsample:
        SR.addSample(qcdSample)
        #SR_loose.addSample(qcdSample)

    if useSyst:
        #for sam in SR_loose.sampleList: 

            #if usePreComputedError: 
                #if sam.name.find("Wjets") >= 0:             
                    #sam.addSystematic(theoSysWSR)        
                #if sam.name.find("Top") >= 0:             
                    #sam.addSystematic(theoSysTopSR)
              
            #if sam.name.find("Diboson") >= 0:             
                #sam.addSystematic(theoSysDibosonSR)
            #if sam.name.find("Multijets") >= 0:                       
                #if useQCDMethodSyst:
                    #sam.addSystematic(QCDTailSys )
                    #sam.addSystematic(QCDGausSys )
                #else:
                    #sam.addSystematic(theoSysQCD)
        
        for sam in SR.sampleList: 

            if usePreComputedError and useSyst: 
                if sam.name.find("Wjets") >= 0:             
                    sam.addSystematic(theoSysWSR)        
                if sam.name.find("Top") >= 0:             
                    sam.addSystematic(theoSysTopSR)
              
            if sam.name.find("Diboson") >= 0 and useSyst:             
                sam.addSystematic(theoSysDibosonSR)
            if sam.name.find("Multijets") >= 0 and useSyst:                       
                if useQCDMethodSyst:
                    sam.addSystematic(QCDTailSys )
                    sam.addSystematic(QCDGausSys )
                else:
                    sam.addSystematic(theoSysQCD)

##             if not useChargeAsymmetry:
##                 if sam.name.find("Top") >= 0 or sam.name.find("W") >= 0:
##                     sam.addSystematic(bTagSys)
##                     pass
 
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
        VRList=[]

        ######################################################################
        # VR with leptons
        ######################################################################        
        VRList1=[(["VRZ"],"CRZ"),
                 (["VRZf"],"CRZ"),
                 (["VRT2L"],"CRZ_VR1b"),
                 #(["CRT"],"CRWT"),
                 (["VRTf"],"CRWT"),
                 #(["VRTM"],"VRWT_SRAll"),
                 (["VRTMf"],"VRWT_SRAll"),
                 #(["CRW"],"CRWT"),
                 (["VRWf"],"CRWT"),
                 #(["VRWM"],"VRWT_SRAll"),
                 (["VRWMf"],"VRWT_SRAll"),
                 #(["VRWTPlus"],"CRWT"),
                 #(["VRWTMinus"],"CRWT"),
                 (["VRWTPlusf"],"CRWT"),
                 (["VRWTMinusf"],"CRWT")
                 ]

        lepFlavours=["any"]
        #lepFlavours=["any","mu","ele"]
        
        for element in VRList1:
            for lepF in lepFlavours:

                print "####",lepF,element
                regionName=element[0][0]

                #Do not redo existing regions
                if regionName in ["CRT","CRW","VRWTPlus","VRWTMinus"] and lepF == "any":
                    continue
                
                # e/mu separation only for selected regions                
                if lepF != "any" and regionName not in ["CRT","CRW","VRTM","VRWM"]:
                    continue
               
                # if useAlternativeBaseline, take out crashing regions
                if useAlternativeBaseline:
                    if regionName == "VRT2L" and (anaShortName.startswith("SRB") or anaShortName == "SRCt"):
                        continue

                if lepF=="mu":
                    oldRegionName=regionName
                    regionName+="mu"
                    regionName=regionName.replace("CR","VR")
                    configMgr.cutsDict[regionName]=configMgr.cutsDict[oldRegionName]+" && abs(lep1sign)==13"
                    print configMgr.cutsDict[regionName]

                if lepF=="ele":
                    oldRegionName=regionName
                    regionName+="ele"
                    regionName=regionName.replace("CR","VR")
                    configMgr.cutsDict[regionName]=configMgr.cutsDict[oldRegionName]+" && abs(lep1sign)==11"

                print "==>",regionName
                
                if not useShapeFit:
                    VR = myFitConfig.addChannel("cuts", [regionName], 1, 0.5, 1.5)
                else:
                    VR = myFitConfig.addChannel(binVar, [regionName], nBins, minbin, maxbin)
                    VR.useOverflowBin = True
                    VR.useUnderflowBin = False

                VRList.append(VR)

                for sam in VR.sampleList:
                    sam.setTreeName(sam.treeName.replace("SRAll", element[1]))

                    if usePreComputedError and useSyst: 
                        if sam.name.find("Wjets") >= 0 and element in  ["VRWMf","VRWM","VRTMf","VRTM"]:
                            sam.addSystematic(theoSysWVRWT)                            
                        if sam.name.find("Top") >= 0 and element in  ["VRWMf","VRWM","VRTMf","VRTM"]:
                            sam.addSystematic(theoSysTopVRWT)

                    if sam.name.find("Diboson") >= 0 and useSyst:
                        if element in  ["VRWMf","VRWM","VRTMf","VRTM"]:
                            sam.addSystematic(theoSysDibosonVRWT)
                        elif element in  ["VRWf","VRTf"]:
                            sam.addSystematic(theoSysDibosonCRWT)
                        else: 
                            sam.addSystematic(theoSysDibosonCR)
                            
                    if sam.treeName.find("Data") >= 0:
                        sam.setFileList(dataCRWTFiles)
                        pass
                #if (not useCRWTY and myFitType==FitType.Background) or not useChargeAsymmetry:
                myFitConfig.setValidationChannels(VR)
                #    titi
                #else:
                #    myFitConfig.setBkgConstrainChannels(VR)
                #    print regionName
                #    toto

        ######################################################################
        # VRQ
        ######################################################################
        VRList2=[["VRQ1"],["VRQ2"],["VRQ3"],["VRQ4"]]
        for element in VRList2:
            # VR
            if not useShapeFit:
                VR = myFitConfig.addChannel("cuts", element, 1, 0.5, 1.5)
            else:
                VR = myFitConfig.addChannel(binVar, element, nBins, minbin, maxbin)
                VR.useOverflowBin = True
                VR.useUnderflowBin = False

            VRList.append(VR)

            myFitConfig.setValidationChannels(VR)
            if useQCDsample:
                VR.addSample(qcdSample)

            if useSyst:                
                for sam in VR.sampleList:       
                    if sam.name.find("Multijets") >= 0 and useSyst:                       
                        if useQCDMethodSyst:
                            sam.addSystematic(QCDTailSys )
                            sam.addSystematic(QCDGausSys )
                        else:
                            sam.addSystematic(theoSysQCD)

        ############################################################################        
        # VRTau
        ############################################################################
        if not (useAlternativeBaseline and (anaShortName == "SRBt") or (useShapeFit and pickedSRs[0] == "SRB" and minbin>2000000) ):
            if not useShapeFit:
                VRWTau = myFitConfig.addChannel("cuts", ["VRWTau"], 1, 0.5, 1.5)
            else:
                VRWTau = myFitConfig.addChannel(binVar, ["VRWTau"], nBins, minbin, maxbin)
                VRWTau.useOverflowBin = True
                VRWTau.useUnderflowBin = False
            myFitConfig.setValidationChannels(VRWTau)
            if useQCDsample:
                VRWTau.addSample(qcdSample)#not for QCDdd
            VRWTau.addWeight("bTagWeight")
            for sam in VRWTau.sampleList:
                if useSyst:
                    if sam.name.find("Top") >= 0 or sam.name.find("W") >= 0:
                        if not useChargeAsymmetry: sam.addSystematic(bTagSys)
                        pass

            VRList.append(VRWTau)
        
        if not useShapeFit:
            VRttbarTau = myFitConfig.addChannel("cuts", ["VRttbarTau"], 1, 0.5, 1.5)
        else:
            VRttbarTau = myFitConfig.addChannel(binVar, ["VRttbarTau"], nBins, minbin, maxbin)
            VRttbarTau.useOverflowBin = True
            VRttbarTau.useUnderflowBin = False
        myFitConfig.setValidationChannels(VRttbarTau)
        if useQCDsample:
            VRttbarTau.addSample(qcdSample)#not for QCDdd
        VRttbarTau.addWeight("bTagWeight")
        for sam in VRttbarTau.sampleList:
            if useSyst:
                if sam.name.find("Top") >= 0 or sam.name.find("W") >= 0:
                    if not useChargeAsymmetry: sam.addSystematic(bTagSys)
                    pass

        VRList.append(VRttbarTau)
