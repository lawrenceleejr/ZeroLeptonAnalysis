################################################################
##
## 2012 Meff binned 0-lepton analysis
## 
## Usage: HistFitter.py -p -t -w -d -f -r "SRE,tight" --exclfit -g "2400_400" analysis/ZeroLepton_example_1DBin2012_Meff.py
## 
################################################################


#----------------------------------------------
# some useful functions
#----------------------------------------------
def myreplace(l1,l2,element):
    idx=l1.index(element)
    if idx>=0:
        return l1[:idx] + l2 + l1[idx+1:]
    else:
        print "WARNING idx negative"
        return l1



#----------------------------------------------
#
#----------------------------------------------
print sys.argv


from configManager import configMgr
from ROOT import kBlack,kWhite,kGray,kRed,kPink,kMagenta,kViolet,kBlue,kAzure,kCyan,kTeal,kGreen,kSpring,kYellow,kOrange
from configWriter import TopLevelXML,Measurement,ChannelXML,Sample
from systematic import Systematic
from math import sqrt
import pickle


#-------------------------------
# Analysis parameters
#-------------------------------

### For the simplest fit setup ###
# Default is True, but for wo stat errors=>False
useStat=True
# Default is True, but for wo systematic errors=>False
useSyst=True
# Default is True, but for wo CR constraints=>False
useCR=True 



### Initialize but will be modified later depending on fit setup ###
chn=0                   #analysis channel 0=A,1=B,..
level='loose'           #loose, medium, tight
meff=1400000            # final meff cut
metomeff=0.3            # final met/meff cut
grid="msugra_0_10_P"           # only grid implemented up to now
allpoints=["2000_400"]  #msugra points given as M0_M12
anaName="test"          #

#final cuts dictionnary
metomeffDefault=(0.3,0.25,0.25,0.20,0.15)
selections={
    'loose' : [(0.4,1000000),           None, (0.30,1000000),           None, (0.30,1000000)],
    'medium': [(0.4,1300000), (0.30,1300000), (0.30,1300000),           None, (0.25,1300000)],
    'tight' : [(0.3,1900000), (0.25,1900000), (0.25,1900000), (0.15,1700000), (0.15,1400000)]
    }

#theo sys on bkg
theoSysTopNumber=0.50
theoSysWNumber=0.50
theoSysZNumber=0.50
theoSysQCDNumber=0.99

useTheoSysOnTF=False          # theo sys on transfer factors
useTheoSysOnlyInSR=False      # theo sys only in SR/VR
useConservativeTheoSys=False  # add had-hoc theo sys in SR/VR 
useTheoSys=True               # fit the theo sys

useQCD=True

# For exclusion limits setting with SigXSec Nominal/Up/Down #
configMgr.fixSigXSec=True

#-------------------------------
# Options
#-------------------------------

# sigSampless is set by the "-g" HistFitter option    
try:
    sigSamples
except NameError:
    sigSamples = None
    
if sigSamples!=None:
    allpoints=sigSamples

# pickedSRs is set by the "-r" HistFitter option    
try:
    pickedSRs
except NameError:
    pickedSRs = None
    
if pickedSRs != None and len(pickedSRs) >= 1: 
    if pickedSRs[0]=="SRA":chn=0
    if pickedSRs[0]=="SRB":chn=1
    if pickedSRs[0]=="SRC":chn=2
    if pickedSRs[0]=="SRD":chn=3
    if pickedSRs[0]=="SRE":chn=4
    metomeff=metomeffDefault[chn]
    
    if len(pickedSRs)>=2 and pickedSRs[1] in selections.keys():
        level=pickedSRs[1]
        meff=selections[pickedSRs[1]][chn][1]
        metomeff=selections[pickedSRs[1]][chn][0]
        anaName=pickedSRs[0]+pickedSRs[1]
    else:
        try:
            anaName=pickedSRs[0]
            if len(pickedSRs)>=2:
                meff=int(pickedSRs[1])*1000
                anaName+="-meff"+pickedSRs[1]
            if len(pickedSRs)>=3:
                metomeff=float(pickedSRs[2])
                anaName+="-metomeff"+pickedSRs[2]
        except:
            print "WARNING: analysis not defined"
            sys.exit()




# No input signal for discovery and bkg fit
if myFitType==FitType.Discovery:
    allpoints=["Discovery"]
if myFitType==FitType.Background:
    allpoints=["Background"]


if meff==None or chn>5 or chn<0:
    print "ERROR analysis not defined!!!"
    print chn,meff
    print pickedSRs
    sys.exit()

# Location of the ntuples
INPUTDIR="/afs/cern.ch/atlas/groups/susy/0lepton/ZeroLeptonFitter/SUSY12/"

#-------------------------------
# Parameters for hypothesis test
#-------------------------------
#configMgr.doHypoTest=False
configMgr.nTOYs=2000      # number of toys when doing frequentist calculator
configMgr.doExclusion=False
if myFitType==FitType.Exclusion:
    configMgr.doExclusion=True 
configMgr.calculatorType=2 # 2=asymptotic calculator, 0=frequentist calculator
configMgr.testStatType=3   # 3=one-sided profile likelihood test statistic (LHC default)
configMgr.nPoints=20       # number of values scanned of signal-strength for upper-limit determination of signal strength.


#-------------------------------------
# Now we start to build the data model
#-------------------------------------

# Scaling calculated by outputLumi / inputLumi
configMgr.inputLumi = 0.001 # Luminosity of input TTree after weighting
configMgr.outputLumi = 5.8 # Luminosity required for output histograms
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
    qcdFiles.append(INPUTDIR+"/QCDdd.root") ##dd means data-driven
    dibosonFiles.append(INPUTDIR+"/DibosonSherpa2011.root")
    dibosonFiles.append(INPUTDIR+"/VGamma.root")
    topFiles.append(INPUTDIR+"/AllTop.root")
    wFiles.append(INPUTDIR+"/W.root")
    zFiles.append(INPUTDIR+"/Z.root")
    gammaFiles.append(INPUTDIR+"/GAMMA.root")
    dataFiles.append(INPUTDIR+"/DataJetTauEtmiss.root")
    dataCRWTFiles.append(INPUTDIR+"/DataEgamma.root")
    dataCRWTFiles.append(INPUTDIR+"/DataMuon.root")
    
 

########################################
# Analysis description
########################################

baselineSR=["(veto==0 && nJet>=2 && jet1Pt>130000 && jet2Pt>60000)",
            "(veto==0 && nJet>=3 && jet1Pt>130000 && jet2Pt>60000 && jet3Pt>60000)",
            "(veto==0 && nJet>=4 && jet1Pt>130000 && jet2Pt>60000 && jet3Pt>60000 && jet4Pt>60000)",
            "(veto==0 && nJet>=5 && jet1Pt>130000 && jet2Pt>60000 && jet3Pt>60000 && jet4Pt>60000 && jet5Pt>60000)",
            "(veto==0 && nJet>=6 && jet1Pt>130000 && jet2Pt>60000 && jet3Pt>60000 && jet4Pt>60000 && jet5Pt>60000 && jet6Pt>60000)"]

