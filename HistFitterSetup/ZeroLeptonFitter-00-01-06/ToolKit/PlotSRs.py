#!/usr/bin/env python
"""
This python script is plotting event counts in all SRs

Usage:
python ToolKit/MakePullPlots.py
python ToolKit/PlotSRs.py
"""
import sys
import math
import copy
import pickle
import ROOT
import os
import os
import errno

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

from ChannelsDict import *
from ROOT import *

ROOT.gROOT.SetBatch(True) # Turn off online histogram drawing

index=-1
MinThres=0.5
Min2=0.
Max2=1.9

doData=False#True#False


plots = {}
dMU = {}
dNP = {}
hNP = {}

labels = {}
labels["Top"] = "Top"
labels["Wjets"] = "W+jets"
labels["Zjets"] = "Z+jets"
labels["Multijets"] = "Multijets"
labels["GAMMA"] = "Gamma"
labels["Diboson"] = "Diboson"

colors={}
colors["Top"]=ROOT.kGreen-9
colors["Wjets"]=ROOT.kAzure-4
colors["Zjets"]=ROOT.kBlue+3
colors["Multijets"]=ROOT.kOrange
colors["GAMMA"]=ROOT.kYellow
colors["Diboson"]=ROOT.kRed+3

samples = ["Zjets","Top","Wjets","Multijets","Diboson"]#"GAMMAjets"

def PoissonError(obs):
    posError = TMath.ChisquareQuantile(1. - (1. - 0.68)/2. , 2.* (obs + 1.)) / 2. - obs - 1
    negError = obs - TMath.ChisquareQuantile((1. - 0.68)/2., 2.*obs) / 2
    symError=abs(posError-negError)/2.

    return (posError,negError,symError)

