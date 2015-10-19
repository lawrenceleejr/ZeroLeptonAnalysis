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

import scipy.interpolate


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
			'Diboson'
			]

lumiscale = 4
writePlots = True

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
# 	'W+Jets': 'green',
# 	'Z+Jets': 'blue',
# }


myfiles = {
	# 'Data':   'hists/hist-DataMain_periodC.root.root',
	# 'QCD': 'hists/BG/hist-QCD.root.root',
	'Top': 'hists/BG/Top/hist-Top.root.root',
	'W': 'hists/BG/W/hist-Wjets.root.root',
	'Z': 'hists/BG/Z/hist-Zjets.root.root',
	'Diboson':'hists/BG/Diboson/hist-Diboson.root.root',
}


signalsamples = os.listdir("hists/signal/")
# print signalsamples
signalsamples = [x for x in signalsamples if "GG_direct" in x]
signalsamples = [x for x in signalsamples if "SRAll" in x]
# print signalsamples

plottedsignals =  ["_1100_500_SRAll","_1100_300_SRAll","_1100_700_SRAll" ]
# plottedsignals = []


histogramNames = [
		"H2PP",
	]

cuts = [
		# "no_cut",
		"SR1",
		"SR2",
		"SR3",
		"SR4",
		"SR5",
]




# style_mpl()
fig = plt.figure(figsize=(6,7.5), dpi=100)

# for (tmphist,tmpcut) in [(x,y) for x in histogramNames for y in cuts]:
# 	histogramName = tmphist+"_"+tmpcut

# 	plt.clf()

# 	hists = {}
# 	histsToStack = []
# 	stack = HistStack()

# 	for sample in samples:
# 		f = root_open(myfiles[sample])
# 		# f.ls()
# 		hists[sample] = f.Get(histogramName).Clone(sample)
# 		hists[sample].Sumw2()
# 		if not("nJet" in histogramName)  and not("QCD_Delta" in histogramName):
# 			hists[sample].Rebin(4)
# 		hists[sample].SetTitle(r"%s"%sample)
# 		hists[sample].fillstyle = 'solid'
# 		hists[sample].fillcolor = colors[sample]
# 		hists[sample].linewidth = 0
# 		hists[sample].Scale(lumiscale)
# 		if sample != 'Data':
# 			histsToStack.append( hists[sample] )
# 		else:
# 			hists[sample].markersize = 1.2

# 	# print histsToStack[0].Integral()
# 	# print histsToStack
# 	sortedHistsToStack = sorted(histsToStack, key=lambda x: x.Integral() , reverse=False)
# 	# print sortedHistsToStack

# 	for tmphist in sortedHistsToStack:
# 		if tmphist.Integral():
# 			stack.Add(tmphist)



from ROOT import RooStats

