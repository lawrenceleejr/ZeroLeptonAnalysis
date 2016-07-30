#export ZEROLEPTONFITTER=$PWD

import sys, os, string, shutil,pickle,subprocess, time, socket, argparse

from multiprocessing import Pool,Process,Lock,Queue
import ROOT
from ROOT import *
file_path = os.path.abspath("plot")
sys.path.append(file_path)
from PlotterUtils import *

file_path = os.path.abspath("python")
sys.path.append(file_path)
from ChannelConfig import *
from ChannelsDict import *

def parseCmdLine(args):
#Here you put the regions that you want to plot

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--region", default="SR", type = str)
    parser.add_option("--doCompressed", default=False, action = "store_true")
    parser.add_option("--baseDir", default =  os.getcwd() , help="location of samples to run")
    parser.add_option("--inputSampleDir", default =  "/Users/khoo/Work/ATLAS/", help="location of samples to run")
    parser.add_option("--version", default = 111, help="ntuple version", type = int)
    parser.add_option("--SignalOnTop", action = "store_true", dest="SignalOnTop", help=" Add signal to SM background in SR plots", default=False)
    parser.add_option("--doSyst", action = "store_true", dest="doSyst", help="Run without systematics",default=False)
    parser.add_option("--inputDataFile", default = None , help = "Use an alternative data file (full path).  Will look in --inputSampleDir if not specified")
    parser.add_option("--regionsToRun", default = "" , help =  "Which regions to run.  Uses check if option is a substring of each item in the list.  For example, passing --regionsToRun SRS, while --regionsToRun SRC1 will only run SRC1")
    parser.add_option("--varToRun", default = "" , help =  "Which var to run.")
    parser.add_option("--lumi", dest="lumi", help="lumi", default=13.28, type=float)
    parser.add_option("--integral", dest="int", help="integrals", default=False, action = "store_true")
    parser.add_option("--vrebin", dest="vbins", help="variable binning", default=False, action = "store_true")
    (config, args) = parser.parse_args(args)

    print config
    return config
config = parseCmdLine(sys.argv[1:])

allRegionsList = []
if config.doCompressed:
    allRegionsList += ["SRJigsawSRC1","SRJigsawSRC2","SRJigsawSRC3","SRJigsawSRC4","SRJigsawSRC5"]
else:
    allRegionsList += ["SRJigsawSRG1a","SRJigsawSRG2a","SRJigsawSRG3a",
                       "SRJigsawSRG1b","SRJigsawSRG2b","SRJigsawSRG3b"]
    allRegionsList += ["SRJigsawSRS1a","SRJigsawSRS2a","SRJigsawSRS3a",
                       "SRJigsawSRS1b","SRJigsawSRS2b","SRJigsawSRS3b"]


versionname = '{0}_baseline'.format(config.version)

basedir = config.baseDir + "/"
outplotdir = basedir+"Outplots/v"+str(versionname)+"/"

if not os.path.isdir(outplotdir): os.makedirs(outplotdir)
if 'nikhef' in socket.getfqdn():
    datadir = mcdir = mcaltdir = mcsignaldir = "ZeroLeptonFitter/data/atlas/users/ideigaar/ZeroLeptonRun2/NtuplesWSysForPlotting_160204/"
else:
    sampledir = config.inputSampleDir
    mcdir = sampledir
    datadir = sampledir
    mcsignaldir = sampledir
    mcaltdir = sampledir

anaImInterestedIn = [ana for ana in allRegionsList if (config.regionsToRun in ana)]
print anaImInterestedIn

runData=True
doBlinding = False
doBlindingMC = False
DrawOverflow = True
runSignal=True
SignalOnTop=False
doCRWT=False
doVRWT=False
doCRW=False
doCRT=False
doCRY=False
doVRZ=False
doVRZc=False
doCRQ=False
doSyst=False
doSignificance=False
doAlternativeZ=False
doAlternativeW=False
doAlternativeTopHerwig=False
doAlternativeTopPythia=False
doAlternativeTopMcAtNlo=False

#scale for Yjets
kappaYjets = 1.334

def comparator(x, y):
    if doCRT:
        if "Top" in x: return -1
    elif doCRW:
        if "Wjets" in x: return -1
    elif doVRZ or doVRZc:
        if "Zjets" in x: return -1
    elif doCRY:
        if "Yjets" in x: return -1
    elif doCRQ:
        if "Q" in x: return -1
    return 0



if config.SignalOnTop:
    SignalOnTop = True

if config.doSyst:
    doSyst=True

if config.region=="SR":
    doCRT = doCRW = doCRWT = doVRWT = doCRY = doVRZ = doVRZc = doCRQ = False
    print "Running region: ",config.region
elif config.region=="CRWT":
    doCRWT = True
    print "Running region: ",config.region
elif config.region=="CRT":
    doCRT = True
    print "Running region: ",config.region
elif config.region=="CRW":
    doCRW = True
    print "Running region: ",config.region
elif config.region=="VRWT":
    doVRWT = True
    print "Running region: ",config.region
elif config.region=="CRY":
    doCRY = True
    print "Running region: ",config.region
elif config.region=="VRZ":
    doVRZ = True
    print "Running region: ",config.region
elif config.region=="VRZc":
    doVRZc = True
    print "Running region: ",config.region
elif config.region=="CRQ":
    doCRQ = True
    print "Running region: ",config.region
else:
    print "Region: ",config.region," not defined, running SR"


if doSignificance:
    runSignal=True

if doAlternativeZ:
    doCRWT=doCRY=doCRQ=False
    doVRZ=True
    doVRZc=True

if doAlternativeW or doAlternativeTopHerwig or doAlternativeTopPythia or doAlternativeTopMcAtNlo:
    doVRZ=doVRZc=doCRY=doCRQ=False
    doCRWT=True

if doCRW or doCRT:
    doCRWT=True

if doCRWT or doVRWT or doCRY or doVRZ or doVRZc or doCRQ:
    runSignal=False

if not runSignal:
    SignalOnTop=False

saveToFile=False

if doAlternativeZ and doVRZ:
    versionname = versionname.replace('baseline','alternativeZ')
elif doAlternativeW and doCRWT:
    versionname = versionname.replace('baseline','alternativeW')
elif doAlternativeTopHerwig and doCRWT:
    versionname = versionname.replace('baseline','alternativeTopHerwig')
elif doAlternativeTopPythia and doCRWT:
    versionname = versionname.replace('baseline','alternativeTopPythia')
elif doAlternativeTopMcAtNlo and doCRWT:
    versionname = versionname.replace('baseline','alternativeTopMcAtNlo')

doRun2=True

gStyle=ROOT.gStyle
rootOpt=RootOption(gStyle)
rootOpt.setUpStyle()
gROOT.SetBatch(kTRUE)

lastcutsfull = {
    'SRG': "H_{T 4,1}^{PP}",
    'SRS': "H_{T 2,1}^{PP}",
    'SRC': "p_{T S}^{CM}"
}

ratiocutsfull = {
    'SRG': "H_{1,1}^{PP} / H_{4,1}^{PP}",
    'SRS': "H_{1,1}^{PP} / H_{2,1}^{PP}",
    'SRC': "R_{ISR}"
}

