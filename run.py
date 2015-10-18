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
directory = "/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v51_pT50/BKG/"

my_SHs = {}
for sampleHandlerName in [
							# "QCD",
							"W",
							"Z",
							"Top",
							"Diboson",
							]:

	my_SHs[sampleHandlerName] = ROOT.SH.SampleHandler(); 
	ROOT.SH.ScanDir().sampleDepth(0).samplePattern("%s*"%sampleHandlerName).scan(my_SHs[sampleHandlerName], directory)

	my_SHs[sampleHandlerName].setMetaString("nc_tree", "%s_SRAll"%sampleHandlerName)
	pass


for sampleHandlerName in [
						# "SS_direct",
						"GG_direct",
							]:

	f = ROOT.TFile("%s/%s.root"%(directory,sampleHandlerName) )
	treeList = []
	dirList = ROOT.gDirectory.GetListOfKeys()
	for k1 in dirList: 
		t1 = k1.ReadObj()
		if (type(t1) is ROOT.TTree  ):
			# print t1.GetName()
			treeList.append(t1.GetName())

	for treeName in treeList:
		if "SRAll" in treeName:
			my_SHs[treeName] = ROOT.SH.SampleHandler(); 
			ROOT.SH.ScanDir().sampleDepth(0).samplePattern("%s*"%sampleHandlerName).scan(my_SHs[treeName], directory)
			my_SHs[treeName].setMetaString("nc_tree", "%s"%treeName )


cuts = {}
limits = {}


var_dphiVP = "((dphiVP-pi)/(pi))"
var_dphiPCa = "( dphiPCa*(dphiPCa<pi)+(2*pi-dphiPCa)*(dphiPCa>pi) )"
var_dphiPCb = "( dphiPCb*(dphiPCb<pi)+(2*pi-dphiPCb)*(dphiPCb>pi) )"
var_HT6PP = "(pTPP_V1a+pTPP_V2a+pTPP_V1b+pTPP_V2b+pTPP_Ia+pTPP_Ib)"
var_RPZ = " RPZ / (RPZ+%s)  "%var_HT6PP


cuts["SR1"] = []
cuts["SR1"] += ["(pT_jet1 > 50.)"]
cuts["SR1"] += ["(pT_jet2 > 50.)"]
cuts["SR1"] += ["(MDR > 300.)"]
cuts["SR1"] += ["(deltaQCD/(Rsib-1) < 0.05)"]
cuts["SR1"] += ["(RPT < 0.4)"]
cuts["SR1"] += ["(%s < 0.5)"%var_RPZ]
cuts["SR1"] += ["(abs(%s) < 0.55)"%var_dphiVP ]
cuts["SR1"] += ["(abs(cosP+%s)/2 < 0.3)"%var_dphiVP]
cuts["SR1"] += ["( abs(%s-%s)/pi < 0.7  )"%(var_dphiPCa,var_dphiPCb)]
cuts["SR1"] += ["((%s+%s)/(2*pi) < 0.6  )"%(var_dphiPCa,var_dphiPCb) ]
cuts["SR1"] += ["((H2PP / H6PP) > 0.3)" ] 
cuts["SR1"] += ["((%s / H6PP) > 0.3)"%var_HT6PP ] 
cuts["SR1"] += ["((H2PP/%s) < 0.85)"%var_HT6PP ] 
cuts["SR1"] += ["(abs(H2Pa/H3Pa - H2Pb/H3Pb) < 0.35 )" ] 
cuts["SR1"] += ["(  %s > 1000.  )"%var_HT6PP  ]
cuts["SR1"] += ["(  H2PP > 500.  )"  ]
cuts["SR1"] += ["(  min(H3Pa,H3Pb) > 350. )"  ]
cuts["SR1"] += ["(  min(pTPP_jet2a,pTPP_jet2b)/%s > 0.06 )"%var_HT6PP  ]



