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

indir201 = "/working/rsmith/v57_sys/"
indir207 = "/working/rsmith/v103_sys/"

samplefiles = {
	"Data" : { "201" : root_open("".join([indir201,"DataMain_data15_13TeV.root"])),
		   "207" : root_open("".join([indir207,"DataMain_data15_13TeV.root"])),	},

	"Z"    : { "201" : root_open("".join([indir201,"Zjets.root"])),
		   "207" : root_open("".join([indir207,"Zjets.root"])),                },

	"QCD"    : { "201" : root_open("".join([indir201,"QCD.root"])),
		     "207" : root_open("".join([indir207,"QCD.root"])),                },

	"W"    : { "201" : root_open("".join([indir201,"Wjets.root"])),
		   "207" : root_open("".join([indir207,"Wjets.root"])),                },

	"Top"    : { "201" : root_open("".join([indir201,"Top.root"])),
		     "207" : root_open("".join([indir207,"Top.root"])),                },

	"GAMMA"    : { "201" : root_open("".join([indir201,"GammaJet.root"])),
		       "207" : root_open("".join([indir207,"GammaJet.root"])),                },
	}

samples = {
	}

samples["Data"] = { "201" : samplefiles["Data"]["201"].Get("Data_SRAll"),
		    "207" : samplefiles["Data"]["207"].Get("Data_SRAll"),
	}
samples["Z"] = {   "201"  : samplefiles["Z"]["201"].Get("Z_SRAll"),
		   "207"  : samplefiles["Z"]["207"].Get("Z_SRAll"),
	}
samples["QCD"] = { "201"  : samplefiles["QCD"]["201"].Get("QCD_SRAll"),
		   "207"  : samplefiles["QCD"]["207"].Get("QCD_SRAll"),
	}

samples["Top"] = {"201"  : samplefiles["Top"]["201"].Get("Top_SRAll"),
		  "207"  : samplefiles["Top"]["207"].Get("Top_SRAll"),
		  }

samples["GAMMA"] = {"201"  : samplefiles["GAMMA"]["201"].Get("GAMMA_SRAll"),
		  "207"  : samplefiles["GAMMA"]["207"].Get("GAMMA_SRAll"),
		  }

samples["W"] = {"201"  : samplefiles["W"]["201"].Get("W_SRAll"),
		"207"  : samplefiles["W"]["207"].Get("W_SRAll"),
		  }
print samples

def cleaning(tree, is201 = True) :
	cleanDict = {
		'SRAll'   : "((cleaning&(3))==0)",
		'CRWT' : "((cleaning&(15))==0)",
		'CRZ'  : "((cleaning&(7))==0)",
		'CRY'  : "((cleaning&(15))==0)",
		'CRQ'  : "((cleaning&(3))==0)",
		} if is201  else {
		'SRAll' : "((cleaning&(3+0x80))==0)",
		'CRWT' : "((cleaning&(15+256))==0)",
		'CRZ' : "((cleaning&(7+0x80))==0)",
		'CRY' : "((cleaning&(15+512))==0)",
		'CRQ' : "((cleaning&(3+0x80))==0)",
		}
	return cleanDict[tree]

def runNumberCut(is201 = True, isData = False ) :
	if isData : return ''
	runNumberCut = '(RunNumber >=361444 && RunNumber <= 361467)' if is201 else '(RunNumber >=363415 && RunNumber <= 363435)'
	return runNumberCut

cutlists = {#NTVars.nJet>=2 &&
	"presel" : "1.*( pT_jet1>200 && pT_jet2>50 && veto==0 && abs(timing)<4       && Meff > 800 && MET > 200)",
	"sr2jl"   : "(pT_jet1>=200.0 &&  pT_jet2>=200.0 && veto==0 && (abs(timing)<4) && MET/sqrt(Meff-MET) >= 15.000000 && Meff >= 1200.000000 )",
	"manfredi": "(pT_jet1>=200.0 &&  pT_jet2>=200.0 && veto==0 && (abs(timing)<4) && MET/sqrt(Meff-MET) >= 15.000000 && Meff >= 1200.000000 )", #
}

crtcuts = cutlists['manfredi']

varsToPlot = {}
listOfVars = ['MET', 'Meff', 'pT_jet1', 'NJet']
#listOfVars = ['Meff', 'pT_jet1']
for var in listOfVars :
	varsToPlot[var] = {}
	for treename in samples.keys() :
		varsToPlot[var][treename] = {"201" : None ,
					     "207" : None
					     }

lumiscale = 3240

for datatype, datatypedict in samples.iteritems() :
	for release, reltree in datatypedict.iteritems() :
		weight      = "weight" if (not "Data" in datatype) else "1."
		cleanString = cleaning( reltree.GetName().split('_')[1] , '201' in release)
		cutstring   = crtcuts + "*" + cleanString + '*' + weight #'*' + runCut
		print datatype, release , cutstring
		for var in varsToPlot.keys() :
			c1 = ROOT.TCanvas()
			color = ('blue' if release == '201' else 'red')

			hnew = reltree.Draw(var+">>htemp"+('(20,200,1200)' if
							   (var in ['pT_jet1', 'MET','Meff']) else ('(15,0,300)'
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
	denomHist.Delete()
	for obj in histList + [ratio] :
		obj.Delete()

for varname, histdict in varsToPlot.iteritems() :
	for datatype in samples.keys() :
	        histos = varsToPlot[varname][datatype]
		hist201 = histos['201']
		hist207 = histos['207']
		makeComparisonCanvas([hist207], hist201 , ratioTitle = "20.1 / 20.7",
				     xAxisTitle = varname + (" (GeV) " if varname in ['pT_jet1', 'MET', 'Meff']  else "") )


