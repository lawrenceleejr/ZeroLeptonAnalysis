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
factory.AddVariable("NTRJigsawVars.RJVars_MG/1000.","F") 
#factory.AddVariable("NTRJigsawVars.RJVars_MG*NTRJigsawVars.RJVars_P_0_MassRatioGC/1000.","F") 
#factory.AddVariable("NTRJigsawVars.RJVars_MG*NTRJigsawVars.RJVars_P_1_MassRatioGC/1000.","F") 
#factory.AddVariable("NTRJigsawVars.RJVars_P_0_MassRatioGC/1000.","F") 
#factory.AddVariable("NTRJigsawVars.RJVars_P_1_MassRatioGC/1000.","F") 

#factory.AddVariable("NTRJigsawVars.RJVars_P_0_Jet2_pT/1000." ,"F")
#factory.AddVariable("NTRJigsawVars.RJVars_P_1_Jet2_pT/1000." ,"F")

#factory.AddVariable("NTRJigsawVars.RJVars_PP_Mass/1000." ,"F")

#factory.AddVariable("NTRJigsawVars.RJVars_P_0_CosTheta" ,"F")
#factory.AddVariable("NTRJigsawVars.RJVars_P_1_CosTheta" ,"F")
#factory.AddVariable("NTRJigsawVars.RJVars_P_0_PInvHS" ,"F")
#factory.AddVariable("NTRJigsawVars.RJVars_P_1_PInvHS" ,"F")

#factory.AddVariable("abs(NTRJigsawVars.RJVars_PP_CosTheta)" ,"F")
# # factory.AddVariable("abs(NTRJigsawVars.RJVars_DeltaBetaGG)" ,"F")
# factory.AddVariable("NTRJigsawVars.RJVars_QCD_Rpt" ,"F")
#factory.AddVariable("NTRJigsawVars.RJVars_QCD_Delta1*NTRJigsawVars.RJVars_QCD_Rpsib" ,"F")

#factory.AddVariable("NTRJigsawVars.RJVars_C_0_CosTheta" ,"F")
#factory.AddVariable("NTRJigsawVars.RJVars_C_1_CosTheta" ,"F")
# factory.AddVariable("TMath::Power(cos(NTRJigsawVars.RJVars_P_0_dPhiGC+NTRJigsawVars.RJVars_P_1_dPhiGC),2)" ,"F")
# factory.AddVariable("cos(NTRJigsawVars.RJVars_P_1_dPhiGC)" ,"F")
# factory.AddVariable("NTRJigsawVars.RJVars_P_0_Jet1_pT/1000." ,"F")
# # factory.AddVariable("NTRJigsawVars.RJVars_P_1_Jet1_pT/1000." ,"F")
# factory.AddVariable("NTRJigsawVars.RJVars_dphiVG" ,"F")
# factory.AddVariable("NTRJigsawVars.RJVars_V1_N+NTRJigsawVars.RJVars_V2_N" ,"I")
# # factory.AddVariable("NTRJigsawVars.RJVars_I1_Depth" ,"I")


factory.AddVariable("NTRJigsawVars.RJVars_PP_InvGamma","F")
#factory.AddVariable("NTRJigsawVars.RJVars_PP_InvGamma-NTRJigsawVars.RJVars_PP_VisShape","F")
factory.AddVariable("NTRJigsawVars.RJVars_PP_VisShape","F")

#factory.AddVariable("TMath::Power(TMath::Sin(NTRJigsawVars.RJVars_P_0_dPhiGC/2.+NTRJigsawVars.RJVars_P_1_dPhiGC/2.),2)","F")
#factory.AddVariable("abs(NTRJigsawVars.RJVars_P_0_dPhiGC-NTRJigsawVars.RJVars_P_1_dPhiGC)","F")




f = {}
f["W"]          = ROOT.TFile("/afs/cern.ch/user/l/leejr/work/public/Merged0LNtuples/082715a_40GeVTest/WMassiveCB.root")
f["Z"]          = ROOT.TFile("/afs/cern.ch/user/l/leejr/work/public/Merged0LNtuples/082715a_40GeVTest/ZMassiveCB.root")
f["Top"]        = ROOT.TFile("/afs/cern.ch/user/l/leejr/work/public/Merged0LNtuples/082715a_40GeVTest/Top.root")
f["Diboson"]    = ROOT.TFile("/afs/cern.ch/user/l/leejr/work/public/Merged0LNtuples/082715a_40GeVTest/DibosonMassiveCB.root")
f["signal"]     = ROOT.TFile("/afs/cern.ch/user/l/leejr/work/public/Merged0LNtuples/082715a_40GeVTest/GG_direct.root")

#factory.AddSignalTree( f["signal"].Get("GG_direct_1100_700_SRAll") )
factory.AddSignalTree( f["signal"].Get("GG_direct_1000_600_SRAll") )
#factory.AddSignalTree( f["signal"].Get("GG_direct_1250_750_SRAll") )
#factory.AddSignalTree( f["signal"].Get("GG_direct_812_787_SRAll") )

factory.AddBackgroundTree( f["W"].Get("W_SRAll") )
factory.AddBackgroundTree( f["Z"].Get("Z_SRAll") )
factory.AddBackgroundTree( f["Top"].Get("Top_SRAll") )
factory.AddBackgroundTree( f["Diboson"].Get("Diboson_SRAll") )


factory.SetBackgroundWeightExpression( "NTVars.eventWeight*NTVars.normWeight" );
factory.SetSignalWeightExpression( "NTVars.eventWeight*NTVars.normWeight/2." );########################### BOOKKEPPERS BUG: HAS FACTOR OF TWO DIVIDED OUT!!!!!!!!!!!!!!!!!!!!!
# factory.SetBackgroundWeightExpression( "1" );
# factory.SetSignalWeightExpression( "1" );

preselection = "NTRJigsawVars.RJVars_SS_MDeltaR/1000.>300&&met>100.&&NTRJigsawVars.RJVars_P_0_Jet1_pT/1000.>100.&&NTRJigsawVars.RJVars_P_1_Jet1_pT/1000.>100.&&NTRJigsawVars.RJVars_MG/1000.>300"
preselection += "&&NTRJigsawVars.RJVars_P_0_MassRatioGC>0&&NTRJigsawVars.RJVars_P_1_MassRatioGC>0"
#preselection += "&&NTRJigsawVars.RJVars_P_0_PInvHS>0.1&&NTRJigsawVars.RJVars_P_1_PInvHS>0.1"
#preselection += "&&NTRJigsawVars.RJVars_P_0_CosTheta<0.7&&NTRJigsawVars.RJVars_P_1_CosTheta<0.7"
preselection += "&&NTRJigsawVars.RJVars_QCD_Rpt<0.2"
# preselection = "met>100.&&NTRJigsawVars.RJVars_P_0_Jet1_pT/1000.>100.&&NTRJigsawVars.RJVars_P_1_Jet1_pT/1000.>100."
factory.PrepareTrainingAndTestTree( ROOT.TCut(preselection), ROOT.TCut(preselection) ,
									"V:SplitMode=Random:NormMode=None" )




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