dphicut=["(dPhi>0.4)",
         "(dPhi>0.4)",
         "(dPhi>0.4 && dPhiR>0.2)",
         "(dPhi>0.4 && dPhiR>0.2)",
         "(dPhi>0.4 && dPhiR>0.2)"]

invdphicut=["(dPhi<0.2)",
            "(dPhi<0.2)",
            "(dPhi<0.2 || dPhiR<0.2)",
            "(dPhi<0.2 || dPhiR<0.2)",
            "(dPhi<0.2 || dPhiR<0.2)"]


metomeffcut=["(met/meff2Jet>"+str(metomeff)+")",
             "(met/meff3Jet>"+str(metomeff)+")",
             "(met/meff4Jet>"+str(metomeff)+")",
             "(met/meff5Jet>"+str(metomeff)+")",
             "(met/meff6Jet>"+str(metomeff)+")"]


metomeff_delta=0.1
if metomeff>=0.4:    
    metomeff_delta=0.15
if metomeff<=0.15:    
    metomeff_delta=0.05
if (chn==4 and metomeff>=0.3):#sre,loose
    metomeff_delta=0.15
    
metomeffcutqcd=["(met/meff2Jet<"+str(metomeff)+")&&(met/meff2Jet>"+str(metomeff-metomeff_delta)+")",
                "(met/meff3Jet<"+str(metomeff)+")&&(met/meff3Jet>"+str(metomeff-metomeff_delta)+")",
                "(met/meff4Jet<"+str(metomeff)+")&&(met/meff4Jet>"+str(metomeff-metomeff_delta)+")",
                "(met/meff5Jet<"+str(metomeff)+")&&(met/meff5Jet>"+str(metomeff-metomeff_delta)+")",
                "(met/meff6Jet<"+str(metomeff)+")&&(met/meff6Jet>"+str(metomeff-metomeff_delta)+")"]

### For Meff shape fit, define nbin, minbin(s) and maxbin(s) ###
# minbins will be used for meffcuts #
nbin=5
minbin=meff-300000
if pickedSRs[0]=="SRA": minbin=1400000
if pickedSRs[0]=="SRB": minbin=1200000
if pickedSRs[0]=="SRC": minbin=1200000
if pickedSRs[0]=="SRD": minbin=1000000
if pickedSRs[0]=="SRE": minbin=900000
maxbin=1000000+minbin ##meff+nbin*100000-300000  


meffcut="(meffInc>"+str(minbin)+")"

bjetveto="(nBJet==0)"
bjetcut ="(nBJet>0)"
photonSelection="(phQuality == 2 && phIso < 5000.)"

# Signal regions
configMgr.cutsDict["SR"]    = baselineSR[chn]+" && "+dphicut[chn]+" && "+metomeffcut[chn]+" && "+meffcut

# Control regions
configMgr.cutsDict["CRW"]   = baselineSR[chn]+" && "+meffcut+" && "+bjetveto

configMgr.cutsDict["CRT"] = baselineSR[chn]+" && "+meffcut+" && "+bjetcut
configMgr.cutsDict["CR1a"]  = baselineSR[chn]+" && "+dphicut[chn]+" && "+metomeffcut[chn]+" && "+meffcut+"  &&  "+photonSelection
#configMgr.cutsDict["CRQCD"] = baselineSR[chn]+" && "+invdphicut[chn]+" && "+metomeffcut[chn]+" && "+meffcut
#configMgr.cutsDict["CRQCD"] = baselineSR[chn]+" && "+invdphicut[chn]+" && "+metomeffcutqcd[chn]+" && "+meffcut
configMgr.cutsDict["CRQCD"] = baselineSR[chn]+" && jet1Pt>400000 &&"+invdphicut[chn]+" && "+metomeffcutqcd[chn]+" && "+meffcut

# Validation regions
configMgr.cutsDict["VRQ1"] = baselineSR[chn]+" && "+invdphicut[chn]+" &&  "+metomeffcut[chn]+" && "+meffcut
configMgr.cutsDict["VRQ2"] = baselineSR[chn]+" && "+dphicut[chn]+" && "+metomeffcutqcd[chn]+" && "+meffcut
configMgr.cutsDict["VRZ"]   = baselineSR[chn]+" && "+meffcut
configMgr.cutsDict["VRT2L"] = configMgr.cutsDict["VRZ"]+" && mll>116000 &&  lep1Pt<200000 &&  lep2Pt<100000"
configMgr.cutsDict["VRZ_1c"] = configMgr.cutsDict["VRZ"]

configMgr.cutsDict["VRWT_P"]   = baselineSR[chn]+" && "+meffcut+" && "+" lep1sign>0"
configMgr.cutsDict["VRWT_M"]   = baselineSR[chn]+" && "+meffcut+" && "+" lep1sign<0"

# Similar to CRW,CRT and VRZ but with dphicut and met/meff cut applied
configMgr.cutsDict["VRZ1"]     = configMgr.cutsDict["VRZ"]+" && "+dphicut[chn]+" && "+metomeffcut[chn]
configMgr.cutsDict["VRW1"]     = configMgr.cutsDict["CRW"]+" && "+dphicut[chn]+" && "+metomeffcut[chn]
configMgr.cutsDict["VRT1"]     = configMgr.cutsDict["CRT"]+" && "+dphicut[chn]+" && "+metomeffcut[chn]

# Lepton treated as a neutrino
configMgr.cutsDict["VRW2"]     = configMgr.cutsDict["CRW"]
configMgr.cutsDict["VRT2"]     = configMgr.cutsDict["CRT"]

# Similar to VRW2 and VRT2 but with dphicut and met/meff cut applied
configMgr.cutsDict["VRW3"]     = configMgr.cutsDict["VRW2"]+" && "+dphicut[chn]+" && "+metomeffcut[chn]
configMgr.cutsDict["VRT3"]     = configMgr.cutsDict["VRT2"]+" && "+dphicut[chn]+" && "+metomeffcut[chn]


# Tuples of nominal weights
configMgr.weights = ["genWeight","pileupWeight","normWeight"]


#--------------------------------------------------------------------------
# List of systematics
#--------------------------------------------------------------------------
configMgr.nomName = ""


# JES (tree-based)
jes = Systematic("JES","","_JESUP","_JESDOWN","tree","overallNormHistoSys") #"overallHistoSys") #"overallSys")

# JER (tree-based)a
jer = Systematic("JER","","_JER","_JER","tree","overallNormHistoSysOneSideSym") #"histoSysOneSide")

# SCALEST (tree-based)
scalest = Systematic("SCALEST","","_SCALESTUP","_SCALESTDOWN","tree","overallSys")

# RESOST (tree-based)
resost = Systematic("RESOST","","_RESOSTUP","_RESOSTDOWN","tree","overallSys")

# PU
sysWeight_pileupUp=myreplace(configMgr.weights,["pileupWeightUp"],"pileupWeight")
sysWeight_pileupDown=myreplace(configMgr.weights,["pileupWeightDown"],"pileupWeight")
pileup = Systematic("pileup",configMgr.weights,sysWeight_pileupUp,sysWeight_pileupDown,"weight","overallSys")

