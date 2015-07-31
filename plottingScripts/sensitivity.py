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
		# "jet1pt",
		# "jet2pt",
		"met",
		"meffInc",
		"Ap",
		# "nJet",
		# "RJVars_SS_Mass",
		"RJVars_SS_MDeltaR",
		"RJVars_G_0_PInvHS",
		"RJVars_G_0_CosTheta",
		"RJVars_G_0_Jet2_pT",
		"RJVars_SS_CosTheta",
		"RJVars_DeltaBetaGG",
		"RJVars_QCD_Rpt",
		# # "RJVars_QCD_Delta2",
		"RJVars_QCD_Delta1_x_Rpsib",
		# "cosRJVars_G_0_dPhiGC",
		"RJVars_dphiVG",
		# "RJVars_V1_N",
		# "RJVars_I1_Depth",
		"RJVars_MG",
	]

cuts = [
		# "no_cut",
		# "l1trigger",
		# "hlttrigger",
		# "sr1",
		# "sr2",
		# "sirop_1200_400_tight",
		# "sirop_1200_400_loose",
		"sirop_1200_800",
		# "sirop_tight"

]


# style_mpl()
fig = plt.figure(figsize=(6,7.5), dpi=100)

for (tmphist,tmpcut) in [(x,y) for x in histogramNames for y in cuts]:
	histogramName = tmphist+"_"+tmpcut

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



from ROOT import RooStats

DeltaBG = 0.2
MGCut = 1300

for DeltaBG in [0.2,0.4]:
	for MGCut in [600,700,800,900,1000]:

		plt.clf()
		BG = stack.sum.Integral( stack.sum.FindBin(MGCut), -1 )
		print BG

		x = []
		y = []
		z = []

		for signalsample in signalsamples:
			print signalsample
			# signalfile = root_open("hists/rundir_signal/"+signalsample)
			# print signalfile.ls()
			try:
				signalfile = root_open("hists/rundir_signal/"+signalsample)
				sig =  signalfile.Get("RJVars_MG_sirop_1200_800").Clone( signalsample )
				sig = sig.Integral( sig.FindBin(MGCut), -1 )
				print BG
				print sig*lumiscale
			except:
				continue
			print sig
			print "-------------------------------------"
			if sig:
				myx = float(signalsample.split("direct_")[-1].split("_")[0])
				myy = float(signalsample.split("direct_")[-1].split("_")[1].split(".")[0]  )
				myz = RooStats.NumberCountingUtils.BinomialExpZ(sig*lumiscale, BG, DeltaBG)
				print myx, myy, myz
				print sig*lumiscale, BG
				if myz==float('inf') or myz > 20:
					myz = 20
				if myz < 0:
					myz = 0
				if myx<500:
					continue
				if myz!=float('inf') and myz>0:
					x.append(myx)
					y.append(myy)
					z.append(myz)
					print myz
			signalfile.Close()

		# print x, y, z
		for thing in [400,500,600,700,800,900,1000,1100,1200]:
			x.append(thing)
			y.append(thing)
			z.append(0)


		import scipy.interpolate



		x = np.array(x)
		y = np.array(y)
		z = np.array(z)

		print x

		xi, yi = np.linspace(x.min(), x.max(), 100), np.linspace(y.min(), y.max(), 100)
		xi, yi = np.meshgrid(xi, yi)

		# print x
		# print y
		# print z

		rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
		zi = rbf(xi, yi)

		figSens = plt.figure(  figsize=(8,5), dpi=100  )

		plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], cmap='jet', alpha=0.8)
		plt.colorbar(label=r"Discovery z Value [$\sigma$]")

		CS = plt.contour(zi, [1,2,3,4,5], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="black")
		plt.clabel(CS, fontsize=9, inline=1, colors="white", linecolor="white")

		plt.scatter(x, y, c=z)

		plt.xlabel(r"$m_{\tilde{g}}$ [GeV]")
		plt.ylabel(r"$m_{\chi^0_1}$ [GeV]")
		axes = plt.gca()
		axes.set_xlim([400,1800])
		axes.set_ylim([0,1200])

		plt.annotate(r"$\Delta$BG/BG=%.1f"%DeltaBG,xy=(620,70),color="white") 
		plt.annotate(r"$\int L \sim 10$ fb$^{-1}, 13$ TeV",xy=(620,20), color="white") 
		# plt.show()



		figSens.savefig("plots/massPlaneSensitivity_%d_%d.pdf"%(MGCut,DeltaBG*10) )









