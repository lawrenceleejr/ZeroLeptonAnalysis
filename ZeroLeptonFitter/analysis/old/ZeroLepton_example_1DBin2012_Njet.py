################################################################
##
## 2012 Njet binned 0-lepton analysis
## Usage: HistFitter.py -p -t -w -d -f -r "1D,SR23456" --exclfit -g "2400_400" analysis/ZeroLepton_example_1DBin2012_Njet.py
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


### Initialize but will be modified later depending on fit setup and SR ###
chn=0                   #analysis channel 0=A,1=B,..
level='loose'           #loose, medium, tight
meff=1400000            # final meff cut
#meff=1000000            # final meff cut
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
useConservativeTheoSys=False # add had-hoc theo sys in SR/VR 
useTheoSys=True            # fit the theo sys

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
            anaName=pickedSRs[0]
            if len(pickedSRs)>=2:
                anaName+=pickedSRs[1]
            print "Analysis defined in a special way!", anaName
            #sys.exit()




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

### For Njet shape fit, define exclusive baseline njet SRs ###
### Default cut values are used except for meffInc. ###
baselineexSR=[ baselineSR[0] +" && !"+baselineSR[1]+" && !"+baselineSR[2] +" && !"+baselineSR[3]+" && !"+baselineSR[4],
               baselineSR[1] +" && !"+baselineSR[2]+" && !"+baselineSR[3] +" && !"+baselineSR[4],
               baselineSR[2] +" && !"+baselineSR[3]+" && !"+baselineSR[4],
               baselineSR[3] +" && !"+baselineSR[4],
               baselineSR[4]
               ]

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


metomeffcut=["(met/meff2Jet>"+str(metomeffDefault[0])+")",
             "(met/meff3Jet>"+str(metomeffDefault[1])+")",
             "(met/meff4Jet>"+str(metomeffDefault[2])+")",
             "(met/meff5Jet>"+str(metomeffDefault[3])+")",
             "(met/meff6Jet>"+str(metomeffDefault[4])+")"]


metomeff_delta=0.1
if metomeff>=0.4:    
    metomeff_delta=0.15
if metomeff<=0.15:    
    metomeff_delta=0.05
if (chn==4 and metomeff>=0.3):#sre,loose
    metomeff_delta=0.15

metomeff_deltaDefault=[0.1,0.1,0.1,0.1,0.05] 

    
metomeffcutqcd=["(met/meff2Jet<"+str(metomeffDefault[0])+")&&(met/meff2Jet>"+str(metomeffDefault[0]-metomeff_deltaDefault[0])+")",
                "(met/meff3Jet<"+str(metomeffDefault[1])+")&&(met/meff3Jet>"+str(metomeffDefault[1]-metomeff_deltaDefault[1])+")",
                "(met/meff4Jet<"+str(metomeffDefault[2])+")&&(met/meff4Jet>"+str(metomeffDefault[2]-metomeff_deltaDefault[2])+")",
                "(met/meff5Jet<"+str(metomeffDefault[3])+")&&(met/meff5Jet>"+str(metomeffDefault[3]-metomeff_deltaDefault[3])+")",
                "(met/meff6Jet<"+str(metomeffDefault[4])+")&&(met/meff6Jet>"+str(metomeffDefault[4]-metomeff_deltaDefault[4])+")"]

### For Njet shape fit ###
# minbinsorg(=original meffcut-200GeV) will be used for meffcuts #
# nbin, minbins and maxbins are defined as the same way as OneBin setup #
nbin=1
minbin=900000 
if pickedSRs[0]=="SRA": minbin=1200000
if pickedSRs[0]=="SRB": minbin=1200000
if pickedSRs[0]=="SRC": minbin=1200000
if pickedSRs[0]=="SRD": minbin=1000000
if pickedSRs[0]=="SRE": minbin=900000
maxbin=800000+minbin ##meff+nbin*100000-300000 

minminusdefault=200000
minbinsorg=[1900000-minminusdefault, 1900000-minminusdefault, 1900000-minminusdefault, 1700000-minminusdefault, 1400000]
minbins=[0.5,0.5,0.5,0.5,0.5]
maxbins=[1.5,1.5,1.5,1.5,1.5]

meffcut="(meffInc>"+str(minbin)+")"

