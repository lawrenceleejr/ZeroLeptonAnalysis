#!/usr/bin/env python
# usage : 

import time
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

__doc__ = """
.........

"""
from ROOT import *
gSystem.Load("libSusyFitter.so");
#gROOT.LoadMacro("contourmacros/m0_vs_m12_nofloat.C");

gROOT.LoadMacro("ContourUtils.C");
gStyle.SetOptStat(0)
gROOT.SetBatch(True)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
# Import Modules                                                             # 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
import sys, os, string, shutil,pickle,subprocess

# Your list of analyses (i.e. regions) should be in python/AnaList.py 
from MyAnaList_SS import *
from MyAnaList_GG import *
from MyAnaList_SG import *
from AnaList import *

#anaList=anaListOPTI
#anaList=["SRE,medium","SRD,tight"]

class MyGraph():
    def __init__(self,name):
        self.infoList=[]
        self.name=name
        self.tgraph=None

    def Sort(self):
        self.infoList=sorted(self.infoList, key=lambda info: info[0])   # sort by x
        
    def Print(self):
        self.Sort()        
        for i in self.infoList:
            print i[0],i[1],StatTools.GetSigma(i[1]),i[2].replace("jet1","").replace("jet2","").replace("jet3","").replace("jet4","").replace("jet5","").replace("jet6","").replace("pt","").replace("metomeff","").replace("met","").replace("meff","").replace("Sig","").replace("dPhi","").replace("-",",")

    def DeltaMin(self,graph,xmax=-1,xmin=-1):
        #print "In DeltaMin"
        deltamin=10000
        xmin=-999
        #self.Print()
        #graph.Print()
        #toto
        for i in range(len(self.infoList)):
            if True:
            #if (xmax<0 or self.infoList[i][0]<xmax) and (xmin<0 or  self.infoList[i][0]>=xmin):

                #print len(graph.infoList)
                for j in range(len(graph.infoList)):
                    #print self.infoList[i][0],graph.infoList[i][0] 
                    if self.infoList[i][0]==graph.infoList[j][0] :

                        delta=self.infoList[i][1]-graph.infoList[j][1]
                        ##print delta
                        if delta<deltamin:
                            deltamin=delta
                            xmin=graph.infoList[i][0]
        #print deltamin  
        return (deltamin,xmin)
        
    def addPoint(self,x,y,ana=""):
        found=False
        for i in range(len(self.infoList)):
            if x ==self.infoList[i][0]:
                found=True
                if y<self.infoList[i][1]:
                    self.infoList[i]=(x,y,ana)
        if not found:                
                self.infoList.append((x,y,ana))


    def getTGraph(self,color=1):
        if len(self.infoList)==0: return None

        self.Sort()

        g=TGraph(len(self.infoList))
        counter=0
        for i in self.infoList:
            g.SetPoint(counter,i[0],i[1])
            #g.SetPoint(counter,i[0],StatTools.GetSigma(i[1]))
            
            counter+=1
        g.SetName(self.name)
        g.SetLineColor(color)
        g.SetMarkerColor(color) 
        g.SetLineWidth(2)        
        self.tgraph=g
        return g

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
# Some global variables
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#

from summary_harvest_tree_description import treedescription
dummy,description = treedescription()
allpar = description.split(':')
print dummy,description

# INPUTDIR has the workspaces from HistFitter
INPUTDIR="../../results/"
INPUTDIR_SIGNALDB="/afs/cern.ch/atlas/groups/susy/0lepton/ZeroLeptonFitter/ZeroLepton-00-00-36_Light/"

# OUTPUTDIR is where the combination of these using hadd will go, as well as 
#           all the list files for the contours, the histograms and the plots
OUTPUTDIR="Outputs/"
PLOTSDIR="plots/"

try:
    os.mkdir(OUTPUTDIR)
except:
    pass


# List of grids: key maps to array of (xlabel, ylabel, xmin, xmax, ymin, ymax)
# Add your favourite grid here. Note: if interpretation is not hypo_<grid>_<pointX>_<pointY>,
# change makeContours()
gridInfo={}
gridInfo["SM_SS_direct"]=("Squark mass [GeV]","Neutralino1 mass [GeV]",200,1200,25,800,[3])
gridInfo["SM_SG_direct"]=("Gluino mass [GeV]","Neutralino1 mass [GeV]",200,1500,25,1500,range(0,3))#ATT ???
gridInfo["SM_GG_direct"]=("Gluino mass [GeV]","Neutralino1 mass [GeV]",200,1500,25,1100,[1])
gridInfo["msugra_0_10_P"]=("m_{0} [GeV]","m_{1/2} [GeV]",100,3500,300,800,[0,44])
gridInfo["Gluino_Stop_charm"] = ("m_{#tilde{g}} [GeV]", "m_{#tilde{t}} [GeV]", 700, 1220, 200, 1000) 

# Cross sections to use. (Up, down is the theory uncertainty)
# Our plotting always uses Nominal for exp+obs+yellow band, up and down only for two extra obs curves
allXS=["Nominal"]#,"Up","Down"]

###########################################################################
# useful functions
###########################################################################

def parseCmdLine(args):
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-m", dest="doMerge", help="merge output root files", action='store_true', default=False)
    parser.add_option("-c", dest="makeContours", help="create contours", action='store_true', default=False)
    parser.add_option("-o", dest="doOring", help="Analysis Oring", action='store_true', default=False)
    parser.add_option("-p", dest="makePlots", help="create plots", action='store_true', default=False)
    parser.add_option("--all", dest="doAll", help="do all steps", action='store_true', default=False)
    parser.add_option("--grid", dest="grid", help="grid name", default="SM_SS_direct")
    parser.add_option("--suffix", dest="suffix", help="suffix to append after grid name in output files (default empty)", default="")
    parser.add_option("--match", dest="match", help="name to match hypotest files (we construct <match>*<grid>*)", default="")
    parser.add_option("--ul", dest="makeUL", help="do upper limits", action='store_true', default=False)
   
    (config, args) = parser.parse_args(args)

    config.match = config.match+"*"+config.grid+"*"
    config.outputName = config.grid + config.suffix

    return config

# TODO this should NOT use shell expansion. We just want to get the files to be able to match them against a certain grid, region, xs and possibly a match
def MergeFiles(config):
    #merge histfitter output root files
    print config.anaList
    for ana in config.anaList:
        for xs in allXS:
            cmd="hadd -f "+OUTPUTDIR+config.outputName+"_"+ana+"_fixSigXSec"+xs+".root "+ INPUTDIR+"/*"+ana+"*"+config.match+"*fixSigXSec*"+xs+"*hypotest.root*" 
            print cmd
            subprocess.call(cmd, shell=True)

            #if config.makeUL:
            cmd="hadd -f "+OUTPUTDIR+config.grid+"_"+ana+"_upperlimit.root "+ INPUTDIR+"/*"+ana+"_*"+config.grid+"*upperlimit*.root*"
            print cmd
            subprocess.call(cmd, shell=True)
        
        

def mergeFileList(config,clsFileName,upperFileName):
    #This method merge the two files where the hypotest and hypotestinverter results are stored
    #Information on cross-section are also added
    
    #get list of process
    procs=gridInfo[config.grid][6]
    
    try:
        picklefile = open('signalPointPickle2012.pkl','rb')
    except:
        cmd="python ../../ToolKit/makeSignalPointPickle2012.py;"
        print cmd
        subprocess.call(cmd, shell=True)
        
        picklefile = open('signalPointPickle2012.pkl','rb')
    
    pointdict = pickle.load(picklefile)

    #invert map
    invert_pointdict={}
    for key,info in pointdict[config.grid].items():
        invert_pointdict[info]=key



    file = TFile.Open(INPUTDIR_SIGNALDB+"/SignalDB_"+config.grid+".root");
    map=file.Get("runNumToXsec")#grid);

    #open the first file and get info
    myMap={}
    try:
        f = open(clsFileName, 'r')
    except:
        print "WARNING: ",clsFileName,"can't be found. skipped"        
        return
    
    for line in f.readlines():
        elements=line.strip().split()
        key=(elements[-2],elements[-1])
        myMap[key]=elements[:-2]
    f.close()

    #open the second file and get info
    try:
        f = open(upperFileName, 'r')
    except:
        print "WARNING: ",upperFileName,"can't be found. skipped"        
        return
    
    for line in f.readlines():
        elements=line.strip().split()
        key=(elements[-2],elements[-1]) #key id (m0,m12)
        if key not in myMap.keys():
            myMap[key]=elements[:-2]
        else:
             myMap[key]=myMap[key][:14]+ elements[14:-2]#replace info on upperlimits
    f.close()


    newfile = open(clsFileName, 'w')
    for key,infos in myMap.items():

        #compute mc id and compute xsec
        id=invert_pointdict[ (int(float(key[0])),int(float(key[1])))]

        xsec=0
        if len(procs)>1:
            print "WARNING: several processes are defined for this grid" 
            print "Cross-section computation need to be checked"
            #time.sleep(3)
            
        for proc in procs:    
            newkey=str(id)+":"+str(proc)
            vec=map.GetValue(newkey)
            if vec!=None:
                xsec+=float(vec[0])
        infos[-2]=xsec*1000#units = fb


        #multiply upperLimits by xsec
        #for i in range(14,22):
        #    infos[i]=float(infos[i])*infos[-2]




        #write in file
        line=""
        for info in infos:
            line+=" "+str(info)
        for k in key:
            line+=" "+str(k)
        newfile.write(line+"\n")
        
    newfile.close()



def MakeContours(config):
    #merge histfitter output root files

    for ana in config.anaList:        
        for xs in allXS:

            basename = OUTPUTDIR+config.outputName+"_"+ana+"_fixSigXSec"+xs            
            
            # Format of the hypotests, normally follows e.g. hypo_<grid>_2000_1000 
            format     = "hypo_"+config.grid+"_%f_%f";
            interpretation = "m0:m12";            
            
            # pMSSM is different; if your grid is also different, add here
            if config.grid == "pMSSM":
                format     = "hypo_"+config.grid+"_%f";
                interpretation = "id";  
            
            cutStr = "1"; # accept everything

            inputfile = basename+".root"
            CollectAndWriteHypoTestResults( inputfile, format, interpretation, cutStr ) ;
            cmd="mv *_list "+OUTPUTDIR
            subprocess.call(cmd, shell=True)

            #extra information from upper limits computation and merge the files
            basenameUL = OUTPUTDIR+config.grid+"_"+ana+"_upperlimit"  
            #if config.makeUL and xs=="Nominal":
            inputfile = basenameUL+".root"
            CollectAndWriteHypoTestResults( inputfile, format, interpretation, cutStr ) ;
            cmd="mv *_list "+OUTPUTDIR
            subprocess.call(cmd, shell=True)
            #merge the 2 files in 1
            mergeFileList(config,basename+"__1_harvest_list",basenameUL+"__1_harvest_list")
            cmd="mv *_list "+OUTPUTDIR
            subprocess.call(cmd, shell=True)

            
            cmd = "root -b -q \"makecontourhists.C(\\\""+basename+"__1_harvest_list"+"\\\")\""
            print cmd
            subprocess.call(cmd, shell=True)
                        
            cmd = "mv -v *_list.root "+OUTPUTDIR
            print cmd
            subprocess.call(cmd, shell=True)

            pass
        pass
    pass



