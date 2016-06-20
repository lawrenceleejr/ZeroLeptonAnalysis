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
# treename = "CRY"
treename = "SRAll"

my_SHs = {}
for sampleHandlerName in [
#							"QCD",
#							"GammaJet",
#							"Wjets",
#							"Zjets",
#							"Top",
#							"Diboson",
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
							]:
	my_SHs[sampleHandlerName] = ROOT.SH.SampleHandler(); 
	ROOT.SH.ScanDir().sampleDepth(0).samplePattern("%s.root"%sampleHandlerName).scan(my_SHs[sampleHandlerName], datadirectory)
	print my_SHs[sampleHandlerName]
	print len(my_SHs[sampleHandlerName])
	my_SHs[sampleHandlerName].setMetaString("nc_tree", "Data_%s"%treename )

	for sample in my_SHs[sampleHandlerName]:
		print sample
		print sample.makeTChain().GetEntries()




# print ChannelsDict.finalChannelsDict
# print ChannelsDict.finalChannelsDict["SRJigsawSRS1a"]
print ChannelsDict.finalChannelsDict["SRJigsawSRS1a"].getCuts()
# print ChannelsDict.finalChannelsDict["SRJigsawSRS1a"].NV
print ChannelsDict.finalChannelsDict["SRJigsawSRS1a"].getCutsDict()
print ChannelsDict.finalChannelsDict["SRJigsawSRS1a"].commonCutList



cuts = {}
limits = {}


#############################################################
## Loose Plotting Regions

cuts["SRSLoose"] = OrderedDict()
cuts["SRSLoose"]["( deltaQCD > 0)"]           = (50,-1,1)
cuts["SRSLoose"]["( RPT_HT3PP < 0.2  )"]     = (50,0,1)
cuts["SRSLoose"]["( R_H2PP_H3PP > 0.2)"]      = (50,0,1)
cuts["SRSLoose"]["( RPZ_HT3PP < 0.8)"]       = (50,0,1)
cuts["SRSLoose"]["( pT_jet2 / HT3PP > 0.05)"] = (50,0,0.5)
cuts["SRSLoose"]["( HT3PP > 800)"]      = (50,0,4000)    
cuts["SRSLoose"]["( H2PP > 800)"]       = (50,0,2000)    


cuts["SRGLoose"] = OrderedDict()
cuts["SRGLoose"]["( deltaQCD > 0)"]              = (50,-1,1)
cuts["SRGLoose"]["( RPT_HT5PP < 0.2 )"]          = (50,0,1)
cuts["SRGLoose"]["( R_H2PP_H5PP > 0.2)"]         = (50,0,1)
cuts["SRGLoose"]["( R_HT5PP_H5PP > 0.2)"]        = (50,0,1)
cuts["SRGLoose"]["( RPZ_HT5PP < 0.8)"]           = (50,0,1)
cuts["SRGLoose"]["( minR_pTj2i_HT3PPi > 0.0)"]   = (50,0,0.5)
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
## Squark RJR - 3

cuts["SRS1"] = OrderedDict()
cuts["SRS1"]["( deltaQCD > 0)"]            = (50,-1,1)        
cuts["SRS1"]["( RPT_HT3PP < 0.08  )"]      = (50,0,1)              
cuts["SRS1"]["( R_H2PP_H3PP > 0.6)"]       = (50,0,1)             
cuts["SRS1"]["( R_H2PP_H3PP < 0.95)"]      = (50,0,1)              
cuts["SRS1"]["( RPZ_HT3PP < 0.5)"]        = (50,0,1)            
cuts["SRS1"]["( pT_jet2 / HT3PP > 0.16)"]  = (50,0,0.5)                  

cuts["SRS1a"] = deepcopy(cuts["SRS1"])
cuts["SRS1a"]["( HT3PP > 1000)"]  = (50,0,4000)   
cuts["SRS1a"]["( H2PP > 1000)"]    = (50,0,2000)     

cuts["SRS1b"] = deepcopy(cuts["SRS1"])
cuts["SRS1b"]["( HT3PP > 1200)"]  = (50,0,4000)         
cuts["SRS1b"]["( H2PP > 1000)"]    = (50,0,2000)       


