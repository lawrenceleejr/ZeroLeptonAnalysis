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

from copy import deepcopy

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

lumiscale = 3.26
# lumiscale = 1.9
writePlots = True
combineRegions = 1

SignalGrids = ["SS_direct"]
# SignalGrids = ["GG_direct"]
# SignalGrids = ["SS_direct","GG_direct"]
# SignalGrids = ["GG_onestepCC"]


myxlabel = {}
myxlabel["SS_direct"] = r"$m_{\tilde{q}}$ [GeV]"
myxlabel["GG_direct"] = r"$m_{\tilde{g}}$ [GeV]"
myxlabel["GG_onestepCC"] = r"$m_{\tilde{g}}$ [GeV]"

# MeffRegions = 0
MeffRegions = [
# "SR2jCo",
# "SR2jl",
# "SR2jm",
# "SR2jt",
# "SR4jt",
# "SR5j",
# "SR6jm",
# "SR6jt",
]


cuts = [
		# "SR1ASq",
		# "SR1BSq",
		# "SR2ASq",
		# "SR2BSq",
		# "SR3ASq",
		# "SR3BSq",

		# "SR1A",
		# "SR1B",
		# "SR1C",
		# "SR2A",
		# "SR2B",
		# "SR2C",
		# # "SR2D",
		# "SR3A",
		# "SR3B",
		# "SR3C",


		"SR1ACo",
		# "SR1BCo",
		# "SR2ACo",
		# "SR2BCo",
		# "SR3ACo",
		# "SR3BCo",
		# "SR4ACo",
		# "SR4BCo",

] + MeffRegions


# DeltaBGs = [0.2]

DeltaBGs = {}
DeltaBGs["BaselineSyst"] = {}

for cut in cuts:
	DeltaBGs["BaselineSyst"][cut] = 0.1 if ("SR2j" in cut or "Sq" in cut or "Co" in cut) else 0.2

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



histogramNames = [
		"MET",
	]


fig = plt.figure(figsize=(6,7.5), dpi=300)

from ROOT import RooStats