limits["SR1"] =   []  #[]
limits["SR1"] +=  [(50,0,1000)]  # ["(pT_jet1>50.&&pT_jet1>50.)"]
limits["SR1"] +=  [(50,0,1000)]  # ["(pT_jet1>50.&&pT_jet1>50.)"]
limits["SR1"] +=  [(50,0,2000)]  # ["(MDR>300)"]
limits["SR1"] +=  [(50,-1,1)]  # ["(deltaQCD>0.05*(1-Rsib))"]
limits["SR1"] +=  [(50,0,1)]  # ["(RPT<0.4)"]
limits["SR1"] +=  [(50,0,1)]  # ["(RPZ<0.5)"]
limits["SR1"] +=  [(50,0,1)]  # ["(abs(%s)<0.55)"%var_dphiVP ]
limits["SR1"] +=  [(50,0,1)]  # ["(abs(cosP+%s)/2<0.3)"%var_dphiVP]
limits["SR1"] +=  [(50,0,1)]  # ["( abs(var_dphiPCa-var_dphiPCb) < 0.7  )"]
limits["SR1"] +=  [(50,0,1)]  # ["(var_dphiPCa+var_dphiPCb < 0.6  )"]
limits["SR1"] +=   [(50,0,1)]       # ["((H2PP / H6PP) > 0.3)" ] 
limits["SR1"] +=   [(50,0,1)]       # ["((%s / H6PP) > 0.3)"%var_HT6PP ] 
limits["SR1"] +=   [(50,0,1)]       # ["((H2PP/%s) < 0.85)"%var_HT6PP ] 
limits["SR1"] +=   [(50,0,1)]       # ["(abs(H2Pa/H3Pa - H2Pb/H3Pb) < 0.35" ] 
limits["SR1"] +=  [(50,0,4000)]  # ["(  %s > 1000  )"%var_HT6PP  ]
limits["SR1"] +=  [(50,0,4000)]  # ["(  H2PP > 500  )"  ]
limits["SR1"] +=  [(50,0,2000)]  # ["(  min(H3Pa,H3pb) > 350 )"  ]
limits["SR1"] +=  [(50,0,0.2)]  # ["(  min(pTPP_jet2a,pTPP_jet2b)/%s > 350 )"%var_HT6PP  ]



cuts["SR2"] = []
cuts["SR2"] += ["(pT_jet1 > 50.)"]
cuts["SR2"] += ["(pT_jet2 > 50.)"]
cuts["SR2"] += ["(MDR > 300.)"]
cuts["SR2"] += ["(deltaQCD/(Rsib-1) < 0.05)"]
cuts["SR2"] += ["(RPT < 0.4)"]
cuts["SR2"] += ["(%s < 0.5)"%var_RPZ]
cuts["SR2"] += ["(abs(cosP+%s)/2 < 0.5)"%var_dphiVP]
cuts["SR2"] += ["(abs(cosP-%s)/2 < 0.5)"%var_dphiVP]
cuts["SR2"] += ["( abs(%s-%s)/pi  < 0.7  )"%(var_dphiPCa,var_dphiPCb)]
cuts["SR2"] += ["( (%s+%s)/(2*pi)  < 0.6  )"%(var_dphiPCa,var_dphiPCb) ]
cuts["SR2"] += ["((H2PP / H6PP) > 0.3)" ] 
cuts["SR2"] += ["((%s / H6PP) > 0.75)"%var_HT6PP ] 
cuts["SR2"] += ["((H2PP/%s) < 0.9)"%var_HT6PP ] 
cuts["SR2"] += ["(abs(H2Pa/H3Pa - H2Pb/H3Pb) < 0.35)" ] 
cuts["SR2"] += ["(  %s > 1100.  )"%var_HT6PP  ]
cuts["SR2"] += ["(  H2PP > 600.  )"  ]
cuts["SR2"] += ["(  min(H3Pa,H3Pb) > 400. )"  ]
cuts["SR2"] += ["(  min(pTPP_jet2a,pTPP_jet2b)/%s > 0.06 )"%var_HT6PP  ]


