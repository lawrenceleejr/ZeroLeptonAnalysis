#!/usr/bin/env python
import rootpy.ROOT as ROOT
import rootpy.io as io
import os

ROOT.gROOT.SetBatch(True)
import AtlasStyle
ROOT.SetAtlasStyle()

myfiles = {
#	'Znunu'  : root_open('../rundir_znunu_lo.root'),
	'Gamma'  : io.root_open('hist-gamma_lo_truth.root'),
	'Znunu'  : io.root_open('hist-z_lo_truth.root'),
}


filterRw = lambda i : ('Zvv' not in i.GetName()
                   and 'Zll' not in i.GetName()
                   and 'EventLoop' not in i.GetName()
                   and 'R' != i.GetName()[0]
                   and 'P' != i.GetName()[0]
                   and 'min' not in i.GetName()
                   and 'max' not in i.GetName()
                   and 'QCD' not in i.GetName()
                       )
histoList = [i for i in myfiles["Znunu"].GetListOfKeys() if filterRw(i)]
print histoList

inputdir = '/r04/atlas/khoo/Data_2015/zeroleptonRJR/v53_Data_pT50/'
if 'bnl' in os.getenv('HOSTNAME') :
    inputdir = '/pnfs/usatlas.bnl.gov/users/russsmith/RJWorkshopSamples/v53_Data_pT50/'
if 'lxplus' in os.getenv('HOSTNAME') :
    inputdir = '/afs/cern.ch/work/c/crogan/public/RJWorkshopSamples/v53_Data_pT50/'

cry_chain = ROOT.TChain('Data_CRY')
cry_chain.Add(inputdir+'Data_Nov11.root')

crz_chain = ROOT.TChain('Data_CRZ')
crz_chain.Add(inputdir+'Data_Nov11.root')

weightfile = ROOT.TFile('CRY_weights_RZG.root')
weighttree = weightfile.Get('CRY_weights_RZG')

cry_chain.AddFriend(weighttree)
crz_chain.AddFriend(weighttree)

outputdir =  'plots/'
if not os.path.isdir(outputdir) :
    os.mkdir(outputdir)

rwvars = {'bosonPt': ROOT.kBlue,
          'nJet'   : ROOT.kGreen,
          'dPhi'   : ROOT.kOrange
          }

for counter, histoKey in enumerate(histoList) :
    histoname = histoKey.GetName()
    histos = {}
    for filename , myfile in myfiles.iteritems() :
        histos[filename] = myfile.Get(histoname)
        if filename == 'Gamma' :
            for rwvar in rwvars.keys() :
                splitname = histoname.split('_')
                splitname.insert( 1, 'Zvv_' + rwvar)
                rwvarhistoname = '_'.join(splitname)
                print rwvarhistoname
                histos[filename +'_'+rwvar] = myfile.Get(rwvarhistoname)
#                histos['_'.join([filename, rwvars])] = myfile.Get(h

    if histos["Gamma"].Integral() < 1e-9 : continue
    c1 = ROOT.TCanvas("c1_"+histoKey.GetName(),
                      "c1_"+histoKey.GetName(),
                      800 , 600
                      )
    c1.Draw()

    pad1 = ROOT.TPad("pad1","pad1",0. ,0.3, 1.,1.)
    pad1.SetBottomMargin(0);
#    pad1.SetGrid(1,1)
    pad1.Draw()
    pad1.SetLogy()
    pad1.cd()

    for histoname, histo in histos.iteritems() :
        print histoname , " : Integral = " , histo.Integral()
        histo.Sumw2()
        histo.Scale(1./histo.Integral())

    histos["Znunu"].SetMarkerColor(ROOT.kRed)
    histos["Znunu"].SetMarkerStyle(ROOT.kFullCircle)
    histos["Gamma"].SetMarkerStyle(ROOT.kFullCircle)



    histos["Gamma"].Draw("p")
    histos["Znunu"].Draw("psame")

    for histoname, histo in histos.iteritems() :
        splitname = histoname.split('_')
        if len(splitname) > 1 :
            histo.SetMarkerColor( rwvars[splitname[1]])
            histo.Draw("psame")

    leg4 = ROOT.TLegend(.6, 0.6, 0.8 , 0.8)
    for histoname,histo in histos.iteritems() :
        leg4.AddEntry(histo , histoname)
    leg4.Draw("same")

    c1.cd()
    pad2 = ROOT.TPad("pad2","pad2",0. ,0.0, 1.,0.3  )
    pad2.SetTopMargin(0);
    pad2.SetGrid(0,1)
    pad2.Draw()
    pad2.cd()


    didDraw = False
    ratioDict = {}
    for histoname, histo in histos.iteritems() :
        if 'Gamma' in histoname :
            ratio = histos["Znunu"].Clone()
            ratioDict[histoname] = ratio
            ratio.SetMarkerColor(histo.GetMarkerColor())
            ratio.SetMinimum(0)
            ratio.SetMaximum(2.1)

            ratio.Divide(histo)


            ratio.GetYaxis().SetTitle("Z / gamma");
            ratio.GetYaxis().SetNdivisions(505);
            ratio.GetYaxis().SetTitleSize(20);
            ratio.GetYaxis().SetTitleFont(43);
            ratio.GetYaxis().SetTitleOffset(1.55);
            ratio.GetYaxis().SetLabelFont(43);
            ratio.GetYaxis().SetLabelSize(15);

            ratio.GetXaxis().SetTitleSize(20);
            ratio.GetXaxis().SetTitleFont(43);
            ratio.GetXaxis().SetTitleOffset(2.);
            ratio.GetXaxis().SetLabelFont(43);
            ratio.GetXaxis().SetLabelSize(15);
#            ratio.GetXaxis().SetTitle(histoKey.GetName().replace("RJVars","").replace("cry_tight","").replace("no_cuts","").replace("_","")) #RJVars_QCD_dPhiR_cry_tight

            if not didDraw :
                ratio.Draw("p")
                didDraw = True
            else :
                ratio.Draw("psame")


    c1.cd()
    c1.Print("/afs/usatlas.bnl.gov/users/russsmith/plots/"+c1.GetName()+".eps")
    histos = None
