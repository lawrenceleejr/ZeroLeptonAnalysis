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
from math import sqrt,pow
from ChannelConfig import *
from ChannelsDict import *

do4jt=True
do2jt=False
doApMeffEx=False
doBosonBaselineSample=True

version=51
if not doBosonBaselineSample:
	versionname = '51_alternative'
else:
	versionname = '51_baseline'

varList = [
        {'varName':'meffincl','varNtuple':'meffInc','plotName':'m_{eff}(incl.)','nbinvar':'21','minvar':'0','maxvar':'2100.','unit':'GeV'},
        {'varName':'met','varNtuple':'met','plotName':'E_{T}^{miss}','nbinvar':'20','minvar':'0','maxvar':'1000.','unit':'GeV'},
        {'varName':'metSig','varNtuple':'met/sqrt(meffInc-met)','plotName':'E_{T}^{miss}/#sqrt{H_{T}}','nbinvar':'25','minvar':'0','maxvar':'50','unit':'#sqrt{GeV}'}, 
        {'varName':'metomeff','varNtuple':'met/meffInc','plotName':'E_{T}^{miss}/m_{eff}(incl.)','nbinvar':'24','minvar':'0','maxvar':'1.2','unit':''},
        {'varName':'metomeff2jet','varNtuple':'met/(met+jetPt[0]+jetPt[1])','plotName':'E_{T}^{miss}/m_{eff}(N_{jets})','nbinvar':'24','minvar':'0','maxvar':'1.2','unit':''},
        {'varName':'metomeff3jet','varNtuple':'met/(met+jetPt[0]+jetPt[1]+jetPt[2])','plotName':'E_{T}^{miss}/m_{eff}(N_{jets})','nbinvar':'24','minvar':'0','maxvar':'1.2','unit':''},
        {'varName':'metomeff4jet','varNtuple':'met/(met+jetPt[0]+jetPt[1]+jetPt[2]+jetPt[3])','plotName':'E_{T}^{miss}/m_{eff}(N_{jets})','nbinvar':'24','minvar':'0','maxvar':'1.2','unit':''},
        {'varName':'metomeff5jet','varNtuple':'met/(met+jetPt[0]+jetPt[1]+jetPt[2]+jetPt[3]+jetPt[4])','plotName':'E_{T}^{miss}/m_{eff}(N_{jets})','nbinvar':'24','minvar':'0','maxvar':'1.2','unit':''},
        {'varName':'meff2jet','varNtuple':'met+jetPt[0]+jetPt[1]','plotName':'m_{eff}(2j)','nbinvar':'50','minvar':'0','maxvar':'5000.','unit':'GeV'},
        {'varName':'dphi','varNtuple':'dPhi','plotName':'min(#Delta#phi(E_{T}^{miss},jet_{1,2,3}))','nbinvar':'40','minvar':'0','maxvar':'4.0','unit':''},
        {'varName':'nJets','varNtuple':'nJet', 'plotName': 'N_{jets} (p_{T}>40 GeV, |#eta|<2.8)', 'nbinvar':'15','minvar':'0','maxvar':'15','unit':''},
        {'varName':'nJets60all','varNtuple':'nJet', 'plotName': 'N_{jets} (all jets with p_{T}>60 GeV, |#eta|<2.8)', 'nbinvar':'15','minvar':'0','maxvar':'15','unit':'', 'extracuts':'(jetPt[nJet-1]>60.)'},    
        {'varName':'nbJets','varNtuple':'nBJet', 'plotName': 'N_{bjets} (p_{T}>40 GeV, |#eta|<2.5)', 'nbinvar':'15','minvar':'0','maxvar':'15','unit':''},
        {'varName':'jetpT1','varNtuple':'jetPt[0]', 'plotName': 'p_{T}(jet_{1})', 'nbinvar':'40','minvar':'0','maxvar':'2000','unit':'GeV'},
        {'varName':'jetpT2','varNtuple':'jetPt[1]', 'plotName': 'p_{T}(jet_{2})', 'nbinvar':'40','minvar':'0','maxvar':'2000','unit':'GeV'},
        {'varName':'jetpT3','varNtuple':'jetPt[2]', 'plotName': 'p_{T}(jet_{3})', 'nbinvar':'40','minvar':'0','maxvar':'1000','unit':'GeV'},
        {'varName':'jetpT4','varNtuple':'jetPt[3]', 'plotName': 'p_{T}(jet_{4})', 'nbinvar':'40','minvar':'0','maxvar':'1000','unit':'GeV'},
        {'varName':'jetpT5','varNtuple':'jetPt[4]', 'plotName': 'p_{T}(jet_{5})', 'nbinvar':'20','minvar':'0','maxvar':'500','unit':'GeV'},
        {'varName':'jetpT6','varNtuple':'jetPt[5]', 'plotName': 'p_{T}(jet_{6})', 'nbinvar':'20','minvar':'0','maxvar':'500','unit':'GeV'},
        {'varName':'mDR','varNtuple':'mdeltaR', 'plotName':'m^{#Delta}_{R}', 'nbinvar':'40','minvar':'0','maxvar':'2000.','unit':'GeV'},
        {'varName':'Ap','varNtuple':'Ap','nbinvar':'50','plotName':'Aplanarity', 'minvar':'0','maxvar':'0.5','unit':''},
        {'varName':'mT2', 'varNtuple':'mT2', 'plotName':'m_{T2}', 'nbinvar':'60','minvar':'0','maxvar':'3000.','unit':'GeV'},
        ## NOT FILLED {'varName':'mT2_noISR', 'varNtuple':'mT2_noISR/1000.', 'plotName':'m_{T2}(noISR)', 'nbinvar':'60','minvar':'0','maxvar':'3000.','unit':'GeV'},
        {'varName':"lep1Pt", 'varNtuple':"lep1Pt", 'plotName': 'p_{T}(lep_{1})', 'nbinvar':'25','minvar':'0','maxvar':'500','unit':'GeV'}, 
        {'varName':"lep1Eta", 'varNtuple':"lep1Eta", 'plotName': '#eta(lep_{1})', 'nbinvar':'40','minvar':'-4','maxvar':'4','unit':''},
        {'varName':"lep1Phi", 'varNtuple':"lep1Phi", 'plotName': '#phi(lep_{1})', 'nbinvar':'40','minvar':'-4','maxvar':'4','unit':''},
        {'varName':"lep1sign", 'varNtuple':"lep1sign", 'plotName': 'sign(lep_{1})', 'nbinvar':'5','minvar':'-2','maxvar':'3','unit':''},
        {'varName':"lep2Pt", 'varNtuple':"lep2Pt", 'plotName': 'p_{T}(lep_{1})', 'nbinvar':'50','minvar':'0','maxvar':'1000','unit':'GeV'}, 
        {'varName':"lep2Eta", 'varNtuple':"lep2Eta", 'plotName': '#eta(lep_{2})', 'nbinvar':'40','minvar':'-4','maxvar':'4','unit':''},
        {'varName':"lep2Phi", 'varNtuple':"lep2Phi", 'plotName': '#phi(lep_{2})', 'nbinvar':'40','minvar':'-4','maxvar':'4','unit':''},
        {'varName':"lep2sign", 'varNtuple':"lep2sign", 'plotName': 'sign(lep_{2})', 'nbinvar':'5','minvar':'-2','maxvar':'3','unit':''},
        {'varName':"llsign", 'varNtuple':"lep1sign*lep2sign", 'plotName': 'sign(lep_{1})#timessign(lep_{2})', 'nbinvar':'5','minvar':'-2','maxvar':'3','unit':''},
        {'varName':'mt', 'varNtuple':'mt', 'plotName':'m_{T}', 'nbinvar':'50','minvar':'20','maxvar':'120.','unit':'GeV'},
        {'varName':'Wpt', 'varNtuple':'Wpt', 'plotName':'p_{T}(W)', 'nbinvar':'25','minvar':'0','maxvar':'1000.','unit':'GeV'},
        {'varName':'mll', 'varNtuple':'mll', 'plotName':'m_{ll}', 'nbinvar':'50','minvar':'40','maxvar':'140.','unit':'GeV'},
        {'varName':'Zpt', 'varNtuple':'Zpt', 'plotName':'p_{T}(Z)', 'nbinvar':'50','minvar':'0','maxvar':'2000.','unit':'GeV'},        
        {'varName':'mettrack','varNtuple':'mettrack','plotName':'E_{T}^{miss,track}','nbinvar':'60','minvar':'0','maxvar':'3000.','unit':'GeV'},
        {'varName':"mettrack_phi", 'varNtuple':"mettrack_phi", 'plotName': '#phi(E_{T}^{miss,track})', 'nbinvar':'40','minvar':'-4','maxvar':'4','unit':''},
        {'varName':"phPt", 'varNtuple':"phPt", 'plotName': 'p_{T}(#gamma)', 'nbinvar':'50','minvar':'0','maxvar':'2000','unit':'GeV'}, 
        {'varName':"phEta", 'varNtuple':"phEta", 'plotName': '#eta(#gamma)', 'nbinvar':'20','minvar':'-4','maxvar':'4','unit':''},
        {'varName':"phPhi", 'varNtuple':"phPhi", 'plotName': '#phi(#gamma)', 'nbinvar':'20','minvar':'-4','maxvar':'4','unit':''},
        {'varName':"phSignal", 'varNtuple':"phSignal", 'plotName': 'is_#gammaSignal', 'nbinvar':'6','minvar':'-1','maxvar':'5','unit':''},  ## always 1
        {'varName':'origmet','varNtuple':'origmet','plotName':'E_{T}^{miss,orig}','nbinvar':'40','minvar':'0','maxvar':'2000.','unit':'GeV'},
        {'varName':"origmetPhi", 'varNtuple':"origmetPhi", 'plotName': '#phi(E_{T}^{miss,orig})', 'nbinvar':'40','minvar':'-1','maxvar':'7','unit':''},
]
mcdir ="root://eosatlas.cern.ch//eos/atlas/user/l/lduflot/atlasreadable/ZeroLeptonRun2-00-00-"+str(version)+"/filtered/"
commonsyst=" "  

if not doBosonBaselineSample:
	ZName = 'ZPowhegPythia'
	WName = 'WPowhegPythia'
else:
	ZName = 'ZMassiveCB'
	WName = 'WMassiveCB'
mc = [  
	{'key':'Diboson','name':'Diboson','ds':'lDiboson','redoNormWeight':'redoNormWeight',
	 'color':ROOT.kPink-4,'inputdir':mcdir+'DibosonMassiveCB.root','treePrefix':'Diboson_',
	 'syst':commonsyst},
	{'key':'Zjets','name':'Z+jets','ds':'lZjets','redoNormWeight':'redoNormWeight',
	 'color':ROOT.kBlue+3,'inputdir':mcdir+ZName+'.root','veto':1,'treePrefix':'Z_',
	 'syst':commonsyst},
        {'key':'Top','name':'t#bar{t}(+X) & single top','ds':'lTop','redoNormWeight':'redoNormWeight',
         'color':ROOT.kGreen-9,'inputdir':mcdir+('Top.root'),
         'treePrefix':'Top_','syst':commonsyst},
        {'key':'Wjets','name':'W+jets','ds':'lWjets','redoNormWeight':'redoNormWeight',
         'color':ROOT.kAzure-4,'inputdir':mcdir+WName+'.root','veto':1,'treePrefix':'W_',
         'syst':commonsyst},
        {'key':'QCDMC','name':'Multijet (MC)','ds':'lQCDMC','redoNormWeight':'redoNormWeight',
	 'color':ROOT.kOrange-4,'inputdir':mcdir+'QCD.root','treePrefix':'QCD_',
	 'syst':commonsyst},
	{'key':'Yjets','name':'#gamma+jets','ds':'lYjets','redoNormWeight':'redoNormWeight', 
	 'color':ROOT.kYellow,'inputdir':mcdir+'GAMMAMassiveCB.root','veto':1,'treePrefix':'GAMMA_','syst':commonsyst},
	]