meffcuts=[
    "(meffInc>"+str(minbinsorg[0])+")",
    "(meffInc>"+str(minbinsorg[1])+")",
    "(meffInc>"+str(minbinsorg[2])+")",
    "(meffInc>"+str(minbinsorg[3])+")",
    "(meffInc>"+str(minbinsorg[4])+")"
    ]


bjetveto="(nBJet==0)"
bjetcut ="(nBJet>0)"
photonSelection="(phQuality == 2 && phIso < 5000.)"

# Signal regions
configMgr.cutsDict["SR"]    = baselineSR[chn]+" && "+dphicut[chn]+" && "+metomeffcut[chn]+" && "+meffcut
configMgr.cutsDict["SR6"]   = baselineexSR[4]+" && "+dphicut[4]+" && "+metomeffcut[4]+" && "+meffcuts[4]
configMgr.cutsDict["SR5"]   = baselineexSR[3]+" && "+dphicut[3]+" && "+metomeffcut[3]+" && "+meffcuts[3]
configMgr.cutsDict["SR4"]   = baselineexSR[2]+" && "+dphicut[2]+" && "+metomeffcut[2]+" && "+meffcuts[2]
configMgr.cutsDict["SR3"]   = baselineexSR[1]+" && "+dphicut[1]+" && "+metomeffcut[1]+" && "+meffcuts[1]
configMgr.cutsDict["SR2"]   = baselineexSR[0]+" && "+dphicut[0]+" && "+metomeffcut[0]+" && "+meffcuts[0]

# Control regions
configMgr.cutsDict["CRW"]   = baselineSR[chn]+" && "+meffcut+" && "+bjetveto
configMgr.cutsDict["CRT"] = baselineSR[chn]+" && "+meffcut+" && "+bjetcut
configMgr.cutsDict["CR1a"]  = baselineSR[chn]+" && "+dphicut[chn]+" && "+metomeffcut[chn]+" && "+meffcut+"  &&  "+photonSelection
#configMgr.cutsDict["CRQCD"] = baselineSR[chn]+" && "+invdphicut[chn]+" && "+metomeffcut[chn]+" && "+meffcut
#configMgr.cutsDict["CRQCD"] = baselineSR[chn]+" && "+invdphicut[chn]+" && "+metomeffcutqcd[chn]+" && "+meffcut
configMgr.cutsDict["CRQCD"] = baselineSR[chn]+" && jet1Pt>400000 &&"+invdphicut[chn]+" && "+metomeffcutqcd[chn]+" && "+meffcut

configMgr.cutsDict["CRW2"]   = baselineexSR[0]+" && "+meffcuts[0]+" && "+bjetveto
configMgr.cutsDict["CRT2"]   = baselineexSR[0]+" && "+meffcuts[0]+" && "+bjetcut
configMgr.cutsDict["CR1a2"]  = baselineexSR[0]+" && "+dphicut[0]+" && "+metomeffcut[0]+" && "+meffcuts[0]+"  &&  "+photonSelection
configMgr.cutsDict["CRQCD2"] = baselineexSR[0]+" && jet1Pt>400000 &&"+invdphicut[0]+" && "+metomeffcutqcd[0]+" && "+meffcuts[0]

configMgr.cutsDict["CRW3"]   = baselineexSR[1]+" && "+meffcuts[1]+" && "+bjetveto
configMgr.cutsDict["CRT3"]   = baselineexSR[1]+" && "+meffcuts[1]+" && "+bjetcut
configMgr.cutsDict["CR1a3"]  = baselineexSR[1]+" && "+dphicut[1]+" && "+metomeffcut[1]+" && "+meffcuts[1]+"  &&  "+photonSelection
configMgr.cutsDict["CRQCD3"] = baselineexSR[1]+" && jet1Pt>400000 &&"+invdphicut[1]+" && "+metomeffcutqcd[1]+" && "+meffcuts[1]

configMgr.cutsDict["CRW4"]   = baselineexSR[2]+" && "+meffcuts[2]+" && "+bjetveto
configMgr.cutsDict["CRT4"]   = baselineexSR[2]+" && "+meffcuts[2]+" && "+bjetcut
configMgr.cutsDict["CR1a4"]  = baselineexSR[2]+" && "+dphicut[2]+" && "+metomeffcut[2]+" && "+meffcuts[2]+"  &&  "+photonSelection
configMgr.cutsDict["CRQCD4"] = baselineexSR[2]+" && jet1Pt>400000 &&"+invdphicut[2]+" && "+metomeffcutqcd[2]+" && "+meffcuts[2]

configMgr.cutsDict["CRW5"]   = baselineexSR[3]+" && "+meffcuts[3]+" && "+bjetveto
configMgr.cutsDict["CRT5"]   = baselineexSR[3]+" && "+meffcuts[3]+" && "+bjetcut
configMgr.cutsDict["CR1a5"]  = baselineexSR[3]+" && "+dphicut[3]+" && "+metomeffcut[3]+" && "+meffcuts[3]+"  &&  "+photonSelection
configMgr.cutsDict["CRQCD5"] = baselineexSR[3]+" && jet1Pt>400000 &&"+invdphicut[3]+" && "+metomeffcutqcd[3]+" && "+meffcuts[3]

configMgr.cutsDict["CRW6"]   = baselineexSR[4]+" && "+meffcuts[4]+" && "+bjetveto
configMgr.cutsDict["CRT6"]   = baselineexSR[4]+" && "+meffcuts[4]+" && "+bjetcut
configMgr.cutsDict["CR1a6"]  = baselineexSR[4]+" && "+dphicut[4]+" && "+metomeffcut[4]+" && "+meffcuts[4]+"  &&  "+photonSelection
configMgr.cutsDict["CRQCD6"] = baselineexSR[4]+" && jet1Pt>400000 &&"+invdphicut[4]+" && "+metomeffcutqcd[4]+" && "+meffcuts[4]


# Validation regions
configMgr.cutsDict["VRQ1"] = baselineSR[chn]+" && "+invdphicut[chn]+" &&  "+metomeffcut[chn]+" && "+meffcut
configMgr.cutsDict["VRQ2"] = baselineSR[chn]+" && "+dphicut[chn]+" && "+metomeffcutqcd[chn]+" && "+meffcut
configMgr.cutsDict["VRZ"]   = baselineSR[chn]+" && "+meffcut
configMgr.cutsDict["VRT2L"] = configMgr.cutsDict["VRZ"]+" && mll>116000 &&  lep1Pt<200000 &&  lep2Pt<100000"
configMgr.cutsDict["VRZ_1c"] = configMgr.cutsDict["VRZ"]

configMgr.cutsDict["VRWT_P"]   = baselineSR[chn]+" && "+meffcut+" && "+" lep1sign>0"
configMgr.cutsDict["VRWT_M"]   = baselineSR[chn]+" && "+meffcut+" && "+" lep1sign<0"

configMgr.cutsDict["VRQ12"] = baselineexSR[0]+" && "+invdphicut[0]+" &&  "+metomeffcut[0]+" && "+meffcuts[0]
configMgr.cutsDict["VRQ22"] = baselineexSR[0]+" && "+dphicut[0]+" && "+metomeffcutqcd[0]+" && "+meffcuts[0]
configMgr.cutsDict["VRZ2"]   = baselineexSR[0]+" && "+meffcuts[0]
configMgr.cutsDict["VRT2L2"] = configMgr.cutsDict["VRZ2"]+" && mll>116000 &&  lep1Pt<200000 &&  lep2Pt<100000"
configMgr.cutsDict["VRZ_1c2"] = configMgr.cutsDict["VRZ2"]

configMgr.cutsDict["VRWT_P2"]   = baselineexSR[0]+" && "+meffcuts[0]+" && "+" lep1sign>0"
configMgr.cutsDict["VRWT_M2"]   = baselineexSR[0]+" && "+meffcuts[0]+" && "+" lep1sign<0"

configMgr.cutsDict["VRQ13"] = baselineexSR[1]+" && "+invdphicut[1]+" &&  "+metomeffcut[1]+" && "+meffcuts[1]
configMgr.cutsDict["VRQ23"] = baselineexSR[1]+" && "+dphicut[1]+" && "+metomeffcutqcd[1]+" && "+meffcuts[1]
configMgr.cutsDict["VRZ3"]   = baselineexSR[1]+" && "+meffcuts[1]
configMgr.cutsDict["VRT2L3"] = configMgr.cutsDict["VRZ3"]+" && mll>116000 &&  lep1Pt<200000 &&  lep2Pt<100000"
configMgr.cutsDict["VRZ_1c3"] = configMgr.cutsDict["VRZ3"]

