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

lumiscale = 1
writePlots = True
combineRegions = 1

# SignalGrids = ["SS_direct","GG_direct"]
SignalGrids = ["GG_direct"]
# SignalGrids = ["GG_onestepCC"]


myxlabel = {}
myxlabel["SS_direct"] = r"$m_{\tilde{q}}$ [GeV]"
myxlabel["GG_direct"] = r"$m_{\tilde{g}}$ [GeV]"
myxlabel["GG_onestepCC"] = r"$m_{\tilde{g}}$ [GeV]"


MeffRegions = [

]


cuts = [
		"SRJigsawSR1Loose",
] + MeffRegions


colorpal = sns.color_palette("husl", 4 )





fig = plt.figure(figsize=(6,7.5), dpi=100)

from ROOT import RooStats


import json

for SignalGrid in SignalGrids:

	bestZbi = {}
	bestmeffZbi = {}

	for tmpcut in cuts:


		with open('JSON/SRJigsawSR1Loose_GG_direct__1_harvest_list.json') as data_file:    
		    data = json.load(data_file)


		plt.clf()

		x = []
		y = []
		z = []

		print tmpcut

		for ipoint in data:

			myx = ipoint["m1"]
			myy = ipoint["m2"]
			myz = ROOT.RooStats.PValueToSignificance( ipoint["p0"] )

			x.append(myx)
			y.append(myy)
			z.append(myz)


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

		(x,y,z,xi,yi,zi) = interpolateGridArray(x,y,z)

		figSens = plt.figure(  figsize=(8,5), dpi=100  )

		plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], cmap='jet', alpha=0.8)


		plt.colorbar(label=r"Discovery z Value [$\sigma$]")

		CS = plt.contour(zi, [2,3,4,5], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="black")
		plt.clabel(CS, fontsize=9, inline=1, colors="white", linecolor="white", fmt='%1.0f $\\sigma$')

		plt.scatter(x, y, c=z)

		plt.xlabel(myxlabel[SignalGrid])
		plt.ylabel(r"$m_{\chi^0_1}$ [GeV]")
		axes = plt.gca()
		axes.set_xlim([400,1800])
		axes.set_ylim([0,1200])


		plt.annotate(r'\textbf{\textit{ATLAS}} Internal',xy=(0.7,1.01),xycoords='axes fraction') 

		plt.annotate(r"HistFitter, %s, %s"%(tmpcut,SignalGrid.translate(None, "_") ),xy=(420,1150),color="white") 
		plt.annotate(r"$\int L \sim %.1f$ fb$^{-1}, 13$ TeV"%(lumiscale),xy=(420,1100), color="white") 
		if writePlots:
			figSens.savefig("plots/massPlaneSensitivity_%s_HF_%d_%s.png"%(SignalGrid,lumiscale,tmpcut) )


	test = {}
	test["jd"]


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
			figSens.savefig("plots/massPlaneSensitivity_%s_%s_%d_CompareToBestMeff.png"%(SignalGrid,DeltaBG,lumiscale) )




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
			figSens.savefig("plots/massPlaneSensitivity_%s_%s_%d_BestSR.png"%(SignalGrid,DeltaBG,lumiscale) )


		#with chosen SR
		plt.clf()
		CS = plt.contour(zi, [2,3,4,5], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="black")
		plt.clabel(CS, fontsize=9, inline=1, colors="black", fmt='%1.0f $\\sigma$')

		for i,j,k in zip(x,y,zSR):
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
			figSens.savefig("plots/massPlaneSensitivity_%s_%s_%d_BestSR_Text.png"%(SignalGrid,DeltaBG,lumiscale) )




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
			figSens.savefig("plots/massPlaneSensitivity_%s_%s_%d_BestMEffSR.png"%(SignalGrid,DeltaBG,lumiscale) )


		#with chosen SR
		plt.clf()
		CS = plt.contour(zi, [2,3,4,5], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="black")
		plt.clabel(CS, fontsize=9, inline=1, colors="black", fmt='%1.0f $\\sigma$')


		print zSR
		for i,j,k in zip(x,y,zSR):
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
			figSens.savefig("plots/massPlaneSensitivity_%s_%s_%d_BestMEffSR_Text.png"%(SignalGrid,DeltaBG,lumiscale) )












