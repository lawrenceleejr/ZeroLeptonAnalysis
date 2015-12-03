#!/usr/bin/env python
import rootpy.ROOT as ROOT
import numpy as np
from rootpy.io import root_open

# from rootpy.plotting import Hist, HistStack, Legend, Canvas, Graph
# from rootpy.plotting.style import get_style, set_style
# from rootpy.plotting.utils import get_limits
# from rootpy.interactive import wait
# from rootpy.io import root_open
# import rootpy.plotting.root2matplotlib as rplt
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# from matplotlib.ticker import AutoMinorLocator, MultipleLocator
# from pylab import *
import os

ROOT.gROOT.SetBatch(True)
import AtlasStyle

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--dataSource" , help="select reco or truth inputs", choices=("truth","reco"), default="truth")
(options, args) = parser.parse_args()

if options.dataSource == 'truth':
    myfiles = {
	'Znunu'  : ROOT.TFile('rundir_truth_znunu_lo.root'),
	'Gamma'  : ROOT.TFile('rundir_truth_gamma.root'),
        }
    reweightfile = ROOT.TFile('ratZG.root')
    reweighthist = reweightfile.Get('met_met50')

elif options.dataSource == 'reco':
    myfiles = {
	'Znunu'  : ROOT.TFile('rundir_reco_zjets/hist-Zjets.root'),
	'Gamma'  : ROOT.TFile('rundir_reco_gamma/hist-GammaJet.root'),
        }
    reweightfile = ROOT.TFile('ratZG_reco.root')
    reweighthist = reweightfile.Get('ratMET_reco')

outputdir =  'plots/'+options.dataSource+'/'

histoList = myfiles['Znunu'].GetListOfKeys()
#histoList.Print()

for counter, histoKey in enumerate(histoList) :
#    def printHisto( key ) :
    histos = {}
    if "PROOF" in histoKey.GetName(): continue
    if "EventLoop" in histoKey.GetName(): continue
    if "Missing" in histoKey.GetName(): continue
    for name, ifile in myfiles.items() :
        hist=ifile.Get(histoKey.GetName())
        if hist.ClassName().startswith("TH2"):
            hist2d = hist
            if( not hist2d ) :
                continue
            if( not hist2d.GetEntries()) :
                continue
            print histoKey.GetName()+ ' ' + str(name) +  ' ' + str(hist2d.GetEntries())
            if name=='Znunu':
                histos[name] = hist2d.ProjectionX(hist2d.GetName()+'_znunu')
            else:
                histos[name] = hist2d.ProjectionX(hist2d.GetName()+'_gamma')
                histos[name+'Reweight'] = hist2d.ProjectionX(hist2d.GetName()+'_gammareweight',1,1)
                histos[name+'Reweight'].Reset()
                for ibin in range(1,hist2d.GetYaxis().GetNbins()+2):
                    projx = hist2d.ProjectionX(hist2d.GetName()+'_gammaproj',ibin,ibin)
                    projx.Scale(reweighthist.GetBinContent(ibin))
                    histos[name+'Reweight'].Add(projx)
                print 'integral:', histos[name].Integral(), '==>', histos[name+'Reweight'].Integral()
        elif hist.ClassName().startswith("TH1"):# and name.startswith('met'):
            histos[name] = hist
            if( not histos[name] ) :
                continue
            if( not histos[name].GetEntries()) :
                continue
            print histoKey.GetName()+ ' ' + str(name) +  ' ' + str(histos[name].GetEntries())

    if( not name in histos ) :
        continue

    c1 = ROOT.TCanvas('c1_'+histoKey.GetName().replace('$',''),
                      'c1_'+histoKey.GetName().replace('$',''),
                      600 , 600
                      )
    c1.Draw()

    pad1 = ROOT.TPad('pad1','pad1',0. ,0.3, 1.,1.)
    pad1.SetBottomMargin(0);
    #pad1.SetGrid(1,1)
    pad1.Draw()
    pad1.SetLogy()
    pad1.cd()

