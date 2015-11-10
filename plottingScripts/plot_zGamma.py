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

import AtlasStyle

ROOT.gROOT.SetBatch(True)
#AtlasStyle.SetAtlasStyle()

myfiles = {
	'Znunu'  : root_open('../rundir_znunu_lo.root'),
	'Gamma'  : root_open('../rundir_gamma.root'),
}

histoList = myfiles["Znunu"].GetListOfKeys()
#histoList.Print()

for counter, histoKey in enumerate(histoList) :
    def printHisto( key ) :
        histos = {}
        for name, ifile in myfiles.items() :
            histos[name] = ifile.Get(histoKey.GetName())
#   #        histos[name].Print()
            if( not histos[name] ) :
                return None
            if( not histos[name].GetEntries()) :
                return None
            print histoKey.GetName()+ " " + str(name) +  str(histos[name].GetEntries())


        c1 = ROOT.TCanvas("c1_"+histoKey.GetName(),
                          "c1_"+histoKey.GetName(),
                          600 , 600
                          )
        c1.Draw()

        pad1 = ROOT.TPad("pad1","pad1",0. ,0.3, 1.,1.)
        pad1.SetBottomMargin(0);
        pad1.SetGrid(1,1)
        pad1.Draw()
        pad1.SetLogy()
        pad1.cd()

#        histos["Znunu"] = histos["Znunu"]
        histos["Znunu"].SetMarkerColor(ROOT.kRed)
        histos["Znunu"].SetMarkerStyle(ROOT.kFullCircle)
        histos["Gamma"].SetMarkerStyle(ROOT.kFullCircle)

        histos["Gamma"].Draw("p")
        histos["Znunu"].Draw("psame")
        leg4 = ROOT.TLegend(.6, 0.6, 0.8 , 0.8)
        leg4.AddEntry(histos["Gamma"] , "Gamma")
        leg4.AddEntry(histos["Znunu"] , "Znunu")
        leg4.Draw("same")

        c1.cd()
        pad2 = ROOT.TPad("pad2","pad2",0. ,0.0, 1.,0.3  )
        pad2.SetTopMargin(0);
        pad2.SetGrid(1,1)
        pad2.Draw()
        pad2.cd()

        ratio = histos["Znunu"].Clone()
        ratio.SetMinimum(0)
        ratio.SetMaximum(5.0)
        ratio.Sumw2()
        ratio.Divide(histos["Gamma"])


        ratio.GetYaxis().SetTitle("Z / gamma");
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
        ratio.GetXaxis().SetTitle(histoKey.GetName().replace("RJVars","").replace("cry_tight","").replace("no_cuts","").replace("_","")) #RJVars_QCD_dPhiR_cry_tight

        ratio.Draw()

        c1.cd()
        c1.Print("plots/"+c1.GetName()+".eps")
        histos = None
        return

    printHisto(histoKey)

import time
#time.sleep(120)