configMgr.cutsDict["VRWT_P3"]   = baselineexSR[1]+" && "+meffcuts[1]+" && "+" lep1sign>0"
configMgr.cutsDict["VRWT_M3"]   = baselineexSR[1]+" && "+meffcuts[1]+" && "+" lep1sign<0"

configMgr.cutsDict["VRQ14"] = baselineexSR[2]+" && "+invdphicut[2]+" &&  "+metomeffcut[2]+" && "+meffcuts[2]
configMgr.cutsDict["VRQ24"] = baselineexSR[2]+" && "+dphicut[2]+" && "+metomeffcutqcd[2]+" && "+meffcuts[2]
configMgr.cutsDict["VRZ4"]   = baselineexSR[2]+" && "+meffcuts[2]
configMgr.cutsDict["VRT2L4"] = configMgr.cutsDict["VRZ4"]+" && mll>116000 &&  lep1Pt<200000 &&  lep2Pt<100000"
configMgr.cutsDict["VRZ_1c4"] = configMgr.cutsDict["VRZ4"]

configMgr.cutsDict["VRWT_P4"]   = baselineexSR[2]+" && "+meffcuts[2]+" && "+" lep1sign>0"
configMgr.cutsDict["VRWT_M4"]   = baselineexSR[2]+" && "+meffcuts[2]+" && "+" lep1sign<0"

configMgr.cutsDict["VRQ15"] = baselineexSR[3]+" && "+invdphicut[3]+" &&  "+metomeffcut[3]+" && "+meffcuts[3]
configMgr.cutsDict["VRQ25"] = baselineexSR[3]+" && "+dphicut[3]+" && "+metomeffcutqcd[3]+" && "+meffcuts[3]
configMgr.cutsDict["VRZ5"]   = baselineexSR[3]+" && "+meffcuts[3]
configMgr.cutsDict["VRT2L5"] = configMgr.cutsDict["VRZ5"]+" && mll>116000 &&  lep1Pt<200000 &&  lep2Pt<100000"
configMgr.cutsDict["VRZ_1c5"] = configMgr.cutsDict["VRZ5"]

configMgr.cutsDict["VRWT_P5"]   = baselineexSR[3]+" && "+meffcuts[3]+" && "+" lep1sign>0"
configMgr.cutsDict["VRWT_M5"]   = baselineexSR[3]+" && "+meffcuts[3]+" && "+" lep1sign<0"

configMgr.cutsDict["VRQ16"] = baselineexSR[4]+" && "+invdphicut[4]+" &&  "+metomeffcut[4]+" && "+meffcuts[4]
configMgr.cutsDict["VRQ26"] = baselineexSR[4]+" && "+dphicut[4]+" && "+metomeffcutqcd[4]+" && "+meffcuts[4]
configMgr.cutsDict["VRZ6"]   = baselineexSR[4]+" && "+meffcuts[4]
configMgr.cutsDict["VRT2L6"] = configMgr.cutsDict["VRZ6"]+" && mll>116000 &&  lep1Pt<200000 &&  lep2Pt<100000"
configMgr.cutsDict["VRZ_1c6"] = configMgr.cutsDict["VRZ6"]

configMgr.cutsDict["VRWT_P6"]   = baselineexSR[4]+" && "+meffcuts[4]+" && "+" lep1sign>0"
configMgr.cutsDict["VRWT_M6"]   = baselineexSR[4]+" && "+meffcuts[4]+" && "+" lep1sign<0"


# Similar to CRW,CRT and VRZ but with dphicut and met/meff cut applied
configMgr.cutsDict["VRZ1"]     = configMgr.cutsDict["VRZ"]+" && "+dphicut[chn]+" && "+metomeffcut[chn]
configMgr.cutsDict["VRW1"]     = configMgr.cutsDict["CRW"]+" && "+dphicut[chn]+" && "+metomeffcut[chn]
configMgr.cutsDict["VRT1"]     = configMgr.cutsDict["CRT"]+" && "+dphicut[chn]+" && "+metomeffcut[chn]

