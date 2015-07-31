################################################################
## In principle all you have to setup is defined in this file ##
################################################################
from configManager import configMgr
from ROOT import kBlack,kWhite,kGray,kRed,kPink,kMagenta,kViolet,kBlue,kAzure,kCyan,kTeal,kGreen,kSpring,kYellow,kOrange
from configWriter import fitConfig,Measurement,Channel,Sample
from systematic import Systematic
from math import sqrt

import os

# Setup for ATLAS plotting
from ROOT import gROOT
#gROOT.LoadMacro("./macros/AtlasStyle.C")
import ROOT
#ROOT.SetAtlasStyle()

################################################################
## Configurable options can be set below                      ##
################################################################
useConRegions = False
useValRegions = False
useSigRegions = True 


# where to find inputs
baseDir = '/afs/cern.ch/work/l/leejr/public/SklimmerOutput/fromGrid/rucio/063015a/'



################################################################
## HistFitter attributes                                      ##
################################################################
configMgr.analysisName = "RJigsaw_0lepton_SM_GG_direct_v0"
configMgr.outputFileName = "results/"+configMgr.analysisName+"_Output.root"


# Blinding status:
#configMgr.blindSR = True
#configMgr.blindVR = True

# Hypothesis test paramters:
configMgr.doHypoTest=False
#configMgr.nTOYs=2000
configMgr.calculatorType=2 #0 #for frequentist #2 for asymptotics
configMgr.testStatType=3
configMgr.nPoints=20

configMgr.writeXML = True


################################################################
## Inputs
################################################################
configMgr.inputFileNames = []




################################################################
## Luminosity                                                 ##
################################################################
# scaling calculated by outputLumi / inputLumi
# Question: Are our mini-ntuple normalized to some int. lumi?
# If so, need to do this:
#configMgr.inputLumi = 0.001                       # Luminosity of input TTree after weighting
#configMgr.outputLumi = 20.28 #(20.3837*0.97120714)  # Luminosity of output results
#configMgr.setLumiUnits("fb-1")




################################################################
## Dictionary of 'region' cuts                                ##
################################################################

fitLimits = {} # what we will fit to in control regions

# define control regions
if useConRegions:
    # --- Multijets ---
    
    # --- Wjets ---
    # Example:
    #fitLimits['WJ_CR0LEP_HF']   = ['MR',8,800,1600] # fit in MR
    #configMgr.cutsDict['WJ_CR0LEP_HF']   = '((AnalysisType==1 && AnalysisTypeTrig3==13) || (AnalysisType==2 && AnalysisTypeTrig1==11)) && R>0.3 && R<0.55 && MR>%f && nBJet40==0'%(fitLimits['WJ_CR0LEP_HF'][2]) 

    # --- Zjets ---

    # --- Top ---    

    pass # end if useConRegions

# define validation regions
if useValRegions:
    # --- Multijets ---
    
    # --- Wjets ---
    # Example:
    #fitLimits['WJ_VR0LEP_HF']   = ['MR',6,400,1000] # fit in MR
    #configMgr.cutsDict['WJ_VR0LEP_HF']   = '((AnalysisType==1 && AnalysisTypeTrig3==13) || (AnalysisType==2 && AnalysisTypeTrig1==11)) && R>0.55 && R<1.0 && MR>%f && MR<%f && nBJet40==0'%(fitLimits['WJ_VR0LEP_HF'][2],fitLimits['WJ_VR0LEP_HF'][3])

    # --- Zjets ---

    # --- Top ---    

    pass # end if useValRegions


#### define signal regions ####
if useSigRegions:
    # Example:
    # RvMRcutlist = {'SR_0LEP_HT': [0.60,1.0,900,1500,6]}
    # configMgr.cutsDict['SR_0LEP_HT'] = 'AnalysisType==10 && AnalysisTypeTrig2==102 && met>160 && jet1Pt>200 && jet2Pt>200 && DeltaPhi_jet1_met>1.4 && DeltaPhi_jet2_met>1.4 && R>%f && MR>%f'%(RvMRcutlist['SR_0LEP_HT'][0],RvMRcutlist['SR_0LEP_HT'][2])

    # pass if useSigRegions



################################################################
## Samples                                                    ##
################################################################

#-- ttbar
topSample = Sample("ttbar",kGreen-9) #ichep coloring scheme
topSample.setStatConfig(useStat)
#topSample.setFileList([baseDir+'razor_0leptonBox/HistFitterInputs/UpdatedVars/razor_0leptonBox_Input_PowhegTTbar.root',])


#-- Zjets
zxSample = Sample("ZX",38)
zxSample.setStatConfig(useStat)
#zxSample.setFileList([baseDir+'razor_0leptonBox/HistFitterInputs/UpdatedVars/razor_0leptonBox_Input_Zjets.root',])

#-- Wjets
wxSample = Sample("WX",kAzure+1)
wxSample.setStatConfig(useStat)
#wxSample.setFileList([baseDir+'razor_0leptonBox/HistFitterInputs/UpdatedVars/razor_0leptonBox_Input_Wjets.root',])

#-- Data
dataSample = Sample("Data",kBlack)
dataSample.setData()
#dataSample.setFileList([baseDir+'razor_0leptonBox/HistFitterInputs/UpdatedVars/razor_0leptonBox_Input_Data.root',])