# b-tag systematics
bTagWeights=configMgr.weights+["bTagWeight"]
bTagSystWeightsUp=myreplace(bTagWeights,["bTagWeightBUp","bTagWeightCUp","bTagWeightLUp"] ,"bTagWeight")
bTagSystWeightsDown=myreplace(bTagWeights,["bTagWeightBDown","bTagWeightCDown","bTagWeightLDown"] ,"bTagWeight")

#bTagTop = Systematic("bTag", bTagWeights ,bTagSystWeightsUp,bTagSystWeightsDown,"weight","overallSys")
#bTagW = Systematic("bTag",bTagWeights,bTagSystWeightsUp,bTagSystWeightsDown,"weight","overallSys")

bTagTop = Systematic("bTag", bTagWeights ,bTagSystWeightsUp,bTagSystWeightsDown,"weight","overallNormHistoSys") #"overallSys")
bTagW = Systematic("bTag",bTagWeights,bTagSystWeightsUp,bTagSystWeightsDown,"weight","overallNormHistoSys") #"overallSys")

# photon systematics
photonWeights=configMgr.weights+["photonWeight","triggerWeight"]
photonSystWeightsUp=myreplace(photonWeights,["photonWeightUp"] ,"photonWeight")
photonSystWeightsDown=myreplace(photonWeights,["photonWeightDown"] ,"photonWeight")
photonSys = Systematic("photonSys", photonWeights ,photonSystWeightsUp,photonSystWeightsDown,"weight","overallSys")

# trigger scaling
triggerSystWeightsUp=myreplace(photonWeights,["triggerWeightUp"] ,"triggerWeight")
triggerSystWeightsDown=myreplace(photonWeights,["triggerWeightDown"] ,"triggerWeight")
triggerSys = Systematic("triggerSys", photonWeights ,triggerSystWeightsUp,triggerSystWeightsDown,"weight","overallSys")



#--------------------------------------------------------------------------
# List of theo systematics
#--------------------------------------------------------------------------


#conservative theo sys
theoConservativeSysTop = Systematic("theoConservativeSysTop", configMgr.weights, 1.+theoSysTopNumber,1.-theoSysTopNumber, "user","userOverallSys")
theoConservativeSysW = Systematic("theoConservativeSysW", configMgr.weights, 1.+theoSysWNumber,1.-theoSysWNumber, "user","userOverallSys")
theoConservativeSysZ = Systematic("theoConservativeSysZ", configMgr.weights, 1.+theoSysZNumber,1.-theoSysZNumber, "user","userOverallSys")


# signal
sysWeight_theoSysSigUp=myreplace(configMgr.weights,["normWeightUp"],"normWeight")
sysWeight_theoSysSigDown=myreplace(configMgr.weights,["normWeightDown"],"normWeight")
theoSysSig = Systematic("SigXSec",configMgr.weights,sysWeight_theoSysSigUp,sysWeight_theoSysSigDown,"weight","overallSys") #"overallNormHistoSys")

# MC theo systematics
theoSysTop = Systematic("theoSysTop","","_Sherpa","_Sherpa","tree","normHistoSysOneSide") 

mu1ScaleSysTop = Systematic("mu1ScaleSys",configMgr.weights,configMgr.weights+["mu1ScaleWeightUp"],configMgr.weights+["mu1ScaleWeightDown"],"weight","overallNormHistoSys") #"overallSys")
mu2ScaleSysTop = Systematic("mu2ScaleSys",configMgr.weights,configMgr.weights+["mu2ScaleWeightUp"],configMgr.weights+["mu2ScaleWeightDown"],"weight","overallNormHistoSys") #"overallSys")
matchScaleSysTop = Systematic("matchScaleSys",configMgr.weights,configMgr.weights+["matchScaleWeightUp"],configMgr.weights+["matchScaleWeightDown"],"weight","overallNormHistoSys") #"overallSys")

# W MC
#theoSysW = Systematic("theoSysW", configMgr.weights, 1.0+theoSysWNumber,1.0-theoSysWNumber, "user","userOverallSys")
mu1ScaleSysW = Systematic("mu1ScaleSys",configMgr.weights,configMgr.weights+["mu1ScaleWeightUp"],configMgr.weights+["mu1ScaleWeightDown"],"weight","overallNormHistoSys") #"overallSys")
mu2ScaleSysW = Systematic("mu2ScaleSys",configMgr.weights,configMgr.weights+["mu2ScaleWeightUp"],configMgr.weights+["mu2ScaleWeightDown"],"weight","overallNormHistoSys") #"overallSys")
matchScaleSysW = Systematic("matchScaleSys",configMgr.weights,configMgr.weights+["matchScaleWeightUp"],configMgr.weights+["matchScaleWeightDown"],"weight","overallNormHistoSys") #"overallSys")
sherpaBugSigW=myreplace(configMgr.weights,["normWeightUp"],"normWeight")
sherpaBugW = Systematic("sherpaBugW",configMgr.weights,sherpaBugSigW,sherpaBugSigW   ,"weight","normHistoSysOneSideSym") #"histoSysOneSide")
nPartonsSysW = Systematic("nPartonsSysW",configMgr.weights,configMgr.weights+["nPartonsWeight"],configMgr.weights+["nPartonsWeight"],"weight","overallNormHistoSysOneSideSym") #"histoSysOneSide")

# Z MC
mu1ScaleSysZ = Systematic("mu1ScaleSys",configMgr.weights,configMgr.weights+["mu1ScaleWeightUp"],configMgr.weights+["mu1ScaleWeightDown"],"weight","overallNormHistoSys") #"overallSys")
mu2ScaleSysZ = Systematic("mu2ScaleSys",configMgr.weights,configMgr.weights+["mu2ScaleWeightUp"],configMgr.weights+["mu2ScaleWeightDown"],"weight","overallNormHistoSys") #"overallSys")
matchScaleSysZ = Systematic("matchScaleSys",configMgr.weights,configMgr.weights+["matchScaleWeightUp"],configMgr.weights+["matchScaleWeightDown"],"weight","overallNormHistoSys") #"overallSys")

# Photon systematics in SR for Z
#gammaToZSyst = Systematic("gammaToZSyst", configMgr.weights, 1.25,0.75, "user","userOverallSys")

# QCD
theoSysQCD = Systematic("theoSysQCD", configMgr.weights, 1.0+theoSysQCDNumber,1.0-theoSysQCDNumber, "user","userOverallSys")

QCDGausSys = Systematic("QCDGausSys","","_ghi","_glo","tree","overallNormHistoSys")
QCDTailSys = Systematic("QCDTailSys","","_thi","_tlo","tree","overallNormHistoSys")

# Diboson
theoSysDiboson = Systematic("theoSysDiboson", configMgr.weights, 1.5,0.5, "user","userOverallSys")




