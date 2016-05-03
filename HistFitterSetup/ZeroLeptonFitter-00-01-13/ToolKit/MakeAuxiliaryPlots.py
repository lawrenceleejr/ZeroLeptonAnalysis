#!/usr/bin/env python
# usage : 

__doc__ = """
This script make the auxiliary material plot for acceptance, efficiency,
cross-section, number of events.

it expects in the current directory:

 - signal.dat : a concatenation of the MCBackground.dat from getMCInfo.py
 - one directory per grid named GRIDNAME_acc with text files describing the acceptance with the format
MCChannelID,370750
Normalization,5000
PreSelection,1.
SR2jl,0.491399
SR2jm,0.231555
SR2jt,0.000885762
SR4jt,0.0286297
SR5j,0.0278378
SR6jm,0.0109974
SR6jt,0.00974419

Change the variable INPUTDIR to point to the directory with mini-tuples

"""

#  Laurent Duflot: adapted from Run1 script by Nikola Makovec
#
#  not tested: hability to read efficiencies from a pickle file
#  not implemented: overlay upper limits

upperLimitDict={}



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
# Import Modules                                                             # 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
import sys, os, pickle, copy
from optparse import OptionParser
from array import array
from math import pow,log10,ceil
from ChannelConfig import *
from ChannelsDict import *


import ROOT
# setup root
ROOT.gSystem.Load("libSusyFitter.so")

# to use the ATLAS style a lot of fine tuning is need in the text placement
#from PlotterUtils import RootOption
#gStyle=ROOT.gStyle
#rootOpt=RootOption(gStyle)
#rootOpt.setUpStyle()
ROOT.gROOT.SetBatch(True)


###########################################################################
###########################################################################
INPUTDIR="/data/atlas/duflot/ZLdata/zl2_57/filtered/"
MYWORKINGDIR=os.getcwd().strip()+"/"
LUMI=3209
ModelIndUL = { 'SR2jl': 16., 'SR2jm': 15.,   'SR2jt': 5.2,  'SR4jt': 2.7,  'SR5j': 1.7,  'SR6jm': 1.7,  'SR6jt': 1.6, }

###########################################################################
###########################################################################

def buildxsecDB():
    db = {}
    for line in open("signal.dat"):
        line = line.strip()
        if len(line) == 0: continue
        if line.startswith("#"): continue
        if line.startswith("id"): continue
        if line.startswith("SAMPLE"): continue
        words = line.split()
        db[(int(words[0]),int(words[1]))] = float(words[2])
        pass
    return copy.deepcopy(db)


class InfoPerPoint:
    def __init__(self, name,grid,m1=-999,m2=-999,MCstat=-999,xsec=-999,xsecEr=-999):
        self.name = name 
        self.grid = grid
        self.m1=m1
        self.m2=m2
        self.m3=-1
        self.m1min=-1
        self.m1max=-1
        self.m2min=-1
        self.m2max=-1
        self.m1title=-1
        self.m2title=-1
        self.title=-1
        self.MCstat = MCstat
        self.xsec=xsec
        self.xsecEr=xsecEr
        self.acceptance={}
        self.efficiency={}
        self.uncertainties={}
        self.CLs={}
        self.expCLs={}
        self.bestSR={}
        self.isProblematic=False

    def getUncertainty(self,ana):
        total=0
        for source,unc in self.uncertainties[ana].items():
            total+=unc*unc
        if total>0:
            total=sqrt(total)

        if total>1.2:
            print "ATT Large error: ",self.acceptance,self.efficiency,self.uncertainties[ana]
            total=1.2

        return total

    def getN(self,treename,rootfile,cmd):
        #get tree
        tree=rootfile.Get(treename)
        #draw
        hist=ROOT.TH1F("hist","hist",1,0,1)   
        try:
            tree.Draw("0>>hist",cmd)
        except:
                #print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                #print "Can't get tree for the point:"   
                self.isProblematic=True
                #self.Print()
                #print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                pass 
        N=hist.Integral()
        del tree
        del hist
        return N
       
    def SymmetrizeUncertainty(self,Nominal,Up,Down):
        if Nominal==0: return 0
        up=abs(Up-Nominal)
        down=abs(Down-Nominal)
        return (up+down)/2/Nominal



    def computeEfficiency(self,myAnaList):
        for anaShortName in myAnaList:
            #anaName = anaDict[anaShortName]

            #compute total number of events
            NTotal=LUMI*self.xsec
            if NTotal<=0:
                print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                print "Problem with N !!!!!!!!!!!!!"
                self.isProblematic=True
                self.Print()
                print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!" 
                return

            #selection
            cuts=finalChannelsDict[anaShortName].getCutsDict()
            #weights="1"
            #weights="normWeight*genWeight*pileupWeight*"+str(LUMI)
            weights="normWeight*genWeight*"+str(LUMI)
            cmd="("+cuts["SR"]+")*"+weights
            #print cmd

            #open root file
            filename=INPUTDIR+self.grid+".root"        
            rootfile = ROOT.TFile.Open(filename)

            #get tree (nominal)
            treename=self.grid+"_"+str(int(self.m1))+"_"+str(int(self.m2))
            if int(self.m3) > 0: treename += "_"+str(int(self.m3))
            treename+="_SRAll"
            Nominal=self.getN(treename,rootfile,cmd)
            self.efficiency[anaShortName]=Nominal/NTotal
            #print self.name,treename,Nominal,self.efficiency

            #store uncertainty results in a dict  LD: removed systematics part
            results={}
            
            #store results
            self.uncertainties[anaShortName]=results
            rootfile.Close()


    def Print(self):
        print "self.name" , self.name
        print "self.m1",self.m1
        print "self.m2",self.m2
        print "self.MCstat ",self. MCstat
        print "self.xsec",self.xsec
        print "self.xsecEr",self.xsecEr
        print "self.CLs",self.CLs
        print "self.expCLs",self.expCLs
        print "self.bestSR",self.bestSR
        

