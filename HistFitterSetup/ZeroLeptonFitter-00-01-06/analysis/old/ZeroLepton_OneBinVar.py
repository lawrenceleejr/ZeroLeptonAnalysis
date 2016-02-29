################################################################
##
## WORK IN PROGRES!!!!!!!!!!!!!!!!!!!!!!!! 
##
## VERY PRELIMINARY IMPLEMENTATION OF THE 0LEPTON ANALYSIS
## IT WILL BE REWRITTEN MORE ELEGANTLY AND MORE ROBUSTLY
## WHEN ALL ELEMENTS ARE IN PLACE
##
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

#enum type for fits
def enum(typename, field_names):
    "Create a new enumeration type"

    if isinstance(field_names, str):
        field_names = field_names.replace(',', ' ').split()
    d = dict((reversed(nv) for nv in enumerate(field_names)), __slots__ = ())
    return type(typename, (object,), d)()
FITTYPE = enum('FITTYPE','Discovery , Exclusion , Background')


#----------------------------------------------
#
#---------------------------------------------- 



from configManager import configMgr
from ROOT import kBlack,kWhite,kGray,kRed,kPink,kMagenta,kViolet,kBlue,kAzure,kCyan,kTeal,kGreen,kSpring,kYellow,kOrange
from configWriter import TopLevelXML,Measurement,ChannelXML,Sample
from systematic import Systematic
from math import sqrt
import pickle

#from ROOT import gROOT
#gROOT.LoadMacro("./macros/AtlasStyle.C")
#import ROOT
#ROOT.SetAtlasStyle()


#-------------------------------
# Fit parameters
#-------------------------------
#MYFIT=FITTYPE.Discovery
MYFIT=FITTYPE.Exclusion
#MYFIT=FITTYPE.Background


#-------------------------------
# Analysis parameters
#-------------------------------



useStat=True
chn=0                   #analysis channel 0=A,1=Ap,2=B,...
meff=1400000            # final meff cut
grid="msugra"           # only grid implemented up to now
allpoints=["3060_270"]  #msugra points given as M0_M12
anaName="test"          #

#meff cut dictionnary
selections={
      'loose': [ None, None, None, 900000, None, 900000],
      'medium':[1400000,1200000, None,1200000, None,1200000],
      'tight': [1900000, None,1900000,1500000,1500000,1400000]
      }

theoSysWMap={
    'loose': [None, None, None,  8, None, 11],
    'medium':[   8,    7, None, 22, None, 12],
    'tight': [   9, None,   32, 56,   14, 12]
    }

theoSysTopMap={
    'loose': [None, None, None,  8, None, 11],
    'medium':[  57,   17, None, 21, None, 12],
    'tight': [  85, None,   71, 61,   58, 63]
    }

if pickedSRs!=None:  #pickedSRs is set by the "-r" HistFitter option
    allpoints=pickedSRs[2:]
    if pickedSRs[0]=="SRA":chn=0
    if pickedSRs[0]=="SRAp":chn=1
    if pickedSRs[0]=="SRB":chn=2
    if pickedSRs[0]=="SRC":chn=3
    if pickedSRs[0]=="SRD":chn=4
    if pickedSRs[0]=="SRE":chn=5
    meff=selections[pickedSRs[1]][chn]
    theoSysTopNumber=theoSysTopMap[pickedSRs[1]][chn]/100.
    theoSysWNumber=theoSysWMap[pickedSRs[1]][chn]/100.
    anaName=pickedSRs[0]+pickedSRs[1]


#no input signal for discovery and bkg fit
if MYFIT==FITTYPE.Discovery:
    allpoints=["Discovery"]
if MYFIT==FITTYPE.Background:
    allpoints=["Background"]

### Externam cut for SR optimization
useExtCut=False
if len(sys.argv)>1 and sys.argv[len(sys.argv)-1].startswith("meff"):
    meff=sys.argv[len(sys.argv)-1].replace("meff","")
    useExtCut=True
    print meff
    
if meff==None or chn>6 or chn<0:
    print "ERROR analysis not defined!!!"
    print chn,meff
    print pickedSRs
    sys.exit()

#Location of the ntuples
INPUTDIR="root://eosatlas//eos/atlas/user/m/makovec/SuSy/HistFitterNtuples/v1.1/"

#-------------------------------
# Parameters for hypothesis test
#-------------------------------
#configMgr.doHypoTest=False
configMgr.nTOYs=5000      # number of toys when doing frequentist calculator
configMgr.doExclusion=False
if MYFIT==FITTYPE.Exclusion:
    configMgr.doExclusion=True 
    
