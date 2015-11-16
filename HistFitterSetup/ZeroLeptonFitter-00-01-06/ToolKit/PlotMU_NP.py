#!/usr/bin/env python
"""
This python script is plotting mu and theta parameters for all SRs simultaneouly.

Usage:
python ToolKit/MakePullPlots.py
python ToolKit/PlotMU_NP.py
"""
import sys
import math
import copy
import pickle
import ROOT
from ChannelsDict import *
from ZLFitterConfig import *
import os

from ZLFitterConfig import *
zlFitterConfig = ZLFitterConfig()

ROOT.gROOT.SetBatch(True) # Turn off online histogram drawing

plots = {}
dMU = {}
dNP = {}
hNP = {}


def MakeBox(color=ROOT.kGreen,offset=0,ymin=-1,ymax=1):
    graph = ROOT.TGraph(4);
    graph.SetPoint(0,0.3+offset,ymin);
    graph.SetPoint(1,0.3+offset,ymax);
    graph.SetPoint(2,0.7+offset,ymax);
    graph.SetPoint(3,0.7+offset,ymin);    
    graph.SetFillColor(color); 
    graph.SetLineColor(2);
    graph.SetLineWidth(5);
    graph.SetLineStyle(1);
    return graph


def main():
    ## Get list of mu parameters (present in all SRs)
    for channel in sorted(finalChannelsDict.keys()):
        if not os.path.exists("MU_%s.pkl" % channel):
            continue
        
        try:
            fMU = open('MU_%s.pkl' % channel,'r')
        except:
            print "Could not open MU_%s.pkl" % channel
            continue


        theList = pickle.load(fMU)
        print theList
        print "========="

        for item in theList:
            #if not 'Yield' in item[0]: continue
            if not item[0] in dMU: dMU[item[0]] = {}
            dMU[item[0]][channel] = [item[1],item[2]]
            #print item[0],channel,dMU[item[0]][channel],item
        fMU.close()
       
        try:
            fNP = open('NP_%s.pkl' % channel,'r')
        except:
            print "Could not open NP_%s.pkl" % channel
            continue
        
        theList = pickle.load(fNP)
        for item in theList:
            if not item[0] in dNP: dNP[item[0]] = {}
            dNP[item[0]][channel] = [item[1],item[2]]
            #print item[0],channel,dNP[item[0]][channel],item
        fNP.close()
    
    ## Prepare MU histograms
    nChannels = len(finalChannelsDict.keys())
    for mu in dMU:
        print mu
        print sorted(dMU[mu].keys())
        print sorted(finalChannelsDict.keys())
        if len(dMU[mu].keys()) != nChannels:
            print "nChannels = %d, len(dMU) = %d" % (nChannels, len(dMU[mu].keys()))
            continue
        hname = 'MU_%s' % mu
        print hname
        dMU[mu]['hist'] = ROOT.TH1F(hname,hname,nChannels,0,nChannels)
        dMU[mu]['histbis'] = ROOT.TH1F(hname,hname,nChannels,0,nChannels)
        dMU[mu]['hist'].GetYaxis().SetTitle('#mu(%s)' % zlFitterConfig.getSampleNiceName(mu))
        dMU[mu]['hist'].GetXaxis().SetLabelSize(0.02)
        dMU[mu]['hist'].SetFillColor(zlFitterConfig.getSampleColor(mu))
        dMU[mu]['histbis'].SetLineColor(ROOT.kRed)
        dMU[mu]['histbis'].SetLineWidth(1)
        for bin,channel in enumerate(sorted(finalChannelsDict)):
            dMU[mu]['hist'].SetBinContent(bin+1,dMU[mu][channel][0])
            dMU[mu]['hist'].SetBinError(bin+1,dMU[mu][channel][1])
            dMU[mu]['hist'].GetXaxis().SetBinLabel(bin+1,channel[2:])
            dMU[mu]['histbis'].SetBinContent(bin+1,dMU[mu][channel][0])
            dMU[mu]['histbis'].SetBinError(bin+1,0.0001)
    
    ## Prepare NP histograms
    for ichan,channel in enumerate(sorted(finalChannelsDict.keys())):
        hname = 'hNP_%s' % channel
        print hname
        hNP[hname] = ROOT.TH2F(hname,hname,len(dNP.keys()),0,len(dNP.keys()),14,-2.25,2.25)
        hNP[hname].GetYaxis().SetTitle(channel[2:])
        hNP[hname].GetYaxis().CenterTitle(True)
        hNP[hname].GetYaxis().SetNdivisions(503)
        hNP[hname].GetXaxis().SetLabelOffset(0.02)
        hNP[hname].GetXaxis().SetLabelSize(0.1)
        if ichan < nChannels - 1:
            hNP[hname].GetYaxis().SetTitleOffset(0.2)
            hNP[hname].GetYaxis().SetTitleSize(0.2)
            hNP[hname].GetYaxis().SetLabelSize(0.2)
        else:
            hNP[hname].GetYaxis().SetTitleOffset(0.7)
            hNP[hname].GetYaxis().SetTitleSize(0.05)
            hNP[hname].GetYaxis().SetLabelSize(0.05)
        for bin,np in enumerate(sorted(dNP)):
            hNP[hname].GetXaxis().SetBinLabel(bin+1,np)
        hNP[hname].GetXaxis().LabelsOption("v")
    return