class InfoPerGrid:
    def __init__(self, name):
        self.name = name
        self.proc=-1
        self.allPoints={}

        try:
            picklefile = open(MYWORKINGDIR+'/signalPointPickle.pkl','rb')
        except:
            print 'Could not open signalPointPickle.pkl'
            sys.exit(1)

        pointdict = pickle.load(picklefile)
        
        for  mcid,masses in pointdict[name].items():
            if not self.allPoints.has_key(mcid):
                self.allPoints[mcid]=InfoPerPoint(mcid,self.name,m1=masses[0],m2=masses[1])
                if len(masses)>2: self.allPoints[mcid].m3=masses[2]
            else:
                print "mcid ",mcid,"already exist. Skip"
            pass
        pass
       
        

    def dumpAll(self,name):
        import pickle
        pickle.dump( self.allPoints, open( name, "wb" ) )

    def computeAcceptance(self,DIR):
        #acceptance are already computed and they are extracted from the files in DIR
        allFiles=os.popen("ls "+DIR +"/*txt").readlines()

        for filename in allFiles:
            filename=filename.strip()
            f = open(filename, 'r')
            lines=f.readlines()
            if len(lines)<3  or lines[0].split(",")[0]!="MCChannelID" or lines[1].split(",")[0]!="Normalization" or lines[2].split(",")[0]!="PreSelection":
                print "skip ",filename,len(lines),lines[0].split(",")[0],lines[1].split(",")[0],lines[2].split(",")[0]
                continue
            
            MCChannelID=int(lines[0].split(",")[1])
            Normalization=float(lines[1].split(",")[1])
            PreSelection=float(lines[2].split(",")[1])
            
            results={}
            for iline in range(3,len(lines)):
                ana=lines[iline].split(",")[0].replace("SR3jt","SR3j").replace("SR5jt","SR5j").replace("SR6jvt","SR6jt+").replace("SR4jvl","SR4jl-")#ATT: different naming convention is used in txt file
                acceptance=lines[iline].split(",")[1]
                results[ana]=float(acceptance)
            #print MCChannelID,Normalization,PreSelection,results
                
            if  self.allPoints.has_key(MCChannelID):        
                self.allPoints[MCChannelID].MCstat=Normalization
                self.allPoints[MCChannelID].acceptance=results
            else:
                #print "skip ",filename,MCChannelID
                continue


        

    def computeEfficiency(self,myAnaList,readDB,nameDB):
        if readDB:
            self.allPoints=pickle.load( open( nameDB, "rb" ) )
            print self.allPoints

        else:
            for p in self.allPoints.values():
                if not p.isProblematic:
                    p.computeEfficiency(myAnaList)
            self.dumpAll(nameDB)


    def getXsec(gridInfo):
        xsecDB = buildxsecDB()
        for p in gridInfo.allPoints.values():
            key=(int(p.name), int(gridInfo.proc))
            if xsecDB.has_key(key):
                p.xsec=xsecDB[key]
                p.xsecEr=0.
            else:
                #print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                print "No x-sec info the point:", p.name,p.m1,p.m2
                p.isProblematic=True
                #p.Print()
                #print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                pass    
            pass



    def MakePlot(self,name,m1List,m2List,varList,doLogz=True,minimum=-1,maximum=-1,info="",drawValue=False):
        varArray=array("d", varList)
        m1Array=array("d", m1List)
        m2Array=array("d", m2List)
        
        #For HEPData
        dscomment=""
        offset=14
        gridForHEPDATA="P P --> SQUARK SQUARK TOTO P P --> SQUARK < QUARK NEUTRALINO> SQUARK < QUARK NEUTRALINO>"
        if self.name.find("GG_")>=0:
            gridForHEPDATA="P P --> GLUINO GLUINO TOTO P P --> GLUINO < QUARK QUARK NEUTRALINO> GLUINO < QUARK QUARK NEUTRALINO>"
            offset=30
        allAna=finalChannelsDict.keys()
        counter=0
        for ana in allAna:
            counter+=1
            if name.split("_")[0]==ana:
                #print offset,counter
                offset+=counter
        nameForHEPData=name
        letter=""
        ana=name.split("_")[0]

        #print offset
    
        if name=="Stat":
            dscomment="Number of simulated events"
            nameForHEPData="Number of events"
        if name=="xsec":
            dscomment="Production cross-section in PB"
            nameForHEPData="Cross-section in PB"
        if name.find("Acc")>=0 and name.find("AccEff")<0:
            dscomment="Signal acceptance in PCT for "+ana
            nameForHEPData="Signal acceptance in PCT"
            letter="a"
        if name.find("AccEff")>=0:
            dscomment="Signal acceptance times reconstruction efficiency in PCT for "+ana
            nameForHEPData="Signal acceptance times reconstruction efficiency in PCT"
            letter="b"
        if name.find("Unc")>=0:
            dscomment="Uncertainty on signal acceptance times reconstruction efficiency for "+ana
            nameForHEPData="Uncertainty on signal acceptance times reconstruction efficiency"
            letter="c"

        figureNb=str(offset)+letter

        canvas = ROOT.TCanvas(name,name)
        canvas.SetTicks(1,1)
        canvas.SetRightMargin(0.15)
        if doLogz:
            canvas.SetLogz()
        g = ROOT.TGraph2D(len(varArray),m1Array,m2Array,varArray)
        g.SetName(dscomment+" TOTO Auxiliary Figure "+figureNb+" TOTO "+gridForHEPDATA)
        g.SetTitle(dscomment+"TOTO Auxiliary Figure "+figureNb+" TOTO "+gridForHEPDATA)
        hist=g.GetHistogram()





        if minimum<0:
            minimum=0.1*hist.GetMinimum(0.)
        hist.SetMinimum(minimum)
        if maximum<0:
            if doLogz:
                # nearest power of 10 above max
                hist.SetMaximum(1.01*pow(10.,float(ceil(log10(hist.GetMaximum())))))
            else:
                hist.SetMaximum(1.01*hist.GetMaximum())
        else:
            hist.SetMaximum(maximum)
            

        #self.m1name=self.m1name.replace("m_{#tilde{q}} [GeV]","SQUARK MASS IN GEV").replace("m_{#tilde{g}} [GeV]","GLUINO MASS IN GEV")
        #self.m2name=self.m2name.replace("m_{#tilde{#chi}^{0}_{1}} [GeV]","NEUTRALINO MASS IN GEV")

        hist.SetTitle("")
        hist.GetXaxis().SetTitle(self.m1name)
        hist.GetYaxis().SetTitle(self.m2name)
        hist.GetZaxis().SetTitle(nameForHEPData)

        g.GetXaxis().SetTitle(self.m1name)
        g.GetYaxis().SetTitle(self.m2name)
        g.GetZaxis().SetTitle(nameForHEPData)

        hist.SetAxisRange(self.m1min,self.m1max,"X")
        hist.SetAxisRange(self.m2min,self.m2max,"Y")
        hist.Draw("colz")

        tex =  ROOT.TLatex(0.1,0.92,self.title+" - "+info);
        tex.SetNDC()
        tex.SetTextFont(42);
        tex.SetTextSize(0.035);
        tex.SetLineWidth(2);
        tex.Draw();

        
        text = ROOT.TLatex()
        text.SetTextFont(42);
        text.SetTextSize(0.045);
        text.SetTextColor(ROOT.kBlack);
        text.SetNDC(ROOT.kTRUE);
        text.DrawLatex(0.15,0.82,"#bf{#it{ATLAS}} Internal      ");

        xmin = g.GetXaxis().GetXmin()
        xmax = g.GetXaxis().GetXmax()
        ymin = g.GetYaxis().GetXmin()
        ymax = g.GetYaxis().GetXmax()
        if drawValue:
            for i in range(len(m1List)):
                latex=ROOT.TLatex()
                latex.SetTextSize(0.015)
                tt="%.2f" % varList[i]
                x = m1List[i]
                y = m2List[i]
                if x>xmin and x<=xmax and y>=ymin and y<=ymax:
                    latex.DrawText(x,y,tt)
                    pass
                pass
            pass
        else:
            for p in self.allPoints.values():
                latex=ROOT.TLatex()
                latex.SetTextSize(0.015)            
            #tt="%.2f" % float(line[allpar.index("expectedUpperLimit")])
                tt="o"
                x = p.m1
                if p.m3 > 0: 
                    y = p.m3
                    pass
                else:
                    y = p.m2
                    pass

                if x>xmin and x<=xmax and y>=ymin and y<=ymax:
                    latex.DrawText(x,y,tt)
                    pass
                pass
            pass




        hist.Draw("axis,same")


