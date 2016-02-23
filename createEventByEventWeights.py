import ROOT
import os

ROOT.gROOT.SetBatch(True)

from optparse import OptionParser
parser = OptionParser()
parser.add_option('--reweightCuts'       , help='cuts used to derive ratio', choices=('no_cuts','met160','base_meff','cry_tight'), default='no_cuts')
parser.add_option('--reweightDataSource' , help='reweight by truth with reco efficiency or directly from reco', choices=('truth','reco'), default='truth')
parser.add_option('--reweightHists'      , help='reweight in which variables', choices=('bosonPt_dPhi','bosonEt_dPhi','Nj50_dPhi'),default='bosonPt_dPhi')
parser.add_option('--doZnunuEffWeight'   , help='Don\'t assume that Znunu have reco eff of 1 .', action="store_true", default=False)
(options, args) = parser.parse_args()

#todo cache the rw histos
reweightfile = None
if os.path.isfile('ratZG.root') :
    reweightfile = ROOT.TFile.Open('ratZG.root','UPDATE')
#def checkWeightHistogramCache(rwfile, weightVar ) :
#    if
def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def getWeightHistogram(z_tree , g_tree, weightVar = 'bosonPt' , selection='1.' ) :
    global reweightfile#maybe clean this up
    selection = selection+'*normweight*(NTVars.eventWeight)'
    if reweightfile :
        rw_hist = reweightfile.Get('_'.join([weightVar,selection]))
        return rw_hist

    z_treeHist = None
    g_treeHist = None

    print 'creating weight histo for z'
    z_tree.Draw(weightVar+">>z_treeHist",selection);
    print 'creating weight histo for g'
    g_tree.Draw(weightVar+">>g_treeHist",selection);
    print 'created weighting histos'

    ROOT.gDirectory.Print()

    z_treeHist = ROOT.gDirectory.Get("z_treeHist");
    g_treeHist = ROOT.gDirectory.Get("g_treeHist");

    rw_hist = z_treeHist.Clone()
    rw_hist.SetName('_'.join([weightVar,selection]))
    rw_hist.Divide(g_treeHist)

    reweightfile = ROOT.TFile.Open('ratZG.root','NEW')
    rw_hist.Write()

    return rw_hist


#inputdir = '/r04/atlas/khoo/Data_2015/zeroleptonRJR/v53_Data_pT50/'
inputdir = None
if 'bnl'    in os.getenv('HOSTNAME') : inputdir = '/pnfs/usatlas.bnl.gov/users/russsmith/photonTruthStudies_MERGED/'
if 'lxplus' in os.getenv('HOSTNAME') : inputdir = '/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v53_Data_pT50/'

myfiles = {
    'gamma' : ROOT.TFile.Open(inputdir + 'gamma_lo_truth/Gamma.root'),
    'zjets' : ROOT.TFile.Open(inputdir + 'z_lo_truth/ZJets.root')
}

mytrees = {
    'gamma' : myfiles['gamma'].Get('CRY_SRAllNT'),
    'zjets' : myfiles['gamma'].Get('SRAllNT'    )
}

reweightvars  = ['dPhi']
reweightHists = {}
#somehow do a list of vars you want to create weights for
for rwvar in reweightvars :
    reweightHists[rwvar] = getWeightHistogram(mytrees['gamma'],mytrees['zjets'], rwvar )

print reweightvars

myfiles['zjets'].Close()

weightfile = ROOT.TFile('CRY_weights_RZG.root','recreate')
weighttree = ROOT.TTree('CRY_weights_RZG','Weights to scale CRY photon events to Z expectation in SR or Z CR')

def addWeightBranch(rwvar, evtweighthelpers) :

    structname       = 'evtweight_'   +rwvar+'_t'
    weightRZvvG_name = 'weight_RZvvG'
    weightRZllG_name = 'weight_RZllG'

    ROOT.gROOT.ProcessLine(
        'struct '           +structname+      ' {\
         Float_t           '+weightRZvvG_name+';\
         Float_t           '+weightRZllG_name+';\
         };' );

    evtweighthelper = getattr(ROOT, structname)()
    zvvweightbranch = weighttree.Branch(weightRZvvG_name,
                                    ROOT.AddressOf(evtweighthelper,weightRZvvG_name),
                                    weightRZvvG_name+'/F')
    zllweightbranch = weighttree.Branch(weightRZllG_name,
                                    ROOT.AddressOf(evtweighthelper,weightRZllG_name),
                                    weightRZllG_name+'/F')

    evtweighthelpers[rwvar] = evtweighthelper

evtweighthelpers = {}
for rwvar in reweightvars :
    addWeightBranch(rwvar, evtweighthelpers)

count = 0
print "phPt dphi eff_fact xsec_fact weight_RZvvG weight_RzllG"
for event in mytrees['gamma'] :

    phPt  = min(event.phPt,999.99)
    dphi  = event.dPhi
    njets = event.jetPt.size()
    if njets > 14 : njets = 14 #todo extend njets reach


#here do a loop over the rw vars
    for rwvar, helper in evtweighthelpers.iteritems() :
        rwvarvalue     = getattr(event, rwvar)
        rwvarvalueTest = event.dPhi
        print count
        print rwvar, rwvarvalue
        print rwvar, rwvarvalueTest
        assert(isclose(rwvarvalue,rwvarvalueTest)


        continue
        helper.weight_RZvvG = 0
        helper.weight_RZllG = 0

        zll_eff_fact  = effhistzll.Interpolate(phPt)/geffhist.Interpolate(phPt)
        evtweighthelper.weight_RZllG = zll_eff_fact*zll_xsec_fact


        # evtweighthelper.weight_RZvvG = 0
        # evtweighthelper.weight_RZllG = 0

    # if geffhist.Interpolate(phPt)>0:
    #     zvv_eff       = effhistzvv.Interpolate(phPt)        #if options.doZnunuEffWeight else 1.
    #     zvv_eff_fact  = zvv_eff/geffhist.Interpolate(phPt)  #if options.reweightDataSource=='truth' else 1.

    #     zvv_xsec_fact = 0
    #     zvv_xsec_fact = reweightzvv.Interpolate(phPt,dphi)
    #     if not zvv_xsec_fact :
    #         print 'you have no zvv xsec fact'
    #         print phPt,njets,dphi
    #         exit()

        # evtweighthelper.weight_RZvvG = zvv_eff_fact*zvv_xsec_fact

        # zll_xsec_fact = 0
        # if options.reweightHists == 'bosonPt_dPhi' :
        #     zll_xsec_fact = reweightzll.Interpolate(phPt,dphi)
        # if options.reweightHists == 'Nj50_dPhi' :
        #     #print 'doing njet dphi weight for zll'
        #    zll_xsec_fact = reweightzll.Interpolate(njets,dphi)
        #     #print 'interpolateed zll'
        # if not zll_xsec_fact :
        #     print 'you have no zll xsec fact'
        #     print phPt,njets,dphi
        #     exit()


    # if count<10:
    #     #print phPt, dphi, eff_fact, xsec_fact, evtweighthelper.weight_RZvvG, evtweighthelper.weight_RZllG
    #     print phPt, dphi, zll_xsec_fact, evtweighthelper.weight_RZvvG, evtweighthelper.weight_RZllG
    if (count%10000)==0: print count, '/', mytrees['gamma'].GetEntries()

    weighttree.Fill()
    count+=1

weighttree.Write()
weightfile.Close()
