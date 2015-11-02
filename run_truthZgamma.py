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
search_directories = ["/afs/cern.ch/work/r/rsmith/photonTruthStudies_v3/"]

##
##
########### Gather input ######################################
##
##

logging.info("creating new sample handler")
sh_all = ROOT.SH.SampleHandler()

discoverInput.discover(sh_all, search_directories)

sh_all.setMetaString("nc_tree", "CRY_SRAllNT")

ROOT.SH.readSusyMeta(sh_all,"optimization/susy_crosssections_13TeV.txt")

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
#sh_bg["znunu_nlo"] = sh_all.find("znunu_nlo")

sh_bg["gamma"]   .setMetaString("nc_tree","CRY_SRAllNT")
sh_bg["znunu_lo"].setMetaString("nc_tree","SRAllNT")

print sh_bg
sh_bg["gamma"]    .printContent()
sh_bg["znunu_lo" ].printContent()
#sh_bg["znunu_nlo"].printContent()

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
                mychain = sample.makeTChain()
                print sample
                print mychain.GetEntries()
#                print mychain.Print()
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

        no_cuts = {}
	no_cuts["1"] = [50,0,1000]
#	no_cuts["met>0."] = [50,0,1000]

	baseline_cuts = no_cuts.copy()#[]
	baseline_cuts["met>140"]                                         = [50,0,1000]
        baseline_cuts["NTRJigsawVars.RJVars_PP_MDeltaR/1000.>300."]      = [50,0,2000]
        baseline_cuts["NTRJigsawVars.RJVars_QCD_Rpt<.4"]                 = [50,-1,1]
        baseline_cuts["NTRJigsawVars.RJVars_QCD_Delta1 / (1 - NTRJigsawVars.RJVars_QCD_Rsib) > .05"] = [50,-1,1]
