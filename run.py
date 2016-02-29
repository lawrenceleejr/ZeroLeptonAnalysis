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

directory = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v51_Nov07_nosys_pT50/"
# datadirectory = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v53_Data_pT50/"
signaldirectory = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v51_SIG_nosys_pT50/"
# signaldirectory = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v53_Anum_pT50/"

# directory = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v53_Anum_pT50/"
# signaldirectory = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v53_Anum_pT50/"

#directory = "/mnt/shared/leejr/Work/WorkshopNtuples/"
#signaldirectory = directory


my_SHs = {}
for sampleHandlerName in [
							#"QCD",
							"W",
							"Z",
							"Top",
							"Diboson",
							]:

	my_SHs[sampleHandlerName] = ROOT.SH.SampleHandler(); 
	ROOT.SH.ScanDir().sampleDepth(0).samplePattern("%s*"%sampleHandlerName).scan(my_SHs[sampleHandlerName], directory+"/BKG/")

	my_SHs[sampleHandlerName].setMetaString("nc_tree", "%s_SRAll"%sampleHandlerName)
	pass



commonPlots  = {
# "H5PP" : [50, 0, 10000],      
"MET"  : [100, 0, 10000],     
"Meff" : [100, 0, 10000],      
}


commonPlots2D  = {
("MET","Meff") : ([50, 0, 3000] , [50, 0, 3000]   ),      
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
		if "SRAll" in treeName:
			print treeName
			my_SHs[treeName] = ROOT.SH.SampleHandler(); 
			ROOT.SH.ScanDir().sampleDepth(0).samplePattern("%s.root"%sampleHandlerName).scan(my_SHs[treeName], signaldirectory)
			my_SHs[treeName].setMetaString("nc_tree", "%s"%treeName )


baseline = "( pT_jet1 > 50.) * ( pT_jet2 > 50.) * ( MDR > 300.)"
baselineMET = "( pT_jet1 > 50.) * ( pT_jet2 > 50.) * ( MET > 200.)"


cuts = {}
limits = {}


## ZL Team




cuts["SR2jCo"] = []
cuts["SR2jCo"] += ["( MET > 200 )"]
cuts["SR2jCo"] += ["( pT_jet1 > 300 )"]
cuts["SR2jCo"] += ["( pT_jet2 > 50 )"]
cuts["SR2jCo"] += ["( dphi > 0.4 )"]
cuts["SR2jCo"] += ["( MET/sqrt(Meff-MET) > 15 )"]
cuts["SR2jCo"] += ["( Meff > 1600 )"]

limits["SR2jCo"] = []
limits["SR2jCo"] +=  [(50,0,1000)]     #["( MET > 200 )"]
limits["SR2jCo"] +=  [(50,0,1000)]     #["( pT_jet1 > 200 )"]
limits["SR2jCo"] +=  [(50,0,1000)]     #["( pT_jet2 > 100 )"]
limits["SR2jCo"] +=  [(50,0,4)]     #["( dphi > 0.4 )"]
limits["SR2jCo"] +=  [(50,0,50)]     #["( MET/(MET+pT_jet1+pT_jet2+pT_jet3+pT_jet4+pT_jet5) > 0.25 )"]
limits["SR2jCo"] +=  [(50,0,4000)]     #["( Meff > 1600 )"]



cuts["SR2jl"] = []
cuts["SR2jl"] += ["( MET > 200 )"]
cuts["SR2jl"] += ["( pT_jet1 > 200 )"]
cuts["SR2jl"] += ["( pT_jet2 > 200 )"]
cuts["SR2jl"] += ["( dphi > 0.8 )"]
cuts["SR2jl"] += ["( MET/sqrt(Meff-MET) > 15 )"]
cuts["SR2jl"] += ["( Meff > 1200 )"]

limits["SR2jl"] = []
limits["SR2jl"] +=  [(50,0,1000)]     #["( MET > 200 )"]
limits["SR2jl"] +=  [(50,0,1000)]     #["( pT_jet1 > 200 )"]
limits["SR2jl"] +=  [(50,0,1000)]     #["( pT_jet2 > 100 )"]
limits["SR2jl"] +=  [(50,0,4)]     #["( dphi > 0.4 )"]
limits["SR2jl"] +=  [(50,0,50)]     #["( MET/(MET+pT_jet1+pT_jet2+pT_jet3+pT_jet4+pT_jet5) > 0.25 )"]
limits["SR2jl"] +=  [(50,0,4000)]     #["( Meff > 1600 )"]



cuts["SR2jm"] = []
cuts["SR2jm"] += ["( MET > 200 )"]
cuts["SR2jm"] += ["( pT_jet1 > 200 )"]
cuts["SR2jm"] += ["( pT_jet2 > 60 )"]
cuts["SR2jm"] += ["( dphi > 0.4 )"]
cuts["SR2jm"] += ["( MET/sqrt(Meff-MET) > 20 )"]
cuts["SR2jm"] += ["( Meff > 1800 )"]

limits["SR2jm"] = []
limits["SR2jm"] +=  [(50,0,1000)]     #["( MET > 200 )"]
limits["SR2jm"] +=  [(50,0,1000)]     #["( pT_jet1 > 200 )"]
limits["SR2jm"] +=  [(50,0,1000)]     #["( pT_jet2 > 100 )"]
limits["SR2jm"] +=  [(50,0,4)]     #["( dphi > 0.4 )"]
limits["SR2jm"] +=  [(50,0,50)]     #["( MET/(MET+pT_jet1+pT_jet2+pT_jet3+pT_jet4+pT_jet5) > 0.25 )"]
limits["SR2jm"] +=  [(50,0,4000)]     #["( Meff > 1600 )"]



cuts["SR2jt"] = []
cuts["SR2jt"] += ["( MET > 200 )"]
cuts["SR2jt"] += ["( pT_jet1 > 200 )"]
cuts["SR2jt"] += ["( pT_jet2 > 200 )"]
cuts["SR2jt"] += ["( dphi > 0.8 )"]
cuts["SR2jt"] += ["( MET/sqrt(Meff-MET) > 20 )"]
cuts["SR2jt"] += ["( Meff > 2200 )"]

limits["SR2jt"] = []
limits["SR2jt"] +=  [(50,0,1000)]     #["( MET > 200 )"]
limits["SR2jt"] +=  [(50,0,1000)]     #["( pT_jet1 > 200 )"]
limits["SR2jt"] +=  [(50,0,1000)]     #["( pT_jet2 > 100 )"]
limits["SR2jt"] +=  [(50,0,4)]     #["( dphi > 0.4 )"]
limits["SR2jt"] +=  [(50,0,50)]     #["( MET/(MET+pT_jet1+pT_jet2+pT_jet3+pT_jet4+pT_jet5) > 0.25 )"]
limits["SR2jt"] +=  [(50,0,4000)]     #["( Meff > 1600 )"]


cuts["SR4jt"] = []
cuts["SR4jt"] += ["( MET > 200 )"]
cuts["SR4jt"] += ["( pT_jet1 > 200 )"]
cuts["SR4jt"] += ["( pT_jet2 > 100 )"]
cuts["SR4jt"] += ["( pT_jet3 > 100 )"]
cuts["SR4jt"] += ["( pT_jet4 > 100 )"]
cuts["SR4jt"] += ["( dphi > 0.4 )"]
cuts["SR4jt"] += ["( dphiR > 0.2 )"]
cuts["SR4jt"] += ["( Aplan > 0.04 )"]
cuts["SR4jt"] += ["( MET/(MET+pT_jet1+pT_jet2+pT_jet3+pT_jet4) > 0.2 )"]
cuts["SR4jt"] += ["( Meff > 2200 )"]

limits["SR4jt"] = []
limits["SR4jt"] +=  [(50,0,1000)]     #["( MET > 200 )"]
limits["SR4jt"] +=  [(50,0,1000)]     #["( pT_jet1 > 200 )"]
limits["SR4jt"] +=  [(50,0,1000)]     #["( pT_jet2 > 100 )"]
limits["SR4jt"] +=  [(50,0,1000)]     #["( pT_jet3 > 100 )"]
limits["SR4jt"] +=  [(50,0,1000)]     #["( pT_jet4 > 100 )"]
limits["SR4jt"] +=  [(50,0,4)]     #["( dphi > 0.4 )"]
limits["SR4jt"] +=  [(50,0,4)]     #["( dphiR > 0.2 )"]
limits["SR4jt"] +=  [(50,0,0.5)]     #["( Aplan > 0.04 )"]
limits["SR4jt"] +=  [(50,0,1)]     #["( MET/(MET+pT_jet1+pT_jet2+pT_jet3+pT_jet4+pT_jet5) > 0.25 )"]
limits["SR4jt"] +=  [(50,0,4000)]     #["( Meff > 1600 )"]


cuts["SR5j"] = []
cuts["SR5j"] += ["( MET > 200 )"]
cuts["SR5j"] += ["( pT_jet1 > 200 )"]
cuts["SR5j"] += ["( pT_jet2 > 100 )"]
cuts["SR5j"] += ["( pT_jet3 > 100 )"]
cuts["SR5j"] += ["( pT_jet4 > 100 )"]
cuts["SR5j"] += ["( pT_jet5 > 60 )"]
cuts["SR5j"] += ["( dphi > 0.4 )"]
cuts["SR5j"] += ["( dphiR > 0.2 )"]
cuts["SR5j"] += ["( Aplan > 0.04 )"]
cuts["SR5j"] += ["( MET/(MET+pT_jet1+pT_jet2+pT_jet3+pT_jet4+pT_jet5) > 0.25 )"]
cuts["SR5j"] += ["( Meff > 1600 )"]

limits["SR5j"] = []
limits["SR5j"] +=  [(50,0,1000)]     #["( MET > 200 )"]
limits["SR5j"] +=  [(50,0,1000)]     #["( pT_jet1 > 200 )"]
limits["SR5j"] +=  [(50,0,1000)]     #["( pT_jet2 > 100 )"]
limits["SR5j"] +=  [(50,0,1000)]     #["( pT_jet3 > 100 )"]
limits["SR5j"] +=  [(50,0,1000)]     #["( pT_jet4 > 100 )"]
limits["SR5j"] +=  [(50,0,1000)]     #["( pT_jet5 > 50 )"]
limits["SR5j"] +=  [(50,0,4)]     #["( dphi > 0.4 )"]
limits["SR5j"] +=  [(50,0,4)]     #["( dphiR > 0.2 )"]
limits["SR5j"] +=  [(50,0,0.5)]     #["( Aplan > 0.04 )"]
limits["SR5j"] +=  [(50,0,1)]     #["( MET/(MET+pT_jet1+pT_jet2+pT_jet3+pT_jet4+pT_jet5) > 0.25 )"]
limits["SR5j"] +=  [(50,0,4000)]     #["( Meff > 1600 )"]


cuts["SR6jm"] = []
cuts["SR6jm"] += ["( MET > 200 )"]
cuts["SR6jm"] += ["( pT_jet1 > 200 )"]
cuts["SR6jm"] += ["( pT_jet2 > 100 )"]
cuts["SR6jm"] += ["( pT_jet3 > 100 )"]
cuts["SR6jm"] += ["( pT_jet4 > 100 )"]
cuts["SR6jm"] += ["( pT_jet5 > 60 )"]
cuts["SR6jm"] += ["( pT_jet6 > 60 )"]
cuts["SR6jm"] += ["( dphi > 0.4 )"]
cuts["SR6jm"] += ["( dphiR > 0.2 )"]
cuts["SR6jm"] += ["( Aplan > 0.04 )"]
cuts["SR6jm"] += ["( MET/(MET+pT_jet1+pT_jet2+pT_jet3+pT_jet4+pT_jet5+pT_jet6) > 0.25 )"]
cuts["SR6jm"] += ["( Meff > 1600 )"]

limits["SR6jm"] = []
limits["SR6jm"] +=  [(50,0,1000)]     #["( MET > 200 )"]
limits["SR6jm"] +=  [(50,0,1000)]     #["( pT_jet1 > 200 )"]
limits["SR6jm"] +=  [(50,0,1000)]     #["( pT_jet2 > 100 )"]
limits["SR6jm"] +=  [(50,0,1000)]     #["( pT_jet3 > 100 )"]
limits["SR6jm"] +=  [(50,0,1000)]     #["( pT_jet4 > 100 )"]
limits["SR6jm"] +=  [(50,0,1000)]     #["( pT_jet5 > 50 )"]
limits["SR6jm"] +=  [(50,0,1000)]     #["( pT_jet5 > 50 )"]
limits["SR6jm"] +=  [(50,0,4)]     #["( dphi > 0.4 )"]
limits["SR6jm"] +=  [(50,0,4)]     #["( dphiR > 0.2 )"]
limits["SR6jm"] +=  [(50,0,0.5)]     #["( Aplan > 0.04 )"]
limits["SR6jm"] +=  [(50,0,1)]     #["( MET/(MET+pT_jet1+pT_jet2+pT_jet3+pT_jet4+pT_jet5) > 0.25 )"]
limits["SR6jm"] +=  [(50,0,4000)]     #["( Meff > 1600 )"]



cuts["SR6jt"] = []
cuts["SR6jt"] += ["( MET > 200 )"]
cuts["SR6jt"] += ["( pT_jet1 > 200 )"]
cuts["SR6jt"] += ["( pT_jet2 > 100 )"]
cuts["SR6jt"] += ["( pT_jet3 > 100 )"]
cuts["SR6jt"] += ["( pT_jet4 > 100 )"]
cuts["SR6jt"] += ["( pT_jet5 > 60 )"]
cuts["SR6jt"] += ["( pT_jet6 > 60 )"]
cuts["SR6jt"] += ["( dphi > 0.4 )"]
cuts["SR6jt"] += ["( dphiR > 0.2 )"]
cuts["SR6jt"] += ["( Aplan > 0.04 )"]
cuts["SR6jt"] += ["( MET/(MET+pT_jet1+pT_jet2+pT_jet3+pT_jet4+pT_jet5+pT_jet6) > 0.2 )"]
cuts["SR6jt"] += ["( Meff > 2000 )"]

limits["SR6jt"] = []
limits["SR6jt"] +=  [(50,0,1000)]     #["( MET > 200 )"]
limits["SR6jt"] +=  [(50,0,1000)]     #["( pT_jet1 > 200 )"]
limits["SR6jt"] +=  [(50,0,1000)]     #["( pT_jet2 > 100 )"]
limits["SR6jt"] +=  [(50,0,1000)]     #["( pT_jet3 > 100 )"]
limits["SR6jt"] +=  [(50,0,1000)]     #["( pT_jet4 > 100 )"]
limits["SR6jt"] +=  [(50,0,1000)]     #["( pT_jet5 > 50 )"]
limits["SR6jt"] +=  [(50,0,1000)]     #["( pT_jet5 > 50 )"]
limits["SR6jt"] +=  [(50,0,4)]     #["( dphi > 0.4 )"]
limits["SR6jt"] +=  [(50,0,4)]     #["( dphiR > 0.2 )"]
limits["SR6jt"] +=  [(50,0,0.5)]     #["( Aplan > 0.04 )"]
limits["SR6jt"] +=  [(50,0,1)]     #["( MET/(MET+pT_jet1+pT_jet2+pT_jet3+pT_jet4+pT_jet5) > 0.25 )"]
limits["SR6jt"] +=  [(50,0,4000)]     #["( Meff > 1600 )"]





#############################################################
## Squark RJR



cuts["SR1Sq"] = []
cuts["SR1Sq"] += ["( deltaQCD > 0)"]
cuts["SR1Sq"] += ["( RPT_HT3PP < 0.08  )"]
cuts["SR1Sq"] += ["( R_H2PP_H3PP > 0.6)"]
cuts["SR1Sq"] += ["( R_H2PP_H3PP < 0.95)"]
cuts["SR1Sq"] += ["( RPZ_HT3PP < 0.55)"]
cuts["SR1Sq"] += ["( pT_jet2 / HT3PP > 0.16)"]
cuts["SR1Sq"] += ["( abs(cosP) < 0.65)"]

limits["SR1Sq"] = []
limits["SR1Sq"] += [(50,-1,1)]#["( deltaQCD > 0)"]
limits["SR1Sq"] += [(50,0,1)]#["( RPT_HT5PP < 0.08  )"]
limits["SR1Sq"] += [(50,0,1)]#["( R_H2PP_H5PP > 0.35)"]
limits["SR1Sq"] += [(50,0,1)]#["( R_H2PP_H5PP > 0.35)"]
limits["SR1Sq"] += [(50,0,1)]#["( RPZ_HT5PP < 0.5)"]
limits["SR1Sq"] += [(50,0,0.5)]#["( RPZ_HT5PP < 0.5)"]
limits["SR1Sq"] += [(50,0,1)]#["( cosP
limits["SR1Sq"] += [(50,0,4000)]#["( HT5PP > 800)"]
limits["SR1Sq"] += [(50,0,2000)]#["( H2PP > 550)"]

cuts["SR1ASq"] = deepcopy(cuts["SR1Sq"])
cuts["SR1ASq"] += ["( HT3PP > 1100)"]
cuts["SR1ASq"] += ["( H2PP > 900)"]
limits["SR1ASq"] = deepcopy(limits["SR1Sq"])

cuts["SR1BSq"] = deepcopy(cuts["SR1Sq"])
cuts["SR1BSq"] += ["( HT3PP > 1200)"]
cuts["SR1BSq"] += ["( H2PP > 1000)"]
limits["SR1BSq"] = deepcopy(limits["SR1Sq"])



cuts["SR2Sq"] = []
cuts["SR2Sq"] += ["( deltaQCD > 0)"]
cuts["SR2Sq"] += ["( RPT_HT3PP < 0.08  )"]
cuts["SR2Sq"] += ["( R_H2PP_H3PP > 0.55)"]
cuts["SR2Sq"] += ["( R_H2PP_H3PP < 0.96)"]
cuts["SR2Sq"] += ["( RPZ_HT3PP < 0.6)"]
cuts["SR2Sq"] += ["( pT_jet2 / HT3PP > 0.15)"]
cuts["SR2Sq"] += ["( abs(cosP) < 0.7)"]

limits["SR2Sq"] = []
limits["SR2Sq"] += [(50,-1,1)]#["( deltaQCD > 0)"]
limits["SR2Sq"] += [(50,0,1)]#["( RPT_HT5PP < 0.08  )"]
limits["SR2Sq"] += [(50,0,1)]#["( R_H2PP_H5PP > 0.35)"]
limits["SR2Sq"] += [(50,0,1)]#["( R_H2PP_H5PP > 0.35)"]
limits["SR2Sq"] += [(50,0,1)]#["( RPZ_HT5PP < 0.5)"]
limits["SR2Sq"] += [(50,0,0.5)]#["( RPZ_HT5PP < 0.5)"]
limits["SR2Sq"] += [(50,0,1)]#["( cosP
limits["SR2Sq"] += [(50,0,4000)]#["( HT5PP > 800)"]
limits["SR2Sq"] += [(50,0,2000)]#["( H2PP > 550)"]

cuts["SR2ASq"] = deepcopy(cuts["SR2Sq"])
cuts["SR2ASq"] += ["( HT3PP > 1300)"]
cuts["SR2ASq"] += ["( H2PP > 1100)"]
limits["SR2ASq"] = deepcopy(limits["SR2Sq"])

cuts["SR2BSq"] = deepcopy(cuts["SR2Sq"])
cuts["SR2BSq"] += ["( HT3PP > 1450)"]
cuts["SR2BSq"] += ["( H2PP > 1200)"]
limits["SR2BSq"] = deepcopy(limits["SR2Sq"])


cuts["SR3Sq"] = []
cuts["SR3Sq"] += ["( deltaQCD > 0)"]
cuts["SR3Sq"] += ["( RPT_HT3PP < 0.08  )"]
cuts["SR3Sq"] += ["( R_H2PP_H3PP > 0.5)"]
cuts["SR3Sq"] += ["( R_H2PP_H3PP < 0.98)"]
cuts["SR3Sq"] += ["( RPZ_HT3PP < 0.63)"]
cuts["SR3Sq"] += ["( pT_jet2 / HT3PP > 0.13)"]
cuts["SR3Sq"] += ["( abs(cosP) < 0.8)"]


limits["SR3Sq"] = []
limits["SR3Sq"] += [(50,-1,1)]#["( deltaQCD > 0)"]
limits["SR3Sq"] += [(50,0,1)]#["( RPT_HT5PP < 0.08  )"]
limits["SR3Sq"] += [(50,0,1)]#["( R_H2PP_H5PP > 0.35)"]
limits["SR3Sq"] += [(50,0,1)]#["( R_H2PP_H5PP > 0.35)"]
limits["SR3Sq"] += [(50,0,1)]#["( RPZ_HT5PP < 0.5)"]
limits["SR3Sq"] += [(50,0,0.5)]#["( RPZ_HT5PP < 0.5)"]
limits["SR3Sq"] += [(50,0,1)]#["( cosP
limits["SR3Sq"] += [(50,0,4000)]#["( HT5PP > 800)"]
limits["SR3Sq"] += [(50,0,2000)]#["( H2PP > 550)"]

cuts["SR3ASq"] = deepcopy(cuts["SR3Sq"])
cuts["SR3ASq"] += ["( HT3PP > 1600)"]
cuts["SR3ASq"] += ["( H2PP > 1350)"]
limits["SR3ASq"] = deepcopy(limits["SR3Sq"])

cuts["SR3BSq"] = deepcopy(cuts["SR3Sq"])
cuts["SR3BSq"] += ["( HT3PP > 1800)"]
cuts["SR3BSq"] += ["( H2PP > 1500)"]
limits["SR3BSq"] = deepcopy(limits["SR3Sq"])



##############################################################
#Gluino RJR

cuts["SR1"] = []
cuts["SR1"] += ["( deltaQCD > 0)"]
cuts["SR1"] += ["( RPT_HT5PP < 0.08  )"]
cuts["SR1"] += ["( R_H2PP_H5PP > 0.35)"]
cuts["SR1"] += ["( R_HT5PP_H5PP > 0.8)"]
cuts["SR1"] += ["( RPZ_HT5PP < 0.5)"]
cuts["SR1"] += ["( minR_pTj2i_HT3PPi > 0.125)"]
cuts["SR1"] += ["( maxR_H1PPi_H2PPi < 0.95)"]
cuts["SR1"] += ["( dangle < 0.5 )"]


limits["SR1"] = []
limits["SR1"] += [(50,-1,1)]#["( deltaQCD > 0)"]
limits["SR1"] += [(50,0,1)]#["( RPT_HT5PP < 0.08  )"]
limits["SR1"] += [(50,0,1)]#["( R_H2PP_H5PP > 0.35)"]
limits["SR1"] += [(50,0,1)]#["( R_HT5PP_H5PP > 0.8)"]
limits["SR1"] += [(50,0,1)]#["( RPZ_HT5PP < 0.5)"]
limits["SR1"] += [(50,0,0.5)]#["( minR_pTj2i_HT3PPi > 0.125)"]
limits["SR1"] += [(50,0.5,1)]#["( maxR_H1PPi_H2PPi < 0.95)"]
limits["SR1"] += [(50,-1,1)]#["( dangle < 0.5 )"]
limits["SR1"] += [(50,0,4000)]#["( HT5PP > 800)"]
limits["SR1"] += [(50,0,2000)]#["( H2PP > 550)"]

cuts["SR1A"] = deepcopy(cuts["SR1"])
cuts["SR1A"] += ["( HT5PP > 800)"]
cuts["SR1A"] += ["( H2PP > 550)"]
limits["SR1A"] = deepcopy(limits["SR1"])


cuts["SR1B"] = deepcopy(cuts["SR1"])
cuts["SR1B"] += ["( HT5PP > 1000)"]
cuts["SR1B"] += ["( H2PP > 550)"]
limits["SR1B"] = deepcopy(limits["SR1"])

cuts["SR1C"] = deepcopy(cuts["SR1"])
cuts["SR1C"] += ["( HT5PP > 1200)"]
cuts["SR1C"] += ["( H2PP > 550)"]
limits["SR1C"] = deepcopy(limits["SR1"])



cuts["SR2"] = []
cuts["SR2"] += ["( deltaQCD > 0)"]
cuts["SR2"] += ["( RPT_HT5PP < 0.08  )"]
cuts["SR2"] += ["( R_H2PP_H5PP > 0.25)"]
cuts["SR2"] += ["( R_HT5PP_H5PP > 0.75)"]
cuts["SR2"] += ["( RPZ_HT5PP < 0.55)"]
cuts["SR2"] += ["( minR_pTj2i_HT3PPi > 0.11)"]
cuts["SR2"] += ["( maxR_H1PPi_H2PPi < 0.97)"]

limits["SR2"] = []
limits["SR2"] += [(50,-1,1)]#["( deltaQCD > 0)"]
limits["SR2"] += [(50,0,1)]#["( RPT_HT5PP < 0.08  )"]
limits["SR2"] += [(50,0,1)]#["( R_H2PP_H5PP > 0.35)"]
limits["SR2"] += [(50,0,1)]#["( R_HT5PP_H5PP > 0.8)"]
limits["SR2"] += [(50,0,1)]#["( RPZ_HT5PP < 0.5)"]
limits["SR2"] += [(50,0,0.5)]#["( minR_pTj2i_HT3PPi > 0.125)"]
limits["SR2"] += [(50,0.5,1)]#["( maxR_H1PPi_H2PPi < 0.95)"]
limits["SR2"] += [(50,0,4000)]#["( HT5PP > 800)"]
limits["SR2"] += [(50,0,2000)]#["( H2PP > 550)"]


cuts["SR2A"] = deepcopy(cuts["SR2"])
cuts["SR2A"] += ["( HT5PP > 1400)"]
cuts["SR2A"] += ["( H2PP > 750)"]
limits["SR2A"] = deepcopy(limits["SR2"])

cuts["SR2B"] = deepcopy(cuts["SR2"])
cuts["SR2B"] += ["( HT5PP > 1600)"]
cuts["SR2B"] += ["( H2PP > 750)"]
limits["SR2B"] = deepcopy(limits["SR2"])


cuts["SR2C"] = deepcopy(cuts["SR2"])
cuts["SR2C"] += ["( HT5PP > 1800)"]
cuts["SR2C"] += ["( H2PP > 750)"]
limits["SR2C"] = deepcopy(limits["SR2"])


cuts["SR2D"] = deepcopy(cuts["SR2"])
cuts["SR2D"] += ["( HT5PP > 2000)"]
cuts["SR2D"] += ["( H2PP > 850)"]
limits["SR2D"] = deepcopy(limits["SR2"])


cuts["SR3"] = []
cuts["SR3"] += ["( deltaQCD > 0)"]
cuts["SR3"] += ["( RPT_HT5PP < 0.08  )"]
cuts["SR3"] += ["( R_H2PP_H5PP > 0.2)"]
cuts["SR3"] += ["( R_HT5PP_H5PP > 0.65)"]
cuts["SR3"] += ["( RPZ_HT5PP < 0.6)"]
cuts["SR3"] += ["( minR_pTj2i_HT3PPi > 0.09)"]
cuts["SR3"] += ["( maxR_H1PPi_H2PPi < 0.98)"]


limits["SR3"] = []
limits["SR3"] += [(50,-1,1)]#["( deltaQCD > 0)"]
limits["SR3"] += [(50,0,1)]#["( RPT_HT5PP < 0.08  )"]
limits["SR3"] += [(50,0,1)]#["( R_H2PP_H5PP > 0.35)"]
limits["SR3"] += [(50,0,1)]#["( R_HT5PP_H5PP > 0.8)"]
limits["SR3"] += [(50,0,1)]#["( RPZ_HT5PP < 0.5)"]
limits["SR3"] += [(50,0,0.5)]#["( minR_pTj2i_HT3PPi > 0.125)"]
limits["SR3"] += [(50,0.5,1)]#["( maxR_H1PPi_H2PPi < 0.95)"]
limits["SR3"] += [(50,0,4000)]#["( HT5PP > 800)"]
limits["SR3"] += [(50,0,2000)]#["( H2PP > 550)"]

cuts["SR3A"] = deepcopy(cuts["SR3"])
cuts["SR3A"] += ["( HT5PP > 2000)"]
cuts["SR3A"] += ["( H2PP > 850)"]
limits["SR3A"] = deepcopy(limits["SR3"])


cuts["SR3B"] = deepcopy(cuts["SR3"])
cuts["SR3B"] += ["( HT5PP > 2250)"]
cuts["SR3B"] += ["( H2PP > 850)"]
limits["SR3B"] = deepcopy(limits["SR3"])


cuts["SR3C"] = deepcopy(cuts["SR3"])
cuts["SR3C"] += ["( HT5PP > 2500)"]
cuts["SR3C"] += ["( H2PP > 850)"]
limits["SR3C"] = deepcopy(limits["SR3"])




## Compressed stuff: ##########################

cuts["SR1Co"] = []
cuts["SR1Co"] += ["( RPT_HT1CM < 0.15  )"]
cuts["SR1Co"] += ["( PIoHT1CM > 0.9 )"]
cuts["SR1Co"] += ["( cosS > 0.8 )"]

limits["SR1Co"] = []
limits["SR1Co"] += [(50,0,1)]#["( RPT_HT5PP < 0.08  )"]
limits["SR1Co"] += [(50,0,1)]#["( R_H2PP_H5PP > 0.35)"]
limits["SR1Co"] += [(50,-1,1)]#["( R_HT5PP_H5PP > 0.8)"]
limits["SR1Co"] += [(50,0,2000)]#["( RPZ_HT5PP < 0.5)"]


cuts["SR1ACo"] = deepcopy(cuts["SR1Co"])
cuts["SR1ACo"] += ["( HT1CM > 700)"]
limits["SR1ACo"] = deepcopy(limits["SR1Co"])

cuts["SR1BCo"] = deepcopy(cuts["SR1Co"])
cuts["SR1BCo"] += ["( HT1CM > 900)"]
limits["SR1BCo"] = deepcopy(limits["SR1Co"])



cuts["SR2Co"] = []
cuts["SR2Co"] += ["( RPT_HT1CM < 0.15  )"]
cuts["SR2Co"] += ["( PIoHT1CM > 0.8 )"]
cuts["SR2Co"] += ["( MS > 100 )"]
cuts["SR2Co"] += ["( cosS > 0.8 )"]

limits["SR2Co"] = []
limits["SR2Co"] += [(50,0,1)]#["( RPT_HT5PP < 0.08  )"]
limits["SR2Co"] += [(50,0,1)]#["( R_H2PP_H5PP > 0.35)"]
limits["SR2Co"] += [(50,-1,1)]#["( R_HT5PP_H5PP > 0.8)"]
limits["SR2Co"] += [(50,0,1000)]# MS
limits["SR2Co"] += [(50,0,2000)]#["( RPZ_HT5PP < 0.5)"]


cuts["SR2ACo"] = deepcopy(cuts["SR2Co"])
cuts["SR2ACo"] += ["( HT1CM > 700)"]
limits["SR2ACo"] = deepcopy(limits["SR2Co"])

cuts["SR2BCo"] = deepcopy(cuts["SR2Co"])
cuts["SR2BCo"] += ["( HT1CM > 900)"]
limits["SR2BCo"] = deepcopy(limits["SR2Co"])





cuts["SR3Co"] = []
cuts["SR3Co"] += ["( RPT_HT1CM < 0.15  )"]
cuts["SR3Co"] += ["( PIoHT1CM > 0.7 )"]
cuts["SR3Co"] += ["( MS > 200 )"]
cuts["SR3Co"] += ["( cosS > 0.8 )"]

limits["SR3Co"] = []
limits["SR3Co"] += [(50,0,1)]#["( RPT_HT5PP < 0.08  )"]
limits["SR3Co"] += [(50,0,1)]#["( R_H2PP_H5PP > 0.35)"]
limits["SR3Co"] += [(50,-1,1)]#["( R_HT5PP_H5PP > 0.8)"]
limits["SR3Co"] += [(50,0,1000)]# MS
limits["SR3Co"] += [(50,0,2000)]#["( RPZ_HT5PP < 0.5)"]

cuts["SR3ACo"] = deepcopy(cuts["SR3Co"])
cuts["SR3ACo"] += ["( HT1CM > 700)"]
limits["SR3ACo"] = deepcopy(limits["SR3Co"])

cuts["SR3BCo"] = deepcopy(cuts["SR3Co"])
cuts["SR3BCo"] += ["( HT1CM > 900)"]
limits["SR3BCo"] = deepcopy(limits["SR3Co"])





cuts["SR4Co"] = []
cuts["SR4Co"] += ["( RPT_HT1CM < 0.15  )"]
cuts["SR4Co"] += ["( PIoHT1CM > 0.6 )"]
cuts["SR4Co"] += ["( MS > 400 )"]
cuts["SR4Co"] += ["( cosS > 0.8 )"]

limits["SR4Co"] = []
limits["SR4Co"] += [(50,0,1)]#["( RPT_HT5PP < 0.08  )"]
limits["SR4Co"] += [(50,0,1)]#["( R_H2PP_H5PP > 0.35)"]
limits["SR4Co"] += [(50,-1,1)]#["( R_HT5PP_H5PP > 0.8)"]
limits["SR4Co"] += [(50,0,1000)]# MS
limits["SR4Co"] += [(50,0,2000)]#["( RPZ_HT5PP < 0.5)"]

cuts["SR4ACo"] = deepcopy(cuts["SR4Co"])
cuts["SR4ACo"] += ["( HT1CM > 700)"]
limits["SR4ACo"] = deepcopy(limits["SR4Co"])

cuts["SR4BCo"] = deepcopy(cuts["SR4Co"])
cuts["SR4BCo"] += ["( HT1CM > 900)"]
limits["SR4BCo"] = deepcopy(limits["SR4Co"])




############### QCD #############################

cuts["CR1QCD"] = deepcopy(cuts["SR1A"])
limits["CR1QCD"] = deepcopy(limits["SR1A"])
cuts["CR1QCD"].pop(0)
cuts["CR1QCD"].pop(1)
limits["CR1QCD"].pop(0)
limits["CR1QCD"].pop(1)


cuts["CR2QCD"] = deepcopy(cuts["SR2A"])
limits["CR2QCD"] = deepcopy(limits["SR2A"])
cuts["CR2QCD"].pop(0)
cuts["CR2QCD"].pop(1)
limits["CR2QCD"].pop(0)
limits["CR2QCD"].pop(1)

cuts["CR1SqQCD"] = deepcopy(cuts["SR1ASq"])
limits["CR1SqQCD"] = deepcopy(limits["SR1ASq"])
cuts["CR1SqQCD"].pop(0)
cuts["CR1SqQCD"].pop(1)
limits["CR1SqQCD"].pop(0)
limits["CR1SqQCD"].pop(1)

cuts["CR2SqQCD"] = deepcopy(cuts["SR2ASq"])
limits["CR2SqQCD"] = deepcopy(limits["SR2ASq"])
cuts["CR2SqQCD"].pop(0)
cuts["CR2SqQCD"].pop(1)
limits["CR2SqQCD"].pop(0)
limits["CR2SqQCD"].pop(1)



## Define your cut strings here....
regions = {
	# "no_cut": "(1)",

	"SR2jCo": "*".join( ["(%s)"%mycut for mycut in cuts["SR2jCo"] ]),
	"SR2jl": "*".join( ["(%s)"%mycut for mycut in cuts["SR2jl"] ]),
	"SR2jm": "*".join( ["(%s)"%mycut for mycut in cuts["SR2jm"] ]),
	"SR2jt": "*".join( ["(%s)"%mycut for mycut in cuts["SR2jt"] ]),
	"SR4jt": "*".join( ["(%s)"%mycut for mycut in cuts["SR4jt"] ]),
	"SR5j": "*".join( ["(%s)"%mycut for mycut in cuts["SR5j"] ]),
	"SR6jm": "*".join( ["(%s)"%mycut for mycut in cuts["SR6jm"] ]),
	"SR6jt": "*".join( ["(%s)"%mycut for mycut in cuts["SR6jt"] ]),

	"SR1ASq": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR1ASq"] ]),
	"SR1BSq": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR1BSq"] ]),
	"SR2ASq": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR2ASq"] ]),
	"SR2BSq": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR2BSq"] ]),
	"SR3ASq": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR3ASq"] ]),
	"SR3BSq": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR3BSq"] ]),

	"SR1A": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR1A"] ]),
	"SR1B": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR1B"] ]),
	"SR1C": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR1C"] ]),
	"SR2A": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR2A"] ]),
	"SR2B": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR2B"] ]),
	"SR2C": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR2C"] ]),
	"SR2D": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR2D"] ]),
	"SR3A": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR3A"] ]),
	"SR3B": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR3B"] ]),
	"SR3C": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR3C"] ]),


	"SR1ACo": baselineMET+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR1ACo"] ]),
	"SR1BCo": baselineMET+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR1BCo"] ]),
	"SR2ACo": baselineMET+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR2ACo"] ]),
	"SR2BCo": baselineMET+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR2BCo"] ]),
	"SR3ACo": baselineMET+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR3ACo"] ]),
	"SR3BCo": baselineMET+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR3BCo"] ]),
	"SR4ACo": baselineMET+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR4ACo"] ]),
	"SR4BCo": baselineMET+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR4BCo"] ]),


	"CR1QCD": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["CR1QCD"] ]),
	"CR2QCD": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["CR2QCD"] ]),
	"CR1SqQCD": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["CR1SqQCD"] ]),
	"CR2SqQCD": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["CR2SqQCD"] ]),



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

		if not('QCD' in region):
			for varname,varlimits in commonPlots.items() :
				# print varname
				job.algsAdd(
	            	ROOT.MD.AlgHist(
	            		ROOT.TH1F(varname+"_%s"%region, varname+"_%s"%region, varlimits[0], varlimits[1], varlimits[2]),
						varname,
						"weight*%s"%regions[region]
						)
					)


		# if "QCD" in region:

		for varname,varlimits in commonPlots2D.items():
			# print varname
			job.algsAdd(
            	ROOT.MD.AlgHist(
            		ROOT.TH2F("%s_%s_%s"%(varname[0], varname[1], region), "%s_%s_%s"%(varname[0], varname[1], region), varlimits[0][0], varlimits[0][1], varlimits[0][2], varlimits[1][0], varlimits[1][1], varlimits[1][2]),
					varname[0], varname[1],
					"weight*%s"%regions[region]
					)
				)

	driver = ROOT.EL.DirectDriver()
	if os.path.exists( "output/"+SH_name ):
		shutil.rmtree( "output/"+SH_name )
	driver.submit(job, "output/"+SH_name )



