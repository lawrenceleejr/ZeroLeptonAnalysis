#!/usr/bin/env python

import ROOT
import numpy as np
from rootpy.plotting import Hist, HistStack, Legend, Canvas, Graph
from rootpy.plotting.style import get_style, set_style
from rootpy.plotting.utils import get_limits
from rootpy.interactive import wait
from rootpy.io import root_open
import rootpy.plotting.root2matplotlib as rplt
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from pylab import *
import os

from ATLASStyle import *

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
# import style_mpl

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

mpl.rcParams['text.latex.preamble'] = [
       r'\usepackage{siunitx}',   # i need upright \micro symbols, but you need...
       r'\sisetup{detect-all}',   # ...this to force siunitx to actually use your fonts
       r'\usepackage{helvet}',    # set the normal font here
       r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
       r'\sansmath'               # <- tricky! -- gotta actually tell tex to use!
]

def chrisZbi(Nsig, Nbkg, g_deltaNbkg = .2) :
	Nobs = Nsig+Nbkg;
	tau = 1./Nbkg/(g_deltaNbkg*g_deltaNbkg);
	aux = Nbkg*tau;
	Pvalue = ROOT.TMath.BetaIncomplete(1./(1.+tau),Nobs,aux+1.);
	return ROOT.TMath.Sqrt(2.)*ROOT.TMath.ErfcInverse(Pvalue*2);

indir201 = "~/eos/atlas/user/l/lduflot/atlasreadable/ZeroLeptonRun2-00-00-57/filtered/"
indir207 = " /afs/cern.ch/work/r/rsmith/public/p2596/"

samplefiles = {
	}

samplefiles["Data"] = { "201" : root_open("".join([indir201,"DataMain.root"])),
			"207" : root_open("".join([indir207,"DataMain.root"])),
	}
samplefiles["Top"] = { "201" : root_open("".join([indir201,"Top.root"])),
		       "207" : root_open("".join([indir207,"Top.root"])),
	}

samples = {
	}

samples["Data"] = { "201" : samplefiles["Data"]["201"].Get("Data_SRAll"),
		    "207" : samplefiles["Data"]["207"].Get("Data_SRAll"),
	}
samples["Top"] = { "201"  : samplefiles["Top"]["201"].Get("Top_SRAll"),
		   "207"  : samplefiles["Top"]["207"].Get("Top_SRAll"),
	}

crtcuts = "1.*(NTVars.nJet>=2 && jetPt[0]>200 && jetPt[1]>50 && NTVars.veto==0 && abs(NTVars.timing)<4)"

varsToPlot = { "met" : {
		"Data" : {
			"201" : None,
			"207" : None
			},
		"Top"  : {
			"201" : None,
			"207" : None
			},
		}, #fill histo after
	       "jetPt"          : {
		"Data" : {
			"201" : None,
			"207" : None
			},
		"Top"  : {
			"201" : None,
			"207" : None
			},
		},
	       "Length$(jetPt)" : {
		"Data" : {
			"201" : None,
			"207" : None
			},
		"Top"  : {
			"201" : None,
			"207" : None
			},
		},
}

lumiscale = 3.24

for datatype, datatypedict in samples.iteritems() :
	for release, reltree in datatypedict.iteritems() :
		weight = "eventWeight*normWeight"
		cutstring = crtcuts + "*" + weight
		for var in varsToPlot.keys() :
			c1 = ROOT.TCanvas()
			color = ('black' if release == '201' else 'red')
			hnew = reltree.Draw(var+">>htemp"+('(20,0,1000)' if (var in ['jetPt', 'met']) else '(15, -.5, 14.5)'),
					    cutstring,
					    linecolor = color,
					    fillcolor = color,
					    markercolor = color,)
			varsToPlot[var][datatype][release] =  hnew
			hnew.SetName     (var+ "_" + datatype+"_"+ release)
			print hnew, hnew.GetEntries()

def makeComparisonCanvas(histList, denomHist = None) :
	if not denomHist : denomHist = histList[-1]
	c1 = ROOT.TCanvas()
	c1.SetGrid(0)

	pad1 = ROOT.TPad("pad1","pad1",0. ,0.3, 1.,1.0  )
	pad1.SetBottomMargin(0);
	pad1.SetGrid(0)
	pad1.Draw()
	pad1.cd()
	pad1.SetLogy(1)

	denomHist.Draw()
	leg = ROOT.TLegend(.5, 0.2, 0.7 , 0.4)
	leg.AddEntry( denomHist , denomHist.GetName())
	for hist in histList :
		hist.Draw("same")
		leg.AddEntry( hist , hist.GetName())
	leg.Draw("same")
#	AtlasUtils.ATLAS_LABELInternal(.6,.8,ROOT.kBlack)

	c1.cd()
	pad2 = ROOT.TPad("pad2","pad2",0. ,0.0, 1.,0.3  )
	pad2.SetTopMargin(0);
	pad2.SetGrid(0)
	pad2.Draw()
	pad2.cd()

	for hist in histList :
		ratio = denomHist.Clone()
		ratio.GetYaxis().SetTitle( hist.GetName() + " " + denomHist.GetName());
		ratio.GetYaxis().SetNdivisions(505);
		ratio.GetYaxis().SetTitleSize(20);
		ratio.GetYaxis().SetTitleFont(43);
		ratio.GetYaxis().SetTitleOffset(1.55);
		ratio.GetYaxis().SetLabelFont(43);
		ratio.GetYaxis().SetLabelSize(15);
		ratio.GetXaxis().SetTitleSize(20);
		ratio.GetXaxis().SetTitleFont(43);
		ratio.GetXaxis().SetTitleOffset(4.);
		ratio.GetXaxis().SetLabelFont(43);
		ratio.GetXaxis().SetLabelSize(15);

		ratio.SetMinimum(.8)
		ratio.SetMaximum(1.2)
		ratio.Sumw2()

		ratio.Divide(hist)
		ratio.Draw()

	c1.Print('plots/' + '_'.join([denomHist.GetName()]+ [i.GetName() for i in histList] +  [".eps"]).replace("$",""))
	for obj in histList + [ratio] :
		obj.Delete()

for varname, histdict in varsToPlot.iteritems() :
	for datatype in samples.keys() :
	        histos = varsToPlot[varname][datatype]
		hist201 = histos['201']
		hist207 = histos['207']
		makeComparisonCanvas([hist207], hist201 )


