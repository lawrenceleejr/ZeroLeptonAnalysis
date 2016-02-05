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

sampleChoices = (        "zvv_nlo_reco" ,"zll_nlo_reco","gamma_reco",
                         "zvv_lo_truth" ,"zll_lo_truth",
                         "zvv_nlo_truth","zll_nlo_truth","gamma_truth"
                         )

parser = OptionParser()
parser.add_option("--driver"      , help="select where to run", choices=("direct","lsf", "prooflite", "grid", "condor"), default="direct")
parser.add_option("--isTest", action="store_true", default=False)
parser.add_option("--dryRun", action="store_true", default=False)
#parser.add_argument("--no-isTest", dest="isTest", action="store_false")
parser.add_option("--samplesToRun", help="Run a subset of samples. Note we need to do this for the LSF driver as things are",
#                  choices=(sampleChoices+('all',)),
                  default="all")


#parser.add_option("--nevents", type=int, help="number of events to process for all the datasets")
#parser.add_option("--skip-events", type=int, help="skip the first n events")
#parser.add_option("--runTag", help="", default="Test_XXYYZZa")

(options, args) = parser.parse_args()

import atexit
atexit.register
def quiet_exit():
    ROOT.gSystem.Exit(0)

def cuts_from_dict(cutdict):
    return "*".join( ["(%s)"%mycut for mycut in cutdict.keys() ])

def checkBranchExists(branchname, chain) :
    checkBranchExistsBool = False
    for branch in mychain.GetListOfBranches() :
        if varname == branch.GetName() : checkBranchExistsBool = True
    return checkBranchExistsBool

logging.info("loading packages")
ROOT.gROOT.Macro("$ROOTCOREDIR/scripts/load_packages.C")

##
##
########### Configuration ######################################
##
##

lumi = 3320  ## in pb-1
search_directories = ["/afs/cern.ch/work/r/rsmith/photonTruthStudies/"]
import os
if os.getenv("USER")=="khoo":
    search_directories = ["/r04/atlas/khoo/Data_2015/zeroleptonRJR/zG_180116"]
if "bnl" in os.getenv("HOSTNAME") :
    search_directories = ["/pnfs/usatlas.bnl.gov/users/russsmith/photonTruthStudies_zG_test/"]

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

ROOT.SH.readSusyMeta(sh_all,"$ROOTCOREBIN/data/SUSYTools/susy_crosssections_13TeV.txt")

## Split up samplehandler into per-BG SH"s based on tag metadata

#sh_data   = sh_all.find("data")
#sh_signal = sh_all.find("signal")
sh_bg = {}

#sh_bg["qcd"  ] = sh_all.find("qcd"  )
#sh_bg["top"  ] = sh_all.find("top"  )

sampleslist = (list(sampleChoices)) if options.samplesToRun == 'all' else [sample for sample in list(sampleChoices) if options.samplesToRun in sample]#can do any combos here
print sampleslist
if not sampleslist :
    print 'your expression isn\' a substring of any of the following sample choices :'
    print sampleChoices
    print 'Exiting'
    quiet_exit()


for sample in sampleslist:
    sh_bg[sample] = sh_all.find(sample)
    sh_bg[sample].printContent()
    if "zvv" in sample:
        sh_bg[sample].setMetaString("nc_tree", "SRAllNT")
    elif "zll" in sample:
        sh_bg[sample].setMetaString("nc_tree", "CRZ_SRAllNT")
    elif "g" in sample:
        sh_bg[sample].setMetaString("nc_tree", "CRY_SRAllNT")

if len(sh_bg)==0:
    print "please give a sample to run on.  Exiting."
    quiet_exit()

#print sh_bg

# for key, sh in sh_bg.iteritems() :
#     print key
#     sh.printContent()

#Creation of output directory names
tempDirDict = {}

for key in sh_bg.keys() :
    tempDirDict[key] = "rundir_" + key

def sherpaScaleFactor(sample) :
    name = sample.getMetaString("sample_name")
    scalef = 1.
    if "e4133" in name :
        splitPt = name.split("Pt")[1]  #find the pt
        startingPtSlice = int(splitPt.split("_")[0])
        if startingPtSlice > 279. :
            scalef = 1.
    return scalef

