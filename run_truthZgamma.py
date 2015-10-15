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
########### Configuration ######################################
##
##

lumi = 3.5  ## in pb-1
search_directories = ["/data/users/rsmith/photonTruthStudies/"]

##
##
########### Gather input ######################################
##
##

logging.info("creating new sample handler")
sh_all = ROOT.SH.SampleHandler()

discoverInput.discover(sh_all, search_directories)

sh_all.setMetaString("nc_tree", "CRY_SRAllNT")

ROOT.SH.readSusyMeta(sh_all,"./susy_crosssections_13TeV.txt")

logging.info("adding my tags defined in discoverInput.py")
discoverInput.addTags(sh_all)

## Split up samplehandler into per-BG SH's based on tag metadata

#sh_data   = sh_all.find("data")
#sh_signal = sh_all.find("signal")
sh_bg = {}

#sh_bg["qcd"  ] = sh_all.find("qcd"  )
#sh_bg["top"  ] = sh_all.find("top"  )
sh_bg["gamma"]    = sh_all.find("gamma")
sh_bg["znunu_lo"] = sh_all.find("znunu_lo")

print sh_bg
sh_bg["gamma"].printContent()
sh_bg["znunu_lo"].printContent()

######This will be done per samplehandler ############################
##
##


#Creation of output directory names
tempDirDict = {}

for key in sh_bg.keys() :
    tempDirDict[key] = "rundir_" + key



#To scale the histograms in the files after the event loop is done...
def scaleMyRootFiles(mysamplehandlername,mylumi):
        mysamplehandler = sh_bg[mysamplehandlername]
	for sample in mysamplehandler:
		tempxs = sample.getMetaDouble("nc_xs") * sample.getMetaDouble("kfactor") * sample.getMetaDouble("filter_efficiency")

		print "Scaling %s by %f/(%f or %f)"%(sample.getMetaString("short_name"), tempxs, sample.getMetaDouble("nc_nevt"), sample.getMetaDouble("nc_sumw"))
		m_eventscaling = tempxs
		if sample.getMetaDouble("nc_nevt"):
			m_eventscaling /= sample.getMetaDouble("nc_nevt") if "jetjet" in sample.getMetaString("short_name") else sample.getMetaDouble("nc_sumw")
		else:
			m_eventscaling = 0.
		myfile = ROOT.TFile( tempDirDict[mysamplehandlername]+"/hist-"+sample.fileName(0).split("/")[-2]+".root","UPDATE")
		dirList = ROOT.gDirectory.GetListOfKeys()
		for k1 in dirList:
			h1 = k1.ReadObj()
			h1.Scale(m_eventscaling)
			h1.Scale(mylumi)
			h1.Write()
		myfile.Close()



for mysamplehandlername in sh_bg.keys():
        mysamplehandler = sh_bg[mysamplehandlername]
	for sample in mysamplehandler:
                print sample
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


	job = ROOT.EL.Job()
	job.sampleHandler(mysamplehandler)

	baseline_cuts = []#[]
	baseline_cuts += ["met>140"]
	baseline_cuts += ["NTRJigsawVars.RJVars_SS_MDeltaR/1000.>300"   ]
#        baseline_cuts += ["Length%(jetPt) >= 2"]
#        baseline_cuts += ["jetPt[0] > 50"]
#        baseline_cuts += ["jetPt[1] > 50"]
        baseline_cuts += ["NTRJigsawVars.RJVars_QCD_Rpt<0.4"]
        baseline_cuts += ["NTRJigsawVars.RJVars_QCD_Delta1>.05 * (1 - NTRJigsawVars.RJVars_QCD_Rpsib)"]

        cry_cuts = []
        cry_cuts.extend(baseline_cuts)

#        cry_cuts += ["NTRJigsawVars.RJVars_QCD_Delta1>*NTRJigsawVars.RJVars_QCD_Rpsib>-0.7"   ]
	#
	# cry_cuts += ["NTRJigsawVars.RJVars_G_0_Jet1_pT/1000.>150."   ]
	# cry_cuts += ["NTRJigsawVars.RJVars_G_1_Jet1_pT/1000.>150."   ]
	# cry_cuts += ["NTRJigsawVars.RJVars_G_0_Jet2_pT/1000.>110."   ]
	# cry_cuts += ["NTRJigsawVars.RJVars_G_1_Jet2_pT/1000.>110."   ]
	# cry_cuts += ["NTRJigsawVars.RJVars_G_0_PInvHS>0.25"   ]
	# cry_cuts += ["NTRJigsawVars.RJVars_G_1_PInvHS>0.25"   ]
	# cry_cuts += ["NTRJigsawVars.RJVars_dphiVG>0.3 && NTRJigsawVars.RJVars_dphiVG<2.7"   ]
	# cry_cuts += ["NTRJigsawVars.RJVars_C_0_CosTheta>-0.75 && NTRJigsawVars.RJVars_C_0_CosTheta<0.8"   ]
	# cry_cuts += ["NTRJigsawVars.RJVars_C_1_CosTheta>-0.75 && NTRJigsawVars.RJVars_C_1_CosTheta<0.8"   ]
	# cry_cuts += ["NTRJigsawVars.RJVars_G_0_CosTheta>-0.7 && NTRJigsawVars.RJVars_G_0_CosTheta<0.7"   ]
	# cry_cuts += ["NTRJigsawVars.RJVars_G_1_CosTheta>-0.7 && NTRJigsawVars.RJVars_G_1_CosTheta<0.7"   ]
	# cry_cuts += ["cos(NTRJigsawVars.RJVars_G_0_dPhiGC)>-0.8 && cos(NTRJigsawVars.RJVars_G_0_dPhiGC)<0.7"]
	# cry_cuts += ["cos(NTRJigsawVars.RJVars_G_1_dPhiGC)>-0.8 && cos(NTRJigsawVars.RJVars_G_1_dPhiGC)<0.7"]
	# cry_cuts += ["abs(NTRJigsawVars.RJVars_SS_CosTheta)<0.9"   ]
	# cry_cuts += ["NTRJigsawVars.RJVars_SS_VisShape>0.1"   ]
	# cry_cuts += ["NTRJigsawVars.RJVars_MG/1000.>800"   ]

	cry_limits = []
	cry_limits += [ (50,0,1000) ]  #["met>100"]
	cry_limits += [ (50,0,2000) ]  #["NTRJigsawVars.RJVars_SS_MDeltaR/1000.>300"   ]
	cry_limits += [ (50,0,500) ]  #["NTRJigsawVars.RJVars_G_0_Jet1_pT/1000.>150."   ]
	cry_limits += [ (50,0,500) ]  #["NTRJigsawVars.RJVars_G_1_Jet1_pT/1000.>150."   ]
	cry_limits += [ (50,0,500) ]  #["NTRJigsawVars.RJVars_G_0_Jet2_pT/1000.>110."   ]
	cry_limits += [ (50,0,500) ]  #["NTRJigsawVars.RJVars_G_1_Jet2_pT/1000.>110."   ]
	cry_limits += [ (50,0,1) ]  #["abs(NTRJigsawVars.RJVars_SS_CosTheta)<0.9"   ]
	cry_limits += [ (50,0,1) ]  #["NTRJigsawVars.RJVars_G_0_PInvHS>0.25 && NTRJigsawVars.RJVars_G_0_PInvHS<1"   ]
	cry_limits += [ (50,0,1) ]  #["NTRJigsawVars.RJVars_G_1_PInvHS>0.25 && NTRJigsawVars.RJVars_G_0_PInvHS<1"   ]
	cry_limits += [ (50,-1,1) ]  #["NTRJigsawVars.RJVars_G_0_CosTheta>-0.7 && NTRJigsawVars.RJVars_G_0_CosTheta<0.7"   ]
	cry_limits += [ (50,-1,1) ]  #["NTRJigsawVars.RJVars_G_1_CosTheta>-0.7 && NTRJigsawVars.RJVars_G_0_CosTheta<0.7"   ]
	cry_limits += [ (50,-1,1) ]  #["NTRJigsawVars.RJVars_C_0_CosTheta>-0.75 && NTRJigsawVars.RJVars_C_0_CosTheta<0.8"   ]
	cry_limits += [ (50,-1,1) ]  #["NTRJigsawVars.RJVars_C_1_CosTheta>-0.75 && NTRJigsawVars.RJVars_C_0_CosTheta<0.8"   ]
	cry_limits += [ (50,-1,1) ]  #["cos(NTRJigsawVars.RJVars_G_0_dPhiGC)>-0.8 && cos(NTRJigsawVars.RJVars_G_0_dPhiGC)<0.7"]
	cry_limits += [ (50,-1,1) ]  #["cos(NTRJigsawVars.RJVars_G_1_dPhiGC)>-0.8 && cos(NTRJigsawVars.RJVars_G_1_dPhiGC)<0.7"]
	cry_limits += [ (50,0,1) ]  #["NTRJigsawVars.RJVars_DeltaBetaGG>0.2" ]
	cry_limits += [ (50,0,4) ]  #["NTRJigsawVars.RJVars_dphiVG>0.3 && NTRJigsawVars.RJVars_dphiVG<2.7"   ]
	cry_limits += [ (50,0,1) ]  #["NTRJigsawVars.RJVars_QCD_Rpt<0.3"]
	cry_limits += [ (50,-1,1) ]  #["NTRJigsawVars.RJVars_QCD_Delta1*NTRJigsawVars.RJVars_QCD_Rpsib>-0.7"   ]
	cry_limits += [ (50,0,1) ]  #visshape
	cry_limits += [ (50,0,2000) ]  #["NTRJigsawVars.RJVars_QCD_Delta1*NTRJigsawVars.RJVars_QCD_Rpsib>-0.7"   ]


	## Define your cut strings here....
	cuts = {
		# "no_cut": "(NTRJigsawVars.RJVars_G_0_Jet1_pT/1000. > 250)",
		# "l1trigger": "(NTVars.nJet>1 && met > 100)",
#		"hlttrigger": "(NTVars.nJet>1 && met > 100)*(NTRJigsawVars.RJVars_SS_MDeltaR/1000.>300)",
#		"sirop_1200_800": "*".join( ["(%s)"%mycut for mycut in sirop_1200_800_cuts ]),
		"sirop_tight": "*".join( ["(%s)"%mycut for mycut in cry_cuts ])
	}


	#################################################################################################

	## This part sets up both N-1 hists and the cutflow histogram for "sirop_tight"

	cutflow = ROOT.TH1F ("cutflow", "cutflow", len(cry_cuts)+1 , 0, len(cry_cuts)+1 );
	cutflow.GetXaxis().SetBinLabel (1, "NTVars.eventWeight");

	for i,cutpart in enumerate(cry_cuts):

		cutpartname = cutpart.split("/")[0].replace("*","x").split("<")[0].split(">")[0]
		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("sirop_tight_minus_%s"%cutpartname, "sirop_tight_%s"%cutpartname, cry_limits[i][0], cry_limits[i][1], cry_limits[i][2] ),
			cutpart.split("<")[0].split(">")[0],
			"NTVars.eventWeight*%s"%("*".join( ["(%s)"%mycut for mycut in cry_cuts if  mycut!=cutpart ]))    )        )

		cutflow.GetXaxis().SetBinLabel (i+2, cutpart);

	job.algsAdd(ROOT.MD.AlgCFlow (cutflow))


	#################################################################################################

	for cut in cuts:
                print cut
		## each of this histograms will be made for each cut

		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("jet1pt_%s"%cut, "jet1pt_%s"%cut, 100, 0, 1000),
			"jetPt[0]",
			"NTVars.eventWeight*%s"%cuts[cut]))
		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("jet2pt_%s"%cut, "jet2pt_%s"%cut, 100, 0, 1000),
			"jetPt[1]",
			"NTVars.eventWeight*%s"%cuts[cut]))
		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("met_%s"%cut, "met_%s"%cut, 100, 0, 1000),
			"met",
			"NTVars.eventWeight*%s"%cuts[cut]))
		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("nJet_%s"%cut, "nJet_%s"%cut, 20, 0, 20),
			"NTVars.nJet",
			"NTVars.eventWeight*%s"%cuts[cut]))
		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("RJVars_SS_Mass_%s"%cut, "RJVars_SS_Mass_%s"%cut, 100, 0, 6000),
			"NTRJigsawVars.RJVars_SS_Mass/1000.",
			"NTVars.eventWeight*%s"%cuts[cut]))
		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("RJVars_SS_MDeltaR_%s"%cut, "RJVars_SS_MDeltaR_%s"%cut, 100, 0, 2000),
			"NTRJigsawVars.RJVars_SS_MDeltaR/1000.",
			"NTVars.eventWeight*%s"%cuts[cut]))
		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("RJVars_MG_%s"%cut, "RJVars_MG_%s"%cut, 100, 0, 2000),
			"NTRJigsawVars.RJVars_MG/1000.",
			"NTVars.eventWeight*%s"%cuts[cut]))
		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("RJVars_G_0_PInvHS_%s"%cut, "RJVars_G_0_PInvHS_%s"%cut, 100, -1, 1),
			"NTRJigsawVars.RJVars_G_0_PInvHS",
			"NTVars.eventWeight*%s"%cuts[cut]))

		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("RJVars_G_0_CosTheta_%s"%cut, "RJVars_G_0_CosTheta_%s"%cut, 100, -1, 1),
			"NTRJigsawVars.RJVars_G_0_CosTheta",
			"NTVars.eventWeight*%s"%cuts[cut]))
		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("RJVars_G_0_Jet2_pT_%s"%cut, "RJVars_G_0_Jet2_pT_%s"%cut, 100, -1, 1000),
			"NTRJigsawVars.RJVars_G_0_Jet2_pT/1000.",
			"NTVars.eventWeight*%s"%cuts[cut]))
		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("RJVars_SS_CosTheta_%s"%cut, "RJVars_SS_CosTheta_%s"%cut, 100, -1, 1),
			"NTRJigsawVars.RJVars_SS_CosTheta",
			"NTVars.eventWeight*%s"%cuts[cut]))
		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("RJVars_DeltaBetaGG_%s"%cut, "RJVars_DeltaBetaGG_%s"%cut, 100, 0, 1),
			"NTRJigsawVars.RJVars_DeltaBetaGG",
			"NTVars.eventWeight*%s"%cuts[cut]))
		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("RJVars_dphiVG_%s"%cut, "RJVars_dphiVG_%s"%cut, 100, 0, 4),
			"NTRJigsawVars.RJVars_dphiVG",
			"NTVars.eventWeight*%s"%cuts[cut]))
		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("RJVars_QCD_Rpt_%s"%cut, "RJVars_QCD_Rpt_%s"%cut, 100, 0, 1),
			"NTRJigsawVars.RJVars_QCD_Rpt",
			"NTVars.eventWeight*%s"%cuts[cut]))
		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("RJVars_QCD_Delta2_%s"%cut, "RJVars_QCD_Delta2_%s"%cut, 100, -1, 1),
			"NTRJigsawVars.RJVars_QCD_Delta2",
			"NTVars.eventWeight*%s"%cuts[cut]))
		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("RJVars_QCD_Delta1_x_Rpsib_%s"%cut, "RJVars_QCD_Delta1_x_Rpsib_%s"%cut, 100, -1, 1),
			"(NTRJigsawVars.RJVars_QCD_Delta1)*(NTRJigsawVars.RJVars_QCD_Rpsib)",
			"NTVars.eventWeight*%s"%cuts[cut]))

		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("cosNTRJigsawVars.RJVars_G_1_dPhiGC_%s"%cut, "cosNTRJigsawVars.RJVars_G_1_dPhiGC_%s"%cut, 100, -1, 1),
			"cos(NTRJigsawVars.RJVars_G_1_dPhiGC)",
			"NTVars.eventWeight*%s"%cuts[cut]))
		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("meffInc_%s"%cut, "meffInc_%s"%cut, 100, 0, 3000),
			"NTVars.meffInc",
			"NTVars.eventWeight*%s"%cuts[cut]))

		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("Ap_%s"%cut, "Ap_%s"%cut, 100, 0, 1),
			"NTExtraVars.Ap",
			"NTVars.eventWeight*%s"%cuts[cut]))


	driver = ROOT.EL.DirectDriver()
	if os.path.exists( tempDirDict[mysamplehandlername] ):
		shutil.rmtree( tempDirDict[mysamplehandlername] )
        print "submitting to dir : " + tempDirDict[mysamplehandlername]
	driver.submit(job, tempDirDict[mysamplehandlername] )

        mysamplehandler.printContent()
#	if mysamplehandler!=sh_data:
        scaleMyRootFiles(mysamplehandlername,lumi)
        os.system('hadd -f %s.root %s/hist*root*'%(tempDirDict[mysamplehandlername] ,tempDirDict[mysamplehandlername] ) )

#	if mysamplehandler!=sh_signal:





