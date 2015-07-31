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


# style_mpl()
fig = plt.figure(figsize=(10,5), dpi=100)


histogramName = "cutflow"

plt.clf()

hists = {}
histsToStack = []
stack = HistStack()

for sample in samples:
	f = root_open(myfiles[sample])
	# f.ls()
	hists[sample] = f.Get(histogramName).Clone(sample)
	hists[sample].Sumw2()
	hists[sample].SetTitle(r"%s"%sample)
	# hists[sample].fillstyle = 'solid'
	hists[sample].fillcolor = colors[sample]
	hists[sample].linecolor = colors[sample]
	hists[sample].linewidth = 2
	hists[sample].Scale(1./hists[sample].GetBinContent(1) )
	if sample != 'Data':
		histsToStack.append( hists[sample] )
	else:
		hists[sample].markersize = 1.2

sortedHistsToStack = sorted(histsToStack, key=lambda x: x.Integral() , reverse=False)


axes = plt.subplot()
axes.set_yscale('log')


axes.set_xticks(np.arange(21)+0.5 )
# ax.set_xticklabels( ('G1', 'G2', 'G3', 'G4', 'G5') )
axes.set_xticklabels( [
	r"1",
	r"met 100",
	r"MDeltaR 300"   ,
	r"P0 Jet1 pT 150."   ,
	r"P1 Jet1 pT 150."   ,
	r"P0 Jet2 pT 110."   ,
	r"P1 Jet2 pT 110."   ,
	r"QCD Rpt 0.3",
	r"QCD Delta1*QCD Rpsib -0.7"   ,
	r"P0 PInvHS 0.25"   ,
	r"P1 PInvHS 0.25"   ,
	r"0.3 dphiVG 2.7"   ,
	r"-0.75 C0 CosTheta 0.8"   ,
	r"-0.75 C1 CosTheta 0.8"   ,
	r"-0.7 G0 CosTheta 0.7"   ,
	r"-0.7 G1 CosTheta 0.7"   ,
	r"-0.8 cos(P0 dPhiGC) 0.7",
	r"-0.8 cos(P1 dPhiGC) 0.7",
	r"abs(CosThetaPP) 0.9"   ,
	r"VisShape 0.1"   ,
	r"MP 800"   ,
	], rotation=90 )

for tmphist in sortedHistsToStack:
	if tmphist.Integral():
		stack.Add(tmphist)
		rplt.hist(tmphist, alpha=0.5, emptybins=False)



rplt.errorbar(hists['Data'], xerr=False, emptybins=False, axes=axes)

ylim([1e-17,2])
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.35)






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
		hists[signalsample].Scale(1./hists[sample].GetBinContent(1)  )
		hists[signalsample].color = "red"
		rplt.errorbar(hists[signalsample], axes=axes, yerr=False, xerr=False, alpha=0.9, fmt="--", markersize=0)
		print "%s %f"%(signalsample, hists[signalsample].Integral()  )
	except:
		continue


print "BG: %f"%stack.sum.Integral()


# leg = plt.legend(loc="best")
axes.annotate(r'\textbf{\textit{ATLAS}} Internal',xy=(0.3,0.05),xycoords='axes fraction') 
axes.annotate(r'$\sqrt{s}$=13 TeV',xy=(0.5,0.05),xycoords='axes fraction') 



# get handles
handles, labels = axes.get_legend_handles_labels()
# remove the errorbars
# handles = [h[0] for h in handles]
for myhandle in handles:
	try:
		myhandle = myhandle[0]
	except:
		pass

# use them in the legend
axes.legend(handles, labels, loc='best',numpoints=1)



axes.set_ylabel('Cut Flow Efficiency')

plt.show()


print "saving"
fig.savefig("N-1_plots/%s.pdf"%histogramName)


