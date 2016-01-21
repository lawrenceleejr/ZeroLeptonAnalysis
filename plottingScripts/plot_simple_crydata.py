import ROOT
import os

from optparse import OptionParser
parser = OptionParser()
(options, args) = parser.parse_args()

inputdir = '/r04/atlas/khoo/Data_2015/zeroleptonRJR/v53_Data_pT50/'
cry_chain = ROOT.TChain('Data_CRY')
for i in sorted(os.listdir(inputdir)):
    cry_chain.Add(inputdir+i)

weightfile = ROOT.TFile('CRY_weights_RZG.root')
weighttree = weightfile.Get('CRY_weights_RZG')

cry_chain.AddFriend(weighttree)

cry_chain.Draw('deltaQCD>>deltaQCD_noRW(100,-1,1)')
cry_chain.Draw('deltaQCD>>deltaQCD_RW(100,-1,1)','weight_RZG','same')

ROOT.deltaQCD_RW.SetMarkerSize(0.5)
ROOT.deltaQCD_RW.SetMarkerColor(ROOT.kRed)
ROOT.deltaQCD_RW.SetMarkerStyle(ROOT.kFullCircle)
