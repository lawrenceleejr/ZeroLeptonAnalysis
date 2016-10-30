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
import multiprocessing as mp


import atexit
@atexit.register
def quite_exit():
	ROOT.gSystem.Exit(0)

logging.info("loading packages")
ROOT.gROOT.Macro("$ROOTCOREDIR/scripts/load_packages.C")

ROOT.TH1.SetDefaultSumw2()


directory = "/data/jack/ICHEP/0Lepton/v111/RJ_submit_28072016/"
datadirectory = "/data/larryl/ZeroLepton/v111/"
signaldirectory = "/data/jack/ICHEP/0Lepton/v111/RJ_submit_28072016/"


regionNames = ["SR","CRW","CRT","CRY"]

ncores = 6
# regionNames = ["CRY"]

blindSR = False

import ChannelsDict


print "\n++++++++++++++++++++++++++++++++++++++++++++++\n\n"
print "List of region names to run over: " 
print regionNames


def submitTheThing(driver,job,directory):
	driver.submit(job, directory )

def submitTheThingWrapper(stuff):
	submitTheThing(*stuff)

for regionName in regionNames:

	print "Running over region: %s"%regionName

	extraCutsFromChannel = ChannelsDict.finalChannelsDict["SRJigsawSRG1a"].regionDict[regionName].extraCutList
	weightStringFromChannel = ChannelsDict.finalChannelsDict["SRJigsawSRG1a"].getWeights(regionName)
	cutString = ChannelsDict.finalChannelsDict["SRJigsawSRG1a"].getCuts(regionName)
	treename = ChannelsDict.finalChannelsDict["SRJigsawSRG3b"].getSuffixTreeName(regionName)

	my_SHs = {}
	for sampleHandlerName in [
								"QCD",
								"GammaJet",
								"WMassiveCB",
								"ZMassiveCB",
								"Top",
								"DibosonMassiveCB",
								]:

		print sampleHandlerName
		my_SHs[sampleHandlerName] = ROOT.SH.SampleHandler();
		ROOT.SH.ScanDir().sampleDepth(0).samplePattern("%s.*"%sampleHandlerName).scan(my_SHs[sampleHandlerName], directory+"/" ) #"/BKG/"
		print len(my_SHs[sampleHandlerName])

		tmpTreeName = sampleHandlerName
		if sampleHandlerName == "GammaJet":
			tmpTreeName = "GAMMA"

		if sampleHandlerName == "WMassiveCB":
			tmpTreeName = "W"

		if sampleHandlerName == "ZMassiveCB":
			tmpTreeName = "Z"
		if sampleHandlerName == "DibosonMassiveCB":
			tmpTreeName = "Diboson"

		my_SHs[sampleHandlerName].setMetaString("nc_tree", "%s_%s"%(tmpTreeName, treename) )
		pass



	commonPlots  = {
	# "H5PP" : [50, 0, 10000],
	"MET"  : [20, 0, 5000],
	"Meff" : [20, 0, 5000],
	"Meff-MET" : [20, 0, 5000],
	"MET/(MET+pT_jet1+pT_jet2+pT_jet3+pT_jet4)" : [50, 0, 1],
	"Aplan" : [20, 0, 0.5],
	"metTST" : [20, 0, 200],
	"dphi" : [20, 0, 4],
	"pT_jet1" : [20, 0, 2000],
	"pT_jet4" : [20, 0, 1000],
	"eta_jet1" : [20, -5, 5],
	"eta_jet4" : [20, -5, 5],
	"NJet" : [20, 0, 20],
	"nBJet" : [20, 0, 20],
	}


	commonPlots2D  = {
	# ("MET","Meff") : ([50, 0, 3000] , [50, 0, 3000]   ),
	# ("deltaQCD","R_H2PP_H3PP") : ([50, -1, 1] , [50, 0, 1]   ),
	}


	for sampleHandlerName in [
							# "SS_direct",
							"GG_direct",
							# "GG_onestepCC_fullsim"
								]:

		f = ROOT.TFile("%s/%s.root"%(signaldirectory,sampleHandlerName) )
		treeList = []
		dirList = ROOT.gDirectory.GetListOfKeys()
		for k1 in dirList:
			t1 = k1.ReadObj()
			if (type(t1) is ROOT.TTree  ):
				treeList.append(t1.GetName())

		for treeName in treeList:
			if "1800_0" not in treeName:
				continue
			if treename in treeName and treename+"_" not in treeName:
				my_SHs[treeName] = ROOT.SH.SampleHandler();
				ROOT.SH.ScanDir().sampleDepth(0).samplePattern("%s.root"%sampleHandlerName).scan(my_SHs[treeName], signaldirectory)
				my_SHs[treeName].setMetaString("nc_tree", "%s"%treeName )



	for sampleHandlerName in [
							"DataMain",
								]:
		my_SHs[sampleHandlerName] = ROOT.SH.SampleHandler();
		ROOT.SH.ScanDir().sampleDepth(0).samplePattern("%s.root"%sampleHandlerName).scan(my_SHs[sampleHandlerName], datadirectory)
		print len(my_SHs[sampleHandlerName])
		my_SHs[sampleHandlerName].setMetaString("nc_tree", "Data_%s"%treename )

		# for sample in my_SHs[sampleHandlerName]:
		# 	print sample
		# 	print sample.makeTChain().GetEntries()




	## Define your cut strings here....
	regions = {
		# "no_cut": "(1)",

		"SRG1a": ChannelsDict.finalChannelsDict["SRJigsawSRG1a"].getCuts(regionName),
		"SRG1b": ChannelsDict.finalChannelsDict["SRJigsawSRG1b"].getCuts(regionName),
		"SRG2a": ChannelsDict.finalChannelsDict["SRJigsawSRG2a"].getCuts(regionName),
		"SRG2b": ChannelsDict.finalChannelsDict["SRJigsawSRG2b"].getCuts(regionName),
		"SRG3a": ChannelsDict.finalChannelsDict["SRJigsawSRG3a"].getCuts(regionName),
		"SRG3b": ChannelsDict.finalChannelsDict["SRJigsawSRG3b"].getCuts(regionName),

		"SRG1Common": ChannelsDict.finalChannelsDict["SRJigsawSRG1Common"].getCuts(regionName),
		"SRG2Common": ChannelsDict.finalChannelsDict["SRJigsawSRG2Common"].getCuts(regionName),
		"SRG3Common": ChannelsDict.finalChannelsDict["SRJigsawSRG3Common"].getCuts(regionName),

	}

	job = {}

	for SH_name, mysamplehandler in my_SHs.iteritems():

		job[SH_name] = ROOT.EL.Job()
		job[SH_name].sampleHandler(mysamplehandler)

		cutflow = {}

		if "Data" in SH_name:
			weightstring = "(1)"
		else:
			weightstring = "(%s)"%weightStringFromChannel



		for region in regions:

			cutlist = regions[region][1:-1].split("&&")

			cutflow[region] = ROOT.TH1F ("cutflow_%s"%region, "cutflow_%s"%region, len(cutlist)+1 , 0, len(cutlist)+1);
			cutflow[region].GetXaxis().SetBinLabel(1, weightstring);


			for i,cutpart in enumerate(cutlist):

				skipCut = False
				for extraCut in extraCutsFromChannel:
					if cutpart.translate(None, " ") in extraCut:
						skipCut = True
						break
				if skipCut:
					continue

				cutpartname = cutpart.translate(None, " (),.")
				cutpartname = cutpartname.replace("*","_x_").replace("/","_over_")
				cutpartname = cutpartname.split("<=")[0].split(">=")[0].split("==")[0]\
											.split("<")[0].split(">")[0]

				variablename = cutpart.split("<=")[0].split(">=")[0].split("==")[0]\
											.split("<")[0].split(">")[0].replace("((","(").replace("( abs","abs")

				# print variablename

				limits = (20,0,1)
				if "deltaQCD" in variablename:
					limits = (20,-1,1)
				elif "RPZ_" in variablename:
					limits = (20,0,0.5)
				elif " minR_pTj2i_HT3PPi " in variablename:
					limits = (20,0,0.5)
				elif " maxR_H1PPi_H2PPi "  in variablename:
					limits = (20,0.5,1)
				elif " HT5PP " in variablename:
					limits = (20,0,4000)
				elif " H2PP " in variablename:
					limits = (20,0,3000)
				elif "lep1Pt" in variablename:
					limits = (20,0,200)


				if "Data" in SH_name and blindSR:
					# Flip the cut so the region is blinded
					flippedcutpart = cutpart.replace(">","%TEMP%").replace("<",">").replace("%TEMP%","<")
					job[SH_name].algsAdd(  ROOT.MD.AlgHist(
						ROOT.TH1F("%s_minus_%s"%(region,cutpartname),
							"%s_%s"%(region,cutpartname),
							limits[0], limits[1], limits[2]),
						variablename,
						weightstring+"*%s"%"*".join(["(%s)"%mycut for mycut in cutlist if mycut!=cutpart ]) + "*" + flippedcutpart
						)
					)
				else:
					# Don't blind anything above the cut
					job[SH_name].algsAdd(  ROOT.MD.AlgHist(
						ROOT.TH1F("%s_minus_%s"%(region,cutpartname),
							"%s_%s"%(region,cutpartname),
							limits[0], limits[1], limits[2]),
						variablename,
						weightstring+"*%s"%"*".join(["(%s)"%mycut for mycut in cutlist if mycut!=cutpart ])
						)
					)

				cutflow[region].GetXaxis().SetBinLabel (i+2, cutpart);

			job[SH_name].algsAdd(ROOT.MD.AlgCFlow (cutflow[region]))


			## each of this histograms will be made for each region
			for varname,varlimits in commonPlots.items() :
				job[SH_name].algsAdd(
	            	ROOT.MD.AlgHist(
	            		ROOT.TH1F(varname.replace("/","_over_")+"_%s"%region, varname+"_%s"%region, varlimits[0], varlimits[1], varlimits[2]),
						varname,
						weightstring+"*%s"%regions[region]
						)
					)

			for varname,varlimits in commonPlots2D.items():
				job[SH_name].algsAdd(
	            	ROOT.MD.AlgHist(
	            		ROOT.TH2F("%s_%s_%s"%(varname[0], varname[1], region), "%s_%s_%s"%(varname[0], varname[1], region), varlimits[0][0], varlimits[0][1], varlimits[0][2], varlimits[1][0], varlimits[1][1], varlimits[1][2]),
						varname[0], varname[1],
						weightstring+"*%s"%regions[region]
						)
					)

	driver = ROOT.EL.DirectDriver()

	jobs = []
	outputDirs = []
	for SH_name, mysamplehandler in my_SHs.iteritems():
		if not os.path.exists( "output/%s"%( regionName ) ):
			os.makedirs( "output/%s/"%( regionName ) )
		if os.path.exists( "output/%s/%s"%( regionName, SH_name ) ):
			shutil.rmtree( "output/%s/%s"%( regionName, SH_name ) )
		jobs.append(job[SH_name])
		outputDirs.append("output/%s/%s"%( regionName, SH_name ) )



	pool = mp.Pool(processes=ncores)
	pool.map(submitTheThingWrapper,
		itertools.izip( itertools.repeat(driver),
			jobs,
			outputDirs )
		)
	pool.close()
	pool.join()

	os.system("tar cvzf {0}.tgz output/{0}/*/hist-*.root".format( regionName )   )

