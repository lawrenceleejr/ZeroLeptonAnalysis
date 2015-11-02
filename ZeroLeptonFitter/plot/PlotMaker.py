#export ZEROLEPTONFITTER=$PWD

import sys, os, string, shutil,pickle,subprocess, time

from multiprocessing import Process,Lock,Queue
import ROOT
from ROOT import *
file_path = os.path.abspath("plot")
sys.path.append(file_path)
from PlotterUtils import *

file_path = os.path.abspath("python")
sys.path.append(file_path)
from ChannelConfig import *
from allChannelsDict import *

runData=True
runSignal=True
doCRWT=False
doCRY=True
doCRZ=False
doSyst=False
doSignificance=False

if doSignificance:
	runSignal=True

if doCRWT or doCRY or doCRZ:
        runSignal=False
        
saveToFile=False

version=34

doRun2=True
if(doRun2):
        runData=False


gStyle=ROOT.gStyle
rootOpt=RootOption(gStyle)
rootOpt.setUpStyle()

varList = [
        {'varName':'meffincl','varNtuple':'meffInc/1000.','plotName':'m_{eff}(incl.)','nbinvar':'50','minvar':'0','maxvar':'5000.','unit':'GeV'},
        {'varName':'met','varNtuple':'met/1000.','plotName':'E_{T}^{miss}','nbinvar':'60','minvar':'0','maxvar':'3000.','unit':'GeV'},
        {'varName':'metSig','varNtuple':'met/1000./sqrt((meffInc-met)/1000.)','plotName':'E_{T}^{miss}/#sqrt{H_{T}}','nbinvar':'25','minvar':'0','maxvar':'50','unit':'#sqrt{GeV}'}, 
        {'varName':'metomeff','varNtuple':'met/meffInc','plotName':'E_{T}^{miss}/m_{eff}(incl.)','nbinvar':'24','minvar':'0','maxvar':'1.2','unit':''},
        {'varName':'metomeff2jet','varNtuple':'met/(met+jetPt[0]+jetPt[1])','plotName':'E_{T}^{miss}/m_{eff}(N_{jets})','nbinvar':'24','minvar':'0','maxvar':'1.2','unit':''},
        {'varName':'metomeff4jet','varNtuple':'met/(met+jetPt[0]+jetPt[1]+jetPt[2]+jetPt[3])','plotName':'E_{T}^{miss}/m_{eff}(N_{jets})','nbinvar':'24','minvar':'0','maxvar':'1.2','unit':''},
        {'varName':'metomeff5jet','varNtuple':'met/(met+jetPt[0]+jetPt[1]+jetPt[2]+jetPt[3]+jetPt[4])','plotName':'E_{T}^{miss}/m_{eff}(N_{jets})','nbinvar':'24','minvar':'0','maxvar':'1.2','unit':''},
        {'varName':'meff2jet','varNtuple':'(met+jetPt[0]+jetPt[1])/1000.','plotName':'m_{eff}(2j)','nbinvar':'50','minvar':'0','maxvar':'5000.','unit':'GeV'},
        {'varName':'dphi','varNtuple':'dPhi','plotName':'min(#Delta#phi(E_{T}^{miss},jet_{1,2,3}))','nbinvar':'40','minvar':'0','maxvar':'4.0','unit':''},
        {'varName':'nJets','varNtuple':'nJet', 'plotName': 'N_{jets} (p_{T}>40 GeV, |#eta|<2.8)', 'nbinvar':'15','minvar':'0','maxvar':'15','unit':''},
        {'varName':'nJets60all','varNtuple':'nJet', 'plotName': 'N_{jets} (all jets with p_{T}>60 GeV, |#eta|<2.8)', 'nbinvar':'15','minvar':'0','maxvar':'15','unit':'', 'extracuts':'(jetPt[nJet-1]>60000.)'},    
        {'varName':'nbJets','varNtuple':'nBJet', 'plotName': 'N_{bjets} (p_{T}>40 GeV, |#eta|<2.5)', 'nbinvar':'15','minvar':'0','maxvar':'15','unit':''},
        {'varName':'jetpT1','varNtuple':'jetPt[0]/1000.', 'plotName': 'p_{T}(jet_{1})', 'nbinvar':'40','minvar':'0','maxvar':'2000','unit':'GeV'},
        {'varName':'jetpT2','varNtuple':'jetPt[1]/1000.', 'plotName': 'p_{T}(jet_{2})', 'nbinvar':'40','minvar':'0','maxvar':'2000','unit':'GeV'},
        {'varName':'jetpT3','varNtuple':'jetPt[2]/1000.', 'plotName': 'p_{T}(jet_{3})', 'nbinvar':'40','minvar':'0','maxvar':'1000','unit':'GeV'},
        {'varName':'jetpT4','varNtuple':'jetPt[3]/1000.', 'plotName': 'p_{T}(jet_{4})', 'nbinvar':'40','minvar':'0','maxvar':'1000','unit':'GeV'},
        {'varName':'jetpT5','varNtuple':'jetPt[4]/1000.', 'plotName': 'p_{T}(jet_{5})', 'nbinvar':'20','minvar':'0','maxvar':'500','unit':'GeV'},
        {'varName':'jetpT6','varNtuple':'jetPt[5]/1000.', 'plotName': 'p_{T}(jet_{6})', 'nbinvar':'20','minvar':'0','maxvar':'500','unit':'GeV'},
        {'varName':'mDR','varNtuple':'mdeltaR/1000.', 'plotName':'m^{#Delta}_{R}', 'nbinvar':'40','minvar':'0','maxvar':'2000.','unit':'GeV'},
        {'varName':'Ap','varNtuple':'Ap','nbinvar':'50','plotName':'Aplanarity', 'minvar':'0','maxvar':'0.5','unit':''},
        {'varName':'mT2', 'varNtuple':'mT2/1000.', 'plotName':'m_{T2}', 'nbinvar':'60','minvar':'0','maxvar':'3000.','unit':'GeV'},
        ## NOT FILLED {'varName':'mT2_noISR', 'varNtuple':'mT2_noISR/1000.', 'plotName':'m_{T2}(noISR)', 'nbinvar':'60','minvar':'0','maxvar':'3000.','unit':'GeV'},
        {'varName':"lep1Pt", 'varNtuple':"lep1Pt/1000.", 'plotName': 'p_{T}(lep_{1})', 'nbinvar':'50','minvar':'0','maxvar':'1000','unit':'GeV'}, 
        {'varName':"lep1Eta", 'varNtuple':"lep1Eta", 'plotName': '#eta(lep_{1})', 'nbinvar':'40','minvar':'-4','maxvar':'4','unit':''},
        {'varName':"lep1Phi", 'varNtuple':"lep1Phi", 'plotName': '#phi(lep_{1})', 'nbinvar':'40','minvar':'-4','maxvar':'4','unit':''},
        {'varName':"lep1sign", 'varNtuple':"lep1sign", 'plotName': 'sign(lep_{1})', 'nbinvar':'5','minvar':'-2','maxvar':'3','unit':''},
        {'varName':"lep2Pt", 'varNtuple':"lep2Pt/1000.", 'plotName': 'p_{T}(lep_{1})', 'nbinvar':'50','minvar':'0','maxvar':'1000','unit':'GeV'}, 
        {'varName':"lep2Eta", 'varNtuple':"lep2Eta", 'plotName': '#eta(lep_{2})', 'nbinvar':'40','minvar':'-4','maxvar':'4','unit':''},
        {'varName':"lep2Phi", 'varNtuple':"lep2Phi", 'plotName': '#phi(lep_{2})', 'nbinvar':'40','minvar':'-4','maxvar':'4','unit':''},
        {'varName':"lep2sign", 'varNtuple':"lep2sign", 'plotName': 'sign(lep_{2})', 'nbinvar':'5','minvar':'-2','maxvar':'3','unit':''},
        {'varName':"llsign", 'varNtuple':"lep1sign*lep2sign", 'plotName': 'sign(lep_{1})#timessign(lep_{2})', 'nbinvar':'5','minvar':'-2','maxvar':'3','unit':''},
        {'varName':'mt', 'varNtuple':'mt/1000.', 'plotName':'m_{T}', 'nbinvar':'50','minvar':'20','maxvar':'120.','unit':'GeV'},
        {'varName':'Wpt', 'varNtuple':'Wpt/1000.', 'plotName':'p_{T}(W)', 'nbinvar':'50','minvar':'0','maxvar':'2000.','unit':'GeV'},
        {'varName':'mll', 'varNtuple':'mll/1000.', 'plotName':'m_{ll}', 'nbinvar':'50','minvar':'40','maxvar':'140.','unit':'GeV'},
        {'varName':'Zpt', 'varNtuple':'Zpt/1000.', 'plotName':'p_{T}(Z)', 'nbinvar':'50','minvar':'0','maxvar':'2000.','unit':'GeV'},        
        {'varName':'mettrack','varNtuple':'mettrack/1000.','plotName':'E_{T}^{miss,track}','nbinvar':'60','minvar':'0','maxvar':'3000.','unit':'GeV'},
        {'varName':"mettrack_phi", 'varNtuple':"mettrack_phi", 'plotName': '#phi(E_{T}^{miss,track})', 'nbinvar':'40','minvar':'-4','maxvar':'4','unit':''},
        {'varName':"phPt", 'varNtuple':"phPt/1000.", 'plotName': 'p_{T}(#gamma)', 'nbinvar':'50','minvar':'0','maxvar':'2000','unit':'GeV'}, 
        {'varName':"phEta", 'varNtuple':"phEta", 'plotName': '#eta(#gamma)', 'nbinvar':'20','minvar':'-4','maxvar':'4','unit':''},
        {'varName':"phPhi", 'varNtuple':"phPhi", 'plotName': '#phi(#gamma)', 'nbinvar':'20','minvar':'-4','maxvar':'4','unit':''},
        {'varName':"phSignal", 'varNtuple':"phSignal", 'plotName': 'is_#gammaSignal', 'nbinvar':'6','minvar':'-1','maxvar':'5','unit':''},  ## always 1
        {'varName':'origmet','varNtuple':'origmet/1000.','plotName':'E_{T}^{miss,orig}','nbinvar':'40','minvar':'0','maxvar':'2000.','unit':'GeV'},
        {'varName':"origmetPhi", 'varNtuple':"origmetPhi", 'plotName': '#phi(E_{T}^{miss,orig})', 'nbinvar':'40','minvar':'-1','maxvar':'7','unit':''},
]



datafile =[
        {'whichdata':'SR','filename':'/afs/cern.ch/atlas/groups/susy/0lepton/ZeroLeptonFitter/ZeroLepton-00-00-53_Light/DataJetTauEtmiss.root',
         'dataname':'Data_SRAll'},
        #{'whichdata':'CRWT','filename':{'/afs/cern.ch/atlas/groups/susy/0lepton/ZeroLeptonFitter/ZeroLepton-00-00-53_Light/DataMuon.root','/afs/cern.ch/atlas/groups/susy/0lepton/ZeroLeptonFitter/ZeroLepton-00-00-53_Light/DataEgamma.root'},
         #'dataname':'Data_CRWT'},
]

mcdir ="/afs/cern.ch/atlas/groups/susy/0lepton/ZeroLeptonFitter/ZeroLepton-00-00-53_Light/"
if(doRun2):
        mcdir ="/afs/cern.ch/atlas/groups/susy/0lepton/ZeroLeptonFitter/ZeroLeptonRun2-00-00-"+str(version)+"/xAOD_13TeV/"
        if version>30:
                mcdir="/afs/cern.ch/work/n/nakahama/public/ZLdata/ZeroLeptonRun2-00-00-"+str(version)+"/p1872_13TeV/"

commonsyst=" "  

kindOfCuts=[]

kindOfCuts_SR=[
        {"type":"SR","var":["nJets","nJets60all","nbJets","met","metSig","mettrack","mettrack_phi","mT2"]},        
        {"type":"SR_no_meffcut","var":["meffincl"]},
        {"type":"SR_no_dphicut","var":["dphi"]},
        {"type":"SR_no_JetpT1cut","var":["jetpT1"]},
        {"type":"SR_no_JetpT2cut","var":["jetpT2"]},
        {"type":"SR_no_JetpT3cut","var":["jetpT3"]},
        {"type":"SR_no_JetpT4cut","var":["jetpT4"]},
        {"type":"SR_no_Apcut","var":["Ap"]},
        {"type":"SR_no_metomeffcut","var":["metomeff2jet","metomeff4jet","met","meffincl"]},
        ]

kindOfCuts_CRWT=[
        {"type":"CRW_no_meffcut","var":["meffincl"]},
        #{"type":"CRW_no_Apcut","var":["Ap"]},
        {"type":"CRW","var":["nJets",'nJets60all',"nbJets","dphi","met","metSig","metomeff2jet","metomeff4jet","lep1Pt","lep1Eta","lep1Phi","lep1sign","mt","Wpt","Ap","mettrack","mettrack_phi","mT2"]},
        {"type":"CRT_no_meffcut","var":["meffincl"]},
        #{"type":"CRT_no_Apcut","var":["Ap"]},
        {"type":"CRT","var":["nJets","nbJets","dphi","met","metSig","metomeff2jet","metomeff4jet","lep1Pt","lep1Eta","lep1Phi","lep1sign","mt","Wpt","Ap","mettrack","mettrack_phi","mT2"]},
        ]

kindOfCuts_CRY=[
        {"type":"CRY_no_meffcut","var":["meffincl"]},
        {"type":"CRY","var":["nJets",'nJets60all',"dphi","met","metSig","metomeff2jet","metomeff4jet","phPt","phEta","phPhi","phSignal","Ap","mettrack","mettrack_phi","origmet","origmetPhi"]},
        ]

kindOfCuts_CRZ=[
        {"type":"CRZ_no_meffcut","var":["meffincl"]},
        {"type":"CRZ","var":["nJets",'nJets60all',"dphi","met","metSig","metomeff2jet","metomeff4jet","lep1Pt", "lep2Pt", "lep1Eta", "lep2Eta", "lep1Phi", "lep2Phi","lep1sign","lep2sign","llsign","mll","Zpt"]},
        ]

if doCRY:
        kindOfCuts=kindOfCuts_CRY
elif doCRWT:
        kindOfCuts=kindOfCuts_CRWT
elif doCRZ:
        kindOfCuts=kindOfCuts_CRZ        
else:
        kindOfCuts=kindOfCuts_SR


anaImInterestedIn=['SR2jvl', 'SR2jvt', 'SR4jAp']#, 'SR2jMoriond','SR5jMoriond', 

mc = [  
	{'key':'Zjets','name':'Z+jets','ds':'lZjets','redoNormWeight':'redoNormWeight',
         'color':ROOT.kBlue+3,'inputdir':mcdir+'ZMassiveCB.root','veto':1,'treePrefix':'Z_',
         'syst':commonsyst},
        {'key':'Top','name':'t#bar{t}(+X) & single top','ds':'lTop','redoNormWeight':'redoNormWeight',
         'color':ROOT.kGreen-9,'inputdir':mcdir+('Top.root' if doRun2 else 'TopP2011C_rwgt.root'),
         'treePrefix':'Top_','syst':commonsyst},
        {'key':'Wjets','name':'W+jets','ds':'lWjets','redoNormWeight':'redoNormWeight',
         'color':ROOT.kAzure-4,'inputdir':mcdir+'WMassiveCB.root','veto':1,'treePrefix':'W_',
         'syst':commonsyst},
        ]

if doCRY:
        mc.append({'key':'Yjets','name':'#gamma+jets','ds':'lYjets','redoNormWeight':'redoNormWeight', 'color':ROOT.kYellow,'inputdir':mcdir+'GAMMAMassiveCB.root','veto':1,'treePrefix':'GAMMA_','syst':commonsyst})

signalPoint=[
        {'name':'GG_direct_1350_0','filename':mcdir+'GG_direct.root',
         'color':ROOT.kMagenta,
         'linestyle': 7,
         'sigplotname':'#tilde{g}#tilde{g} direct, m(#tilde{g}, #tilde{#chi^{1}_{0}})=(1350, 0)',
         'sigSR':['SR5jMoriond','SR4jAp','SR2jvt'],
         },
        {'name':'GG_direct_1050_600','filename':mcdir+'GG_direct.root',
         'color':ROOT.kOrange+7,
         'linestyle': 3,
         'sigplotname':'#tilde{g}#tilde{g} direct, m(#tilde{g}, #tilde{#chi^{1}_{0}})=(1050, 600)',
         'sigSR':['SR5jMoriond','SR4jAp','SR2jvt'],      
         },
        {'name':'SS_direct_900_0','filename':mcdir+'SS_direct.root',
         'color':ROOT.kMagenta,
         'linestyle': 7,
         'sigplotname':'#tilde{q}#tilde{q} direct, m(#tilde{q}, #tilde{#chi^{1}_{0}})=(900, 0)',
         'sigSR':['SR2jMoriond'],#,'SR2jvt'], v34
         },
        {'name':'SS_direct_700_400','filename':mcdir+'SS_direct.root',
         'color':ROOT.kOrange+7,
         'linestyle': 3,
         'sigplotname':'#tilde{q}#tilde{q} direct, m(#tilde{q}, #tilde{#chi^{1}_{0}})=(700, 400)',
         'sigSR':['SR2jMoriond'],#,'SR2jvt'], v34
         },
    ]


start_time = time.time()

if doSyst and doRun2 and version>30:
	systDict=[
		"_JET_GroupedNP_1_1up",
		"_JET_GroupedNP_2_1up",
		"_JET_GroupedNP_3_1up",
		"_JET_GroupedNP_1_1down",
		"_JET_GroupedNP_2_1down",
		"_JET_GroupedNP_3_1down",
		"_JER_1up",
		]
elif doSyst:
	systDict=[
#		"_PUup",
#		"_PUdown",
		"_JESUP",
		"_JESDOWN",
		"_JER",
		]
#         "_SCALESTUP",
#         "_SCALESTDOWN",
#         "_RESOST",
#         "_bTagBup",
#         "_bTagBdown",
#         "_bTagCup",
#         "_bTagCdown",
#         "_bTagLup",
#         "_bTagLdown",
#         "_GamWeightUP",
#         "_GamWeightDOWN",
#         "_mu1Up",
#         "_mu1Down",
#         "_mu2Up",
#         "_mu2Down",
#         "_ghi",
#         "_glo",
#         "_thi",
#         "_tlo",
#         ]
else:
	systDict=[]
def projAll(l,var,varname,title,cuts,syst,myNtHandler,nbinvar,minvar,maxvar,output):                
        print '------------------------- projAll',title,varname,nbinvar,minvar,maxvar
	#print 'inprojall ',myNtHandler.printAll()
        myHisto=ROOT.TH1F(title,varname,nbinvar,minvar,maxvar)
        myHisto.SetFillColor(myNtHandler.color)
        myNtHandler.project(l,title,var,cuts)
        #print 'in projall', title,myHisto.GetEntries(),myNtHandler.color
        output.put(myHisto)
        
class NtHandler:
        def __init__(self,name,filename,treename,basecuts,color,weights,dataormc,lumi):
                self.data=dataormc
                self.color=color
                self.weights=weights
                self.lumi=lumi
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
                print basecuts, self.tree.GetEntries()
                print self.tree.Draw('>>entryList'+name,basecuts,'entrylist')
                elist = ROOT.gDirectory.Get('entryList'+name)
                #print elist
                self.tree.SetEntryList(elist)
                print 'done,',name," ",elist.GetN(),' entries'
                #print 'time',time.time()-start_time
                return
        def printAll(self):
                print 'printall from nthandler',self.lumi,self.tree.GetName()
                return
        def project(self,l,histname,var,cuts):
                weight=str(self.weights)+"*"+str(self.lumi)
                if self.data=="data":  weight="1"
                print 'histname',self.data,histname,"weight",weight,"var",var,cuts
                self.tree.Project(histname,var,"("+cuts+")*("+weight+")")
                print 'time Project',time.time()-start_time


def main(configMain):
        for whichKind in kindOfCuts:
#                print 'whichKind',whichKind['type']

                allChannel = allChannelsDict
                
                #----------------------------------------------------------
                # SR2j preselection
                #----------------------------------------------------------
                anaSR2jvl=ChannelConfig("SR2jvl",regionDict)
                anaSR2jvl.nJet=2
                anaSR2jvl.dPhi=0.4
                anaSR2jvl.dPhiR=0.2
                anaSR2jvl.met_over_meffNj=0.0
                anaSR2jvl.meff=400*1000
                allChannelsDict[anaSR2jvl.name]=anaSR2jvl
                allAna = allChannelsDict.keys()

                #allChannelsDict={}
                #allChannelsDict[anaSR6jl.name]=anaSR6jl
                #anaSR6jl.Print()
                
                allRegion = regionDict.keys()
                onlyExtraWeights=False
                
                for ana in allAna: 
                        if ana in anaImInterestedIn:                  
                                for region  in allRegion:
                                        config=ChannelConfig(ana,region)
#                                        print ana,region,whichKind
                                        if (whichKind['type'] in region) or ("SR" in region and "SR" in whichKind['type']) or ("CRW" in region and "CRW" in whichKind['type']) or ("CRT" in region and "CRT" in whichKind['type']) or ("CRY" in region and "CRY" in whichKind['type']) or ("CRZ" in region and "CRZ" in whichKind['type']):
                                                #print 'going to run', whichKind['type']
                                                ch=allChannelsDict[ana]
                                                ch.setWithoutMeffCut(False)
                                                ch.setWithoutMetOverMeffCut(False)
                                                ch.setWithoutdPhiCut(False)
                                                ch.setWithoutApCut(False)
                                                ch.setWithoutJetpT1Cut(False)
                                                ch.setWithoutJetpT2Cut(False)
                                                ch.setWithoutJetpT3Cut(False)
                                                ch.setWithoutJetpT4Cut(False)
                                                if("no_meffcut" in whichKind['type']):
                                                        ch.setWithoutMeffCut(True)
                                                        #print 'setting nomeffcut!!' 
                                                if("no_metomeffcut" in whichKind['type']):
                                                        ch.setWithoutMetOverMeffCut(True)
                                                        #print 'setting nometovermeffcut!!' 
                                                if("no_dphicut" in whichKind['type']):
                                                        ch.setWithoutdPhiCut(True)
                                                        #print 'setting nodphicut!!'
                                                if("no_Apcut" in whichKind['type']):
                                                        ch.setWithoutApCut(True)
                                                        #print 'setting noApcut!!'
                                                if("no_JetpT1cut" in whichKind['type']):
                                                        ch.setWithoutJetpT1Cut(True)
                                                if("no_JetpT2cut" in whichKind['type']):
                                                        ch.setWithoutJetpT2Cut(True)
                                                        #print 'setting noJetpT2cut!!'
                                                if("no_JetpT3cut" in whichKind['type']):
                                                        ch.setWithoutJetpT3Cut(True)
                                                        #print 'setting noJetpT3cut!!'
                                                if("no_JetpT4cut" in whichKind['type']):
                                                        ch.setWithoutJetpT4Cut(True)
                                                        #print 'setting noJetpT4cut!!'
                                                cuts=ch.getCuts(region)
                                                print "channel",cuts
						
                                                weights=allChannelsDict[ana].getWeights(region,onlyExtraWeights)
                                                #print ana, region, cuts,weights,"remove pileupweights"
                                                for varinList in varList:
                                                        if varinList['varName'] in whichKind['var'] or 'all' in whichKind['var']:
                                                                if 'extracuts' in varinList:
                                                                        temp="(("+cuts+")&&("+varinList['extracuts']+"))"
                                                                        cuts=temp
                                                                print 'adding extracuts for var',varinList['varName'],cuts
                                                               #print "Create variable", varinList['varName'], ' for this cut:', whichKind['type'] 
                                                                varname=varinList['varName']
                                                                plotname=varinList['plotName']
                                                                var=varinList['varNtuple']
                                                                nbinvar=int(varinList['nbinvar'])
                                                                minvar=float(varinList['minvar'])
                                                                maxvar=float(varinList['maxvar'])
                                                                unit=varinList['unit']
                                                                
                                                                plotData=[]
                                                                if runData:
                                                                        for wData in datafile:
                                                                                if (wData['whichdata'] in region) or ("SR" in region and "SR" in wData['whichdata']):
                                                                                        print 'nthandler data',wData['whichdata']
                                                                                        nt=NtHandler(ana+region+"data_baseline",wData['filename'],wData['dataname'],cuts,ROOT.kBlack,1.,"data",configMain.lumi)
                                                                                        plotData.append(nt)


                                                                plotSignalList=[]
                                                                signalHistos=[]
                                                                nameSignalHistos=[]
                                                                if runSignal:
                                                                        for point in signalPoint:
                                                                                for sigSR in point['sigSR']:
                                                                                        if sigSR==ana or sigSR=='all':
                                                                                                tmptreename="_SRAll"
                                                                                                if doCRY:
                                                                                                        tmptreename="_CRY"
                                                                                                elif doCRWT:
                                                                                                        tmptreename="_CRWT"
                                                                                                elif doCRZ:
                                                                                                        tmptreename="_CRZ"
                                                                                                ntsig=NtHandler(ana+region+point['name']+tmptreename,point['filename'],point['name']+tmptreename,cuts,point['color'],weights,"signal",configMain.lumi)
                                                                                                plotSignalList.append(ntsig)
                                                                                                print 'signal point',point['name']
                                                                                                signalHisto=ROOT.TH1F(varname+point['name']+tmptreename+ana+region,varname,nbinvar,minvar,maxvar)
                                                                                                ntsig.project(1.,varname+point['name']+tmptreename+ana+region,var,cuts)
                                                                                                signalHisto.SetLineColor(point['color'])
                                                                                                signalHisto.SetLineStyle(point['linestyle'])
                                                                                                signalHisto.SetLineWidth(2)
                                                                                                signalHistos.append(signalHisto)           
                                                                                                nameSignalHistos.append(point['sigplotname'])

                                                                fullPlotMC=[]
                                                                fullPlotMCSyst=[]
                                                                
                                                                jobs=[]
                                                                output=Queue()
                                                                for process in mc:
                                                                        mcname=process['treePrefix']+"SRAll"
                                                                        if doCRWT: mcname=process['treePrefix']+"CRWT"
                                                                        if doCRY: mcname=process['treePrefix']+"CRY"
                                                                        if doCRZ: mcname=process['treePrefix']+"CRZ" 
                                                                        ntmc=NtHandler(ana+region+process['treePrefix']+"_baseline",process['inputdir'],mcname,cuts,process['color'],weights,"mc",configMain.lumi)
                                                                        
                                                                        fullPlotMC.append(mcname)
									#print 'process in mc', mcname
                                                                        p=Process(target=projAll,args=(1,var,varname,varname+process['treePrefix']+ana+region+"",cuts,"",ntmc,nbinvar,minvar,maxvar,output,))
                                                                        jobs.append(p)


                                                                        for syst in systDict:
                                                                                mcname=process['treePrefix']+"SRAll"+syst
                                                                                if doCRWT: mcname=process['treePrefix']+"CRWT"+syst
                                                                                if doCRY: mcname=process['treePrefix']+"CRY"+syst
                                                                                if doCRZ: mcname=process['treePrefix']+"CRZ"+syst
                                                                                
                                                                                ntsyst=NtHandler(ana+region+process['treePrefix']+"_baseline"+syst,process['inputdir'],mcname,cuts,process['color'],weights,"mc",configMain.lumi)
                                                                                fullPlotMCSyst.append(ntsyst)
                                                                                p=Process(target=projAll,args=(1,var,varname,varname+process['treePrefix']+ana+region+syst,cuts,syst,ntsyst,nbinvar,minvar,maxvar,output,))
                                                                                jobs.append(p)

                                                                for j in jobs:
                                                                        j.start()
                                                                        print 'START',j                                    
                                        # Wait for all of them to finish
                                                                for j in jobs:
                                                                        j.join()
                                                                mcHisto=[]
                                                                mcSystHisto=[]
                                                                for j in jobs:
                                                                        print 'GET OUTPUT',j
                                                                        j.result_queue=output
                                                                        histo=output.get()
                                                                        clone=histo.Clone()
                                                                        lock_sys=0
                                                                        for sys in systDict:
                                                                                if sys in histo.GetName(): 
                                                                                        lock_sys=1
                                                                                #print 'loop over sys',sys,lock_sys,histo.GetName()
                                                                        if lock_sys == 0:
                                                                                mcHisto.append(clone)
                                                                        else:
                                                                                mcSystHisto.append(clone)
                                                                
								#print 'before terminate'
                                                                for j in jobs:
                                                                        j.terminate()
                                                                output.close()
                                                                output.join_thread()

                                                                lock=1    
                                                                
                                                                canvas = ROOT.TCanvas(" "," ",10,32,668,643)
                                                                canvas.SetFrameFillColor(kWhite)
                                                                canvas.SetLogy(ROOT.kTRUE)
                                                                if(runData or len(systDict)>0 or doSignificance ):
                                                                        upperPad = ROOT.TPad("upperPad", "upperPad", .001, .15, .995, .995)
                                                                        lowerPad = ROOT.TPad("lowerPad", "lowerPad", .001, .001, .995, .27)
                                                                        rootOpt.setUpPads("_logy",upperPad,lowerPad)
                                                                        upperPad.cd()
  
                                                                if(runData):
                                                                        print 'new data plot',varname+"data"+ana+region,varname,nbinvar,minvar,maxvar
                                                                        dataHisto=ROOT.TH1F(varname+"data"+ana+region,varname,nbinvar,minvar,maxvar)
                                                                        dataHisto.GetXaxis().SetTitle(plotname)
                                                                        lock=1
                                                                        for plot in plotData:
                                                                                plot.project(lock,varname+"data"+ana+region,var,cuts)
                                                                                #print 'verification des data',dataHisto.GetEntries()
                                                                        
                                                                       # upperPad = ROOT.TPad("upperPad", "upperPad", .001, .15, .995, .995)
                                                                       # lowerPad = ROOT.TPad("lowerPad", "lowerPad", .001, .001, .995, .27)
                                                                       # rootOpt.setUpPads("_logy",upperPad,lowerPad)

                                                                       # upperPad.cd()
                                                                        datah_Poiss = ROOT.TGraphAsymmErrors(dataHisto.GetNbinsX())
                                                                        datah_Poiss.SetMarkerStyle(20)
                                                                        datah_Poiss.SetMarkerSize(1.2)
                                                                        datah_Poiss.SetMarkerColor(kBlack)
                                                                        datah_Poiss.SetLineColor(kBlack)
                                                                        datah_Poiss.SetLineWidth(3)
                                                                        setAsymmErrors(dataHisto,datah_Poiss)
                                                                        
                                                                        dataClone = ROOT.TGraphAsymmErrors(dataHisto.GetNbinsX())
                                                                        dataClone.SetMarkerStyle(20)
                                                                        dataClone.SetMarkerSize(1.5) 
                                                                        dataClone.SetLineWidth(5)
                                                                        dataClone.SetMarkerColor(kWhite)
                                                                        dataClone.SetLineColor(kWhite)
                                                                        setAsymmErrors(dataHisto,dataClone)
                                                                        min = 0.25
                                                                        max = dataHisto.GetMaximum()  
                                                                        if (max <= 2.) :  min = 0.02   
                                                                        yfactor=4
                                                                        dataHisto.GetYaxis().SetRangeUser(min,max*yfactor)
                                                                        datah_Poiss.GetYaxis().SetRangeUser(min,max*yfactor)
                                                                        
                                                                        binWidth=dataHisto.GetBinWidth(1)
                                                                        XUnit="events / "+str(binWidth)
                                                                        if(unit): XUnit=XUnit+" "+unit
                                                                        dataHisto.GetYaxis().SetTitle(XUnit)
                                                                        dataHisto.GetYaxis().SetLabelSize(0.05)
                                                                        dataHisto.GetYaxis().SetTitleSize(0.05)
                                                                        dataHisto.GetYaxis().SetTitleOffset(1.4)
                                                                        dataHisto.GetYaxis().SetTitleFont(42)
                                                                        
                                                                        dataHisto.Draw("hist")
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
                                                                        #print 'loop over mc', whichmc
                                                                        for h in mcHisto:
                                                                                #print 'loop over histo',h
                                                                                if whichmc['treePrefix'] in h.GetName():
                                                                                        #print 'histo found', h.GetName(),h.Integral()
                                                                                        clone=h.Clone()
                                                                                        Clone_mcHisto.append(clone)
                                                                                        mcStack.Add(clone)
                                                                                        mcTotal.Add(clone)
                                                                                        binWidth=clone.GetBinWidth(1) if varname.find("Jets")<0 else int(clone.GetBinWidth(1))
                                                                                        XUnitStack="events / "+str(binWidth)+" "+unit
                                                                                        
                                                                #print 'xunit',XUnitStack

                                                                sumSystHist=[]
                                                                for isyst in systDict:
#                                                                       tempHist=mcSystHisto[0]
#									tempHist.Clear()
                                                                        tempHist=ROOT.TH1D("tempHist","tempHist",mcSystHisto[0].GetNbinsX(),mcSystHisto[0].GetXaxis().GetXmin(),mcSystHisto[0].GetXaxis().GetXmax())
                                                                        tempHist.Print()
                                                                        print 'init',tempHist.GetBinContent(8)
                                                                        for h in mcSystHisto:
                                                                                if isyst in h.GetName():        
                                                                                        tempHist.Add(h)
                                                                        #print 'getName',h.GetName(),h.GetBinContent(8),tempHist.GetBinContent(8)
                                                                        sumSystHist.append(tempHist)
                                                                        #print 'getname add',isyst,tempHist.GetBinContent(8)
								#print 'before doing anything number of sumsysthist',len(sumSystHist)
                                                                if(runData):
                                                                        mcStack.Draw("same:hist")
                                                                        mcTotal.Draw("hist:same")
                                                                        dataClone.Draw("p:e:same")
                                                                        datah_Poiss.Draw("p:e:same")
                                                                        if(runSignal):
                                                                                for hsig in signalHistos:
                                                                                        hsig.Draw("hist:same")  
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
								#mcTotal_Poiss.Draw("e2:same")
                                                                       	maxsig = -1.
                                                                       	if(runSignal):
                                                                       	            for hsig in signalHistos:
                                                                       	                hsig.Draw("hist:same")
                                                                       	                maxsig = TMath.Max(maxsig, hsig.GetMaximum())
                                                                       	min = 0.25
                                                                       	maxbkg = mcStack.GetMaximum()
                                                                       	max = TMath.Max(maxbkg, maxsig)
                                                                       	if (max <= 2.) :  min = 0.02   
                                                                       	yfactor=4
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

                                                                arrow=-1
                                                                SpecialArrow=""
                                                                if varname.find("meffincl")>=0 and whichKind['type'].find("no_meffcut")>=0:
                                                                        varcut=ch.returnMeffCut()/1000.
                                                                        SpecialArrow=plotname+">"+str(int(varcut))
                                                                        arrow=1
                                                                if varname.find("metomeff")>=0 and whichKind['type'].find("no_metomeffcut")>=0:
                                                                        varcut=ch.returnMetOverMeffCut()
                                                                        SpecialArrow=plotname+">"+str((varcut))
                                                                        arrow=1
                                                                if varname.find("dphi")>=0 and whichKind['type'].find("no_dphicut")>=0:
                                                                        varcut=ch.returndPhiCut()
                                                                        SpecialArrow=plotname+">"+str((varcut))
                                                                        arrow=1
                                                                if varname.find("Ap")>=0 and whichKind['type'].find("no_Apcut")>=0:
                                                                        varcut=ch.returnApCut()
                                                                        SpecialArrow=plotname+">"+str((varcut))
                                                                        arrow=1
                                                                if varname.find("jetpT1")>=0 and whichKind['type'].find("no_JetpT1cut")>=0:
                                                                        varcut=ch.returnJetpT1Cut()/1000. 
                                                                        SpecialArrow=plotname+">"+str((varcut))
                                                                        arrow=1
                                                                if varname.find("jetpT2")>=0 and whichKind['type'].find("no_JetpT2cut")>=0:
                                                                        varcut=ch.returnJetpT2Cut()/1000. 
                                                                        SpecialArrow=plotname+">"+str((varcut))
                                                                        arrow=1
                                                                if varname.find("jetpT3")>=0 and whichKind['type'].find("no_JetpT3cut")>=0:
                                                                        varcut=ch.returnJetpT3Cut()/1000. 
                                                                        SpecialArrow=plotname+">"+str((varcut))
                                                                        arrow=1
                                                                        
                                                                if varname.find("jetpT4")>=0 and whichKind['type'].find("no_JetpT4cut")>=0:
                                                                        varcut=ch.returnJetpT4Cut()/1000. 
                                                                        SpecialArrow=plotname+">"+str((varcut))
                                                                        arrow=1
                                                                        
                                                                if arrow>0:
                                                                        #ar=TArrow(varcut,mcStack.GetMinimum(),varcut,1.0 if not whichKind['type'].find("baseline")>=0 else 100,0.05,"<")
                                                                        ar=TArrow(varcut,mcStack.GetMinimum(),varcut, 1.0 if not whichKind['type'].find("baseline")>=0 else 100, 0.05,"<")
                                                                        ar.SetLineWidth(3)
                                                                        ar.SetLineColor(TColor.kRed+1)
                                                                        ar.SetFillColor(TColor.kRed+1)
                                                                        ar.Draw("")
                                                                        
                                                                forPlotMcHisto=mcHisto[0]
                                                                cHisto=0
                                                                for h in mcHisto:
                                                                        if cHisto>0: forPlotMcHisto.Add(h)
                                                                        cHisto=cHisto+1
								#print 'forplotMcHisto has a sum of ', cHisto, 'components'
                                                                text=ROOT.TLatex()
                                                                if(runData):
                                                                        PrintText(dataHisto.GetName(),text)

                                                                atlaslabel=ROOT.TLatex(0.2,0.89,"#bf{#it{ATLAS}} Simulation Internal") 
                                                                atlaslabel.SetNDC()
                                                                atlaslabel.SetTextSize(0.03)
                                                                atlaslabel.SetTextFont(42)
                                                                atlaslabel.Draw("same")

                                                                lumilabel=ROOT.TLatex(0.2,0.835,("#int L dt = ")+str(int(float(configMain.lumi)*0.001))+" fb^{-1} #sqrt{s}=13 TeV")                                                 #               lumilabel=ROOT.TLatex(0.42,0.89,("MC simulation (#sqrt{s}=13 TeV) #int L dt = ")+str(" %d" % str(configMain.lumi*0.001) )+" fb^{-1}") 
                                                                lumilabel.SetNDC()
                                                                lumilabel.SetTextSize(0.03)
                                                                lumilabel.SetTextFont(42)
                                                                lumilabel.Draw("same")

                                                                tobewritten=(whichKind['type']+" for " if whichKind['type'].find("CR")>=0 else "") +ana + ((", "+SpecialArrow+" "+unit) if whichKind['type'].find("SR_no")>=0  else "")
                                                                analabel=ROOT.TLatex(0.59, 0.89, (tobewritten))
                                                                analabel.SetNDC()
                                                                analabel.SetTextSize(0.03)
                                                                analabel.SetTextFont(42)
                                                                analabel.Draw("same")          

                                                                legend=ROOT.TLegend(0.59,0.66,0.82,0.87)
                                                                if(runData):
                                                                        legend.AddEntry(dataHisto,"Data 2012 (#sqrt{s} = 8 TeV)","p")
                                                                legend.AddEntry(mcTotal,"SM Total","l")    
                                                                legend.SetTextSize(0.025)
                                                                legend.SetFillColor(0)
                                                                legend.SetFillStyle(0) 
                                                                legend.SetBorderSize(0)

                                                                if(runData):
                                                                        legend.AddEntry(dataHisto,"Data 2012 (#sqrt{s} = 8 TeV)","p")
                                                                if(runSignal):
                                                                        isig=0
                                                                        for hsig in signalHistos:
                                                                                legend.AddEntry(hsig,nameSignalHistos[isig],"l")
                                                                                isig+=1
                                                                for whichmc in mc:
                                                                        for h in mcHisto:
                                                                                if whichmc['treePrefix'] in h.GetName():
                                                                                        legend.AddEntry(h,whichmc['name'],"f")


                                                                legend.SetLineColor(10)
                                                                legend.SetFillColor(10)
                                                                legend.Draw()
								
								#Allsys_band=ROOT.TGraphAsymmErrors(dataHisto.GetNbinsX())
								#Allsys_plusTheory_band=ROOT.TGraphAsymmErrors(dataHisto.GetNbinsX())
								#Allsys_band.SetFillColor(kYellow)
								#Allsys_plusTheory_band.SetFillColor(kGreen)
								#if(len(mcSystHisto)>0):
								#		estimSyst(forPlotMcHisto,sumSystHist,Allsys_band,Allsys_plusTheory_band)

                                                                if(runData or len(mcSystHisto)>0 or doSignificance):
                                                                       	lowerPad.cd()
                                                                       	if(runData):
                                                                       	        ratio=ROOT.TGraphAsymmErrors(dataHisto.GetNbinsX())
                                                                       	        Allsys_band=ROOT.TGraphAsymmErrors(dataHisto.GetNbinsX())
										#Allsys_plusTheory_band=ROOT.TGraphAsymmErrors(dataHisto.GetNbinsX())
                                                                       	        skeletonRatio=ROOT.TH1D("skeleton","skeleton",dataHisto.GetNbinsX(),dataHisto.GetXaxis().GetXmin(),dataHisto.GetXaxis().GetXmax())
                                                                       	        Redline=ROOT.TLine(dataHisto.GetXaxis().GetXmin(),1,dataHisto.GetXaxis().GetXmax(),1)
                                                                       	        skeletonRatio.GetXaxis().SetTitle(dataHisto.GetXaxis().GetTitle())
                                                                       	elif doSyst:
                                                                       	        ratio=ROOT.TGraphAsymmErrors(forPlotMcHisto.GetNbinsX())
                                                                       	        Allsys_band=ROOT.TGraphAsymmErrors(forPlotMcHisto.GetNbinsX())
										#Allsys_plusTheory_band=ROOT.TGraphAsymmErrors(forPlotMcHisto.GetNbinsX())
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
                                                                       	estimSyst(forPlotMcHisto,sumSystHist,Allsys_band)
                                                                       	if(runData):
                                                                       	        GetDataMCRatio(dataHisto,forPlotMcHisto,ratio)
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

                                                                       	skeletonRatio.GetXaxis().SetLabelSize(0.11)
                                                                       	skeletonRatio.GetXaxis().SetTitleSize(0.13)
                                                                        
                                                                       	skeletonRatio.GetXaxis().SetTitleOffset(1)
                                                                       	skeletonRatio.GetYaxis().SetLabelSize(0.11)
                                                                       	skeletonRatio.GetYaxis().SetTitleSize(0.15)
                                                                       	skeletonRatio.GetYaxis().SetTitleOffset(0.48)
                                                                       	skeletonRatio.GetYaxis().SetRangeUser(0,2.8)
                                                                       	if runData :
                                                                       	        skeletonRatio.GetYaxis().SetTitle("DATA / MC")
                                                                       	elif doSignificance:
                                                                       	        skeletonRatio.GetYaxis().SetTitle("Significance")
                                                                       	        skeletonRatio.GetYaxis().SetRangeUser(0,6.)
                                                                       	else:
                                                                       	        skeletonRatio.GetYaxis().SetTitle("MC syst")

                                                                       	Redline.SetLineColor(2)
                                                                       	Redline.SetLineStyle(2)
                                                                       	Redline.SetLineWidth(2)
                                                                        
                                                                       	skeletonRatio.Draw()
                                                                        #Allsys_plusTheory_band.Draw("2 same")
                                                                       	if doSyst:
                                                                       	        Allsys_band.Draw("2 same")
                                                                       	elif doSignificance:
										#print 'on est la'
                                                                       	        for s in sigRatios:
                                                                       	                s.Draw("2 same")
                                                                       	ratio.Draw("same:p:e")
                                                                       	if not doSignificance:
                                                                       	        Redline.Draw("same")  
                                                                       	lowerPad.RedrawAxis("same") 
                                                


                                                                canvas.SaveAs("Outplots/v"+str(version)+str('/intL%0difb' % (float(configMain.lumi)/1000.))+"_"+region+"_"+ana+"_"+varname+"_"+whichKind['type']+".pdf")
                                                                        
#    if(saveToFile):
#        myTFile=ROOT.TFile("plots/mytfile.root","RECREATE")
#        for histo in dataHistos:
#            histo.Write()
#        for histo in mcHistos:
#            histo.Write()
#        myTFile.Write()

def parseCmdLine(args):
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--lumi", dest="lumi", help="lumi", default=3000.)
    (config, args) = parser.parse_args(args)
    return config


if __name__ == "__main__":
        config = parseCmdLine(sys.argv[1:])
        main(config)
