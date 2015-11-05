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

reweightfile = ROOT.TFile('ratZG.root')
reweighthist = reweightfile.Get('ratZG_met')
myfiles = {
	'Znunu'  : root_open('rundir_znunu_lo.root'),
	'Gamma'  : root_open('rundir_gamma.root'),
}

outputdir =  'plots/'

histoList = myfiles['Znunu'].GetListOfKeys()
#histoList.Print()

for counter, histoKey in enumerate(histoList) :
#    def printHisto( key ) :
    histos = {}
    for name, ifile in myfiles.items() :
        hist=ifile.Get(histoKey.GetName())
        if hist.ClassName() == "TH2D":
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
                for ibin in range(1,hist2d.GetYaxis().GetNbins()+1):
                    projx = hist2d.ProjectionX(hist2d.GetName()+'_gammaproj',ibin,ibin)
                    projx.Scale(reweighthist.GetBinContent(ibin))
                    histos[name+'Reweight'].Add(projx)
                print 'integral:', histos[name].Integral(), '==>', histos[name+'Reweight'].Integral()
        elif hist.ClassName() == "TH1D":
            histos[name] = hist
            if( not histos[name] ) :
                continue
            if( not histos[name].GetEntries()) :
                continue
            print histoKey.GetName()+ ' ' + str(name) +  ' ' + str(histos[name].GetEntries())

    if( not name in histos ) :
        continue

    c1 = ROOT.TCanvas('c1_'+histoKey.GetName(),
                      'c1_'+histoKey.GetName(),
                      600 , 600
                      )
    c1.Draw()

    pad1 = ROOT.TPad('pad1','pad1',0. ,0.3, 1.,1.)
    pad1.SetBottomMargin(0);
    pad1.SetGrid(1,1)
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

    histos['Gamma'].Draw('p')
    histos['Znunu'].Draw('psame')

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
    else:
        leg4.AddEntry(histos['Gamma'] , 'Gamma')
    leg4.Draw('same')

    c1.cd()
    pad2 = ROOT.TPad('pad2','pad2',0. ,0.0, 1.,0.3  )
    pad2.SetTopMargin(0);
    pad2.SetGrid(1,1)
    pad2.Draw()
    pad2.cd()

    if 'cutflow' in histos['Znunu'].GetName():
        pad2.SetBottomMargin(0.6)
        pad2.SetRightMargin(0.3)
        pad1.SetRightMargin(0.3)

    ratio = histos['Znunu'].Clone()
    ratio.SetMinimum(0)
    ratio.SetMaximum(2.0)
    ratio.Sumw2()
    ratio.Divide(histos['Gamma'])

    ratio.GetYaxis().SetTitle('Z / gamma');
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
    ratio.GetXaxis().SetTitle(histoKey.GetName().replace('RJVars','').replace('cry_tight','').replace('no_cuts','').replace('_','')) #RJVars_QCD_dPhiR_cry_tight

    ratio.Draw()
    if 'GammaReweight' in histos.keys():
        ratio2 = histos['GammaReweight'].Clone()
        ratio2.Sumw2()
        ratio2.Divide(histos['Gamma'])
        ratio2.Draw('same')

    c1.cd()
    c1.Print(outputdir+c1.GetName()+'.eps')
    histos = None

#    printHisto(histoKey)

import time
#time.sleep(120)