configMgr.calculatorType=2 # 2=asymptotic calculator, 0=frequentist calculator
configMgr.testStatType=3   # 3=one-sided profile likelihood test statistic (LHC default)
configMgr.nPoints=20       # number of values scanned of signal-strength for upper-limit determination of signal strength.



#-------------------------------------
# Now we start to build the data model
#-------------------------------------

# Scaling calculated by outputLumi / inputLumi
configMgr.inputLumi = 0.001 # Luminosity of input TTree after weighting
configMgr.outputLumi = 4.713 # Luminosity required for output histograms
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
    qcdFiles.append(INPUTDIR+"/QCD.root")
    dibosonFiles.append(INPUTDIR+"/Diboson.root")
    topFiles.append(INPUTDIR+"/Top.root")
    wFiles.append(INPUTDIR+"/W.root")
    zFiles.append(INPUTDIR+"/Z.root")
    gammaFiles.append(INPUTDIR+"/GAMMA.root")
    dataFiles.append(INPUTDIR+"/DataJetTauEtmiss.root")
    dataCRWTFiles.append(INPUTDIR+"/DataEgamma.root")
    dataCRWTFiles.append(INPUTDIR+"/DataMuon.root")
    
 

########################################
# Analysis description
########################################

baselineSR=["(nJet>=2 && jet1Pt>130000 && jet2Pt>60000)",
            "(nJet>=2 && jet1Pt>130000 && jet2Pt>60000)",
            "(nJet>=3 && jet1Pt>130000 && jet2Pt>60000 && jet3Pt>60000)",
            "(nJet>=4 && jet1Pt>130000 && jet2Pt>60000 && jet3Pt>60000 && jet4Pt>60000)",
            "(nJet>=5 && jet1Pt>130000 && jet2Pt>60000 && jet3Pt>60000 && jet4Pt>60000 && jet5Pt>40000)",
            "(nJet>=6 && jet1Pt>130000 && jet2Pt>60000 && jet3Pt>60000 && jet4Pt>60000 && jet5Pt>40000 && jet6Pt>40000)"]

dphicut=["(dPhi>0.4)","(dPhi>0.4)","(dPhi>0.4)",
         "(dPhi>0.4 && dPhiR>0.2)","(dPhi>0.4 && dPhiR>0.2)","(dPhi>0.4 && dPhiR>0.2)"]

invdphicut=["(dPhi<0.2)","(dPhi<0.2)","(dPhi<0.2)",
            "(dPhi<0.2 || dPhiR<0.2)","(dPhi<0.2 || dPhiR<0.2)","(dPhi<0.2 || dPhiR<0.2)"]

metomeffcut=["(met/meff2Jet>0.3)","(met/meff2Jet>0.4)","(met/meff3Jet>0.25)",
             "(met/meff4Jet>0.25)","(met/meff5Jet>0.2)","(met/meff6Jet>0.15)"]

meffcut="(meffInc>"+str(meff)+")"
bjetveto="(nBJet==0)"
bjetcut ="(nBJet>0)"

configMgr.cutsDict["SR"]    = baselineSR[chn]+" && "+dphicut[chn]+" && "+metomeffcut[chn]+" && "+meffcut
configMgr.cutsDict["CRZ"]   = baselineSR[chn]+" && "+meffcut
configMgr.cutsDict["CRW"]   = baselineSR[chn]+" && "+meffcut+" && "+bjetveto
configMgr.cutsDict["CRTop"] = baselineSR[chn]+" && "+meffcut+" && "+bjetcut
configMgr.cutsDict["CRQCD"] = baselineSR[chn]+" && "+invdphicut[chn]+" && "+metomeffcut[chn]+" && "+meffcut
configMgr.cutsDict["CR1a"]  = baselineSR[chn]+" && "+dphicut[chn]+" && "+metomeffcut[chn]+" && "+meffcut

# Tuples of nominal weights
configMgr.weights = ["genWeight","pileupWeight","normWeight"]


#--------------------------------------------------------------------------
# List of systematics
#--------------------------------------------------------------------------
configMgr.nomName = ""


#JES (tree-based)
jes = Systematic("JES","","_JESUP","_JESDOWN","tree","histoSys") #"overallSys")

#JER (tree-based)a
jer = Systematic("JER","","_JER","_JER","tree","histoSysOneSide")

#SCALEST (tree-based)
scalest = Systematic("SCALEST","","_SCALESTUP","_SCALESTDOWN","tree","overallSys")

#RESOST (tree-based)
resost = Systematic("RESOST","","_RESOSTUP","_RESOSTDOWN","tree","overallSys")

#PU
sysWeight_pileupUp=myreplace(configMgr.weights,["pileupWeightUp"],"pileupWeight")
sysWeight_pileupDown=myreplace(configMgr.weights,["pileupWeightDown"],"pileupWeight")
pileup = Systematic("pileup",configMgr.weights,sysWeight_pileupUp,sysWeight_pileupDown,"weight","overallSys")