varList = [
           {'varName':'LastCut','varNtuple':'LastCut','plotName':'LastCut [GeV]','nbinvar':'27','minvar':'800','maxvar':'3500.','unit':'GeV'},
           {'varName':'Ratio','varNtuple':'Ratio','plotName':'Ratio','nbinvar':'30','minvar':'0','maxvar':'1.2','unit':''},
           {'varName':'deltaQCD','varNtuple':'deltaQCD','plotName':'#Delta_{QCD}','nbinvar':'60','minvar':'-1.2','maxvar':'1.2','unit':''},
           {'varName':'H2PP','varNtuple':'H2PP','plotName':'H_{1,1}^{PP} [GeV]','nbinvar':'50','minvar':'0','maxvar':'5000.','unit':'GeV'},
           #
           {'varName':'RPZ_HT3PP','varNtuple':'RPZ_HT3PP','plotName':'p_{PP,z}^{lab} / (p_{PP,z}^{lab} + H_{T 2,1}^ {PP})','nbinvar':'60','minvar':'0','maxvar':'1.2','unit':''},
           {'varName':'RPZ_HT5PP','varNtuple':'RPZ_HT5PP','plotName':'p_{PP,z}^{lab} / (p_{PP,z}^{lab} + H_{T 4,1}^ {PP})','nbinvar':'60','minvar':'0','maxvar':'1.2','unit':''},
           {'varName':'R_pTj2_HT3PP','varNtuple':'R_pTj2_HT3PP','plotName':'p^{PP}_{j2 T} / H_{T 2,1 i}^{PP}','nbinvar':'60','minvar':'0','maxvar':'1.2','unit':''},
           {'varName':'minR_pTj2i_HT3PPi','varNtuple':'minR_pTj2i_HT3PPi','plotName':'min(p_{T}^{j2 T i}/H_{T 2,1}^{PP,i})','nbinvar':'60','minvar':'0','maxvar':'1.2','unit':''},
           {'varName':'maxR_H1PPi_H2PPi','varNtuple':'maxR_H1PPi_H2PPi','plotName':'min(H_{1, 0}^{Pi}/H_{2,0}^{Pi})','nbinvar':'60','minvar':'0','maxvar':'1.2','unit':''},
           {'varName':'dangle','varNtuple':'dangle','plotName':'|#frac{2}{3}#Delta#phi^{PP}_{V,P} - #frac{1}{3}cos#theta_{P}|','nbinvar':'60','minvar':'-1.2','maxvar':'1.2','unit':''},
           {'varName':'sangle','varNtuple':'sangle','plotName':'sangle','nbinvar':'60','minvar':'-1.2','maxvar':'1.2','unit':''},
           #
           {'varName':'dphiISRI','varNtuple':'dphiISRI','plotName':'#Delta#phi(ISR, I)','nbinvar':'30','minvar':'2','maxvar':'3.5','unit':''},
           {'varName':'dphiMin2','varNtuple':'dphiMin2','plotName':'min(#Delta#phi_{MET,j1}, #Delta#phi_{MET,j2})','nbinvar':'40','minvar':'0','maxvar':'4.0','unit':''},
           {'varName':'MS','varNtuple':'MS','plotName':'M_{T S} [GeV]','nbinvar':'30','minvar':'0','maxvar':'1500.','unit':'GeV'},
           {'varName':'NV','varNtuple':'NV', 'plotName': 'N_{jet}^{V}', 'nbinvar':'10','minvar':'0','maxvar':'10','unit':''},
           #
           {'varName':'meffincl','varNtuple':'Meff','plotName':'m_{eff}(incl.) [GeV]','nbinvar':'50','minvar':'0','maxvar':'5000.','unit':'GeV'},
           {'varName':'met','varNtuple':'MET','plotName':'E_{T}^{miss} [GeV]','nbinvar':'50','minvar':'0','maxvar':'2500.','unit':'GeV'},
           {'varName':'metSig','varNtuple':'MET/sqrt(Meff-MET)','plotName':'E_{T}^{miss}/#sqrt{H_{T}} [GeV]^{1/2}','nbinvar':'25','minvar':'0','maxvar':'50','unit':'(GeV)^{1/2}'},
           {'varName':'metomeff','varNtuple':'MET/Meff','plotName':'E_{T}^{miss}/m_{eff}(incl.)','nbinvar':'24','minvar':'0','maxvar':'1.2','unit':''},
           {'varName':'metomeff2jet','varNtuple':'MET/(MET+pT_jet1+pT_jet2)','plotName':'E_{T}^{miss}/m_{eff}(N_{jets})','nbinvar':'24','minvar':'0','maxvar':'1.2','unit':''},
           {'varName':'metomeff3jet','varNtuple':'MET/(MET+pT_jet1+pT_jet2+pT_jet3)','plotName':'E_{T}^{miss}/m_{eff}(N_{jets})','nbinvar':'24','minvar':'0','maxvar':'1.2','unit':''},
           {'varName':'metomeff4jet','varNtuple':'MET/(MET+pT_jet1+pT_jet2+pT_jet3+pT_jet4)','plotName':'E_{T}^{miss}/m_{eff}(N_{jets})','nbinvar':'24','minvar':'0','maxvar':'1.2','unit':''},
           {'varName':'metomeff5jet','varNtuple':'MET/(MET+pT_jet1+pT_jet2+pT_jet3+pT_jet4+pT_jet5)','plotName':'E_{T}^{miss}/m_{eff}(N_{jets})','nbinvar':'24','minvar':'0','maxvar':'1.2','unit':''},
           {'varName':'metomeff6jet','varNtuple':'MET/(MET+pT_jet1+pT_jet2+pT_jet3+pT_jet4+pT_jet5+pT_jet6)','plotName':'E_{T}^{miss}/m_{eff}(N_{jets})','nbinvar':'24','minvar':'0','maxvar':'1.2','unit':''},
           {'varName':'meff2jet','varNtuple':'MET+pT_jet1+pT_jet2','plotName':'m_{eff}(2j) [GeV]','nbinvar':'50','minvar':'0','maxvar':'5000.','unit':'GeV'},
           {'varName':'dphi','varNtuple':'dphi','plotName':'min(#Delta#phi(E_{T}^{miss},jet_{1,2,3}))','nbinvar':'40','minvar':'0','maxvar':'4.0','unit':''},
           {'varName':'nJets','varNtuple':'NJet', 'plotName': 'N_{jets} (p_{T}>50 GeV, |#eta|<2.8)', 'nbinvar':'15','minvar':'0','maxvar':'15','unit':''},
           {'varName':'nJets60all','varNtuple':'NJet', 'plotName': 'N_{jets} (all jets with p_{T}>50 GeV, |#eta|<2.8)', 'nbinvar':'15','minvar':'0','maxvar':'15','unit':'', 'extracuts':'(jetPt[nJet-1]>60.)'},
           {'varName':'nbJets','varNtuple':'nBJet', 'plotName': 'N_{bjets} (p_{T}>50 GeV, |#eta|<2.5)', 'nbinvar':'15','minvar':'0','maxvar':'15','unit':''},
           {'varName':'jetpT1','varNtuple':'pT_jet1', 'plotName': 'p_{T}(jet_{1}) [GeV]', 'nbinvar':'40','minvar':'0','maxvar':'2000','unit':'GeV'},
           {'varName':'jetpT2','varNtuple':'pT_jet2', 'plotName': 'p_{T}(jet_{2}) [GeV]', 'nbinvar':'40','minvar':'0','maxvar':'2000','unit':'GeV'},
           {'varName':'jetpT3','varNtuple':'pT_jet3', 'plotName': 'p_{T}(jet_{3}) [GeV]', 'nbinvar':'40','minvar':'0','maxvar':'1000','unit':'GeV'},
           {'varName':'jetpT4','varNtuple':'pT_jet4', 'plotName': 'p_{T}(jet_{4}) [GeV]', 'nbinvar':'40','minvar':'0','maxvar':'1000','unit':'GeV'},
           {'varName':'jetpT5','varNtuple':'pT_jet5', 'plotName': 'p_{T}(jet_{5}) [GeV]', 'nbinvar':'20','minvar':'0','maxvar':'500','unit':'GeV'},
           {'varName':'jetpT6','varNtuple':'pT_jet6', 'plotName': 'p_{T}(jet_{6}) [GeV]', 'nbinvar':'20','minvar':'0','maxvar':'500','unit':'GeV'},
           {'varName':'mDR','varNtuple':'MDR', 'plotName':'m^{#Delta}_{R} [GeV]', 'nbinvar':'50','minvar':'0','maxvar':'5000.','unit':'GeV'},
           {'varName':'lep1Pt', 'varNtuple':'lep1Pt', 'plotName': 'p_{T}(lep_{1}) [GeV]', 'nbinvar':'25','minvar':'0','maxvar':'1000','unit':'GeV'},
           {'varName':'lep1Eta', 'varNtuple':'lep1Eta', 'plotName': '#eta(lep_{1})', 'nbinvar':'40','minvar':'-4','maxvar':'4','unit':''},
           {'varName':'lep1Phi', 'varNtuple':'lep1Phi', 'plotName': '#phi(lep_{1})', 'nbinvar':'40','minvar':'-4','maxvar':'4','unit':''},
           {'varName':'lep1sign', 'varNtuple':'lep1sign', 'plotName': 'sign(lep_{1})', 'nbinvar':'5','minvar':'-2','maxvar':'3','unit':''},
           {'varName':'lep2Pt', 'varNtuple':'lep2Pt', 'plotName': 'p_{T}(lep_{1}) [GeV]', 'nbinvar':'50','minvar':'0','maxvar':'1000','unit':'GeV'},
           {'varName':'lep2Eta', 'varNtuple':'lep2Eta', 'plotName': '#eta(lep_{2})', 'nbinvar':'40','minvar':'-4','maxvar':'4','unit':''},
           {'varName':'lep2Phi', 'varNtuple':'lep2Phi', 'plotName': '#phi(lep_{2})', 'nbinvar':'40','minvar':'-4','maxvar':'4','unit':''},
           {'varName':'lep2sign', 'varNtuple':'lep2sign', 'plotName': 'sign(lep_{2})', 'nbinvar':'5','minvar':'-2','maxvar':'3','unit':''},
           {'varName':'llsign', 'varNtuple':'lep1sign*lep2sign', 'plotName': 'sign(lep_{1})#timessign(lep_{2})', 'nbinvar':'5','minvar':'-2','maxvar':'3','unit':''},
           {'varName':'mt', 'varNtuple':'mt', 'plotName':'m_{T} [GeV]', 'nbinvar':'50','minvar':'20','maxvar':'120.','unit':'GeV'},
           {'varName':'Wpt', 'varNtuple':'Wpt', 'plotName':'p_{T}(W) [GeV]', 'nbinvar':'25','minvar':'0','maxvar':'1500.','unit':'GeV'},
           {'varName':'mll', 'varNtuple':'mll', 'plotName':'m_{ll} [GeV]', 'nbinvar':'50','minvar':'40','maxvar':'140.','unit':'GeV'},
           {'varName':'Zpt', 'varNtuple':'Zpt', 'plotName':'p_{T}(Z) [GeV]', 'nbinvar':'50','minvar':'0','maxvar':'2000.','unit':'GeV'},
           {'varName':'mettrack','varNtuple':'mettrack','plotName':'E_{T}^{miss,track} [GeV]','nbinvar':'60','minvar':'0','maxvar':'3000.','unit':'GeV'},
           {'varName':'mettrack_phi', 'varNtuple':'mettrack_phi', 'plotName': '#phi(E_{T}^{miss,track})', 'nbinvar':'40','minvar':'-4','maxvar':'4','unit':''},
           {'varName':'phPt', 'varNtuple':'phPt', 'plotName': 'p_{T}(#gamma) [GeV]', 'nbinvar':'50','minvar':'0','maxvar':'2000','unit':'GeV'},
           {'varName':'phEta', 'varNtuple':'phEta', 'plotName': '#eta(#gamma)', 'nbinvar':'20','minvar':'-4','maxvar':'4','unit':''},
           {'varName':'phPhi', 'varNtuple':'phPhi', 'plotName': '#phi(#gamma)', 'nbinvar':'20','minvar':'-4','maxvar':'4','unit':''},
           {'varName':'phSignal', 'varNtuple':'phSignal', 'plotName': 'is_#gammaSignal', 'nbinvar':'6','minvar':'-1','maxvar':'5','unit':''},  ## always 1
           {'varName':'phTopoetcone20', 'varNtuple':'phTopoetcone20[0]/1000.', 'plotName': 'phTopoetcone20', 'nbinvar':'50','minvar':'0','maxvar':'50','unit':''},  ## always 1
           {'varName':'origmet','varNtuple':'origmet','plotName':'E_{T}^{miss,orig} [GeV]','nbinvar':'40','minvar':'0','maxvar':'2000.','unit':'GeV'},
           {'varName':'origmetPhi', 'varNtuple':'origmetPhi', 'plotName': '#phi(E_{T}^{miss,orig})', 'nbinvar':'40','minvar':'-1','maxvar':'7','unit':''},
           ]

from array import array
varbin_lastcut = [0,100,200,300,400,500,600,700,800,900,1000,1100,1200,1400,1600,1800,2000,2500,3000,3500,4000,4500,5000]
varbin_rescale = [1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,.5,.5,.5,.5,.5,.2,.2,.2,.2,.2]
Nvarbin_lastcut = len(varbin_lastcut)-1

if config.doCompressed:
    varList[0]['nbinvar'] = '9'
    varList[0]['minvar'] = '200.'
    varList[0]['maxvar'] = '2000.'
    varbin_lastcut = varbin_lastcut[:-5]
    varbin_rescale = varbin_rescale[:-5]
    Nvarbin_lastcut = len(varbin_lastcut)-1

datafile = 'DataMain.root'
fullDataPath = config.inputDataFile if config.inputDataFile else (datadir + datafile)

datafile =[
           {'whichdata':['SR','VRZc','VRZca'],
            'filename':fullDataPath,
            'dataname':'Data_SRAll'},
           {'whichdata':['CRWT','CRW','CRT','CRWa','CRWb','CRT','CRTa','CRTb'],
            'filename':fullDataPath,
            'dataname':'Data_CRWT'},
           {'whichdata':['VRW','VRWa','VRWb','VRT','VRTa','VRTb'],
            'filename':fullDataPath,
            'dataname':'Data_VRWT'},
           {'whichdata':['CRY'],
            'filename':fullDataPath,
            'dataname':'Data_CRY'},
           {'whichdata':['VRZ','VRZa','VRZb','VRTZl'],
            'filename':fullDataPath,
            'dataname':'Data_CRZ'},
           {'whichdata':['CRQ','VRQ','VRQa','VRQb','VRQc'],
            'filename':fullDataPath,
            'dataname':'Data_SRAll'},
           ]

commonsyst=" "

kindOfCuts=[]

plotlists = {
    "Common":   [["LastCut","meffincl","mDR"],
                 ["met"],
                 ["Ratio"],
                 ["deltaQCD"],
                 ],
    "SRS":      [["RPZ_HT3PP"],
                 ["R_pTj2_HT3PP"],
                 ["H2PP"],
                 ],
    "SRG":      [
                 ["RPZ_HT5PP"],
                 ["H2PP"],
                 ["R_HT5PP_H5PP"],
                 ["minR_pTj2i_HT3PPi"],
                 ["maxR_H1PPi_H2PPi"],
                 ["dangle"],
                 #                 ["sangle"]
                 ],
    "SRC":      [
                 ["MS"],
                 ["dphiISRI"],
                 ["dphiMin2"],
                 ["NV"],
                 ],
    "CRWT":     [["nbJets"]]
    }

plotlist = {srtype:plotlists["Common"]+plotlists[srtype] for srtype in ["SRS","SRG","SRC"]}
if config.region in ["CRW","CRT","CRWT"]:
    {srtype:plotlists["Common"]+plotlists[srtype]+plotlists["CRWT"] for srtype in ["SRS","SRG","SRC"]}
#plotlist = {srtype:plotlists["Common"] for srtype in ["SRS","SRG","SRC"]}
#plotlist = {srtype:plotlists["CRWT"] for srtype in ["SRS","SRG","SRC"]}
#plotlist = {srtype:plotlists[srtype] for srtype in ["SRS","SRG","SRC"]}
#plotlist = {srtype:plotlists["SRS"] for srtype in ["SRS","SRG","SRC"]}

kindOfCuts_SR =     [ {"type":"SR_minusone",    "var": plotlist, "name":"SR"} ]
kindOfCuts_CRWT =   [ {"type":"CRW_minusone",   "var": plotlist, "name":"CRW"},
                      {"type":"CRT_minusone",   "var": plotlist, "name":"CRT"} ]