cuts["SRS2"] = OrderedDict()
cuts["SRS2"]["( deltaQCD > 0)"]            =  (50,-1,1)
cuts["SRS2"]["( RPT_HT3PP < 0.08  )"]      =  (50,0,1)
cuts["SRS2"]["( R_H2PP_H3PP > 0.55)"]      =  (50,0,1)
cuts["SRS2"]["( R_H2PP_H3PP < 0.96)"]      =  (50,0,1)
cuts["SRS2"]["( RPZ_HT3PP < 0.55)"]         =  (50,0,1)
cuts["SRS2"]["( pT_jet2 / HT3PP > 0.15)"]  =  (50,0,0.5)

cuts["SRS2a"] = deepcopy(cuts["SRS2"])
cuts["SRS2a"]["( HT3PP > 1400)"]  = (50,0,4000)      
cuts["SRS2a"]["( H2PP > 1400)"]   = (50,0,2000)     

cuts["SRS2b"] = deepcopy(cuts["SRS2"])
cuts["SRS2b"]["( HT3PP > 1600)"]  = (50,0,4000)      
cuts["SRS2b"]["( H2PP > 1400)"]   = (50,0,2000)     

cuts["SRS3"] = OrderedDict()
cuts["SRS3"]["( deltaQCD > 0)"]           = (50,-1,1)
cuts["SRS3"]["( RPT_HT3PP < 0.08  )"]     = (50,0,1)
cuts["SRS3"]["( R_H2PP_H3PP > 0.5)"]      = (50,0,1)
cuts["SRS3"]["( R_H2PP_H3PP < 0.98)"]     = (50,0,1)
cuts["SRS3"]["( RPZ_HT3PP < 0.6)"]       = (50,0,1)
cuts["SRS3"]["( pT_jet2 / HT3PP > 0.13)"] = (50,0,0.5)

cuts["SRS3a"] = deepcopy(cuts["SRS3"])
cuts["SRS3a"]["( HT3PP > 1800)"]      = (50,0,4000)    
cuts["SRS3a"]["( H2PP > 1600)"]       = (50,0,2000)    

cuts["SRS3b"] = deepcopy(cuts["SRS3"])
cuts["SRS3b"]["( HT3PP > 2000)"] = (50,0,4000)    
cuts["SRS3b"]["( H2PP > 1600)"]  = (50,0,2000)    



cuts["CRTSLoose"] = deepcopy(cuts["SRS3"])
cuts["CRTSLoose"]["( HT3PP > 500 )"] = (50,0,4000)    
cuts["CRTSLoose"]["( H2PP > 500 )"]  = (50,0,2000)   
cuts["CRTSLoose"]["( nBJet > 0 )"]   = (10,0,5)  

cuts["CRWSLoose"] = deepcopy(cuts["SRS3"])
cuts["CRWSLoose"]["( HT3PP > 500 )"] = (50,0,4000)    
cuts["CRWSLoose"]["( H2PP > 500 )"]  = (50,0,2000)   
cuts["CRWSLoose"]["( nBJet < 1 )"]   = (10,0,5)  


# cuts["CRYSLoose"] = deepcopy(cuts["SRS3"])
# cuts["CRYSLoose"]["( HT3PP > 500)"] = (50,0,4000)
# cuts["CRYSLoose"]["( H2PP > 500)"]  = (50,0,2000)



##############################################################
#Gluino RJR

cuts["SRG1"] = OrderedDict()
cuts["SRG1"]["( deltaQCD > 0)"]               = (50,-1,1)
cuts["SRG1"]["( RPT_HT5PP < 0.08  )"]         = (50,0,1)
cuts["SRG1"]["( R_H2PP_H5PP > 0.35)"]         = (50,0,1)
cuts["SRG1"]["( R_HT5PP_H5PP > 0.8)"]         = (50,0,1)
cuts["SRG1"]["( RPZ_HT5PP < 0.5)"]            = (50,0,1)
cuts["SRG1"]["( minR_pTj2i_HT3PPi > 0.12)"]  = (50,0,0.5)
cuts["SRG1"]["( maxR_H1PPi_H2PPi < 0.95)"]    = (50,0.5,1)
cuts["SRG1"]["( dangle < 0.5 )"]              = (50,-1,1)

cuts["SRG1a"] = deepcopy(cuts["SRG1"])
cuts["SRG1a"]["( HT5PP > 1000)"]  = (50,0,4000)
cuts["SRG1a"]["( H2PP > 600)"]    = (50,0,2000)

cuts["SRG1b"] = deepcopy(cuts["SRG1"])
cuts["SRG1b"]["( HT5PP > 1200)"]  = (50,0,4000)     
cuts["SRG1b"]["( H2PP > 600)"]    = (50,0,2000)  


cuts["SRG2"] = OrderedDict()
cuts["SRG2"]["( deltaQCD > 0)"]             = (50,-1,1)
cuts["SRG2"]["( RPT_HT5PP < 0.08  )"]       = (50,0,1)
cuts["SRG2"]["( R_H2PP_H5PP > 0.25)"]       = (50,0,1)
cuts["SRG2"]["( R_HT5PP_H5PP > 0.75)"]      = (50,0,1)
cuts["SRG2"]["( RPZ_HT5PP < 0.55)"]         = (50,0,1)
cuts["SRG2"]["( minR_pTj2i_HT3PPi > 0.1)"] = (50,0,0.5)
cuts["SRG2"]["( maxR_H1PPi_H2PPi < 0.97)"]  = (50,0.5,1)

cuts["SRG2a"] = deepcopy(cuts["SRG2"])
cuts["SRG2a"]["( HT5PP > 1500)"]   = (50,0,4000)
cuts["SRG2a"]["( H2PP > 800)"]     = (50,0,2000) 

cuts["SRG2b"] = deepcopy(cuts["SRG2"])
cuts["SRG2b"]["( HT5PP > 1900)"] = (50,0,4000)
cuts["SRG2b"]["( H2PP > 800)"]   = (50,0,2000) 


cuts["SRG3"] = OrderedDict()
cuts["SRG3"]["( deltaQCD > 0)"]              = (50,-1,1)
cuts["SRG3"]["( RPT_HT5PP < 0.08  )"]        = (50,0,1)
cuts["SRG3"]["( R_H2PP_H5PP > 0.2)"]         = (50,0,1)
cuts["SRG3"]["( R_HT5PP_H5PP > 0.65)"]       = (50,0,1)
cuts["SRG3"]["( RPZ_HT5PP < 0.6)"]           = (50,0,1)
cuts["SRG3"]["( minR_pTj2i_HT3PPi > 0.08)"]  = (50,0,0.5)
cuts["SRG3"]["( maxR_H1PPi_H2PPi < 0.98)"]   = (50,0.5,1)

cuts["SRG3a"] = deepcopy(cuts["SRG3"])
cuts["SRG3a"]["( HT5PP > 2300)"]  = (50,0,4000)
cuts["SRG3a"]["( H2PP > 900)"]    = (50,0,2000)   

cuts["SRG3b"] = deepcopy(cuts["SRG3"])
cuts["SRG3b"]["( HT5PP > 2800)"] = (50,0,4000)
cuts["SRG3b"]["( H2PP > 900)"]   = (50,0,2000)  





cuts["CRTGLoose"] = deepcopy(cuts["SRG3"])
cuts["CRTGLoose"]["( HT5PP > 500 )"]    = (50,0,4000) 
cuts["CRTGLoose"]["( H2PP > 500 )"]    = (50,0,2000) 
cuts["CRTGLoose"]["( nBJet > 0 )"]    = (10,0,5) 

cuts["CRWGLoose"] = deepcopy(cuts["SRG3"])
cuts["CRWGLoose"]["( HT5PP > 500 )"]    = (50,0,4000) 
cuts["CRWGLoose"]["( H2PP > 500 )"]    = (50,0,2000) 
cuts["CRWGLoose"]["( nBJet < 1 )"]    = (10,0,5)  

# cuts["CRWGLoose"] = deepcopy(cuts["SRG3"])
# cuts["CRWGLoose"] += ["( HT3PP > 500 )"]
# cuts["CRWGLoose"] += ["( H2PP > 500 )"]
# cuts["CRWGLoose"] += ["( nBJet < 1 )"]
# limits["CRWGLoose"] = deepcopy(limits["SRG3"])
# limits["CRWGLoose"] += [(10,0,10)]

cuts["CRYGLoose"] = deepcopy(cuts["SRG3"])
cuts["CRYGLoose"]["( HT3PP > 500)"] = (50,0,4000)
cuts["CRYGLoose"]["( H2PP > 500)"]  = (50,0,2000)





## Compressed stuff: ##########################

cuts["SRC1"] = OrderedDict()
cuts["SRC1"]["( RISR > 0.9 )"]     = (50,0,1)      
cuts["SRC1"]["( MS > 100 )"]       = (50,0,2000)   
cuts["SRC1"]["( dphiISRI > 3.1 )"] = (50,0,4)         
cuts["SRC1"]["( PTISR > 800  )"]   = (50,0,2000)       
cuts["SRC1"]["( NV > 0  )"]        = (10,0,10)  

cuts["SRC2"] = OrderedDict()
cuts["SRC2"]["( RISR > 0.85 )"]     = (50,0,1)      
cuts["SRC2"]["( MS > 100 )"]       = (50,0,2000)   
cuts["SRC2"]["( dphiISRI > 3.07 )"] = (50,0,4)         
cuts["SRC2"]["( PTISR > 800  )"]   = (50,0,2000)       
cuts["SRC2"]["( NV > 0  )"]        = (10,0,10)  


cuts["SRC3"] = OrderedDict()
cuts["SRC3"]["( RISR > 0.8 )"]     = (50,0,1)      
cuts["SRC3"]["( MS > 200 )"]       = (50,0,2000)   
cuts["SRC3"]["( dphiISRI > 2.95 )"] = (50,0,4)         
cuts["SRC3"]["( PTISR > 700  )"]   = (50,0,2000)       
cuts["SRC3"]["( NV > 1  )"]        = (10,0,10)  


cuts["SRC4"] = OrderedDict()
cuts["SRC4"]["( RISR > 0.75 )"]     = (50,0,1)      
cuts["SRC4"]["( MS > 500 )"]       = (50,0,2000)   
cuts["SRC4"]["( dphiISRI > 2.95 )"] = (50,0,4)         
cuts["SRC4"]["( dphiMin2 > 0.4   )"]   = (50,0,4)      
cuts["SRC4"]["( PTISR > 700  )"]   = (50,0,2000)      
cuts["SRC4"]["( NV > 1  )"]        = (10,0,10)  


cuts["SRC5"] = OrderedDict()
cuts["SRC5"]["( RISR > 0.7 )"]     = (50,0,1)      
cuts["SRC5"]["( MS > 500 )"]       = (50,0,2000)   
cuts["SRC5"]["( dphiISRI > 2.95 )"] = (50,0,4)         
cuts["SRC5"]["( dphiMin2 > 0.4   )"]   = (50,0,4)      
cuts["SRC5"]["( PTISR > 700  )"]   = (50,0,2000)       
cuts["SRC5"]["( NV > 2  )"]        = (10,0,10)  


# cuts["CRWCLoose"] = deepcopy(cuts["SRC4"])
# cuts["CRWCLoose"] += ["( nBJet < 1 )"]
# limits["CRWCLoose"] = deepcopy(limits["SRC4"])
# limits["CRWCLoose"].pop()
# limits["CRWCLoose"] += [(10,0,10)]

cuts["CRTCLoose"] = deepcopy(cuts["SRC1"])
cuts["CRTCLoose"]["( nBJet > 0 )"] = (10,0,5)

cuts["CRWCLoose"] = deepcopy(cuts["SRC1"])
cuts["CRWCLoose"]["( nBJet < 1 )"] = (10,0,5)
# limits["CRTCLoose"] = deepcopy(limits["SRC4"])
# limits["CRTCLoose"].pop()
# limits["CRTCLoose"] += [(10,0,10)]

cuts["CRYC"] = deepcopy(cuts["SRC1"])