#b-tag systematics
bTagWeights=configMgr.weights+["bTagWeight"]
bTagSystWeightsUp=myreplace(bTagWeights,["bTagWeightBUp","bTagWeightCUp","bTagWeightLUp"] ,"bTagWeight")
bTagSystWeightsDown=myreplace(bTagWeights,["bTagWeightBDown","bTagWeightCDown","bTagWeightLDown"] ,"bTagWeight")
bTagTop = Systematic("bTag", bTagWeights ,bTagSystWeightsUp,bTagSystWeightsDown,"weight","overallSys")
bTagW = Systematic("bTag",bTagWeights,bTagSystWeightsUp,bTagSystWeightsDown,"weight","overallSys")

#photon systematics
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

#signal
sysWeight_theoSysSigUp=myreplace(configMgr.weights,["normWeightUp"],"normWeight")
sysWeight_theoSysSigDown=myreplace(configMgr.weights,["normWeightDown"],"normWeight")
theoSysSig = Systematic("theoSysSig",configMgr.weights,sysWeight_theoSysSigUp,sysWeight_theoSysSigDown,"weight","overallSys")

#MC theo systematics
theoSysTop = Systematic("theoSysTop", configMgr.weights, 1.+theoSysTopNumber,1.-theoSysTopNumber, "user","userOverallSys")
theoSysW = Systematic("theoSysW", configMgr.weights, 1.0+theoSysWNumber,1.0-theoSysWNumber, "user","userOverallSys")

#diboson
theoSysDiboson = Systematic("theoSysDiboson", configMgr.weights, 1.5,0.5, "user","userOverallSys")

#photon systematics in SR for Z
gammaToZSyst = Systematic("gammaToZSyst", configMgr.weights, 1.25,0.75, "user","userOverallSys")



#-------------------------------------------
# List of samples and their plotting colours
#-------------------------------------------
dibosonSample = Sample("Diboson",kRed+3)
dibosonSample.setTreeName("Diboson_SRAll")
dibosonSample.setFileList(dibosonFiles)
dibosonSample.setStatConfig(useStat)
dibosonSample.addSystematic(theoSysDiboson)

topSample = Sample("Top",kGreen-9)
topSample.setTreeName("Top_SRAll")
topSample.setNormFactor("mu_Top",1.,0.,500.)
topSample.setFileList(topFiles)
topSample.setStatConfig(useStat)

qcdSample = Sample("MCMultijet",kOrange+2)
qcdSample.setTreeName("QCD_SRAll")
qcdSample.setNormFactor("mu_MCMultijet",1.,0.,500.)
qcdSample.setFileList(qcdFiles)
qcdSample.setStatConfig(useStat)

wSample = Sample("W",kAzure+1)
wSample.setTreeName("W_SRAll")
wSample.setNormFactor("mu_W",1.,0.,500.)
wSample.setFileList(wFiles)
wSample.setStatConfig(useStat)

zSample = Sample("Z",kBlue)
zSample.setTreeName("Z_SRAll")
zSample.setNormFactor("mu_Z",1.,0.,500.)
zSample.setFileList(zFiles)
zSample.setStatConfig(useStat)

gammaSample = Sample("GAMMA",kYellow)
gammaSample.setTreeName("GAMMA_SRAll")
gammaSample.setNormFactor("mu_Z",1.,0.,500.)
gammaSample.setFileList(gammaFiles)
gammaSample.setStatConfig(useStat)

dataSample = Sample("Data",kBlack)
dataSample.setTreeName("Data_SRAll")
dataSample.setData()
dataSample.setFileList(dataFiles)


#**************
# Exclusion fit
#**************

# First define HistFactory attributes
configMgr.analysisName = "ZeroLepton"+"_"+anaName+"_"+grid+"_"+allpoints[0] #ATT
#configMgr.analysisName = "ZeroLepton"+"_"+anaName+"_"+grid
configMgr.histCacheFile = "data/"+configMgr.analysisName+".root"
configMgr.outputFileName = "results/"+configMgr.analysisName+"_Output.root"