#        level=array('d', [100])
#        hist.SetContour(len(level),level) 
#        hist.SetLineWidth(3)
#        hist.Draw("cont3") #colz")

        canvas.Print(self.name+"_"+name+".eps")
        canvas.Print(self.name+"_"+name+".gif")

        rootfilename="Fig_"+figureNb+".root"
        rootfile=ROOT.TFile.Open(rootfilename,"RECREATE")
        g.Write()
        hist.SetName(g.GetName()+'_TG2Dhist')
        hist.Write()
        rootfile.Write()
        rootfile.Close()


        

    def makePlots(self,myAnaList,doXsec,doAcceptance,doEfficiency):
        debugMCChannelIds = [370911,370975,370930,370711,370738,370749,371686,372743,371678,370747]
        #cross-section
        if doXsec:        
            xsecList=[]
            m1List=[]
            m2List=[]
            for p in self.allPoints.values():
                if not p.isProblematic:
                    m1List.append(float(p.m1))
                    if p.m3 > 0 :   # e.g. for GG_onestepCC
                        m2List.append(float(p.m3))
                    else:
                        m2List.append(float(p.m2))
                    xsecList.append(float(p.xsec))
            self.MakePlot("xsec",m1List,m2List,xsecList,info="cross-section [pb]")

        #efficiency 
        if doEfficiency:
            for ana in myAnaList:
                m1List=[]
                m2List=[]
                effList=[]
                ULcheckList=[]
                uncList=[]
                for p in self.allPoints.values():
                    if p.isProblematic: continue
                    if p.efficiency.has_key(ana):
                        eff=float(p.efficiency[ana])
                        unc=p.getUncertainty(ana)
                        uncList.append(unc) 
                        effList.append(eff)
                        if eff>0:
                            ULcheckList.append(ModelIndUL[ana]/eff)
                        else:
                            ULcheckList.append(99999.)
                        m1List.append(float(p.m1))
                        if p.m3 > 0 :   # e.g. for GG_onestepCC
                            m2List.append(float(p.m3))
                        else:
                            m2List.append(float(p.m2))                    
                        if int(p.name) in debugMCChannelIds: print ana,'efficiency',p.name,p.m1,p.m2,eff
                        pass

                #self.MakePlot(ana+"_Unc",m1List,m2List,uncList,info="Uncertainty "+ana)
                self.MakePlot(ana+"_AccEff",m1List,m2List,effList,info="Acceptance#timesEfficiency "+ana,maximum=1.01)
                self.MakePlot(ana+"_ULCheck",m1List,m2List,ULcheckList,info="ApproximateUL "+ana,drawValue=True)
                pass

        #acceptance 
        if doAcceptance:
            for ana in myAnaList:
                m1List=[]
                m2List=[]
                accList=[]
                nbList=[]
                statList=[]
                for p in self.allPoints.values():                    
                    if p.isProblematic: continue
                    if  p.acceptance.has_key(ana):
                        acc=float(p.acceptance[ana]) 
                        accList.append(acc)  
                        m1List.append(float(p.m1))
                        if p.m3 > 0 :   # e.g. for GG_onestepCC
                            m2List.append(float(p.m3))
                        else:
                            m2List.append(float(p.m2)) 
                        statList.append(float(p.MCstat)) 
                        if int(p.name) in debugMCChannelIds: print ana,'acceptance',p.name,p.m1,p.m2,acc
                    else:
                        print "no acc for:",p.m1,p.m2
                        pass
                self.MakePlot("Stat",m1List,m2List,statList,info="MC Statistics")                
                self.MakePlot(ana+"_Acc",m1List,m2List,accList,info="Acceptance "+ana,maximum=1.01)
                pass


