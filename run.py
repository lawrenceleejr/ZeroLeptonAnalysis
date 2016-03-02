#!/usr/bin/env python

########### Initialization ######################################
##
##

import ROOT
import logging
import shutil
import os
import itertools
import re

logging.basicConfig(level=logging.INFO)
from optparse import OptionParser

from copy import deepcopy

import atexit
@atexit.register
def quite_exit():
	ROOT.gSystem.Exit(0)


logging.info("loading packages")
ROOT.gROOT.Macro("$ROOTCOREDIR/scripts/load_packages.C")

ROOT.TH1.SetDefaultSumw2()

directory = "/afs/cern.ch/work/r/rogan/public/RJWorkshopSamples/v57_sys/"
# datadirectory = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v53_Data_pT50/"
signaldirectory = "/afs/cern.ch/work/r/rogan/public/RJWorkshopSamples/v57_sys/"
# signaldirectory = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v53_Anum_pT50/"

# directory = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v53_Anum_pT50/"
# signaldirectory = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v53_Anum_pT50/"

#directory = "/mnt/shared/leejr/Work/WorkshopNtuples/"
#signaldirectory = directory

bgkfiletreedict = {
	"QCD" : "QCD_SRAll",
	"Wjets": "W_SRAll",
	"Zjets": "Z_SRAll",
	"Top"  : "Top_SRAll",
	"Diboson" :"Diboson_SRAll",
	}



my_SHs = {}
for sampleHandlerName in [
							"QCD",
							"Wjets",
							"Zjets",
							"Top",
							"Diboson",
							]:

	my_SHs[sampleHandlerName] = ROOT.SH.SampleHandler();
	ROOT.SH.ScanDir().sampleDepth(0).samplePattern("%s.root"%sampleHandlerName).scan(my_SHs[sampleHandlerName], directory)
	my_SHs[sampleHandlerName].setMetaString("nc_tree", ("%s_SRAll"%sampleHandlerName).replace("jets",""))
	pass


# limits["SR2jm"] = []
# limits["SR2jm"] +=  [(50,0,1000)]     #["( MET > 200 )"]
# limits["SR2jm"] +=  [(50,0,1000)]     #["( pT_jet1 > 200 )"]
# limits["SR2jm"] +=  [(50,0,1000)]     #["( pT_jet2 > 100 )"]
# limits["SR2jm"] +=  [(50,0,4)]     #["( dphi > 0.4 )"]
# limits["SR2jm"] +=  [(50,0,50)]     #["( MET/(MET+pT_jet1+pT_jet2+pT_jet3+pT_jet4+pT_jet5) > 0.25 )"]
# limits["SR2jm"] +=  [(50,0,4000)]     #["( Meff > 1600 )"]

intRange   = [10, 0 , 10  ]
ptRange    = [50, 0 , 1000]
scaleRange = [50, 0 , 4000]
ratioRange = [50, -1, 1   ]
angleRange = [50, 0 , 4   ]