#    histos['Znunu'] = histos['Znunu']
    histos['Znunu'].SetLineColor(ROOT.kRed)
    histos['Znunu'].SetMarkerColor(ROOT.kRed)
    histos['Znunu'].SetMarkerStyle(ROOT.kFullCircle)
    histos['Gamma'].SetMarkerStyle(ROOT.kOpenCircle)

    leg4 = ROOT.TLegend(.6, 0.6, 0.9, 0.8) if 'GammaReweight' in histos.keys() else ROOT.TLegend(.6, 0.6, 0.8, 0.8)
    leg4.SetFillStyle(0)
    leg4.SetBorderSize(0)
    leg4.AddEntry(histos['Znunu'] , 'Znunu')

    if histos['Gamma'].GetNbinsX() ==100 :
        for proc in histos.keys():
            histos[proc].Rebin(4)

    histos['Gamma'].Draw('p')
    histos['Znunu'].Draw('psame')

    ratio = histos['Znunu'].Clone(histos['Znunu'].GetName()+'_ratZg')
    ratio.SetMinimum(0)
    ratio.SetMaximum(2.5)
    #ratio.Sumw2()

    scalef = 1.
    if 'GammaReweight' in histos.keys():
        histos['GammaReweight'].SetLineColor(ROOT.kGreen+2)
        histos['GammaReweight'].SetMarkerColor(ROOT.kGreen+2)
        histos['GammaReweight'].SetMarkerStyle(ROOT.kFullCircle)

        scalef = histos['GammaReweight'].Integral()/histos['Gamma'].Integral() if histos['Gamma'].Integral()>0. else 0.
        histos['Gamma'].Scale(scalef)
        histos['GammaReweight'].Draw('psame')
        leg4.AddEntry(histos['Gamma'] , 'Gamma#bullet{0:.3f}'.format(scalef))
        leg4.AddEntry(histos['GammaReweight'] , 'Gamma#bulletR(Z/#gamma)')
        ratio.Divide(histos['GammaReweight'])
    else:
        leg4.AddEntry(histos['Gamma'] , 'Gamma')
        ratio.Divide(histos['Gamma'])
    leg4.Draw('same')

    c1.cd()
    pad2 = ROOT.TPad('pad2','pad2',0. ,0.0, 1.,0.3  )
    pad2.SetTopMargin(0);
    #pad2.SetGrid(1,1)
    pad2.Draw()
    pad2.cd()

    if 'cutflow' in histos['Znunu'].GetName():
        pad2.SetBottomMargin(0.6)
        pad2.SetRightMargin(0.3)
        pad1.SetRightMargin(0.3)
        histos['Gamma'].SetMinimum(1)

    ratio.GetYaxis().SetTitle('Z / #gamma (reweighted)');
    ratio.GetYaxis().SetNdivisions(505);
    ratio.GetYaxis().SetTitleSize(20);
    ratio.GetYaxis().SetTitleFont(43);
    ratio.GetYaxis().SetTitleOffset(1.55);
    ratio.GetYaxis().SetLabelFont(43);
    ratio.GetYaxis().SetLabelSize(15);

    ratio.GetXaxis().SetTitleSize(20);
    ratio.GetXaxis().SetTitleFont(43);
    ratio.GetXaxis().SetTitleOffset(2.);
    ratio.GetXaxis().SetLabelFont(43);
    ratio.GetXaxis().SetLabelSize(15);
    ratio.GetXaxis().SetTitle(histoKey.GetName().replace('RJVars','').replace('cry_tight','').replace('no_cuts','').replace('_','').replace('$','')) #RJVars_QCD_dPhiR_cry_tight

    ratio.Draw()
    if 'GammaReweight' in histos.keys():
        ratio2 = histos['Gamma'].Clone(histos['Gamma'].GetName()+'_ratGg')
        ratio2.Sumw2()
        ratio2.Divide(histos['GammaReweight'])
        ratio2.Draw('same')
    else:
        ratio.SetMaximum(1)

    c1.cd()
    c1.Print(outputdir+c1.GetName()+'.eps')
    histos = None

#    printHisto(histoKey)

import time
#time.sleep(120)