limits["SR2"] = []
limits["SR2"] += [(50,0,1000)]  #["(pT_jet1>50.&&pT_jet1>50.)"]
limits["SR2"] += [(50,0,1000)]  #["(pT_jet1>50.&&pT_jet1>50.)"]
limits["SR2"] += [(50,0,2000)]  #["(MDR>300.)"]
limits["SR2"] += [(50,-1,1)]  #["(deltaQCD>0.05*(1.-Rsib))"]
limits["SR2"] += [(50,0,1)]  #["(RPT<0.4)"]
limits["SR2"] += [(50,0,1)]  #["(%s<0.5)"%var_RPZ]
limits["SR2"] += [(50,0,1)]  #["(abs(cosP+%s)/2<0.5)"%var_dphiVP]
limits["SR2"] += [(50,0,1)]  #["(abs(cosP-%s)/2<0.5)"%var_dphiVP]
limits["SR2"] += [(50,0,1)]  #["( abs(%s-%s) < 0.7  )"%(var_dphiPCa,var_dphiPCb)]
limits["SR2"] += [(50,0,1)]  #["(%s+%s < 0.6  )"%(var_dphiPCa,var_dphiPCb) ]
limits["SR2"] += [(50,0,1)]  #["((H2PP / H6PP) > 0.3)" ] 
limits["SR2"] += [(50,0,1)]  #["((%s / H6PP) > 0.75)"%var_HT6PP ] 
limits["SR2"] += [(50,0,1)]  #["((H2PP/%s) < 0.9)"%var_HT6PP ] 
limits["SR2"] += [(50,0,1)]  #["(abs(H2Pa/H3Pa - H2Pb/H3Pb) < 0.35)" ] 
limits["SR2"] += [(50,0,4000)]  #["(  %s > 1100.  )"%var_HT6PP  ]
limits["SR2"] += [(50,0,4000)]  #["(  H2PP > 600.  )"  ]
limits["SR2"] += [(50,0,2000)]  #["(  min(H3Pa,H3Pb) > 400. )"  ]
limits["SR2"] += [(50,0,0.2)]  #["(  min(pTPP_jet2a,pTPP_jet2b)/%s > 0.06 )"%var_HT6PP  ]



cuts["SR3"] = []
cuts["SR3"] += ["(pT_jet1 > 50.)"]
cuts["SR3"] += ["(pT_jet2 > 50.)"]
cuts["SR3"] += ["(MDR > 300.)"]
cuts["SR3"] += ["(deltaQCD/(Rsib-1) < 0.05)"]
cuts["SR3"] += ["(RPT < 0.4)"]
cuts["SR3"] += ["(%s < 0.55)"%var_RPZ]
cuts["SR3"] += ["(abs(cosP+%s)/2 < 0.3)"%var_dphiVP]
cuts["SR3"] += ["((H2PP / H6PP) > 0.23)" ] 
cuts["SR3"] += ["((%s / H6PP) > 0.55)"%var_HT6PP ] 
cuts["SR3"] += ["(  min(H3Pa,H3Pb)/H6PP > 0.22)" ] 
cuts["SR3"] += ["(abs(H2Pa/H3Pa - H2Pb/H3Pb) < 0.5)" ] 
cuts["SR3"] += ["(  %s > 1800.  )"%var_HT6PP  ]
cuts["SR3"] += ["(  H2PP > 700.  )"  ]
cuts["SR3"] += ["(  min(H3Pa,H3Pb) > 500. )"  ]
cuts["SR3"] += ["(  min(pTPP_jet2a,pTPP_jet2b)/%s > 0.06 )"%var_HT6PP  ]


limits["SR3"] = []
limits["SR3"] += [(50,0,1000)]  #["(pT_jet1>50.&&pT_jet1>50.)"]
limits["SR3"] += [(50,0,1000)]  #["(pT_jet1>50.&&pT_jet1>50.)"]
limits["SR3"] += [(50,0,2000)]  #["(MDR>300.)"]
limits["SR3"] += [(50,-1,1)]  #["(deltaQCD>0.05*(1.-Rsib))"]
limits["SR3"] += [(50,0,1)]  #["(RPT<0.4)"]
limits["SR3"] += [(50,0,1)]  #["(%s<0.5)"%var_RPZ]
limits["SR3"] += [(50,0,1)]  #["(abs(cosP+%s)/2<0.5)"%var_dphiVP]
limits["SR3"] += [(50,0,1)]  #["((H2PP / H6PP) > 0.3)" ] 
limits["SR3"] += [(50,0,1)]  #["((%s / H6PP) > 0.75)"%var_HT6PP ] 
limits["SR3"] += [(50,0,1)]  #["((H2PP/%s) < 0.9)"%var_HT6PP ] 
limits["SR3"] += [(50,0,1)]  #["(abs(H2Pa/H3Pa - H2Pb/H3Pb) < 0.35)" ] 
limits["SR3"] += [(50,0,4000)]  #["(  %s > 1100.  )"%var_HT6PP  ]
limits["SR3"] += [(50,0,4000)]  #["(  H2PP > 600.  )"  ]
limits["SR3"] += [(50,0,2000)]  #["(  min(H3Pa,H3Pb) > 400. )"  ]
limits["SR3"] += [(50,0,0.2)]  #["(  min(pTPP_jet2a,pTPP_jet2b)/%s > 0.06 )"%var_HT6PP  ]



cuts["SR4"] = []
cuts["SR4"] += ["(pT_jet1 > 50.)"]
cuts["SR4"] += ["(pT_jet2 > 50.)"]
cuts["SR4"] += ["(MDR > 300.)"]
cuts["SR4"] += ["(deltaQCD/(Rsib-1) < 0.05)"]
cuts["SR4"] += ["(RPT < 0.4)"]
cuts["SR4"] += ["(%s < 0.55)"%var_RPZ]
cuts["SR4"] += ["(abs(cosP+%s)/2 < 0.6)"%var_dphiVP]
cuts["SR4"] += ["((H2PP / H6PP) > 0.24)" ] 
cuts["SR4"] += ["(  min(H3Pa,H3Pb)/H6PP > 0.22)" ] 
cuts["SR4"] += ["(abs(H2Pa/H3Pa - H2Pb/H3Pb) < 0.5)" ] 
cuts["SR4"] += ["(  %s > 1900.  )"%var_HT6PP  ]
cuts["SR4"] += ["(  H2PP > 650.  )"  ]
cuts["SR4"] += ["(  min(H3Pa,H3Pb) > 600. )"  ]
cuts["SR4"] += ["(  min(pTPP_jet2a,pTPP_jet2b)/%s > 0.06 )"%var_HT6PP  ]


limits["SR4"] = []
limits["SR4"] += [(50,0,1000)]  #["(pT_jet1>50.&&pT_jet1>50.)"]
limits["SR4"] += [(50,0,1000)]  #["(pT_jet1>50.&&pT_jet1>50.)"]
limits["SR4"] += [(50,0,2000)]  #["(MDR>300.)"]
limits["SR4"] += [(50,-1,1)]  #["(deltaQCD>0.05*(1.-Rsib))"]
limits["SR4"] += [(50,0,1)]  #["(RPT<0.4)"]
limits["SR4"] += [(50,0,1)]  #["(%s<0.5)"%var_RPZ]
limits["SR4"] += [(50,0,1)]  #["(abs(cosP+%s)/2<0.5)"%var_dphiVP]
limits["SR4"] += [(50,0,1)]  #["((H2PP / H6PP) > 0.3)" ] 
limits["SR4"] += [(50,0,1)]  #["((H2PP/%s) < 0.9)"%var_HT6PP ] 
limits["SR4"] += [(50,0,1)]  #["(abs(H2Pa/H3Pa - H2Pb/H3Pb) < 0.35)" ] 
limits["SR4"] += [(50,0,4000)]  #["(  %s > 1100.  )"%var_HT6PP  ]
limits["SR4"] += [(50,0,4000)]  #["(  H2PP > 600.  )"  ]
limits["SR4"] += [(50,0,2000)]  #["(  min(H3Pa,H3Pb) > 400. )"  ]
limits["SR4"] += [(50,0,0.2)]  #["(  min(pTPP_jet2a,pTPP_jet2b)/%s > 0.06 )"%var_HT6PP  ]


cuts["SR5"] = []
cuts["SR5"] += ["(pT_jet1 > 50.)"]
cuts["SR5"] += ["(pT_jet2 > 50.)"]
cuts["SR5"] += ["(MDR > 300.)"]
cuts["SR5"] += ["(deltaQCD/(Rsib-1) < 0.05)"]
cuts["SR5"] += ["(RPT < 0.4)"]
cuts["SR5"] += ["(%s < 0.55)"%var_RPZ]
cuts["SR5"] += ["(abs(cosP+%s)/2 < 0.5)"%var_dphiVP]
cuts["SR5"] += ["(abs(cosP-%s)/2 < 0.875)"%var_dphiVP]
cuts["SR5"] += ["(  min(H3Pa,H3Pb)/H6PP > 0.2)" ] 
cuts["SR5"] += ["(abs(H2Pa/H3Pa - H2Pb/H3Pb) < 0.65)" ] 
cuts["SR5"] += ["(  %s > 2700.  )"%var_HT6PP  ]
cuts["SR5"] += ["(  H2PP > 900.  )"  ]
cuts["SR5"] += ["(  min(H3Pa,H3Pb) > 900. )"  ]
cuts["SR5"] += ["(  min(pTPP_jet2a,pTPP_jet2b)/%s > 0.035 )"%var_HT6PP  ]


