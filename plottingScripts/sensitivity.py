#!/usr/bin/env python


import ROOT
import numpy as np
from rootpy import asrootpy
from rootpy.plotting import Hist, HistStack, Legend, Canvas, Graph
from rootpy.plotting.style import get_style, set_style
from rootpy.plotting.utils import get_limits
from rootpy.interactive import wait
from rootpy.io import root_open
import rootpy.plotting.root2matplotlib as rplt
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from pylab import *
import os

from ATLASStyle import *

from interpolateGrid import *

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



# Config ##########################################################


samples = [
			# 'Data',
			# 'QCD',
			'Top',
			'W',
			'Z',
			'Diboson'
			]

lumiscale = 4
writePlots = True
combineRegions = 1

SignalGrid = "GG_direct"

# MeffRegions = 0
MeffRegions = [
"SR2jl",
"SR2jm",
"SR2jt",
"SR4jt",
"SR5j",
"SR6jm",
"SR6jt",
]


cuts = [
		"SR1A",
		"SR1B",
		"SR1C",
		"SR2A",
		"SR2B",
		"SR2C",
		"SR3A",
		"SR3B",
		"SR3C",
] + MeffRegions


# DeltaBGs = [0.2]

DeltaBGs = {}
DeltaBGs["BaselineSyst"] = {}

for cut in cuts:
	DeltaBGs["BaselineSyst"][cut] = 0.1 if "SR2j" in cut else 0.2

colorpal = sns.color_palette("husl", 4 )


colors = {
	'Data': 'black',
	'QCD': 'gray',
	'Top': colorpal[0],
	'W': colorpal[1],
	'Z': colorpal[2],
	'Diboson': colorpal[3],
}


myfiles = {
	# 'Data':   'hists/hist-DataMain_periodC.root.root',
	# 'QCD': 'hists/output/hist-QCD.root.root',
	'Top': 'hists/output/Top/hist-Top.root.root',
	'W': 'hists/output/W/hist-Wjets.root.root',
	'Z': 'hists/output/Z/hist-Zjets.root.root',
	'Diboson':'hists/output/Diboson/hist-Diboson.root.root',
}


signalsamples = os.listdir("hists/output/")
signalsamples = [x for x in signalsamples if SignalGrid in x]
signalsamples = [x for x in signalsamples if "SRAll" in x]


histogramNames = [
		"MET",
	]


fig = plt.figure(figsize=(6,7.5), dpi=100)

from ROOT import RooStats