#       baseline_cuts["jetPt[0] > 50"]                                                             = [50,0,500]
#       baseline_cuts["jetPt[1] > 50"]                                                             = [50,0,500]
#        baseline_cuts["NTRJigsawVars.RJVars_QCD_Rpt<0.4"]                                          = [50,-1,1]
#        baseline_cuts["NTRJigsawVars.RJVars_QCD_Delta1/1000./(1 - NTRJigsawVars.RJVars_QCD_Rsib/1000.)>.05"] = [50,-1,1]

        cry_cuts = baseline_cuts.copy()
        print cry_cuts
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
	# cry_cuts += ["abs(NTRJigsawVars.RJVars_PP_CosTheta)<0.9"   ]
	# cry_cuts += ["NTRJigsawVars.RJVars_PP_VisShape>0.1"   ]
	# cry_cuts += ["NTRJigsawVars.RJVars_MG/1000.>800"   ]

	# cry_limits = []
	# cry_limits += [ (50,0,1000) ]  #["met>100"]
	# cry_limits += [ (50,0,2000) ]  #["NTRJigsawVars.RJVars_PP_MDeltaR/1000.>300"   ]
	# cry_limits += [ (50,0,500) ]  #["NTRJigsawVars.RJVars_G_0_Jet1_pT/1000.>150."   ]
	# cry_limits += [ (50,0,500) ]  #["NTRJigsawVars.RJVars_G_1_Jet1_pT/1000.>150."   ]
	# cry_limits += [ (50,0,500) ]  #["NTRJigsawVars.RJVars_G_0_Jet2_pT/1000.>110."   ]
	# cry_limits += [ (50,0,500) ]  #["NTRJigsawVars.RJVars_G_1_Jet2_pT/1000.>110."   ]
	# cry_limits += [ (50,0,1) ]  #["abs(NTRJigsawVars.RJVars_PP_CosTheta)<0.9"   ]
	# cry_limits += [ (50,0,1) ]  #["NTRJigsawVars.RJVars_G_0_PInvHS>0.25 && NTRJigsawVars.RJVars_G_0_PInvHS<1"   ]
	# cry_limits += [ (50,0,1) ]  #["NTRJigsawVars.RJVars_G_1_PInvHS>0.25 && NTRJigsawVars.RJVars_G_0_PInvHS<1"   ]
	# cry_limits += [ (50,-1,1) ]  #["NTRJigsawVars.RJVars_G_0_CosTheta>-0.7 && NTRJigsawVars.RJVars_G_0_CosTheta<0.7"   ]
	# cry_limits += [ (50,-1,1) ]  #["NTRJigsawVars.RJVars_G_1_CosTheta>-0.7 && NTRJigsawVars.RJVars_G_0_CosTheta<0.7"   ]
	# cry_limits += [ (50,-1,1) ]  #["NTRJigsawVars.RJVars_C_0_CosTheta>-0.75 && NTRJigsawVars.RJVars_C_0_CosTheta<0.8"   ]
	# cry_limits += [ (50,-1,1) ]  #["NTRJigsawVars.RJVars_C_1_CosTheta>-0.75 && NTRJigsawVars.RJVars_C_0_CosTheta<0.8"   ]
	# cry_limits += [ (50,-1,1) ]  #["cos(NTRJigsawVars.RJVars_G_0_dPhiGC)>-0.8 && cos(NTRJigsawVars.RJVars_G_0_dPhiGC)<0.7"]
	# cry_limits += [ (50,-1,1) ]  #["cos(NTRJigsawVars.RJVars_G_1_dPhiGC)>-0.8 && cos(NTRJigsawVars.RJVars_G_1_dPhiGC)<0.7"]
	# cry_limits += [ (50,0,1) ]  #["NTRJigsawVars.RJVars_DeltaBetaGG>0.2" ]
	# cry_limits += [ (50,0,4) ]  #["NTRJigsawVars.RJVars_dphiVG>0.3 && NTRJigsawVars.RJVars_dphiVG<2.7"   ]
	# cry_limits += [ (50,0,1) ]  #["NTRJigsawVars.RJVars_QCD_Rpt<0.3"]
	# cry_limits += [ (50,-1,1) ]  #["NTRJigsawVars.RJVars_QCD_Delta1*NTRJigsawVars.RJVars_QCD_Rpsib>-0.7"   ]
	# cry_limits += [ (50,0,1) ]  #visshape
	# cry_limits += [ (50,0,2000) ]  #["NTRJigsawVars.RJVars_QCD_Delta1*NTRJigsawVars.RJVars_QCD_Rpsib>-0.7"   ]

	## Define your cut strings here....
	cuts = {
		# "no_cut": "(NTRJigsawVars.RJVars_G_0_Jet1_pT/1000. > 250)",
		# "l1trigger": "(NTVars.nJet>1 && met > 100)",
#		"hlttrigger": "(NTVars.nJet>1 && met > 100)*(NTRJigsawVars.RJVars_PP_MDeltaR/1000.>300)",
#		"cry_1200_800": "*".join( ["(%s)"%mycut for mycut in cry_1200_800_cuts ]),
		"cry_tight": "*".join( ["(%s)"%mycut for mycut in cry_cuts.keys() ]),
		"no_cuts"  : "*".join( ["(%s)"%mycut for mycut in no_cuts .keys() ])
	}


	#################################################################################################

	## This part sets up both N-1 hists and the cutflow histogram for "cry_tight"

	cutflow = ROOT.TH1F ("cutflow", "cutflow", len(cry_cuts.keys())+1 , 0, len(cry_cuts.keys())+1 );
	cutflow.GetXaxis().SetBinLabel (1, "NTVars.eventWeight");

	for i,cutpart in enumerate(cry_cuts.keys()):

		cutpartname = cutpart.split("/")[0].replace("*","x").split("<")[0].split(">")[0]
		job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("cry_tight_minus_%s"%cutpartname, "cry_tight_%s"%cutpartname, cry_cuts.values()[i][0], cry_cuts.values()[i][1], cry_cuts.values()[i][2] ),
			cutpart.split("<")[0].split(">")[0],
			"NTVars.eventWeight*%s"%("*".join( ["(%s)"%mycut for mycut in cry_cuts.keys() if  mycut!=cutpart ]))    )        )

		cutflow.GetXaxis().SetBinLabel (i+2, cutpart);

	job.algsAdd(ROOT.MD.AlgCFlow (cutflow))

#include all these
        RJigsawVariables = {
            "RJVars_PP_MDeltaR"        :  [100, 0 , 1000, True],
            "RJVars_PP_Mass"           :  [100, 0 , 1000, True],
            "RJVars_PP_InvGamma"       :  [100, -1 , 1, False ],
            "RJVars_PP_dPhiBetaR"      :  [100, -1 , 1, False ],
            "RJVars_PP_dPhiVis"        :  [100, -1 , 1, False ],
            "RJVars_PP_CosTheta"       :  [100, -1 , 1, False ],
            "RJVars_PP_dPhiDecayAngle" :  [100, -1 , 1, False ],
            "RJVars_PP_VisShape"       :  [100, 0  , 1, False ],
            "RJVars_P1_Mass"           :  [100, 0 , 1000, True],
            "RJVars_P1_CosTheta"       :  [100, -1 , 1, False ],
            "RJVars_P2_Mass"           :  [100, 0 , 1000, True],
            "RJVars_P2_CosTheta"       :  [100, -1 , 1, False ],
#            "RJVars_I1_Depth"          :  [100, 0 , 1000,False],
#            "RJVars_I2_Depth"          :  [100, 0 , 1000,False],
            "RJVars_dphiPV1a"  :  [100, -1 , 1, False ],
            "RJVars_cosV1a"    :  [100, -1 , 1, False ],
            "RJVars_dphiCV2a"  :  [100, -1 , 1, False ],
            "RJVars_cosV2a"    :  [100, -1 , 1, False ],
            "RJVars_dphiPV1b" :  [100, -1 , 1, False ],
            "RJVars_cosV1b"   :  [100, -1 , 1, False ],
            "RJVars_dphiCV2b" :  [100, -1 , 1, False ],
            "RJVars_cosV2b":  [100, -1 , 1, False ],
            "RJVars_V1_N" :  [20, 0 , 20, False],
            "RJVars_V2_N" :  [20, 0 , 20, False],
            "RJVars_MP"          :  [100, 0 , 1000, True],
            "RJVars_DeltaBetaGG" :  [100, -1 , 1, False ],
            "RJVars_dphiVG"      :  [100, -1 , 1, False ],
            "RJVars_QCD_dPhiR"    :  [100, -1 , 1, False ],
            "RJVars_QCD_Rpt"      :  [100, -1 , 1, False ],
            "RJVars_QCD_Rsib"    :  [100, -1 , 1, False ],
            "RJVars_QCD_Delta1"   :  [100, -1 , 1, False ],
            "RJVars_H2PP":  [100, 0 , 4000, True],
            "RJVars_H3PP":  [100, 0 , 4000, True],
            "RJVars_H4PP":  [100, 0 , 4000, True],
            "RJVars_H6PP":  [100, 0 , 4000, True],
            "RJVars_H2Pa":  [100, 0 , 4000, True],
            "RJVars_H2Pb":  [100, 0 , 4000, True],
            "RJVars_H3Pa":  [100, 0 , 4000, True],
            "RJVars_H3Pb":  [100, 0 , 4000, True],
            "RJVars_H4Pa":  [100, 0 , 4000, True],
            "RJVars_H4Pb":  [100, 0 , 4000, True],
            "RJVars_H5Pa":  [100, 0 , 4000, True],
            "RJVars_H5Pb":  [100, 0 , 4000, True],
            "RJVars_H2Ca":  [100, 0 , 4000, True],
            "RJVars_H2Cb":  [100, 0 , 4000, True],
            "RJVars_H3Ca":  [100, 0 , 4000, True],
            "RJVars_H3Cb":  [100, 0 , 4000, True],
            "RJVars_HT4PP":  [100, 0 , 4000, True],
            "RJVars_HT6PP":  [100, 0 , 4000, True],
            "RJVars_minH3P":  [100, 0 , 4000, True],
            "RJVars_sangle":  [100, -1 , 1, False],
            "RJVars_dangle":  [100, -1 , 1, False ],
            "RJVars_ddphiPC":  [100, -1 , 1, False ],
            "RJVars_sdphiPC":  [100, -1 , 1, False ],
            "RJVars_dH2o3P":  [100, -1 , 1, True],
            "RJVars_RPZ_HT4PP":  [100, -1 , 1, False],
            "RJVars_RPZ_HT6PP":  [100, -1 , 1, False ],
            }
	#################################################################################################


        for cut in cuts:
            cutstring = "NTVars.eventWeight*%s"%cuts[cut]
#            cutstring = "1."
            for varname,limits in RJigsawVariables.items() :
		print varname
                print cutstring
                job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F(varname+"_%s"%cut,
                                                       varname+"_%s"%cut,
                                                       limits[0],
                                                       limits[1],
                                                       limits[2]
                                                       ),
                                                       #100, 0, 1000),#todo make this use the other half of the dictionary
                                             "NTRJigsawVars."+varname+"/1000." if limits[3] else  "NTRJigsawVars."+varname,
                                             cutstring
                                             )
                             )



	driver = ROOT.EL.DirectDriver()
#        driver = ROOT.EL.ProofDriver()
#        driver.numWorkers = 8

	if os.path.exists( tempDirDict[mysamplehandlername] ):
		shutil.rmtree( tempDirDict[mysamplehandlername] )
        print "submitting to dir : " + tempDirDict[mysamplehandlername]
	driver.submit(job, tempDirDict[mysamplehandlername] )



        mysamplehandler.printContent()
#	if mysamplehandler!=sh_data:
        scaleMyRootFiles(mysamplehandlername,lumi)
        os.system('hadd -f %s.root %s/hist*root*'%(tempDirDict[mysamplehandlername] ,tempDirDict[mysamplehandlername] ) )

#	if mysamplehandler!=sh_signal:





