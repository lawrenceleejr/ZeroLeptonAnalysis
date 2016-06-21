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
from collections import OrderedDict

import ChannelsDict


import atexit
@atexit.register
def quite_exit():
	ROOT.gSystem.Exit(0)

logging.info("loading packages")
ROOT.gROOT.Macro("$ROOTCOREDIR/scripts/load_packages.C")

ROOT.TH1.SetDefaultSumw2() 

# directory = "/afs/cern.ch/work/r/rogan/public/RJWorkshopSamples/v57_sys/"
# datadirectory = "/afs/cern.ch/work/r/rogan/public/RJWorkshopSamples/v57_sys/"
# signaldirectory = "/afs/cern.ch/work/r/rogan/public/RJWorkshopSamples/v57_sys/"

directory = "/afs/cern.ch/work/r/rogan/public/RJWorkshopSamples/v103_sys/"
datadirectory = "/afs/cern.ch/work/r/rogan/public/RJWorkshopSamples/v103_sys/"
signaldirectory = "/afs/cern.ch/work/r/rogan/public/RJWorkshopSamples/v103_sys/"


# treename = "%s_SRAll"%sampleHandlerName
# treename = "%s_CRWT"%sampleHandlerName
# treename = "CRWT"
treename = "CRZ"
# treename = "CRY"
# treename = "SRAll"


# HistFitterRegion = "SR"
# HistFitterRegion = "CRW"
# HistFitterRegion = "CRT"
HistFitterRegion = "VRZ"

my_SHs = {}
for sampleHandlerName in [
							"QCD",
							"GammaJet",
							"Wjets",
							"Zjets",
							"Top",
							"Diboson",
							]:

	print sampleHandlerName
	my_SHs[sampleHandlerName] = ROOT.SH.SampleHandler(); 
	ROOT.SH.ScanDir().sampleDepth(0).samplePattern("%s.*"%sampleHandlerName).scan(my_SHs[sampleHandlerName], directory+"/" ) #"/BKG/"
	print my_SHs[sampleHandlerName]
	print len(my_SHs[sampleHandlerName])

	tmpTreeName = sampleHandlerName
	if sampleHandlerName == "GammaJet":
		tmpTreeName = "GAMMA"

	if sampleHandlerName == "Wjets":
		tmpTreeName = "W"

	if sampleHandlerName == "Zjets":
		tmpTreeName = "Z"

	my_SHs[sampleHandlerName].setMetaString("nc_tree", "%s_%s"%(tmpTreeName, treename) )
	pass



commonPlots  = {
# "H5PP" : [50, 0, 10000],      
"MET"  : [100, 0, 10000],     
"Meff" : [100, 0, 10000],      
}


commonPlots2D  = {
# ("MET","Meff") : ([50, 0, 3000] , [50, 0, 3000]   ),      
# ("deltaQCD","R_H2PP_H3PP") : ([50, -1, 1] , [50, 0, 1]   ),      
}



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
		if treename in treeName and treename+"_" not in treeName:
			print treeName
			my_SHs[treeName] = ROOT.SH.SampleHandler(); 
			ROOT.SH.ScanDir().sampleDepth(0).samplePattern("%s.root"%sampleHandlerName).scan(my_SHs[treeName], signaldirectory)
			my_SHs[treeName].setMetaString("nc_tree", "%s"%treeName )



for sampleHandlerName in [
						"DataMain2015",
						# "DataMain2016",
							]:
	my_SHs[sampleHandlerName] = ROOT.SH.SampleHandler(); 
	ROOT.SH.ScanDir().sampleDepth(0).samplePattern("%s.root"%sampleHandlerName).scan(my_SHs[sampleHandlerName], datadirectory)
	print my_SHs[sampleHandlerName]
	print len(my_SHs[sampleHandlerName])
	my_SHs[sampleHandlerName].setMetaString("nc_tree", "Data_%s"%treename )

	for sample in my_SHs[sampleHandlerName]:
		print sample
		print sample.makeTChain().GetEntries()


def removeUnusedCuts(cutList):
	cutList = [ x for x in cutList if "NJet" not in x \
								and not("pT_jet" in x and "-1" in x ) \
								and "veto" not in x   \
								and "abs(timing)" not in x \
								and "cleaning&" not in x \
								and "m_jet1_chf" not in x]
	return cutList