def main():

    allAna=sorted(finalChannelsDict.keys())

    #order per number of events per jet multiplicity
    #allAna=
    #allAna=["SR2jl","SR2jm","SR2jt","SR2jW","SR3j","SR4jl-","SR4jl","SR4jm","SR4jt","SR4jW","SR5j","SR6jl","SR6jm","SR6jt","SR6jt+"]

    nSR=len(allAna)

    hist_data = TH1F("data","data",nSR,0,nSR)
    hist_data.GetYaxis().SetTitle("Number of events")
    hist_data.GetXaxis().SetTitle("Signal Region")
    hist_data.GetYaxis().SetTitleOffset(0.85)
    hist_dataClone=hist_data.Clone()
    graph_data=TGraphAsymmErrors(nSR)
    graph_dataClone=TGraphAsymmErrors(nSR)


    hist_sumbkg = TH1F("sumbkg","sumbkg",nSR,0,nSR)
    hist_sumbkg.SetLineColor(2)
    hist_sumbkg.SetLineWidth(1)

    hist_bkgMap={}
    for sam in samples:
        hist_bkgMap[sam]=TH1F(sam,sam,nSR,0,nSR)
        hist_bkgMap[sam].SetFillColor(colors[sam])
        hist_bkgMap[sam].SetLineWidth(0)
        hist_bkgMap[sam].SetLineStyle(0)

    ## Get list of mu parameters (present in all SRs)
    counter=0
    for channel in allAna:
        counter+=1

        if not os.path.exists("yield_%s_all.pickle" % channel):
            continue
        try:
            fYield = open('yield_%s_all.pickle' % channel,'r')
        except:
            print "Could not open yield_%s_all.pickl" % channel
            continue

        theMap = pickle.load(fYield)

        print theMap.keys()
        #ATT: Assume that SR is the last one!!!



        nobs=float(theMap["nobs"][index])
        print nobs
        nsumbkgEr=theMap["TOTAL_FITTED_bkg_events_err"][index]
        nsumbkg=theMap["TOTAL_FITTED_bkg_events"][index]

        print channel
        hist_data.GetXaxis().SetBinLabel(counter,channel.replace("SR",""))
        hist_data.GetXaxis().SetLabelSize(0.015)

        hist_data.SetBinContent(counter,nobs)
        graph_data.SetPoint(counter-1,hist_data.GetBinCenter(counter),nobs)
        pEr=PoissonError(nobs)
        graph_data.SetPointError(counter-1,0.,0,pEr[1],pEr[0])

        hist_dataClone.SetBinContent(counter,nobs)
        graph_dataClone.SetPoint(counter-1,hist_data.GetBinCenter(counter),nobs)
        if nobs==0:
            hist_dataClone.SetBinContent(counter,MinThres)
            graph_dataClone.SetPoint(counter-1,hist_data.GetBinCenter(counter),MinThres)



        if nobs > 0:
            hist_data.SetBinError(counter,0.00001)#sqrt(nobs))

        hist_sumbkg.SetBinContent(counter,nsumbkg)
        hist_sumbkg.SetBinError(counter,nsumbkgEr)

        for sam in samples:
            n=theMap["Fitted_events_"+sam][index]
            er=theMap["Fitted_err_"+sam][index]
            hist_bkgMap[sam].SetBinContent(counter,n)


        #lepton sys
        #nsumLeptonicbkg=(theMap["Fitted_events_Wjets"][index]+theMap["Fitted_events_Top"][index])*0.4*0.1
        #        print "toto ",channel,sqrt((nsumLeptonicbkg*nsumLeptonicbkg)+(nsumbkgEr*nsumbkgEr)+nsumbkg)/sqrt((nsumbkgEr*nsumbkgEr)+nsumbkg)-1
        #print "toto ",channel,nsumbkgEr,sqrt(nsumLeptonicbkg*nsumLeptonicbkg+(nsumbkgEr*nsumbkgEr)),sqrt(nsumLeptonicbkg*nsumLeptonicbkg+(nsumbkgEr*nsumbkgEr))/nsumbkgEr-1




        pass

    hist_data.SetMinimum(MinThres)
    hist_data.SetMaximum(hist_data.GetMaximum()*10)
    hist_data.SetMaximum(100000)



    stack=THStack("stack","stack")
    for sam in samples:
        h=hist_bkgMap[sam]
        stack.Add(h)
    stack.Draw("same")
    hist_sumbkg.SetMarkerSize(0)
    hist_sumbkg.Draw("hist,same")
    hist_sumbkg2=  hist_sumbkg.Clone()
    hist_sumbkg2.SetFillStyle(3005)
    hist_sumbkg2.SetFillColor(2)
    hist_sumbkg2.SetLineColor(2)
    hist_sumbkg2.Draw("E2,same")
    #hist_data.SetMarkerSize(graph_data.GetMarkerSize()*2)
    #hist_data.SetMarkerColor(0)
    #hist_data.Draw("E,same")
    #hist_data.Draw("axis,same")
    hist_sumbkg.SetMaximum(100000)
    hist_sumbkg.SetMinimum(MinThres)


    print graph_data.GetMarkerSize(),"======================"

    graph_data.SetMarkerStyle(20)
    graph_data.SetLineWidth(3)
    if doData:
        graph_data.Draw("P")
        graph_dataClone.Draw("P")

    Max=hist_data.GetMaximum()
    Min=hist_data.GetMinimum()

    all=[]
    for counter in range(1,nSR):#[4,6,10,11]:
        line=TLine(counter,Min,counter,Max)
        line=TLine(float(counter),Min-1000000,float(counter),Max)
        line.SetLineWidth(2)
        line.SetLineColor(18)
        line.Draw("same")
        all.append(line)

    leg1= TLegend(0.76,0.52,0.93,0.87);
    leg1.SetTextSize( 0.05 );
    leg1.SetTextFont( 42 );
    leg1.SetFillColor( 10 );
    leg1.SetBorderSize( 0 );
#    leg1.AddEntry(hist_data,"Data 2012 (#sqrt{s}=8TeV)","P")
    leg1.AddEntry(hist_data,"Data 2015","P")
    leg1.AddEntry(hist_sumbkg2,"SM Total","LF")
    for sam in reversed(samples):
        leg1.AddEntry(hist_bkgMap[sam],sam.replace("Wjets","W+jets").replace("Zjets","Z+jets"),"F")
    leg1.Draw()

#     leg2= TLegend(0.35,0.9-0.12,0.5,0.9);
#     leg2.SetTextSize( 0.04 );
#     leg2.SetTextFont( 42 );
#     leg2.SetFillColor( 10 );
#     leg2.SetBorderSize( 0 );
#     leg2.AddEntry(hist_data,"Data 2012 (#sqrt{s}=8TeV)","P")
#     leg2.AddEntry(hist_sumbkg2,"SM Total","LF")
# #    for sam in samples:
# #        leg2.AddEntry(hist_bkgMap[sam],sam.replace("Wjets","W+jets").replace("Zjets","Z+jets"),"F")
#     leg2.Draw()

    text = TLatex()
    text.SetTextFont(42);
    text.SetTextSize(0.05);
    text.SetTextColor(kBlack);
    text.SetNDC(True);
    text.DrawLatex(0.23,0.84,"#bf{#it{ATLAS Internal}}          #intL dt = X fb^{-1}, #sqrt{s}=13TeV");

    text2 = TLatex()
    text2.SetTextFont(42);
    text2.SetTextSize(0.05);
    text2.SetTextColor(kBlack);
    text2.SetNDC(True);
    #text2.DrawLatex(0.23,0.79,"Internal");


    ###############
    hist_ratio=hist_data.Clone()
    hist_bkgerror=hist_data.Clone()
    graph_ratio=TGraphAsymmErrors(nSR)#graph_data.Clone()

    for counter in range(1,hist_data.GetNbinsX()+1):
        ratio=-1000
        nExp=hist_sumbkg.GetBinContent(counter)
        if nExp==0:
            nExp=0.01

        if doData:
            ratio=hist_data.GetBinContent(counter)/nExp
        pEr=PoissonError(hist_data.GetBinContent(counter))
        nExp=hist_sumbkg.GetBinContent(counter)
        nExpEr=hist_sumbkg.GetBinError(counter)



        #print hist_data.GetBinContent(counter)/nExp,pEr[1]/nExp,pEr[0]/nExp
        graph_ratio.SetPoint(counter-1,hist_data.GetBinCenter(counter),ratio)
        try:
            graph_ratio.SetPointError(counter-1,0.,0,pEr[1]/nExp,pEr[0]/nExp)
            hist_bkgerror.SetBinError(counter,nExpEr/nExp)
        except ZeroDivisionError:
            graph_ratio.SetPointError(counter-1, 0., 0, 0, 0)
            hist_bkgerror.SetBinError(counter, 0)

        hist_ratio.SetBinContent(counter,ratio)
        hist_ratio.SetBinError(counter,0.000001)

        hist_bkgerror.SetBinContent(counter,1)




        print counter,ratio,  hist_data.GetBinContent(counter), hist_sumbkg.GetBinContent(counter)," toto"

    ###########

    canvas = TCanvas("canvas","canvas",1000,800)
    canvas.SetLeftMargin(0.1)
    upperPad = ROOT.TPad("upperPad","upperPad",0.001,0.35,0.995,0.995)
    lowerPad = ROOT.TPad("lowerPad","lowerPad",0.001,0.001,0.995,0.35)

    upperPad.SetLogy()
    upperPad.SetFillColor(0);
    upperPad.SetBorderMode(0);
    upperPad.SetBorderSize(2);
    #upperPad.SetTicks()
    upperPad.SetTopMargin   ( 0.05 );
    upperPad.SetRightMargin ( 0.05 );
    upperPad.SetBottomMargin( 0.00 );
    upperPad.SetLeftMargin( 0.10 );
    upperPad.SetFrameBorderMode(0);
    upperPad.SetFrameBorderMode(0);
    upperPad.Draw()

    #lowerPad.SetGridx();
    #lowerPad.SetGridy();
    lowerPad.SetFillColor(0);
    lowerPad.SetBorderMode(0);
    lowerPad.SetBorderSize(2);
    #lowerPad.SetTickx(1);
    #lowerPad.SetTicky(1);
    lowerPad.SetTopMargin   ( 0.00 );
    lowerPad.SetRightMargin ( 0.05 );
    lowerPad.SetBottomMargin( 0.4 );
    lowerPad.SetLeftMargin( 0.10 );
    lowerPad.Draw()

    canvas.SetFrameFillColor(ROOT.kWhite)

    upperPad.cd()


    #DRAW=======================
    if doData:
        hist_data.Draw("E")
    else:
        hist_sumbkg.Draw("hist")

    all=[]
    for counter in range(1,nSR):#[4,6,10,11]:
        line=TLine(counter,Min,counter,Max)
        line=TLine(float(counter),Min-1000000,float(counter),Max)
        line.SetLineWidth(2)
        line.SetLineColor(18)
        line.Draw("same")
        all.append(line)


    stack.Draw("same")
    hist_sumbkg.Draw("hist,same")
    hist_sumbkg2.Draw("E2,same")

    graph_dataShadow=graph_data.Clone()
    graph_dataShadow.SetLineWidth(5)
    graph_dataShadow.SetMarkerSize(graph_data.GetMarkerSize()*1.3)
    graph_dataShadow.SetMarkerColor(0)
    graph_dataShadow.SetLineColor(0)
    if doData:
        graph_dataShadow.Draw("P")
        hist_data.Draw("E,same")
        graph_data.Draw("P")
        hist_data.Draw("axis,same")




    leg1.Draw()
    text.DrawLatex(0.23,0.80,"#bf{#it{ATLAS}} Internal          #intL dt = X fb^{-1}, #sqrt{s}=13TeV");
    #text2.DrawLatex(0.23,0.75,"Internal");

    lowerPad.cd()
    hist_ratio.SetMaximum(Max2)
    hist_ratio.SetMinimum(Min2)
    hist_ratio.GetYaxis().SetTitle("Data/Bkg")

    print "rrrr",hist_ratio.GetYaxis().GetLabelSize(),hist_ratio.GetYaxis().GetTitleSize(),hist_ratio.GetYaxis().GetTitleOffset()
    hist_ratio.GetYaxis().SetLabelSize(0.08)
    hist_ratio.GetYaxis().SetTitleSize(0.08)
    hist_ratio.GetYaxis().SetTitleOffset(0.5)

    hist_ratio.GetXaxis().SetLabelSize(0.12)
    hist_ratio.GetXaxis().SetTitleSize(0.1)
    hist_ratio.GetXaxis().SetTitleOffset(1.4)
    hist_ratio.GetXaxis().SetLabelOffset(0.02)
    print "rrrr",hist_ratio.GetYaxis().GetLabelSize(),hist_ratio.GetYaxis().GetTitleSize(),hist_ratio.GetYaxis().GetTitleOffset()


    hist_ratio.Draw("E")
    for counter in range(1,nSR):#[4,6,10,11]:
        line=TLine(float(counter),Min2,float(counter),Max2)
        line.SetLineWidth(2)
        line.SetLineColor(18)
        line.Draw("same")
        all.append(line)

    line=TLine(0,1,nSR,1)
    line.SetLineWidth(2)
    line.SetLineColor(18)
    line.Draw("same")
    all.append(line)

    hist_bkgerror.SetFillStyle(3005)
    hist_bkgerror.SetFillColor(2)
    hist_bkgerror.SetLineColor(2)
    hist_bkgerror.SetMarkerSize(0)
    hist_bkgerror.Draw("E2,same")

    if doData:
        graph_ratio.Draw("P")


    #canvas.Print("plotSR.gif")
    #canvas.Print("plotSR.pdf")

    make_sure_path_exists("plots/")
    canvas.Print("plots/plotSR.eps")

if __name__ == "__main__":

    import AtlasStyle
    AtlasStyle.SetAtlasStyle()
    from math import *

    main()
