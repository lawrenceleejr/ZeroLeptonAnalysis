#!/usr/local/bin/python

from ROOT import *

from collections import OrderedDict


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
intree["CRWT"] = ftree.Get("Data_CRWT")
intree["CRZ"] = ftree.Get("Data_CRZ")
intree["CRY"] = ftree.Get("Data_CRY")

for regionName in intree:

	skimtree = OrderedDict()

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