configMgr.cutsDict["VRZ12"]     = configMgr.cutsDict["VRZ2"]+" && "+dphicut[0]+" && "+metomeffcut[0]
configMgr.cutsDict["VRW12"]     = configMgr.cutsDict["CRW2"]+" && "+dphicut[0]+" && "+metomeffcut[0]
configMgr.cutsDict["VRT12"]     = configMgr.cutsDict["CRT2"]+" && "+dphicut[0]+" && "+metomeffcut[0]

configMgr.cutsDict["VRZ13"]     = configMgr.cutsDict["VRZ3"]+" && "+dphicut[1]+" && "+metomeffcut[1]
configMgr.cutsDict["VRW13"]     = configMgr.cutsDict["CRW3"]+" && "+dphicut[1]+" && "+metomeffcut[1]
configMgr.cutsDict["VRT13"]     = configMgr.cutsDict["CRT3"]+" && "+dphicut[1]+" && "+metomeffcut[1]

configMgr.cutsDict["VRZ14"]     = configMgr.cutsDict["VRZ4"]+" && "+dphicut[2]+" && "+metomeffcut[2]
configMgr.cutsDict["VRW14"]     = configMgr.cutsDict["CRW4"]+" && "+dphicut[2]+" && "+metomeffcut[2]
configMgr.cutsDict["VRT14"]     = configMgr.cutsDict["CRT4"]+" && "+dphicut[2]+" && "+metomeffcut[2]

configMgr.cutsDict["VRZ15"]     = configMgr.cutsDict["VRZ5"]+" && "+dphicut[3]+" && "+metomeffcut[3]
configMgr.cutsDict["VRW15"]     = configMgr.cutsDict["CRW5"]+" && "+dphicut[3]+" && "+metomeffcut[3]
configMgr.cutsDict["VRT15"]     = configMgr.cutsDict["CRT5"]+" && "+dphicut[3]+" && "+metomeffcut[3]

configMgr.cutsDict["VRZ16"]     = configMgr.cutsDict["VRZ6"]+" && "+dphicut[4]+" && "+metomeffcut[4]
configMgr.cutsDict["VRW16"]     = configMgr.cutsDict["CRW6"]+" && "+dphicut[4]+" && "+metomeffcut[4]
configMgr.cutsDict["VRT16"]     = configMgr.cutsDict["CRT6"]+" && "+dphicut[4]+" && "+metomeffcut[4]

# Lepton treated as a neutrino
configMgr.cutsDict["VRW2"]     = configMgr.cutsDict["CRW"]
configMgr.cutsDict["VRT2"]     = configMgr.cutsDict["CRT"]

configMgr.cutsDict["VRW22"]     = configMgr.cutsDict["CRW2"]
configMgr.cutsDict["VRT22"]     = configMgr.cutsDict["CRT2"]

configMgr.cutsDict["VRW23"]     = configMgr.cutsDict["CRW3"]
configMgr.cutsDict["VRT23"]     = configMgr.cutsDict["CRT3"]

configMgr.cutsDict["VRW24"]     = configMgr.cutsDict["CRW4"]
configMgr.cutsDict["VRT24"]     = configMgr.cutsDict["CRT4"]

configMgr.cutsDict["VRW25"]     = configMgr.cutsDict["CRW5"]
configMgr.cutsDict["VRT25"]     = configMgr.cutsDict["CRT5"]

configMgr.cutsDict["VRW26"]     = configMgr.cutsDict["CRW6"]
configMgr.cutsDict["VRT26"]     = configMgr.cutsDict["CRT6"]

# Similar to VRW2 and VRT2 but with dphicut and met/meff cut applied
configMgr.cutsDict["VRW3"]     = configMgr.cutsDict["VRW2"]+" && "+dphicut[chn]+" && "+metomeffcut[chn]
configMgr.cutsDict["VRT3"]     = configMgr.cutsDict["VRT2"]+" && "+dphicut[chn]+" && "+metomeffcut[chn]

configMgr.cutsDict["VRW32"]     = configMgr.cutsDict["VRW22"]+" && "+dphicut[0]+" && "+metomeffcut[0]
configMgr.cutsDict["VRT32"]     = configMgr.cutsDict["VRT22"]+" && "+dphicut[0]+" && "+metomeffcut[0]

