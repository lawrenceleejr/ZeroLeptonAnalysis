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
			'DataMain2015',
			'DataMain2016',
			'QCD',
			'GammaJet',
			'Top',
			'Wjets',
			'Zjets',
			'Diboson',
			]

combineDS1 = 1


lumiscale = 3.24
if combineDS1:
	lumiscale = 5.8



colorpal = sns.color_palette("husl", 5 )


colors = {
	'DataMain2015': 'black',
	'DataMain2016': 'red',
	'QCD': 'gray',
	'Top': colorpal[0],
	'Wjets': colorpal[1],
	'Zjets': colorpal[2],
	'Diboson': colorpal[3],
	'GammaJet': colorpal[4],
}

# colors = {
# 	'Data': 'black',
# 	'QCD': 'gray',
# 	'Top': 'red',
# 	'W': 'green',
# 	'Z': 'blue',
# }

myfiles = {
	'DataMain2015':   root_open('hists/output/DataMain_data15_13TeV/hist-DataMain_data15_13TeV.root.root'),
	'DataMain2016':   root_open('hists/output/DataMain_data16_13TeV/hist-DataMain_data16_13TeV.root.root'),
	'QCD':    root_open('hists/output/QCD/hist-QCD.root.root'),
	'GammaJet':    root_open('hists/output/GAMMAMassiveCB/hist-GAMMAMassiveCB.root.root'),

	'Top':    root_open('hists/output/Top/hist-Top.root.root'),
	'Wjets':      root_open('hists/output/WMassiveCB/hist-WMassiveCB.root.root'),
	'Zjets':      root_open('hists/output/ZMassiveCB/hist-ZMassiveCB.root.root'),
	'Diboson':root_open('hists/output/DibosonMassiveCB/hist-DibosonMassiveCB.root.root'),
}

rebinfactor = 6

signalsamples = os.listdir("hists/output/")
# print signalsamples
signalsamples = [x for x in signalsamples if "GG_direct" in x or "SS_direct" in x or "GG_onestepCC" in x]
# print signalsamples

# plottedsignals =  ["_1100_300_SRAll","_1100_500_SRAll","_1100_700_SRAll" ]
# plottedsignals =  ["_1500_100_SRAll","_1600_0_SRAll","_1100_700_SRAll" ]
# plottedsignals = []

plottedsignals = {}

plottedsignals["SR2jl"] = ["SS_direct_900_0","SS_direct_900_200" ]
plottedsignals["SR2jm"] = ["SS_direct_900_0","SS_direct_900_200" ]
plottedsignals["SR2jCo"] = ["SS_direct_900_500","SS_direct_1000_600","SS_direct_1100_700" ]
plottedsignals["SR2jt"] = ["SS_direct_900_0","SS_direct_900_200" ]
plottedsignals["SR4jt"] = ["GG_direct_1400_0","GG_direct_1500_100","GG_direct_1600_0" ]
plottedsignals["SR5j"] = ["GG_direct_900_500","GG_direct_1000_600","GG_direct_1100_700" ]
plottedsignals["SR6jm"] = ["GG_direct_900_500","GG_direct_1000_600","GG_direct_1100_700" ]
plottedsignals["SR6jt"] = ["GG_direct_900_500","GG_direct_1000_600","GG_direct_1100_700" ]

plottedsignals["SRS1a"] = ["SS_direct_700_600","SS_direct_700_500","SS_direct_700_400", ]
plottedsignals["SRS1b"] = ["SS_direct_700_600","SS_direct_700_500","SS_direct_700_400", ]
plottedsignals["SRS2a"] = ["SS_direct_900_0","SS_direct_900_200" ]
plottedsignals["SRS2b"] = ["SS_direct_900_0","SS_direct_900_200" ]
plottedsignals["SRS3a"] = ["SS_direct_900_0","SS_direct_900_200" ]
plottedsignals["SRS3b"] = ["SS_direct_900_0","SS_direct_900_200" ]



plottedsignals["SRC1a"] = ["SS_direct_500_450","GG_direct_612_587","GG_direct_650_550" ]
plottedsignals["SRC1b"] = ["SS_direct_500_450","GG_direct_612_587","GG_direct_650_550" ]
plottedsignals["SRC2a"] = ["SS_direct_500_450","GG_direct_612_587","GG_direct_650_550" ]
plottedsignals["SRC2b"] = ["SS_direct_500_450","GG_direct_612_587","GG_direct_650_550" ]
plottedsignals["SRC3a"] = ["SS_direct_500_450","GG_direct_612_587","GG_direct_650_550" ]
plottedsignals["SRC3b"] = ["SS_direct_500_450","GG_direct_612_587","GG_direct_650_550" ]
plottedsignals["SRC4a"] = ["SS_direct_500_450","GG_direct_612_587","GG_direct_650_550" ]
plottedsignals["SRC4b"] = ["SS_direct_500_450","GG_direct_612_587","GG_direct_650_550" ]