# List of samples:
sampleListMC =  ['ttbar','ZX','WX',]
sampleSet = [dataSample,topSample,zxSample,wxSample] # order of plotting

# Question: not sure what these commands do:
# configMgr.cutsDict["UserRegion"] = "1."
#bkgSample.buildHisto([nbkg],"UserRegion","cuts",0.5)
#bkgSample.buildStatErrors([nbkgErr],"UserRegion","cuts")


################################################################
## Weights                                                   ##
################################################################
# Example of ttbar pt reweighting we did:
# ttbarWeightString = '1.'
# if(doTTbarReweighting==True): ttbarWeightString = '(1.+(117050==RunNumber)*(ttbarWeight-1.))'

# configMgr.weights = ['genWeight','eventWeight',ttbarWeightString,'bTagWeight'] # list of common event weights for all samples
configMgr.weights = "1." # basic setting



################################################################
## Systematics                                                ##
################################################################
# List of systematics.  Type can be 'weight','tree', or 'user'.  Method can be 'histoSys','overallHistoSys','normHistoSys','shapeSys','overallSys', or 'userOverallSys'

# Example of systematic from input tree:
# Systematic('JER', '','_JER'    ,'_JER'      ,'tree','overallNormHistoSysOneSide'),

# Define the nominal sample
#configMgr.nomName = "_NoSys"
configMgr.nomName = ""









################################################################
## Bkg only fit                                               ##
################################################################
bkt = configMgr.addFitConfig("BkgOnlyFit")
bkt.addSamples(sampleSet)


# luminosity uncert
lumiError=0.05
meas = ana.addMeasurement(name="NormalMeasurement",lumi=1.0,lumiErr=lumiError)
meas.addPOI("mu_Sig")


# Add constraints (aka control regions) - make sure that the MR cut is high enough for all the different guys...
constraints = []
print "Adding constraints (aka control regions)"
print "sorted(configMgr.cutsDict) = ",sorted(configMgr.cutsDict)
for acut in sorted(configMgr.cutsDict):
    if not 'CR' in acut: continue
    #constraints += [ bkt.addChannel( fitLimits[acut][0] , [acut] , fitLimits[acut][1] , fitLimits[acut][2] , fitLimits[acut][3] ) ]
    #constraints[-1].logY = True
    #constraints[-1].minY = 0.5
    #constraints[-1].maxY = 1000000000.
    #constraints[-1].showLumi = True
    #constraints[-1].ATLASLabelText = "Internal"
    #constraints[-1].ATLASLabelX = 0.31
    #constraints[-1].ATLASLabelY = 0.64
    pass # end loop over cuts
bkt.setBkgConstrainChannels(constraints)


# Add validation regions 
validations = []
for acut in sorted(configMgr.cutsDict):
    if not 'VR' in acut: continue

    validations += [ bkt.addChannel( fitLimits[acut][0] , [acut] , fitLimits[acut][1] , fitLimits[acut][2] , fitLimits[acut][3] ) ]
    validations[-1].showLumi = True
    validations[-1].ATLASLabelText = "Internal"
    validations[-1].ATLASLabelX = 0.31
    validations[-1].ATLASLabelY = 0.64
    pass # end if validation regions
bkt.setValidationChannels(validations)


# Add signal regions as validation regions
srvalidations = []
for acut in configMgr.cutsDict:

    if not 'SR' in acut: continue

    srvalidations += [ bkt.addChannel('MR',[acut],RvMRcutlist[acut][4],RvMRcutlist[acut][2],RvMRcutlist[acut][3]) ]
    srvalidations[-1].showLumi = True
    srvalidations[-1].ATLASLabelText = "Internal"
    srvalidations[-1].ATLASLabelX = 0.31
    srvalidations[-1].ATLASLabelY = 0.64
    pass # end loop over signal regions as validations
bkt.setValidationChannels(srvalidations)


print bkt # Dump the whole thing... 


################################################################
## Hypthoesis test fits                                       ##
################################################################



# define sigSamples (ex SM_SS_800_100, etc.)
for sig in sigSamples:
    if 'SM_SS_direct' in sig:
        sigFiles = [baseDir+'razor_0leptonBox/HistFitterInputs/UpdatedVars/razor_0leptonBox_Input_SM.root'] # assuming all in one

    myTopLvl = configMgr.addFitConfigClone(bkt,"Sig_%s"%sig)


    sigSample = Sample(sig,kGray) #kPink)
    sigSample.setNormByTheory()
    sigSample.setStatConfig(useStat)
    sigSample.setNormFactor("mu_SIG",1.,0.,5.)
    # add systematics for signal here ...

    myTopLvl.addSamples(sigSample)
    myTopLvl.setSignalSample(sigSample)

    # Add signal regions
    signalregions=[]
    for acut in sorted(configMgr.cutsDict):
        if not 'SR' in acut: continue
        #signalregions += [ bkt.getChannel('MR',[acut]) ]
        #iPop = myTopLvl.validationChannels.index(acut+'_MR')
        myTopLvl.validationChannels.pop(iPop)
    for sr in signalregions:
        sr.useOverflowBin=True
    myTopLvl.setSignalChannels(signalregions)
    pass #end loop over signal samples











# These lines are needed for the user analysis to run
# Make sure file is re-made when executing HistFactory
if configMgr.executeHistFactory:
    if os.path.isfile("data/%s.root"%configMgr.analysisName):
        os.remove("data/%s.root"%configMgr.analysisName) 