commonPlots  = {
# 'pTPP_jet2a' : ptRange ,
#'nBJet'      : intRange ,
# 'NJ2b'      : intRange ,
# 'dH2o3P'    : ratioRange,
# 'NJ2a'      : intRange ,
 'RPZ_HT5PP':  ratioRange,
# 'pPP_jet3b':  ptRange,
 'dphi': angleRange,
# 'pTCM':ptRange,
# 'nCJet':intRange ,
 'RPZ_HT9PP':ratioRange,
# 'H3Pb': scaleRange,
# 'lept2Pt':ptRange,
# 'NJet':intRange ,
 # 'dphiPV1a':ratioRange,
 # 'dphiPV1b':ratioRange,
# 'lept1Pt':ptRange,
# 'pPP_jet2b':ptRange,
# 'pPP_jet2a':ptRange,
 'R_H2PP_H9PP':ratioRange,
# 'NJ1b':intRange ,
# 'NJ1a':intRange ,
# 'pTPP_V2b':ptRange,
# 'pPP_jet3a':ptRange,
 'dphiR':angleRange,
# 'cosPP':angleRange,
 'PP_VisShape':ptRange,
 'R_HT5PP_H5PP':ratioRange,
 'HT5PP':scaleRange,
 'Rsib':ratioRange,
# 'HT6PP':scaleRange,
# 'ddphiP':ratioRange,
# 'pZCM':ptRange,
# 'H5Pa':scaleRange,
# 'H5Pb':scaleRange,
 'MET'     :ptRange,
 'MET/Meff':ratioRange,

 'deltaQCD':ratioRange,
 'cosS':ratioRange,
 'cosP':ratioRange,
# 'H10PP':scaleRange,
 'R_H2PP_H5PP':ratioRange,
 # 'pPP_V2b':ptRange,
 # 'pPP_V2a':ptRange,
 'RPT_HT3PP':ratioRange,
 # 'pTPP_jet1':ptRange,
 # 'pTPP_jet2':ptRange,
 # 'pTPP_jet1a':ptRange,
 # 'pTPP_Va':ptRange,
# 'HT10PP':scaleRange,
 'NVS':ratioRange,
# 'HT6PP':scaleRange,
# 'pPP_Ib':ptRange,
 'HT3PP':scaleRange,
# 'pPP_Ia':ptRange,
# 'pPP_Vb':ptRange,
 'MS':scaleRange,
# 'NJb':intRange ,
# 'NJa':intRange ,
 'dangle':ratioRange,
 'RPT_HT5PP':ratioRange,
# 'dphiCV2a':ratioRange,
# 'dphiCV2b':ratioRange,
 # 'pT_jet6':ptRange,
 # 'pT_jet5':ptRange,
 # 'pT_jet4':ptRange,
 # 'pT_jet3':ptRange,
 # 'pT_jet2':ptRange,
 # 'pT_jet1':ptRange,
 # 'pT_jet1b':ptRange,
 # 'pT_jet1a':ptRange,
 # 'pTPP_V1a':ptRange,
 # 'pTPP_V1b':ptRange,
 # 'pTPP_jet1b':ptRange,
 # 'pTPP_Vb':ptRange,
# 'RPT_HT9PP':ratioRange,
 'MDR':scaleRange,
# 'Mll':scaleRange,
# 'H9PP':scaleRange,
# 'pTPP_jet3b':ptRange,
# 'pTPP_jet3a':ptRange,
 'maxR_H1PPi_H2PPi':ratioRange,
 'dphiPPV':ratioRange,
 'RPT_HT1CM':ratioRange,
 'Aplan':ratioRange,
 'R_pTj2_HT3PP':ratioRange,
# 'dphiPb':ratioRange,
# 'dphiPa':ratioRange,
 'HT1CM':ratioRange,
 'PIoHT1CM':ratioRange,
# 'pPP_V1b':ptRange,
# 'pPP_V1a':ptRange,
# 'phPt':ptRange,
# 'pPP_jet1b':ptRange,
 'H2PP':scaleRange,
# 'pPP_jet1a':ptRange,
 # 'H3Cb':scaleRange,
 # 'H3Ca':scaleRange,
 # 'H2Pb':scaleRange,
# 'cosV1a':ratioRange,
# 'cosV1b':ratioRange,
# 'H2Pa':scaleRange,
# 'pTPP_jet2b':ptRange,
# 'Idepth':intRange,
 'minR_pTj2i_HT3PPi':ratioRange,
# 'pTPP_Ib':ptRange,
 'HT9PP':scaleRange,
 'RPZ_HT3PP':ratioRange,
# 'pPP_Va':ptRange,
# 'sdphiP':ratioRange,
# 'MTW':scaleRange,
 # 'H2Cb':scaleRange,
 # 'H2Ca':scaleRange,
 'dphiVP':ratioRange,
 # 'H3Pa':scaleRange,
 # 'H4Pa':scaleRange,
 # 'H4Pb':scaleRange,
# 'pT_jet2b':ptRange,
 'Meff':scaleRange,
# 'pT_jet2a':ptRange,
# 'cosV2a':angleRange,
# 'cosV2b':angleRange,
 'HT3PP':scaleRange,
# 'H4PP':scaleRange,
 'R_HT9PP_H9PP':ratioRange,
# 'HT4PP':scaleRange,
# 'pTPP_Ia':ptRange,
# 'pTPP_V2a':ptRange,
 'sangle':ratioRange,
# 'HT5PP':scaleRange,
 'R_H2PP_H3PP': ratioRange,
}


commonPlots2D = {}
for key1, value1 in commonPlots.iteritems() :
	for key2, value2 in commonPlots.iteritems() :
		commonPlots2D[ (key1,key2) ] = (value1, value2)

#print commonPlots2D
print len(commonPlots2D)

for sampleHandlerName in [
						"SS_direct",
						"GG_direct",
						# "GG_onestepCC_fullsim"
							]:

	f = ROOT.TFile("%s/%s.root"%(signaldirectory,sampleHandlerName) )
	treeList = []
	dirList = ROOT.gDirectory.GetListOfKeys()
	for k1 in dirList:
		t1 = k1.ReadObj()
		if (type(t1) is ROOT.TTree  ):
			# print t1.GetName()
			treeList.append(t1.GetName())

	for treeName in treeList:
		if( (len(treeName.split("_"))) <= 5 ) :
			if "SRAll" in treeName:
				my_SHs[treeName] = ROOT.SH.SampleHandler();
				ROOT.SH.ScanDir().sampleDepth(0).samplePattern("%s.root"%sampleHandlerName).scan(my_SHs[treeName], signaldirectory)
				my_SHs[treeName].setMetaString("nc_tree", "%s"%treeName )

baseline    = "( pT_jet1 > 50.) * ( pT_jet2 > 50.) * ( MDR > 300.)"
baselineMET = "( pT_jet1 > 50.) * ( pT_jet2 > 50.) * ( MET > 200.)"


cuts = {}
limits = {}



## Define your cut strings here....
regions = {
	# "no_cut": "(1)",

        "baseline"   : baseline,
        "baselineMET": baselineMET,
}


for SH_name, mysamplehandler in my_SHs.iteritems():

	job = ROOT.EL.Job()
	job.sampleHandler(mysamplehandler)

	cutflow = {}


	for region in regions:


		if "SR" in region:
			# ## This part sets up both N-1 hists and the cutflow histogram for region

			cutflow[region] = ROOT.TH1F ("cutflow_%s"%region, "cutflow_%s"%region, len(cuts[region])+2 , 0, len(cuts[region])+2 );
			cutflow[region].GetXaxis().SetBinLabel(1, "weight");
			cutflow[region].GetXaxis().SetBinLabel(2, baseline);

			for i,cutpart in enumerate(cuts[region]):

				cutpartname = cutpart.translate(None, " (),.").replace("*","_x_").replace("/","_over_").split(" < ")[0].split(" > ")[0]
				variablename = cutpart.split("<")[0].split(">")[0]+")"

				# print variablename
				job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("%s_minus_%s"%(region,cutpartname), "%s_%s"%(region,cutpartname), limits[region][i][0], limits[region][i][1], limits[region][i][2] ), variablename ,baseline+"*weight*%s"%"*".join(["(%s)"%mycut for mycut in cuts[region] if mycut!=cutpart ])    )        )

				cutflow[region].GetXaxis().SetBinLabel (i+3, cutpart);

			job.algsAdd(ROOT.MD.AlgCFlow (cutflow[region]))


		###################################################################

		## each of this histograms will be made for each region


		for varname,varlimits in commonPlots.items() :
			# print varname
			job.algsAdd(
				ROOT.MD.AlgHist(
					ROOT.TH1F(varname.replace("/","")+"_%s"%region,
						  varname.replace("/","")+"_%s"%region,
						  varlimits[0], varlimits[1], varlimits[2]),
					varname,
					"weight*%s"%regions[region]
					)
				)

		for varname,varlimits in commonPlots2D.items():
			# print varname
			job.algsAdd(
            	ROOT.MD.AlgHist(
            		ROOT.TH2F("%s_%s_%s"%(varname[0].replace("/",""), varname[1].replace("/",""), region),
				  "%s_%s_%s"%(varname[0].replace("/",""), varname[1].replace("/",""), region),
				  varlimits[0][0], varlimits[0][1], varlimits[0][2],
				  varlimits[1][0], varlimits[1][1], varlimits[1][2]),
					varname[0], varname[1],
					"weight*%s"%regions[region]
					)
				)

	driver = ROOT.EL.LSFDriver()
#	driver = ROOT.EL.DirectDriver()
	job.options().setString(ROOT.EL.Job.optSubmitFlags, "-q 8nh");
	if os.path.exists( "/afs/cern.ch/work/r/rsmith/outputCorrelationPlotsv2/output/"+SH_name ):
		print 'can\'t print to there!!! you already have output there'
		exit()
#		shutil.rmtree( "/afs/cern.ch/work/r/rsmith/outputCorrelationPlots/output/"+SH_name )
	driver.submitOnly(job, "/afs/cern.ch/work/r/rsmith/outputCorrelationPlotsv2/output/"+SH_name )