def MakePlots(config):


    if config.grid=="SM_SS_direct":
        allLines=[##("v",550,0,550),
                  ("h",0,350,1200),
                  ##("v",787,0,550),
                  ("v",487,0,550),
                  ("v",750,0,550)
                  ]    
    elif config.grid=="SM_GG_direct":
        allLines=[("v",700,0,1000),
                  ("h",0,600,1500),
                  ("v",1125,00,700)]

    elif config.grid=="SM_SG_direct":
        allLines=[("v",1012,0,1100),
                  ("h",0,900,1700),
                  ("v",1387,0,900)]

        

    
    for aLine in allLines:

        MIN=0.1 
        MAX=5
        logY=False#True
        MASSMIN=aLine[2]#0
        MASSMAX=aLine[3]#600
        line=aLine[0]
        cut=aLine[1]



        canvas = TCanvas("","");
        if logY:
            canvas.SetLogy()

        leg= TLegend(0.11,0.6,0.57,0.89);
        leg.SetTextSize( 0.03 );
        leg.SetTextFont( 42 );
        leg.SetFillColor( 0 );
        leg.SetFillStyle(1001);

        colors=[1,3,4,ROOT.kOrange,7,1,50,35,ROOT.kPink,45,56]*100
        counter=0
        best= MyGraph("best")
        bestSUSY12= MyGraph("bestSUSY12")


        bestMETSig = MyGraph("best MET significance")
        bestMETOMEFF  = MyGraph("best MET/meff")
        bestDPhi0 = MyGraph("best no extra dphi cut")
        
        xsecGraph= MyGraph("xsec")
        allMyGraphs=[]

        missingFiles=[]
        for ana in config.anaList:
            filename=OUTPUTDIR+config.grid+"_"+ana+"_fixSigXSecNominal__1_harvest_list"
            #print "OPEN: ",filename
            try:                
                textfile=open(filename)
            except:
                missingFiles.append(filename)
                print "WARNING: ",filename,"can't be found. skipped"        
                continue
            
            
            graph = MyGraph(ana)
            for text in textfile.readlines():
                text=text.strip().split()
                UL=float(text[allpar.index("expectedUpperLimit")])
                #UL=float(text[allpar.index("CLsexp")])
                #UL=StatTools.GetSigma(float(text[allpar.index("CLsexp")]))
                xsec=float(text[allpar.index("xsec")])

                m0=float(text[-2])#600
                m12=float(text[-1])#50
                deltaM=m0-m12
                ####print m0,UL
                if UL<=0: continue

                var=0
                if line=="d":
                    if deltaM!=cut: continue
                    var=m0
                elif line=="h":
                    if m12!=cut:continue
                    var=m0
                else:
                    if m0!=cut:continue
                    var=m12
                    #print UL,m12,ana


                graph.addPoint(var,UL,ana)
                best.addPoint(var,UL,ana)
                if ana.find("loose")>=0 or ana.find("medium")>=0  or ana.find("tight")>=0 :
                    bestSUSY12.addPoint(var,UL,ana)
                if ana.find("Sig0-")>=0:                    
                    bestMETOMEFF.addPoint(var,UL,ana)
                else:                    
                    bestMETSig.addPoint(var,UL,ana)
                if ana.find("-dPhi0")>=0 and ana.find("-dPhi0.") <0:
                    bestDPhi0.addPoint(var,UL,ana) 


                #bestMETSig
                #bestMETOMEFF
                
                xsecGraph.addPoint(var,xsec,ana)

            allMyGraphs.append(graph)
            textfile.close()
            #graph.Print()



        selectedMyGraphs=[]
        #print "============================ooo"
        for  mg in allMyGraphs:
            counter+=1
            deltaMin=mg.DeltaMin(best,xmax=MASSMAX,xmin=MASSMIN)[0]
            #print deltaMin,mg.name
            
            if  deltaMin<0.0001:
                selectedMyGraphs.append(mg)

        #selectedMyGraph=sorted(allMyGraphs, key=lambda toto: toto.DeltaMin(best,xmax=MASSMAX,xmin=MASSMIN)[0])   # sort by x

        ###best=sorted(best, key=lambda toto: toto[0])   # sort by x
        best.Print()

        
        g=best.getTGraph()
        g2=xsecGraph.getTGraph()
        g.SetMaximum(MAX)
        g.SetMinimum(MIN)
        g.SetMarkerStyle(25)
        g.GetXaxis().SetLimits(MASSMIN,MASSMAX)
        g.GetYaxis().SetTitle("#sigma_{excluded}/#sigma_{nominal}")

        xaxis="TOTO"
        if line=="h":
            xaxis=gridInfo[config.grid][0]            
            g.SetTitle(gridInfo[config.grid][1]+" = "+str(cut))
        if line=="v":
            xaxis=gridInfo[config.grid][1]            
            g.SetTitle(gridInfo[config.grid][0]+" = "+str(cut))
            
        g.GetXaxis().SetTitle(xaxis)
      
        
        g.Draw("AP")
        leg.AddEntry(g,"oring of all analysis","P")
        value=1##0.05###1.64485
        tline=TLine(MASSMIN,value,MASSMAX,value)
        tline.SetLineStyle(2)
        tline.Draw("same")
     ##    gSUSY12=bestSUSY12.getTGraph(2)