kindOfCuts_VRWT =   [ {"type":"VRW_minusone",   "var": plotlist, "name":"VRW"},
                      {"type":"VRT_minusone",   "var": plotlist, "name":"VRT"},
                      {"type":"VRWa_minusone",  "var": plotlist, "name":"VRWa"},
                      {"type":"VRTa_minusone",  "var": plotlist, "name":"VRTa"},
                      {"type":"VRWb_minusone",  "var": plotlist, "name":"VRWb"},
                      {"type":"VRTb_minusone",  "var": plotlist, "name":"VRTb"}]
kindOfCuts_CRY =    [ {"type":"CRY_minusone",   "var": plotlist, "name":"CR#gamma"} ]
kindOfCuts_VRZ =    [ {"type":"VRZ_minusone",   "var": plotlist, "name":"VRZ"},
                      {"type":"VRZa_minusone",  "var": plotlist, "name":"VRZa"},
                      {"type":"VRZb_minusone",  "var": plotlist, "name":"VRZb"} ]
kindOfCuts_VRZc =   [ {"type":"VRZc_minusone",  "var": plotlist, "name":"VRZc"},
                      {"type":"VRZca_minusone", "var": plotlist, "name":"VRZca"}]
kindOfCuts_CRQ =    [ {"type":"CRQ_minusone",   "var": plotlist, "name":"CRQ"} ]

if doCRY:
    kindOfCuts=kindOfCuts_CRY
elif doCRWT:
    kindOfCuts=kindOfCuts_CRWT
elif doVRWT:
    kindOfCuts=kindOfCuts_VRWT
elif doVRZ:
    kindOfCuts=kindOfCuts_VRZ
elif doVRZc:
    kindOfCuts=kindOfCuts_VRZc
elif doCRQ:
    kindOfCuts=kindOfCuts_CRQ
else:
    kindOfCuts=kindOfCuts_SR


print kindOfCuts

ZName = 'ZMassiveCB'
WName = 'WMassiveCB'
TopName = 'Top'

if doSyst:
    ZName = 'ZMassiveCB'
    WName = 'WMassiveCB'

if doAlternativeZ and (doVRZ or doVRZc):
    ZName = 'ZMadgraphPythia8'
    print "Running alternative Z sample!"
if doAlternativeW and doCRWT:
    WName = 'WMadgraphPythia8'
    print "Running alternative W sample!"
if doAlternativeTopHerwig and doCRWT:
    TopName = 'TopPowhegHerwigpp'
    print "Running alternative TopPowhegHerwigpp sample!"
if doAlternativeTopPythia and doCRWT:
    TopName = 'TopPowhegPythia8'
    print "Running alternative TopPowhegPythia8 sample!"
if doAlternativeTopMcAtNlo and doCRWT:
    TopName = 'TopMCatNLO.root'
    print "Running alternative TopMcAtNloHerwigpp sample!"

mufacts = {}
import pickle
for sr in allRegionsList:
    mufacts[sr] = {}
    fpkl = open("plot/muvalues/MU_{0}.pkl".format(sr))
    for mu in pickle.load(fpkl):
        mufacts[sr][mu[0]] = mu[1]
    mufacts[sr]['Diboson'] = 1.
    mufacts[sr]['QCDMC'] = 1.

mc = [
      {'key':'Diboson','name':'Diboson','ds':'lDiboson','redoNormWeight':'redoNormWeight',
      'color':ROOT.kPink-4,'inputdir':mcdir+'DibosonMassiveCB.root','treePrefix':'Diboson_',
      'syst':commonsyst},
      {'key':'Zjets','name':'Z+jets','ds':'lZjets','redoNormWeight':'redoNormWeight',
      'color':ROOT.kOrange-4,'inputdir':mcdir+ZName+'.root','veto':1,'treePrefix':'Z_',
      'syst':commonsyst},
      {'key':'Top','name':'t#bar{t}(+EW) & single top','ds':'lTop','redoNormWeight':'redoNormWeight',
      'color':ROOT.kGreen-9,'inputdir':mcdir+TopName+'.root',
      'treePrefix':'Top_','syst':commonsyst},
      {'key':'Wjets','name':'W+jets','ds':'lWjets','redoNormWeight':'redoNormWeight',
      'color':ROOT.kAzure-4,'inputdir':mcdir+WName+'.root','veto':1,'treePrefix':'W_',
      'syst':commonsyst},
      ]

if doCRY:
    mc.append({'key':'Yjets','name':'#gamma+jets','ds':'lYjets','redoNormWeight':'redoNormWeight',
              'color':ROOT.kYellow,'inputdir':mcdir+'GAMMAMassiveCB.root','veto':1,'treePrefix':'GAMMA_',
              'syst':commonsyst},
              )
if not doVRZ:
    if config.region=='SR' or config.region=='CRQ' or config.region=='VRZc':
        mc.append({'key':'QCDJS','name':'Multi-jet','ds':'lQCDJS','redoNormWeight':'redoNormWeight',
                  'color':ROOT.kBlue+3,'inputdir':mcdir+'JetSmearing_2015.root','treePrefix':'Data_',
                  'syst':commonsyst})
    else:
        mc.append({'key':'QCDMC','name':'Multi-jet','ds':'lQCDMC','redoNormWeight':'redoNormWeight',
                  'color':ROOT.kBlue+3,'inputdir':mcdir+'QCD.root','treePrefix':'QCD_',
                  'syst':commonsyst})

#To make sure that the dominant background is on top
mc = sorted(mc, cmp=comparator, key=lambda k: k['key'], reverse=True)

print mc

mc_alternative = [
#                  {'key':'Zjets_alternative','name':'Z+jets','ds':'lZjets','redoNormWeight':'redoNormWeight',
#                  'color':ROOT.kBlue+3,'inputdir':mcaltdir+'ZMadgraphPythia8.root','veto':1,'treePrefix':'Z_','treeSuffix':'_Madgraph',
#                  'syst':commonsyst},
                  # Hack to implement flat systematic
                  {'key':'Zjets_alternative_systup','name':'Z+jets','ds':'lZjets','redoNormWeight':'redoNormWeight',
                  'color':ROOT.kOrange-4,'inputdir':mcdir+ZName+'.root','veto':1,'treePrefix':'Z_',
                  'syst':commonsyst},
                  {'key':'Zjets_alternative_systdn','name':'Z+jets','ds':'lZjets','redoNormWeight':'redoNormWeight',
                  'color':ROOT.kOrange-4,'inputdir':mcdir+ZName+'.root','veto':1,'treePrefix':'Z_',
                  'syst':commonsyst},
                  # Hack to implement flat systematic
                  {'key':'Diboson_alternative_systup','name':'Diboson','ds':'lDiboson','redoNormWeight':'redoNormWeight',
                  'color':ROOT.kPink-4,'inputdir':mcdir+'DibosonMassiveCB.root','treePrefix':'Diboson_',
                  'syst':commonsyst},
                  {'key':'Diboson_alternative_systdn','name':'Diboson','ds':'lDiboson','redoNormWeight':'redoNormWeight',
                  'color':ROOT.kPink-4,'inputdir':mcdir+'DibosonMassiveCB.root','treePrefix':'Diboson_',
                  'syst':commonsyst},
                  # Cover all top systs
                  {'key':'Top_alternativeMCatNLO','name':'t#bar{t}(+X) & single top','ds':'lTop','redoNormWeight':'redoNormWeight',
                  'color':ROOT.kGreen-9,'inputdir':mcaltdir+'TopMCatNLO.root',
                  'treePrefix':'Top_','treeSuffix':'_aMcAtNloHerwigpp','syst':commonsyst},
                 {'key':'Wjets_alternative','name':'W+jets','ds':'lWjets','redoNormWeight':'redoNormWeight',
                  'color':ROOT.kAzure-4,'inputdir':mcaltdir+'WMadgraphPythia8.root','veto':1,'treePrefix':'W_','treeSuffix':'_Madgraph',
                  'syst':commonsyst},
                  ]
if config.version>107:
	mc_alternative += [
	                  {'key':'Top_alternativePy8','name':'t#bar{t}(+X) & single top','ds':'lTop','redoNormWeight':'redoNormWeight',
	                  'color':ROOT.kGreen-9,'inputdir':mcaltdir+'TopPowhegPythia8.root',
	                  'treePrefix':'Top_','treeSuffix':'_PowhegPythia8','syst':commonsyst},
	                  {'key':'Top_alternativeHpp','name':'t#bar{t}(+X) & single top','ds':'lTop','redoNormWeight':'redoNormWeight',
	                  'color':ROOT.kGreen-9,'inputdir':mcaltdir+'TopPowhegHerwig.root',
	                  'treePrefix':'Top_','treeSuffix':'_PowhegHerwigpp','syst':commonsyst},
	                  {'key':'Top_alternativeRadHi','name':'t#bar{t}(+X) & single top','ds':'lTop','redoNormWeight':'redoNormWeight',
	                  'color':ROOT.kGreen-9,'inputdir':mcaltdir+'TopRadHi.root',
	                  'treePrefix':'Top_','treeSuffix':'_RadHi','syst':commonsyst},
	                  {'key':'Top_alternativeRadLo','name':'t#bar{t}(+X) & single top','ds':'lTop','redoNormWeight':'redoNormWeight',
	                  'color':ROOT.kGreen-9,'inputdir':mcaltdir+'TopRadLo.root',
	                  'treePrefix':'Top_','treeSuffix':'_RadLo','syst':commonsyst},
	                   ]

if not doVRZ:
    if config.region=='SR' or config.region=='CRQ' or config.region=='VRZc':
        mc_alternative.append({'key':'QCDJS_alternative_systup','name':'Multi-jet','ds':'lQCDJS','redoNormWeight':'redoNormWeight',
                  'color':ROOT.kBlue+3,'inputdir':mcdir+'JetSmearing_2015.root','treePrefix':'Data_',
                  'syst':commonsyst})
        mc_alternative.append({'key':'QCDJS_alternative_systdn','name':'Multi-jet','ds':'lQCDJS','redoNormWeight':'redoNormWeight',
                  'color':ROOT.kBlue+3,'inputdir':mcdir+'JetSmearing_2015.root','treePrefix':'Data_',
                  'syst':commonsyst})
    else:
        mc_alternative.append({'key':'QCDMC_alternative_systup','name':'Multi-jet','ds':'lQCDMC','redoNormWeight':'redoNormWeight',
                              'color':ROOT.kBlue+3,'inputdir':mcdir+'QCD.root','treePrefix':'QCD_',
                              'syst':commonsyst})
        mc_alternative.append({'key':'QCDMC_alternative_systdn','name':'Multi-jet','ds':'lQCDMC','redoNormWeight':'redoNormWeight',
                              'color':ROOT.kBlue+3,'inputdir':mcdir+'QCD.root','treePrefix':'QCD_',
                              'syst':commonsyst})

mc_truth = [
            {'key':'Yjets_TRUTH','name':'#gamma+jets','ds':'lYjets','redoNormWeight':'redoNormWeight',
            'color':ROOT.kYellow,'inputdir':mcdir+'GAMMAMassiveCB_TRUTH.root','veto':1,'treePrefix':'GAMMA_','treeSuffix':'','syst':commonsyst},
            {'key':'Yjets_TRUTH_alternative','name':'#gamma+jets','ds':'lYjets','redoNormWeight':'redoNormWeight',
            'color':ROOT.kYellow,'inputdir':mcdir+'GAMMAMadgraph_TRUTH.root','veto':1,'treePrefix':'GAMMA_','treeSuffix':'_TRUTH_Madgraph','syst':commonsyst}
            ]