for SignalGrid in SignalGrids:


	signalsamples = os.listdir("hists/output/")
	signalsamples = [x for x in signalsamples if SignalGrid in x]
	signalsamples = [x for x in signalsamples if "SRAll" in x]


	if SignalGrid == "GG_onestepCC":
		signalsamples = [x for x in signalsamples if (int(x.split("_")[2])+int(x.split("_")[4]) )/2 == int(x.split("_")[3])  ]
		# print signalsamples


	DeltaBG = "BaselineSyst"

	bestZbi = {}
	bestmeffZbi = {}

	for tmpcut in cuts:
		print tmpcut

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
			# if not("400_375" in signalsample):
			# 	continue

			if ("400_0" in signalsample):
				continue
			print signalsample

			# signalfile = root_open("hists/rundir_signal/"+signalsample)
			# print signalfile.ls()
			try:
				signalfile = root_open("hists/output/%s/hist-%s.root.root"%(signalsample,SignalGrid))
				sig =  signalfile.Get("MET_%s"%tmpcut ).Clone( signalsample )
				sig.Scale(lumiscale)
				if SignalGrid == "SS_direct":
					sig.Scale(0.8)
				sig = sig.Integral( )
				# print BG
				# print sig
			except:
				print "Problem getting signal: %s" % signalsample
				continue

			myx = float(signalsample.split("_")[2])
			myy = float(signalsample.split("_")[3].split(".")[0]  )

			if SignalGrid == "GG_onestepCC":
				myy = float(signalsample.split("_")[4].split(".")[0]  )


			# print DeltaBGs[DeltaBG][cut]
			# print DeltaBG[tmpcut]
			myz = RooStats.NumberCountingUtils.BinomialExpZ(sig, BG, DeltaBGs[DeltaBG][tmpcut])

			# print myx, myy, myz
			print sig, BG, myz
			if myz==float('inf') or myz > 20:
				myz = 20
			if myz < 0:
				myz = 0
			# if myx<500:
			# 	continue
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

		xarray, yarray, zarray = deepcopy(x),deepcopy(y),deepcopy(z)

		(x,y,z,xi,yi,zi) = interpolateGridArray(x,y,z,withZeros=1)

		figSens = plt.figure(  figsize=(8,5), dpi=300  )

		plt.imshow(zi, vmin=0, vmax=7, origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], cmap='jet', alpha=0.8)


		plt.colorbar(label=r"Discovery z Value [$\sigma$]")


		CS = plt.contour(zi, [2,3,4,5], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="black")
		# CS = plt.tricontour(xi, yi, zi, 15, linewidths=0.5, colors='k')

		plt.clabel(CS, fontsize=9, inline=1, colors="black", linecolor="black", fmt='%1.0f $\\sigma$')


		(x,y,z,xi,yi,zi) = interpolateGridArray(xarray,yarray,zarray,withZeros=0)

		plt.scatter(x, y, c=z, vmin=0, vmax=7, cmap='jet')

		plt.xlabel(myxlabel[SignalGrid])
		plt.ylabel(r"$m_{\chi^0_1}$ [GeV]")
		axes = plt.gca()
		axes.set_xlim([400,1800])
		axes.set_ylim([0,1200])


		plt.annotate(r'\textbf{\textit{ATLAS}} Internal',xy=(0.7,1.01),xycoords='axes fraction') 

		plt.annotate(r"$\Delta$BG/BG=%.1f, %s, %s"%(DeltaBGs[DeltaBG][tmpcut],tmpcut,SignalGrid.translate(None, "_") ),xy=(420,1150),color="white") 
		plt.annotate(r"$\int L \sim %.1f$ fb$^{-1}, 13$ TeV"%(lumiscale),xy=(420,1100), color="white") 
		if writePlots:
			figSens.savefig("plots/massPlaneSensitivity_%s_%d_%d_%s.png"%(SignalGrid,DeltaBGs[DeltaBG][tmpcut]*10,lumiscale,tmpcut) , dpi=100)



	if MeffRegions:

		plt.clf()

		(x,y,z,zSR,xi,yi,zi) = interpolateGridDictionary(bestZbi,bestmeffZbi, withZeros=1)

		# mymin, mymax = -1,2
		# plt.tricontourf(xi, yi, zi, np.linspace(mymin, mymax, 100), cmap='jet' )
		# cb = plt.colorbar(label=r"Difference in Discovery z Value [$\sigma$]", ticks=np.linspace(mymin, mymax,  (mymax-mymin)*2+1  )    )
		# CS = plt.tricontour(xi, yi, zi, levels=[-0.5,0,0.5,1,1.5], colors='k')


		plt.imshow(zi, vmin=-1, vmax=4, origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], cmap='jet', alpha=0.8)
		plt.colorbar(label=r"Difference in Discovery z Value [$\sigma$]")
		CS = plt.contour(zi, [-0.5,0,0.5,1,1.5,2.0], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="black")


		plt.clabel(CS, fontsize=9, inline=1, colors="black", linecolor="black", fmt='%+1.1f $\\sigma$')

		(x,y,z,zSR,xi,yi,zi) = interpolateGridDictionary(bestZbi,bestmeffZbi, withZeros=0)


		plt.scatter(x, y, c=z, vmin=-1, vmax=4, cmap='jet')

		plt.xlabel(myxlabel[SignalGrid])
		plt.ylabel(r"$m_{\chi^0_1}$ [GeV]")
		axes = plt.gca()
		axes.set_xlim([400,1800])
		axes.set_ylim([0,1200])

		plt.annotate(r'\textbf{\textit{ATLAS}} Internal',xy=(0.7,1.01),xycoords='axes fraction') 

		plt.annotate(r"$\Delta$BG/BG=%s, Best SR Z - Best MEff SR Z, %s"%(DeltaBG,SignalGrid.translate(None, "_") )  ,xy=(420,1150),color="white") 
		plt.annotate(r"$\int L \sim %.1f$ fb$^{-1}, 13$ TeV"%(lumiscale),xy=(420,1100), color="white") 
		# plt.show()

		if writePlots:
			figSens.savefig("plots/massPlaneSensitivity_%s_%s_%d_CompareToBestMeff.png"%(SignalGrid,DeltaBG,lumiscale) ,dpi=300)




	if combineRegions:

		plt.clf()

		# (x,y,z,zSR,xi,yi,zi)=interpolateGridDictionary(bestZbi)
		(x,y,z,zSR,xi,yi,zi)=interpolateGridDictionary(bestZbi,withZeros=1)



		plt.imshow(zi, vmin=0, vmax=7, origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], cmap='jet', alpha=0.8)
		plt.colorbar(label=r"Discovery z Value [$\sigma$]")


		# mymin, mymax = 0,7
		# plt.tricontourf(xi, yi, zi, np.linspace(mymin, mymax, 100), cmap='jet' )
		# cb = plt.colorbar(label=r"Discovery z Value [$\sigma$]", ticks=np.linspace(mymin, mymax,  (mymax-mymin)*2+1  )    )
		# CS = plt.tricontour(xi, yi, zi, levels=[2,3,4,5], colors='k')

		CS = plt.contour(zi, [2,3,4,5], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="black")
		# # CS = plt.tricontour(xi, yi, zi, 15, linewidths=0.5, colors='k')

		plt.clabel(CS, fontsize=9, inline=1, colors="black", linecolor="black", fmt='%1.0f $\\sigma$')

		(x,y,z,zSR,xi,yi,zi)=interpolateGridDictionary(bestZbi,withZeros=0)


		plt.scatter(x, y, c=z, vmin=0, vmax=7, cmap='jet')

		plt.xlabel(myxlabel[SignalGrid])
		plt.ylabel(r"$m_{\chi^0_1}$ [GeV]")
		axes = plt.gca()
		axes.set_xlim([400,1800])
		axes.set_ylim([0,1200])

		plt.annotate(r'\textbf{\textit{ATLAS}} Internal',xy=(0.7,1.01),xycoords='axes fraction') 

		plt.annotate(r"$\Delta$BG/BG=%s, Best SR, %s"%(DeltaBG,SignalGrid.translate(None, "_") ),xy=(420,1150),color="white") 
		plt.annotate(r"$\int L \sim %.1f$ fb$^{-1}, 13$ TeV"%(lumiscale),xy=(420,1100), color="white") 
		# plt.show()

		if writePlots:
			figSens.savefig("plots/massPlaneSensitivity_%s_%s_%d_BestSR.png"%(SignalGrid,DeltaBG,lumiscale) , dpi=300)


		#with chosen SR
		plt.clf()

		(x,y,z,zSR,xi,yi,zi)=interpolateGridDictionary(bestZbi,withZeros=1)


		# mymin, mymax = 0,7
		# plt.tricontourf(xi, yi, zi, np.linspace(mymin, mymax, 100), cmap='jet' )
		# cb = plt.colorbar(label=r"Discovery z Value [$\sigma$]", ticks=np.linspace(mymin, mymax,  (mymax-mymin)*2+1  )    )
		# CS = plt.tricontour(xi, yi, zi, levels=[2,3,4,5], colors='k')


		CS = plt.contour(zi, [2,3,4,5], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="black")
		plt.clabel(CS, fontsize=9, inline=1, colors="black", fmt='%1.0f $\\sigma$')

		for i,j,k in zip(x,y,zSR):
			if i==j:
				continue
			plt.annotate(k, xy=(i,j), size=6, horizontalalignment='center', verticalalignment='center' )

		plt.xlabel(myxlabel[SignalGrid])
		plt.ylabel(r"$m_{\chi^0_1}$ [GeV]")
		axes = plt.gca()
		axes.set_xlim([400,1800])
		axes.set_ylim([0,1200])

		plt.annotate(r'\textbf{\textit{ATLAS}} Internal',xy=(0.7,1.01),xycoords='axes fraction') 

		plt.annotate(r"$\Delta$BG/BG=%s, Best SR, %s"%(DeltaBG,SignalGrid.translate(None, "_") ),xy=(420,1150)) 
		plt.annotate(r"$\int L \sim %.1f$ fb$^{-1}, 13$ TeV"%(lumiscale),xy=(420,1100)) 
		# plt.show()

		if writePlots:
			figSens.savefig("plots/massPlaneSensitivity_%s_%s_%d_BestSR_Text.pdf"%(SignalGrid,DeltaBG,lumiscale) )




		####### Plotting best Meff regions #############################

		plt.clf()

		(x,y,z,zSR,xi,yi,zi)=interpolateGridDictionary(bestmeffZbi,withZeros=1)

		print zSR 


		# mymin, mymax = 0,7
		# plt.tricontourf(xi, yi, zi, np.linspace(mymin, mymax, 100), cmap='jet' )
		# cb = plt.colorbar(label=r"Discovery z Value [$\sigma$]", ticks=np.linspace(mymin, mymax,  (mymax-mymin)*2+1  )    )
		# CS = plt.tricontour(xi, yi, zi, levels=[2,3,4,5], colors='k')



		plt.imshow(zi, vmin=0, vmax=7, origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], cmap='jet', alpha=0.8)
		plt.colorbar(label=r"Discovery z Value [$\sigma$]")

		CS = plt.contour(zi, [2,3,4,5], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="black")
		plt.clabel(CS, fontsize=9, inline=1, colors="black", linecolor="black", fmt='%1.0f $\\sigma$')

		(x,y,z,zSR,xi,yi,zi)=interpolateGridDictionary(bestmeffZbi,withZeros=0)

		plt.scatter(x, y, c=z, vmin=0, vmax=7, cmap='jet')

		plt.xlabel(myxlabel[SignalGrid])
		plt.ylabel(r"$m_{\chi^0_1}$ [GeV]")
		axes = plt.gca()
		axes.set_xlim([400,1800])
		axes.set_ylim([0,1200])

		plt.annotate(r'\textbf{\textit{ATLAS}} Internal',xy=(0.7,1.01),xycoords='axes fraction') 

		plt.annotate(r"$\Delta$BG/BG=%s, Best MEff SR, %s"%(DeltaBG,SignalGrid.translate(None, "_") ),xy=(420,1150),color="white") 
		plt.annotate(r"$\int L \sim %.1f$ fb$^{-1}, 13$ TeV"%(lumiscale),xy=(420,1100), color="white") 
		# plt.show()

		if writePlots:
			figSens.savefig("plots/massPlaneSensitivity_%s_%s_%d_BestMEffSR.png"%(SignalGrid,DeltaBG,lumiscale) ,dpi=300)


		#with chosen SR
		plt.clf()

		(x,y,z,zSR,xi,yi,zi)=interpolateGridDictionary(bestmeffZbi,withZeros=1)

		CS = plt.contour(zi, [2,3,4,5], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="black")


		# CS = plt.tricontour(xi, yi, zi, levels=[2,3,4,5], colors='k')

		plt.clabel(CS, fontsize=9, inline=1, colors="black", fmt='%1.0f $\\sigma$')


		print zSR
		for i,j,k in zip(x,y,zSR):
			if i==j:
				continue
			plt.annotate(k, xy=(i,j), size=6, horizontalalignment='center', verticalalignment='center' )

		plt.xlabel(myxlabel[SignalGrid])
		plt.ylabel(r"$m_{\chi^0_1}$ [GeV]")
		axes = plt.gca()
		axes.set_xlim([400,1800])
		axes.set_ylim([0,1200])

		plt.annotate(r'\textbf{\textit{ATLAS}} Internal',xy=(0.7,1.01),xycoords='axes fraction') 

		plt.annotate(r"$\Delta$BG/BG=%s, Best MEff SR, %s"%(DeltaBG,SignalGrid.translate(None, "_") ),xy=(420,1150)) 
		plt.annotate(r"$\int L \sim %.1f$ fb$^{-1}, 13$ TeV"%(lumiscale),xy=(420,1100)) 
		# plt.show()

		if writePlots:
			figSens.savefig("plots/massPlaneSensitivity_%s_%s_%d_BestMEffSR_Text.pdf"%(SignalGrid,DeltaBG,lumiscale) )