for point in allpoints:
    if point=="":continue
    
    #Fit config instance
    name="Fit_"+"_"+point
    myFitConfig = configMgr.addTopLevelXML(name)
    if useStat:
        myFitConfig.statErrThreshold=0.05 
    else:
        myFitConfig.statErrThreshold=None
        
    meas=myFitConfig.addMeasurement(name="NormalMeasurement",lumi=1.0,lumiErr=0.039)
    meas.addPOI("mu_SIG")
    meas.addParamSetting("mu_Diboson",True,1) # fix diboson to MC prediction

    #Samples
    myFitConfig.addSamples([gammaSample,topSample,wSample,zSample,qcdSample,dibosonSample,dataSample])
    #myFitConfig.addSamples([topSample,wSample,zSample,qcdSample,dibosonSample,dataSample])

    #-------------------------------------------------
    # signal
    #-------------------------------------------------
    if MYFIT==FITTYPE.Exclusion:
        sigSample = Sample("msugra_"+point,kRed)
        sigSample.setFileList([INPUTDIR+grid+".root"])
        sigSample.setTreeName("msugra_"+point+"_SRAll")
        sigSample.setNormByTheory()
        sigSample.setNormFactor("mu_SIG",1,0.,100.)
        sigSample.addSystematic(theoSysSig)
        sigSample.setStatConfig(useStat)
        myFitConfig.addSamples(sigSample)
        myFitConfig.setSignalSample(sigSample)

    # Systematics    
    myFitConfig.addSystematic(pileup)
    myFitConfig.addSystematic(jes)
    myFitConfig.addSystematic(jer)
    myFitConfig.addSystematic(scalest)
    myFitConfig.addSystematic(resost)

    #Channel
    if MYFIT!=FITTYPE.Background:
        SR = myFitConfig.addChannel("cuts",["SR"],1,0.5,1.5)
        myFitConfig.setSignalChannels([SR])
        for sam in SR.sampleList:
            if sam.name.find("Z")>=0:                       
                sam.addSystematic(gammaToZSyst)
                pass
            if sam.name.find("W")>=0:                       
                sam.addSystematic(theoSysW)
                pass
            if sam.name.find("Top")>=0:                       
                sam.addSystematic(theoSysTop)
                pass
            
        if MYFIT==FITTYPE.Discovery:
            SR.addDiscoverySamples(["SIG"],[1.],[0.],[100.],[kMagenta])

    #-------------------------------------------------
    # Constraining regions - statistically independent
    #-------------------------------------------------

    CRQCD = myFitConfig.addChannel("cuts",["CRQCD"],1,0.5,1.5)
    for sam in CRQCD.sampleList:
        sam.setTreeName(sam.treeName.replace("SRAll","CRQCD"))
        pass
    myFitConfig.setBkgConstrainChannels(CRQCD)


    CRTop = myFitConfig.addChannel("cuts",["CRTop"],1,0.5,1.5)
    CRTop.addWeight("bTagWeight")    
    for sam in CRTop.sampleList:
        sam.setTreeName(sam.treeName.replace("SRAll","CRWT"))
        if sam.name.find("Top")>=0:                       
            sam.addSystematic(bTagTop)
            pass
        if sam.name.find("W")>=0:                       
            sam.addSystematic(bTagW)
            pass            
        if sam.treeName.find("Data")>=0:
            sam.setFileList(dataCRWTFiles)
            pass
        pass
    myFitConfig.setBkgConstrainChannels(CRTop)

    CRW = myFitConfig.addChannel("cuts",["CRW"],1,0.5,1.5)
    CRW.addWeight("bTagWeight")   
    for sam in CRW.sampleList:
        sam.setTreeName(sam.treeName.replace("SRAll","CRWT"))
        if sam.name.find("Top")>=0:                       
            sam.addSystematic(bTagTop)
            pass
        if sam.name.find("W")>=0:                       
            sam.addSystematic(bTagW)
            pass    
        if sam.treeName.find("Data")>=0:
            sam.setFileList(dataCRWTFiles)
        pass
    myFitConfig.setBkgConstrainChannels(CRW)

    CRZ = myFitConfig.addChannel("cuts",["CRZ"],1,0.5,1.5)
    for sam in CRZ.sampleList:
        sam.setTreeName(sam.treeName.replace("SRAll","CRZ"))
        if sam.treeName.find("Data")>=0:
            sam.setFileList(dataCRWTFiles)
        pass
    myFitConfig.setBkgConstrainChannels(CRZ)


    CRGAMMA = myFitConfig.addChannel("cuts",["CR1a"],1,0.5,1.5)
    for sam in CRGAMMA.sampleList:
        sam.setTreeName(sam.treeName.replace("SRAll","CR1a"))
        if sam.name.find("GAMMA")>=0:
            sam.addWeight("photonWeight")
            sam.addWeight("triggerWeight") 
            sam.addSystematic(photonSys)
            sam.addSystematic(triggerSys)
            pass           
        if sam.treeName.find("Data")>=0:
            sam.setFileList(dataCRWTFiles)
        pass
    #CRGAMMA.addSample(gammaSample) #UGLY!!!!!!!!!!!!!!!!!!!!
    myFitConfig.setBkgConstrainChannels(CRGAMMA)