signalPoint=[
             {'name':'SS_direct_1300_0','filename':mcsignaldir+'SS_direct.root',
             'color':ROOT.kBlue,
             'linestyle': ROOT.kDashed,
             'sigplotname':'#tilde{q}#tilde{q} direct,',
             'masspoint':'m(#tilde{q}, #tilde{#chi_{1}^{0}})=(1300, 0)',
             'sigSR':['SRJigsawSRS1a','SRJigsawSRS2a','SRJigsawSRS3a',
                      'SRJigsawSRS1b','SRJigsawSRS2b','SRJigsawSRS3b'],
             },
             {'name':'SS_direct_1100_500','filename':mcsignaldir+'SS_direct.root',
             'color':ROOT.kViolet-1,
             'linestyle': ROOT.kDashDotted,
             'sigplotname':'#tilde{q}#tilde{q} direct,',
             'masspoint':'m(#tilde{q}, #tilde{#chi_{1}^{0}})=(1100, 500)',
             'sigSR':['SRJigsawSRS1a','SRJigsawSRS2a','SRJigsawSRS3a',
                      'SRJigsawSRS1b','SRJigsawSRS2b','SRJigsawSRS3b'],
             },
#             {'name':'SS_direct_800_500','filename':mcsignaldir+'SS_direct.root',
#             'color':ROOT.kViolet-1,
#             'linestyle': ROOT.kDotted,
#             'sigplotname':'#tilde{q}#tilde{q} direct,',
#             'masspoint':'m(#tilde{q}, #tilde{#chi_{1}^{0}})=(800, 500)',
#             'sigSR':['SRJigsawSRS1a','SRJigsawSRS2a','SRJigsawSRS3a',
#                      'SRJigsawSRS1b','SRJigsawSRS2b','SRJigsawSRS3b'],
#             },
             {'name':'GG_direct_1800_0','filename':mcsignaldir+'GG_direct.root',
             'color':ROOT.kBlue,
             'linestyle': ROOT.kDotted,
             'sigplotname':'#tilde{g}#tilde{g} direct,',
             'masspoint':'m(#tilde{g}, #tilde{#chi_{1}^{0}})=(1800, 0)',
             'sigSR':['SRJigsawSRG1a','SRJigsawSRG2a','SRJigsawSRG3a',
                      'SRJigsawSRG1b','SRJigsawSRG2b','SRJigsawSRG3b'],
             },
             {'name':'GG_direct_1500_700','filename':mcsignaldir+'GG_direct.root',
             'color':ROOT.kViolet-1,
             'linestyle': ROOT.kDashDotted,
             'sigplotname':'#tilde{g}#tilde{g} direct,',
             'masspoint':'m(#tilde{g}, #tilde{#chi_{1}^{0}})=(1500, 700)',
             'sigSR':['SRJigsawSRG1a','SRJigsawSRG2a','SRJigsawSRG3a',
                      'SRJigsawSRG1b','SRJigsawSRG2b','SRJigsawSRG3b'],
             },
             {'name':'GG_direct_825_775','filename':mcsignaldir+'GG_direct.root',
             'color':ROOT.kGray+2,
             'linestyle': ROOT.kDashed,
             'sigplotname':'#tilde{g}#tilde{g} direct,',
             'masspoint':'m(#tilde{g}, #tilde{#chi_{1}^{0}})=(825, 775)',
             'sigSR':['SRJigsawSRG1a','SRJigsawSRG2a','SRJigsawSRG3a',
                      'SRJigsawSRG1b','SRJigsawSRG2b','SRJigsawSRG3b',
                      'SRJigsawSRC1','SRJigsawSRC2','SRJigsawSRC3','SRJigsawSRC4','SRJigsawSRC5'],
             },
             {'name':'SS_direct_700_600','filename':mcsignaldir+'SS_direct.root',
             'color':ROOT.kGreen+2,
             'linestyle': ROOT.kDotted,
             'sigplotname':'#tilde{q}#tilde{q} direct,',
             'masspoint':'m(#tilde{q}, #tilde{#chi_{1}^{0}})=(700, 600)',
             'sigSR':['SRJigsawSRS1a','SRJigsawSRS2a','SRJigsawSRS3a',
                      'SRJigsawSRS1b','SRJigsawSRS2b','SRJigsawSRS3b',
                      'SRJigsawSRC1','SRJigsawSRC2','SRJigsawSRC3','SRJigsawSRC4','SRJigsawSRC5'],
             },
#             {'name':'GG_onestepCC_1265_945_625','filename':mcsignaldir+'GG_onestepCC.root',
#             'color':ROOT.kViolet,
#             'linestyle': 7,
#             'sigplotname':'#tilde{g}#tilde{g} onestep,',
#             'masspoint':'m(#tilde{g}, #tilde{#chi_{1}^{#pm}}, #tilde{#chi_{1}^{0}})=(1265, 945, 625)',
#             'sigSR':['SRJigsawSRG1a'],
#             },
#             {'name':'GG_onestepCC_1385_705_25','filename':mcsignaldir+'GG_onestepCC.root',
#             'color':ROOT.kViolet,
#             'linestyle': 7,
#             'sigplotname':'#tilde{g}#tilde{g} onestep,',
#             'masspoint':'m(#tilde{g}, #tilde{#chi_{1}^{#pm}}, #tilde{#chi_{1}^{0}})=(1385, 705, 25)',
#             'sigSR':['SRJigsawSRG3a'],
#             },
             #{'name':'GG_direct_1350_0','filename':mcdir+'GG_direct.root',
             # 'color':ROOT.kMagenta,
             # 'linestyle': 7,
             # 'sigplotname':'#tilde{g}#tilde{g} direct, m(#tilde{g}, #tilde{#chi^{1}_{0}})=(1350, 0)',
             # 'sigSR':['SR5jMoriond','SR4jAp','SR2jvt'],
             #},
             #{'name':'GG_direct_1050_600','filename':mcdir+'GG_direct.root',
             # 'color':ROOT.kOrange+7,
             # 'linestyle': 3,
             # 'sigplotname':'#tilde{g}#tilde{g} direct, m(#tilde{g}, #tilde{#chi^{1}_{0}})=(1050, 600)',
             # 'sigSR':['SR5jMoriond','SR4jAp','SR2jvt'],
             # },
             #{'name':'SS_direct_900_0','filename':mcdir+'SS_direct.root',
             # 'color':ROOT.kMagenta,
             # 'linestyle': 7,
             # 'sigplotname':'#tilde{q}#tilde{q} direct, m(#tilde{q}, #tilde{#chi^{1}_{0}})=(900, 0)',
             # 'sigSR':['SR2jMoriond'],#,'SR2jvt'], v34
             # },
             #{'name':'SS_direct_700_400','filename':mcdir+'SS_direct.root',
             # 'color':ROOT.kOrange+7,
             # 'linestyle': 3,
             # 'sigplotname':'#tilde{q}#tilde{q} direct, m(#tilde{q}, #tilde{#chi^{1}_{0}})=(700, 400)',
             # 'sigSR':['SR2jMoriond'],#,'SR2jvt'], v34
             # },
    ]


start_time = time.time()

if doSyst:
    if doRun2 and config.version>30:
        systDict=[
                  "_JET_GroupedNP_1_1down",
                  "_JET_GroupedNP_2_1down",
                  "_JET_GroupedNP_3_1down",

                  "_JET_GroupedNP_1_1up",
                  "_JET_GroupedNP_2_1up",
                  "_JET_GroupedNP_3_1up",
                  "_JET_JER_SINGLE_NP_1up",

                  "_MET_SoftTrk_ResoPara",
                  "_MET_SoftTrk_ResoPerp",
                  "_MET_SoftTrk_ScaleDown",
                  "_MET_SoftTrk_ScaleUp",

                  #"_EG_SCALE_ALL_1down",
                  #"_EG_RESOLUTION_ALL_1down",
                  #"_JET_BJES_Response_1down",
                  #"_JET_EffectiveNP_1_1down",
                  #"_JET_EffectiveNP_2_1down",
                  #"_JET_EffectiveNP_3_1down",
                  #"_JET_EffectiveNP_4_1down",
                  #"_JET_EffectiveNP_5_1down",
                  #"_JET_EffectiveNP_6restTerm_1down",
                  #"_JET_EtaIntercalibration_Modelling_1down",
                  #"_JET_EtaIntercalibration_TotalStat_1down",
                  #"_JET_Flavor_Composition_1down",
                  #"_JET_Flavor_Response_1down",
                  #"_JET_Pileup_OffsetMu_1down",
                  #"_JET_Pileup_OffsetNPV_1down",
                  #"_JET_Pileup_PtTerm_1down",
                  #"_JET_Pileup_RhoTopology_1down",
                  #"_JET_PunchThrough_MC12_1down",
                  #"_JET_SingleParticle_HighPt_1down",
                  #"_MET_SoftTrk_ScaleDown",
                  #"_MUONS_ID_1down",
                  #"_MUONS_MS_1down",
                  #"_MUONS_SCALE_1down",
                  #"_TAUS_SME_TOTAL_1down",

                  #"_EG_SCALE_ALL_1up",
                  #"_EG_RESOLUTION_ALL_1up",
                  #"_JET_BJES_Response_1up",
                  #"_JET_EffectiveNP_1_1up",
                  #"_JET_EffectiveNP_2_1up",
                  #"_JET_EffectiveNP_3_1up",
                  #"_JET_EffectiveNP_4_1up",
                  #"_JET_EffectiveNP_5_1up",
                  #"_JET_EffectiveNP_6restTerm_1up",
                  #"_JET_EtaIntercalibration_Modelling_1up",
                  #"_JET_EtaIntercalibration_TotalStat_1up",
                  #"_JET_Flavor_Composition_1up",
                  #"_JET_Flavor_Response_1up",
                  #"_JET_JER_SINGLE_NP_1up",
                  #"_JET_Pileup_OffsetMu_1up",
                  #"_JET_Pileup_OffsetNPV_1up",
                  #"_JET_Pileup_PtTerm_1up",
                  #"_JET_Pileup_RhoTopology_1up",
                  #"_JET_PunchThrough_MC12_1up",
                  #"_JET_SingleParticle_HighPt_1up",
                  #"_MET_SoftTrk_ScaleUp",
                  #"_MUONS_ID_1up",
                  #"_MUONS_MS_1up",
                  #"_MUONS_SCALE_1up",
                  #"_TAUS_SME_TOTAL_1up",

                  #"_MET_SoftTrk_ResoPara",
                  #"_MET_SoftTrk_ResoPerp",

                  #"_JET_GroupedNP_1_1up",
                  #"_JET_GroupedNP_2_1up",
                  #"_JET_GroupedNP_3_1up",
                  #"_JET_GroupedNP_1_1down",
                  #"_JET_GroupedNP_2_1down",
                  #"_JET_GroupedNP_3_1down",
                  #"_JER_1up",
                  ]
else:
    systDict=[]

def projAll(l,var,varname,title,cuts,syst,myNtHandler,nbinvar,minvar,maxvar,output):
    print '------------------------- projAll',title,varname,nbinvar,minvar,maxvar
    myHisto=ROOT.TH1F(title,varname,nbinvar,minvar,maxvar)
    myHisto.SetFillColor(myNtHandler.color)
    myNtHandler.project(l,title,var,cuts)
    output.put(myHisto)

def parallelProcessProj(processList,l,var,varname,ana,region,cuts,syst,handlername,nbinvar,minvar,maxvar):
    if len(processList)==0: return []

    hists = []
    # avoid hitting limits on number of open files
    chunksize=5
    chunks = [processList[x:x+chunksize] for x in xrange(0, len(processList), chunksize)]
    for chunk in chunks:
        print "CHUNK", len(chunk)
        thesehists = []
        jobs = []
        output=Queue()

        label = syst
        for ip,process in enumerate(chunk):
            suffix = syst
            if "mcTreeSuffix" in process.keys(): suffix = process["mcTreeSuffix"]
            if syst=="Syst":
                suffix = process["ntsyst"]
                label = process["ntsyst"]
            title = varname+process['mctreePrefix']+ana+region+suffix
            pargs = (l,var,varname,title,cuts,label,process[handlername],nbinvar,minvar,maxvar,output)
            p=Process(target=projAll,args=pargs)
            jobs.append(p)
            print 'START',p, title
            p.result_queue = output
            p.start()
            #time.sleep(0.2)
        working=True
        while working:
            thesehists.append(output.get())
            if len(thesehists)==len(jobs): working=False
        for j in jobs:
            j.terminate()
        DeleteList(jobs)
        output.close()
        output.join_thread()
        hists += thesehists
    return hists

