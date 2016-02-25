import ROOT
import os
import string
import discoverInput
import copy

def cuts_from_dict(cutdict):
    return "*".join( ["(%s)"%mycut for mycut in cutdict.keys() ])

ROOT.gROOT.SetBatch(True)

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--driver"             , help="select where to run", choices=("direct","lsf", "prooflite", "grid", "condor"), default="direct")
parser.add_option('--reweightCuts'       , help='cuts used to derive ratio', choices=('no_cuts','met160','base_meff','cry_tight'), default='no_cuts')
parser.add_option('--reweightDataSource' , help='reweight by truth with reco efficiency or directly from reco', choices=('truth','reco'), default='truth')
parser.add_option('--reweightHists'      , help='reweight in which variables', choices=('bosonPt_dPhi','bosonEt_dPhi','Nj50_dPhi'),default='bosonPt_dPhi')
parser.add_option('--doZnunuEffWeight'   , help='Don\'t assume that Znunu have reco eff of 1 .', action="store_true", default=False)
(options, args) = parser.parse_args()

#gamma_lo_truth  gamma_reco  z_lo_truth  z_nlo_truth  z_reco

#inputdir = '/r04/atlas/khoo/Data_2015/zeroleptonRJR/v53_Data_pT50/'
inputdir = ['/usatlas/workarea/russsmith/photonTruthStudies_MERGED/']
if 'lxplus' in os.getenv('HOSTNAME') : inputdir = '/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v53_Data_pT50/'

ROOT.gROOT.Macro("$ROOTCOREDIR/scripts/load_packages.C")

print 'finding samples'
sh_all = ROOT.SH.SampleHandler()
discoverInput.discover(sh_all, inputdir)
print 'found'

sh_bg = {}

for sample in sh_all:
#    sample.printContent()
    if 'z_' in sample.name() :
        sample_zvv = sample
        sample_zll = copy.deepcopy(sample)

        sample_zvv.setMetaString('nc_tree', 'SRAllNT')
        sample_zll.setMetaString('nc_tree', 'CRZ_SRAllNT')

        sh_bg[sample.name() + '_zvv'] = sample_zvv
        sh_bg[sample.name() + '_zll'] = sample_zll
    if 'gamma_' in sample.name() :
        sample_gamma = sample
        sample_gamma.setMetaString('nc_tree', 'CRY_SRAllNT')

        sh_bg[sample.name()] = sample_gamma

print sh_bg

no_cuts = {}
no_cuts["1"] = [10,0,1000]
cuts = {
    "no_cuts"     : cuts_from_dict(no_cuts),
    }

#reweightvars  = ['dPhi']
#reweightHists = {}
#somehow do a list of vars you want to create weights for
#for rwvar in reweightvars :
#    reweightHists[rwvar] = getWeightHistogram(mytrees['gamma'],mytrees['zvv'], rwvar , "1.*(dPhi<4.)")

for samplename, sample in sh_bg.iteritems() :
#    if not (samplename == 'gamma_lo_truth') : continue

    sh = ROOT.SH.SampleHandler()
    sh.add(sample)

    job = ROOT.EL.Job()
    job.sampleHandler(sh)


    limits = (100, 0, 1000)
    for cut in cuts :
        for varname in ['met'] :
            weight = 'normweight*(NTVars.eventWeight)'
            cutstring = "weight_RZvvG*NTVars.eventWeight*normweight*(%s)"%cuts[cut]
            thehist = ROOT.TH1D(varname+"_%s"%cut, varname+"_%s"%cut,
                                limits[0], limits[1], limits[2])
            job.algsAdd(ROOT.MD.AlgHist(thehist,varname,cutstring))

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

    print "submitting to dir : "
    driver.submit(job, 'testdir_' + samplename )