if __name__ == "__main__":
    main()

    import AtlasStyle
    AtlasStyle.SetAtlasStyle()
    from math import *
    
    # #MUZ/W plot
    # for k,v in dMU["W"].items():
    #    if k.find("hist")>=0: continue
    #    print "toto",k,(dMU["W"][k][0]-dMU["Z"][k][0])/dMU["Z"][k][0],(dMU["W"][k][0]-dMU["Z"][k][0])/sqrt(pow(dMU["W"][k][1],2)+pow(dMU["Z"][k][1],2))

    
    ## MU plot
    plots['MU'] = {}
    plots['MU']['canvas'] = ROOT.TCanvas('cMU','cMU')
    canvas = plots['MU']['canvas']
    plots['MU']['pads'] = []
    for ipad in range(len(dMU.keys())):
        width = (0.95 - 0.05) / len(dMU.keys())
        ymax = 0.95 - ipad * width
        ymin = 0.95 - (ipad + 1) * width
        if ipad == len(dMU.keys()) - 1: ymin = ymin - 0.025
        plots['MU']['pads'].append(ROOT.TPad("MU_%d" % (ipad+1),"MU_%d" % (ipad+1),0.001,ymin,0.995,ymax))
        pad = plots['MU']['pads'][ipad]
        pad.SetFillColor(0)
        pad.SetBorderMode(0)
        pad.SetBorderSize(2)
        pad.SetTicks()
        pad.SetTopMargin(0.05)
        pad.SetRightMargin(0.15)
        if ipad != len(dMU.keys()) - 1:
            pad.SetBottomMargin(0.)
        else:
            pad.SetBottomMargin(0.30)
        pad.SetLeftMargin(0.10)
        pad.SetFrameBorderMode(0)
        pad.SetFrameBorderMode(0)
        pad.Draw()
    
    for imu,mu in enumerate(dMU.keys()):
        pad = plots['MU']['pads'][imu]
        pad.cd()

        if not mu in dMU:
            continue

        if not 'hist' in dMU[mu]:
            continue

        dMU[mu]['hist'].GetXaxis().SetLabelOffset(0.02)
        dMU[mu]['hist'].GetXaxis().SetLabelSize(0.11)
        dMU[mu]['hist'].GetYaxis().SetTitleOffset(0.25)
        dMU[mu]['hist'].GetYaxis().SetTitleSize(0.15)
        dMU[mu]['hist'].GetYaxis().SetLabelSize(0.15)
        dMU[mu]['hist'].GetYaxis().SetNdivisions(505)
        dMU[mu]['hist'].GetYaxis().CenterTitle(True)
        if 'Top' in mu:
            dMU[mu]['hist'].GetYaxis().SetRangeUser(-0.25,4.)
        elif not 'Multijets' in mu:
            dMU[mu]['hist'].GetYaxis().SetRangeUser(-0.25,1.75)
        dMU[mu]['hist'].Draw('E2')
        dMU[mu]['histbis'].Draw('E SAME')
        if not 'Multijets' in mu:
            dMU[mu]['line'] = ROOT.TLine(0.,1.,len(finalChannelsDict.keys()),1.)
            dMU[mu]['line'].SetLineColor(ROOT.kRed) 
            dMU[mu]['line'].SetLineStyle(2) 
            dMU[mu]['line'].SetLineWidth(2) 
            dMU[mu]['line'].Draw() 
    canvas.Print('summaryMU.eps')
    canvas.Print('summaryMU.png')
    # canvas.Print('summaryMU.pdf')

    ## NP plot
    nChannels = len(finalChannelsDict.keys())
    plots['NP'] = {}
    plots['NP']['canvas'] = ROOT.TCanvas('cNP','cNP',600,800)
    canvas = plots['NP']['canvas']
    plots['NP']['pads'] = []
    for ipad,channel in enumerate(sorted(finalChannelsDict.keys())):
        width = (0.95 - 0.25) / nChannels
        ymax = 0.95 - ipad * width
        ymin = 0.95 - (ipad + 1) * width
        if ipad == nChannels - 1: ymin = ymin - 0.2
        plots['NP']['pads'].append(ROOT.TPad("NP_%d" % (ipad+1),"NP_%d" % (ipad+1),0.001,ymin,0.995,ymax))
        pad = plots['NP']['pads'][ipad]
        pad.SetFillColor(0)
        pad.SetBorderMode(0)
        pad.SetBorderSize(2)
        pad.SetTicks()
        pad.SetTopMargin(0.)
        pad.SetRightMargin(0.15)
        if ipad != nChannels - 1:
            pad.SetBottomMargin(0.)
        else:
            pad.SetBottomMargin(0.7)
        pad.SetLeftMargin(0.10)
        pad.SetFrameBorderMode(0)
        pad.SetFrameBorderMode(0)
        pad.Draw()
    for ipad,channel in enumerate(sorted(finalChannelsDict.keys())):
        pad = plots['NP']['pads'][ipad]
        pad.cd()
        hNP['hNP_%s' % channel].Draw()
        hNP['graph_%s' % channel] = []
        for inp,np in enumerate(sorted(dNP.keys())):
            if not channel in dNP[np]: continue
            y = dNP[np][channel][0]
            ey = dNP[np][channel][1]
            color = ROOT.kGreen-9
            if ey < 0.5: color = ROOT.kRed-7
            elif ey < 0.8 or ey > 1.2: color = ROOT.kOrange
            elif math.fabs(y/ey) > 0.2: color = ROOT.kOrange
            graph=MakeBox(offset=inp,ymin=y-ey,ymax=y+ey,color=color)
            hNP['graph_%s' % channel].append(copy.deepcopy(graph))
        for graph in hNP['graph_%s' % channel]:
            graph.Draw("LF")
    canvas.Print('summaryNP.eps')
    canvas.Print('summaryNP.png')
    # canvas.Print('summaryNP.pdf')