#To scale the histograms in the files after the event loop is done...
def scaleMyRootFiles(processname,mylumi):
    process = sh_bg[processname]
    for sample in process:
        tempxs = sample.getMetaDouble("nc_xs") * sample.getMetaDouble("kfactor") * sample.getMetaDouble("filter_efficiency") * sherpaScaleFactor(sample)

        print "Scaling %s by %f/(%f)"%(sample.getMetaString("short_name"), tempxs, sample.getMetaDouble("nc_sumw"))
        m_eventscaling = tempxs
        if sample.getMetaDouble("nc_sumw")>0:
            m_eventscaling /= sample.getMetaDouble("nc_sumw")
        else:
            m_eventscaling = 0.
        myfile = ROOT.TFile( tempDirDict[processname]+"/hist-"+sample.fileName(0).split("/")[-2]+".root","UPDATE")
        dirList = ROOT.gDirectory.GetListOfKeys()
        for k1 in dirList:
            h1 = k1.ReadObj()
            if h1.ClassName() == "TH1D" or h1.ClassName() == "TH2D" or h1.ClassName() == "TH3D":
                h1.Scale(m_eventscaling)
                h1.Scale(mylumi)
                h1.Write()
        myfile.Close()

for processname in sh_bg.keys():
    process = sh_bg[processname]
    emptylist = []
    for sample in process:
        mychain = sample.makeTChain()
        # print sample
        # print mychain.GetEntries()
        if mychain.GetEntries()==0:
            emptylist.append(sample)
        m_nevt = 0
        m_sumw = 0
        # filter out empty files, because BatchDriver fails on them
        for ifile in xrange(sample.numFiles()):
            myfile = ROOT.TFile(sample.fileName(ifile))
            mytree = myfile.Get("SRAllNT") if processname.split("_")[0]=="zvv" else myfile.Get("CRZ_SRAllNT") if processname.split("_")[0]=="zll" else myfile.Get("CRY_SRAllNT")
            # if mytree.GetEntries()==0:
            #     emptylist.append(sample)
            #     continue
            try:
                m_nevt += myfile.Get("Counter_JobBookeeping_JobBookeeping").GetBinContent(1)
                m_sumw += myfile.Get("Counter_JobBookeeping_JobBookeeping").GetBinContent(2)
            except:
                pass
            myfile.Close()
            sample.setMetaDouble("nc_nevt",m_nevt)
            sample.setMetaDouble("nc_sumw",m_sumw)
    for emptysample in emptylist:
        print emptysample
        process.remove(emptysample)

    job = ROOT.EL.Job()
    job.sampleHandler(process)

    no_cuts = {}
    no_cuts["1"] = [10,0,1000]

    met50 = no_cuts.copy()
    met50["met>50"] = [10,0,1000]

    met100 = no_cuts.copy()
    met100["met>100"] = [10,0,1000]

    met160 = no_cuts.copy()
    met160["met>160"] = [10,0,1000]

    met300 = no_cuts.copy()
    met300["met>300"] = [10,0,1000]

    met500 = no_cuts.copy()
    met500["met>500"] = [10,0,1000]

    met600 = no_cuts.copy()
    met600["met>600"] = [10,0,1000]

    met50_2jet = no_cuts.copy()
    met50_2jet["met>50"] = [10,0,1000]
    met50_2jet["PP_MDeltaR>0.1"] = [10,0,2000]

    met100_2jet = no_cuts.copy()
    met100_2jet["met>100"] = [10,0,1000]
    met100_2jet["PP_MDeltaR>0.1"] = [10,0,2000]

    met300_2jet = no_cuts.copy()
    met300_2jet["met>300"] = [10,0,1000]
    met300_2jet["PP_MDeltaR>0.1"] = [10,0,2000]

    baseline_cuts = no_cuts.copy()#[]
    # baseline_cuts["jetPt[0] > 100"] = [10,0,500]
    baseline_cuts["met>160"] = [10,0,1000]
    baseline_cuts["meffInc>800"] = [10,0,5000]

    cry_cuts = baseline_cuts.copy()
    cry_cuts["PP_MDeltaR>300."]      = [10,0,2000]
    cry_cuts["RPT_HT5PP<.4"]                 = [10,-1,1]
    cry_cuts["QCD_Delta1 / (1 - QCD_Rsib) > .05"] = [10,-1,1]

    cry_cuts_met300 = cry_cuts.copy()
    cry_cuts_met300["met>300"] = [10,0,1000]

    cry_cuts_met500 = cry_cuts.copy()
    cry_cuts_met500["met>500"] = [10,0,1000]

    cry_cuts_met600 = cry_cuts.copy()
    cry_cuts_met600["met>600"] = [10,0,1000]