#--------------------------------------------------------------------------
# Systematics on TF
#--------------------------------------------------------------------------
if useTheoSysOnTF==True:
    f = open('data/SRsyst.pkl','rb')
    import pickle
    WMap = pickle.load(f)
    ZMap = pickle.load(f)
    TopMap = pickle.load(f)

    mu1ScaleTFSysW  = Systematic("mu1ScaleTFSys", configMgr.weights, 1.0+WMap['mu1ScaleWeightUp'][level][chn],1.0-WMap['mu1ScaleWeightDown'][level][chn], "user","userOverallSys")
    mu2ScaleTFSysW  = Systematic("mu2ScaleTFSys", configMgr.weights, 1.0+WMap['mu2ScaleWeightUp'][level][chn],1.0-WMap['mu2ScaleWeightDown'][level][chn], "user","userOverallSys")
    matchScaleTFSysW  = Systematic("matchScaleTFSys", configMgr.weights, 1.0+WMap['matchScaleWeightUp'][level][chn],1.0, "user","userOverallSys")
    
    
    mu1ScaleTFSysZ  = Systematic("mu1ScaleTFSys", configMgr.weights, 1.0+ZMap['mu1ScaleWeightUp'][level][chn],1.0-ZMap['mu1ScaleWeightDown'][level][chn], "user","userOverallSys")
    mu2ScaleTFSysZ  = Systematic("mu2ScaleTFSys", configMgr.weights, 1.0+ZMap['mu2ScaleWeightUp'][level][chn],1.0-ZMap['mu2ScaleWeightDown'][level][chn], "user","userOverallSys")

    sherpaTFSysTop  = Systematic("sherpaTFSys", configMgr.weights, 1.0+TopMap['topSherpa'][level][chn],1.0-TopMap['topSherpa'][level][chn], "user","userOverallSys")
    


#-------------------------------------------
# List of samples and their plotting colours
#-------------------------------------------
dibosonSample = Sample("Diboson",kRed+3)
dibosonSample.setTreeName("Diboson_SRAll")
dibosonSample.setFileList(dibosonFiles)
dibosonSample.setStatConfig(useStat)
if useSyst: dibosonSample.addSystematic(theoSysDiboson)


topSample = Sample("ttbar",kGreen-9)
topSample.setTreeName("Top_SRAll")
topSample.setNormFactor("mu_Top",1.,0.,500.)
topSample.setFileList(topFiles)
topSample.setStatConfig(useStat) 
if useTheoSys:
    if useSyst: topSample.addSystematic(theoSysTop)
    ####topSample.addSystematic(mu1ScaleSysTop)
    ####topSample.addSystematic(mu2ScaleSysTop)
    ####topSample.addSystematic(matchScaleSysTop)
topSample.setNormRegions([("CRT","meffInc"),("CRW","meffInc")])


qcdSample = Sample("Multijets",kOrange+2)
qcdSample.setTreeName("QCDdd")
qcdSample.setNormFactor("mu_Multijets",1.,0.,500.)
qcdSample.setFileList(qcdFiles)
qcdSample.setStatConfig(useStat)
qcdSample.addWeight("0.000001")#qcd prenormalisation
#qcdSample.addSystematic(QCDGausSys)
#qcdSample.addSystematic(QCDTailSys)
qcdSample.setNormRegions([("CRQCD","meffInc")])

    
wSample = Sample("Wjets",kAzure+1)
wSample.setTreeName("W_SRAll")
wSample.setNormFactor("mu_W",1.,0.,500.)
wSample.setFileList(wFiles)
wSample.setStatConfig(useStat)
if useTheoSys:
    if useSyst: wSample.addSystematic(mu1ScaleSysW)
    if useSyst: wSample.addSystematic(mu2ScaleSysW)
    if useSyst: wSample.addSystematic(matchScaleSysW)
    if useSyst: wSample.addSystematic(sherpaBugW)
    if useSyst: wSample.addSystematic(nPartonsSysW)
wSample.setNormRegions([("CRT","meffInc"),("CRW","meffInc")])


gammaSample = Sample("GAMMAjets",kYellow)
gammaSample.setTreeName("GAMMA_SRAll")
gammaSample.setNormFactor("mu_Z",1.,0.,500.)
gammaSample.setFileList(gammaFiles)
gammaSample.setStatConfig(useStat)
if useTheoSys:
    if useSyst: gammaSample.addSystematic(mu1ScaleSysZ)
    if useSyst: gammaSample.addSystematic(mu2ScaleSysZ)
    if useSyst: gammaSample.addSystematic(matchScaleSysZ)
gammaSample.setNormRegions([("CR1a","meffInc")])
#gammaSample.noRenormSys = True


zSample = Sample("Zjets",kBlue)
zSample.setTreeName("Z_SRAll")
zSample.setNormFactor("mu_Z",1.,0.,500.)
zSample.setFileList(zFiles)
zSample.setStatConfig(useStat)
if useTheoSys:
    if useSyst: zSample.addSystematic(mu1ScaleSysZ)
    if useSyst: zSample.addSystematic(mu2ScaleSysZ)
    if useSyst: zSample.addSystematic(matchScaleSysZ)
zSample.setNormRegions([("CR1a","meffInc")]) 
#zSample.setNormRegions([("CRT","cuts"),("CRW","cuts"),("CR1a","cuts")])
zSample.normSampleRemap = "GAMMAjets"


dataSample = Sample("Data",kBlack)
dataSample.setTreeName("Data_SRAll")
dataSample.setData()
dataSample.setFileList(dataFiles)


#**************
# Exclusion fit
#**************

# First define HistFactory attributes
configMgr.analysisName = "ZL_1DBin2012_Meff_"+anaName+"_meff"+str(minbin)+"-"+str(maxbin)+"_nbin"+str(nbin)+"_"+grid+"_"+allpoints[0]
configMgr.histCacheFile = "data/"+configMgr.analysisName+".root"
configMgr.outputFileName = "results/"+configMgr.analysisName+"_Output.root"


