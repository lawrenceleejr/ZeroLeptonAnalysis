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
from ZLFitterConfig import *


zlFitterConfig = ZLFitterConfig() 
if not zlFitterConfig.datadriven:
    sys.exit()
domeffABCD=True
domeffABCD=zlFitterConfig.meffABCD
doAlternativeZ=False
doAlternativeW=False
doAlternativeY=False
doRun2=True
version=51
if doAlternativeZ:
	versionname = '51_alternativeZ'
elif doAlternativeW:
	versionname = '51_alternativeW'
else:
	versionname = '51_baseline'

gStyle=ROOT.gStyle
rootOpt=RootOption(gStyle)
rootOpt.setUpStyle()
gROOT.SetBatch(kTRUE)

mcdir ="/afs/cern.ch/atlas/groups/susy/0lepton/ZeroLeptonFitter/ZeroLepton-00-00-53_Light/"
mcgammadir="/afs/cern.ch/user/y/yamanaka/public/v02/"
if(doRun2):
	mcdir ="/afs/cern.ch/atlas/groups/susy/0lepton/ZeroLeptonFitter/ZeroLeptonRun2-00-00-"+str(version)+"/xAOD_13TeV/"
	mcdir='/afs/cern.ch/user/m/marijam/work/public/ZeroLeptonRun2-41/'
	mcdir='/afs/cern.ch/user/m/marijam/work/public/ZeroLeptonRun2-41-forEPS/'
	mcdir='/afs/cern.ch/user/m/marijam/work/public/ZeroLeptonRun2-43-forEPS/'
	mcdirqcd='/afs/cern.ch/user/m/marijam/work/public/ZeroLeptonRun2-44-forEPS/DataSUSY9_p2375_MCSUSY1_p2372/'
	mcdir ="root://eosatlas//eos/atlas/user/l/lduflot/atlasreadable/ZeroLeptonRun2-00-00-51/filteredOct7/" 
	mcdir ="root://eosatlas//eos/atlas/user/i/ideigaar/Ntuples_ZLFv51/"
	mcdir ="/afs/cern.ch/user/m/marijam/work/public/ZeroLeptonRun2-51/"
	mcdir ="/data/maxi158/atljphys/yminami/small/ZeroLeptonRun2-00-00-51/filteredOct17/"
	mcdir ="/data/maxi153/atljphys/shadachi/analysis/ntuple/ZeroLeptonRun2/00-00-51/filteredNov26/withsystematics/"
	mcdir ="/data/maxi158/atljphys/yminami/small/ZeroLeptonRun2-00-00-51/"
commonsyst=" "  

ZName = 'ZMassiveCB'
WName = 'WMassiveCB'
YName = 'GAMMAMassiveCB'
if doAlternativeZ:
    ZName = 'ZMadgraphPythia8'
    print "Running alternative Z sample!"
if doAlternativeW:
    WName = 'WMadgraphPythia8'
    print "Running alternative W sample!"
if doAlternativeY:
    YName = 'GAMMAMassiveCB_TRUTH_filtered'
    print "Running alternative Y sample!"
mc ={}
mc['Diboson']={'name':'Diboson','ds':'lDiboson','redoNormWeight':'redoNormWeight',
	 'color':ROOT.kPink-4,'inputdir':mcdir+'DibosonMassiveCB.root','treePrefix':'Diboson_','treeSuffix':'',
	 'syst':commonsyst}
if doAlternativeZ:
    mc['Zjets']={'name':'Z+jets','ds':'lZjets','redoNormWeight':'redoNormWeight',
	 'color':ROOT.kBlue+3,'inputdir':mcdir+ZName+'.root','veto':1,'treePrefix':'Z_','treeSuffix':'_Madgraph',
	 'syst':commonsyst}
else:
    mc['Zjets']={'name':'Z+jets','ds':'lZjets','redoNormWeight':'redoNormWeight',
	 'color':ROOT.kBlue+3,'inputdir':mcdir+ZName+'.root','veto':1,'treePrefix':'Z_','treeSuffix':'',
	 'syst':commonsyst}
mc['Top']={'name':'t#bar{t}(+X) & single top','ds':'lTop','redoNormWeight':'redoNormWeight','treeSuffix':'',
         'color':ROOT.kGreen-9,'inputdir':mcdir+('Top.root'),
         'treePrefix':'Top_','syst':commonsyst}
if doAlternativeW:
    mc['Wjets']={'name':'W+jets','ds':'lWjets','redoNormWeight':'redoNormWeight',
         'color':ROOT.kAzure-4,'inputdir':mcdir+WName+'.root','veto':1,'treePrefix':'W_','treeSuffix':'_Madgraph',
         'syst':commonsyst}
else:
    mc['Wjets']={'name':'W+jets','ds':'lWjets','redoNormWeight':'redoNormWeight',
         'color':ROOT.kAzure-4,'inputdir':mcdir+WName+'.root','veto':1,'treePrefix':'W_','treeSuffix':'',
         'syst':commonsyst}
mc['QCDMC']={'name':'Multijet (MC)','ds':'lQCDMC','redoNormWeight':'redoNormWeight',
	 'color':ROOT.kOrange-4,'inputdir':mcdirqcd+'QCD.root','treePrefix':'QCD_','treeSuffix':'',
	 'syst':commonsyst}
if doAlternativeY:
    mc['Yjets']={'name':'#gamma+jets','ds':'lYjets','redoNormWeight':'redoNormWeight', 
	 'color':ROOT.kYellow,'inputdir':mcgammadir+YName+'.root','veto':1,'treePrefix':'GAMMA_','treeSuffix':'_TRUTH_MadGraph','syst':commonsyst}
else:
    mc['Yjets']={'name':'#gamma+jets','ds':'lYjets','redoNormWeight':'redoNormWeight', 
	 'color':ROOT.kYellow,'inputdir':mcdir+YName+'.root','veto':1,'treePrefix':'GAMMA_','treeSuffix':'','syst':commonsyst}

allCoeffRegionsList =zlFitterConfig.allDataDrivenRegionsList()
allCoeffRegionsList += ["CRZllL"]
allCoeffRegionsList += ["VRZf"]

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
                    print filename
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
def CalcErrorR(val1,error1,val2,error2,val3,error3,val4,error4):
    return sqrt(pow(error1/val1,2)+pow(error2/val2,2)+pow(error3/val3,2)+pow(error4/val4,2))