class NtHandler:
    def __init__(self,name,filename,treename,basecuts,color,weights,dataormc,lumi):
        self.data=dataormc
        self.color=color
        self.weights=weights
        self.lumi=str(lumi)
        if type(filename) is list:
            self.tfile = ROOT.TChain(treename)
            for f in filename:
                self.tfile.Add(f)
            self.tree = self.tfile
        else:
            self.tfile = ROOT.TFile.Open(filename)
            if not self.tfile:
                print "no tfile:",filename
                sys.exit(1)
            self.tree = self.tfile.Get(treename)
            if not self.tree:
                print "no tree:",treename
                sys.exit(1)
        print name, treename, basecuts, self.tree.GetEntries()
        #print
        self.tree.Draw('>>entryList'+name,basecuts,'entrylist')
        elist = ROOT.gDirectory.Get('entryList'+name)
        print elist, name
        self.tree.SetEntryList(elist)
        #print 'done,',name," ",elist.GetN(),' entries'
        return
    def printAll(self):
        print 'printall from nthandler',self.lumi,self.tree.GetName()
        return
    def project(self,l,histname,var,cuts):
        weight=str(self.weights)+"*"+str(self.lumi)
        if self.data=="data":  weight="1"
        #print 'histname',self.data,histname,"weight",weight,"var",var,cuts,self.tree.GetEntries(cuts)
        self.tree.Project(histname,var,"("+cuts+")*("+weight+")")
        print 'time Project',time.time()-start_time,histname

def DeleteNtList(ntList):
    for ntDict in ntList:
        ntDict.clear()
        del ntDict
    del ntList

def DeleteList(List):
    for entry in List:
        del entry
    del List


def DrawErrorsOutsidePad(ratiohist):
    Lines = []
    xaxis = ratiohist.GetXaxis();
    for i in range (1,xaxis.GetNbins()+1):
        xP=ROOT.Double(0)
        yP=ROOT.Double(0)
        ratiohist.GetPoint(i,xP,yP)

        if (yP>2.):
            print xP, yP-ratiohist.GetErrorYlow(i)
            lin = TLine(xP,yP-ratiohist.GetErrorYlow(i),xP,2.)
            lin.SetLineWidth(3)
            lin.SetLineColor(kBlack)
            Lines.append(lin)
    return Lines

def main(configMain):
    #print configMain
    TH1.SetDefaultSumw2()
    for whichKind in kindOfCuts:
        allChannel = finalChannelsDict
        allAna = allChannel.keys()

        allRegion = regionDict.keys()
        onlyExtraWeights=False

        for ana in allAna:
            if ana in anaImInterestedIn or len(anaImInterestedIn)==0:

                region = whichKind['type'].split('_',1)[0]
                print ana,region,whichKind
                chnameshort = allChannel[ana].name.split('Jigsaw')[1][:3]
                for varset in whichKind["var"][chnameshort]:
                    print 'going to run', whichKind['type']
                    ch=copy.deepcopy(allChannel[ana]) # so as to not permanently disable cuts

                    minusvar = varset[0]
                    minusvarname = minusvar
                    for vardict in varList:
                        if vardict["varName"]==minusvar:
                            minusvarname = vardict["varNtuple"]
                    if("minusone" in whichKind['type']):
                        if minusvar == "LastCut": minusvar = minusvarname = lastcuts[chnameshort]
                        elif minusvar == "Ratio": minusvar = minusvarname = ratiocuts[chnameshort]
                        if hasattr(ch,minusvar):
                            if minusvar in ch.regionListDict[region].keys() and "invert" in ch.regionListDict[region][minusvar]:
                                ch.regionListDict[region][minusvar] = "minusone_invert"
                            else:
                                ch.regionListDict[region][minusvar] = "minusone"
                        if hasattr(ch,minusvar+"_upper"):
                            if minusvar+"_upper" in ch.regionListDict[region].keys() and "invert" in ch.regionListDict[region][minusvar+"_upper"]:
                                ch.regionListDict[region][minusvar+"_upper"] = "minusone_invert"
                            else:
                                ch.regionListDict[region][minusvar+"_upper"] = "minusone"
                        if minusvar+"_loose" in ch.regionListDict[region].keys() and hasattr(ch,minusvar+"_loose"):
                            if minusvar+"_loose" in ch.regionListDict[region].keys() and "invert" in ch.regionListDict[region][minusvar+"_loose"]:
                                ch.regionListDict[region][minusvar+"_loose"] = "minusone_invert"
                            else:
                                ch.regionListDict[region][minusvar+"_loose"] = "minusone_loose"
                        if hasattr(ch,minusvar+"_upper_loose"):
                            if minusvar+"_upper_loose" in ch.regionListDict[region].keys() and "invert" in ch.regionListDict[region][minusvar+"_upper_loose"]:
                                ch.regionListDict[region][minusvar+"_upper_loose"] = "minusone_invert_loose"
                            else:
                                ch.regionListDict[region][minusvar+"_upper_loose"] = "minusone_loose"
                    print "MINUS", minusvar, minusvarname

                    cuts=ch.getCuts(region)
                    truthcuts = cuts