for DeltaBG in DeltaBGs:

	print DeltaBG

	bestZbi = {}
	bestmeffZbi = {}

	for tmpcut in cuts:


		for tmphist in histogramNames:
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
				# if not("nJet" in histogramName)  and not("QCD_Delta" in histogramName):
				# 	hists[sample].Rebin(4)
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

		plt.clf()
		BG = stack.sum.Integral()
		# print "nBG:    %f --------"%BG

		x = []
		y = []
		z = []

		print tmpcut
		# print len(signalsamples)

		for signalsample in signalsamples:
			# print signalsample
			# signalfile = root_open("hists/rundir_signal/"+signalsample)
			# print signalfile.ls()
			try:
				signalfile = root_open("hists/output/%s/hist-%s.root.root"%(signalsample,SignalGrid))
				sig =  signalfile.Get("MET_%s"%tmpcut ).Clone( signalsample )
				sig.Scale(lumiscale)
				sig = sig.Integral( )
				# print BG
				# print sig
			except:
				continue

			myx = float(signalsample.split("direct_")[-1].split("_")[0])
			myy = float(signalsample.split("direct_")[-1].split("_")[1].split(".")[0]  )
			# print DeltaBGs[DeltaBG][cut]
			# print DeltaBG[tmpcut]
			myz = RooStats.NumberCountingUtils.BinomialExpZ(sig, BG, DeltaBGs[DeltaBG][tmpcut])

			# print myx, myy, myz
			# print sig, BG, myz
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
				# print myz

			# if compareToMeff != tmpcut:
			try:
				if not(tmpcut in MeffRegions) and myz > bestZbi[(myx,myy)][0] and BG>1:
					bestZbi[(myx,myy)] = (myz,tmpcut)

				if tmpcut in MeffRegions and myz > bestmeffZbi[(myx,myy)][0]  and BG>1:
					bestmeffZbi[(myx,myy)] = (myz,tmpcut)

			except:
				if tmpcut in MeffRegions:
					bestmeffZbi[(myx,myy)] = (myz,tmpcut)
				else:
					bestZbi[(myx,myy)] = (myz,tmpcut)



			signalfile.Close()

		(x,y,z,xi,yi,zi) = interpolateGridArray(x,y,z)

		figSens = plt.figure(  figsize=(8,5), dpi=100  )

		plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], cmap='jet', alpha=0.8)


		plt.colorbar(label=r"Discovery z Value [$\sigma$]")

		CS = plt.contour(zi, [2,3,4,5], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="black")
		plt.clabel(CS, fontsize=9, inline=1, colors="white", linecolor="white", fmt='%1.0f $\\sigma$')

		plt.scatter(x, y, c=z)

		plt.xlabel(r"$m_{\tilde{g}}$ [GeV]")
		plt.ylabel(r"$m_{\chi^0_1}$ [GeV]")
		axes = plt.gca()
		axes.set_xlim([400,1800])
		axes.set_ylim([0,1200])


		plt.annotate(r'\textbf{\textit{ATLAS}} Internal',xy=(0.7,1.01),xycoords='axes fraction') 

		plt.annotate(r"$\Delta$BG/BG=%.1f, %s"%(DeltaBGs[DeltaBG][tmpcut],tmpcut),xy=(420,1150),color="white") 
		plt.annotate(r"$\int L \sim %.1f$ fb$^{-1}, 13$ TeV"%(lumiscale),xy=(420,1100), color="white") 
		if writePlots:
			figSens.savefig("plots/massPlaneSensitivity_%d_%d_%s.png"%(DeltaBGs[DeltaBG][tmpcut]*10,lumiscale,tmpcut) )



	if MeffRegions:

		plt.clf()

		(x,y,z,zSR,xi,yi,zi) = interpolateGridDictionary(bestZbi,bestmeffZbi)

		plt.imshow(zi, vmin=-2, vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], cmap='jet', alpha=0.8)
		plt.colorbar(label=r"Difference in Discovery z Value [$\sigma$]")

		CS = plt.contour(zi, [-0.5,0.1,0.5,1,1.5], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="black")
		plt.clabel(CS, fontsize=9, inline=1, colors="white", linecolor="white", fmt='%+1.1f $\\sigma$')

		plt.scatter(x, y, c=z)

		plt.xlabel(r"$m_{\tilde{g}}$ [GeV]")
		plt.ylabel(r"$m_{\chi^0_1}$ [GeV]")
		axes = plt.gca()
		axes.set_xlim([400,1800])
		axes.set_ylim([0,1200])

		plt.annotate(r'\textbf{\textit{ATLAS}} Internal',xy=(0.7,1.01),xycoords='axes fraction') 

		plt.annotate(r"$\Delta$BG/BG=%s, Best SR Z - Best MEff SR Z"%(DeltaBG)  ,xy=(420,1150),color="white") 
		plt.annotate(r"$\int L \sim %.1f$ fb$^{-1}, 13$ TeV"%(lumiscale),xy=(420,1100), color="white") 
		# plt.show()

		if writePlots:
			# figSens.savefig("plots/massPlaneSensitivity_%d_%d_CompareToBestMeff.pdf"%(DeltaBG*10,lumiscale) )
			figSens.savefig("plots/massPlaneSensitivity_%s_%d_CompareToBestMeff.png"%(DeltaBG,lumiscale) )




	if combineRegions:

		plt.clf()

		(x,y,z,zSR,xi,yi,zi)=interpolateGridDictionary(bestZbi)

		plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], cmap='jet', alpha=0.8)
		plt.colorbar(label=r"Discovery z Value [$\sigma$]")

		CS = plt.contour(zi, [2,3,4,5], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="black")
		plt.clabel(CS, fontsize=9, inline=1, colors="white", linecolor="white", fmt='%1.0f $\\sigma$')

		plt.scatter(x, y, c=z)

		plt.xlabel(r"$m_{\tilde{g}}$ [GeV]")
		plt.ylabel(r"$m_{\chi^0_1}$ [GeV]")
		axes = plt.gca()
		axes.set_xlim([400,1800])
		axes.set_ylim([0,1200])

		plt.annotate(r'\textbf{\textit{ATLAS}} Internal',xy=(0.7,1.01),xycoords='axes fraction') 

		plt.annotate(r"$\Delta$BG/BG=%s, Best SR"%DeltaBG,xy=(420,1150),color="white") 
		plt.annotate(r"$\int L \sim %.1f$ fb$^{-1}, 13$ TeV"%(lumiscale),xy=(420,1100), color="white") 
		# plt.show()

		if writePlots:
			# figSens.savefig("plots/massPlaneSensitivity_%d_%d_BestSR.pdf"%(DeltaBG*10,lumiscale) )
			figSens.savefig("plots/massPlaneSensitivity_%s_%d_BestSR.png"%(DeltaBG,lumiscale) )


		#with chosen SR
		plt.clf()
		CS = plt.contour(zi, [2,3,4,5], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="black")
		plt.clabel(CS, fontsize=9, inline=1, colors="black", fmt='%1.0f $\\sigma$')

		for i,j,k in zip(x,y,zSR):
			plt.annotate(k, xy=(i,j), size=6, horizontalalignment='center', verticalalignment='center' )

		plt.xlabel(r"$m_{\tilde{g}}$ [GeV]")
		plt.ylabel(r"$m_{\chi^0_1}$ [GeV]")
		axes = plt.gca()
		axes.set_xlim([400,1800])
		axes.set_ylim([0,1200])

		plt.annotate(r'\textbf{\textit{ATLAS}} Internal',xy=(0.7,1.01),xycoords='axes fraction') 

		plt.annotate(r"$\Delta$BG/BG=%s, Best SR"%DeltaBG,xy=(420,1150)) 
		plt.annotate(r"$\int L \sim %.1f$ fb$^{-1}, 13$ TeV"%(lumiscale),xy=(420,1100)) 
		# plt.show()

		if writePlots:
			# figSens.savefig("plots/massPlaneSensitivity_%d_%d_BestSR_Text.pdf"%(DeltaBG*10,lumiscale) )
			figSens.savefig("plots/massPlaneSensitivity_%s_%d_BestSR_Text.png"%(DeltaBG*10,lumiscale) )




		####### Plotting best Meff regions #############################

		plt.clf()

		(x,y,z,zSR,xi,yi,zi)=interpolateGridDictionary(bestmeffZbi)

		print zSR 

		plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], cmap='jet', alpha=0.8)
		plt.colorbar(label=r"Discovery z Value [$\sigma$]")

		CS = plt.contour(zi, [2,3,4,5], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="black")
		plt.clabel(CS, fontsize=9, inline=1, colors="white", linecolor="white", fmt='%1.0f $\\sigma$')

		plt.scatter(x, y, c=z)

		plt.xlabel(r"$m_{\tilde{g}}$ [GeV]")
		plt.ylabel(r"$m_{\chi^0_1}$ [GeV]")
		axes = plt.gca()
		axes.set_xlim([400,1800])
		axes.set_ylim([0,1200])

		plt.annotate(r'\textbf{\textit{ATLAS}} Internal',xy=(0.7,1.01),xycoords='axes fraction') 

		plt.annotate(r"$\Delta$BG/BG=%s, Best MEff SR"%DeltaBG,xy=(420,1150),color="white") 
		plt.annotate(r"$\int L \sim %.1f$ fb$^{-1}, 13$ TeV"%(lumiscale),xy=(420,1100), color="white") 
		# plt.show()

		if writePlots:
			# figSens.savefig("plots/massPlaneSensitivity_%d_%d_BestSR.pdf"%(DeltaBG*10,lumiscale) )
			figSens.savefig("plots/massPlaneSensitivity_%s_%d_BestMEffSR.png"%(DeltaBG,lumiscale) )


		#with chosen SR
		plt.clf()
		CS = plt.contour(zi, [2,3,4,5], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="black")
		plt.clabel(CS, fontsize=9, inline=1, colors="black", fmt='%1.0f $\\sigma$')


		print zSR
		for i,j,k in zip(x,y,zSR):
			plt.annotate(k, xy=(i,j), size=6, horizontalalignment='center', verticalalignment='center' )

		plt.xlabel(r"$m_{\tilde{g}}$ [GeV]")
		plt.ylabel(r"$m_{\chi^0_1}$ [GeV]")
		axes = plt.gca()
		axes.set_xlim([400,1800])
		axes.set_ylim([0,1200])

		plt.annotate(r'\textbf{\textit{ATLAS}} Internal',xy=(0.7,1.01),xycoords='axes fraction') 

		plt.annotate(r"$\Delta$BG/BG=%s, Best MEff SR"%DeltaBG,xy=(420,1150)) 
		plt.annotate(r"$\int L \sim %.1f$ fb$^{-1}, 13$ TeV"%(lumiscale),xy=(420,1100)) 
		# plt.show()

		if writePlots:
			# figSens.savefig("plots/massPlaneSensitivity_%d_%d_BestSR_Text.pdf"%(DeltaBG*10,lumiscale) )
			figSens.savefig("plots/massPlaneSensitivity_%s_%d_BestMEffSR_Text.png"%(DeltaBG,lumiscale) )