configMgr.cutsDict["VRW33"]     = configMgr.cutsDict["VRW23"]+" && "+dphicut[1]+" && "+metomeffcut[1]
configMgr.cutsDict["VRT33"]     = configMgr.cutsDict["VRT23"]+" && "+dphicut[1]+" && "+metomeffcut[1]

configMgr.cutsDict["VRW34"]     = configMgr.cutsDict["VRW24"]+" && "+dphicut[2]+" && "+metomeffcut[2]
configMgr.cutsDict["VRT34"]     = configMgr.cutsDict["VRT24"]+" && "+dphicut[2]+" && "+metomeffcut[2]

configMgr.cutsDict["VRW35"]     = configMgr.cutsDict["VRW25"]+" && "+dphicut[3]+" && "+metomeffcut[3]
configMgr.cutsDict["VRT35"]     = configMgr.cutsDict["VRT25"]+" && "+dphicut[3]+" && "+metomeffcut[3]

configMgr.cutsDict["VRW36"]     = configMgr.cutsDict["VRW26"]+" && "+dphicut[4]+" && "+metomeffcut[4]
configMgr.cutsDict["VRT36"]     = configMgr.cutsDict["VRT26"]+" && "+dphicut[4]+" && "+metomeffcut[4]


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
topSample.setNormRegions([("CRT2","cuts"),("CRW2","cuts"),("CRT3","cuts"),("CRW3","cuts"),("CRT4","cuts"),("CRW4","cuts"),("CRT5","cuts"),("CRW5","cuts"),("CRT6","cuts"),("CRW6","cuts")])


qcdSample = Sample("Multijets",kOrange+2)
qcdSample.setTreeName("QCDdd")
qcdSample.setNormFactor("mu_Multijets",1.,0.,500.)
qcdSample.setFileList(qcdFiles)
qcdSample.setStatConfig(useStat)
qcdSample.addWeight("0.000001")#qcd prenormalisation
#qcdSample.addSystematic(QCDGausSys)
#qcdSample.addSystematic(QCDTailSys)
qcdSample.setNormRegions([("CRQCD2","cuts"),("CRQCD3","cuts"),("CRQCD4","cuts"),("CRQCD5","cuts"),("CRQCD6","cuts")])


    
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
wSample.setNormRegions([("CRT2","cuts"),("CRW2","cuts"),("CRT3","cuts"),("CRW3","cuts"),("CRT4","cuts"),("CRW4","cuts"),("CRT5","cuts"),("CRW5","cuts"),("CRT6","cuts"),("CRW6","cuts")])


gammaSample = Sample("GAMMAjets",kYellow)
gammaSample.setTreeName("GAMMA_SRAll")
gammaSample.setNormFactor("mu_Z",1.,0.,500.)
gammaSample.setFileList(gammaFiles)
gammaSample.setStatConfig(useStat)
if useTheoSys:
    if useSyst: gammaSample.addSystematic(mu1ScaleSysZ)
    if useSyst: gammaSample.addSystematic(mu2ScaleSysZ)
    if useSyst: gammaSample.addSystematic(matchScaleSysZ)
gammaSample.setNormRegions([("CR1a2","cuts"),("CR1a3","cuts"),("CR1a4","cuts"),("CR1a5","cuts"),("CR1a6","cuts")])
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
zSample.setNormRegions([("CR1a2","cuts"),("CR1a3","cuts"),("CR1a4","cuts"),("CR1a5","cuts"),("CR1a6","cuts")]) 
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
configMgr.analysisName = "ZLMB2012_"+anaName+"_woCRstatsyst_1DNBin23456"+"_nbin"+str(nbin)+"_"+grid+"_"+allpoints[0]
#configMgr.analysisName = "ZLMB2012_"+anaName+"_meff"+str(minbin)+"-"+str(maxbin)+"_nbin"+str(nbin)+"_"+grid+"_"+allpoints[0]
###configMgr.analysisName = "ZL2012_"+"_"+anaName+"_"+grid+"_"+allpoints[0]
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

    ### For Njet shape fit, make a list of exclusive CR1as to be combined ###
    CR1as=["CR1a2","CR1a3","CR1a4","CR1a5","CR1a6"]
    for (iBin,cr1a) in enumerate(CR1as):
        CRGAMMA = myFitConfig.addChannel("cuts",[cr1a],nbin,minbins[iBin],maxbins[iBin])
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
    
    ### For Njet shape fit, make a list of exclusive SRs to be combined ###
    SRs=["SR2","SR3","SR4","SR5","SR6"]
    for (iBin,sr) in enumerate(SRs):
        print "SR", sr
        SR = myFitConfig.addChannel("cuts",[sr],nbin,minbins[iBin],maxbins[iBin])
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
    if useQCD==True:
        ### For Njet shape fit, make a list of exclusive CRQCDs to be combined ###
        CRQCDs=["CRQCD2","CRQCD3","CRQCD4","CRQCD5","CRQCD6"]
        for (iBin,crqcd) in enumerate(CRQCDs):
            print "CRQCD", crqcd
            CRQCD = myFitConfig.addChannel("cuts",[crqcd],nbin,minbins[iBin],maxbins[iBin])
            CRQCD.useOverflowBin=True 
            CRQCD.useUnderflowBin=False
            if useCR: myFitConfig.setBkgConstrainChannels(CRQCD)
            CRQCD.addSample(qcdSample)
            CRQCD.addWeight("(genWeight<400)")    #reject events with large weights
            for sam in CRQCD.sampleList:
                if sam.name.find("ttbar")>=0 or sam.name.find("W")>=0 or sam.name.find("Z")>=0 or sam.name.find("Diboson")>=0 or sam.name.find(sigSampleName)>=0:
                    #if useSyst: sam.addSystematic(pileup) #ATT: remove due to fit instability
                    if useSyst: sam.addSystematic(jes)
                    if useSyst: sam.addSystematic(jer)
                    if useSyst: sam.addSystematic(scalest)
                    if useSyst: sam.addSystematic(resost)

    ### For Njet shape fit, make a list of exclusive CRTs to be combined ###
    CRTs=["CRT2","CRT3","CRT4","CRT5","CRT6"]
    for (iBin,crt) in enumerate(CRTs):
        CRT = myFitConfig.addChannel("cuts",[crt],nbin,minbins[iBin],maxbins[iBin]) 
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

    ### For Njet shape fit, make a list of exclusive CRWs to be combined ###
    CRWs=["CRW2","CRW3","CRW4", "CRW5","CRW6"]
    for (iBin,crw) in enumerate(CRWs):
        CRW = myFitConfig.addChannel("cuts",[crw],nbin,minbins[iBin],maxbins[iBin]) 
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


    ### For Njet shape fit, make a list of exclusive VRs to be combined ###
    if doValidation:
        if not (len(pickedSRs)>=2 and pickedSRs[1].find("tight")>=0 and pickedSRs[0]=="SRD"): #no stat in SRD,tight
            VRZs=["VRZ2","VRZ3","VRZ4","VRZ5","VRZ6"]
            for (iBin,vrz) in enumerate(VRZs):
                VRZ = myFitConfig.addChannel("cuts",[vrz],nbin,minbins[iBin],maxbins[iBin]) 
                VRZ.useOverflowBin=True 
                VRZ.useUnderflowBin=False 
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
            VRT2Ls=["VRT2L2","VRT2L3","VRT2L4","VRT2L5","VRT2L6"]
            for (iBin,vrt2l) in enumerate(VRT2Ls):
                VRZ_1b = myFitConfig.addChannel("cuts",[vrt2l],nbin,minbins[iBin],maxbins[iBin])
                VRZ_1b.useOverflowBin=True 
                VRZ_1b.useUnderflowBin=False
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

        VRWT_Ps=["VRWT_P2","VRWT_P3","VRWT_P4","VRWT_P5","VRWT_P6"]
        for (iBin,vrwt_p) in enumerate(VRWT_Ps):
            VRWT_P = myFitConfig.addChannel("cuts",[vrwt_p],nbin,minbins[iBin],maxbins[iBin]) 
            VRWT_P.useOverflowBin=True 
            VRWT_P.useUnderflowBin=False
            VRWT_P.addSystematic(pileup)
            VRWT_P.addSystematic(jes)
            VRWT_P.addSystematic(jer)
            VRWT_P.addSystematic(scalest)
            VRWT_P.addSystematic(resost)
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


        VRWT_Ms=["VRWT_M2","VRWT_M3","VRWT_M4","VRWT_M5","VRWT_M6"]
        for (iBin,vrwt_m) in enumerate(VRWT_Ms):
            VRWT_M = myFitConfig.addChannel("cuts",[vrwt_m],nbin,minbins[iBin],maxbins[iBin])
            VRWT_M.useOverflowBin=True
            VRWT_M.useUnderflowBin=False
            VRWT_M.addSystematic(pileup)
            VRWT_M.addSystematic(jes)
            VRWT_M.addSystematic(jer)
            VRWT_M.addSystematic(scalest)
            VRWT_M.addSystematic(resost)
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




        VRW1s=["VRW12","VRW13","VRW14","VRW15","VRW16"]
        for (iBin,vrw1) in enumerate(VRW1s):
            VRW1 = myFitConfig.addChannel("cuts",[vrw1],nbin,minbins[iBin],maxbins[iBin])
            VRW1.useOverflowBin=True
            VRW1.useUnderflowBin=False
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

        VRT1s=["VRT12","VRT13","VRT14","VRT15","VRT16"]
        for (iBin,vrt1) in enumerate(VRT1s):
            VRT1 = myFitConfig.addChannel("cuts",[vrt1],nbin,minbins[iBin],maxbins[iBin])
            VRT1.useOverflowBin=True
            VRT1.useUnderflowBin=False
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



        VRW2s=["VRW22","VRW23","VRW24","VRW25","VRW26"]
        for (iBin,vrw2) in enumerate(VRW2s):
            VRW2 = myFitConfig.addChannel("cuts",[vrw2],nbin,minbins[iBin],maxbins[iBin])
            VRW2.useOverflowBin=True
            VRW2.useUnderflowBin=False
            if useSyst: VRW2.addSystematic(pileup)
            if useSyst: VRW2.addSystematic(jes)
            if useSyst: VRW2.addSystematic(jer)
            if useSyst: VRW2.addSystematic(scalest)
            if useSyst: VRW2.addSystematic(resost)
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


        VRT2s=["VRT22","VRT23","VRT24","VRT25","VRT26"]
        for (iBin,vrt2) in enumerate(VRT2s):
            VRT2 = myFitConfig.addChannel("cuts",[vrt2],nbin,minbins[iBin],maxbins[iBin])
            VRT2.useOverflowBin=True
            VRT2.useUnderflowBin=False
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






        VRW3s=["VRW32","VRW33","VRW34","VRW35","VRW36"]
        for (iBin,vrw3) in enumerate(VRW3s): 
            VRW3 = myFitConfig.addChannel("cuts",[vrw3],nbin,minbins[iBin],maxbins[iBin])
            VRW3.useOverflowBin=True 
            VRW3.useUnderflowBin=False
            if useSyst: VRW3.addSystematic(pileup)
            if useSyst: VRW3.addSystematic(jes)
            if useSyst: VRW3.addSystematic(jer)
            if useSyst: VRW3.addSystematic(scalest)
            if useSyst: VRW3.addSystematic(resost)
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


        VRT3s=["VRT32","VRT33","VRT34","VRT35","VRT36"]
        for (iBin,vrt3) in enumerate(VRT3s):
            VRT3 = myFitConfig.addChannel("cuts",[vrt3],nbin,minbins[iBin],maxbins[iBin])
            VRT3.useOverflowBin=True
            VRT3.useUnderflowBin=False
            if useSyst: VRT3.addSystematic(pileup)
            if useSyst: VRT3.addSystematic(jes)
            if useSyst: VRT3.addSystematic(jer)
            if useSyst: VRT3.addSystematic(scalest)
            if useSyst: VRT3.addSystematic(resost)
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
            VRQCD2s=["VRQ22","VRQ23","VRQ24","VRQ25","VRQ26"]
            for (iBin,vrqcd2) in enumerate(VRQCD2s):
                VRQCD2 = myFitConfig.addChannel("cuts",[vrqcd2],nbin,minbins[iBin],maxbins[iBin])
                VRQCD2.useOverflowBin=True
                VRQCD2.useUnderflowBin=False
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

            VRQ1s=["VRQ12","VRQ13","VRQ14","VRQ15","VRQ16"]
            for (iBin,vrq1) in enumerate(VRQ1s):
                VRQCD1 = myFitConfig.addChannel("cuts",[vrq1],nbin,minbins[iBin],maxbins[iBin])
                VRQCD1.useOverflowBin=True
                VRQCD1.useUnderflowBin=False
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

