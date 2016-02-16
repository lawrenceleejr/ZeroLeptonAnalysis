import ROOT
import os

from optparse import OptionParser
parser = OptionParser()
parser.add_option('--reweightCuts'       , help='cuts used to derive ratio', choices=('no_cuts','met160','base_meff','cry_tight'), default='no_cuts')
parser.add_option('--reweightDataSource' , help='reweight by truth with reco efficiency or directly from reco', choices=('truth','reco'), default='truth')
parser.add_option('--reweightHists'      , help='reweight in which variables', choices=('bosonPt_dPhi','bosonEt_dPhi','Nj50_dPhi'),default='bosonPt_dPhi')
parser.add_option('--doZnunuEffWeight'   , help='Don\'t assume that Znunu have reco eff of 1 .', action="store_true", default=False)
(options, args) = parser.parse_args()

inputdir = '/r04/atlas/khoo/Data_2015/zeroleptonRJR/v53_Data_pT50/'
if 'bnl' in os.getenv('HOSTNAME') : inputdir = '/pnfs/usatlas.bnl.gov/users/russsmith/RJWorkshopSamples/v53_Data_pT50/'
cry_chain = ROOT.TChain('Data_CRY')
#for i in sorted(os.listdir(inputdir)):
cry_chain.Add(inputdir+'Data_Nov11.root')

reweightfile = ROOT.TFile('ratZG.root')

reweightzvv = reweightfile.Get(options.reweightDataSource+'/Rzvvg_'+options.reweightHists+'_'+options.reweightCuts)
effhistzvv  = reweightfile.Get('efficiency/Eff_bosonPt_zvv_'+options.reweightCuts)

reweightzll = reweightfile.Get(options.reweightDataSource+'/Rzllg_'+options.reweightHists+'_'+options.reweightCuts)
effhistzll  = reweightfile.Get('efficiency/Eff_bosonPt_zll_'+options.reweightCuts)

geffhist = reweightfile.Get('efficiency/Eff_bosonPt_gamma_'+options.reweightCuts)

weightfile = ROOT.TFile('CRY_weights_RZG.root','recreate')
weighttree = ROOT.TTree('CRY_weights_RZG','Weights to scale CRY photon events to Z expectation in SR or Z CR')

ROOT.gROOT.ProcessLine(
'struct evtweight_t {\
   Float_t           weight_RZvvG;\
   Float_t           weight_RZllG;\
};' );
evtweighthelper = ROOT.evtweight_t()
zvvweightbranch = weighttree.Branch('weight_RZvvG', ROOT.AddressOf(evtweighthelper,'weight_RZvvG'), 'weight_RZvvG/F')
zllweightbranch = weighttree.Branch('weight_RZllG', ROOT.AddressOf(evtweighthelper,'weight_RZllG'), 'weight_RZllG/F')

count = 0
print "phPt dphi eff_fact xsec_fact weight_RZvvG weight_RzllG"
for event in cry_chain:
    phPt  = min(event.phPt,999.99)
    dphi  = event.dphi
    njets = event.NJet
    if njets > 9 : njets = 9 #todo extend njets reach
    #print  njets, dphi

    evtweighthelper.weight_RZvvG = 0
    evtweighthelper.weight_RZllG = 0

    if geffhist.Interpolate(phPt)>0:
        zvv_eff       = effhistzvv.Interpolate(phPt)        if options.doZnunuEffWeight else 1.
        zvv_eff_fact  = zvv_eff/geffhist.Interpolate(phPt)  if options.reweightDataSource=='truth' else 1.

        zvv_xsec_fact = 0
        if options.reweightHists == 'bosonPt_dPhi' :
            zvv_xsec_fact = reweightzvv.Interpolate(phPt,dphi)
        if options.reweightHists == 'Nj50_dPhi' :
            #print 'doing njet dphi weight'
            zvv_xsec_fact = reweightzvv.Interpolate(njets,dphi)
            #print 'interpolated'
        if not zvv_xsec_fact :
            print 'you have no zvv xsec fact'
            print phPt,njets,dphi
            exit()
        evtweighthelper.weight_RZvvG = zvv_eff_fact*zvv_xsec_fact

        zll_xsec_fact = 0
        if options.reweightHists == 'bosonPt_dPhi' :
            zll_xsec_fact = reweightzll.Interpolate(phPt,dphi)
        if options.reweightHists == 'Nj50_dPhi' :
            #print 'doing njet dphi weight for zll'
           zll_xsec_fact = reweightzll.Interpolate(njets,dphi)
            #print 'interpolateed zll'
        if not zll_xsec_fact :
            print 'you have no zll xsec fact'
            print phPt,njets,dphi
            exit()

        zll_eff_fact  = effhistzll.Interpolate(phPt)/geffhist.Interpolate(phPt)   if options.reweightDataSource=='truth' else 1.
        evtweighthelper.weight_RZllG = zll_eff_fact*zll_xsec_fact

    if count<10:
        #print phPt, dphi, eff_fact, xsec_fact, evtweighthelper.weight_RZvvG, evtweighthelper.weight_RZllG
        print phPt, dphi, zll_xsec_fact, evtweighthelper.weight_RZvvG, evtweighthelper.weight_RZllG
    if (count%10000)==0: print count, '/', cry_chain.GetEntries()

    weighttree.Fill()
    count+=1

weighttree.Write()
weightfile.Close()