def constructLimitsDict(cutDict,cutList):
	for icut in cutList:
		limits = (50,0,1)
		if "R_" in icut:
			limits = (50,0,1)
		elif "deltaQCD" in icut:
			limits = (50,-1,1)
		elif "RPT" in icut:
			limits = (50,0,0.5)
		elif "RPZ" in icut:
			limits = (50,0,1)
		elif "HT" in icut and "PP" in icut:
			limits = (50,0,4000)
		elif "H2PP" in icut:
			limits = (50,0,2000)
		elif "MS" in icut:
			limits = (50,0,2000)
		elif "PTISR" in icut:
			limits = (50,0,2000)
		elif "dphi" in icut:
			limits = (50,0,4)
		elif "NV" in icut or "nBJet" in icut:
			limits = (10,0,10)
		cutDict[ "( %s )"%icut ] = limits
	return cutDict

cuts = {}
limits = {}


#############################################################
## Loose Plotting Regions

cuts["SRSLoose"] = OrderedDict()
cuts["SRSLoose"]["( deltaQCD > 0)"]           = (50,-1,1)
cuts["SRSLoose"]["( RPT_HT3PP < 0.2  )"]     = (50,0,1)
cuts["SRSLoose"]["( R_H2PP_H3PP > 0.2)"]      = (50,0,1)
cuts["SRSLoose"]["( RPZ_HT3PP < 0.8)"]       = (50,0,1)
cuts["SRSLoose"]["( pT_jet2 / HT3PP > 0.15)"] = (50,0,0.5)
cuts["SRSLoose"]["( HT3PP > 800)"]            = (50,0,4000)    
cuts["SRSLoose"]["( H2PP > 800)"]             = (50,0,2000)    

cuts["SRGLoose"] = OrderedDict()
cuts["SRGLoose"]["( deltaQCD > 0)"]              = (50,-1,1)
cuts["SRGLoose"]["( RPT_HT5PP < 0.2 )"]          = (50,0,1)
cuts["SRGLoose"]["( R_H2PP_H5PP > 0.2)"]         = (50,0,1)
cuts["SRGLoose"]["( R_HT5PP_H5PP > 0.2)"]        = (50,0,1)
cuts["SRGLoose"]["( RPZ_HT5PP < 0.8)"]           = (50,0,1)
cuts["SRGLoose"]["( minR_pTj2i_HT3PPi > 0.1)"]   = (50,0,0.5)
cuts["SRGLoose"]["( maxR_H1PPi_H2PPi < 1)"]      = (50,0.5,1)
cuts["SRGLoose"]["( HT5PP > 800)"]               = (50,0,4000)
cuts["SRGLoose"]["( H2PP > 800)"]                = (50,0,2000)   

cuts["SRCLoose"] = OrderedDict()
cuts["SRCLoose"]["( RISR > 0.6 )"]     = (50,0,1)      
cuts["SRCLoose"]["( MS > 0 )"]         = (50,0,2000)   
cuts["SRCLoose"]["( dphiISRI > 1.5 )"] = (50,0,4)         
cuts["SRCLoose"]["( dphiMin2 > 0.4   )"]   = (50,0,4)      
cuts["SRCLoose"]["( PTISR > 300  )"]   = (50,0,2000)       
cuts["SRCLoose"]["( NV > 0  )"]        = (10,0,10)  


#############################################################
## Squark RJR
squarkRegions = [
		"SRJigsawSRS1a",
		"SRJigsawSRS1b",
		"SRJigsawSRS2a",
		"SRJigsawSRS2b",
		"SRJigsawSRS3a",
		"SRJigsawSRS3b",
		]

##############################################################
#Gluino RJR
gluinoRegions = [
		"SRJigsawSRG1a",
		"SRJigsawSRG1b",
		"SRJigsawSRG2a",
		"SRJigsawSRG2b",
		"SRJigsawSRG3a",
		"SRJigsawSRG3b",
		]

## Compressed stuff: ##########################
compressedRegions = [
		"SRJigsawSRC1",
		"SRJigsawSRC2",
		"SRJigsawSRC3",
		"SRJigsawSRC4",
		"SRJigsawSRC5",
		]


allRegions = squarkRegions + gluinoRegions + compressedRegions


for iRegion in allRegions:
	tmpcuts = removeUnusedCuts( ChannelsDict.finalChannelsDict[iRegion].getCutsDict()[HistFitterRegion][1:-1].split("&&")  )
	cuts[iRegion] = OrderedDict()
	constructLimitsDict( cuts[iRegion], tmpcuts )
	print iRegion
	print cuts[iRegion]


