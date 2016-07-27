#!/usr/bin/env python
"""
This python script is plotting event counts in all SRs

Usage:
python ToolKit/MakePullPlots.py
python ToolKit/PlotSRs.py
"""

from ZLFitterConfig import *
zlFitterConfig = ZLFitterConfig()


import sys
import math
import copy
import pickle
import ROOT

import os
from ROOT import *
import AtlasStyle

from ChannelsDict import *

AtlasStyle.SetAtlasStyle()
gStyle.SetPalette(1)
ROOT.gROOT.SetBatch(True) # Turn off online histogram drawing

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
    return symError

def VRNameFct(VR):
    return VR

def checkInvalidRegions(ana, VR) :
    if VR == "VRQ" : return True
    if "SRC" in ana :
        if VR == "VRQa" : return True
        if VR == "VRQb" : return True

        if VR == "VRZ"  : return True
        if VR == "VRZa" : return True
        if VR == "VRZb" : return True

        if VR == "VRWa" : return True
        if VR == "VRWb" : return True

        if VR == "VRTa" : return True
        if VR == "VRTb" : return True

    if ("SRG" in ana) or ("SRS" in ana) :
        if VR == "VRQc"  : return True
        if VR == "VRZc"  : return True
        if VR == "VRZca" : return True
    return False

#.replace("VRttbarTau","VRT$\\tau$").replace("VRWTau","VRW$\\tau$")

def main():


    allAna = sorted(finalChannelsDict.keys())
    #order per number of events per jet multiplicity
#    allAna=["SR2jl","SR2jm","SR2jt","SR4jt","SR5j","SR6jm","SR6jt"]
    nSR = len(allAna)
    print allAna

    # allVRs = ['VRW',
    #           'VRT',#:
    #               'VRQa',#:
    #               'SR',#:
    #               'VRTb',#:
    #               'VRWa',#:
    #               'VRZca',#:
    #               'VRTa',#:
    #               'VRZ',#:
    #               'VRZb',#:
    #               'VRWb',#:
    #               'VRQb',#:
    #               ]

    allVRs = zlFitterConfig.validationRegionsList
    allVRs.remove("VRQ")

    linesForTable=[]
    allVRsForChi2=allVRs #["VRZf","VRWMf","VRWTau","VRTMf","VRttbarTau","VRQ1","VRQ4"]

    lineVR=" Region & "
    for VR in allVRs:
        lineVR+=VRNameFct(VR)
        if VR!=allVRs[-1]:
            lineVR+="   &   "
    else:
        lineVR+="\\\\"
    linesForTable.append(lineVR)
    linesForTable.append("\\hline")

    bidim = TH2F("bidim","bidim",len(allVRs),0,len(allVRs),len(allAna),0,len(allAna))
    bidim.GetZaxis().SetTitle("(n_{obs}-n_{pred}) / #sigma_{tot}");

    ## Get list of mu parameters (present in all SRs)
    counterAna=0
    for channel in reversed(allAna):
        counterAna+=1
        channelName=channel.replace("Jigsaw","").replace("SRSR", "SR").replace("SR", "RJR-")

        if not os.path.exists("pull_%s.pkl" % channel):
            continue

        try:
            fPull = open('pull_%s.pkl' % channel,'r')
        except:
            print "Could not open pull_%s.pkl" % channel
            continue

        theMap = pickle.load(fPull)

#        print theMap

        lineForTable="{\\bf "+channelName+"} & "
        counterVR=0
        chi2=0
        chi2bis=0
        for VR in allVRs:
                counterVR+=1
            #pull="%.1f"%theMap[VR]
                try :
                    pull="%.2f"%theMap[VR][0]
                    nObs="%.1f"%theMap[VR][1]
                    nExp="%.1f"%theMap[VR][2]
                    nExpEr="%.1f"%theMap[VR][3]
                except KeyError :
                    print "missing this VR in the map, setting pull value to - "
                    pull  = "999"
                    nObs  = "999"
                    nExp  = "999"
                    nExpEr= "999"

                if checkInvalidRegions(channelName, VR) :
                    print "invalid, setting pulls to 999" , channelName , VR
                    pull  = "999"
                    nObs  = "999"
                    nExp  = "999"
                    nExpEr= "999"

                print channel, VR, pull

                pullstring = str(pull) if float(pull) < 500 else "N/A"
                lineForTable+= pullstring+"  "
                if VR!=allVRs[-1]:
                    lineForTable+=" & "
                else:
                    lineForTable+="\\\\"
                bidim.SetBinContent(counterVR,counterAna,float(pull))
                labelX=VRNameFct(VR).replace("$","").replace("\\","#")
#   #            print channel,labelX, nObs,nExp,nExpEr,"============= ",float(nExpEr)/sqrt(float(nExp)+0.0001)
                bidim.GetXaxis().SetBinLabel(counterVR,labelX)
                if VR in allVRsForChi2:
                    #chi2+=theMap[VR]*theMap[VR]
                    pull2=(float(nObs)-float(nExp))/PoissonError(float(nExp))
                    print nObs,nExp,PoissonError(float(nExp)),pull2
                    chi2bis+=pull2
#                    chi2+=theMap[VR][0]*theMap[VR][0]
            # except KeyError:
            #     print "missing" + VR
            #     pass

#        print "chi2 ",channel,chi2/len(allVRsForChi2),chi2bis/len(allVRsForChi2)
        linesForTable.append(lineForTable)
        #print lineForTable
        linesForTable.append("\\hline")
        bidim.GetYaxis().SetBinLabel(counterAna,channelName)

    canvas = TCanvas("canvas","canvas",1000,800)
    canvas.SetLeftMargin(0.1)
    canvas.SetRightMargin(0.2)
    canvas.SetBottomMargin(0.1)
    canvas.SetTopMargin(0.1)
    bidim.SetMaximum(3)
    bidim.SetMinimum(-3)
    bidim.Draw("colz")
    gStyle.SetPaintTextFormat("1.1f");
    bidim.Draw("text,same")


    text = TLatex()
    text.SetTextFont(42);
    text.SetTextSize(0.04);
    text.SetTextColor(kBlack);
    text.SetNDC(True);
    text.DrawLatex(0.1,0.93,"#bf{#it{ATLAS}}                                  #sqrt{s}=13TeV,"+str(round(zlFitterConfig.luminosity,1))+" fb^{-1}");
    text2 = TLatex()
    text2.SetTextFont(42);
    text2.SetTextSize(0.05);
    text2.SetTextColor(kBlack);
    text2.SetNDC(True);
    text2.DrawLatex(0.22,0.93,"Internal");




    canvas.Print("SummaryPull.eps")
    canvas.Print("SummaryPull.gif")
    canvas.Print("SummaryPull.pdf")

    debut="""
    \\begin{table}
    \\begin{center}
    \\caption{Differences between the numbers of observed events in data and SM background expectations for each VR, expressed as fractions of the uncertainties on the latter.\\label{tab:vrpull}}
    \\vspace{2mm}
%    \\setlength{\\tabcolsep}{0.0pc}
    {\\scriptsize
    %%
    \\renewcommand\\arraystretch{1.2}
    \\begin{tabular*}{\\textwidth}{@{\\extracolsep{\\fill}}lrrrrrrrrr}
    \\hline
              Signal  &\\multicolumn{9}{c}{Validation Region} \\\\
    \\cline{2-10}
    """

    fin="""
%\\hline

\\end{tabular*}
%%%
}
\\end{center}

\\end{table}
"""

    milieu=""
    for l in    linesForTable:
        milieu+=l+"\n"
        pass

    f=open("SummaryPull.tex","w")
    f.write(debut+milieu+fin)
    f.close()

    return bidim

if __name__ == "__main__":

    import AtlasStyle
    AtlasStyle.SetAtlasStyle()
    from math import *

    main()