def main(configMain):
    CountDict={}
    myChannelsDict ={}
    ##get channel (signal region)
    channel = finalChannelsDict[configMain.region]
    channel.Print()
    cutsDict ={}
    cutsDict = channel.getCutsDict()
    domeffABCDlocal =domeffABCD
    if channel.Ap <0 :
        domeffABCDlocal=False
    
    anaName = channel.name

    #setbaseline
    for regionName in allCoeffRegionsList:
        print regionName 
        ##get treename 
        treeBaseName = regionDict[regionName].suffixTreeName
        weight = channel.getWeights(regionName)
        ##remove pileupWeight  ###
        weight = weight.replace("pileupWeight * ","")
        print "remove pileupWeight"

        cuts = cutsDict[regionName]
        print "channel",cuts, weight
        each = {}
        if ("CRY" in regionName)or("VRY" in regionName):
            each = mc["Yjets"]
        if ("CRW" in regionName)or("VRW" in regionName):
            each = mc["Wjets"]
        if ("CRZll" in regionName)or("VRZll" in regionName):
            each = mc["Zjets"]
        if ("VRZlmtA" == regionName)or("VRZtmlA" == regionName)or("VRZlmlA" == regionName)or("VRZL" == regionName)or("VRZVL" == regionName)or("SR"==regionName)or("VRZf" == regionName):
            each = mc["Zjets"]

        count=Count(regionName, each['inputdir'], each["treePrefix"]+treeBaseName+each["treeSuffix"],cuts,weight, "mc", zlFitterConfig.luminosity*1000)
        tmphist=ROOT.TH1F(regionName+"meffInc","meffInc",1,0.,14000.)
        count.project(1.,regionName+"meffInc", "meffInc",cuts )
        value=tmphist.GetBinContent(1) 
        error=tmphist.GetBinError(1) 
        CountDict[regionName] = {"value":value,"error":error}
                       
    print CountDict
    CountDict["eff_YtmtA"] = {"value":CountDict["CRYtmtA"]["value"]/CountDict["SR"]["value"],
    "error":CountDict["CRYtmtA"]["value"]/CountDict["SR"]["value"]*CalcError(CountDict["SR"]["value"], CountDict["SR"]["error"],CountDict["CRYtmtA"]["value"],CountDict["CRYtmtA"]["error"])}
    
    CountDict["eff_ZllVL"] = {"value":CountDict["VRZVL"]["value"]/CountDict["SR"]["value"],
    "error":CountDict["VRZVL"]["value"]/CountDict["SR"]["value"]*CalcError(CountDict["SR"]["value"], CountDict["SR"]["error"],CountDict["VRZVL"]["value"],CountDict["VRZVL"]["error"])}
    
    CountDict["eff_WL"] = {"value":CountDict["CRWL"]["value"]/CountDict["CRYL"]["value"],
    "error":CountDict["CRWL"]["value"]/CountDict["CRYL"]["value"]*CalcError(CountDict["CRYL"]["value"], CountDict["CRYL"]["error"],CountDict["CRWL"]["value"],CountDict["CRWL"]["error"])}
    
    CountDict["SF_nunuperll"] = {"value":CountDict["VRZVL"]["value"]/CountDict["CRZllVL"]["value"],
    "error":CountDict["VRZVL"]["value"]/CountDict["CRZllVL"]["value"]*CalcError(CountDict["VRZVL"]["value"], CountDict["VRZVL"]["error"],CountDict["CRZllVL"]["value"],CountDict["CRZllVL"]["error"])}

    CountDict["SF_llpernunu"] = {"value":CountDict["CRZllVL"]["value"]/CountDict["VRZVL"]["value"],
    "error":CountDict["CRZllVL"]["value"]/CountDict["VRZVL"]["value"]*CalcError(CountDict["CRZllVL"]["value"], CountDict["CRZllVL"]["error"],CountDict["VRZVL"]["value"],CountDict["VRZVL"]["error"])}
    
    CountDict["R_ZperW"] = {"value":CountDict["CRWVL"]["value"]/CountDict["CRZllVL"]["value"]*CountDict["CRZllL"]["value"]/CountDict["CRWL"]["value"],
    "error":CountDict["CRWVL"]["value"]/CountDict["CRZllVL"]["value"]*CountDict["CRZllL"]["value"]/CountDict["CRWL"]["value"]*CalcErrorR(
                        CountDict["CRWL"]["value"], CountDict["CRWL"]["error"],CountDict["CRZllL"]["value"],CountDict["CRZllL"]["error"],
                        CountDict["CRWVL"]["value"], CountDict["CRWVL"]["error"],CountDict["CRZllVL"]["value"],CountDict["CRZllVL"]["error"]
                    )
                            }
    CountDict["R_nunuperll"] = {"value":CountDict["CRZllVL"]["value"]/CountDict["VRZVL"]["value"]*CountDict["SR"]["value"]/CountDict["VRZf"]["value"],
    "error":CountDict["CRZllVL"]["value"]/CountDict["VRZVL"]["value"]*CountDict["SR"]["value"]/CountDict["VRZf"]["value"]*CalcErrorR(
                        CountDict["VRZf"]["value"], CountDict["VRZf"]["error"],CountDict["SR"]["value"],CountDict["SR"]["error"],
                        CountDict["CRZllVL"]["value"], CountDict["CRZllVL"]["error"],CountDict["VRZVL"]["value"],CountDict["VRZVL"]["error"]
                    )
                            }

    CountDict["eff_YL"] = {"value":CountDict["CRYL"]["value"]/CountDict["CRYtmtA"]["value"],
    "error":CountDict["CRYL"]["value"]/CountDict["CRYtmtA"]["value"]*CalcError(CountDict["CRYtmtA"]["value"], CountDict["CRYtmtA"]["error"],CountDict["CRYL"]["value"],CountDict["CRYL"]["error"])}

    CountDict["R_WperY"] = {"value":CountDict["VRWtmtA"]["value"]/CountDict["CRYtmtA"]["value"]*CountDict["CRYL"]["value"]/CountDict["CRWL"]["value"],
        "error":CountDict["VRWtmtA"]["value"]/CountDict["CRYtmtA"]["value"]*CountDict["CRYL"]["value"]/CountDict["CRWL"]["value"]*CalcErrorR(
                CountDict["CRWL"]["value"], CountDict["CRWL"]["error"],CountDict["CRYL"]["value"],CountDict["CRYL"]["error"],
                CountDict["VRWtmtA"]["value"], CountDict["VRWtmtA"]["error"],CountDict["CRYtmtA"]["value"],CountDict["CRYtmtA"]["error"]
                    )
                        }
    CountDict["R_ZperY"] = {"value":CountDict["SR"]["value"]/CountDict["CRYtmtA"]["value"]*CountDict["CRYL"]["value"]/CountDict["VRZL"]["value"],
        "error":CountDict["SR"]["value"]/CountDict["CRYtmtA"]["value"]*CountDict["CRYL"]["value"]/CountDict["VRZL"]["value"]*CalcErrorR(
                CountDict["VRZL"]["value"], CountDict["VRZL"]["error"],CountDict["CRYL"]["value"],CountDict["CRYL"]["error"],
                CountDict["SR"]["value"], CountDict["SR"]["error"],CountDict["CRYtmtA"]["value"],CountDict["CRYtmtA"]["error"]
                    )
                        }
    CountDict["R_YperZ"] = {"value":CountDict["CRYtmtA"]["value"]/CountDict["SR"]["value"]*CountDict["VRZL"]["value"]/CountDict["CRYL"]["value"],
        "error":CountDict["CRYtmtA"]["value"]/CountDict["SR"]["value"]*CountDict["VRZL"]["value"]/CountDict["CRYL"]["value"]*CalcErrorR(
                CountDict["CRYL"]["value"], CountDict["CRYL"]["error"],CountDict["VRZL"]["value"],CountDict["VRZL"]["error"],
                CountDict["CRYtmtA"]["value"], CountDict["CRYtmtA"]["error"],CountDict["SR"]["value"],CountDict["SR"]["error"]
                    )
                        }
    #only for w/o ABCD   
    if not domeffABCDlocal:
        CountDict["eff_YlmlA"] = {"value":CountDict["CRYlmlA"]["value"]/CountDict["SR"]["value"],
        "error":CountDict["CRYlmlA"]["value"]/CountDict["SR"]["value"]*CalcError(CountDict["SR"]["value"], CountDict["SR"]["error"],CountDict["CRYlmlA"]["value"],CountDict["CRYlmlA"]["error"])}

    else:
        #only for w/ ABCD
        CountDict["eff_YtmlA"] = {"value":CountDict["CRYtmlA"]["value"]/CountDict["CRYtmtA"]["value"],
        "error":CountDict["CRYtmlA"]["value"]/CountDict["CRYtmtA"]["value"]*CalcError(CountDict["CRYtmtA"]["value"], CountDict["CRYtmtA"]["error"],CountDict["CRYtmlA"]["value"],CountDict["CRYtmlA"]["error"])}

        CountDict["eff_YlmtA"] = {"value":CountDict["CRYlmtA"]["value"]/CountDict["CRYtmtA"]["value"],
        "error":CountDict["CRYlmtA"]["value"]/CountDict["CRYtmtA"]["value"]*CalcError(CountDict["CRYtmtA"]["value"], CountDict["CRYtmtA"]["error"],CountDict["CRYlmtA"]["value"],CountDict["CRYlmtA"]["error"])}


        CountDict["R_YABCD"] = {"value":CountDict["CRYlmlA"]["value"]/CountDict["CRYlmtA"]["value"]*CountDict["CRYtmtA"]["value"]/CountDict["CRYtmlA"]["value"],
        "error":CountDict["CRYlmlA"]["value"]/CountDict["CRYlmtA"]["value"]*CountDict["CRYtmtA"]["value"]/CountDict["CRYtmlA"]["value"]*CalcErrorR(
                        CountDict["CRYtmlA"]["value"], CountDict["CRYtmlA"]["error"],CountDict["CRYtmtA"]["value"],CountDict["CRYtmtA"]["error"],
                        CountDict["CRYlmlA"]["value"], CountDict["CRYlmlA"]["error"],CountDict["CRYlmtA"]["value"],CountDict["CRYlmtA"]["error"]
                    )
                        }
        CountDict["R_WABCD"] = {"value":CountDict["VRWlmlA"]["value"]/CountDict["VRWlmtA"]["value"]*CountDict["VRWtmtA"]["value"]/CountDict["VRWtmlA"]["value"],
    "error":CountDict["VRWlmlA"]["value"]/CountDict["VRWlmtA"]["value"]*CountDict["VRWtmtA"]["value"]/CountDict["VRWtmlA"]["value"]*CalcErrorR(
                        CountDict["VRWtmlA"]["value"], CountDict["VRWtmlA"]["error"],CountDict["VRWtmtA"]["value"],CountDict["VRWtmtA"]["error"],
                        CountDict["VRWlmlA"]["value"], CountDict["VRWlmlA"]["error"],CountDict["VRWlmtA"]["value"],CountDict["VRWlmtA"]["error"]
                    )
                        }
        CountDict["R_ZABCD"] = {"value":CountDict["VRZlmlA"]["value"]/CountDict["VRZlmtA"]["value"]*CountDict["SR"]["value"]/CountDict["VRZtmlA"]["value"],
    "error":CountDict["VRZlmlA"]["value"]/CountDict["VRZlmtA"]["value"]*CountDict["SR"]["value"]/CountDict["VRZtmlA"]["value"]*CalcErrorR(
                        CountDict["VRZtmlA"]["value"], CountDict["VRZtmlA"]["error"],CountDict["SR"]["value"],CountDict["SR"]["error"],
                        CountDict["VRZlmlA"]["value"], CountDict["VRZlmlA"]["error"],CountDict["VRZlmtA"]["value"],CountDict["VRZlmtA"]["error"]
                    )
                        }
    print CountDict
    f_count = open("count.dat","a")    
    f_eff = open("coeff.dat","a")
    if domeffABCDlocal:
        f_count.write(configMain.region +" w/ " )
        f_eff.write(configMain.region + " w/ " )
    else : 
        f_count.write(configMain.region +" w/o " )
        f_eff.write(configMain.region + " w/o " )
    f_count.write("meffABCD\n"  )
    f_eff.write("meffABCD\n" )

    for count in CountDict.keys():
        f_count.write(count + " " +str(CountDict[count]["value"])+ " " + str(CountDict[count]["error"]) + "\n")
    for count in CountDict.keys():
        if not "eff_" in count and "SF_" not in count and "R_" not in count:
            continue
        f_eff.write(count + " " +str(CountDict[count]["value"]) + " " + str(CountDict[count]["error"]) +"\n")
    f_count.close()
    f_eff.close()


def parseCmdLine(args):
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--r", dest="region", help="region", default="SR4jt")
    (config, args) = parser.parse_args(args)
    return config

if __name__ == "__main__":
        config = parseCmdLine(sys.argv[1:])
        main(config)