for point in allpoints:
    if point=="":continue
    
    # Fit config instance
    name="Fit_"+"_"+point
    myFitConfig = configMgr.addTopLevelXML(name)
    if useStat:
        myFitConfig.statErrThreshold=0.05 
    else:
        myFitConfig.statErrThreshold=None
        
    meas=myFitConfig.addMeasurement(name="NormalMeasurement",lumi=1.0,lumiErr=0.039)
    meas.addPOI("mu_SIG")
    meas.addParamSetting("mu_Diboson",True,1) # fix diboson to MC prediction
    

    # Samples
    #myFitConfig.addSamples([gammaSample,topSample,wSample,zSample,qcdSample,dibosonSample,dataSample])
    #if useQCD==True:
    #    myFitConfig.addSamples([qcdSample,topSample,wSample,zSample,dataSample])
    #else:
    myFitConfig.addSamples([dibosonSample,topSample,wSample,zSample,dataSample])
        

    #-------------------------------------------------
    # Signal
    #-------------------------------------------------
    sigSampleName=grid+"_"+point
    if myFitType==FitType.Exclusion:
        sigSample = Sample(sigSampleName,kRed)
        sigSample.setFileList([INPUTDIR+grid+".root"])
        sigSample.setTreeName(grid+"_"+point+"_SRAll")
        sigSample.setNormByTheory()
        sigSample.setNormFactor("mu_SIG",1,0.,100.)
        sigSample.addSystematic(theoSysSig)
        sigSample.setStatConfig(useStat)
        myFitConfig.addSamples(sigSample)
        myFitConfig.setSignalSample(sigSample)
    
    #Channel
    SR = myFitConfig.addChannel("meffInc",["SR"],nbin,minbin,maxbin)
    SR.useOverflowBin=True
    SR.useUnderflowBin=False
    if useQCD==True:
        SR.addSample(qcdSample)
    for sam in SR.sampleList:
        if sam.name.find("Multijets")>=0:                       
            if useSyst: sam.addSystematic(theoSysQCD)
            pass        
        if sam.name.find("ttbar")>=0   or   sam.name.find("W")>=0 or  sam.name.find("Z")>=0 or  sam.name.find("Diboson")>=0 or  sam.name.find(sigSampleName)>=0: 
            if useSyst: sam.addSystematic(pileup)
            if useSyst: sam.addSystematic(jes)
            if useSyst: sam.addSystematic(jer)
            if useSyst: sam.addSystematic(scalest)
            if useSyst: sam.addSystematic(resost) 
            
        if useConservativeTheoSys:
            if sam.name.find("ttbar")>=0:  
                if useSyst: sam.addSystematic(theoConservativeSysTop)
            if sam.name.find("Wjets")>=0:  
                if useSyst: sam.addSystematic(theoConservativeSysW)
            if sam.name.find("Zjets")>=0:  
                if useSyst: sam.addSystematic(theoConservativeSysZ)

        if useTheoSysOnlyInSR:
            if sam.name.find("ttbar")>=0:  
                if useSyst: sam.addSystematic(theoSysTop)
            if sam.name.find("Wjets")>=0:  
                if useSyst: sam.addSystematic(mu1ScaleSysW)
                if useSyst: sam.addSystematic(mu2ScaleSysW)
                if useSyst: sam.addSystematic(matchScaleSysW)
                if useSyst: sam.addSystematic(sherpaBugW)
                if useSyst: sam.addSystematic(nPartonsSysW)
            if sam.name.find("Zjets")>=0:  
                if useSyst: sam.addSystematic(mu1ScaleSysZ)
                if useSyst: sam.addSystematic(mu2ScaleSysZ)
                if useSyst: sam.addSystematic(matchScaleSysZ)

        if useTheoSysOnTF:
            if sam.name.find("ttbar")>=0:  
                if useSyst: sam.addSystematic(sherpaTFSysTop)
                pass
            if sam.name.find("Wjets")>=0:  
                if useSyst: sam.addSystematic(mu1ScaleTFSysW)
                if useSyst: sam.addSystematic(mu2ScaleTFSysW)
                if useSyst: sam.addSystematic(matchScaleTFSysW)
                #if useSyst: sam.addSystematic(sherpaBugW)
                #if useSyst: sam.addSystematic(nPartonsTFSysW)
            if sam.name.find("Zjets")>=0:  
                if useSyst: sam.addSystematic(mu1ScaleTFSysZ)
                if useSyst: sam.addSystematic(mu2ScaleTFSysZ)
                #if useSyst: sam.addSystematic(matchScaleTFSysZ)
                pass


    if myFitType!=FitType.Background:
        myFitConfig.setSignalChannels([SR]) 
    else:
        myFitConfig.setValidationChannels(SR) 
            
    if myFitType==FitType.Discovery:
        SR.addDiscoverySamples(["SIG"],[1.],[0.],[100.],[kMagenta])


    #-------------------------------------------------
    # Constraining regions - statistically independent
    #-------------------------------------------------
    ### For Meff shape fit ###
    CRGAMMA = myFitConfig.addChannel("meffInc",["CR1a"],nbin,minbin,maxbin)
    CRGAMMA.useOverflowBin=True
    CRGAMMA.useUnderflowBin=False
    if useSyst: CRGAMMA.addSystematic(pileup)
    if useSyst: CRGAMMA.addSystematic(jes)
    if useSyst: CRGAMMA.addSystematic(jer)
    if useSyst: CRGAMMA.addSystematic(scalest)
    if useSyst: CRGAMMA.addSystematic(resost)
    CRGAMMA.addSample(gammaSample,0)
    for sam in CRGAMMA.sampleList:
        sam.setTreeName(sam.treeName.replace("SRAll","CR1a"))
        if sam.name.find("GAMMA")>=0:
            sam.addWeight("photonWeight")
            sam.addWeight("triggerWeight") 
            if useSyst: sam.addSystematic(photonSys)
            if useSyst: sam.addSystematic(triggerSys)
            if useSyst: sam.addSystematic(pileup)
            if useSyst: sam.addSystematic(jes)
            if useSyst: sam.addSystematic(jer)
            if useSyst: sam.addSystematic(scalest)
            if useSyst: sam.addSystematic(resost) 
            pass           
        if sam.treeName.find("Data")>=0:
            sam.setFileList(dataCRWTFiles)
        pass 
    if useCR: myFitConfig.setBkgConstrainChannels(CRGAMMA)


    CRT = myFitConfig.addChannel("meffInc",["CRT"],nbin,minbin,maxbin)
    CRT.useOverflowBin=True
    CRT.useUnderflowBin=False
    if useSyst: CRT.addSystematic(pileup)
    if useSyst: CRT.addSystematic(jes)
    if useSyst: CRT.addSystematic(jer)
    if useSyst: CRT.addSystematic(scalest)
    if useSyst: CRT.addSystematic(resost)
    CRT.addWeight("bTagWeight")    
    for sam in CRT.sampleList:
        sam.setTreeName(sam.treeName.replace("SRAll","CRWT"))
        if sam.name.find("ttbar")>=0:                       
            if useSyst: sam.addSystematic(bTagTop)
            pass
        if sam.name.find("W")>=0:                       
            if useSyst: sam.addSystematic(bTagW)
            pass            
        if sam.treeName.find("Data")>=0:
            sam.setFileList(dataCRWTFiles)
            pass
        pass
    if useCR: myFitConfig.setBkgConstrainChannels(CRT)

    CRW = myFitConfig.addChannel("meffInc",["CRW"],nbin,minbin,maxbin)
    CRW.useOverflowBin=True
    CRW.useUnderflowBin=False
    if useSyst: CRW.addSystematic(pileup)
    if useSyst: CRW.addSystematic(jes)
    if useSyst: CRW.addSystematic(jer)
    if useSyst: CRW.addSystematic(scalest)
    if useSyst: CRW.addSystematic(resost) 
    CRW.addWeight("bTagWeight")
    for sam in CRW.sampleList:
        sam.setTreeName(sam.treeName.replace("SRAll","CRWT"))
        if sam.name.find("ttbar")>=0:                       
            if useSyst: sam.addSystematic(bTagTop)
            pass
        if sam.name.find("W")>=0:                       
            if useSyst: sam.addSystematic(bTagW)
            pass    
        if sam.treeName.find("Data")>=0:
            sam.setFileList(dataCRWTFiles)
        pass
    if useCR: myFitConfig.setBkgConstrainChannels(CRW)
    
    if useQCD==True:
        CRQCD = myFitConfig.addChannel("meffInc",["CRQCD"],nbin,minbin,maxbin)
        CRQCD.useOverflowBin=True
        CRQCD.useUnderflowBin=False
        if useCR: myFitConfig.setBkgConstrainChannels(CRQCD)
        CRQCD.addSample(qcdSample)
        CRQCD.addWeight("(genWeight<400)")    #reject events with large weights
        for sam in CRQCD.sampleList:
            if sam.name.find("ttbar")>=0   or   sam.name.find("W")>=0 or  sam.name.find("Z")>=0 or  sam.name.find("Diboson")>=0 or  sam.name.find(sigSampleName)>=0:
                #if useSyst: sam.addSystematic(pileup) #ATT: remove due to fit instability
                if useSyst: sam.addSystematic(jes)
                if useSyst: sam.addSystematic(jer)
                if useSyst: sam.addSystematic(scalest)
                if useSyst: sam.addSystematic(resost)



    if doValidation:
        if not (len(pickedSRs)>=2 and pickedSRs[1].find("tight")>=0 and pickedSRs[0]=="SRD"): #no stat in SRD,tight
            VRZ = myFitConfig.addChannel("cuts",["VRZ"],1,0.5,1.5)
            if useSyst: VRZ.addSystematic(pileup)
            if useSyst: VRZ.addSystematic(jes)
            if useSyst: VRZ.addSystematic(jer)
            if useSyst: VRZ.addSystematic(scalest)
            if useSyst: VRZ.addSystematic(resost)
            for sam in VRZ.sampleList:
                sam.setTreeName(sam.treeName.replace("SRAll","CRZ"))
                if sam.treeName.find("Data")>=0:
                    sam.setFileList(dataCRWTFiles)
                    pass
                if useConservativeTheoSys:
                    if sam.name.find("ttbar")>=0:  
                        if useSyst: sam.addSystematic(theoConservativeSysTop)
                    if sam.name.find("Wjets")>=0:  
                        if useSyst: sam.addSystematic(theoConservativeSysW)
                    if sam.name.find("Zjets")>=0:  
                        if useSyst: sam.addSystematic(theoConservativeSysZ)
                if useTheoSysOnlyInSR:
                    if sam.name.find("ttbar")>=0:  
                        if useSyst: sam.addSystematic(theoSysTop)
                    if sam.name.find("Wjets")>=0:  
                        if useSyst: sam.addSystematic(mu1ScaleSysW)
                        if useSyst: sam.addSystematic(mu2ScaleSysW)
                        if useSyst: sam.addSystematic(matchScaleSysW)
                        if useSyst: sam.addSystematic(sherpaBugW)
                        if useSyst: sam.addSystematic(nPartonsSysW)
                    if sam.name.find("Zjets")>=0:  
                        if useSyst: sam.addSystematic(mu1ScaleSysZ)
                        if useSyst: sam.addSystematic(mu2ScaleSysZ)
                        if useSyst: sam.addSystematic(matchScaleSysZ)
            myFitConfig.setValidationChannels(VRZ)


        
        if len(pickedSRs)>=2 and pickedSRs[1].find("tight")<0:
            VRZ_1b = myFitConfig.addChannel("cuts",["VRT2L"],1,0.5,1.5)
            if useSyst: VRZ_1b.addSystematic(pileup)
            if useSyst: VRZ_1b.addSystematic(jes)
            if useSyst: VRZ_1b.addSystematic(jer)
            if useSyst: VRZ_1b.addSystematic(scalest)
            if useSyst: VRZ_1b.addSystematic(resost)
            for sam in VRZ_1b.sampleList:
                sam.setTreeName(sam.treeName.replace("SRAll","CRZ_VR1b"))
                if sam.treeName.find("Data")>=0:
                    sam.setFileList(dataCRWTFiles)
                    pass
                if useConservativeTheoSys:
                    if sam.name.find("ttbar")>=0:  
                        if useSyst: sam.addSystematic(theoConservativeSysTop)
                    if sam.name.find("Wjets")>=0:  
                        if useSyst: sam.addSystematic(theoConservativeSysW)
                    if sam.name.find("Zjets")>=0:  
                        if useSyst: sam.addSystematic(theoConservativeSysZ)
                if useTheoSysOnlyInSR:
                    if sam.name.find("ttbar")>=0:  
                        if useSyst: sam.addSystematic(theoSysTop)
                    if sam.name.find("Wjets")>=0:  
                        if useSyst: sam.addSystematic(mu1ScaleSysW)
                        if useSyst: sam.addSystematic(mu2ScaleSysW)
                        if useSyst: sam.addSystematic(matchScaleSysW)
                        if useSyst: sam.addSystematic(sherpaBugW)
                        if useSyst: sam.addSystematic(nPartonsSysW)
                    if sam.name.find("Zjets")>=0:  
                        if useSyst: sam.addSystematic(mu1ScaleSysZ)
                        if useSyst: sam.addSystematic(mu2ScaleSysZ)
                        if useSyst: sam.addSystematic(matchScaleSysZ)
                pass
            myFitConfig.setValidationChannels(VRZ_1b)

            
