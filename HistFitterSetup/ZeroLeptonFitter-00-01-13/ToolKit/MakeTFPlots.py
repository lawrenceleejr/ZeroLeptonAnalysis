#!/usr/bin/env python
# usage : 

__doc__ = """
.........

"""
import ROOT
from ROOT import *

gStyle.SetOptStat(0)
gROOT.SetBatch(True)
from ChannelsDict import *

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
# Import Modules                                                             # 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
gSystem.Load("libSusyFitter.so")
import sys, os, string, shutil,pickle,subprocess
import ROOT
from ROOT import *
from ROOT import TMsgLogger
from math import *

def Symmetrize(default,histLow,histHigh):

    newLow=histLow.Clone()
    newHigh=histHigh.Clone()
    for ibin in range(1,newLow.GetNbinsX()+1):
        diff=abs(histLow.GetBinContent(ibin)-histHigh.GetBinContent(ibin))/2
        # if abs(default.GetBinContent(ibin)-histLow.GetBinContent(ibin))>diff:
        #     diff=abs(default.GetBinContent(ibin)-histLow.GetBinContent(ibin))
        # if abs(default.GetBinContent(ibin)-histHigh.GetBinContent(ibin))>diff:
        #     diff=abs(default.GetBinContent(ibin)-histHigh.GetBinContent(ibin))
        newLow.SetBinContent(ibin, default.GetBinContent(ibin)-diff)        
        newHigh.SetBinContent(ibin, default.GetBinContent(ibin)+diff )

        #print default.GetBinContent(ibin)
    return (newLow,newHigh)


def getNb(bkg,sys,region,rootfile):

    histname="h"+bkg+sys+"_"+region+"_obs_cuts"
    print histname
    try:
        hist = rootfile.Get(histname)
        res=(hist.GetBinContent(1),hist.GetBinError(1))
    except:
        res=(0,0)
    print res
    return res

def computeTF(bkg,sys,region,bkg2,sys2,region2,rootfile):

    nb2tuple=getNb(bkg2,sys2,region2,rootfile)
    nb2=nb2tuple[0]
    nb2Er=nb2tuple[1]
    print nb2

    nbtuple=getNb(bkg,sys,region,rootfile)
    nb=nbtuple[0]
    nbEr=nbtuple[1]
    #print nb,nbEr,nb2,nb2Er

    tf=0
    tfer=0
    if nb2!=0:
        tf=nb/nb2
        if nb!=0:
            tfer=tf*sqrt(nbEr*nbEr/nb/nb+nb2Er*nb2Er/nb2/nb2)
        else:
            tfer=tf*sqrt(nb2Er*nb2Er/nb2/nb2)

    return (tf,tfer,nb,nbEr,nb2,nb2Er)
        
        
def createGraph(bkg,sys,region,bkg2,sys2,region2):

    cmd="ls data/*/*Background*root*"
    res = sorted(os.popen(cmd).readlines(), key=str.lower)
    hist = TH1F("h_"+bkg+"_"+sys+"_"+region+"_"+bkg2+"_"+sys2+"_"+region2,"",len(res),0,len(res))
    hist1 = TH1F("h_"+bkg+"_"+sys+"_"+region,"",len(res),0,len(res))
    hist2 = TH1F("h_"+bkg2+"_"+sys2+"_"+region2,"",len(res),0,len(res))

    myMap={}
    for filename in res:
        filename=filename.strip()        
        anaShortName=filename.strip().split("/")[-1].replace("ZL_","").replace("_Background.root","")
        if anaShortName not in  finalChannelsDict.keys(): continue
#        if anaShortName!="SR4jt": continue
        myMap[anaShortName]=filename


   


    counter=0
    for anaShortName,filename in sorted(myMap.items()):
        print "================================"
        print anaShortName,filename
        counter+=1

        rootfile = TFile.Open(filename)
        
        tf=computeTF(bkg,sys,region,bkg2,sys2,region2,rootfile)
        
        hist.SetBinContent(counter,tf[0])
        hist.SetBinError(counter,tf[1])
        hist.GetXaxis().SetBinLabel(counter,anaShortName)
        hist.GetYaxis().SetTitle("TF")

        hist1.SetBinContent(counter,tf[2])
        hist1.SetBinError(counter,tf[3])
        hist1.GetXaxis().SetBinLabel(counter,anaShortName)

        hist2.SetBinContent(counter,tf[4])
        hist2.SetBinError(counter,tf[5])
        hist2.GetXaxis().SetBinLabel(counter,anaShortName)

        #print anaShortName,tf

        rootfile.Close()

    # canvas=TCanvas()
    # hist1.Draw("E")
    # hist2.SetLineColor(2)
    # hist2.Draw("E,same")
    # canvas.Print("h_"+bkg+"_"+sys+"_"+region+".gif")

    return hist

###########################################################################
#Main
###########################################################################
if __name__ == "__main__":
    
    doSym=True

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-b", "--bkg", help="background", default = "Wjets")
    (options, args) = parser.parse_args()
    
    
    bkg=options.bkg

    #####################################################
    allHist=[]
    canvas = TCanvas("can","can",900,600)
    leg= TLegend(0.5,0.6,0.9,0.9);
    leg.SetTextSize( 0.03 );
    leg.SetTextFont( 42 );
    leg.SetFillColor( 0 );
    min=0
    max=1

    #####################################################
    allSys=["JET_GroupedNP_1","JET_GroupedNP_2","JET_GroupedNP_3","MET_SoftTrk_Scale","MET_SoftTrk_ResoPerp","MET_SoftTrk_ResoPara"]
 #   allSys=[]
    sys="Nom"
    sys2=sys
    region="SR"
    
    if  bkg=="Multijets":
        max=0.002
        bkg2=bkg
        region2="CRQ"
        allSys=[]

   
    if  bkg=="Wjets":
        max=0.4
        bkg2=bkg
        region2="CRW"
        allSys+=["generatorW"]

    if bkg=="Top":
        max=0.2
        bkg2=bkg
        region2="CRT"
        allSys+=["generatorTop","fragmentationTop","TopTuneA14","TopRadiation"]#,"TopTuneA14"]#"theoSysTop","TopDiffXsecSys"]

    if bkg=="Zjets":
        max=0.6
        bkg2="GAMMAjets"
        region2="CRY"
        allSys+=["GeneratorZ","Kappa"]


   

    default=createGraph(bkg,sys,region,bkg2,sys2,region2)
    default.SetFillColor(5) 
    default.SetMaximum(max)
    default.SetMinimum(min)
    default.DrawCopy("E2") 
    default.SetFillColor(0)
    default.SetLineColor(1)
    default.SetLineWidth(2)
    default.DrawCopy("hist,same")
    default.SetFillColor(5) 
    leg.AddEntry(default,sys,"LF")

    #for ibin in range(1,default.GetNbinsX()+1):
    #        print default.GetXaxis().GetBinLabel(ibin),default.GetBinContent(ibin)


    colors=[kBlue-9,kBlue,kBlue+2,
            15,12,1,
            2,3,6,7,50,40,30,20,1]

    allHist.append(default)

    counter=0
    for mysys in allSys:
        print "===>", sys
        sys=mysys+"High"
        sys2=sys
        if sys.find("photon")>=0 or  sys.find("GeneratorZ")>=0 or  sys.find("Kappa")>=0 or sys.find("QCD")>=0 or sys.find("TopTuneA14")>=0 or sys.find("TopRadiation")>=0:
            sys2="Nom"

        if sys.find("QCD")>=0:
            sys2="Nom"

        
        histHigh=createGraph(bkg,sys,region,bkg2,sys2,region2)
        histLow=createGraph(bkg,sys.replace("High","Low"),region,bkg2,sys2.replace("High","Low"),region2)
        
        if doSym:
            newHists=Symmetrize(default,histLow,histHigh)
            histLow=newHists[0]
            histHigh=newHists[1]


        histHigh.SetLineStyle(2)
        histHigh.SetLineColor(colors[counter])
        histHigh.SetLineWidth(2)

        histLow.SetLineStyle(2)
        histLow.SetLineColor(colors[counter])
        histLow.SetLineWidth(2)

        # for ibin in range(1,histLow.GetNbinsX()+1):
        #     mysysStr=mysys.replace("theoSysTop","topTheoSysErrSRDict").replace("theoSysZ","zTheoSysErrSRDict").replace("theoSysW","wTheoSysErrSRDict")
        #     tfLow=(default.GetBinContent(ibin)-histLow.GetBinContent(ibin))/default.GetBinContent(ibin)
        #     if tfLow<-1: tfLow=-1.
        #     #print mysysStr+"[\""+str(default.GetXaxis().GetBinLabel(ibin))+"\"]   =  "+str(tfLow)
        #     tfHigh=(default.GetBinContent(ibin)-histHigh.GetBinContent(ibin))/default.GetBinContent(ibin)
        #     if tfHigh<-1: tfHigh=-1.
        #     #print mysysStr+"[\""+str(default.GetXaxis().GetBinLabel(ibin))+"\"]   =  "+str(tfHigh)


        #     print mysysStr+"[\""+str(default.GetXaxis().GetBinLabel(ibin))+"\"]   =  "+str(abs(tfHigh)/2+abs(tfLow)/2)
            

        histHigh.DrawCopy("hist,same")
        histLow.DrawCopy("hist,same")
        counter+=1
        leg.AddEntry(histHigh,mysys,"LF")
        allHist.append(histHigh)
        allHist.append(histLow)
        
        
        

    leg.Draw()
    canvas.Print("TF_"+bkg+".pdf")
    canvas.Print("TF_"+bkg+".gif")