print "*".join( cuts["SRJigsawSRC1"].keys() )
print "*".join( cuts["SRJigsawSRS1a"].keys() )
print "*".join( cuts["SRJigsawSRG1a"].keys() )
# print "*".join( cuts["SRSLoose"].keys() )

# region = {}
# region["Sdf"]

if HistFitterRegion=="SR":
	cleaning = "(  veto == 0  )*(  (abs(timing) < 4)  )*(  ((cleaning&(0x80+3)) < 1)  )"
if HistFitterRegion=="CRW" or HistFitterRegion=="CRT":
	cleaning = "(  veto == 0  )*(  (abs(timing) < 4)  )*(  ((cleaning&(15+256)) < 1)  )"
if HistFitterRegion=="CRZ" or HistFitterRegion=="VRZ":
	cleaning = "(  veto == 0  )*(  (abs(timing) < 4)  )*(  ((cleaning&(7+0x80)) < 1)  )"
if HistFitterRegion=="CRY":
	cleaning = "(  veto == 0  )*(  (abs(timing) < 4)  )*(  ((cleaning&(15+256)) < 1)  )"


## Define your cut strings here....
regions = {
	# "no_cut": "(1)",

	"SRJigsawSRS1a": cleaning+"*"+"*".join( cuts["SRJigsawSRS1a"].keys() ),
	"SRJigsawSRS1b": cleaning+"*"+"*".join( cuts["SRJigsawSRS1b"].keys() ),
	"SRJigsawSRS2a": cleaning+"*"+"*".join( cuts["SRJigsawSRS2a"].keys() ),
	"SRJigsawSRS2b": cleaning+"*"+"*".join( cuts["SRJigsawSRS2b"].keys() ),
	"SRJigsawSRS3a": cleaning+"*"+"*".join( cuts["SRJigsawSRS3a"].keys() ),
	"SRJigsawSRS3b": cleaning+"*"+"*".join( cuts["SRJigsawSRS3b"].keys() ),

	"SRJigsawSRG1a": cleaning+"*"+"*".join( cuts["SRJigsawSRG1a"].keys() ),
	"SRJigsawSRG1b": cleaning+"*"+"*".join( cuts["SRJigsawSRG1b"].keys() ),
	"SRJigsawSRG2a": cleaning+"*"+"*".join( cuts["SRJigsawSRG2a"].keys() ),
	"SRJigsawSRG2b": cleaning+"*"+"*".join( cuts["SRJigsawSRG2b"].keys() ),
	"SRJigsawSRG3a": cleaning+"*"+"*".join( cuts["SRJigsawSRG3a"].keys() ),
	"SRJigsawSRG3b": cleaning+"*"+"*".join( cuts["SRJigsawSRG3b"].keys() ),

	"SRJigsawSRC1": cleaning+"*"+"*".join( cuts["SRJigsawSRC1"].keys() ),
	"SRJigsawSRC2": cleaning+"*"+"*".join( cuts["SRJigsawSRC2"].keys() ),
	"SRJigsawSRC3": cleaning+"*"+"*".join( cuts["SRJigsawSRC3"].keys() ),
	"SRJigsawSRC4": cleaning+"*"+"*".join( cuts["SRJigsawSRC4"].keys() ),
	"SRJigsawSRC5": cleaning+"*"+"*".join( cuts["SRJigsawSRC5"].keys() ),

	"SRSLoose": cleaning+"*"+"*".join( cuts["SRSLoose"].keys() ),
	"SRGLoose": cleaning+"*"+"*".join( cuts["SRGLoose"].keys() ),
	"SRCLoose": cleaning+"*"+"*".join( cuts["SRCLoose"].keys() ),

}


for SH_name, mysamplehandler in my_SHs.iteritems():

	job = ROOT.EL.Job()
	job.sampleHandler(mysamplehandler)

	cutflow = {}

	if "Data" in SH_name:
		weightstring = "(1)"
	else:
		weightstring = "weight*WZweight"

	if "CRWT" in treename :#and "Data" not in SH_name:
		weightstring = weightstring + "*(bTagWeight)"

	if "CRY" in treename:
		weightstring = weightstring + "*(phSignal[0]==1 && phPt[0]>130.)"
		if "Data" not in SH_name:
			if "QCD" in SH_name:
				weightstring = weightstring + "*(phTruthOrigin[0]!=38)"

	weightstring += "*(%s)"%cleaning


	for region in regions:

		if "SR" in region:
			# ## This part sets up both N-1 hists and the cutflow histogram for region

			cutflow[region] = ROOT.TH1F ("cutflow_%s"%region, "cutflow_%s"%region, len(cuts[region])+1 , 0, len(cuts[region])+1 );
			cutflow[region].GetXaxis().SetBinLabel(1, weightstring);
			# cutflow[region].GetXaxis().SetBinLabel(2, cleaning);

			for i,cutpart in enumerate(cuts[region]):

				cutpartname = cutpart.translate(None, " (),.").replace("*","_x_").replace("/","_over_").replace(">=",">").replace("<=","<").split(" < ")[0].split(" > ")[0]
				variablename = cutpart.split("<")[0].split(">")[0]+")"

				if "Data" not in SH_name or "Loose" in region or HistFitterRegion!="SR":
					job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("%s_minus_%s"%(region,cutpartname), "%s_%s"%(region,cutpartname), cuts[region][cutpart][0], cuts[region][cutpart][1], cuts[region][cutpart][2] ), variablename ,weightstring+"*%s"%"*".join(["(%s)"%mycut for mycut in cuts[region] if mycut!=cutpart ])    )        )
				else:
					flippedcutpart = cutpart.replace(">","%TEMP%").replace("<",">").replace("%TEMP%","<")
					job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("%s_minus_%s"%(region,cutpartname), "%s_%s"%(region,cutpartname), cuts[region][cutpart][0], cuts[region][cutpart][1], cuts[region][cutpart][2] ), variablename ,weightstring+"*%s"%"*".join(["(%s)"%mycut for mycut in cuts[region] if mycut!=cutpart ]) + "*" + flippedcutpart  )        )

				cutpart = cutpart.replace(")","").replace("(","").replace(">=",">").replace("<=","<")
				# print cutpart
				cutflow[region].GetXaxis().SetBinLabel (i+2, cutpart);

			job.algsAdd(ROOT.MD.AlgCFlow (cutflow[region]))


		if "CR" in region:
			# ## This part sets up both N-1 hists and the cutflow histogram for region

			cutflow[region] = ROOT.TH1F ("cutflow_%s"%region, "cutflow_%s"%region, len(cuts[region])+2 , 0, len(cuts[region])+2 );
			cutflow[region].GetXaxis().SetBinLabel(1, weightstring);
			# cutflow[region].GetXaxis().SetBinLabel(2, baseline);

			for i,cutpart in enumerate(cuts[region]):

				cutpartname = cutpart.translate(None, " (),.").replace("*","_x_").replace("/","_over_").split(" < ")[0].split(" > ")[0]
				variablename = cutpart.split("<")[0].split(">")[0]+")"

				job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("%s_minus_%s"%(region,cutpartname), "%s_%s"%(region,cutpartname), cuts[region][cutpart][0], cuts[region][cutpart][1], cuts[region][cutpart][2] ), variablename ,weightstring+"*%s"%"*".join(["(%s)"%mycut for mycut in cuts[region] if mycut!=cutpart ])    )        )

				cutflow[region].GetXaxis().SetBinLabel (i+2, cutpart);

			job.algsAdd(ROOT.MD.AlgCFlow (cutflow[region]))

		###################################################################

		## each of this histograms will be made for each region

		if not('QCD' in region):
			for varname,varlimits in commonPlots.items() :
				# print varname
				job.algsAdd(
	            	ROOT.MD.AlgHist(
	            		ROOT.TH1F(varname+"_%s"%region, varname+"_%s"%region, varlimits[0], varlimits[1], varlimits[2]),
						varname,
						weightstring+"*%s"%regions[region]
						)
					)


		# if "QCD" in region:

		for varname,varlimits in commonPlots2D.items():
			# print varname
			job.algsAdd(
            	ROOT.MD.AlgHist(
            		ROOT.TH2F("%s_%s_%s"%(varname[0], varname[1], region), "%s_%s_%s"%(varname[0], varname[1], region), varlimits[0][0], varlimits[0][1], varlimits[0][2], varlimits[1][0], varlimits[1][1], varlimits[1][2]),
					varname[0], varname[1],
					weightstring+"*%s"%regions[region]
					)
				)

	driver = ROOT.EL.DirectDriver()
	if os.path.exists( "output/"+SH_name ):
		shutil.rmtree( "output/"+SH_name )
	driver.submit(job, "output/"+SH_name )



