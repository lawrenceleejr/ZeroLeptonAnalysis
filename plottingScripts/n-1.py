#!/usr/bin/env python

import sys
sys.argv.append( '-b-' )

import ROOT
import numpy as np
import rootpy
from rootpy.plotting import Hist, HistStack, Legend, Canvas, Graph, Pad
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
import gc

import glob

from ATLASStyle import *

from rootpy import asrootpy

ROOT.gROOT.LoadMacro("~/atlasstyle-00-03-04/AtlasStyle.C")
ROOT.gROOT.LoadMacro("~/atlasstyle-00-03-04/AtlasLabels.C")
ROOT.SetAtlasStyle()
# import style_mpl

ROOT.gROOT.SetBatch()
rootpy.ROOT.gROOT.SetBatch()

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



combineDS1 = 0
plotWithROOT = True
plotWithMPL = False

lumiscale = 36.47



kindOfRegion = "SR"
# kindOfRegion = "CRY"
# kindOfRegion = "CRQ"
# kindOfRegion = "CRW"
# kindOfRegion = "VRZ"



samples = [
			'DataMain',
			# 'DataMain2016',
			'QCD',
			# 'GAMMAMassiveCB',
			'Top',
			'WMassiveCB',
			'ZMassiveCB',
			'DibosonMassiveCB',
			# 'GG_direct_1800_0',
			]

if "CRY" in kindOfRegion:
	samples += ['GAMMAMassiveCB']



# colorpal = sns.color_palette("husl", 5 )
colorpal = sns.color_palette("husl", 5 )


colors = {
	'DataMain': 'black',
	# 'DataMain2016': 'red',
	'QCD': 'gray',
	'Top': colorpal[0],
	'WMassiveCB': colorpal[1],
	'ZMassiveCB': colorpal[2],
	'DibosonMassiveCB': colorpal[3],
	"GG_direct_1800_0" : 'white',
	'GAMMAMassiveCB': colorpal[4],
}

myfiles = {
	'DataMain':   ROOT.TFile('hists/output/%s/DataMain/hist-DataMain.root.root'%kindOfRegion),
	# 'DataMain2016':   ROOT.TFile('hists/output/%s/DataMain_data16_13TeV/hist-DataMain_data16_13TeV.root.root'%kindOfRegion),
	'QCD':    ROOT.TFile('hists/output/%s/QCD/hist-JetSmearing.root.root'%kindOfRegion),
	# 'GammaJet':    ROOT.TFile('hists/output/%s/GAMMAMassiveCB/hist-GAMMAMassiveCB.root.root'%kindOfRegion),

	'Top':    ROOT.TFile('hists/output/%s/Top/hist-Top.root.root'%kindOfRegion),
	'WMassiveCB':      ROOT.TFile('hists/output/%s/WMassiveCB/hist-WMassiveCB.root.root'%kindOfRegion),
	'ZMassiveCB':      ROOT.TFile('hists/output/%s/ZMassiveCB/hist-ZMassiveCB.root.root'%kindOfRegion),
	'DibosonMassiveCB':ROOT.TFile('hists/output/%s/DibosonMassiveCB/hist-DibosonMassiveCB.root.root'%kindOfRegion),
}

rebinfactor = 2

signalsamples = os.listdir("hists/output/%s/"%kindOfRegion)
# print signalsamples
signalsamples = [x for x in signalsamples if "GG_direct" in x or "SS_direct" in x or "GG_onestepCC" in x]
print signalsamples

# plottedsignals =  ["_1100_300_SRAll","_1100_500_SRAll","_1100_700_SRAll" ]
# plottedsignals =  ["_1500_100_SRAll","_1600_0_SRAll","_1100_700_SRAll" ]
# plottedsignals = []

plottedsignals = {}

plottedsignals["SRG1a"] = ["GG_direct_1800_0"]
plottedsignals["SRG1b"] = ["GG_direct_1800_0"]
plottedsignals["SRG2a"] = ["GG_direct_1800_0"]
plottedsignals["SRG2b"] = ["GG_direct_1800_0"]
plottedsignals["SRG3a"] = ["GG_direct_1800_0"]
plottedsignals["SRG3b"] = ["GG_direct_1800_0"]