##         leg.AddEntry(gSUSY12,"oring of SUSY12 analysis","L")
##         gSUSY12.Draw("PL")
##         gMETOMEFF=bestMETOMEFF.getTGraph(4)
##         leg.AddEntry(gMETOMEFF,"oring of met/meff analysis","L")
##         gMETOMEFF.Draw("PL")
##         gMETSig=bestMETSig.getTGraph(3)
##         leg.AddEntry(gMETSig,"oring of MET Sig analysis","L")
##         gMETSig.Draw("PL")
        
        #gDPhi0=bestDPhi0.getTGraph(6)
        #leg.AddEntry(gDPhi0,"oring of analysis without tighten dphi cut","L")
        #gDPhi0.Draw("PL")
        
        #g2.Draw("L*")
        counter=0
        for  mg in selectedMyGraphs:
            counter+=1
            g=mg.getTGraph(color=colors[counter])
            if g == None:
                continue
            legendname=mg.name.replace("jet1","").replace("jet2","").replace("jet3","").replace("jet4","").replace("jet5","").replace("jet6","").replace("pt","").replace("metomeff","").replace("met","").replace("meff","").replace("Sig","").replace("dPhi","").replace("-",",")
            leg.AddEntry(g,legendname,"L")
            g.SetMarkerStyle(24)
            g.SetLineStyle(1)
            if g.GetName().find("loose")>=0 or g.GetName().find("medium")>=0  or g.GetName().find("tight")>=0 :
                g.SetLineStyle(1)
            g.Draw("L")

        leg.Draw("same")

        #canvas.Print(PLOTSDIR+"/"+config.outputName+"_"+line+str(cut)+".gif")
        canvas.Print(PLOTSDIR+"/"+config.outputName+"_"+line+str(cut)+".eps")
        canvas.Print(PLOTSDIR+"/"+config.outputName+"_"+line+str(cut)+".pdf")
        canvas.Print(PLOTSDIR+"/"+config.outputName+"_"+line+str(cut)+".png")
        if len(missingFiles)>0:
            print "##########################################################"
            print "##########################################################"
            print "##########################################################"
            print "# Missing files:                             "
            for file in missingFiles:
                print file
            print "##########################################################"


# Merge regions into combination based on best region (simply pick lowest p-value)
def Oring(config):
    import sys, os, string, shutil, pickle, subprocess    
    import ROOT
    ROOT.gROOT.Reset()
    ROOT.gROOT.SetBatch(True)



    # For all xsecs, merge on best selectpar (normally expected CLs)
    for xsecStr in allXS:
        myMap = {}
        selectpar = "CLsexp"
        par1 = "m0"
        par2 = "m12"

        for ana in config.anaList:
            filename = OUTPUTDIR+config.outputName+"_"+ana+"_fixSigXSec"+xsecStr+"__1_harvest_list"
            print filename

            if not os.path.exists(filename):
                continue

            f = open(filename,'r')
            for line in f.readlines():
                vals = line.strip().split(' ')
                if len(allpar) != len(vals): 
                    print 'PRB!!!!!!!!!!!!!!!!!!!!'
                    print len(allpar),len(vals)
                    continue
                
                pval = float( vals[allpar.index(selectpar)])
                par1 = float( vals[allpar.index("m0")])
                par2 = float( vals[allpar.index("m12")])

                if pval<0:#remove negative pvalue
                    continue 
                key = (par1,par2)

                if key not in myMap.keys():
                    myMap[key] = [pval,line]
                else:
                    if pval < myMap[key][0] and pval>=0:
                        myMap[key][0] = pval
                        myMap[key][1] = line
            f.close()

        #print myMap
        combined_filename = OUTPUTDIR+config.outputName+"_combined_fixSigXSec"+xsecStr+"__1_harvest_list"
        f = open(combined_filename,"w")
        for key,info in myMap.items():
            f.write(info[1])
        f.close()

        cmd="root -b -q \"makecontourhists.C(\\\""+combined_filename+"\\\")\""
        ###print cmd
        subprocess.call(cmd, shell=True)
        cmd="mv *_list.root "+OUTPUTDIR
        subprocess.call(cmd, shell=True)

###########################################################################
#Main
###########################################################################

def main():
    config = parseCmdLine(sys.argv[1:])

    
    anaList=None
    if config.grid=="SM_SS_direct":
        anaList=anaListOPTI_SS
    elif config.grid=="SM_GG_direct":
        anaList=anaListOPTI_GG
    elif config.grid=="SM_SG_direct":
        anaList=anaListOPTI_SG
    #anaList+=anaListSUSY12
    config.anaList=[AnaConvert(ana) for ana in anaList]


    #print anaList
    
    if config.doMerge or config.doAll:
        MergeFiles(config)
        
    if config.makeContours or config.doAll:
        MakeContours(config)

    if config.doOring or config.doAll:
        Oring(config)
  
    if config.makePlots or config.doAll:
        MakePlots(config)
        
if __name__ == "__main__":
    main()
