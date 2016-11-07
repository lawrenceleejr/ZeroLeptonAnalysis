#!/usr/local/bin/python

from ROOT import *
from ROOT import RooStats
from collections import OrderedDict
from array import array

gROOT.LoadMacro("~/atlasstyle-00-03-04/AtlasStyle.C")
gROOT.LoadMacro("~/atlasstyle-00-03-04/AtlasLabels.C")
SetAtlasStyle()
# import style_mpl

f = TFile("ilumi2histo.root")

h_den = f.Get("lumi_histo").Clone("h_den")

h_num = {}
h_eff = {}

ftree = TFile("../DataFiles/RJR/DataMain_306451.root")

intree = {}

intree["SR"] = ftree.Get("Data_SRAll")
# intree["CRWT"] = ftree.Get("Data_CRWT")
# intree["CRZ"] = ftree.Get("Data_CRZ")
# intree["CRY"] = ftree.Get("Data_CRY")

# signalRegionVsLumi = 0

for regionName in intree:

	skimtree = OrderedDict()

	preselectiontree = intree[regionName].CopyTree("1")
	skimtree["SRG3b N-2"] = intree[regionName].CopyTree("((cleaning&0x30F)==0)* ( deltaQCD > 0)* ( RPT_HT5PP < 0.08  )* ( R_H2PP_H5PP > 0.2)* ( R_HT5PP_H5PP > 0.65)* ( RPZ_HT5PP < 0.6)* ( minR_pTj2i_HT3PPi > 0.08)* ( maxR_H1PPi_H2PPi < 0.98)")
	skimtree["SRG3b N-1"] = intree[regionName].CopyTree("((cleaning&0x30F)==0)* ( deltaQCD > 0)* ( RPT_HT5PP < 0.08  )* ( R_H2PP_H5PP > 0.2)* ( R_HT5PP_H5PP > 0.65)* ( RPZ_HT5PP < 0.6)* ( minR_pTj2i_HT3PPi > 0.08)* ( maxR_H1PPi_H2PPi < 0.98)* ( H2PP > 900)")
	skimtree["SRG3b"] = intree[regionName].CopyTree("((cleaning&0x30F)==0)* ( deltaQCD > 0)* ( RPT_HT5PP < 0.08  )* ( R_H2PP_H5PP > 0.2)* ( R_HT5PP_H5PP > 0.65)* ( RPZ_HT5PP < 0.6)* ( minR_pTj2i_HT3PPi > 0.08)* ( maxR_H1PPi_H2PPi < 0.98)* ( H2PP > 900)*(HT5PP>2800)")

	c = TCanvas("c","c",1400,300)

	colors = [1,2,3,4]


	legend = TLegend(0.7,0.7,0.9,0.9)

	for itree,mytree in enumerate(skimtree):
		h_num[mytree] = f.Get("lumi_histo").Clone("h_num_%s"%mytree)
		h_num[mytree].Scale(0)

		for event in skimtree[mytree]:
			runNumber = event.RunNumber
			if h_num[mytree].GetXaxis().FindFixBin(str(runNumber)) != -1:
				h_num[mytree].Fill(str(runNumber) , 1.)

		h_eff[mytree] = h_num[mytree].Clone(mytree)
		h_eff[mytree].Divide(h_num[mytree],h_den,1,1,"B")
		h_eff[mytree].GetYaxis().SetTitle("Lumi-Normalized Acceptance");
		h_eff[mytree].SetLineColor(colors[itree])
		h_eff[mytree].SetMarkerColor(colors[itree])
		h_eff[mytree].SetMarkerStyle(20)
		h_eff[mytree].SetMarkerSize(0.5)

		gPad.SetLogy()
		h_eff[mytree].Draw("same" if itree > 0 else "")
		legend.AddEntry(h_eff[mytree], mytree ,"LP")

	legend.SetBorderSize(1)
	legend.SetTextSize(0.03)
	legend.Draw()

	ATLASLabel(0.2,0.9,"Internal          %s"%regionName)
	c.SaveAs("AcceptanceVsRun_%s.pdf"%regionName)





c = TCanvas("c","c",1400,300)
h_den.SetMarkerStyle(20)
h_den.SetMarkerSize(0.5)

h_den.Draw()

ATLASLabel(0.2,0.9,"Internal ")
c.SaveAs("LumiVsRun.pdf")






c = TCanvas("c","c",600,600)

integratedLumi = []
expectedZValue = []
expectedUpZValue = []
expectedDownZValue = []
observedZValue = []
tmpIntegratedLumi = 0.0

for ibin in xrange( h_den.GetNbinsX() ):
	if tmpIntegratedLumi/1000.>22.1:
		break
	tmpIntegratedLumi += h_den.GetBinContent(ibin)

	nobs = h_num["SRG3b"].Integral(0,ibin)
	nexp = 2.8*tmpIntegratedLumi/(22.1 * 1000.)
	nexpsig = 10*tmpIntegratedLumi/(22.1 * 1000.)

	integratedLumi.append(tmpIntegratedLumi/1000.)

	tmpPvalue = RooStats.NumberCountingUtils.BinomialObsP(nexpsig,nexp,0.27)/2.
	tmpZvalue = RooStats.PValueToSignificance( tmpPvalue ) if tmpPvalue else 0
	expectedZValue.append( tmpZvalue )

	tmpPvalue = RooStats.NumberCountingUtils.BinomialObsP(nexpsig,nexp*(1+0.27),0.27)/2.
	tmpZvalue = RooStats.PValueToSignificance( tmpPvalue ) if tmpPvalue else 0
	expectedUpZValue.append( tmpZvalue )
	tmpPvalue = RooStats.NumberCountingUtils.BinomialObsP(nexpsig,nexp*(1-0.27),0.27)/2.
	tmpZvalue = RooStats.PValueToSignificance( tmpPvalue ) if tmpPvalue else 0
	expectedDownZValue.append( tmpZvalue )

	tmpPvalue = RooStats.NumberCountingUtils.BinomialObsP(nobs,nexp,0.27)/2.
	tmpZvalue = RooStats.PValueToSignificance( tmpPvalue ) if tmpPvalue else 0
	observedZValue.append(  tmpZvalue )



gr_obs = TGraph( len(integratedLumi)  ,
	array('d',integratedLumi),
	array('d',observedZValue) )
gr_exp = TGraph( len(integratedLumi)  ,
	array('d',integratedLumi),
	array('d',expectedZValue) )
gr_exp_up = TGraph( len(integratedLumi)  ,
	array('d',integratedLumi),
	array('d',expectedUpZValue) )
gr_exp_down = TGraph( len(integratedLumi)  ,
	array('d',integratedLumi),
	array('d',expectedDownZValue) )

gr_exp.SetLineWidth(2)
gr_exp.SetLineColor(kBlue)
gr_exp.SetLineStyle(2)


gr_exp_up.SetLineWidth(1)
gr_exp_up.SetLineColor(kBlue)
gr_exp_up.SetLineStyle(3)
gr_exp_down.SetLineWidth(1)
gr_exp_down.SetLineColor(kBlue)
gr_exp_down.SetLineStyle(3)

gr_obs.SetMarkerStyle(20)
gr_obs.SetMarkerSize(0.6)

gr_exp.GetXaxis().SetTitle("Integrated Luminosity [fb^{-1}]")
gr_exp.GetYaxis().SetTitle("Significance")
gr_exp.GetYaxis().SetRangeUser(0,4)
gr_exp.SetMaximum(4)

gr_exp.Draw("AL")
gr_exp_up.Draw("L")
gr_exp_down.Draw("L")
gr_obs.Draw("LP")

line = TLine()
line.SetLineStyle(7)
line.DrawLine(13.3,0,13.3,3)
line.DrawLine(22.1,0,22.1,3)

text = TLatex()
text.SetTextAngle(90)
text.SetTextSize(0.02)
text.DrawText(13.2,0.1,"ICHEP")
text.DrawText(22.0,0.1,"22.1 ifb")


gPad.SetGrid()
ATLASLabel(0.2,0.9,"Internal          SRG3b")

c.SaveAs("SignificanceVsLumi.pdf")








