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
ROOT.TH1.SetDefaultSumw2(True)

logging.basicConfig(level=logging.INFO)
from optparse import OptionParser

parser = OptionParser()
parser.add_option("--driver"      , help="select where to run", choices=("direct","lsf", "prooflite", "grid", "condor"), default="direct")
parser.add_option('--isTest', action="store_true", default=False)
parser.add_option('--dryRun', action="store_true", default=False)
#parser.add_argument('--no-isTest', dest='isTest', action='store_false')
parser.add_option("--samplesToRun", help="Run a subset of samples. Note we need to do this for the LSF driver as things are", choices=("znunu_lo","gamma","both")         , default="both")
#parser.add_option("--nevents", type=int, help="number of events to process for all the datasets")
#parser.add_option("--skip-events", type=int, help="skip the first n events")
#parser.add_option("--runTag", help="", default="Test_XXYYZZa")

(options, args) = parser.parse_args()

import atexit
@atexit.register
def quiet_exit():
    ROOT.gSystem.Exit(0)

def cuts_from_dict(cutdict):
    return "*".join( ["(%s)"%mycut for mycut in cutdict.keys() ])

logging.info("loading packages")
ROOT.gROOT.Macro("$ROOTCOREDIR/scripts/load_packages.C")

##
##
########### Configuration ######################################
##
##

lumi = 3.5  ## in pb-1
search_directories = ["/afs/cern.ch/work/r/rsmith/photonTruthStudies/"]
import os
if os.getenv('USER')=='khoo':
    search_directories = ["/r04/atlas/khoo/Data_2015/zeroleptonRJR/truth.vvFast/"]
#search_directories = ["test/"]

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
    tempDirDict[key] = "rundir_truth_" + key

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
                        if h1.ClassName() == "TH1D" or h1.ClassName() == "TH2D":
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

        met50 = no_cuts.copy()
        met50["met>50"] = [50,0,1000]

        met100 = no_cuts.copy()
        met100["met>100"] = [50,0,1000]

        met160 = no_cuts.copy()
        met160["met>160"] = [50,0,1000]

        met300 = no_cuts.copy()
        met300["met>300"] = [50,0,1000]

        met50_2jet = no_cuts.copy()
        met50_2jet["met>50"] = [50,0,1000]
        met50_2jet["NTRJigsawVars.PP_MDeltaR>0.1"] = [40,0,2000]

        met100_2jet = no_cuts.copy()
        met100_2jet["met>100"] = [50,0,1000]
        met100_2jet["NTRJigsawVars.PP_MDeltaR>0.1"] = [40,0,2000]

        met300_2jet = no_cuts.copy()
        met300_2jet["met>300"] = [50,0,1000]
        met300_2jet["NTRJigsawVars.PP_MDeltaR>0.1"] = [40,0,2000]

	baseline_cuts = no_cuts.copy()#[]
	baseline_cuts["met>140"]                                         = [50,0,1000]
        baseline_cuts["NTRJigsawVars.PP_MDeltaR/1000.>300."]      = [50,0,2000]
        baseline_cuts["NTRJigsawVars.RPT_HT5PP<.4"]                 = [50,-1,1]
        baseline_cuts["NTRJigsawVars.QCD_Delta1 / (1 - NTRJigsawVars.QCD_Rsib) > .05"] = [50,-1,1]
#       baseline_cuts["jetPt[0] > 50"]                                                             = [50,0,500]
#       baseline_cuts["jetPt[1] > 50"]                                                             = [50,0,500]
#        baseline_cuts["NTRJigsawVars.RPT_HT5PP<0.4"]                                          = [50,-1,1]
#        baseline_cuts["NTRJigsawVars.QCD_Delta1/1000./(1 - NTRJigsawVars.QCD_Rsib/1000.)>.05"] = [50,-1,1]

        cry_cuts = baseline_cuts.copy()
        print cry_cuts
#        cry_cuts += ["NTRJigsawVars.QCD_Delta1>*NTRJigsawVars.QCD_Rpsib>-0.7"   ]
	#
	# cry_cuts += ["NTRJigsawVars.G_0_Jet1_pT/1000.>150."   ]
	# cry_cuts += ["NTRJigsawVars.G_1_Jet1_pT/1000.>150."   ]
	# cry_cuts += ["NTRJigsawVars.G_0_Jet2_pT/1000.>110."   ]
	# cry_cuts += ["NTRJigsawVars.G_1_Jet2_pT/1000.>110."   ]
	# cry_cuts += ["NTRJigsawVars.G_0_PInvHS>0.25"   ]
	# cry_cuts += ["NTRJigsawVars.G_1_PInvHS>0.25"   ]
	# cry_cuts += ["NTRJigsawVars.dphiVG>0.3 && NTRJigsawVars.dphiVG<2.7"   ]
	# cry_cuts += ["NTRJigsawVars.C_0_CosTheta>-0.75 && NTRJigsawVars.C_0_CosTheta<0.8"   ]
	# cry_cuts += ["NTRJigsawVars.C_1_CosTheta>-0.75 && NTRJigsawVars.C_1_CosTheta<0.8"   ]
	# cry_cuts += ["NTRJigsawVars.G_0_CosTheta>-0.7 && NTRJigsawVars.G_0_CosTheta<0.7"   ]
	# cry_cuts += ["NTRJigsawVars.G_1_CosTheta>-0.7 && NTRJigsawVars.G_1_CosTheta<0.7"   ]
	# cry_cuts += ["cos(NTRJigsawVars.G_0_dPhiGC)>-0.8 && cos(NTRJigsawVars.G_0_dPhiGC)<0.7"]
	# cry_cuts += ["cos(NTRJigsawVars.G_1_dPhiGC)>-0.8 && cos(NTRJigsawVars.G_1_dPhiGC)<0.7"]
	# cry_cuts += ["abs(NTRJigsawVars.PP_CosTheta)<0.9"   ]
	# cry_cuts += ["NTRJigsawVars.PP_VisShape>0.1"   ]
	# cry_cuts += ["NTRJigsawVars.MG/1000.>800"   ]

	# cry_limits = []
	# cry_limits += [ (50,0,1000) ]  #["met>100"]
	# cry_limits += [ (50,0,2000) ]  #["NTRJigsawVars.PP_MDeltaR/1000.>300"   ]
	# cry_limits += [ (50,0,500) ]  #["NTRJigsawVars.G_0_Jet1_pT/1000.>150."   ]
	# cry_limits += [ (50,0,500) ]  #["NTRJigsawVars.G_1_Jet1_pT/1000.>150."   ]
	# cry_limits += [ (50,0,500) ]  #["NTRJigsawVars.G_0_Jet2_pT/1000.>110."   ]
	# cry_limits += [ (50,0,500) ]  #["NTRJigsawVars.G_1_Jet2_pT/1000.>110."   ]
	# cry_limits += [ (50,0,1) ]  #["abs(NTRJigsawVars.PP_CosTheta)<0.9"   ]
	# cry_limits += [ (50,0,1) ]  #["NTRJigsawVars.G_0_PInvHS>0.25 && NTRJigsawVars.G_0_PInvHS<1"   ]
	# cry_limits += [ (50,0,1) ]  #["NTRJigsawVars.G_1_PInvHS>0.25 && NTRJigsawVars.G_0_PInvHS<1"   ]
	# cry_limits += [ (50,-1,1) ]  #["NTRJigsawVars.G_0_CosTheta>-0.7 && NTRJigsawVars.G_0_CosTheta<0.7"   ]
	# cry_limits += [ (50,-1,1) ]  #["NTRJigsawVars.G_1_CosTheta>-0.7 && NTRJigsawVars.G_0_CosTheta<0.7"   ]
	# cry_limits += [ (50,-1,1) ]  #["NTRJigsawVars.C_0_CosTheta>-0.75 && NTRJigsawVars.C_0_CosTheta<0.8"   ]
	# cry_limits += [ (50,-1,1) ]  #["NTRJigsawVars.C_1_CosTheta>-0.75 && NTRJigsawVars.C_0_CosTheta<0.8"   ]
	# cry_limits += [ (50,-1,1) ]  #["cos(NTRJigsawVars.G_0_dPhiGC)>-0.8 && cos(NTRJigsawVars.G_0_dPhiGC)<0.7"]
	# cry_limits += [ (50,-1,1) ]  #["cos(NTRJigsawVars.G_1_dPhiGC)>-0.8 && cos(NTRJigsawVars.G_1_dPhiGC)<0.7"]
	# cry_limits += [ (50,0,1) ]  #["NTRJigsawVars.DeltaBetaGG>0.2" ]
	# cry_limits += [ (50,0,4) ]  #["NTRJigsawVars.dphiVG>0.3 && NTRJigsawVars.dphiVG<2.7"   ]
	# cry_limits += [ (50,0,1) ]  #["NTRJigsawVars.RPT_HT5PP<0.3"]
	# cry_limits += [ (50,-1,1) ]  #["NTRJigsawVars.QCD_Delta1*NTRJigsawVars.QCD_Rpsib>-0.7"   ]
	# cry_limits += [ (50,0,1) ]  #visshape
	# cry_limits += [ (50,0,2000) ]  #["NTRJigsawVars.QCD_Delta1*NTRJigsawVars.QCD_Rpsib>-0.7"   ]

	## Define your cut strings here....
	cuts = {
		# "no_cut": "(NTRJigsawVars.G_0_Jet1_pT/1000. > 250)",
		# "l1trigger": "(NTVars.nJet>1 && met > 100)",
#		"hlttrigger": "(NTVars.nJet>1 && met > 100)*(NTRJigsawVars.PP_MDeltaR/1000.>300)",
#		"cry_1200_800": "*".join( ["(%s)"%mycut for mycut in cry_1200_800_cuts ]),
		"cry_tight"   : cuts_from_dict(cry_cuts),
		"no_cuts"     : cuts_from_dict(no_cuts),
		"met50"       : cuts_from_dict(met50),
		"met100"      : cuts_from_dict(met100),
		"met160"      : cuts_from_dict(met160),
		"met300"      : cuts_from_dict(met300),
		"met50_2jet"  : cuts_from_dict(met50_2jet),
		"met100_2jet" : cuts_from_dict(met100_2jet),
		"met300_2jet" : cuts_from_dict(met300_2jet)
                }


	#################################################################################################

	## This part sets up both N-1 hists and the cutflow histogram for "cry_tight"

	cutflow = ROOT.TH1D ("cutflow", "cutflow", len(cry_cuts.keys())+1 , 0, len(cry_cuts.keys())+1 );
	cutflow.GetXaxis().SetBinLabel (1, "NTVars.eventWeight");
        
	for i,cutpart in enumerate(cry_cuts.keys()):
            
            cutpartname = cutpart.split("/")[0].replace("*","x").split("<")[0].split(">")[0]
            job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1D("cry_tight_minus_%s"%cutpartname, "cry_tight_%s"%cutpartname, cry_cuts.values()[i][0], cry_cuts.values()[i][1], cry_cuts.values()[i][2] ),
                                         cutpart.split("<")[0].split(">")[0],
                                         "NTVars.eventWeight*%s"%("*".join( ["(%s)"%mycut for mycut in cry_cuts.keys() if  mycut!=cutpart ]))    )        )

            cutflow.GetXaxis().SetBinLabel (i+2, cutpart);

	job.algsAdd(ROOT.MD.AlgCFlow (cutflow))

#include all these
        RJigsawVariables = {
            "HT1CM"                  :  [100, 0 , 5000, True],
            }
        if not options.isTest :
            RJigsawVariables = {
            "HT1CM"                  :  [100, 0 , 5000, True],
            "PIoHT1CM"               :  [100, 0 , 1, False ],
            "cosS"                   :  [100, -1 , 1, False ],
            "NVS"                    :  [10,  0 , 10, False ],
            "RPT_HT1CM"              :  [100, 0 , 1, False ],
            "MS"                     :  [100,  0, 5000, True ],
            "ddphiP"                 :  [100, -1 , 1, False ],
            "sdphiP"                 :  [100, 0 , 1, False ],
            "pPP_Ia"                 :  [100, 0 , 5000, True],
            "pPP_Ib"                 :  [100, 0 , 5000, True ],
            "pT_jet1a"               :  [100, 0 , 2500, True ],
            "pT_jet1b"               :  [100, 0 , 2500, True ],
            "pT_jet2a"               :  [100, 0 , 2500, True ],
            "pT_jet2b"               :  [100, 0 , 2500, True ],
            "pTPP_jet1"              :  [100, 0 , 5000, True ],
            "pTPP_jet2"              :  [100, 0 , 5000, True ],
            "pTPP_jet1a"             :  [100, 0 , 5000, True ],
            "pTPP_jet1b"             :  [100, 0 , 5000, True ],
            "pTPP_jet2a"             :  [100, 0 , 2500, True ],
            "pTPP_jet2b"             :  [100, 0 , 2500, True ],
            "pTPP_jet3a"             :  [100, 0 , 2500, True ],
            "pTPP_jet3b"             :  [100, 0 , 2500, True ],
            "pPP_jet1a"              :  [100, 0 , 5000, True ],
            "pPP_jet1b"              :  [100, 0 , 5000, True ],
            "pPP_jet2a"              :  [100, 0 , 2500, True ],
            "pPP_jet2b"              :  [100, 0 , 2500, True ],
            "pPP_jet3a"              :  [100, 0 , 2500, True ],
            "pPP_jet3b"              :  [100, 0 , 2500, True ],
            "R_H2PP_H3PP"            :  [100, 0 , 1, False ],
            "R_pTj2_HT3PP"           :  [100, 0 , 1, False ],
            "R_HT5PP_H5PP"           :  [100, 0 , 1, False ],
            "R_H2PP_H5PP"            :  [100, 0 , 1, False],
            "minR_pTj2i_HT3PPi"      :  [100, 0 , 1, False],
            "maxR_H1PPi_H2PPi"       :  [100, 0 , 1, False],
            "R_HT9PP_H9PP"           :  [100, 0 , 1, False],
            "R_H2PP_H9PP"            :  [100, 0 , 1, False],
            "RPZ_HT3PP"              :  [100, 0 , 1, False],
            "RPZ_HT5PP"              :  [100, 0 , 1, False],
            "RPZ_HT9PP"              :  [100, 0 , 1, False],
            "RPT_HT3PP"              :  [100, 0 , 1, False],
            "RPT_HT5PP"              :  [100, 0 , 1, False],
            "RPT_HT9PP"              :  [100, 0 , 1, False],
            "PP_InvGamma"            :  [100, 0 , 1, False],
            "PP_dPhiBetaR"           :  [64, -3.2 , 3.2, False],
            "PP_dPhiVis"             :  [64, 0 , 3.2, False],
            "PP_CosTheta"            :  [100, -1 , 1, False],
            "PP_dPhiDecayAngle"      :  [100, -1 ,  1, False],
            "PP_VisShape"            :  [100, 0 , 1, True],
            "PP_MDeltaR"             :  [100, 0 , 2000, True],
            "P1_Mass"                :  [100, 0 , 2000, True],
            "P1_CosTheta"            :  [100, -1 , 1, False],
            "P2_Mass"                :  [100, 0 , 2000, False ],
            "P2_CosTheta"            :  [100, -1 , 1, False ],
            #"I1_Depth"               :  [100, 0 , 10, False ],
            #"I2_Depth"               :  [100, 0 , 10, True],
            "dphiPV1a"               :  [64, 0, 6.4, False],
            "cosV1a"                 :  [100, -1 , 1, False ],
            "dphiCV2a"               :  [64, 0 , 6.4, False],
            "cosV2a"                 :  [100, -1 , 1, False],
            "dphiPV1b"               :  [64, 0 , 6.4, False ],
            "cosV1b"                 :  [100, -1 , 1, False ],
            "dphiCV2b"               :  [64, 0 , 6.4, False ],
            "cosV2b"                 :  [100, -1 , 1, False ],
            "NJa"                    :  [10, 0 , 10, False ],
            "NJb"                    :  [10, 0 , 10, False ],
            "dphiVG"                 :  [100, 0. , 3.2, False ],
#            "QCD_dPhiR"              :  [100, -1 , 1, False ], # always -100
            "QCD_Rsib"               :  [100, 0 , 1, False ],
            "QCD_Delta1"             :  [100, -1 , 1, False ],
            "H2PP"                   :  [100, 0 , 5000, True ],
            "H3PP"                   :  [100, 0 , 5000, True ],
            "H4PP"                   :  [100, 0 , 5000, True ],
            "H6PP"                   :  [100, 0 , 5000, True ],
            "H10PP"                  :  [100, 0 , 5000, True ],
            "HT10PP"                 :  [100, 0 , 5000, True ],
            "H2Pa"                   :  [100, 0 , 5000, True ],
            "H2Pb"                   :  [100, 0 , 5000, True ],
            "H3Pa"                   :  [100, 0 , 5000, True ],
            "H3Pb"                   :  [100, 0 , 5000, True ],
            "H4Pa"                   :  [100, 0 , 5000, True],
            "H4Pb"                   :  [100, 0 , 5000, True],
            "H5Pa"                   :  [100, 0 , 5000, True],
            "H5Pb"                   :  [100, 0 , 5000, True ],
            "H2Ca"                   :  [100, 0 , 5000, True ],
            "H2Cb"                   :  [100, 0 , 5000, True ],
            "H3Ca"                   :  [100, 0 , 5000, True ],
            "H3Cb"                   :  [100, 0 , 5000, True ],
            "HT4PP"                  :  [100, 0 , 5000, True ],
            "HT6PP"                  :  [100, 0 , 5000, True],
            "sangle"                 :  [100, 0 , 1, False],
            "dangle"                 :  [100, -1 , 1, False],
            "Nj50"                   :  [10,  0 , 10,   False, "Sum$(jetPt>50)"],
            "HT50"                   :  [100, 0 , 5000, False, "Sum$(jetPt*(jetPt>50))"],
            }

        NTVariables = {
            "met"  :  [100, 0 , 1000, False],
#            "Nj50" :  [10,  0 , 10,   False, "Sum$(jetPt>50)"],
#            "HT50" :  [100, 0 , 5000, False, "Sum$(jetPt*(jetPt>50))"],
            }
	#################################################################################################

        metlimits = [100, 0, 1000]

        # Assume that we will want to reweight these
        for cut in cuts:
            cutstring = "NTVars.eventWeight*(%s)"%cuts[cut]
#            cutstring = "1."
            for varname,limits in RJigsawVariables.items() :
		print varname
                print cutstring
                vartoplot = limits[4] if len(limits)>4 else 'NTRJigsawVars.'+varname
                if limits[3]: vartoplot += '/1000.'
                job.algsAdd (ROOT.MD.AlgHist(ROOT.TH2D(varname+"_%s"%cut,
                                                       varname+"_%s"%cut,
                                                       limits[0], limits[1], limits[2],
                                                       metlimits[0], metlimits[1], metlimits[2]
                                                       ),
                                                       #100, 0, 1000),#todo make this use the other half of the dictionary
                                             vartoplot,
                                             "met",
                                             cutstring
                                             )
                             )

            # Don't make thiese 2D for now -- we may reweight in them
            for varname,limits in NTVariables.items() :
                vartoplot = limits[4] if len(limits)>4 else varname
#                print varname, ":", vartoplot
#                print cutstring
                job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1D(varname+"_%s"%cut,
                                                       varname+"_%s"%cut,
                                                       limits[0], limits[1], limits[2]
                                                       ),
                                                       #100, 0, 1000),#todo make this use the other half of the dictionary
                                             vartoplot+"/1000." if limits[3] else vartoplot,
                                             cutstring
                                             )
                             )

#        driver = None
	driver = ROOT.EL.DirectDriver()
        if options.driver == "prooflite" :
            driver = ROOT.EL.ProofDriver()
            driver.numWorkers = 6
        elif options.driver == "lsf" :
            driver = ROOT.EL.LSFDriver()
            ROOT.SH.scanNEvents(mysamplehandler);
            mysamplehandler.setMetaDouble(ROOT.EL.Job.optEventsPerWorker, 100000);
            job.options().setString(ROOT.EL.Job.optSubmitFlags, "-q " + "1nh");
        elif options.driver == "condor":
            driver = ROOT.EL.CondorDriver()
            driver.shellInit = 'lsetup root; lsetup "sft pyanalysis1.4_python2.7"';

        if options.dryRun :
            quiet_exit()

        if os.path.exists( tempDirDict[mysamplehandlername] ):
            shutil.rmtree( tempDirDict[mysamplehandlername] )
        print "submitting to dir : " + tempDirDict[mysamplehandlername]
        driver.submit(job, tempDirDict[mysamplehandlername] )

        mysamplehandler.printContent()
#	if mysamplehandler!=sh_data:
        scaleMyRootFiles(mysamplehandlername,lumi)
        os.system('hadd -f %s.root %s/hist*root*'%(tempDirDict[mysamplehandlername] ,tempDirDict[mysamplehandlername] ) )

#	if mysamplehandler!=sh_signal:





