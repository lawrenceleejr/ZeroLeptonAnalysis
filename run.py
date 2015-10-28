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

import atexit
@atexit.register
def quite_exit():
	ROOT.gSystem.Exit(0)


logging.info("loading packages")
ROOT.gROOT.Macro("$ROOTCOREDIR/scripts/load_packages.C")

# directory = "/afs/cern.ch/user/l/leejr/work/public/Merged0LNtuples/WorkshopNtuples/"
directory = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v51_Oct17_pT50/"
datadirectory = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v53_Data_pT50/"
signaldirectory = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v51_SIG_pT50/"
# directory = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v51_pT40/"

#directory = "/mnt/shared/leejr/Work/WorkshopNtuples/"
#signaldirectory = directory


my_SHs = {}
for sampleHandlerName in [
							# "QCD",
							"W",
							"Z",
							"Top",
							"Diboson",
							]:

	my_SHs[sampleHandlerName] = ROOT.SH.SampleHandler(); 
	ROOT.SH.ScanDir().sampleDepth(0).samplePattern("%s*"%sampleHandlerName).scan(my_SHs[sampleHandlerName], directory+"/BKG/")

	my_SHs[sampleHandlerName].setMetaString("nc_tree", "%s_SRAll"%sampleHandlerName)
	pass


for sampleHandlerName in [
						# "SS_direct",
						"GG_direct",
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
			ROOT.SH.ScanDir().sampleDepth(0).samplePattern("%s*"%sampleHandlerName).scan(my_SHs[treeName], signaldirectory)
			my_SHs[treeName].setMetaString("nc_tree", "%s"%treeName )


baseline = "( pT_jet1 > 50.) * ( pT_jet2 > 50.) * ( MDR > 300.)"


cuts = {}
limits = {}


## ZL Team

cuts["SR5j"] = []
cuts["SR5j"] += ["( MET > 200 )"]
cuts["SR5j"] += ["( pT_jet1 > 200 )"]
cuts["SR5j"] += ["( pT_jet2 > 100 )"]
cuts["SR5j"] += ["( pT_jet3 > 100 )"]
cuts["SR5j"] += ["( pT_jet4 > 100 )"]
cuts["SR5j"] += ["( pT_jet5 > 50 )"]
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






cuts["SR1A"] = []
cuts["SR1A"] += ["( deltaQCD > 0)"]
cuts["SR1A"] += ["( RPT < 0.4)"]
cuts["SR1A"] += ["( R_H2PP_H5PP > 0.35)"]
cuts["SR1A"] += ["( R_HT5PP_H5PP > 0.8)"]
cuts["SR1A"] += ["( RPZ_HT5PP < 0.5)"]
cuts["SR1A"] += ["( minR_pTj2i_HT3PPi > 0.125)"]
cuts["SR1A"] += ["( maxR_H1PPi_H2PPi < 0.95)"]
cuts["SR1A"] += ["( dangle < 0.5 )"]
cuts["SR1A"] += ["( HT5PP > 800)"]
cuts["SR1A"] += ["( H2PP > 550)"]


limits["SR1A"] = []
limits["SR1A"] += [(50,-1,1)]#["( deltaQCD > 0)"]
limits["SR1A"] += [(50,0,1)]#["( RPT < 0.4)"]
limits["SR1A"] += [(50,0,1)]#["( R_H2PP_H5PP > 0.35)"]
limits["SR1A"] += [(50,0,1)]#["( R_HT5PP_H5PP > 0.8)"]
limits["SR1A"] += [(50,0,1)]#["( RPZ_HT5PP < 0.5)"]
limits["SR1A"] += [(50,0,0.5)]#["( minR_pTj2i_HT3PPi > 0.125)"]
limits["SR1A"] += [(50,0.5,1)]#["( maxR_H1PPi_H2PPi < 0.95)"]
limits["SR1A"] += [(50,-1,1)]#["( dangle < 0.5 )"]
limits["SR1A"] += [(50,0,4000)]#["( HT5PP > 800)"]
limits["SR1A"] += [(50,0,2000)]#["( H2PP > 550)"]



cuts["SR1B"] = []
cuts["SR1B"] += ["( deltaQCD > 0)"]
cuts["SR1B"] += ["( RPT < 0.4)"]
cuts["SR1B"] += ["( R_H2PP_H5PP > 0.35)"]
cuts["SR1B"] += ["( R_HT5PP_H5PP > 0.8)"]
cuts["SR1B"] += ["( RPZ_HT5PP < 0.5)"]
cuts["SR1B"] += ["( minR_pTj2i_HT3PPi > 0.125)"]
cuts["SR1B"] += ["( maxR_H1PPi_H2PPi < 0.95)"]
cuts["SR1B"] += ["( dangle < 0.5 )"]
cuts["SR1B"] += ["( HT5PP > 1000)"]
cuts["SR1B"] += ["( H2PP > 550)"]


limits["SR1B"] = []
limits["SR1B"] += [(50,-1,1)]#["( deltaQCD > 0)"]
limits["SR1B"] += [(50,0,1)]#["( RPT < 0.4)"]
limits["SR1B"] += [(50,0,1)]#["( R_H2PP_H5PP > 0.35)"]
limits["SR1B"] += [(50,0,1)]#["( R_HT5PP_H5PP > 0.8)"]
limits["SR1B"] += [(50,0,1)]#["( RPZ_HT5PP < 0.5)"]
limits["SR1B"] += [(50,0,0.5)]#["( minR_pTj2i_HT3PPi > 0.125)"]
limits["SR1B"] += [(50,0.5,1)]#["( maxR_H1PPi_H2PPi < 0.95)"]
limits["SR1B"] += [(50,-1,1)]#["( dangle < 0.5 )"]
limits["SR1B"] += [(50,0,4000)]#["( HT5PP > 800)"]
limits["SR1B"] += [(50,0,2000)]#["( H2PP > 550)"]


cuts["SR1C"] = []
cuts["SR1C"] += ["( deltaQCD > 0)"]
cuts["SR1C"] += ["( RPT < 0.4)"]
cuts["SR1C"] += ["( R_H2PP_H5PP > 0.35)"]
cuts["SR1C"] += ["( R_HT5PP_H5PP > 0.8)"]
cuts["SR1C"] += ["( RPZ_HT5PP < 0.5)"]
cuts["SR1C"] += ["( minR_pTj2i_HT3PPi > 0.125)"]
cuts["SR1C"] += ["( maxR_H1PPi_H2PPi < 0.95)"]
cuts["SR1C"] += ["( dangle < 0.5 )"]
cuts["SR1C"] += ["( HT5PP > 1200)"]
cuts["SR1C"] += ["( H2PP > 550)"]


limits["SR1C"] = []
limits["SR1C"] += [(50,-1,1)]#["( deltaQCD > 0)"]
limits["SR1C"] += [(50,0,1)]#["( RPT < 0.4)"]
limits["SR1C"] += [(50,0,1)]#["( R_H2PP_H5PP > 0.35)"]
limits["SR1C"] += [(50,0,1)]#["( R_HT5PP_H5PP > 0.8)"]
limits["SR1C"] += [(50,0,1)]#["( RPZ_HT5PP < 0.5)"]
limits["SR1C"] += [(50,0,0.5)]#["( minR_pTj2i_HT3PPi > 0.125)"]
limits["SR1C"] += [(50,0.5,1)]#["( maxR_H1PPi_H2PPi < 0.95)"]
limits["SR1C"] += [(50,-1,1)]#["( dangle < 0.5 )"]
limits["SR1C"] += [(50,0,4000)]#["( HT5PP > 800)"]
limits["SR1C"] += [(50,0,2000)]#["( H2PP > 550)"]







cuts["SR2A"] = []
cuts["SR2A"] += ["( deltaQCD > 0)"]
cuts["SR2A"] += ["( RPT < 0.4)"]
cuts["SR2A"] += ["( R_H2PP_H5PP > 0.25)"]
cuts["SR2A"] += ["( R_HT5PP_H5PP > 0.75)"]
cuts["SR2A"] += ["( RPZ_HT5PP < 0.55)"]
cuts["SR2A"] += ["( minR_pTj2i_HT3PPi > 0.11)"]
cuts["SR2A"] += ["( maxR_H1PPi_H2PPi < 0.97)"]
cuts["SR2A"] += ["( HT5PP > 1400)"]
cuts["SR2A"] += ["( H2PP > 750)"]


limits["SR2A"] = []
limits["SR2A"] += [(50,-1,1)]#["( deltaQCD > 0)"]
limits["SR2A"] += [(50,0,1)]#["( RPT < 0.4)"]
limits["SR2A"] += [(50,0,1)]#["( R_H2PP_H5PP > 0.35)"]
limits["SR2A"] += [(50,0,1)]#["( R_HT5PP_H5PP > 0.8)"]
limits["SR2A"] += [(50,0,1)]#["( RPZ_HT5PP < 0.5)"]
limits["SR2A"] += [(50,0,0.5)]#["( minR_pTj2i_HT3PPi > 0.125)"]
limits["SR2A"] += [(50,0.5,1)]#["( maxR_H1PPi_H2PPi < 0.95)"]
limits["SR2A"] += [(50,0,4000)]#["( HT5PP > 800)"]
limits["SR2A"] += [(50,0,2000)]#["( H2PP > 550)"]



cuts["SR2B"] = []
cuts["SR2B"] += ["( deltaQCD > 0)"]
cuts["SR2B"] += ["( RPT < 0.4)"]
cuts["SR2B"] += ["( R_H2PP_H5PP > 0.25)"]
cuts["SR2B"] += ["( R_HT5PP_H5PP > 0.75)"]
cuts["SR2B"] += ["( RPZ_HT5PP < 0.55)"]
cuts["SR2B"] += ["( minR_pTj2i_HT3PPi > 0.11)"]
cuts["SR2B"] += ["( maxR_H1PPi_H2PPi < 0.97)"]
cuts["SR2B"] += ["( HT5PP > 1600)"]
cuts["SR2B"] += ["( H2PP > 750)"]


limits["SR2B"] = []
limits["SR2B"] += [(50,-1,1)]#["( deltaQCD > 0)"]
limits["SR2B"] += [(50,0,1)]#["( RPT < 0.4)"]
limits["SR2B"] += [(50,0,1)]#["( R_H2PP_H5PP > 0.35)"]
limits["SR2B"] += [(50,0,1)]#["( R_HT5PP_H5PP > 0.8)"]
limits["SR2B"] += [(50,0,1)]#["( RPZ_HT5PP < 0.5)"]
limits["SR2B"] += [(50,0,0.5)]#["( minR_pTj2i_HT3PPi > 0.125)"]
limits["SR2B"] += [(50,0.5,1)]#["( maxR_H1PPi_H2PPi < 0.95)"]
limits["SR2B"] += [(50,0,4000)]#["( HT5PP > 800)"]
limits["SR2B"] += [(50,0,2000)]#["( H2PP > 550)"]

cuts["SR2C"] = []
cuts["SR2C"] += ["( deltaQCD > 0)"]
cuts["SR2C"] += ["( RPT < 0.4)"]
cuts["SR2C"] += ["( R_H2PP_H5PP > 0.25)"]
cuts["SR2C"] += ["( R_HT5PP_H5PP > 0.75)"]
cuts["SR2C"] += ["( RPZ_HT5PP < 0.55)"]
cuts["SR2C"] += ["( minR_pTj2i_HT3PPi > 0.11)"]
cuts["SR2C"] += ["( maxR_H1PPi_H2PPi < 0.97)"]
cuts["SR2C"] += ["( HT5PP > 1800)"]
cuts["SR2C"] += ["( H2PP > 750)"]


limits["SR2C"] = []
limits["SR2C"] += [(50,-1,1)]#["( deltaQCD > 0)"]
limits["SR2C"] += [(50,0,1)]#["( RPT < 0.4)"]
limits["SR2C"] += [(50,0,1)]#["( R_H2PP_H5PP > 0.35)"]
limits["SR2C"] += [(50,0,1)]#["( R_HT5PP_H5PP > 0.8)"]
limits["SR2C"] += [(50,0,1)]#["( RPZ_HT5PP < 0.5)"]
limits["SR2C"] += [(50,0,0.5)]#["( minR_pTj2i_HT3PPi > 0.125)"]
limits["SR2C"] += [(50,0.5,1)]#["( maxR_H1PPi_H2PPi < 0.95)"]
limits["SR2C"] += [(50,0,4000)]#["( HT5PP > 800)"]
limits["SR2C"] += [(50,0,2000)]#["( H2PP > 550)"]


cuts["SR3A"] = []
cuts["SR3A"] += ["( deltaQCD > 0)"]
cuts["SR3A"] += ["( RPT < 0.4)"]
cuts["SR3A"] += ["( R_H2PP_H5PP > 0.2)"]
cuts["SR3A"] += ["( R_HT5PP_H5PP > 0.65)"]
cuts["SR3A"] += ["( RPZ_HT5PP < 0.6)"]
cuts["SR3A"] += ["( minR_pTj2i_HT3PPi > 0.09)"]
cuts["SR3A"] += ["( maxR_H1PPi_H2PPi < 0.975)"]
cuts["SR3A"] += ["( HT5PP > 2000)"]
cuts["SR3A"] += ["( H2PP > 850)"]


limits["SR3A"] = []
limits["SR3A"] += [(50,-1,1)]#["( deltaQCD > 0)"]
limits["SR3A"] += [(50,0,1)]#["( RPT < 0.4)"]
limits["SR3A"] += [(50,0,1)]#["( R_H2PP_H5PP > 0.35)"]
limits["SR3A"] += [(50,0,1)]#["( R_HT5PP_H5PP > 0.8)"]
limits["SR3A"] += [(50,0,1)]#["( RPZ_HT5PP < 0.5)"]
limits["SR3A"] += [(50,0,0.5)]#["( minR_pTj2i_HT3PPi > 0.125)"]
limits["SR3A"] += [(50,0.5,1)]#["( maxR_H1PPi_H2PPi < 0.95)"]
limits["SR3A"] += [(50,0,4000)]#["( HT5PP > 800)"]
limits["SR3A"] += [(50,0,2000)]#["( H2PP > 550)"]


cuts["SR3B"] = []
cuts["SR3B"] += ["( deltaQCD > 0)"]
cuts["SR3B"] += ["( RPT < 0.4)"]
cuts["SR3B"] += ["( R_H2PP_H5PP > 0.2)"]
cuts["SR3B"] += ["( R_HT5PP_H5PP > 0.65)"]
cuts["SR3B"] += ["( RPZ_HT5PP < 0.6)"]
cuts["SR3B"] += ["( minR_pTj2i_HT3PPi > 0.09)"]
cuts["SR3B"] += ["( maxR_H1PPi_H2PPi < 0.975)"]
cuts["SR3B"] += ["( HT5PP > 2250)"]
cuts["SR3B"] += ["( H2PP > 850)"]


limits["SR3B"] = []
limits["SR3B"] += [(50,-1,1)]#["( deltaQCD > 0)"]
limits["SR3B"] += [(50,0,1)]#["( RPT < 0.4)"]
limits["SR3B"] += [(50,0,1)]#["( R_H2PP_H5PP > 0.35)"]
limits["SR3B"] += [(50,0,1)]#["( R_HT5PP_H5PP > 0.8)"]
limits["SR3B"] += [(50,0,1)]#["( RPZ_HT5PP < 0.5)"]
limits["SR3B"] += [(50,0,0.5)]#["( minR_pTj2i_HT3PPi > 0.125)"]
limits["SR3B"] += [(50,0.5,1)]#["( maxR_H1PPi_H2PPi < 0.95)"]
limits["SR3B"] += [(50,0,4000)]#["( HT5PP > 800)"]
limits["SR3B"] += [(50,0,2000)]#["( H2PP > 550)"]


cuts["SR3C"] = []
cuts["SR3C"] += ["( deltaQCD > 0)"]
cuts["SR3C"] += ["( RPT < 0.4)"]
cuts["SR3C"] += ["( R_H2PP_H5PP > 0.2)"]
cuts["SR3C"] += ["( R_HT5PP_H5PP > 0.65)"]
cuts["SR3C"] += ["( RPZ_HT5PP < 0.6)"]
cuts["SR3C"] += ["( minR_pTj2i_HT3PPi > 0.09)"]
cuts["SR3C"] += ["( maxR_H1PPi_H2PPi < 0.975)"]
cuts["SR3C"] += ["( HT5PP > 2500)"]
cuts["SR3C"] += ["( H2PP > 850)"]


limits["SR3C"] = []
limits["SR3C"] += [(50,-1,1)]#["( deltaQCD > 0)"]
limits["SR3C"] += [(50,0,1)]#["( RPT < 0.4)"]
limits["SR3C"] += [(50,0,1)]#["( R_H2PP_H5PP > 0.35)"]
limits["SR3C"] += [(50,0,1)]#["( R_HT5PP_H5PP > 0.8)"]
limits["SR3C"] += [(50,0,1)]#["( RPZ_HT5PP < 0.5)"]
limits["SR3C"] += [(50,0,0.5)]#["( minR_pTj2i_HT3PPi > 0.125)"]
limits["SR3C"] += [(50,0.5,1)]#["( maxR_H1PPi_H2PPi < 0.95)"]
limits["SR3C"] += [(50,0,4000)]#["( HT5PP > 800)"]
limits["SR3C"] += [(50,0,2000)]#["( H2PP > 550)"]










# cuts["CRDB1B"] = []
# cuts["CRDB1B"] += ["( deltaQCD/(Rsib-1) < 0.05)"]
# cuts["CRDB1B"] += ["( RPT < 0.4)"]
# cuts["CRDB1B"] += ["( sangle < 0.5)"]
# cuts["CRDB1B"] += ["( minH3P/H6PP > 0.2)" ] 
# cuts["CRDB1B"] += ["( R_H2PP_H6PP > 0.25)" ] 
# cuts["CRDB1B"] += ["( R_HT6PP_H6PP > 0.8)" ] 
# cuts["CRDB1B"] += ["( min(R_pTj2a_HT6PP,R_pTj2b_HT6PP) > 0.06 )"  ]
# cuts["CRDB1B"] += ["( RPZ_HT6PP < 0.5)"]
# cuts["CRDB1B"] += ["( abs(dangle) < 0.5 )"  ]
# cuts["CRDB1B"] += ["( R_H2PP_HT6PP < 0.9)" ] 
# cuts["CRDB1B"] += ["( abs(dH2o3P) < 0.5 )" ] 
# cuts["CRDB1B"] += ["( HT6PP > 800.  )"  ]
# cuts["CRDB1B"] += ["( H2PP > 650.  )"  ]
# cuts["CRDB1B"] += ["( H2PP/H3PP < 1  )"  ]
# cuts["CRDB1B"] += ["( H2PP/HT6PP < 1  )"  ]
# cuts["CRDB1B"] += ["( dphiVP > -1  )"  ]
# cuts["CRDB1B"] += ["( H3PP/HT6PP > 0.8  )"  ]
# cuts["CRDB1B"] += ["( abs(cosP) > 0  )"  ]
# cuts["CRDB1B"] += ["( H3PP/HT4PP < 1  )"  ]
# cuts["CRDB1B"] += ["( max(H2Pa,H2Pb)/HT6PP > 0  )"  ]
# cuts["CRDB1B"] += ["( min(H2Pa,H2Pb)/HT6PP > 0  )"  ]
# cuts["CRDB1B"] += ["( min(H2Pa,H2Pb)/minH3P > 0  )"  ]
# cuts["CRDB1B"] += ["( H3PP/(HT4PP+H2PP) < 0.55  )"  ]
# cuts["CRDB1B"] += ["( HT4PP/H4PP > 0  )"  ]
# cuts["CRDB1B"] += ["( min(R_pTj1a_HT4PP,R_pTj1b_HT4PP) > 0 )"  ]

# limits["CRDB1B"] = []
# limits["CRDB1B"] +=   [(50,-1,1)]    #["( deltaQCD/(Rsib-1) < 0.05)"]
# limits["CRDB1B"] +=   [(50,0,1)]    #["( RPT < 0.4)"]
# limits["CRDB1B"] +=   [(50,0,1)]    #["( sangle < 0.5)"]
# limits["CRDB1B"] +=   [(50,0,1)]    #["( minH3P/H6PP > 0.2)" ] 
# limits["CRDB1B"] +=   [(50,0,1)]    #["( R_H2PP_H6PP > 0.25)" ] 
# limits["CRDB1B"] +=   [(50,0,1)]    #["( R_HT6PP_H6PP > 0.7)" ] 
# limits["CRDB1B"] +=   [(50,0,0.2)]    #["( min(R_pTj2a_HT6PP,R_pTj2b_HT6PP) > 0.06 )"  ]
# limits["CRDB1B"] +=   [(50,0,1)]    #["( RPZ_HT6PP < 0.5)"]
# limits["CRDB1B"] +=   [(50,0,1)]    #["( abs(dangle) < 0.5 )"  ]
# limits["CRDB1B"] +=   [(50,0,1)]    #["( R_H2PP_HT6PP < 0.9)" ] 
# limits["CRDB1B"] +=   [(50,0,1)]    #["( abs(dH2o3P) < 0.5 )" ] 
# limits["CRDB1B"] +=   [(50,0,4000)]    #["( HT6PP > 800.  )"  ]
# limits["CRDB1B"] +=   [(50,0,4000)]    #["( H2PP > 650.  )"  ]
# limits["CRDB1B"] +=   [(50,0,1)]    #["( abs(dH2o3P) < 0.5 )" ] 
# limits["CRDB1B"] +=   [(50,0,1)]    #["( abs(dH2o3P) < 0.5 )" ] 
# limits["CRDB1B"] +=   [(50,-1,1)]    #["( abs(dH2o3P) < 0.5 )" ] 
# limits["CRDB1B"] +=   [(50,0,1)]    #["( abs(dH2o3P) < 0.5 )" ] 
# limits["CRDB1B"] +=   [(50,-1,1)]    #["( abs(dH2o3P) < 0.5 )" ] 
# limits["CRDB1B"] +=   [(50,0,1)]    #["( abs(dH2o3P) < 0.5 )" ] 
# limits["CRDB1B"] +=   [(50,0,1)]    #["( abs(dH2o3P) < 0.5 )" ] 
# limits["CRDB1B"] +=   [(50,0,1)]    #["( abs(dH2o3P) < 0.5 )" ] 
# limits["CRDB1B"] +=   [(50,0,1)]    #["( abs(dH2o3P) < 0.5 )" ] 
# limits["CRDB1B"] +=   [(50,0,1)]    #["( abs(dH2o3P) < 0.5 )" ] 
# limits["CRDB1B"] +=   [(50,0,1)]    #["( abs(dH2o3P) < 0.5 )" ] 
# limits["CRDB1B"] +=   [(50,0,1)]    #["( abs(dH2o3P) < 0.5 )" ] 



## Define your cut strings here....
regions = {
	# "no_cut": "(1)",
	"SR5j": "*".join( ["(%s)"%mycut for mycut in cuts["SR5j"] ]),
	"SR4jt": "*".join( ["(%s)"%mycut for mycut in cuts["SR4jt"] ]),
	"SR1A": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR1A"] ]),
	"SR1B": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR1B"] ]),
	"SR1C": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR1C"] ]),
	"SR2A": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR2A"] ]),
	"SR2B": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR2B"] ]),
	"SR2C": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR2C"] ]),
	"SR3A": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR3A"] ]),
	"SR3B": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR3B"] ]),
	"SR3C": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR3C"] ]),
	# "SR3C": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["SR3C"] ]),
	# "CRDB1B": baseline+"*"+"*".join( ["(%s)"%mycut for mycut in cuts["CRDB1B"] ]),

}


for SH_name, mysamplehandler in my_SHs.iteritems():

	job = ROOT.EL.Job()
	job.sampleHandler(mysamplehandler)

	cutflow = {}


	for region in regions:


		if "R" in region:
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


		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("H5PP_%s"%region, "H5PP_%s"%region, 100, 0, 10000), 
			"H5PP",
			"weight*%s"%regions[region]))
		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("MET_%s"%region, "MET_%s"%region, 100, 0, 2000), 
			"MET",
			"weight*%s"%regions[region]))
		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("Meff_%s"%region, "Meff_%s"%region, 100, 0, 5000), 
			"Meff",
			"weight*%s"%regions[region]))
		# job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("pTPP_jet2_over_HT6PP_%s"%region, "pTPP_jet2_over_HT6PP_%s"%region, 100, 0, 0.1), 
		# 	"( min(pTPP_jet2a,pTPP_jet2b)/%s )"%var_HT6PP,
		# 	"weight*%s"%regions[region]))



	driver = ROOT.EL.DirectDriver()
	if os.path.exists( "output/"+SH_name ):
		shutil.rmtree( "output/"+SH_name )
	driver.submit(job, "output/"+SH_name )