##         VRZfull = myFitConfig.addChannel("cuts",["VRZfull"],1,0.5,1.5)
##         for sam in VRZfull.sampleList:
##             sam.setTreeName(sam.treeName.replace("SRAll","CRZ"))
##             if sam.treeName.find("Data")>=0:
##                 sam.setFileList(dataCRWTFiles)
##                 pass
##         myFitConfig.setValidationChannels(VRZfull)
            
##         VRZ_1b = myFitConfig.addChannel("cuts",["VRZ_1b"],1,0.5,1.5)
##         for sam in VRZ_1b.sampleList:
##             sam.setTreeName(sam.treeName.replace("SRAll","CRZ_VR1b"))
##             if sam.treeName.find("Data")>=0:
##                 sam.setFileList(dataCRWTFiles)
##                 pass
##         myFitConfig.setValidationChannels(VRZ_1b)

##         VRZ_1c = myFitConfig.addChannel("cuts",["VRZ_1c"],1,0.5,1.5)
##         for sam in VRZ_1c.sampleList:
##             sam.setTreeName(sam.treeName.replace("SRAll","CRZ_VR1c"))
##             if sam.treeName.find("Data")>=0:
##                 sam.setFileList(dataCRWTFiles)
##                 pass
##         myFitConfig.setValidationChannels(VRZ_1c)


        VRWT_P = myFitConfig.addChannel("cuts",["VRWT_P"],1,0.5,1.5)
        if useSyst: VRWT_P.addSystematic(pileup)
        if useSyst: VRWT_P.addSystematic(jes)
        if useSyst: VRWT_P.addSystematic(jer)
        if useSyst: VRWT_P.addSystematic(scalest)
        if useSyst: VRWT_P.addSystematic(resost)
        for sam in VRWT_P.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll","CRWT"))
            if sam.treeName.find("Data")>=0:
                sam.setFileList(dataCRWTFiles)
                pass
            if useTheoSysOnlyInSR:
                if sam.name.find("ttbar")>=0:  
                    if useSyst: sam.addSystematic(theoSysTop)
                if sam.name.find("Wjets")>=0:  
                    if useSyst: sam.addSystematic(mu1ScaleSysW)
                    if useSyst: sam.addSystematic(mu2ScaleSysW)
                    if useSyst: sam.addSystematic(matchScaleSysW)
                    if useSyst: sam.addSystematic(sherpaBugW)
                    if useSyst: sam.addSystematic(nPartonsSysW)
                if sam.name.find("Zjets")>=0:  
                    if useSyst: sam.addSystematic(mu1ScaleSysZ)
                    if useSyst: sam.addSystematic(mu2ScaleSysZ)
                    if useSyst: sam.addSystematic(matchScaleSysZ)
            if useConservativeTheoSys:
                if sam.name.find("ttbar")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysTop)
                if sam.name.find("Wjets")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysW)
                if sam.name.find("Zjets")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysZ)
        myFitConfig.setValidationChannels(VRWT_P)

        
        VRWT_M = myFitConfig.addChannel("cuts",["VRWT_M"],1,0.5,1.5)
        if useSyst: VRWT_M.addSystematic(pileup)
        if useSyst: VRWT_M.addSystematic(jes)
        if useSyst: VRWT_M.addSystematic(jer)
        if useSyst: VRWT_M.addSystematic(scalest)
        if useSyst: VRWT_M.addSystematic(resost)
        for sam in VRWT_M.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll","CRWT"))
            if sam.treeName.find("Data")>=0:
                sam.setFileList(dataCRWTFiles)
                pass
            if useConservativeTheoSys:
                if sam.name.find("ttbar")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysTop)
                if sam.name.find("Wjets")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysW)
                if sam.name.find("Zjets")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysZ)
            if useTheoSysOnlyInSR:
                if sam.name.find("ttbar")>=0:  
                    if useSyst: sam.addSystematic(theoSysTop)
                if sam.name.find("Wjets")>=0:  
                    if useSyst: sam.addSystematic(mu1ScaleSysW)
                    if useSyst: sam.addSystematic(mu2ScaleSysW)
                    if useSyst: sam.addSystematic(matchScaleSysW)
                    if useSyst: sam.addSystematic(sherpaBugW)
                    if useSyst: sam.addSystematic(nPartonsSysW)
                if sam.name.find("Zjets")>=0:  
                    if useSyst: sam.addSystematic(mu1ScaleSysZ)
                    if useSyst: sam.addSystematic(mu2ScaleSysZ)
                    if useSyst: sam.addSystematic(matchScaleSysZ)
        myFitConfig.setValidationChannels(VRWT_M)




 
        VRW1 = myFitConfig.addChannel("cuts",["VRW1"],1,0.5,1.5)
        if useSyst: VRW1.addSystematic(pileup)
        if useSyst: VRW1.addSystematic(jes)
        if useSyst: VRW1.addSystematic(jer)
        if useSyst: VRW1.addSystematic(scalest)
        if useSyst: VRW1.addSystematic(resost)
        for sam in VRW1.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll","CRWT"))
            if sam.treeName.find("Data")>=0:
                sam.setFileList(dataCRWTFiles)
                pass
            if useTheoSysOnlyInSR:
                if sam.name.find("ttbar")>=0:  
                    if useSyst: sam.addSystematic(theoSysTop)
                if sam.name.find("Wjets")>=0:  
                    if useSyst: sam.addSystematic(mu1ScaleSysW)
                    if useSyst: sam.addSystematic(mu2ScaleSysW)
                    if useSyst: sam.addSystematic(matchScaleSysW)
                    if useSyst: sam.addSystematic(sherpaBugW)
                    if useSyst: sam.addSystematic(nPartonsSysW)
                if sam.name.find("Zjets")>=0:  
                    if useSyst: sam.addSystematic(mu1ScaleSysZ)
                    if useSyst: sam.addSystematic(mu2ScaleSysZ)
                    if useSyst: sam.addSystematic(matchScaleSysZ)
            if useConservativeTheoSys:
                if sam.name.find("ttbar")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysTop)
                if sam.name.find("Wjets")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysW)
                if sam.name.find("Zjets")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysZ)
        myFitConfig.setValidationChannels(VRW1)


        VRT1 = myFitConfig.addChannel("cuts",["VRT1"],1,0.5,1.5)
        if useSyst: VRT1.addSystematic(pileup)
        if useSyst: VRT1.addSystematic(jes)
        if useSyst: VRT1.addSystematic(jer)
        if useSyst: VRT1.addSystematic(scalest)
        if useSyst: VRT1.addSystematic(resost)
        for sam in VRT1.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll","CRWT"))
            if sam.treeName.find("Data")>=0:
                sam.setFileList(dataCRWTFiles)
                pass
            if useTheoSysOnlyInSR:
                if sam.name.find("ttbar")>=0:  
                    if useSyst: sam.addSystematic(theoSysTop)
                if sam.name.find("Wjets")>=0:  
                    if useSyst: sam.addSystematic(mu1ScaleSysW)
                    if useSyst: sam.addSystematic(mu2ScaleSysW)
                    if useSyst: sam.addSystematic(matchScaleSysW)
                    if useSyst: sam.addSystematic(sherpaBugW)
                    if useSyst: sam.addSystematic(nPartonsSysW)
                if sam.name.find("Zjets")>=0:  
                    if useSyst: sam.addSystematic(mu1ScaleSysZ)
                    if useSyst: sam.addSystematic(mu2ScaleSysZ)
                    if useSyst: sam.addSystematic(matchScaleSysZ)
            if useConservativeTheoSys:
                if sam.name.find("ttbar")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysTop)
                if sam.name.find("Wjets")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysW)
                if sam.name.find("Zjets")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysZ)
        myFitConfig.setValidationChannels(VRT1)




        VRW2 = myFitConfig.addChannel("cuts",["VRW2"],1,0.5,1.5)
        VRW2.addSystematic(pileup)
        VRW2.addSystematic(jes)
        VRW2.addSystematic(jer)
        VRW2.addSystematic(scalest)
        VRW2.addSystematic(resost)
        for sam in VRW2.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll","VRWT_SRAll"))
            if sam.treeName.find("Data")>=0:
                sam.setFileList(dataCRWTFiles)
                pass
            if useTheoSysOnlyInSR:
                if sam.name.find("ttbar")>=0:  
                    if useSyst: sam.addSystematic(theoSysTop)
                if sam.name.find("Wjets")>=0:  
                    if useSyst: sam.addSystematic(mu1ScaleSysW)
                    if useSyst: sam.addSystematic(mu2ScaleSysW)
                    if useSyst: sam.addSystematic(matchScaleSysW)
                    if useSyst: sam.addSystematic(sherpaBugW)
                    if useSyst: sam.addSystematic(nPartonsSysW)
                if sam.name.find("Zjets")>=0:  
                    if useSyst: sam.addSystematic(mu1ScaleSysZ)
                    if useSyst: sam.addSystematic(mu2ScaleSysZ)
                    if useSyst: sam.addSystematic(matchScaleSysZ)
            if useConservativeTheoSys:
                if sam.name.find("ttbar")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysTop)
                if sam.name.find("Wjets")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysW)
                if sam.name.find("Zjets")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysZ)
        myFitConfig.setValidationChannels(VRW2)


        VRT2 = myFitConfig.addChannel("cuts",["VRT2"],1,0.5,1.5)
        if useSyst: VRT2.addSystematic(pileup)
        if useSyst: VRT2.addSystematic(jes)
        if useSyst: VRT2.addSystematic(jer)
        if useSyst: VRT2.addSystematic(scalest)
        if useSyst: VRT2.addSystematic(resost)
        for sam in VRT2.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll","VRWT_SRAll"))
            if sam.treeName.find("Data")>=0:
                sam.setFileList(dataCRWTFiles)
                pass
            if useTheoSysOnlyInSR:
                if sam.name.find("ttbar")>=0:  
                    if useSyst: sam.addSystematic(theoSysTop)
                if sam.name.find("Wjets")>=0:  
                    if useSyst: sam.addSystematic(mu1ScaleSysW)
                    if useSyst: sam.addSystematic(mu2ScaleSysW)
                    if useSyst: sam.addSystematic(matchScaleSysW)
                    if useSyst: sam.addSystematic(sherpaBugW)
                    if useSyst: sam.addSystematic(nPartonsSysW)
                if sam.name.find("Zjets")>=0:  
                    if useSyst: sam.addSystematic(mu1ScaleSysZ)
                    if useSyst: sam.addSystematic(mu2ScaleSysZ)
                    if useSyst: sam.addSystematic(matchScaleSysZ)
            if useConservativeTheoSys:
                if sam.name.find("ttbar")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysTop)
                if sam.name.find("Wjets")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysW)
                if sam.name.find("Zjets")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysZ)
        myFitConfig.setValidationChannels(VRT2)






        
        VRW3 = myFitConfig.addChannel("cuts",["VRW3"],1,0.5,1.5)
        VRW3.addSystematic(pileup)
        VRW3.addSystematic(jes)
        VRW3.addSystematic(jer)
        VRW3.addSystematic(scalest)
        VRW3.addSystematic(resost)
        for sam in VRW3.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll","VRWT_SRAll"))
            if sam.treeName.find("Data")>=0:
                sam.setFileList(dataCRWTFiles)
                pass
            if useTheoSysOnlyInSR:
                if sam.name.find("ttbar")>=0:  
                    if useSyst: sam.addSystematic(theoSysTop)
                if sam.name.find("Wjets")>=0:  
                    if useSyst: sam.addSystematic(mu1ScaleSysW)
                    if useSyst: sam.addSystematic(mu2ScaleSysW)
                    if useSyst: sam.addSystematic(matchScaleSysW)
                    if useSyst: sam.addSystematic(sherpaBugW)
                    if useSyst: sam.addSystematic(nPartonsSysW)
                if sam.name.find("Zjets")>=0:  
                    if useSyst: sam.addSystematic(mu1ScaleSysZ)
                    if useSyst: sam.addSystematic(mu2ScaleSysZ)
                    if useSyst: sam.addSystematic(matchScaleSysZ)
            if useConservativeTheoSys:
                if sam.name.find("ttbar")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysTop)
                if sam.name.find("Wjets")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysW)
                if sam.name.find("Zjets")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysZ)
        myFitConfig.setValidationChannels(VRW3)


        VRT3 = myFitConfig.addChannel("cuts",["VRT3"],1,0.5,1.5)
        VRT3.addSystematic(pileup)
        VRT3.addSystematic(jes)
        VRT3.addSystematic(jer)
        VRT3.addSystematic(scalest)
        VRT3.addSystematic(resost)
        for sam in VRT3.sampleList:
            sam.setTreeName(sam.treeName.replace("SRAll","VRWT_SRAll"))
            if sam.treeName.find("Data")>=0:
                sam.setFileList(dataCRWTFiles)
                pass
            if useTheoSysOnlyInSR:
                if sam.name.find("ttbar")>=0:  
                    if useSyst: sam.addSystematic(theoSysTop)
                if sam.name.find("Wjets")>=0:  
                    if useSyst: sam.addSystematic(mu1ScaleSysW)
                    if useSyst: sam.addSystematic(mu2ScaleSysW)
                    if useSyst: sam.addSystematic(matchScaleSysW)
                    if useSyst: sam.addSystematic(sherpaBugW)
                    if useSyst: sam.addSystematic(nPartonsSysW)
                if sam.name.find("Zjets")>=0:  
                    if useSyst: sam.addSystematic(mu1ScaleSysZ)
                    if useSyst: sam.addSystematic(mu2ScaleSysZ)
                    if useSyst: sam.addSystematic(matchScaleSysZ)
            if useConservativeTheoSys:
                if sam.name.find("ttbar")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysTop)
                if sam.name.find("Wjets")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysW)
                if sam.name.find("Zjets")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysZ)
        myFitConfig.setValidationChannels(VRT3)



        

        if useQCD==True:
            VRQCD2 = myFitConfig.addChannel("cuts",["VRQ2"],1,0.5,1.5)
            myFitConfig.setValidationChannels(VRQCD2)
            VRQCD2.addSample(qcdSample)
            VRQCD2.addWeight("(genWeight<400)")   
            for sam in VRQCD2.sampleList:
                if useSyst: sam.addSystematic(theoSysQCD)
                pass
            if useTheoSysOnlyInSR:
                if sam.name.find("ttbar")>=0:  
                    if useSyst: sam.addSystematic(theoSysTop)
                    if sam.name.find("Wjets")>=0:  
                        if useSyst: sam.addSystematic(mu1ScaleSysW)
                        if useSyst: sam.addSystematic(mu2ScaleSysW)
                        if useSyst: sam.addSystematic(matchScaleSysW)
                        if useSyst: sam.addSystematic(sherpaBugW)
                        if useSyst: sam.addSystematic(nPartonsSysW)
                    if sam.name.find("Zjets")>=0:  
                        if useSyst: sam.addSystematic(mu1ScaleSysZ)
                        if useSyst: sam.addSystematic(mu2ScaleSysZ)
                        if useSyst: sam.addSystematic(matchScaleSysZ)
            if useConservativeTheoSys:
                if sam.name.find("ttbar")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysTop)
                if sam.name.find("Wjets")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysW)
                if sam.name.find("Zjets")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysZ)

            
            VRQCD1 = myFitConfig.addChannel("cuts",["VRQ1"],1,0.5,1.5)
            myFitConfig.setValidationChannels(VRQCD1)
            VRQCD1.addSample(qcdSample)
            VRQCD1.addWeight("(genWeight<400)")   
            for sam in VRQCD1.sampleList:
                if useSyst: sam.addSystematic(theoSysQCD)
                pass
            if useTheoSysOnlyInSR:
                if sam.name.find("ttbar")>=0:  
                    if useSyst: sam.addSystematic(theoSysTop)
                    if sam.name.find("Wjets")>=0:  
                        if useSyst: sam.addSystematic(mu1ScaleSysW)
                        if useSyst: sam.addSystematic(mu2ScaleSysW)
                        if useSyst: sam.addSystematic(matchScaleSysW)
                        if useSyst: sam.addSystematic(sherpaBugW)
                        if useSyst: sam.addSystematic(nPartonsSysW)
                    if sam.name.find("Zjets")>=0:  
                        if useSyst: sam.addSystematic(mu1ScaleSysZ)
                        if useSyst: sam.addSystematic(mu2ScaleSysZ)
                        if useSyst: sam.addSystematic(matchScaleSysZ)
            if useConservativeTheoSys:
                if sam.name.find("ttbar")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysTop)
                if sam.name.find("Wjets")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysW)
                if sam.name.find("Zjets")>=0:  
                    if useSyst: sam.addSystematic(theoConservativeSysZ)