limits["SR5"] = []
limits["SR5"] += [(50,0,1000)]  #["(pT_jet1>50.&&pT_jet1>50.)"]
limits["SR5"] += [(50,0,1000)]  #["(pT_jet1>50.&&pT_jet1>50.)"]
limits["SR5"] += [(50,0,2000)]  #["(MDR>300.)"]
limits["SR5"] += [(50,-1,1)]  #["(deltaQCD>0.05*(1.-Rsib))"]
limits["SR5"] += [(50,0,1)]  #["(RPT<0.4)"]
limits["SR5"] += [(50,0,1)]  #["(%s<0.5)"%var_RPZ]
limits["SR5"] += [(50,0,1)]  #["(abs(cosP+%s)/2<0.5)"%var_dphiVP]
limits["SR5"] += [(50,0,1)]  #["(abs(cosP-%s)/2<0.5)"%var_dphiVP]
limits["SR5"] += [(50,0,1)]  #["((H2PP/%s) < 0.9)"%var_HT6PP ] 
limits["SR5"] += [(50,0,1)]  #["(abs(H2Pa/H3Pa - H2Pb/H3Pb) < 0.35)" ] 
limits["SR5"] += [(50,0,4000)]  #["(  %s > 1100.  )"%var_HT6PP  ]
limits["SR5"] += [(50,0,4000)]  #["(  H2PP > 600.  )"  ]
limits["SR5"] += [(50,0,2000)]  #["(  min(H3Pa,H3Pb) > 400. )"  ]
limits["SR5"] += [(50,0,0.2)]  #["(  min(pTPP_jet2a,pTPP_jet2b)/%s > 0.06 )"%var_HT6PP  ]







## Define your cut strings here....
regions = {
	"no_cut": "(1)",
	"SR1": "*".join( ["(%s)"%mycut for mycut in cuts["SR1"] ]),
	"SR2": "*".join( ["(%s)"%mycut for mycut in cuts["SR2"] ]),
	"SR3": "*".join( ["(%s)"%mycut for mycut in cuts["SR3"] ]),
	"SR4": "*".join( ["(%s)"%mycut for mycut in cuts["SR4"] ]),
	"SR5": "*".join( ["(%s)"%mycut for mycut in cuts["SR5"] ]),
}


for SH_name, mysamplehandler in my_SHs.iteritems():

	job = ROOT.EL.Job()
	job.sampleHandler(mysamplehandler)


	cutflow = {}


	for region in regions:


		if "SR" in region:
			# ## This part sets up both N-1 hists and the cutflow histogram for region

			cutflow[region] = ROOT.TH1F ("cutflow_%s"%region, "cutflow_%s"%region, len(cuts[region])+1 , 0, len(cuts[region])+1 );
			cutflow[region].GetXaxis().SetBinLabel(1, "weight");

			for i,cutpart in enumerate(cuts[region]):

				cutpartname = cutpart.translate(None, " (),.").replace("*","_x_").replace("/","_over_").split(" < ")[0].split(" > ")[0]
				variablename = cutpart.split(" < ")[0].split(" > ")[0]+")"

				# print variablename
				job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("%s_minus_%s"%(region,cutpartname), "%s_%s"%(region,cutpartname), limits[region][i][0], limits[region][i][1], limits[region][i][2] ), variablename ,"weight*%s"%"*".join(["(%s)"%mycut for mycut in cuts[region] if mycut!=cutpart ])    )        )

				cutflow[region].GetXaxis().SetBinLabel (i+2, cutpart);

			job.algsAdd(ROOT.MD.AlgCFlow (cutflow[region]))


		###################################################################

		## each of this histograms will be made for each region


		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("H2PP_%s"%region, "H2PP_%s"%region, 100, 0, 2000), 
			"H2PP",
			"weight*%s"%regions[region]))
		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("pTPP_jet2_over_HT6PP_%s"%region, "pTPP_jet2_over_HT6PP_%s"%region, 100, 0, 0.1), 
			"( min(pTPP_jet2a,pTPP_jet2b)/%s )"%var_HT6PP,
			"weight*%s"%regions[region]))



	driver = ROOT.EL.DirectDriver()
	if os.path.exists( SH_name ):
		shutil.rmtree( SH_name )
	driver.submit(job, SH_name )