###########################################################################
###########################################################################
def parseCmdLine(args):
    #from optparse import OptionParser
    import argparse

    parser = argparse.ArgumentParser() 
    parser.add_argument("--grid", dest="grid", help="grid name", default="SS_direct")
    parser.add_argument("--xsec", dest="doXsecPlot", action="store_true", default=False)
    parser.add_argument("--acc", dest="doAcceptance", action="store_true", default=False)
    parser.add_argument("--eff", dest="doEfficiency", action="store_true", default=False)
    parser.add_argument("--readDB", dest="readDB", action="store_true", default=False)
    parser.add_argument("--allSR", dest="doAllSR", action="store_true", default=False)
    parser.add_argument("--SR", dest="SRString", help="", default="")
    config = parser.parse_args(args)
   

    return config



###########################################################################
#
###########################################################################


    

###########################################################################
# Main
###########################################################################

def main():
    config = parseCmdLine(sys.argv[1:])

   
    gridName = config.grid
    #Grid setup
    gridInfo = InfoPerGrid(gridName)
    if gridName=="SS_direct":
        gridInfo.proc=4
        gridInfo.m1min=200
        gridInfo.m1max=1400
        gridInfo.m2min=0
        gridInfo.m2max=1200
        gridInfo.m1name="m_{#tilde{q}} [GeV]"
        gridInfo.m2name="m_{#tilde{#chi}^{0}_{1}} [GeV]"
        #gridInfo.m1name="SQUARK MASS IN GEV"
        #gridInfo.m2name="NEUTRALINO MASS IN GEV"
        gridInfo.title="#tilde{q}#tilde{q} production: #tilde{q}#rightarrow q #tilde{#chi}_{1}^{0}"
    elif gridName=="GG_direct":
        gridInfo.proc=2
        gridInfo.m1min=200
        gridInfo.m1max=2000
        gridInfo.m2min=0
        gridInfo.m2max=1400
        gridInfo.m1name="m_{#tilde{g}} [GeV]"
        gridInfo.m2name="m_{#tilde{#chi}^{0}_{1}} [GeV]"
        #gridInfo.m1name="GLUINO MASS IN GEV"
        #gridInfo.m2name="NEUTRALINO MASS IN GEV"
        gridInfo.title="#tilde{g}#tilde{g} production: #tilde{g}#rightarrow q q #tilde{#chi}_{1}^{0}"
    elif gridName=="GG_onestepCC":
        gridInfo.proc=2
        gridInfo.m1min=150
        gridInfo.m1max=1600
        gridInfo.m2min=0
        gridInfo.m2max=1600
        gridInfo.m1name="m_{#tilde{g}} [GeV]"
        gridInfo.m2name="m_{#tilde{#chi}^{0}_{1}} [GeV]"
        #gridInfo.m1name="GLUINO MASS IN GEV"
        #gridInfo.m2name="NEUTRALINO MASS IN GEV"
        gridInfo.title="#tilde{g}#tilde{g} production: #tilde{g}#rightarrow q q W #tilde{#chi}_{1}^{0} m(#tilde{#chi}_{1}^{#pm}) = (m(#tilde{g}+m(#tilde{#chi}_{1}^{0}))"

    #list of analysis
    anaListShortName=finalChannelsDict.keys()
    if config.doAllSR:
        myAnaList=anaListShortName#["SR2jt"]
    elif config.SRString!="":
        myAnaList=config.SRString.split(",")
    else:
        myAnaList=["SR2jl"]

    #make xsec plot
    if config.doXsecPlot or config.doEfficiency: 
        gridInfo.getXsec()
    #pass

    #compute acceptance times efficiency
    if config.doEfficiency:
        nameDB="eff_"+gridName+"_"+''.join(myAnaList)+".pkl"
        gridInfo.computeEfficiency(myAnaList,config.readDB,nameDB)



    #compute acceptance
    if config.doAcceptance:
        #ACCEPTANCEDIR="/afs/cern.ch/user/l/lduflot/work/public/"
        #gridInfo.computeAcceptance(DIR=ACCEPTANCEDIR+gridName+"_000004")
        gridInfo.computeAcceptance(DIR=MYWORKINGDIR+gridName+"_acc")


    #makeplots
    gridInfo.makePlots(myAnaList,doXsec=config.doXsecPlot,doAcceptance=config.doAcceptance,doEfficiency=config.doEfficiency)

###########################################################################
#Main
###########################################################################
if __name__ == "__main__":
    main()