## Define your cut strings here....
regions = {
	# "no_cut": "(1)",

	"SRS1a": baseline+"*"+"*".join( cuts["SRS1a"].keys() ),
	"SRS1b": baseline+"*"+"*".join( cuts["SRS1b"].keys() ),
	"SRS2a": baseline+"*"+"*".join( cuts["SRS2a"].keys() ),
	"SRS2b": baseline+"*"+"*".join( cuts["SRS2b"].keys() ),
	"SRS3a": baseline+"*"+"*".join( cuts["SRS3a"].keys() ),
	"SRS3b": baseline+"*"+"*".join( cuts["SRS3b"].keys() ),

	"SRG1a": baseline+"*"+"*".join( cuts["SRG1a"].keys() ),
	"SRG1b": baseline+"*"+"*".join( cuts["SRG1b"].keys() ),
	"SRG2a": baseline+"*"+"*".join( cuts["SRG2a"].keys() ),
	"SRG2b": baseline+"*"+"*".join( cuts["SRG2b"].keys() ),
	"SRG3a": baseline+"*"+"*".join( cuts["SRG3a"].keys() ),
	"SRG3b": baseline+"*"+"*".join( cuts["SRG3b"].keys() ),

	"SRC1": baseline+"*"+"*".join( cuts["SRC1"].keys() ),
	"SRC2": baseline+"*"+"*".join( cuts["SRC2"].keys() ),
	"SRC3": baseline+"*"+"*".join( cuts["SRC3"].keys() ),
	"SRC4": baseline+"*"+"*".join( cuts["SRC4"].keys() ),
	"SRC5": baseline+"*"+"*".join( cuts["SRC5"].keys() ),

	"SRSLoose": baseline+"*"+"*".join( cuts["SRSLoose"].keys() ),
	"SRGLoose": baseline+"*"+"*".join( cuts["SRGLoose"].keys() ),
	"SRCLoose": baseline+"*"+"*".join( cuts["SRCLoose"].keys() ),

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



	for region in regions:

		if "SR" in region:
			# ## This part sets up both N-1 hists and the cutflow histogram for region

			cutflow[region] = ROOT.TH1F ("cutflow_%s"%region, "cutflow_%s"%region, len(cuts[region])+2 , 0, len(cuts[region])+2 );
			cutflow[region].GetXaxis().SetBinLabel(1, weightstring);
			cutflow[region].GetXaxis().SetBinLabel(2, baseline);

			for i,cutpart in enumerate(cuts[region]):

				cutpartname = cutpart.translate(None, " (),.").replace("*","_x_").replace("/","_over_").split(" < ")[0].split(" > ")[0]
				variablename = cutpart.split("<")[0].split(">")[0]+")"

				if "Data" not in SH_name:
					job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("%s_minus_%s"%(region,cutpartname), "%s_%s"%(region,cutpartname), cuts[region][cutpart][0], cuts[region][cutpart][1], cuts[region][cutpart][2] ), variablename ,baseline+"*"+weightstring+"*%s"%"*".join(["(%s)"%mycut for mycut in cuts[region] if mycut!=cutpart ])    )        )
				else:
					flippedcutpart = cutpart.replace(">","%TEMP%").replace("<",">").replace("%TEMP%","<")
					job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("%s_minus_%s"%(region,cutpartname), "%s_%s"%(region,cutpartname), cuts[region][cutpart][0], cuts[region][cutpart][1], cuts[region][cutpart][2] ), variablename ,baseline+"*"+weightstring+"*%s"%"*".join(["(%s)"%mycut for mycut in cuts[region] if mycut!=cutpart ]) + "*" + flippedcutpart  )        )

				cutflow[region].GetXaxis().SetBinLabel (i+3, cutpart);

			job.algsAdd(ROOT.MD.AlgCFlow (cutflow[region]))


		if "CR" in region:
			# ## This part sets up both N-1 hists and the cutflow histogram for region

			cutflow[region] = ROOT.TH1F ("cutflow_%s"%region, "cutflow_%s"%region, len(cuts[region])+2 , 0, len(cuts[region])+2 );
			cutflow[region].GetXaxis().SetBinLabel(1, weightstring);
			cutflow[region].GetXaxis().SetBinLabel(2, baseline);

			for i,cutpart in enumerate(cuts[region]):

				cutpartname = cutpart.translate(None, " (),.").replace("*","_x_").replace("/","_over_").split(" < ")[0].split(" > ")[0]
				variablename = cutpart.split("<")[0].split(">")[0]+")"

				job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("%s_minus_%s"%(region,cutpartname), "%s_%s"%(region,cutpartname), cuts[region][cutpart][0], cuts[region][cutpart][1], cuts[region][cutpart][2] ), variablename ,baseline+"*"+weightstring+"*%s"%"*".join(["(%s)"%mycut for mycut in cuts[region] if mycut!=cutpart ])    )        )

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



