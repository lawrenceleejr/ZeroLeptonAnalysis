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


#                                "Transformations=I",

## Allows us to look at low sig eff points...
(ROOT.TMVA.gConfig().GetVariablePlotting()).fNbinsXOfROCCurve =  200

########################################
# factory.AddVariable("Alt$(jetPt[3],0)","F")
# factory.AddVariable("Ap","F")
# # factory.AddVariable("NTVars.nJet","I")
# factory.AddVariable("NTVars.meffInc","F")
# factory.AddVariable("NTVars.met/sqrt(jetPt[0]+jetPt[1]+Alt$(jetPt[2],0)+Alt$(jetPt[3],0))","F")



#######################################
#factory.AddVariable("NTRJigsawVars.RJVars_PP_MDeltaR","F")
# factory.AddVariable("NTRJigsawVars.RJVars_MG/1000.","F")
factory.AddVariable("R_H2PP_H6PP","F")
factory.AddVariable("R_HT5PP_H5PP","F")
factory.AddVariable("minR_pTj2i_HT3PPi","F")
factory.AddVariable("maxR_H1PPi_H2PPi","F")
factory.AddVariable("RPZ_HT5PP","F")
factory.AddVariable("HT5PP","F")
factory.AddVariable("H2PP","F")


f = {}
f["W"]          = ROOT.TFile("/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v51_Oct17_pT50/BKG/Wjets.root")
f["Z"]          = ROOT.TFile("/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v51_Oct17_pT50/BKG/Zjets.root")
f["Top"]        = ROOT.TFile("/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v51_Oct17_pT50/BKG/Top.root")
f["Diboson"]    = ROOT.TFile("/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v51_Oct17_pT50/BKG/Diboson.root")
f["signal"]     = ROOT.TFile("/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v51_SIG_pT50/GG_direct.root")

factory.AddSignalTree( f["signal"].Get("GG_direct_1600_0_SRAll") )
#factory.AddSignalTree( f["signal"].Get("GG_direct_1100_700_SRAll") )
# factory.AddSignalTree( f["signal"].Get("GG_direct_1000_600_SRAll") )
#factory.AddSignalTree( f["signal"].Get("GG_direct_1250_750_SRAll") )
#factory.AddSignalTree( f["signal"].Get("GG_direct_812_787_SRAll") )

factory.AddBackgroundTree( f["W"].Get("W_SRAll") )
factory.AddBackgroundTree( f["Z"].Get("Z_SRAll") )
factory.AddBackgroundTree( f["Top"].Get("Top_SRAll") )
factory.AddBackgroundTree( f["Diboson"].Get("Diboson_SRAll") )


factory.SetBackgroundWeightExpression( "weight" );
# factory.SetSignalWeightExpression( "NTVars.eventWeight*NTVars.normWeight/2." );########################### BOOKKEPPERS BUG: HAS FACTOR OF TWO DIVIDED OUT!!!!!!!!!!!!!!!!!!!!!
# factory.SetBackgroundWeightExpression( "1" );
# factory.SetSignalWeightExpression( "1" );

# preselection = "NTRJigsawVars.RJVars_SS_MDeltaR/1000.>300&&met>100.&&NTRJigsawVars.RJVars_P_0_Jet1_pT/1000.>100.&&NTRJigsawVars.RJVars_P_1_Jet1_pT/1000.>100.&&NTRJigsawVars.RJVars_MG/1000.>300"
# preselection += "&&NTRJigsawVars.RJVars_P_0_MassRatioGC>0&&NTRJigsawVars.RJVars_P_1_MassRatioGC>0"
# #preselection += "&&NTRJigsawVars.RJVars_P_0_PInvHS>0.1&&NTRJigsawVars.RJVars_P_1_PInvHS>0.1"
# #preselection += "&&NTRJigsawVars.RJVars_P_0_CosTheta<0.7&&NTRJigsawVars.RJVars_P_1_CosTheta<0.7"
# preselection += "&&NTRJigsawVars.RJVars_QCD_Rpt<0.2"
preselection = "( ( deltaQCD > 0) && (RPT < 0.4)  && (MDR>300) && (NJet>3) )"
# preselection = "met>100.&&NTRJigsawVars.RJVars_P_0_Jet1_pT/1000.>100.&&NTRJigsawVars.RJVars_P_1_Jet1_pT/1000.>100."
factory.PrepareTrainingAndTestTree( ROOT.TCut(preselection), ROOT.TCut(preselection) ,
									"V:SplitMode=Random:NormMode=EqualNumEvents" )



options = "!H:V:FitMethod=GA:EffSel"
# options = "!H:V:FitMethod=SA:EffSel"
# options += ":VarProp=FSmart"
# options += ":VarProp[3]=NotEnforced"
# options += ":VarProp[4]=NotEnforced"
# options += ":VarProp[12]=NotEnforced"
# options += ":VarProp[13]=NotEnforced"

method = factory.BookMethod(ROOT.TMVA.Types.kCuts, "kCuts", options)

factory.BookMethod( ROOT.TMVA.Types.kFisher, "Fisher", "H:!V:Fisher:VarTransform=None:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=50:NsmoothMVAPdf=10" )
# factory.BookMethod( ROOT.TMVA.Types.kMLP, "MLP",    "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:!UseRegulator" );


#method.OptimizeTuningParameters("SigEffAtBkgEff001")

factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()