for DeltaBG in [0.2]:


	bestZbi = {}

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

		plt.clf()
		BG = stack.sum.Integral()
		# print "nBG:    %f --------"%BG

		x = []
		y = []
		z = []

		for signalsample in signalsamples:
			print signalsample
			# signalfile = root_open("hists/rundir_signal/"+signalsample)
			# print signalfile.ls()
			try:
				signalfile = root_open("hists/signal/%s/hist-GG_direct.root.root"%signalsample)
				sig =  signalfile.Get("H2PP_%s"%tmpcut ).Clone( signalsample )
				sig.Scale(lumiscale)
				sig = sig.Integral( )
				# print BG
				# print sig
			except:
				continue
			# print sig
			# print "-------------------------------------"
			if sig:
				myx = float(signalsample.split("direct_")[-1].split("_")[0])
				myy = float(signalsample.split("direct_")[-1].split("_")[1].split(".")[0]  )
				myz = RooStats.NumberCountingUtils.BinomialExpZ(sig, BG, DeltaBG)

				# print myx, myy, myz
				print sig, BG, myz
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
				try:
					if myz > bestZbi[(myx,myy)][0]:
						bestZbi[(myx,myy)] = (myz,tmpcut)
				except:
					bestZbi[(myx,myy)] = (myz,tmpcut)

			signalfile.Close()

		# print x, y, z
		#for pinning down the diagonal 
		for thing in [400,1200,1800 ]:
			x.append(thing)
			y.append(thing)
			z.append(0)



		x = np.array(x)
		y = np.array(y)
		z = np.array(z)

		# print x

		xi, yi = np.linspace(x.min(), x.max(), 100), np.linspace(y.min(), y.max(), 100)
		xi, yi = np.meshgrid(xi, yi)

		# print x
		# print y
		# print z

		rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
		zi = rbf(xi, yi)


	
		# histogram bin-size testing....

		# tmpgraph = ROOT.TGraph2D(len(x),x,y,z)
		# tmpgraph.SetNpx(50)
		# tmpgraph.SetNpy(50)
		# tmpgraph.Draw("colz")
		# tmpth2 = tmpgraph.GetHistogram()
		# tmpth2.Rebin(500)
		# print tmpth2

		# myc = ROOT.TCanvas("c","c",400,400)
		# tmpth2.Draw("colz")

		# myc.SaveAs("test.png")
		# print asrootpy(tmpth2)

		# print asrootpy(tmpgraph.GetContourList(2)[0])
		# print list(asrootpy(tmpgraph.GetContourList(2)[0]))



		figSens = plt.figure(  figsize=(8,5), dpi=100  )

		plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], cmap='jet', alpha=0.8)

		# rplt.hist2d(tmpth2)
		# rplt.contour(tmpth2, levels = [2,3,4,5])

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

		plt.annotate(r"$\Delta$BG/BG=%.1f, %s"%(DeltaBG,tmpcut),xy=(420,1150),color="white") 
		plt.annotate(r"$\int L \sim %.1f$ fb$^{-1}, 13$ TeV"%(lumiscale),xy=(420,1100), color="white") 
		# plt.show()
		if writePlots:
			figSens.savefig("plots/massPlaneSensitivity_%d_%d_%s.png"%(DeltaBG*10,lumiscale,tmpcut) )



	# print bestZbi
	# print bestZbi.values()
	# # print bestZbi.keys()

	plt.clf()

	# print zip(*bestZbi.keys())[0] #gluino mass
	# print zip(*bestZbi.keys())[1] #LSP mass
	# print zip(*bestZbi.values())[0] #Zbi
	# print zip(*bestZbi.values())[1] #SR

	x =   list( zip( *bestZbi.keys())[0]     )  
	y =   list( zip( *bestZbi.keys())[1]     )  
	z =   list( zip( *bestZbi.values())[0]   ) 
	zSR = list( zip( *bestZbi.values())[1]   ) 


	# print x, y, z
	#for pinning down the diagonal 
	for thing in [400,1200,1800 ]:
		x.append(thing)
		y.append(thing)
		z.append(0)


	x = np.array(x)
	y = np.array(y)
	z = np.array(z)

	xi, yi = np.linspace(x.min(), x.max(), 100), np.linspace(y.min(), y.max(), 100)
	xi, yi = np.meshgrid(xi, yi)
	rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
	zi = rbf(xi, yi)


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

	plt.annotate(r"$\Delta$BG/BG=%.1f, Best SR"%DeltaBG,xy=(420,1150),color="white") 
	plt.annotate(r"$\int L \sim %.1f$ fb$^{-1}, 13$ TeV"%(lumiscale),xy=(420,1100), color="white") 
	# plt.show()

	if writePlots:
		figSens.savefig("plots/massPlaneSensitivity_%d_%d_BestSR.pdf"%(DeltaBG*10,lumiscale) )
		figSens.savefig("plots/massPlaneSensitivity_%d_%d_BestSR.png"%(DeltaBG*10,lumiscale) )


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

	plt.annotate(r"$\Delta$BG/BG=%.1f, Best SR"%DeltaBG,xy=(420,1150)) 
	plt.annotate(r"$\int L \sim %.1f$ fb$^{-1}, 13$ TeV"%(lumiscale),xy=(420,1100)) 
	# plt.show()

	if writePlots:
		figSens.savefig("plots/massPlaneSensitivity_%d_%d_BestSR_Text.pdf"%(DeltaBG*10,lumiscale) )
		figSens.savefig("plots/massPlaneSensitivity_%d_%d_BestSR_Text.png"%(DeltaBG*10,lumiscale) )





