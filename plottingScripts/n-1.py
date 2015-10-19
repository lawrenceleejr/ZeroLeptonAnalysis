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

mpl.rcParams['text.latex.preamble'] = [
       r'\usepackage{siunitx}',   # i need upright \micro symbols, but you need...
       r'\sisetup{detect-all}',   # ...this to force siunitx to actually use your fonts
       r'\usepackage{helvet}',    # set the normal font here
       r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
       r'\sansmath'               # <- tricky! -- gotta actually tell tex to use!
]  


samples = [
			# 'Data',
			# 'QCD',
			'Top',
			'W',
			'Z',
			'Diboson',
			]

lumiscale = 1


colorpal = sns.color_palette("husl", 4 )


colors = {
	'Data': 'black',
	'QCD': 'gray',
	'Top': colorpal[0],
	'W': colorpal[1],
	'Z': colorpal[2],
	'Diboson': colorpal[3],
}

# colors = {
# 	'Data': 'black',
# 	'QCD': 'gray',
# 	'Top': 'red',
# 	'W': 'green',
# 	'Z': 'blue',
# }

myfiles = {
	# 'Data':   'hists/hist-DataMain_periodC.root.root',
	# 'QCD':    'hists/hist-QCD.root.root',
	'Top':    'hists/BG/Top/hist-Top.root.root',
	'W':      'hists/BG/W/hist-Wjets.root.root',
	'Z':      'hists/BG/Z/hist-Zjets.root.root',
	'Diboson':'hists/BG/Diboson/hist-Diboson.root.root',
}



signalsamples = os.listdir("hists/signal/")
# print signalsamples
signalsamples = [x for x in signalsamples if "GG_direct" in x]
# print signalsamples

# plottedsignals =  ["_1100_300_SRAll","_1100_500_SRAll","_1100_700_SRAll" ]
# plottedsignals =  ["_1500_100_SRAll","_1600_0_SRAll","_1100_700_SRAll" ]
# plottedsignals = []

plottedsignals = {}
plottedsignals["SR1"] = ["_800_600","_900_700","_1000_800" ]
plottedsignals["SR2"] = ["_1000_600","_1100_700","_1200_800" ]
plottedsignals["SR3"] = ["_1100_500","_1200_600","_1400_800" ]
plottedsignals["SR4"] = ["_1200_400","_1300_500","_1400_600" ]
plottedsignals["SR5"] = ["_1400_0","_1500_100","_1600_0" ]


# histogramNames = [

# 	]


f = root_open(myfiles['Top'])
# f.ls()
# print [key.GetName() for key in ROOT.gDirectory.GetListOfKeys() if "_minus_" in key.GetName() ]
histogramNames = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys() if "_minus_" in key.GetName()  ]

# myfiles[""]


# style_mpl()
fig = plt.figure(figsize=(6,7.5))

outputFile = open("n-1.tex", 'w')

for histogramName in histogramNames:


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
			hists[sample].Rebin(2)
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
		rplt.bar(stack, stacked=True, axes=axes, yerr=False, alpha=0.5, rasterized=True)
		if hists['Data'].Integral():
			rplt.errorbar(hists['Data'], xerr=False, emptybins=False, axes=axes)
	except:
		# print "no data events..."
		# continue
		pass

	for signalsample in signalsamples:
		skip = 1
		if any([thissig in signalsample for thissig in plottedsignals[histogramName.split("_")[0]  ] ]):
			skip=0
		if skip:
			continue

		signalfile = root_open("hists/signal/%s/hist-GG_direct.root.root"%signalsample)

		hists[signalsample] = signalfile.Get(histogramName).Clone( signalsample )
		hists[signalsample].SetTitle(r"%s"%signalsample.replace("_"," ").replace("SRAll","")  )
		hists[signalsample].Scale(lumiscale)


		if not("nJet" in histogramName) and not("QCD_Delta" in histogramName):
			hists[signalsample].Rebin(4)
		hists[signalsample].color = "red"

		rplt.errorbar(hists[signalsample], axes=axes, yerr=False, xerr=False, alpha=0.9, fmt="--", markersize=0, rasterized=False)

		signalfile.Close()


	print "BG: %f"%stack.sum.Integral()


	# leg = plt.legend(loc="best")
	axes.annotate(r'\textbf{\textit{ATLAS}} Internal',xy=(0.05,0.95),xycoords='axes fraction') 
	axes.annotate(r'$\int{L}\sim$ %d pb$^{-1}$, $\sqrt{s}$=13 TeV, N-1, %s'%(lumiscale, histogramName.split("_")[0] ),xy=(0.0,1.01),xycoords='axes fraction') 


	cutvalue = histogramName.split(">")[-1].split("<")[-1]
	if cutvalue[0]=="0":
		cutvalue = "0."+cutvalue[1:]
	cutvalue = float(cutvalue)
	boxDirection = 1 if ">" in histogramName else -1

	axes.plot( (cutvalue,cutvalue), (1e-10,1), 'g-' , alpha=0.8)
	axes.plot( (cutvalue,cutvalue*1e10*boxDirection), (1,1), 'g-' , alpha=0.8)
	axes.text( cutvalue, 0.01, 'Cut at %.2f'%cutvalue, color="k", size=10, va="top", ha="center", rotation=90)

	# axes_ratio.set_xlabel(histogramName.replace("_"," ").replace(">","$>$").replace("<","$<$") )



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
	axes_ratio.set_xlabel(histogramName.replace("_"," ").replace(">","$>$").replace("<","$<$") )
	axes_ratio.set_ylabel('Data/MC')

	print "saving"
	fig.savefig("N-1Plots/%s.png"%histogramName, dpi=100)

	outputFile.write(r"""
\begin{figure}[tbph]
\begin{center}
\includegraphics[width=0.49\textwidth]{figures/N-1Plots/%s}
\end{center}
\caption{N-1 Plots for %s}
\label{fig:%s}
\end{figure}


		"""%(histogramName, histogramName.split("_")[0], histogramName.translate(None, "<>")  )


		)