#    print cry_cuts

    ## Define your cut strings here....
    if options.isTest:
        cuts = {
            "no_cuts"     : cuts_from_dict(no_cuts),
            }
    else:
        cuts = {
            "no_cuts"     : cuts_from_dict(no_cuts),
            "base_meff"   : cuts_from_dict(baseline_cuts),
            "cry_tight"   : cuts_from_dict(cry_cuts),
            "cry_tight_met300"   : cuts_from_dict(cry_cuts_met300),
            "cry_tight_met500"   : cuts_from_dict(cry_cuts_met500),
            "cry_tight_met600"   : cuts_from_dict(cry_cuts_met600),
            "met50"       : cuts_from_dict(met50),
#            "met100"      : cuts_from_dict(met100),
            "met160"      : cuts_from_dict(met160),
            "met300"      : cuts_from_dict(met300),
            "met500"      : cuts_from_dict(met500),
            "met600"      : cuts_from_dict(met600),
#            "met50_2jet"  : cuts_from_dict(met50_2jet),
#            "met100_2jet" : cuts_from_dict(met100_2jet),
#            "met300_2jet" : cuts_from_dict(met300_2jet)
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
    if options.isTest :
        RJigsawVariables = {
            'HT1CM'                  :  [25, 0 , 5000, True],
            }
    else:
        RJigsawVariables = {
            'HT1CM'                  :  [25, 0 , 5000, True],
            'PIoHT1CM'               :  [26, 0, 1.04, False ],
            'cosS'                   :  [26, -1 , 1.04, False ],
            'NVS'                    :  [10,  0 , 10, False ],
            'RPT_HT1CM'              :  [26, 0, 1.04, False ],
            'MS'                     :  [25,  0, 1000, True ],
            'ddphiP'                 :  [26, -1 , 1.04, False ],
            'sdphiP'                 :  [26, 0, 1.04, False ],
            # 'pPP_Ia'                 :  [25, 0 , 5000, True],
            # 'pPP_Ib'                 :  [25, 0 , 5000, True ],
            # 'pT_jet1a'               :  [25, 0 , 2500, True ],
            # 'pT_jet1b'               :  [25, 0 , 2500, True ],
            # 'pT_jet2a'               :  [25, 0 , 2500, True ],
            # 'pT_jet2b'               :  [25, 0 , 2500, True ],
            # 'pTPP_jet1'              :  [25, 0 , 5000, True ],
            # 'pTPP_jet2'              :  [25, 0 , 5000, True ],
            # 'pTPP_jet1a'             :  [25, 0 , 5000, True ],
            # 'pTPP_jet1b'             :  [25, 0 , 5000, True ],
            # 'pTPP_jet2a'             :  [25, 0 , 2500, True ],
            # 'pTPP_jet2b'             :  [25, 0 , 2500, True ],
            # 'pTPP_jet3a'             :  [25, 0 , 2500, True ],
            # 'pTPP_jet3b'             :  [25, 0 , 2500, True ],
            # 'pPP_jet1a'              :  [25, 0 , 5000, True ],
            # 'pPP_jet1b'              :  [25, 0 , 5000, True ],
            # 'pPP_jet2a'              :  [25, 0 , 2500, True ],
            # 'pPP_jet2b'              :  [25, 0 , 2500, True ],
            # 'pPP_jet3a'              :  [25, 0 , 2500, True ],
            # 'pPP_jet3b'              :  [25, 0 , 2500, True ],
            'R_H2PP_H3PP'            :  [26, 0, 1.04, False ],
            'R_pTj2_HT3PP'           :  [26, 0, 1.04, False ],
            'R_HT5PP_H5PP'           :  [26, 0, 1.04, False ],
            'R_H2PP_H5PP'            :  [26, 0, 1.04, False],
            'minR_pTj2i_HT3PPi'      :  [26, 0, 1.04, False],
            'maxR_H1PPi_H2PPi'       :  [26, 0, 1.04, False],
            'R_HT9PP_H9PP'           :  [26, 0, 1.04, False],
            'R_H2PP_H9PP'            :  [26, 0, 1.04, False],
            'RPZ_HT3PP'              :  [26, 0, 1.04, False],
            'RPZ_HT5PP'              :  [26, 0, 1.04, False],
            'RPZ_HT9PP'              :  [26, 0, 1.04, False],
            'RPT_HT3PP'              :  [26, 0, 1.04, False],
            'RPT_HT5PP'              :  [26, 0, 1.04, False],
            'RPT_HT9PP'              :  [26, 0, 1.04, False],
            #           'cosPP'            :  [26, -1 , 1.04, False],
            'PP_CosTheta'            :  [26, -1 , 1.04, False],
            'PP_VisShape'            :  [26, 0, 1.04, False],
            'PP_MDeltaR'             :  [25, 0 , 2000, True],
            # 'dphiPV1a'               :  [32, 0, 6.4, False],
            # 'cosV1a'                 :  [26, -1 , 1.04, False ],
            # 'dphiCV2a'               :  [32, 0 , 6.4, False],
            # 'cosV2a'                 :  [26, -1 , 1.04, False],
            # 'dphiPV1b'               :  [32, 0 , 6.4, False ],
            # 'cosV1b'                 :  [26, -1 , 1.04, False ],
            # 'dphiCV2b'               :  [32, 0 , 6.4, False ],
            # 'cosV2b'                 :  [26, -1 , 1.04, False ],
            # 'NJa'                    :  [10, 0 , 10, False ],
            # 'NJb'                    :  [10, 0 , 10, False ],
            'QCD_dPhiR'              :  [26, -1 , 1.04, False ], # always -100
            'QCD_Rsib'               :  [26, 0, 1.04, False ],
            'QCD_Delta1'             :  [26, -1 , 1.04, False ],
            'H2PP'                   :  [25, 0 , 5000, True ],
            'H3PP'                   :  [25, 0 , 5000, True ],
            'H4PP'                   :  [25, 0 , 5000, True ],
            'H6PP'                   :  [25, 0 , 5000, True ],
            'H10PP'                  :  [25, 0 , 5000, True ],
            'HT10PP'                 :  [25, 0 , 5000, True ],
            # 'H2Pa'                   :  [25, 0 , 5000, True ],
            # 'H2Pb'                   :  [25, 0 , 5000, True ],
            # 'H3Pa'                   :  [25, 0 , 5000, True ],
            # 'H3Pb'                   :  [25, 0 , 5000, True ],
            # 'H4Pa'                   :  [25, 0 , 5000, True],
            # 'H4Pb'                   :  [25, 0 , 5000, True],
            # 'H5Pa'                   :  [25, 0 , 5000, True],
            # 'H5Pb'                   :  [25, 0 , 5000, True ],
            # 'H2Ca'                   :  [25, 0 , 5000, True ],
            # 'H2Cb'                   :  [25, 0 , 5000, True ],
            # 'H3Ca'                   :  [25, 0 , 5000, True ],
            # 'H3Cb'                   :  [25, 0 , 5000, True ],
            'HT4PP'                  :  [25, 0 , 5000, True ],
            'HT6PP'                  :  [25, 0 , 5000, True],
            'sangle'                 :  [26, 0, 1.04, False],
            'dangle'                 :  [26, -1 , 1.04, False],
            'QCD_dPhiR'              :  [32,  0 , 3.2, False],
            'Nj50'                   :  [10,  0 , 10,   False, 'Sum$(jetPt>50)'],
            'HT50'                   :  [25, 0 , 5000, False, 'Sum$(jetPt*(jetPt>50))'],
            }

    bosonType = processname.split("_")[0]
    if options.isTest:
        NTVariables = {
            "bosonPt"                    :  [25, 0 , 2000, True, "NTExtraVars.ZvvPt" if bosonType=="zvv" else "1000.*NTCRZVars.Zpt" if bosonType=="zll" else "NTCRYVars.phPt"],
            "dPhi"                       :  [32,  0 , 3.2, False],
            }
    else:
        NTVariables = {
            "met"                        :  [25, 0 , 2000, False],
            "bosonPt"                    :  [25, 0 , 1000, True, "NTExtraVars.ZvvPt" if bosonType=="zvv" else "1000.*NTCRZVars.Zpt" if bosonType=="zll" else "NTCRYVars.phPt"],
            "bosonEta"                   :  [25, -5,    5, False, "NTExtraVars.ZvvEta" if bosonType=="zvv" else "0" if bosonType=="zll" else "NTCRYVars.phEta"],
            "bosonEt"                    :  [25, 0 , 1000, True, "sqrt(NTExtraVars.ZvvPt**2+min(NTExtraVars.ZvvM,120e3)**2)" if bosonType=="zvv" else "1000.*sqrt(NTCRZVars.Zpt**2+NTCRZVars.mll**2)" if bosonType=="zll" else "NTCRYVars.phPt"],
            "dPhi"                       :  [32,  0 , 3.2, False],
            #            "Nj50" :  [10,  0 , 10,   False, "Sum$(jetPt>50)"],
            #            "HT50" :  [25, 0 , 5000, False, "Sum$(jetPt*(jetPt>50))"],
            }
    #################################################################################################

    etlimits   = [25, 0, 1000]
    dphilimits = [32, 0, 3.2]
    etalimits  = [20, -5, 5]

    # Assume that we will want to reweight these

    for cut in cuts:
        cutstring = "NTVars.eventWeight*(%s)"%cuts[cut]
        #            cutstring = "1."
        for varname,limits in RJigsawVariables.items() :
            # print varname
            # print cutstring
            vartoplot = limits[4] if len(limits)>4 else varname
            if limits[3]: vartoplot += "/1e3"
            if "z" in processname:
                thehist = ROOT.TH1D(varname+"_%s"%cut, varname+"_%s"%cut,
                                    limits[0], limits[1], limits[2])
                job.algsAdd(ROOT.MD.AlgHist(thehist,vartoplot,cutstring))
            else:
            #                if not checkBranchExists(varname, mychain) : continue
                thehist = ROOT.TH3D(varname+"_%s"%cut, varname+"_%s"%cut,
                                    limits[0], limits[1], limits[2],
                                    etlimits[0], etlimits[1], etlimits[2],
                                    dphilimits[0], dphilimits[1], dphilimits[2])
                job.algsAdd(ROOT.MD.AlgHist(thehist,vartoplot,NTVariables["bosonPt"][4]+"/1000","dPhi",cutstring))

        # Don't make these 2D for now -- we may reweight in them
        for varname,limits in NTVariables.items() :
            vartoplot = limits[4] if len(limits)>4 else varname
            if limits[3]: vartoplot += "/1e3"
#            print varname, ":", vartoplot
#            print cutstring
            thehist = ROOT.TH1D(varname+"_%s"%cut,varname+"_%s"%cut,
                                limits[0], limits[1], limits[2])
            job.algsAdd(ROOT.MD.AlgHist(thehist, vartoplot, cutstring ))

        if not options.isTest:
            therwhist = ROOT.TH2D("bosonPt_dPhi_%s"%cut,"bosonPt_dPhi_%s"%cut,
                                  etlimits[0], etlimits[1], etlimits[2],
                                  dphilimits[0], dphilimits[1], dphilimits[2],
                                  )
            job.algsAdd(ROOT.MD.AlgHist(therwhist, NTVariables["bosonPt"][4]+"/1000","dPhi", cutstring ))

            therwhist = ROOT.TH2D("bosonEt_dPhi_%s"%cut,"bosonEt_dPhi_%s"%cut,
                                  etlimits[0], etlimits[1], etlimits[2],
                                  dphilimits[0], dphilimits[1], dphilimits[2],
                                  )
            job.algsAdd(ROOT.MD.AlgHist(therwhist, NTVariables["bosonEt"][4]+"/1000","dPhi", cutstring ))

            therwhist = ROOT.TH2D("bosonPt_bosonEta_%s"%cut,"bosonPt_bosonEta_%s"%cut,
                                  etlimits[0], etlimits[1], etlimits[2],
                                  etalimits[0], etalimits[1], etalimits[2],
                                  )
            job.algsAdd(ROOT.MD.AlgHist(therwhist, NTVariables["bosonPt"][4]+"/1000",NTVariables["bosonEta"][4], cutstring ))

    driver = None
    if options.driver == "prooflite" :
        driver = ROOT.EL.ProofDriver()
        driver.numWorkers = 3
    elif options.driver == "lsf" :
        driver = ROOT.EL.LSFDriver()
        ROOT.SH.scanNEvents(process);
        process.setMetaDouble(ROOT.EL.Job.optEventsPerWorker, 100000);
        job.options().setString(ROOT.EL.Job.optSubmitFlags, "-q " + "1nh");
    elif options.driver == "condor":
        driver = ROOT.EL.CondorDriver()
        ROOT.SH.scanNEvents(process);
        process.setMetaDouble(ROOT.EL.Job.optEventsPerWorker, 100000);
        driver.options().setString(ROOT.EL.Job.optCondorConf, "notification=never");
        if "bnl" in os.getenv("HOSTNAME") : job.options().setString (ROOT.EL.Job.optCondorConf, "accounting_group = group_atlas.general");

        #driver.shellInit = "source /var/clus/usera/khoo/scripts/khoo_setup.sh; lsetup root; lsetup "sft pyanalysis/1.4_python2.7"";
    else:
        driver = ROOT.EL.DirectDriver()

    if options.dryRun :
        quiet_exit()

    if os.path.exists( tempDirDict[processname] ):
        shutil.rmtree( tempDirDict[processname] )
    print "submitting to dir : " + tempDirDict[processname]
    driver.submit(job, tempDirDict[processname] )

    process.printContent()
    #	if process!=sh_data:
    scaleMyRootFiles(processname,lumi)
    os.system("hadd -f %s.root %s/hist*root*"%(tempDirDict[processname] ,tempDirDict[processname] ) )

    #	if process!=sh_signal:
