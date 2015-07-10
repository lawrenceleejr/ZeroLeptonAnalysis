#!/usr/bin/env python

########### Initialization ######################################
##
##

import ROOT
import logging
import shutil
import os
import itertools

import discoverInput

logging.basicConfig(level=logging.INFO)
from optparse import OptionParser

import atexit
@atexit.register
def quite_exit():
    ROOT.gSystem.Exit(0)


logging.info("loading packages")
ROOT.gROOT.Macro("$ROOTCOREDIR/scripts/load_packages.C")

##
##
########### Gather input ######################################
##
##

logging.info("creating new sample handler")
sh_all = ROOT.SH.SampleHandler()



lumi = 10000.
search_directories = ("/afs/cern.ch/work/l/leejr/public/SklimmerOutput/fromGrid/rucio/063015a/",)

discoverInput.discover(sh_all, search_directories)

sh_all.setMetaString("nc_tree", "SRAllNT")

ROOT.SH.readSusyMeta(sh_all,"./susy_crosssections_13TeV.txt")

logging.info("adding my tags defined in discoverInput.py")
discoverInput.addTags(sh_all)

sh_data = sh_all.find("data")
sh_signal = sh_all.find("signal")
sh_bg = {}

sh_bg["qcd"] = sh_all.find("qcd")
sh_bg["top"] = sh_all.find("top")
sh_bg["wjets"] = sh_all.find("wjets")
sh_bg["zjets"] = sh_all.find("zjets")



######This will be done per samplehandler ############################
##
##



tempDirDict = {   
	sh_data: "rundir_data",
	sh_signal: "rundir_signal",
	sh_bg["qcd"]: "rundir_qcd",
	sh_bg["top"]: "rundir_top",
	sh_bg["wjets"]: "rundir_wjets",
	sh_bg["zjets"]: "rundir_zjets",
    }


ROOT.TMVA.Tools.Instance()
fout = ROOT.TFile("test.root","RECREATE")
factory = ROOT.TMVA.Factory("TMVAClassification", fout,
                            ":".join([
                                "V",
                                "!Silent",
                                "Color",
                                "DrawProgressBar",
                                "Transformations=I",
                                "AnalysisType=Classification"]
                                     ))

## Allows us to look at low sig eff points...
(ROOT.TMVA.gConfig().GetVariablePlotting()).fNbinsXOfROCCurve =  200

#factory.AddVariable("NTRJigsawVars.RJVars_SS_MDeltaR/1000.","F")
#factory.AddVariable("NTRJigsawVars.RJVars_MG/1000.","F") 
#factory.AddVariable("NTRJigsawVars.RJVars_SS_Mass/1000." ,"F")
factory.AddVariable("NTRJigsawVars.RJVars_G_0_CosTheta" ,"F")
factory.AddVariable("NTRJigsawVars.RJVars_G_1_CosTheta" ,"F")
factory.AddVariable("NTRJigsawVars.RJVars_G_0_PInvHS" ,"F")
factory.AddVariable("NTRJigsawVars.RJVars_G_1_PInvHS" ,"F")
factory.AddVariable("NTRJigsawVars.RJVars_G_0_Jet2_pT/1000." ,"F")
factory.AddVariable("NTRJigsawVars.RJVars_G_1_Jet2_pT/1000." ,"F")
factory.AddVariable("abs(NTRJigsawVars.RJVars_SS_CosTheta)" ,"F")
factory.AddVariable("abs(NTRJigsawVars.RJVars_DeltaBetaGG)" ,"F")
factory.AddVariable("NTRJigsawVars.RJVars_QCD_Rpt" ,"F")
factory.AddVariable("NTRJigsawVars.RJVars_QCD_Delta1*NTRJigsawVars.RJVars_QCD_Rpsib" ,"F")