plottedsignals["SRG1"] = ["GG_direct_1800_0"]
plottedsignals["SRG2"] = ["GG_direct_1800_0"]
plottedsignals["SRG3"] = ["GG_direct_1800_0"]

plottedsignals["SRG1Common"] = ["GG_direct_1800_0"]
plottedsignals["SRG2Common"] = ["GG_direct_1800_0"]
plottedsignals["SRG3Common"] = ["GG_direct_1800_0"]

# plottedsignals["SR3A"] = ["GG_onestepCC_745_625_505"]

# plottedsignals["CRDB1B"] = ["_1400_0","_1500_100","_1600_0" ]


f = myfiles['DataMain']
f.cd()

histogramNames = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys() if "dummy" in key.GetName() ]

commonHistNames = [
	"MET_",
	"Meff_",
	# "MET_over_(MET+pT_jet1+pT_jet2+pT_jet3+pT_jet4)", #picked up by MET_
	"Aplan_",
	"metTST_",
	"dphi_",
	"pT_jet1_",
	"pT_jet4_",
	"eta_jet1_",
	"eta_jet4_",
	"NJet",
	"nBJet"
	]

for tmpHistName in commonHistNames:
	histogramNames += [key.GetName() for key in ROOT.gDirectory.GetListOfKeys() if tmpHistName in key.GetName() ]

histogramNames += [key.GetName() for key in ROOT.gDirectory.GetListOfKeys() if "_minus_" in key.GetName() ]



axislabels = {}

axislabels[ "MET" ]       = "MET [GeV]"
axislabels[ "Meff" ]      = "m_{Eff} [GeV]"
axislabels[ "Aplan" ]     = "Aplanarity"
axislabels[ "metTST" ]    = "MET TST Soft Term [GeV]"
axislabels[ "dphi" ]      = "min #Delta #phi_{MET,j_{i}}"
axislabels[ "pT_jet1" ]   = "Leading Jet p_{T}"
axislabels[ "pT_jet4" ]   = "Fourth Leading Jet p_{T}"
axislabels[ "eta_jet1" ]  = "Leading Jet #eta"
axislabels[ "eta_jet4" ]  = "Fourth Leading Jet #eta"
axislabels[ "NJet" ]  = "Jet Multiplicity [p_{T}>50 GeV]"
axislabels[ "nBJet" ]  = "B-Jet Multiplicity [p_{T}>50 GeV]"

axislabels[ "H2PP" ]      = "H_{1,1}^{PP} [GeV]"
axislabels[ "HT5PP" ]     = "H_{T4,1}^{PP} [GeV]"
axislabels[ "maxRH1PPiH2PPi" ]  = "max(H_{1,0}^{Pi} / H_{2,0}^{Pi})"
axislabels[ "minRpTj2iHT3PPi" ] = "min(p_{T,j2i}^{PP} / H_{T2,1i}^{PP})"
axislabels[ "RPZHT5PP" ]   = "p_{PP,z}^{lab} / (p_{PP,z}^{lab}+H_{T4,1}^{PP})"
axislabels[ "RPTHT5PP" ]   = "p_{T,PP}^{lab} / (p_{T,PP}^{lab}+H_{T4,1}^{PP})"
axislabels[ "RHT5PPH5PP" ] = "H_{T4,1}^{PP}/H_{4,1}^{PP}"
axislabels[ "RH2PPH5PP" ]  = "H_{1,1}^{PP}/H_{4,1}^{PP}"
axislabels[ "deltaQCD" ]   = "#Delta QCD"




# additionalRegionName = ", CRY"
additionalRegionName = ""

# myfiles[""]

# print histogramNames


# style_mpl()
if plotWithMPL:
	fig = plt.figure(figsize=(6,7.5))

outputFile = open("n-1.tex", 'w')
outputROOTFile = ROOT.TFile("tmp.root","RECREATE")