plottedsignals["SRG1a"] = ["GG_direct_900_500","GG_direct_1000_600","GG_direct_1100_700" ]
plottedsignals["SRG1b"] = ["GG_direct_900_500","GG_direct_1000_600","GG_direct_1100_700" ]
plottedsignals["SRG1c"] = ["GG_direct_1100_500","GG_direct_1200_600","GG_direct_1200_800" ]
plottedsignals["SRG2a"] = ["GG_direct_1300_300","GG_direct_1400_600" ]
plottedsignals["SRG2b"] = ["GG_direct_1300_300","GG_direct_1400_600" ]
plottedsignals["SRG2c"] = ["GG_direct_1300_300","GG_direct_1400_600" ]
plottedsignals["SRG3a"] = ["GG_direct_1400_0","GG_direct_1500_100","GG_direct_1600_0" ]
plottedsignals["SRG3b"] = ["GG_direct_1400_0","GG_direct_1500_100","GG_direct_1600_0" ]
plottedsignals["SRG3c"] = ["GG_direct_1400_0","GG_direct_1500_100","GG_direct_1600_0" ]


# plottedsignals["SR3A"] = ["GG_onestepCC_745_625_505"]

plottedsignals["CRDB1B"] = ["_1400_0","_1500_100","_1600_0" ]


f = myfiles['DataMain2015']
f.ls()
# f.ls()
# print [key.GetName() for key in ROOT.gDirectory.GetListOfKeys() if "_minus_" in key.GetName() ]
f.cd()
# histogramNames = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys() if "SR" in key.GetName() ]
# histogramNames = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys() if "_minus_" in key.GetName() ]
histogramNames = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys() if "MET" in key.GetName() ]
# histogramNames = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys() if "dphi" in key.GetName() ]
# histogramNames += [key.GetName() for key in ROOT.gDirectory.GetListOfKeys() if "deltaQCD" in key.GetName() ]
# histogramNames = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys() if "Meff_" in key.GetName() ]
# histogramNames = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys() if "MET_" in key.GetName() ]


additionalRegionName = ", CRY"

# myfiles[""]

# print histogramNames


# style_mpl()
fig = plt.figure(figsize=(6,7.5))

outputFile = open("n-1.tex", 'w')