#                    truthcuts = truthcuts.replace("((cleaning&0x30F)==0) && ", " ")
#                    truthcuts = truthcuts.replace(" && (phTopoetcone40==0||phSignal&0x01) && (phTopoetcone40-(phPt*0.022)<2.45)", " ")
#                    truthcuts = truthcuts.replace("&& !(phPt>800 && weight>1 && RunNumber==361040)", "")
                    #print "channel",cuts, truthcuts
                    print "channel",cuts

                    weights=allChannel[ana].getWeights(region,onlyExtraWeights)
                    truthweights = weights.replace("WZweight","1.")

                    print ana, region, cuts,weights
                    blindcut = ""
                    if hasattr(ch,minusvar) and not getattr(ch,minusvar)==None:
                        blindcutlow = getattr(ch,minusvar)
                        blindcut += minusvarname+" < "+str(blindcutlow)
                    if hasattr(ch,minusvar+"_upper") and not getattr(ch,minusvar+"_upper")==None:
                        if len(blindcut)>0:  blindcut += " || "
                        blindcuthigh = getattr(ch,minusvar+"_upper")
                        blindcut += minusvarname+" > "+str(blindcuthigh)
                    if len(blindcut)>0:
                        blindcut = " && ("+blindcut+")"
                    print "BLINDCUT", minusvar, minusvarname, blindcut
                    if runData:
                        plotData=[]
                        for wData in datafile:
                            print region, wData['whichdata']
                            if (region in wData['whichdata']):
                                print 'nthandler data',wData['whichdata']
                                if doBlinding and "SR" in region:
                                    print "Data is blinded beyond SR cut"
                                    nt=NtHandler(ana+region+"data_baseline",wData['filename'],wData['dataname'],cuts+blindcut,ROOT.kBlack,1.,"data",configMain.lumi)
                                else:
                                    nt=NtHandler(ana+region+"data_baseline",wData['filename'],wData['dataname'],cuts,ROOT.kBlack,1.,"data",configMain.lumi)
                                plotData.append(nt)
                    if runSignal:
                        print "SIGNAL!"
                        plotSignalList=[]
                        for point in signalPoint:
                            for sigSR in point['sigSR']:
                                if (sigSR==ana) or (sigSR=='all'):
                                    tmptreename="_"+ch.getSuffixTreeName(region)
                                    ntsig=NtHandler(ana+region+point['name']+tmptreename,point['filename'],point['name']+tmptreename,cuts,point['color'],weights,"signal",configMain.lumi)
                                    plotSignalList.append({'pointname':point['name'],'pointcolor':point['color'],'pointlinestyle':point['linestyle'],'pointsigplotname':point['sigplotname'],'pointmass':point['masspoint'],'nthandle':ntsig})
                                    print 'signal point',point['name']
                        print "SIGNAL", plotSignalList

                    fullPlotMC=[]
                    fullPlotMCSyst=[]
                    fullPlotMCAlt=[]
                    fullPlotMCTruth=[]
                    fullPlotMCTruthAlt=[]

                    for process in mc:
                        print process
                        mcname=process['treePrefix']+ch.getSuffixTreeName(region)
                        if doBlindingMC and "SR" in region and whichKind['type'].find("minusone")==0:
                            if process['key'] == "Yjets":
                                print "Process is: ", process['key'], ", applying scale factor of ", kappaYjets
                                ntmc=NtHandler(ana+region+process['treePrefix']+"_baseline",process['inputdir'],mcname,cuts+" && Meff < 1000 ",process['color'],weights,"mc",configMain.lumi*kappaYjets)
                            else:
                                print "MUFACT:", ana, process['key'], mufacts[ana][process['key']]
                                ntmc=NtHandler(ana+region+process['treePrefix']+"_baseline",process['inputdir'],mcname,cuts+" && Meff < 1000 ",process['color'],weights,"mc",configMain.lumi*mufacts[ana][process['key']])
                                print "MC is blinded beyond meffincl of 1000 GeV"
                        else:
                            if process['key'] == "Yjets":
                                print "Process is: ", process['key'], ", applying scale factor of ", kappaYjets," lumi type: ", type(configMain.lumi), configMain.lumi
                                ntmc=NtHandler(ana+region+process['treePrefix']+"_baseline",process['inputdir'],mcname,cuts,process['color'],weights,"mc",configMain.lumi*kappaYjets)
                            elif process['key'] == "QCDJS":
                                print "Process is: ", process['key'], ", applying weight of 0.01 * eventWeight, lumi type: ", type(configMain.lumi), configMain.lumi
                                print "MUFACT:", ana, process['key'], mufacts[ana]["Multijets"]
                                ntmc=NtHandler(ana+region+process['treePrefix']+"_baseline",process['inputdir'],mcname,cuts,process['color'],"0.01*eventWeight","mc",configMain.lumi*mufacts[ana]["Multijets"])
                            elif process['key'] == "QCDMC" and config.region=="CRY":
                                print "Process is: ", process['key'], ", removing photon overlaps, lumi type: ", type(configMain.lumi), configMain.lumi
                                ntmc=NtHandler(ana+region+process['treePrefix']+"_baseline",process['inputdir'],mcname,cuts+"&&(phTruthOrigin!=38)",process['color'],weights,"mc",configMain.lumi)
                            else:
                                print "MUFACT:", ana, process['key'], mufacts[ana][process['key']]
                                ntmc=NtHandler(ana+region+process['treePrefix']+"_baseline",process['inputdir'],mcname,cuts,process['color'],weights,"mc",configMain.lumi*mufacts[ana][process['key']])
                        fullPlotMC.append({"mcname":mcname,"mctreePrefix":process['treePrefix'],"ntmchandle":ntmc})

                        if doSyst:
                            for syst in systDict:
                                mcname=process['treePrefix']+ch.getSuffixTreeName(region)+syst
                                treename = ana+region+process['treePrefix']+"_baseline"
                                if process['key'] == "QCDMC":
                                    ntsyst=NtHandler(treename,process['inputdir'],process['treePrefix']+ch.getSuffixTreeName(region),cuts,process['color'],weights,"mc",configMain.lumi*mufacts[ana][process['key']])
                                elif process['key'] == "QCDJS":
                                    ntsyst=NtHandler(treename,process['inputdir'],process['treePrefix']+ch.getSuffixTreeName(region),cuts,process['color'],"0.01*eventWeight","mc",configMain.lumi*mufacts[ana]["Multijets"])
                                elif process['key'] == "Yjets":
                                    print "Process is: ", process['key'], ", applying scale factor of ", kappaYjets," weight type: ", type(weights)
                                    ntsyst=NtHandler(treename,process['inputdir'],mcname,cuts,process['color'],weights,"mc",configMain.lumi*kappaYjets)
                                else:
                                    print "MUFACT:", ana, process['key'], mufacts[ana][process['key']]
                                    ntsyst=NtHandler(treename,process['inputdir'],mcname,cuts,process['color'],weights,"mc",configMain.lumi*mufacts[ana][process['key']])
                                fullPlotMCSyst.append({"mcname":mcname,"mctreePrefix":process['treePrefix'],"ntsyst":syst,"ntsysthandle":ntsyst})

                    if doSyst:
                        for process in mc_alternative:
                            print "ALTERNATIVE SAMPLES!: PROCESS: ", process['key']
                            if "QCD" in process['key']:
                                mcname=process['treePrefix']+ch.getSuffixTreeName(region)
                                systfact = 1.99 if 'systup' in process['key'] else 0.01
                                print "QCD SYST", systfact
                                ntsyst=NtHandler(ana+region+process['treePrefix']+"_alternative",process['inputdir'],mcname,cuts,process['color'],0.01,"mc",configMain.lumi*mufacts[ana]["Multijets"]*systfact)
                                fullPlotMCAlt.append({"mcname":mcname,"mctreePrefix":process['treePrefix'],"mctreeSuffix":"","ntmcalthandle":ntsyst})
                            elif "Zjets" in process['key'] or "Diboson" in process['key']:
                                systfact = 1.5 if "Diboson" in process['key'] else 1.11
                                if 'systdn' in process['key']: systfact = 0.5 if "Diboson" in process['key'] else 0.89
                                print process['key'], " SYST", systfact
                                print "MUFACT:", ana, process['key'], mufacts[ana][process['key'].split('_')[0]]
                                mcname=process['treePrefix']+ch.getSuffixTreeName(region)
                                ntsyst=NtHandler(ana+region+process['treePrefix']+"_alternative",process['inputdir'],mcname,cuts,process['color'],weights,"mc",configMain.lumi*mufacts[ana][process['key'].split('_')[0]]*systfact)
                                fullPlotMCAlt.append({"mcname":mcname,"mctreePrefix":process['treePrefix'],"mctreeSuffix":"","ntmcalthandle":ntsyst})
                            else:
                                print "MUFACT:", ana, process['key'], mufacts[ana][process['key'].split('_')[0]]
                                mcname=process['treePrefix']+ch.getSuffixTreeName(region)+process['treeSuffix']
                                ntsyst=NtHandler(ana+region+process['treePrefix']+"_alternative",process['inputdir'],mcname,cuts,process['color'],weights,"mc",configMain.lumi*mufacts[ana][process['key'].split('_')[0]])
                                fullPlotMCAlt.append({"mcname":mcname,"mctreePrefix":process['treePrefix'],"mctreeSuffix":process['treeSuffix'],"ntmcalthandle":ntsyst})
                        if doCRY:
                            for process in mc_truth:
                                mcname=process['treePrefix']+ch.getSuffixTreeName(region)+process['treeSuffix']
                                print "ALTERNATIVE SAMPLES!: PROCESS: ", process['key']
                                print "Process is: ", process['key'], ", applying scale factor of ", kappaYjets

                                ntsyst=NtHandler(ana+region+process['treePrefix']+process['treeSuffix'],process['inputdir'],mcname,truthcuts,process['color'],truthweights,"mc",configMain.lumi*kappaYjets)

                                fullPlotMCTruth.append({"mcname":mcname,"mctreePrefix":process['treePrefix'],"mctreeSuffix":process['treeSuffix'],"ntmctruthalthandle":ntsyst})

                    for varinList in varList:
                        varname=varinList['varName']
                        if not config.varToRun=="" and not varname==config.varToRun: continue
                        if varname in varset or 'all' in varset:
                            var=varinList['varNtuple']
                            if 'extracuts' in varinList:
                                temp="(("+cuts+")&&("+varinList['extracuts']+"))"
                                cuts=temp
                            print 'adding extracuts for var',varinList['varName'],cuts
                            plotname=varinList['plotName']
                            if "LastCut" in plotname:
                                chnameshort = ch.name.split('Jigsaw')[1][:3]
                                plotname = plotname.replace("LastCut",lastcutsfull[chnameshort])
                            elif "Ratio" in plotname:
                                chnameshort = ch.name.split('Jigsaw')[1][:3]
                                plotname = plotname.replace("Ratio",ratiocutsfull[chnameshort])
                            if var == "LastCut":
                                chnameshort = ch.name.split('Jigsaw')[1][:3]
                                var = lastcuts[chnameshort]
                            elif var == "Ratio":
                                chnameshort = ch.name.split('Jigsaw')[1][:3]
                                var = ratiocuts[chnameshort]
                            print "VAR", varname, var
                            nbinvar=int(varinList['nbinvar'])
                            minvar=float(varinList['minvar'])
                            maxvar=float(varinList['maxvar'])
                            unit=varinList['unit']

                            signalHistos=[]
                            nameSignalHistos=[]
                            nameMassSignalHistos=[]

                            histsout = []
                            histsout += parallelProcessProj( fullPlotMC,1,var,varname,ana,region,cuts,"",'ntmchandle',nbinvar,minvar,maxvar )
                            histsout += parallelProcessProj( fullPlotMCAlt,1,var,varname,ana,region,cuts,"Alternative",'ntmcalthandle',nbinvar,minvar,maxvar )
                            histsout += parallelProcessProj( fullPlotMCTruth,1,var,varname,ana,region,truthcuts,"TruthAlternative",'ntmctruthalthandle',nbinvar,minvar,maxvar )
                            histsout += parallelProcessProj( fullPlotMCSyst,1,var,varname,ana,region,cuts,"Syst",'ntsysthandle',nbinvar,minvar,maxvar )

                            print "WHEREAMI"

                            arrow=-1
                            arrowupper=-1
                            varcut = None
                            varcutupper = None
                            arrowvar = var
                            if varname in ["met","meffIncl"]: arrowvar = varname
                            print "ARROW", varname, arrowvar
                            if hasattr(ch,arrowvar) and not getattr(ch,arrowvar)==None:
                                if "loosen" in ch.regionListDict[region][arrowvar].lower():
                                    varcut=getattr(ch,arrowvar+"_loose")
                                else:
                                    varcut=getattr(ch,arrowvar)
                            if hasattr(ch,arrowvar+"_upper") and not getattr(ch,arrowvar+"_upper")==None:
                                if "loosen" in ch.regionListDict[region][arrowvar].lower():
                                    varcutupper=getattr(ch,arrowvar+"_upper_loose")
                                else:
                                    varcutupper=getattr(ch,arrowvar+"_upper")
                            if not varcut==None:
                                print "Place arrow at", arrowvar, " = ", varcut
                                arrow=1
                            if not varcutupper==None:
                                print "Place uppercut arrow at", arrowvar, " = ", varcutupper
                                arrowupper=1
                            if ana.find("Pres")>=0:
                                arrow=0

                            extraarrow = -1
                            extravarcut = None
                            if region=="SR" and varname=="LastCut" and ("SRS" in ana or "SRG" in ana):
                                extraarrow=1
                                if "a" in ana:
                                    extravarcut=allChannel[ana.replace('1a','1b').replace('2a','2b').replace('3a','3b')]
                                elif "b" in ana:
                                    extravarcut=allChannel[ana.replace('1b','1a').replace('2b','2a').replace('3b','3a')]

                            mcInt = {}
                            firstbin = 0
                            lastbin = -1
                            smTotal = 0.
                            mcHisto=[]
                            mcSystHisto=[]
                            mcAltHisto=[]
                            mcTruthAltHisto=[]
                            for histo in histsout:
                                print histo.GetName(), histo.GetEntries()
                                clone=histo.Clone()
                                if varcut != None: firstbin = histo.GetXaxis().FindBin(varcut)
                                if varcutupper != None: lastbin = histo.GetXaxis().FindBin(varcutupper)
                                mcInt[clone.GetName()] = histo.Integral(firstbin,lastbin)
                                smTotal += mcInt[clone.GetName()]
                                print "CLONE", clone.GetName(), "INT", clone.Integral()

                                if config.vbins and (varname=="LastCut" or varname=="H2PP"):
                                    clone = clone.Rebin(Nvarbin_lastcut,clone.GetName()+"_rebin",array('d',varbin_lastcut))
                                    for ibin in range(clone.GetNbinsX()):
                                        clone.SetBinContent(ibin+1,clone.GetBinContent(ibin+1)*varbin_rescale[ibin])
                                        clone.SetBinError(ibin+1,clone.GetBinError(ibin+1)*varbin_rescale[ibin])
                                if DrawOverflow:
                                    print "INGRID: nbins: ",clone.GetNbinsX(), ", Overflowbin: ", clone.GetBinContent(clone.GetNbinsX()+1)
                                    nBins = clone.GetNbinsX()
                                    LastBin = clone.GetBinContent(nBins)
                                    OverflowBin = clone.GetBinContent(nBins+1)
                                    print "Adding overflow bin!"
                                    clone.SetBinContent(nBins,LastBin+OverflowBin)


                                lock_sys=0
                                if "TRUTH" in histo.GetName():
                                    lock_sys=3
                                elif 'alternative' in histo.GetName().lower():
                                    lock_sys=2
                                for sys in systDict:
                                    if sys in histo.GetName():
                                        lock_sys=1
                                if lock_sys == 0:
                                    mcHisto.append(clone)
                                elif lock_sys == 1:
                                    mcSystHisto.append(clone)
                                elif lock_sys == 3:
                                    mcTruthAltHisto.append(clone)
                                else:
                                    mcAltHisto.append(clone)

                            lock=1

                            if runSignal:
                                for point in plotSignalList:
                                    print 'Signal Point: ',point['pointname']
                                    signalHisto=ROOT.TH1F(varname+point['pointname']+tmptreename+ana+region,varname,nbinvar,minvar,maxvar)
                                    print signalHisto
                                    point['nthandle'].project(1.,varname+point['pointname']+tmptreename+ana+region,var,cuts)
                                    print "SIGNAL", signalHisto, signalHisto.GetEntries()
                                    signalHisto.SetLineColor(point['pointcolor'])
                                    signalHisto.SetLineStyle(point['pointlinestyle'])
                                    signalHisto.SetLineWidth(2)
                                    signalHistos.append(signalHisto)
                                    nameSignalHistos.append(point['pointsigplotname'])
                                    nameMassSignalHistos.append(point['pointmass'])