for histogramName in histogramNames:


	myfiles = {
		'DataMain':   ROOT.TFile('hists/output/%s/DataMain/hist-DataMain.root.root'%kindOfRegion),
		# 'DataMain2016':   ROOT.TFile('hists/output/%s/DataMain_data16_13TeV/hist-DataMain_data16_13TeV.root.root'%kindOfRegion),
		# 'QCD':    ROOT.TFile('hists/output/%s/QCD/hist-QCD.root.root'%kindOfRegion),
		'QCD':    ROOT.TFile('hists/output/%s/QCD/hist-JetSmearing.root.root'%kindOfRegion),
		'GAMMAMassiveCB':    ROOT.TFile('hists/output/%s/GAMMAMassiveCB/hist-GAMMAMassiveCB.root.root'%kindOfRegion),

		'Top':    ROOT.TFile('hists/output/%s/Top/hist-Top.root.root'%kindOfRegion),
		'WMassiveCB':      ROOT.TFile('hists/output/%s/WMassiveCB/hist-WMassiveCB.root.root'%kindOfRegion),
		'ZMassiveCB':      ROOT.TFile('hists/output/%s/ZMassiveCB/hist-ZMassiveCB.root.root'%kindOfRegion),
		'DibosonMassiveCB':ROOT.TFile('hists/output/%s/DibosonMassiveCB/hist-DibosonMassiveCB.root.root'%kindOfRegion),
		'GG_direct_1800_0':ROOT.TFile(glob.glob('hists/output/%s/GG_direct_1800_0*/hist-GG_direct.root.root'%kindOfRegion)[0]  ),
	}


	print histogramName
	cleanHistogramName = histogramName.translate(None,"()_+/-")
	if "SR" not in histogramName:
		continue

	# if "Loose" not in histogramName:
	# 	continue
	if "SRG2a" not in histogramName:# and "SRG3Common" not in histogramName:
		continue

	if plotWithMPL:
		plt.clf()

	hists = {}
	histsToStack = []
	stack = HistStack()

	nBinsOrig = False

	for sample in samples:
		f = myfiles[sample]
		# f.ls()
		outputROOTFile.cd()
		# f.Print()
		# hists[sample] =  f.Get(histogramName).Clone(histogramName+sample)

		print sample
		print f
		hists[sample] = asrootpy( f.Get(histogramName).Clone(histogramName+sample) )
		if not nBinsOrig:
			nBinsOrig = hists[sample].GetNbinsX()
		hists[sample].Sumw2()
		if hists[sample].GetNbinsX() > 10:
			hists[sample].Rebin(rebinfactor)
		hists[sample].SetTitle(r"%s"%sample)
		hists[sample].fillstyle = "solid"

		hists[sample].fillcolor = colors[sample]
		# hists[sample].fillcolor = 'green'
		hists[sample].markersize = 1.2
		# hists[sample].linewidth = 0
		if "SS_direct" in sample:
			hists[sample].Scale(0.8)


		if "QCD" in sample:
			hists[sample].Scale(0.006727*lumiscale*1.15)

		elif not 'Data' in sample:
			hists[sample].Scale(lumiscale)

		if not 'Data' in sample:
			histsToStack.append( hists[sample] )

		# print hists[sample].Integral()
		# else:
		# 	# hists[sample].markersize = 1.2
		# 	pass


	outputROOTFile.cd()

	# print histsToStack[0].Integral()
	# print histsToStack
	sortedHistsToStack = sorted(histsToStack, key=lambda x: x.Integral() , reverse=False)
	# print sortedHistsToStack

	for tmphist in sortedHistsToStack:
		if tmphist.Integral():
			stack.Add(tmphist)

	try:
		stack.sum.Integral()
	except:
		print "stack has no integral!"
		continue

	if plotWithMPL:
		gs = mpl.gridspec.GridSpec(2,1,height_ratios=[4,1])
		gs.update(wspace=0.00, hspace=0.00)
		axes = plt.subplot(gs[0])
		axes_ratio = plt.subplot(gs[1], sharex=axes)
		plt.setp(axes.get_xticklabels(), visible=False)


	if plotWithROOT:
		c = Canvas(700,700)
		c.cd()
		pad1 = Pad( 0, 0.3, 1, 1.0)
		pad1.SetBottomMargin(0); # Upper and lower plot are joined
		pad1.SetGrid();         # Vertical grid
		pad1.Draw();             # Draw the upper pad: pad1
		c.cd()
		pad2 = Pad( 0, 0.05, 1, 0.3);
		pad2.SetTopMargin(0); # Upper and lower plot are joined
		pad2.SetBottomMargin(0.3); # Upper and lower plot are joined
		pad2.SetGrid();         # Vertical grid
		pad2.Draw();             # Draw the upper pad: pad1

		pad1.cd();               # pad1 becomes the current pad
		rootstack = ROOT.THStack(stack)
		rootstack.Draw('HIST')
		rootstack.GetYaxis().SetTitle("Entries");
		rootstack.GetYaxis().SetTitleSize(20);
		rootstack.GetYaxis().SetTitleFont(43);
		rootstack.GetYaxis().SetTitleOffset(1.55)
		pad1.SetLogy()


	if plotWithMPL:
		axes.set_yscale('log')
		rplt.bar(stack, stacked=True, axes=axes, yerr=False, alpha=0.5, rasterized=True, ec='grey', linewidth=0)
		tmpstack = stack.sum
		tmpstack.fillstyle = "none"
		for i in xrange(len(stack)):
			myalpha = 0.4 if i>0 else 1.0
			rplt.hist(tmpstack, axes=axes, yerr=False, alpha=myalpha, rasterized=True, ec='grey', linewidth=1, fillstyle="none")
			tmpstack = tmpstack - stack[len(stack)-1-i]

		if hists['DataMain'].Integral():
			rplt.errorbar(hists['DataMain'], xerr=False, emptybins=False, axes=axes, marker='o', lw=1)

	regionName = histogramName.split("_")[0]

	for inameChunk,nameChunk in enumerate(histogramName.split("_")):
		if "SR" in nameChunk:
			regionName = nameChunk


	for signalsample in signalsamples:
		print signalsample
		print plottedsignals[regionName]

		skip = 1
		try:
			if any([thissig in signalsample for thissig in plottedsignals[regionName] ]):
				skip=0
		except:
			skip=1

		if skip:
			print "skipping"
			continue

		if not "SR" in kindOfRegion:
			continue

		signalfile = root_open(glob.glob('hists/output/%s/%s*/hist-*.root'%(kindOfRegion,signalsample) )[0] )

		outputROOTFile.cd()
		hists[signalsample] =  signalfile.Get(histogramName).Clone( histogramName + signalsample )
		hists[signalsample].SetTitle(r"%s"%signalsample.replace("_"," ").replace("SRAll","")+additionalRegionName  )
		hists[signalsample].Scale(lumiscale)

		if hists[signalsample].GetNbinsX() > 10:
			hists[signalsample].Rebin(rebinfactor)
		hists[signalsample].color = "red"


		if hists[signalsample].Integral():
			if plotWithMPL:
				rplt.errorbar(hists[signalsample], axes=axes, yerr=False, xerr=False, alpha=0.9, fmt="--", rasterized=False, markersize=0)

			if plotWithROOT:
				hists[signalsample].SetLineStyle(2)
				hists[signalsample].SetLineWidth(2)
				hists[signalsample].Draw("hist same")


		signalfile.Close()

	if plotWithROOT:

		if hists['DataMain'].Integral():
			hists['DataMain'].Draw("E1 same")
			rootstack.SetMaximum(hists['DataMain'].GetMaximum()*1000)
			rootstack.SetMinimum(0.01)
			# c.Update()
		# c.SaveAs("test.pdf")
		# break
	# plt.ylim([0.1,10])

	# try:
	# 	print "BG: %f"%stack.sum.Integral()
	# except:
	# 	break


	if plotWithMPL:
		# leg = plt.legend(loc="best")
		axes.annotate(r'\textbf{\textit{ATLAS}} Internal',xy=(0.05,0.95),xycoords='axes fraction')
		axes.annotate(r'$\int{L}\sim$ %.1f fb$^{-1}$, $\sqrt{s}$=13 TeV, N-1, %s'%(lumiscale, regionName+additionalRegionName ),xy=(0.0,1.01),xycoords='axes fraction')

		if "MET" in histogramName:
			xlim([0,1500])

		if "Meff" in histogramName:
			xlim([0,6000])

		if "MET_over" in histogramName:
			xlim([0,1])



	try:
		cutvalue = histogramName.split(">")[-1].split("<")[-1]
		if cutvalue[0]=="0":
			cutvalue = "0."+cutvalue[1:]
		cutvalue = float(cutvalue)
		boxDirection = 1 if ">" in histogramName else -1

		if nBinsOrig<11:
			if boxDirection == 1:
				cutvalue += 1.
			elif boxDirection == -1:
				cutvalue -= 1.

		if cutvalue > stack.sum.GetXaxis().GetXmax():
			# print "In the thing!"
			cutvalue = histogramName.split(">")[-1].split("<")[-1]
			# cutvalue.insert(1,".")
			# print cutvalue
			cutvalue = float(cutvalue)
			cutvalue = cutvalue/(10**math.floor(np.log10(cutvalue) ) )
			# print cutvalue

		if plotWithROOT:
			pad1.cd()
			print "cutvalue for arrow: %f" %cutvalue
			arrow = ROOT.TArrow(cutvalue,1,cutvalue,ROOT.gPad.GetUymin(),0.02,"|>");
			arrow.Draw()

		if plotWithMPL:
			linelength = abs(axes.axis()[0]-axes.axis()[1])/10.
			linelength = 10e10

			axes.plot( (cutvalue,cutvalue), (1e-10,1e2), 'g-' , alpha=0.8)
			axes.plot( (cutvalue,cutvalue+linelength*boxDirection), (1e2,1e2), 'g-' , alpha=0.8)
			# import numpy as np
			# myx = np.linspace(cutvalue,cutvalue+linelength*boxDirection,2)
			# myy = array([1,1])
			# axes.quiver(  myx[:-1], myy[:-1], myx[1:]-myx[:-1], myy[1:]-myy[:-1] , scale_units='xy', angles='xy',scale=1 )#, head_width=0.05, head_length=0.1, fc='g', ec='g' , alpha=0.8)
			axes.text( cutvalue, 0.5, 'Cut at %.2f'%cutvalue, color="k", size=10, va="top", ha="right", rotation=90)
	except:
		pass

	# axes_ratio.set_xlabel(histogramName.replace("_"," ").replace(">","$>$").replace("<","$<$") )


	if plotWithMPL:
		# get handles
		handles, labels = axes.get_legend_handles_labels()
		# remove the errorbars
		tmphandles = []
		tmplabels = []
		for a,b in zip(handles,labels):
			if type(a)==Line2D:
				continue
			tmphandles.append(a[0])
			tmplabels.append(b)
		# use them in the legend
		axes.legend(tmphandles, tmplabels, loc='best',numpoints=1)



	axislabel = ""
	for chunk in histogramName.split("_"):
		if "SR" in chunk or "minus" in chunk:
			continue
		axislabel += chunk
	# axislabel = " ".join(histogramName.split("_")[2:])
	axislabel = axislabel.split("<")[0].split(">")[0]




	if 'DataMain' in hists:
		if hists["DataMain"].Integral() and plotWithMPL:
			ratioplot = Graph()
			ratioplot.Divide(  hists['DataMain'], stack.sum , 'pois'  )
			# ratioplot.color = "green"
			tmpyerror,tmpyerror2 = zip(*list(ratioplot.yerr()) )
			tmpx = list(ratioplot.x())
			tmpy = list(ratioplot.y())
			tmpxy = zip(tmpx,tmpy,tmpyerror)
			# print tmpxy
			tmpxy = [tmp for tmp in tmpxy if tmp[1]!=0  ]
			# print tmpxy
			tmpx,tmpy,tmpyerror = zip(*tmpxy)
			# print tmpyerror
			# axes_ratio.errorbar(tmpx,tmpy, yerr = tmpyerror,xerr=False, emptybins=False, marker='o', lw=1, color="black")
			axes_ratio.errorbar(tmpx, tmpy,
								# list(ratioplot.y()),
								yerr = tmpyerror,
								# yerr=[ x[0] for x in list(ratioplot.yerr() ) ] ,
								# xerr=list(ratioplot.y()),
								# emptybins=False,
								fmt='o', lw=1,
								color="black", ms=5)

		if plotWithROOT:
			pad2.cd()
			tmpratio = hists['DataMain'].Clone()
			tmpratio.Divide(stack.sum)
			tmpratio.Draw("e1")

			tmpratio.GetYaxis().SetTitle("Data/BG");
			tmpratio.GetYaxis().SetNdivisions(505);
			tmpratio.GetYaxis().SetTitleSize(20);
			tmpratio.GetYaxis().SetTitleFont(43);
			tmpratio.GetYaxis().SetTitleOffset(1.55);
			tmpratio.GetYaxis().SetLabelFont(43); # Absolute font size in pixel (precision 3)
			tmpratio.GetYaxis().SetLabelSize(15);

			if tmpratio.GetMaximum()>10:
				tmpratio.SetMaximum(11)
			tmpratio.SetMinimum(0)

			# X axis ratio plot settings
			tmpratio.GetXaxis().SetTitleSize(18);
			tmpratio.GetXaxis().SetTitleFont(43);
			tmpratio.GetXaxis().SetTitleOffset(5.);
			tmpratio.GetXaxis().SetLabelFont(43); # Absolute font size in pixel (precision 3)
			tmpratio.GetXaxis().SetLabelSize(15)

			unityline = ROOT.TLine()
			unityline.DrawLine(ROOT.gPad.GetUxmin(),1.,ROOT.gPad.GetUxmax(),1.)

			try:
				axislabel = axislabels[axislabel]
			except:
				axislabel = axislabel
			tmpratio.GetXaxis().SetTitle(axislabel)


	if plotWithROOT:
		pad1.cd()
		ROOT.ATLASLabel(0.2,0.9,"Internal      %s, %s"%(regionName,kindOfRegion)   )

		legend = Legend( 4, leftmargin=0.45, margin=0.35, topmargin=0.07)
		hists["DataMain"].SetTitle("Data 15+16 %s fb^{-1}"%lumiscale)
		legend.AddEntry(hists["DataMain"], style='ep')
		# sortedHistsToStack.reverse()
		for BG in reversed(sortedHistsToStack):
			BG.SetTitle(  BG.GetTitle().replace("MassiveCB","")   )
			legend.AddEntry(BG, style='F')
		for signalsample in signalsamples:
			skip = 1
			try:
				if any([thissig in signalsample for thissig in plottedsignals[regionName] ]):
					skip=0
			except:
				skip=1

			if skip:
				# print "skipping"
				continue
			try:
				legend.AddEntry(hists[signalsample], style='L')
			except:
				continue

		legend.SetBorderSize(1)
		legend.SetTextSize(0.03)
		legend.Draw()

		c.SaveAs("N-1Plots/root/%s.pdf"%(kindOfRegion + "_" + histogramName.split(">")[0].split("<")[0])  )
		# break

	if plotWithMPL:

		xmin, xmax = axes.get_xlim()
		plt.plot([xmin,xmax], [1,1], 'k--', lw=1)

		yticks(arange(0,2.0,0.2))
		ylim([0,2])

		axes_ratio.set_ylabel('Data/MC')

		axes.set_ylabel('Events')
		axes_ratio.set_xlabel( axislabel )

		axes.set_ylim([0.05, 99999])

		fig.savefig("N-1Plots/%s.pdf"%histogramName.split(">")[0].split("<")[0])


	for sample in samples:
		del hists[sample]

# 	outputFile.write(r"""
# \begin{figure}[tbph]
# \begin{center}
# \includegraphics[width=0.49\textwidth]{figures/N-1Plots/%s}
# \end{center}
# \caption{N-1 Plots for %s}
# \label{fig:%s}
# \end{figure}


# 		"""%(histogramName, histogramName.split("_")[0], histogramName.translate(None, "<>")  )
# 		)

	del myfiles
	del hists
	del c
	ROOT.gROOT.Reset()

	gc.collect()