for histogramName in histogramNames:

	print histogramName
	if "SR" not in histogramName:
		continue

	# if "Loose" not in histogramName:
	# 	continue
	# if "SRS" not in histogramName:
		# continue
	# if "CRVR" not in histogramName:
	# 	continue
	# if "dphi" not in histogramName:
	# 	continue

	plt.clf()

	hists = {}
	histsToStack = []
	stack = HistStack()

	for sample in samples:
		f = myfiles[sample]
		# f.ls()
		hists[sample] = f.Get(histogramName).Clone(sample)
		hists[sample].Sumw2()
		if hists[sample].GetNbinsX() > 10:
			hists[sample].Rebin(rebinfactor)
			# hists[sample].Rebin(rebinfactor)
		hists[sample].SetTitle(r"%s"%sample)
		hists[sample].fillstyle = "solid"
		hists[sample].fillcolor = colors[sample]
		# hists[sample].linewidth = 0
		if "SS_direct" in sample:
			hists[sample].Scale(0.8)

		if not 'Data' in sample:
			hists[sample].Scale(lumiscale)
			histsToStack.append( hists[sample] )

		# print hists[sample].Integral()
		# else:
		# 	# hists[sample].markersize = 1.2
		# 	pass



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

	gs = mpl.gridspec.GridSpec(2,1,height_ratios=[4,1])
	gs.update(wspace=0.00, hspace=0.00)
	axes = plt.subplot(gs[0])
	axes_ratio = plt.subplot(gs[1], sharex=axes)
	plt.setp(axes.get_xticklabels(), visible=False)

	# axes = plt.subplot()


	# rplt.bar(stack, stacked=True, axes=axes, yerr=False, alpha=0.5, rasterized=True, ec='grey', linewidth=1)
	# rplt.errorbar(hists['Data'], xerr=False, emptybins=False, axes=axes, marker='o', ms=10)
	


	# try:
	if 1:
		axes.set_yscale('log')
		rplt.bar(stack, stacked=True, axes=axes, yerr=False, alpha=0.5, rasterized=True, ec='grey', linewidth=0)
		tmpstack = stack.sum
		tmpstack.fillstyle = "none"
		for i in xrange(len(stack)):
			myalpha = 0.4 if i>0 else 1.0
			rplt.hist(tmpstack, axes=axes, yerr=False, alpha=myalpha, rasterized=True, ec='grey', linewidth=1, fillstyle="none")
			tmpstack = tmpstack - stack[len(stack)-1-i]

		if combineDS1:
			hists['DataDS1'] = hists['DataMain2015'].Clone()
			hists['DataDS1'].Add(hists['DataMain2016'])
			hists['DataDS1'].SetTitle("Data DS1 5.8 fb$^{-1}$")
			rplt.errorbar(hists['DataDS1'], xerr=False, emptybins=False, axes=axes, marker='o', lw=1)

			# if hists['DataMain2015'].Integral():
			# 	# hists['DataMain2015'].Scale(  hists['DataDS1'].Integral()/ hists['DataMain2015'].Integral() )
			# 	hists['DataMain2015'].color = "green"
			# 	rplt.errorbar(hists['DataMain2015'], xerr=False, emptybins=False, axes=axes, marker='o', lw=1, markersize=3)
			# if hists['DataMain2016'].Integral():
			# 	# hists['DataMain2016'].Scale(  hists['DataDS1'].Integral()/ hists['DataMain2015'].Integral() )
			# 	hists['DataMain2016'].color = "red"
			# 	rplt.errorbar(hists['DataMain2016'], xerr=False, emptybins=False, axes=axes, marker='o', lw=1, markersize=3)
		else:
			if hists['DataMain2015'].Integral():
				rplt.errorbar(hists['DataMain2015'], xerr=False, emptybins=False, axes=axes, marker='o', lw=1)
			if hists['DataMain2016'].Integral():
				hists['DataMain2016'].Scale(  hists['DataMain2015'].Integral()/ hists['DataMain2016'].Integral() )
				hists['DataMain2016'].color = "red"
				rplt.errorbar(hists['DataMain2016'], xerr=False, emptybins=False, axes=axes, marker='o', lw=1, color='red')

	# except:
	# 	print "some sort of problem!"
	# 	pass




	for signalsample in signalsamples:
		# print signalsample
		# print plottedsignals[histogramName.split("_")[0]  ] 
		skip = 1
		try:
			if "MET" in histogramName or "Meff" in histogramName:
				tmpregionname = histogramName.split("_")[1]
			else:
				tmpregionname = histogramName.split("_")[0]
			if any([thissig in signalsample for thissig in plottedsignals[tmpregionname  ] ]):
				skip=0
		except:
			skip=1

		if skip:
			# print "skipping"
			continue

		if not "SR" in signalsample:
			continue

		signalfile = root_open("hists/output/%s/hist-%s.root.root"%(signalsample,  "_".join(signalsample.split("_")[:2])  ) )
		# print "hists/output/%s/hist-%s.root.root"%(signalsample,  "_".join(signalsample.split("_")[:2])  )


		hists[signalsample] = signalfile.Get(histogramName).Clone( signalsample )
		hists[signalsample].SetTitle(r"%s"%signalsample.replace("_"," ").replace("SRAll","")+additionalRegionName  )
		hists[signalsample].Scale(lumiscale)


		if hists[signalsample].GetNbinsX() > 10:
			hists[signalsample].Rebin(rebinfactor)
		hists[signalsample].color = "red"

		if hists[signalsample].Integral():
			rplt.errorbar(hists[signalsample], axes=axes, yerr=False, xerr=False, alpha=0.9, fmt="--", rasterized=False, markersize=0)

		signalfile.Close()

	# plt.ylim([0.1,10])

	try:
		print "BG: %f"%stack.sum.Integral()
	except:
		break

	# leg = plt.legend(loc="best")
	axes.annotate(r'\textbf{\textit{ATLAS}} Internal',xy=(0.05,0.95),xycoords='axes fraction') 
	axes.annotate(r'$\int{L}\sim$ %.1f fb$^{-1}$, $\sqrt{s}$=13 TeV, N-1, %s'%(lumiscale, histogramName.split("_")[0]+additionalRegionName ),xy=(0.0,1.01),xycoords='axes fraction') 

	
	if "MET" in histogramName:
		xlim([0,1500])

	if "Meff" in histogramName:
		xlim([0,6000])




	try:
		cutvalue = histogramName.split(">")[-1].split("<")[-1]
		if cutvalue[0]=="0":
			cutvalue = "0."+cutvalue[1:]
		cutvalue = float(cutvalue)
		boxDirection = 1 if ">" in histogramName else -1

		if stack.sum.GetNbinsX()<11:
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




	# if 'DataMain2015' in hists:
	# 	if hists["DataMain2015"].Integral():
	# 		ratioplot = Graph()
	# 		ratioplot.Divide(  hists['DataMain2015'], stack.sum , 'pois'  )
	# 		ratioplot.color = "green"
	# 		tmpyerror,tmpyerror2 = zip(*list(ratioplot.yerr()) )
	# 		tmpx = list(ratioplot.x())
	# 		tmpy = list(ratioplot.y())
	# 		tmpxy = zip(tmpx,tmpy,tmpyerror)
	# 		# print tmpxy
	# 		tmpxy = [tmp for tmp in tmpxy if tmp[1]!=0  ]
	# 		# print tmpxy
	# 		tmpx,tmpy,tmpyerror = zip(*tmpxy)
	# 		# print tmpyerror
	# 		# axes_ratio.errorbar(tmpx,tmpy, yerr = tmpyerror,xerr=False, emptybins=False, marker='o', lw=1, color="black")
	# 		axes_ratio.errorbar(tmpx, tmpy, 
	# 							# list(ratioplot.y()), 
	# 							yerr = tmpyerror,
	# 							# yerr=[ x[0] for x in list(ratioplot.yerr() ) ] , 
	# 							# xerr=list(ratioplot.y()), 
	# 							# emptybins=False,
	# 							fmt='o', lw=1,
	# 							color="green", ms=3)
	# 							# clip_on=False)
	# 	if hists["DataMain2016"].Integral():
	# 		ratioplot = Graph()
	# 		ratioplot.Divide(  hists['DataMain2016'], stack.sum , 'pois'  )
	# 		ratioplot.color = "red"
	# 		tmpyerror,tmpyerror2 = zip(*list(ratioplot.yerr()) )
	# 		tmpx = list(ratioplot.x())
	# 		tmpy = list(ratioplot.y())
	# 		tmpxy = zip(tmpx,tmpy,tmpyerror)
	# 		tmpxy = [tmp for tmp in tmpxy if tmp[1]!=0  ]
	# 		tmpx,tmpy,tmpyerror = zip(*tmpxy)
	# 		axes_ratio.errorbar(tmpx, tmpy, 
	# 							yerr = tmpyerror,
	# 							fmt='o', lw=1,
	# 							color="red", ms=3)


	# 		print "Data 16 %f"%hists["DataMain2016"].Integral()



	
	if combineDS1:

		if hists["DataDS1"].Integral():
			ratioplot = Graph()
			ratioplot.Divide(  hists['DataDS1'], stack.sum , 'pois'  )
			ratioplot.color = "black"
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
								# clip_on=False)



	xmin, xmax = axes.get_xlim()
	plt.plot([xmin,xmax], [1,1], 'k--', lw=1)

	yticks(arange(0,2.0,0.2))
	ylim([0,2])

	axes_ratio.set_ylabel('Data/MC')



	if "CRDB" in histogramName:

		ratioplot = Graph.divide(  Graph(hists['Diboson']), stack.sum , 'pois'  )
		ratioplot.color = "black"
		axes_ratio.errorbar(list(ratioplot.x()) , 
							list(ratioplot.y()), 
							yerr=[ x[0] for x in list(ratioplot.yerr() ) ] , 
							# xerr=list(ratioplot.y()), 
							fmt='o-',
							color="black")

		yticks(arange(0,2.0,0.2))
		ylim([0.01,1.0])

		axes_ratio.set_ylabel('Diboson Fraction')



	axes.set_ylabel('Events')
	axes_ratio.set_xlabel(histogramName.replace("_"," ").replace(">","$>$").replace("<","$<$") )

	axes.set_ylim([0.05, 99999])

	# axes.set_yscale(nonposy='clip')

	print "saving"

	fig.savefig("N-1Plots/%s.pdf"%histogramName, dpi=100)

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

