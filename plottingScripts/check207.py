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

import AtlasStyle
import AtlasUtils

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
indir207 = "/afs/cern.ch/work/r/rsmith/public/"

samplefiles = {
	}

samplefiles["Data"] = { "201" : root_open("".join([indir201,"DataMain.root"])),
			"207" : root_open("".join([indir207,"p2613/DataMain.root"])),
	}
samplefiles["Top"] = { "201" : root_open("".join([indir201,"Top.root"])),
		       "207" : root_open("".join([indir207,"p2596/Top.root"])),
	}

print samplefiles

samples = {
	}

samples["Data"] = { "201" : samplefiles["Data"]["201"].Get("Data_SRAll"),
		    "207" : samplefiles["Data"]["207"].Get("Data_SRAll"),
	}
samples["Top"] = { "201"  : samplefiles["Top"]["201"].Get("Top_SRAll"),
		   "207"  : samplefiles["Top"]["207"].Get("Top_SRAll"),
	}

print samples

cutlists = {#NTVars.nJet>=2 &&
	"presel" : "1.*( jetPt[0]>200 && jetPt[1]>50 && NTVars.veto==0 && abs(NTVars.timing)<4 && (NTVars.cleaning&3) == 0 && meffInc > 800 && met > 200)",
	"sr2jl"  : "(jetPt[0]>=200.0 &&  jetPt[1]>=200.0 && NTVars.veto==0 && (abs(NTVars.timing)<4) && ((NTVars.cleaning&3) == 0) && met/sqrt(meffInc-met) >= 15.000000 && meffInc >= 1200.000000 )" #
}

crtcuts = cutlists['presel']

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

	       "meffInc" : {
		"Data" : {
			"201" : None,
			"207" : None
			},
		"Top"  : {
			"201" : None,
			"207" : None
			},
		}, #fill histo after


	       # "metSoftTerm" : {
	       # 	"Data" : {
	       # 		"201" : None,
	       # 		"207" : None
	       # 		},
	       # 	"Top"  : {
	       # 		"201" : None,
	       # 		"207" : None
	       # 		},
	       # 	}, #fill histo after
	       "jetPt[0]"          : {
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

lumiscale = 3240

for datatype, datatypedict in samples.iteritems() :
	for release, reltree in datatypedict.iteritems() :
		weight = "normWeight*eventWeight" if (not "Data" in datatype) else "1."
		print datatype, weight
		cutstring = crtcuts + "*" + weight
		for var in varsToPlot.keys() :
			c1 = ROOT.TCanvas()
			color = ('blue' if release == '201' else 'red')

			hnew = reltree.Draw(var+">>htemp"+('(20,200,1200)' if
							   (var in ['jetPt[0]', 'met','meffInc']) else ('(15,0,300)'
													if "metSoftTerm" in var
													else  '(15, -.5, 14.5)') ),
					    cutstring,
					    linecolor = color,
					    fillcolor = color,
					    markercolor = color,)
			varsToPlot[var][datatype][release] =  hnew
			hnew.SetName     (var+ "_" + datatype+"_"+ release)
			hnew.Scale(lumiscale)
			print hnew, hnew.Integral()

def makeComparisonCanvas(histList, denomHist = None, mainTitle = "", ratioTitle = "", xAxisTitle = ""  ) :
	if not denomHist : denomHist = histList[-1]
	c1 = ROOT.TCanvas()
	c1.SetFrameBorderMode(0);
	c1.SetGrid(0,0)

	pad1 = ROOT.TPad("pad1","pad1",0. ,0.3, 1.,1.0  )
	pad1.SetBottomMargin(.001);
	pad1.SetGrid(0,0)
	pad1.Draw()
	pad1.cd()
	pad1.SetLogy(1)

	denomHist.Draw()
	leg = ROOT.TLegend(.7, 0.6, 0.9 , 0.8)
	leg.AddEntry( denomHist , denomHist.GetName().split('_')[-1])
	for hist in histList :
		hist.Draw("same")
		hist.GetYaxis().SetTitle( mainTitle if mainTitle else "Events" )
		leg.AddEntry( hist , hist.GetName().split('_')[-1])
	leg.Draw("same")
	AtlasUtils.ATLAS_LABEL(.7,.85,ROOT.kBlack, "Internal")

	c1.cd()
	pad2 = ROOT.TPad("pad2","pad2",0. ,0, 1.,0.3  )
	pad2.SetTopMargin(0);
	pad2.SetBottomMargin(.2);
	pad2.SetGrid(0,1)
	pad2.Draw()
	pad2.cd()

	for hist in histList :
		ratio = denomHist.Clone()
		ratio.GetYaxis().SetTitle(( ratioTitle if ratioTitle else (hist.GetName() + " " + denomHist.GetName())))
		ratio.SetMarkerColor(ROOT.kBlack);
		ratio.SetLineColor  (ROOT.kBlack);
		ratio.GetYaxis().SetNdivisions(505);
		ratio.GetYaxis().SetTitleSize(20);
		ratio.GetYaxis().SetTitleFont(43);
		ratio.GetYaxis().SetTitleOffset(1.55);
		ratio.GetYaxis().SetLabelFont(43);
		ratio.GetYaxis().SetLabelSize(15);

		ratio.GetXaxis().SetTitle(xAxisTitle)
		ratio.GetXaxis().SetTitleSize(20);
		ratio.GetXaxis().SetTitleFont(43);
#		ratio.GetXaxis().SetTitleOffset();
		ratio.GetXaxis().SetLabelFont(43);
		ratio.GetXaxis().SetLabelSize(15);

		ratio.SetMinimum(.9)
		ratio.SetMaximum(1.1)
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
		makeComparisonCanvas([hist207], hist201 , ratioTitle = "20.1 / 20.7",
				     xAxisTitle = varname + (" (GeV) " if varname in ['jetPt[0]', 'met', 'meffInc']  else "") )