factory.AddVariable("NTRJigsawVars.RJVars_C_0_CosTheta" ,"F")
factory.AddVariable("NTRJigsawVars.RJVars_C_1_CosTheta" ,"F")
factory.AddVariable("cos(NTRJigsawVars.RJVars_G_0_dPhiGC)" ,"F")
factory.AddVariable("cos(NTRJigsawVars.RJVars_G_1_dPhiGC)" ,"F")
factory.AddVariable("NTRJigsawVars.RJVars_G_0_Jet1_pT/1000." ,"F")
factory.AddVariable("NTRJigsawVars.RJVars_G_1_Jet1_pT/1000." ,"F")
factory.AddVariable("NTRJigsawVars.RJVars_dphiVG" ,"F")
factory.AddVariable("NTRJigsawVars.RJVars_V1_N" ,"I")
factory.AddVariable("NTRJigsawVars.RJVars_I1_Depth" ,"I")


for mysamplehandler in [	
							sh_signal,
							sh_bg["qcd"],
							sh_bg["top"],
							sh_bg["wjets"],
							sh_bg["zjets"] 
						]:



	for sample in mysamplehandler:
		m_nevt = 0
		m_sumw = 0
		for ifile in xrange(sample.numFiles() ):
			myfile = ROOT.TFile(sample.fileName(ifile))
			try:
				m_nevt += myfile.Get("Counter_JobBookeeping_JobBookeeping").GetBinContent(1)
				m_sumw += myfile.Get("Counter_JobBookeeping_JobBookeeping").GetBinContent(2)
			except:
				pass
		sample.setMetaDouble("nc_nevt",m_nevt)
		sample.setMetaDouble("nc_sumw",m_sumw)

	if mysamplehandler==sh_signal:
		for sample in mysamplehandler:
			#################################################################################
			## This is hard-coding what signal to optimize against... #######################
			#################################################################################
			if not("_1200_600" in sample.getMetaString("short_name") ):
				continue
			tempxs = sample.getMetaDouble("nc_xs") * sample.getMetaDouble("kfactor") * sample.getMetaDouble("filter_efficiency")
			if sample.getMetaDouble("nc_sumw"):
				factory.AddSignalTree( sample.makeTChain().Clone("signal") , lumi*tempxs / sample.getMetaDouble("nc_sumw")  )

	else:
		for sample in mysamplehandler:
			## Just killing these low JX samples - should be ~kosher for now.
			if "JZ0W" in sample.getMetaString("short_name") or "JZ1W" in sample.getMetaString("short_name"):
				continue
			tempxs = sample.getMetaDouble("nc_xs") * sample.getMetaDouble("kfactor") * sample.getMetaDouble("filter_efficiency")
			if sample.getMetaDouble("nc_sumw"):
				factory.AddBackgroundTree( sample.makeTChain().Clone(sample.getMetaString("short_name") ) , lumi*tempxs / sample.getMetaDouble("nc_sumw")  )


factory.SetBackgroundWeightExpression( "NTVars.eventWeight" );
factory.SetSignalWeightExpression( "NTVars.eventWeight" );

preselection = ROOT.TCut("NTRJigsawVars.RJVars_SS_MDeltaR/1000.>300&&met>100.&&NTRJigsawVars.RJVars_G_0_Jet2_pT/1000.>100.&&NTRJigsawVars.RJVars_G_1_Jet2_pT/1000.>100.")
factory.PrepareTrainingAndTestTree( preselection, preselection ,
									"V:SplitMode=Random:NormMode=NumEvents" )




options = "!H:V:FitMethod=GA:EffSel"
# options = "!H:V:FitMethod=SA:EffSel"
# options += ":VarProp=FSmart"
# options += ":VarProp[3]=NotEnforced"
# options += ":VarProp[4]=NotEnforced"
# options += ":VarProp[12]=NotEnforced"
# options += ":VarProp[13]=NotEnforced"

method = factory.BookMethod(ROOT.TMVA.Types.kCuts, "kCuts", options)

#method.OptimizeTuningParameters("SigEffAtBkgEff001")

factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
