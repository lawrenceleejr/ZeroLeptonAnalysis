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

# import style_mpl

import seaborn as sns
sns.set(style="whitegrid")

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)


samples = [
			'Data',
			'QCD',
			'Top',
			'W+Jets',
			'Z+Jets'
			]

lumiscale = 10000/3.5


colorpal = sns.color_palette("husl", 3 )


colors = {
	'Data': 'black',
	'QCD': 'gray',
	'Top': colorpal[0],
	'W+Jets': colorpal[1],
	'Z+Jets': colorpal[2],
}

# colors = {
# 	'Data': 'black',
# 	'QCD': 'gray',
# 	'Top': 'red',
# 	'W+Jets': 'green',
# 	'Z+Jets': 'blue',
# }

myfiles = {
	'Data': 'hists/rundir_data.root',
	'QCD': 'hists/rundir_qcd.root',
	'Top': 'hists/rundir_top.root',
	'W+Jets': 'hists/rundir_wjets.root',
	'Z+Jets': 'hists/rundir_zjets.root',
}


signalsamples = os.listdir("hists/rundir_signal")
signalsamples = [x for x in signalsamples if "GG_direct" in x]

plottedsignals =  ["_1150_250." , "_1150_450." , "_1150_650." , "_1150_850." ]

histogramNames = [

	"met",
	"NTRJigsawVars.RJVars_SS_MDeltaR"   ,
	"NTRJigsawVars.RJVars_G_0_Jet1_pT"   ,
	"NTRJigsawVars.RJVars_G_1_Jet1_pT"   ,
	"NTRJigsawVars.RJVars_G_0_Jet2_pT"   ,
	"NTRJigsawVars.RJVars_G_1_Jet2_pT"   ,
	"abs(NTRJigsawVars.RJVars_SS_CosTheta)"   ,
	"NTRJigsawVars.RJVars_G_0_PInvHS"   ,
	"NTRJigsawVars.RJVars_G_1_PInvHS"   ,
	"NTRJigsawVars.RJVars_G_0_CosTheta"   ,
	"NTRJigsawVars.RJVars_G_1_CosTheta"   ,
	"NTRJigsawVars.RJVars_C_0_CosTheta"   ,
	"NTRJigsawVars.RJVars_C_1_CosTheta"   ,
	"cos(NTRJigsawVars.RJVars_G_0_dPhiGC)",
	"cos(NTRJigsawVars.RJVars_G_1_dPhiGC)",
	"NTRJigsawVars.RJVars_DeltaBetaGG" ,
	"NTRJigsawVars.RJVars_dphiVG" ,
	"NTRJigsawVars.RJVars_QCD_Rpt",
	"NTRJigsawVars.RJVars_QCD_Delta1xNTRJigsawVars.RJVars_QCD_Rpsib"   ,
	"NTRJigsawVars.RJVars_MG"   ,

	]

cuts = [
		# "no_cut",
		# "l1trigger",
		# "hlttrigger",
		# "sr1",
		# "sr2",
		# "sirop_1200_400_tight",
		# "sirop_1200_400_loose",
		# "sirop_1200_600_noMDR",
		"sirop_tight"

]


# style_mpl()
fig = plt.figure(figsize=(6,7.5), dpi=100)

for (tmphist,tmpcut) in [(x,y) for x in histogramNames for y in cuts]:
	# histogramName = tmphist+"_"+tmpcut

	histogramName = "sirop_tight_minus_%s"%tmphist

	plt.clf()

	hists = {}
	histsToStack = []
	stack = HistStack()

	for sample in samples:
		f = root_open(myfiles[sample])
		# f.ls()
		hists[sample] = f.Get(histogramName).Clone(sample)
		hists[sample].Sumw2()
		if not("nJet" in histogramName)  and not("QCD_Delta" in histogramName):
			hists[sample].Rebin(4)
			# hists[sample].Rebin(100)
		hists[sample].SetTitle(r"%s"%sample)
		hists[sample].fillstyle = 'solid'
		hists[sample].fillcolor = colors[sample]
		hists[sample].linewidth = 0
		hists[sample].Scale(lumiscale)
		if sample != 'Data':
			histsToStack.append( hists[sample] )
		else:
			hists[sample].markersize = 1.2

	# print histsToStack[0].Integral()
	# print histsToStack
	sortedHistsToStack = sorted(histsToStack, key=lambda x: x.Integral() , reverse=False)
	# print sortedHistsToStack

	for tmphist in sortedHistsToStack:
		if tmphist.Integral():
			stack.Add(tmphist)




	gs = mpl.gridspec.GridSpec(2,1,height_ratios=[4,1])
	gs.update(wspace=0.00, hspace=0.00)
	axes = plt.subplot(gs[0])
	axes_ratio = plt.subplot(gs[1], sharex=axes)
	plt.setp(axes.get_xticklabels(), visible=False)

	# axes = plt.subplot()




	try:
		axes.set_yscale('log')
		rplt.bar(stack, stacked=True, axes=axes, yerr=False, alpha=0.5, )
		if hists['Data'].Integral():
			rplt.errorbar(hists['Data'], xerr=False, emptybins=False, axes=axes)
	except:
		# print "no data events..."
		# continue
		pass

	for signalsample in signalsamples:
		skip = 1
		if any([thissig in signalsample for thissig in plottedsignals]):
			skip=0
		if skip:
			continue
		signalfile = root_open("hists/rundir_signal/"+signalsample)
		try:
			hists[signalsample] = signalfile.Get(histogramName).Clone( signalsample )
			hists[signalsample].SetTitle(r"%s"%signalsample.replace("_"," ").split(".")[4].split("MadGraphPythia8EvtGen ")[1]    )
			hists[signalsample].Scale(lumiscale)
			if not("nJet" in histogramName) and not("QCD_Delta" in histogramName):
				hists[signalsample].Rebin(4)
				# hists[signalsample].Rebin(100)
			hists[signalsample].color = "red"
			rplt.errorbar(hists[signalsample], axes=axes, yerr=False, xerr=False, alpha=0.9, fmt="--", markersize=0)
			print "%s %f"%(signalsample, hists[signalsample].Integral()  )
		except:
			continue
		# signalfile.Close()


	print "BG: %f"%stack.sum.Integral()


	# leg = plt.legend(loc="best")
	axes.annotate(r'\textbf{\textit{ATLAS}} Internal',xy=(0.05,0.9),xycoords='axes fraction') 
	axes.annotate(r'$\int{L}\sim$ %d pb$^{-1}$, $\sqrt{s}$=13 TeV, N-1'%(3.5*lumiscale),xy=(0.3,0.82),xycoords='axes fraction') 



	# get handles
	handles, labels = axes.get_legend_handles_labels()
	# remove the errorbars
	handles = [h[0] for h in handles]
	# use them in the legend
	axes.legend(handles, labels, loc='best',numpoints=1)


	if 'Data' in hists:
		ratioplot = Graph.divide(  Graph(hists['Data']), stack.sum , 'pois'  )
		ratioplot.color = "black"
		axes_ratio.errorbar(list(ratioplot.x()) , 
							list(ratioplot.y()), 
							yerr=[ x[0] for x in list(ratioplot.yerr() ) ] , 
							# xerr=list(ratioplot.y()), 
							fmt='o',
							color="black")

		yticks(arange(0,2.0,0.2))
		ylim([0,2])

	axes.set_ylabel('Events')
	axes_ratio.set_xlabel(histogramName.replace("_"," ") )
	axes_ratio.set_ylabel('Data/MC')

	print "saving"
	fig.savefig("N-1_plots/%s.pdf"%histogramName)