RegionList =[
#        {'cuts':'CRZL',"key:Zjets","type":"CRL"}
        {'cuts':'SR',"key":"Zjets","type":"SR","pre":"SRAll"},
        {'cuts':'SRZVL',"key":"Zjets","type":"CRVL","pre":"SRAll"},
        {'cuts':'CRZVL',"key":"Zjets","type":"CRVL","pre":"CRZ"},
        {'cuts':'CRWL',"key":"Wjets","type":"CRL","pre":"VRWT"},
        {'cuts':'CRWVL',"key":"Wjets","type":"CRVL","pre":"VRWT"},
        {'cuts':'CRY',"key":"Yjets","type":"SR","pre":"CRY"},
        {'cuts':'CRYL',"key":"Yjets","type":"CRL","pre":"CRY"},
        ]
#print RegionList

start_time = time.time()
class Count:
        def __init__(self,name,filename,treename,basecuts,weights,dataormc,lumi):
                self.data=dataormc
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
def CalcError(denomi,Edenomi,nume,Enume):
    return sqrt(pow(Edenomi/denomi,2)+pow(Enume/nume,2))
    
def main(configMain):
    CountList=[]
    myChannelsDict ={}
    #setbaseline
    anaSR4jt=ChannelConfig(name="SR4jvt",regionDict=regionDict)
    anaSR4jt.nJets=4
    anaSR4jt.dPhi=0.4
    anaSR4jt.dPhiR=0.2
    anaSR4jt.MET = 200.
    anaSR4jt.jetpt1 = 130.
    anaSR4jt.jetpt2 = 50.
    anaSR4jt.jetpt3 = 50.
    anaSR4jt.jetpt4 = 50.
    anaSR4jt.MET_over_meffNj=0.2
    anaSR4jt.meffIncl=2200
    anaSR4jt.METsig = 0
    anaSR4jt.Ap = 0.04
    myChannelsDict[anaSR4jt.name]=anaSR4jt

    anaCRL4jt=ChannelConfig(name="CRL4jvt",regionDict=regionDict)
    anaCRL4jt.nJets=4
    anaCRL4jt.dPhi=0.4
    anaCRL4jt.dPhiR=0.2
    anaCRL4jt.MET = 440.
    anaCRL4jt.jetpt1 = 130.
    anaCRL4jt.jetpt2 = 50.
    anaCRL4jt.jetpt3 = 50.
    anaCRL4jt.jetpt4 = 50.
    anaCRL4jt.meffIncl=1200
    myChannelsDict[anaCRL4jt.name]=anaCRL4jt

    anaCRVL4jt=ChannelConfig(name="CRVL4jvt",regionDict=regionDict)
    anaCRVL4jt.nJets=4
    anaCRVL4jt.MET = 200.
    anaCRVL4jt.jetpt1 = 130.
    anaCRVL4jt.jetpt2 = 50.
    anaCRVL4jt.jetpt3 = 50.
    anaCRVL4jt.jetpt4 = 50.
    anaCRVL4jt.meffIncl=1200
    myChannelsDict[anaCRVL4jt.name]=anaCRVL4jt
    allAna = myChannelsDict.keys()
    onlyExtraWeights=False

    for region in RegionList:
        print region
        if("SR" in region["type"]) :
            ch=anaSR4jt
            ch.WithoutMeffCut = False
            ch.WithoutMetOverMeffCut = False
            ch.WithoutdPhiCut = False
            ch.WithoutApCut = False
            ch.WithoutJetpT1Cut = False
            ch.WithoutJetpT2Cut = False
            ch.WithoutJetpT3Cut = False
            ch.WithoutJetpT4Cut = False
            weights=ch.getWeights(region["cuts"],onlyExtraWeights)
            cuts=ch.getCuts(region["cuts"])
        if("CRL" in region["type"]) :
            ch=anaCRL4jt
            ch.WithoutMeffCut = False
            ch.WithoutMetOverMeffCut = True
            ch.WithoutdPhiCut = False
            ch.WithoutApCut = True
            ch.WithoutJetpT1Cut = False
            ch.WithoutJetpT2Cut = False
            ch.WithoutJetpT3Cut = False
            ch.WithoutJetpT4Cut = False
            weights=ch.getWeights(region["cuts"],onlyExtraWeights)
            cuts=ch.getCuts(region["cuts"])
            cuts="(("+cuts+")&&(meffInc < "+str(anaSR4jt.meffIncl)+"))"
        if("CRVL" in region["type"]) :
            ch=anaCRVL4jt
            ch.WithoutMeffCut = False
            ch.WithoutMetOverMeffCut = True
            ch.WithoutdPhiCut = True
            ch.WithoutApCut = True
            ch.WithoutJetpT1Cut = False
            ch.WithoutJetpT2Cut = False
            ch.WithoutJetpT3Cut = False
            ch.WithoutJetpT4Cut = False
            weights=ch.getWeights(region["cuts"],onlyExtraWeights)
            cuts=ch.getCuts(region["cuts"])
            cuts="(("+cuts+")&&(met < "+str(anaCRL4jt.MET)+"))"
        print "channel",cuts
        for each in mc:
            if(each["key"] in region["key"]):
                count=Count(region["cuts"], each['inputdir'], each["treePrefix"]+region["pre"],cuts,weights, "mc", configMain.lumi)
                tmphist=ROOT.TH1F(region["cuts"]+"meffInc","meffInc",1,0.,14000.)
                count.project(1.,region["cuts"]+"meffInc", "meffInc",cuts )
                value=tmphist.GetBinContent(1) 
                error=tmphist.GetBinError(1) 
                CountList.append({"region":region["cuts"],"value":value,"error":error})
                        
    print CountList
    for count in CountList:
        print count
        if ("SR" == count["region"]):
            SRcount = count
        if ("SRZVL" == count["region"]):
            SRZVLcount = count
        if ("CRZVL" == count["region"]):
            CRZVLcount = count
        if ("CRWL" == count["region"]):
            CRWLcount = count
        if ("CRWVL" == count["region"]):
            CRWVLcount = count
        if ("CRYL" == count["region"]):
            CRYLcount = count
        if ("CRY" == count["region"]):
            CRYcount = count
    CRYeff={"region":"effCRY","value":CRYcount["value"]/SRcount["value"],"error":CalcError(SRcount["value"], SRcount["error"], CRYcount["value"], CRYcount["error"],)} 
    CountList.append(CRYeff)
    CRYLeff={"region":"effCRYL","value":CRYLcount["value"]/SRcount["value"],"error":CalcError(SRcount["value"], SRcount["error"], CRYLcount["value"], CRYLcount["error"],)} 
    CountList.append(CRYLeff)
    CRWLeff={"region":"effCRWL","value":CRWLcount["value"]/CRYLcount["value"],"error":CalcError(CRYLcount["value"], CRYLcount["error"], CRWLcount["value"], CRWLcount["error"],)} 
    CountList.append(CRWLeff)
    CRZVLeff={"region":"effCRZVL","value":CRZVLcount["value"]/SRcount["value"],"error":CalcError(SRcount["value"], SRcount["error"], CRZVLcount["value"], CRZVLcount["error"],)} 
    CountList.append(CRZVLeff)
    CRZVLSF={"region":"SFCRZVL","value":CRZVLcount["value"]/SRZVLcount["value"],"error":CalcError(SRZVLcount["value"], SRZVLcount["error"], CRZVLcount["value"], CRZVLcount["error"],)} 
    CountList.append(CRZVLSF)
    print CountList
    f = open("4jt.dat","w")
    for count in CountList:
        f.write(count["region"]+" "+str(count["value"]) +" "+str(count["error"])+"\n" )

    f.close()

            


def parseCmdLine(args):
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--lumi", dest="lumi", help="lumi", default=3000.)
    (config, args) = parser.parse_args(args)
    return config

if __name__ == "__main__":
        config = parseCmdLine(sys.argv[1:])
        main(config)