#                                            print "SIGNAL", signalHistos

                            if doCRY and doSyst:
                                for process in fullPlotMCTruth:
                                    TruthHisto = ROOT.TH1F(varname+process['mctreePrefix']+ana+region+process['mctreeSuffix'],varname,nbinvar,minvar,maxvar)
                                    process['ntmctruthalthandle'].project(1.,varname+process['mctreePrefix']+ana+region+process['mctreeSuffix'],var,truthcuts)
                                    #print TruthHisto.GetName()
                                    mcTruthAltHisto.append(TruthHisto)

                            canvas = ROOT.TCanvas(" "," ",10,32,668,643)
                            canvas.SetFrameFillColor(kWhite)
                            canvas.SetLogy(ROOT.kTRUE)
                            if(runData or len(systDict)>0 or doSignificance ):
                                upperPad = ROOT.TPad("upperPad", "upperPad", .001, .15, .995, .995)
                                lowerPad = ROOT.TPad("lowerPad", "lowerPad", .001, .001, .995, .27)
                                rootOpt.setUpPads("_logy",upperPad,lowerPad)
                                lowerPad.SetTopMargin(0.026)
                                upperPad.SetFrameFillStyle(4000)
                                lowerPad.SetFrameFillStyle(4000)
                                upperPad.cd()

                            dataInt = 0
                            if(runData):
                                print 'new data plot',varname+"data"+ana+region,varname,nbinvar,minvar,maxvar
                                dataHisto=ROOT.TH1F(varname+"data"+ana+region,varname,nbinvar,minvar,maxvar)
                                dataHisto.GetXaxis().SetTitle(plotname)
                                lock=1
                                for plot in plotData:
                                    if doBlinding and "SR" in region:
                                        print "Data is blinded beyond SR cut"
                                        plot.project(lock,varname+"data"+ana+region,var,cuts+blindcut)
                                    else:
                                        plot.project(lock,varname+"data"+ana+region,var,cuts)

                                if DrawOverflow:
                                    print "INGRID: nbins: ",dataHisto.GetNbinsX(), ", Overflowbin: ", dataHisto.GetBinContent(dataHisto.GetNbinsX()+1)
                                    nBinsdata = dataHisto.GetNbinsX()
                                    LastBindata = dataHisto.GetBinContent(nBinsdata)
                                    OverflowBindata = dataHisto.GetBinContent(nBinsdata+1)
                                    print "Adding overflow bin!"
                                    dataHisto.SetBinContent(nBinsdata,LastBindata+OverflowBindata)
                                dataInt = dataHisto.Integral(firstbin,lastbin)
                                if config.vbins and (varname=="LastCut" or varname=="H2PP"):
                                    dataHisto = dataHisto.Rebin(Nvarbin_lastcut,dataHisto.GetName()+"_rebin",array('d',varbin_lastcut))
                                    for ibin in range(dataHisto.GetNbinsX()):
                                        dataHisto.SetBinContent(ibin+1,dataHisto.GetBinContent(ibin+1)*varbin_rescale[ibin])
                                        dataHisto.SetBinError(ibin+1,0.)

                                datah_Poiss = ROOT.TGraphAsymmErrors(dataHisto.GetNbinsX())
                                datah_Poiss.SetMarkerStyle(20)
                                datah_Poiss.SetMarkerSize(1.2)
                                datah_Poiss.SetMarkerColor(kBlack)
                                datah_Poiss.SetLineColor(kBlack)
                                datah_Poiss.SetLineWidth(3)
                                if config.vbins and (varname=="LastCut" or varname=="H2PP"):
                                    setAsymmErrors(dataHisto,datah_Poiss,varbin_rescale)
                                else:
                                    setAsymmErrors(dataHisto,datah_Poiss)

                                dataClone = ROOT.TGraphAsymmErrors(dataHisto.GetNbinsX())
                                dataClone.SetMarkerStyle(20)
                                dataClone.SetMarkerSize(1.5)
                                dataClone.SetLineWidth(5)
                                dataClone.SetMarkerColor(kWhite)
                                dataClone.SetLineColor(kWhite)
                                setAsymmErrors(dataHisto,dataClone)
                                if config.vbins and (varname=="LastCut" or varname=="H2PP"):
                                    setAsymmErrors(dataHisto,dataClone,varbin_rescale)
                                else:
                                    setAsymmErrors(dataHisto,dataClone)
                                max = 5e5
                                min = 0.03
                                if config.doCompressed or not unit=='GeV':
                                    if dataHisto.GetMaximum()>1000:
                                        max *= 1000
                                        min *= 10
                                    elif dataHisto.GetMaximum()>100:
                                        max *= 100
                                        min *= 10
                                dataHisto.GetYaxis().SetRangeUser(min,max)
                                datah_Poiss.GetYaxis().SetRangeUser(min,max)

                                binWidth=dataHisto.GetBinWidth(1)
                                XUnit="Events / {0:.2f}".format(binWidth)
                                if(unit): XUnit=XUnit+" "+unit
                                dataHisto.GetYaxis().SetTitle(XUnit)
                                dataHisto.GetYaxis().SetLabelSize(0.05)
                                dataHisto.GetYaxis().SetTitleSize(0.055)
                                dataHisto.GetYaxis().SetTitleOffset(1.35)
                                dataHisto.GetYaxis().SetTitleFont(42)
                                for ibin in range(1,dataHisto.GetNbinsX()+1):
                                    dataHisto.SetBinError(ibin,0.)

                                dataHisto.Draw("p")
                                dataClone.Draw("p:e:same")
                                datah_Poiss.Draw("p:e:same")

                            mcStack = ROOT.THStack("stack","title_stack")
                            mcTotal = ROOT.TH1F("mcTotal",varname,nbinvar,minvar,maxvar)
                            mcTotal.SetLineColor(2)
                            mcTotal.SetLineWidth(2)

                            Clone_mcHisto=[]
                            binWidth=0
                            XUnitStack="units"
                            for whichmc in mc:
                                for h in mcHisto:
                                    if whichmc['treePrefix'] in h.GetName().split(varname)[1]:
                                        print "MCSTACK:", h.GetName(), h.Integral()
                                        clone=h.Clone()
                                        Clone_mcHisto.append(clone)
                                        mcStack.Add(clone)
                                        mcTotal.Add(clone)
                                        binWidth=clone.GetBinWidth(1) if varname.find("Jets")<0 else int(clone.GetBinWidth(1))
                                        XUnitStack="Events / "+str(binWidth)+" "+unit
                            print "MCTOTAL int:", mcTotal.Integral()

                            sumSystHist=[]
                            for isyst in systDict:
                                tempHist=ROOT.TH1D("tempHist_"+isyst,"tempHist",mcSystHisto[0].GetNbinsX(),mcSystHisto[0].GetXaxis().GetXmin(),mcSystHisto[0].GetXaxis().GetXmax())
                                #print 'init',tempHist.GetBinContent(8)
                                for h in mcSystHisto:
                                    if isyst in h.GetName():
                                        #print h.GetName(), h.Integral()
                                        tempHist.Add(h)
                            #tempHist.Print()
                                sumSystHist.append(tempHist)
                            for hAlt in mcAltHisto:
                                mcAltTotal = mcTotal.Clone("mcAltTotal_"+hAlt.GetName())
                                clonealt=None
                                for h in mcHisto:
                                    if "GAMMA" in h.GetName(): continue
                                    print "MCALT:", h.GetName(), hAlt.GetName()
                                    if h.GetName() in hAlt.GetName():
                                        print "MCALTTOTAL: rm", h.GetName(), h.Integral(), "add", hAlt.GetName(), hAlt.Integral()
                                        clonealt=hAlt.Clone()
                                        clonealt.Add(h,-1.)
                                if clonealt: mcAltTotal.Add(clonealt)
                                print "MCALTTOTAL int:", mcAltTotal.Integral()
                                sumSystHist.append(mcAltTotal)

                            if doCRY and len(mcTruthAltHisto)>0:
                                #print mcTruthAltHisto
                                mcTruthAltTotal = ROOT.TH1F("mcTruthAltTotal",varname,nbinvar,minvar,maxvar)
                                mcTruthAltTotal = mcTotal.Clone(mcTotal.GetName()+"TruthAlt")
                                for h in mcTruthAltHisto:
                                    if "Madgraph" in h.GetName():
                                        mcTruthAltTotal.Add(h,1)
                                        print "MCTRUTHALTTOTAL: add", h.GetName(), h.Integral()
                                    else:
                                        mcTruthAltTotal.Add(h,-1)
                                        print "MCTRUTHALTTOTAL: rm", h.GetName(), h.Integral()
                                print "MCTRUTHALTTOTAL int:", mcTruthAltTotal.Integral()
                                sumSystHist.append(mcTruthAltTotal)

                            maxdata = -1
                            if(runData):
                                mcStack.Draw("same:hist")
                                mcTotal.Draw("hist:same")
                                if(runSignal):
                                    for hsig in signalHistos:
                                        if config.vbins and (varname=="LastCut" or varname=="H2PP"):
                                            hsig = hsig.Rebin(Nvarbin_lastcut,hsig.GetName()+"_rebin",array('d',varbin_lastcut))
                                            for ibin in range(hsig.GetNbinsX()):
                                                hsig.SetBinContent(ibin+1,hsig.GetBinContent(ibin+1)*varbin_rescale[ibin])
                                                hsig.SetBinError(ibin+1,hsig.GetBinError(ibin+1)*varbin_rescale[ibin])
                                        if SignalOnTop:
                                            print "SIGNAL", len(signalHistos),signalHistos
                                            #print type(hsig), hsig
                                            hsig.Add(mcTotal,1)
                                            hsig.SetLineWidth(4)
                                            hsig.Draw("hist:same")
                                        else:
                                            #print type(hsig), hsig
                                            hsig.SetLineWidth(4)
                                            hsig.Draw("hist:same")
                                dataClone.Draw("p:e:same")
                                datah_Poiss.Draw("p:e:same")
                            else:
                                mcStack.Draw("hist")
                                mcTotal.Draw("hist:same")
                                mcTotal_Poiss = ROOT.TGraphAsymmErrors(mcTotal.GetNbinsX())
                                mcTotal_Poiss.SetMarkerStyle(20)
                                mcTotal_Poiss.SetMarkerSize(1.2)
                                mcTotal_Poiss.SetMarkerColor(kBlack)
                                mcTotal_Poiss.SetLineColor(kBlack)
                                mcTotal_Poiss.SetLineWidth(3)
                                setAsymmErrors(mcTotal,mcTotal_Poiss)
                                mcTotal_Poiss.SetFillStyle(3444)
                                mcTotal_Poiss.SetFillColor(2)
                                maxsig = -1.
                                if(runSignal):
                                    for hsig in signalHistos:
                                        hsig.SetLineWidth(4)
                                        hsig.Draw("hist:same")
                                        maxsig = TMath.Max(maxsig, hsig.GetMaximum())
                                min = 0.07
                                maxbkg = mcStack.GetMaximum()
                                max = max([maxbkg, maxsig])
                                if (max <= 2.) :  min = 0.007
                                yfactor = 400 if config.doCompressed else 4
                                mcStack.SetMinimum(min)
                                mcStack.SetMaximum(max*yfactor)
                                mcStack.GetYaxis().SetRangeUser(min,max*yfactor)
                                mcStack.GetYaxis().SetTitle(XUnitStack)
                                mcStack.GetYaxis().SetLabelSize(0.05)
                                mcStack.GetYaxis().SetTitleOffset(1.4)
                                mcStack.GetYaxis().SetTitleFont(42)
                                xti=plotname
                                if(unit): xti=xti+" ["+unit+"]"
                                mcStack.GetXaxis().SetTitle(xti)
                                if(len(systDict)>0):
                                    mcStack.GetXaxis().SetLabelSize(0.)
                                else:
                                    mcStack.GetXaxis().SetLabelSize(0.03)
                                mcStack.GetXaxis().SetTitleOffset(.9)
                                mcStack.GetXaxis().SetTitleSize(0.04)
                                canvas.Modified()

                            upperPad.RedrawAxis("same")

                            invertArrows = (varname in ch.regionListDict[region].keys() and "invert" in ch.regionListDict[region][varname])
                            print arrowvar, ch.regionListDict[region]
                            if arrowvar in ch.regionListDict[region].keys():
                                print arrowvar, ch.regionListDict[region][arrowvar]
                                print invertArrows
                            if arrow>0:
                                armax = 5.0 if not whichKind['type'].find("baseline")>=0 else 100
                                ar=TArrow(varcut,1.05*min,varcut,armax,0.05,"-")
                                ar.SetLineWidth(3)
                                ar.SetLineColor(kRed+2)
                                ar.SetFillColor(kRed+2)
                                ar.Draw("")

                                direction = -1 if invertArrows else 1
                                ar1=TArrow(varcut,armax,varcut+binWidth*direction,armax,0.01,"|>")
                                ar1.SetLineWidth(3)
                                ar1.SetLineColor(kRed+2)
                                ar1.SetFillColor(kRed+2)
                                ar1.Draw("")

                            if arrowupper>0:
                                arumax = 5.0 if not whichKind['type'].find("baseline")>=0 else 100
                                aru=TArrow(varcutupper,1.05*min,varcutupper,arumax,0.05,"-")
                                aru.SetLineWidth(3)
                                aru.SetLineColor(kRed+2)
                                aru.SetFillColor(kRed+2)
                                aru.Draw("")

                                direction = -1 if invertArrows else 1
                                aru1=TArrow(varcutupper,arumax,varcutupper-binWidth*direction,arumax,0.01,"|>")
                                aru1.SetLineWidth(3)
                                aru1.SetLineColor(kRed+2)
                                aru1.SetFillColor(kRed+2)
                                aru1.Draw("")

                            if extraarrow>0:
                                earmax = 5.0 if not whichKind['type'].find("baseline")>=0 else 100
                                ear=TArrow(varcut,1.05*min,extravarcut,earmax,0.05,"-")
                                ear.SetLineWidth(3)
                                ear.SetLineColor(kRed+2)
                                ear.SetFillColor(kRed+2)
                                ear.Draw("")

                                ear1=TArrow(varcut,earmax,extravarcut+binWidth,earmax,0.01,"|>")
                                ear1.SetLineWidth(3)
                                ear1.SetLineColor(kRed+2)
                                ear1.SetFillColor(kRed+2)
                                ear1.Draw("")

                            forPlotMcHisto=mcHisto[0]
                            cHisto=0
                            for h in mcHisto:
                                if cHisto>0: forPlotMcHisto.Add(h)
                                cHisto=cHisto+1
                            text=ROOT.TLatex()
                            if(runData):
                                PrintText(dataHisto.GetName(),text)

                            atlaslabel=ROOT.TLatex(0.2,0.89,"#bf{#it{ATLAS}} Preliminary")
                            atlaslabel.SetNDC()
                            atlaslabel.SetTextSize(0.055)
                            atlaslabel.SetTextFont(42)
                            atlaslabel.Draw("same")

                            lumilabel=ROOT.TLatex(0.2,0.82,"#sqrt{s}=13 TeV, %1.2f"  % configMain.lumi+" fb^{-1} " )
                            lumilabel.SetNDC()
                            lumilabel.SetTextSize(0.040)
                            lumilabel.SetTextFont(42)
                            lumilabel.Draw("same")

                            if "Pres" in ana:
                                anaName = ana
                                anaName = anaName.replace("Pres"," Preselection")
                            else:
                                anaName = ana.replace("SRJigsaw","RJR-")
                            tobewritten=(whichKind['name']+" for " if (whichKind['type'].find("CR")>=0 or whichKind['type'].find("VR")>=0) else "") +anaName
                            analabel=ROOT.TLatex(0.2, 0.75, (tobewritten))
                            analabel.SetNDC()
                            analabel.SetTextSize(0.035)
                            analabel.SetTextFont(42)
                            analabel.Draw("same")
                            if (runSignal):
                                if config.doCompressed:
                                    legend=ROOT.TLegend(0.6,0.45,0.85,0.95)
                                else:
                                    legend=ROOT.TLegend(0.6,0.42,0.85,0.95)
                            else:
                                legend=ROOT.TLegend(0.6,0.53,0.89,0.95)
                            if(runData):
                                legend.AddEntry(dataHisto,"Data 2015 and 2016" + (" ({0})".format(dataInt) if varname=="LastCut" and config.int else ""),"p")
                            legend.AddEntry(mcTotal,"SM Total" + (" ({0:.2f})".format(smTotal) if varname=="LastCut" and config.int else ""),"l")
                            if SignalOnTop:
                                legend.SetTextSize(0.03)
                            else:
                                legend.SetTextSize(0.035)
                            legend.SetFillColor(0)
                            legend.SetFillStyle(0)
                            legend.SetBorderSize(0)

                            for whichmc in reversed(mc):
                                for h in mcHisto:
#                                            print h.GetName()
                                    if whichmc['treePrefix'] in h.GetName().split(varname)[1]:
                                        legend.AddEntry(h,whichmc['name'] + (" ({0:.2f})".format(mcInt[h.GetName()[:-6]]) if varname=="LastCut" and config.int else ""),"f")

                            if(runSignal) and SignalOnTop:
                                isig=0
                                for hsig in signalHistos:
                                    legend.AddEntry(hsig,"SM Total + Signal","l")
                                    legend.AddEntry("",nameSignalHistos[isig],"")
                                    legend.AddEntry("",nameMassSignalHistos[isig],"")
                                    isig+=1
                            elif(runSignal):
                                isig=0
                                for hsig in signalHistos:
                                    sigInt = hsig.Integral(firstbin,lastbin)
                                    legend.AddEntry(hsig,nameSignalHistos[isig]+(" ({0:.2f})".format(sigInt) if varname=="LastCut" and config.int else ""),"l")
                                    legend.AddEntry("",nameMassSignalHistos[isig],"")
                                    isig+=1

                            legend.SetLineColor(10)
                            legend.SetFillColor(10)
                            legend.Draw()

                            if(runData or len(mcSystHisto)>0 or doSignificance):
                                lowerPad.cd()
                                if(runData):
                                    ratio=ROOT.TGraphAsymmErrors(dataHisto.GetNbinsX())
                                    Allsys_band=ROOT.TGraphAsymmErrors(dataHisto.GetNbinsX())
                                    Allsys_plusTheory_band=ROOT.TGraphAsymmErrors(dataHisto.GetNbinsX())
                                    skeletonRatio=ROOT.TH1D("skeleton","skeleton",dataHisto.GetNbinsX(),dataHisto.GetXaxis().GetXmin(),dataHisto.GetXaxis().GetXmax())
                                    Redline=ROOT.TLine(dataHisto.GetXaxis().GetXmin(),1,dataHisto.GetXaxis().GetXmax(),1)
                                    skeletonRatio.GetXaxis().SetTitle(dataHisto.GetXaxis().GetTitle())
                                elif doSyst:
                                    ratio=ROOT.TGraphAsymmErrors(forPlotMcHisto.GetNbinsX())
                                    Allsys_band=ROOT.TGraphAsymmErrors(forPlotMcHisto.GetNbinsX())
                                    Allsys_plusTheory_band=ROOT.TGraphAsymmErrors(forPlotMcHisto.GetNbinsX())
                                    skeletonRatio=ROOT.TH1D("skeleton","skeleton",forPlotMcHisto.GetNbinsX(),forPlotMcHisto.GetXaxis().GetXmin(),forPlotMcHisto.GetXaxis().GetXmax())
                                    Redline=ROOT.TLine(forPlotMcHisto.GetXaxis().GetXmin(),1,forPlotMcHisto.GetXaxis().GetXmax(),1)
                                    xti=plotname
                                    if(unit): xti=xti+" ["+unit+"]"
                                    forPlotMcHisto.GetXaxis().SetTitle(xti)
                                    skeletonRatio.GetXaxis().SetTitle(forPlotMcHisto.GetXaxis().GetTitle())
                                elif doSignificance:
                                    ratio=ROOT.TGraphAsymmErrors(forPlotMcHisto.GetNbinsX())
                                    Allsys_band=ROOT.TGraphAsymmErrors(forPlotMcHisto.GetNbinsX())
                                    skeletonRatio=ROOT.TH1D("skeleton","skeleton",forPlotMcHisto.GetNbinsX(),forPlotMcHisto.GetXaxis().GetXmin(),forPlotMcHisto.GetXaxis().GetXmax())
                                    Redline=ROOT.TLine(forPlotMcHisto.GetXaxis().GetXmin(),1,forPlotMcHisto.GetXaxis().GetXmax(),1)
                                    xti=plotname
                                    if(unit): xti=xti+" ["+unit+"]"
                                    forPlotMcHisto.GetXaxis().SetTitle(xti)
                                    skeletonRatio.GetXaxis().SetTitle(forPlotMcHisto.GetXaxis().GetTitle())
                                ratio.SetMarkerStyle(20 if runData else 19)
                                ratio.SetMarkerSize(0.1 if runData else 1.2)
                                ratio.SetLineWidth(3)
                                Allsys_band.SetFillColor(kYellow)
                                Allsys_plusTheory_band.SetFillColor(kRed+2)
                                Allsys_plusTheory_band.SetFillStyle(3354)
                                gStyle.SetHatchesLineWidth(2)
                                estimSystwTheory(forPlotMcHisto,sumSystHist,Allsys_band,Allsys_plusTheory_band)
                                #print forPlotMcHisto, sumSystHist
                                if(runData): GetDataMCRatio(dataHisto,forPlotMcHisto,ratio)
                                if doSignificance:
                                    sigRatios=[]
                                    for s in signalHistos:
                                        print 'in PlotMaker run over s'
                                        sigRatio=ROOT.TH1D("sigR","sigR",s.GetNbinsX(),s.GetXaxis().GetXmin(),s.GetXaxis().GetXmax())
                                        sig_temp=s.Clone()
                                        ComputeSignificance(sig_temp,forPlotMcHisto,sigRatio)
                                        keep_ratio=sigRatio.Clone()
                                        keep_ratio.SetLineColor(s.GetLineColor())
                                        sigRatios.append(keep_ratio)

                                skeletonRatio.GetXaxis().SetLabelSize(0.13)
                                skeletonRatio.GetXaxis().SetTitleSize(0.15)

                                skeletonRatio.GetXaxis().SetTitleOffset(1)
                                skeletonRatio.GetYaxis().SetLabelSize(0.10)
                                skeletonRatio.GetYaxis().SetTitleSize(0.15)
                                skeletonRatio.GetYaxis().SetTitleOffset(0.48)
                                skeletonRatio.GetYaxis().SetRangeUser(0,3.2)
                                skeletonRatio.GetYaxis().SetRangeUser(0,2.)
                                skeletonRatio.GetYaxis().SetNdivisions(504,False)
                                if runData :
                                    skeletonRatio.GetYaxis().SetTitle("Data / MC")
                                elif doSignificance:
                                    skeletonRatio.GetYaxis().SetTitle("Significance")
                                    skeletonRatio.GetYaxis().SetRangeUser(0,6.)
                                else:
                                    skeletonRatio.GetYaxis().SetTitle("MC syst")

                                Redline.SetLineColor(2)
                                Redline.SetLineStyle(2)
                                Redline.SetLineWidth(2)

                                skeletonRatio.Draw()
                                if doSyst:
                                    #Allsys_band.Draw("2 same")
                                    Allsys_plusTheory_band.Draw("2 same")
                                elif doSignificance:
                                    for s in sigRatios:
                                        s.Draw("2 same")
                                ratio.Draw("same:p:e")
                                ErrorLines = DrawErrorsOutsidePad(ratio)

                                for lines in ErrorLines:
                                    lines.Draw()

                                if not doSignificance:
                                    Redline.Draw("same")
                                lowerPad.RedrawAxis("same")

                            if SignalOnTop:
                                canvas.SaveAs(outplotdir+('intL%0difb' % configMain.lumi)+"_"+region+"_"+ana+"_"+varname+"_"+whichKind['type']+"_SignalOnTop"+".pdf")
                                canvas.SaveAs(outplotdir+('intL%0difb' % configMain.lumi)+"_"+region+"_"+ana+"_"+varname+"_"+whichKind['type']+"_SignalOnTop"+".eps")
                            else:
                                canvas.SaveAs(outplotdir+('intL%0difb' % configMain.lumi)+"_"+region+"_"+ana+"_"+varname+"_"+whichKind['type']+".pdf")
                                canvas.SaveAs(outplotdir+('intL%0difb' % configMain.lumi)+"_"+region+"_"+ana+"_"+varname+"_"+whichKind['type']+".eps")
                            del canvas,mcTotal,legend,mcStack
                            DeleteList(mcHisto)
                            DeleteList(Clone_mcHisto)
                            DeleteList(mcSystHisto)
                            DeleteList(mcAltHisto)
                            DeleteList(mcTruthAltHisto)
                    if runData: DeleteList(plotData)
                    if runSignal: DeleteNtList(plotSignalList)
                    DeleteNtList(fullPlotMC)
                    if doSyst: DeleteNtList(fullPlotMCSyst)

if __name__ == "__main__":
    main(config)
