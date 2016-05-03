#!/usr/bin/env python

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
# Import Modules                                                             # 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
import sys, os, string, shutil,pickle,subprocess
from array import array

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
# Root                                                                       # 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
import ROOT
from ROOT import *
gStyle.SetOptStat(0)
#gROOT.SetBatch(True)

gStyle.SetPalette(1)


oldFile=TFile.Open("root://eosatlas.cern.ch//eos/atlas/user/m/marijam/ZeroLeptonRun2-v51/AlternativeBkg_filtered/WMadgraphPythia8.root") 

newFile=TFile.Open("/afs/cern.ch/work/m/marijam/public/ZeroLeptonRun2-57-alternative/WMadgraphPythia8.root")


regionList=["VRWT","CRWT"]#,"SRAll"]

for region in regionList:


    c = TCanvas()
    c.SetLogy()


    selection="( meffInc >= 0 &&  met >= 200 && nJet >= 2 && jetPt[0] >= 300 && jetPt[1] >= 50 && veto==0 && ( dPhi >= 0.400000 ) && met/sqrt(meffInc-met) >= 15 && nBJet==0)"#*normWeight*genWeight"


    hold=TH1F("hold","hold",50,800,2000)
    oldFile.Get("W_"+region+"_Madgraph").Draw("meffInc>>hold",selection)


    hnew=TH1F("hnew","hnew",50,800,2000)
    newFile.Get("W_"+region+"_Madgraph").Draw("meffInc>>hnew",selection+"*2","same,hist")
    hnew.SetLineColor(2)

    hold.Draw()
    hnew.Draw("same")

    c.Print(region+".gif")




