import ROOT
import os

from optparse import OptionParser
parser = OptionParser()
parser.add_option('--reweightCuts' , help='cuts used to derive ratio', choices=('no_cuts','met160','base_meff','cry_tight'), default='no_cuts')
(options, args) = parser.parse_args()

inputdir = '/r04/atlas/khoo/Data_2015/zeroleptonRJR/v53_Data_pT50/'
if 'bnl' in os.getenv('HOSTNAME') : inputdir = '/pnfs/usatlas.bnl.gov/users/russsmith/RJWorkshopSamples/v53_Data_pT50/'
cry_chain = ROOT.TChain('Data_CRY')
for i in sorted(os.listdir(inputdir)):
    cry_chain.Add(inputdir+i)

reweightfile = ROOT.TFile('ratZG.root')
reweighthist = reweightfile.Get('truth/Rzg_bosonPt_dPhi_'+options.reweightCuts)
zeffhist = reweightfile.Get('efficiency/Eff_bosonPt_z_'+options.reweightCuts)
geffhist = reweightfile.Get('efficiency/Eff_bosonPt_gamma_'+options.reweightCuts)

weightfile = ROOT.TFile('CRY_weights_RZG.root','recreate')
weighttree = ROOT.TTree('CRY_weights_RZG','Weights to scale CRY photon events to Z prediction')

ROOT.gROOT.ProcessLine(
'struct evtweight_t {\
   Float_t           weight_RZG;\
};' );
evtweighthelper = ROOT.evtweight_t()
evtweightbranch = weighttree.Branch('weight_RZG', ROOT.AddressOf(evtweighthelper,'weight_RZG'), 'weight_RZG/F')

count = 0
print "phPt dphi eff_fact xsec_fact weight_RZG"
for event in cry_chain:
    phPt = min(event.phPt,999.99)
    dphi = event.dphi
    evtweighthelper.weight_RZG = 0

    if geffhist.Interpolate(phPt)>0:
        eff_fact = zeffhist.Interpolate(phPt)/geffhist.Interpolate(phPt)
        xsec_fact = reweighthist.Interpolate(phPt,dphi)
        evtweighthelper.weight_RZG = eff_fact*xsec_fact

    if count<10:
        print phPt, dphi, eff_fact, xsec_fact, evtweighthelper.weight_RZG
    if (count%10000)==0: print count, '/', cry_chain.GetEntries()

    weighttree.Fill()
    count+=1
    
weighttree.Write()
weightfile.Close()
