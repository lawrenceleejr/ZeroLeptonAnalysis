#!/usr/bin/env python
import rootpy.ROOT as ROOT
#import numpy as np
from rootpy.io import root_open

import os

ROOT.gROOT.SetBatch(True)
import AtlasStyle

# Translate TJ/Russell vars to Chris vars
varmappings = {
'HT1CM':'HT1CM',
'PIoHT1CM':'PIoHT1CM',
'cosS':'cosS',
'NVS':'NVS',
'RPT_HT1CM':'RPT_HT1CM',
'MS':'MS',
'ddphiP':'ddphiP',
'sdphiP':'sdphiP',
'R_H2PP_H3PP':'R_H2PP_H3PP',
'R_pTj2_HT3PP':'R_pTj2_HT3PP',
'R_HT5PP_H5PP':'R_HT5PP_H5PP',
'R_H2PP_H5PP':'R_H2PP_H5PP',
'minR_pTj2i_HT3PPi':'minR_pTj2i_HT3PPi',
'maxR_H1PPi_H2PPi':'maxR_H1PPi_H2PPi',
'R_HT9PP_H9PP':'R_HT9PP_H9PP',
'R_H2PP_H9PP':'R_H2PP_H9PP',
'RPZ_HT3PP':'RPZ_HT3PP',
'RPZ_HT5PP':'RPZ_HT5PP',
'RPZ_HT9PP':'RPZ_HT9PP',
'RPT_HT3PP':'RPT_HT3PP',
'RPT_HT5PP':'RPT_HT5PP',
'RPT_HT9PP':'RPT_HT9PP',
'PP_CosTheta':'cosPP',
'PP_VisShape':'PP_VisShape',
'PP_MDeltaR':'MDR',
'QCD_dPhiR':'dphiR',
'QCD_Rsib':'Rsib',
'QCD_Delta1':'deltaQCD',
'H2PP':'H2PP',
'H3PP':'H3PP',
'H4PP':'H4PP',
'H6PP':'H6PP',
'H10PP':'H10PP',
'HT10PP':'HT10PP',
'HT4PP':'HT4PP',
'HT6PP':'HT5PP',
'sangle':'sangle',
'dangle':'dangle',
}

cuts = {
    'no_cuts':'1',
    'met50':'MET>50',
    'met100':'MET>300',
    'met160':'MET>100',
    'met300':'MET>300',
    'met50_2jet':'MET>50&&MDR>0.1',
    'met100_2jet':'MET>100&&MDR>0.1',
    'met300_2jet':'MET>300&&MDR>0.1',
    'base_meff':'MET>160&&Meff>800',
    'cry_tight':'MET>160&&Meff>800&&MDR>300&&RPT_HT5PP<0.4&&deltaQCD/(1-Rsib)>.05',
}

from optparse import OptionParser
parser = OptionParser()
parser.add_option('--dataSource' , help='select reco or truth inputs', choices=('truth','reco'), default='truth')
parser.add_option('--meOrder' , help='select lo or nlo Z', choices=('lo','nlo'), default='lo')
parser.add_option('--reweightCuts' , help='cuts used to derive ratio', choices=('no_cuts','met160','base_meff','cry_tight'), default='no_cuts')
(options, args) = parser.parse_args()

reweightfile = ROOT.TFile('ratZG.root')
reweighthist = None
if options.dataSource == 'truth':
    myfiles = {
	'Znunu'  : ROOT.TFile('rundir_z_'+options.meOrder+'_truth.root'),
	'Gamma'  : ROOT.TFile('rundir_gamma_truth.root'),
        }
    reweighthist = reweightfile.Get('truth/Rzg_bosonPt_dPhi_'+options.reweightCuts)
    #reweighthist = reweightfile.Get('truth/Rzg_bosonPt_dPhi_'+options.reweightCuts+'_alt')
    #reweighthist = reweightfile.Get('truth/Rzg_bosonPt_no_cuts')
elif options.dataSource == 'reco':
    myfiles = {
	'Znunu'  : ROOT.TFile('rundir_z_'+options.meOrder+'_reco.root'),
	'Gamma'  : ROOT.TFile('rundir_gamma_reco.root'),
        }
#    reweighthist = reweightfile.Get('reco/Rzg_bosonPt_dPhi_'+options.reweightCuts)
    reweighthist = reweightfile.Get('truth/Rzg_bosonPt_dPhi_'+options.reweightCuts)
    zeffhist = reweightfile.Get('efficiency/Eff_bosonPt_z_'+options.reweightCuts)
    geffhist = reweightfile.Get('efficiency/Eff_bosonPt_gamma_'+options.reweightCuts)


inputdir = '/r04/atlas/khoo/Data_2015/zeroleptonRJR/v53_Data_pT50/'
cry_chain = ROOT.TChain('Data_CRY')
#for i in sorted(os.listdir(inputdir)):
#    cry_chain.Add(inputdir+i)
cry_chain.Add(inputdir+'Data_Nov11.root')

weightfile = ROOT.TFile('CRY_weights_RZG.root')
weighttree = weightfile.Get('CRY_weights_RZG')

cry_chain.AddFriend(weighttree)

outputdir =  'plots/'+options.dataSource+'/'

histoList = myfiles['Znunu'].GetListOfKeys()
#histoList.Print()

for counter, histoKey in enumerate(histoList) :
#    def printHisto( key ) :
    histos = {}
    if 'PROOF' in histoKey.GetName(): continue
    if 'EventLoop' in histoKey.GetName(): continue
    if 'Missing' in histoKey.GetName(): continue
    for name, ifile in myfiles.items() :
        hist=ifile.Get(histoKey.GetName())
        if hist.ClassName().startswith('TH3'):
            hist3d = hist
            if( not hist3d ) :
                continue
            if( not hist3d.GetEntries()) :
                continue
            #print histoKey.GetName()+ ' ' + str(name) +  ' ' + str(hist2d.GetEntries())
            if name=='Gamma':
                histos[name] = hist3d.ProjectionX(hist3d.GetName()+'_gamma')
                hist2d = hist3d.Project3D('xz')

                #print hist2d.GetYaxis().GetNbins(), hist2d.GetXaxis().GetNbins()
                hist2d.SetName(hist2d.GetName()+'_rw1')
                hist2d.Reset()
                histos[name+'Reweight'] = hist3d.ProjectionX(hist3d.GetName()+'_gammareweight')
                histos[name+'Reweight'].Reset()
                for ibin in range(1,hist3d.GetYaxis().GetNbins()+2):
                    yval = hist3d.GetYaxis().GetBinCenter(ibin)
                    if yval > reweighthist.GetXaxis().GetXmax(): yval = reweighthist.GetXaxis().GetXmax()*0.99
                    hist3d.GetYaxis().SetRange(ibin,ibin)
                    hist2d = hist3d.Project3D('zx')
                    if options.dataSource=='reco':
                        if zeffhist.Interpolate(yval)*geffhist.Interpolate(yval)>0:
                            hist2d.Scale(zeffhist.Interpolate(yval)/geffhist.Interpolate(yval))
                            #print zeffhist.Interpolate(yval)/geffhist.Interpolate(yval)
                    for jbin in range(1,hist2d.GetYaxis().GetNbins()+1):
                        zval = hist3d.GetZaxis().GetBinCenter(jbin)
                        if zval > reweighthist.GetYaxis().GetXmax(): zval = reweighthist.GetYaxis().GetXmax()*0.99
                        projx = hist2d.ProjectionX(hist2d.GetName()+'_gammaproj',jbin,jbin)
                        prescaleint = projx.Integral()
                        projx.Scale(reweighthist.Interpolate(yval,zval))
#                        print ibin, jbin, yval, zval
#                        print reweighthist.Interpolate(yval,zval), prescaleint, '==>', projx.Integral()
                        histos[name+'Reweight'].Add(projx)
                print 'integral:', histos[name].Integral(), '==>', histos[name+'Reweight'].Integral()
            else: print 'Not supposed to have TH3 for type', name
        elif hist.ClassName().startswith('TH1'):# and name.startswith('met'):
            histos[name] = hist
            if( not histos[name] ) :
                continue
            if( not histos[name].GetEntries()) :
                continue
            #print histoKey.GetName()+ ' ' + str(name) +  ' ' + str(histos[name].GetEntries())

    if( not name in histos ) :
        continue
    print histoKey

    c1 = ROOT.TCanvas('c1_'+histoKey.GetName().replace('$',''),
                      'c1_'+histoKey.GetName().replace('$',''),
                      600 , 600
                      )
    c1.Draw()

    pad1 = ROOT.TPad('pad1','pad1',0. ,0.3, 1.,1.)
    pad1.SetBottomMargin(0);
    #pad1.SetGrid(1,1)
    pad1.Draw()
    pad1.SetLogy()
    pad1.cd()

    histos['Znunu'].SetLineColor(ROOT.kRed)
    histos['Znunu'].SetMarkerColor(ROOT.kRed)
    histos['Znunu'].SetMarkerStyle(ROOT.kFullTriangleUp)
    histos['Znunu'].SetMarkerSize(0.7)
    histos['Gamma'].SetMarkerStyle(ROOT.kOpenSquare)
    histos['Gamma'].SetMarkerSize(0.7)
    histos['Znunu'].Scale(1000)
    histos['Gamma'].Scale(1000)

    leg4 = ROOT.TLegend(.6, 0.7, 0.9, 0.9) if 'GammaReweight' in histos.keys() else ROOT.TLegend(.6, 0.7, 0.9, 0.9)
    leg4.SetFillStyle(0)
    leg4.SetBorderSize(0)
    leg4.AddEntry(histos['Znunu'] , 'Znunu')

    if not ('minus' in histos['Znunu'].GetName() or 'cutflow' in histos['Znunu'].GetName()):
        histname_data = histos['Znunu'].GetName()+'_data'
        cutlevel = ''
        underscore_cut = False
        for i in ['no_cuts', 'base_meff', 'cry_tight', 'met50_2jet', 'met100_2jet', 'met300_2jet']:
            if i in histname_data:
                underscore_cut = True
                cutlevel = i
                break

        varname = ''
        if underscore_cut:
            varname = histname_data.rsplit('_',3)[0]
        else:
            varname,cutlevel = histname_data.rsplit('_',2)[0:2]
        if varname in varmappings: 
            histos['Data'] = histos['Znunu'].Clone(histname_data)
            histos['Data'].Reset()
            cry_chain.Draw('{var}>>{hist}'.format(
                    var=varmappings[varname], hist=histname_data, nbins=histos['Znunu'].GetNbinsX(),
                   ),'weight_RZG*(phSignal&&{cut})'.format(cut=cuts[cutlevel]))
            histos['Data'].SetMarkerStyle(ROOT.kFullCircle)
            histos['Data'].SetMarkerColor(ROOT.kBlack)
            histos['Data'].SetLineColor(ROOT.kBlack)
            leg4.AddEntry(histos['Data'] , 'CRY Data')

    # if histos['Gamma'].GetNbinsX() ==100 :
    #     for proc in histos.keys():
    #         histos[proc].Rebin(4)

    histos['Gamma'].Draw('p')
    histos['Znunu'].Draw('lsame')

    scalef = 1.
    if 'GammaReweight' in histos.keys():
        histos['GammaReweight'].SetLineColor(ROOT.kGreen+2)
        histos['GammaReweight'].SetMarkerColor(ROOT.kGreen+2)
        histos['GammaReweight'].SetMarkerStyle(ROOT.kFullSquare)
        histos['GammaReweight'].SetMarkerSize(0.7)

        histos['GammaReweight'].Scale(1000)
        scalef = histos['GammaReweight'].Integral()/histos['Gamma'].Integral() if histos['Gamma'].Integral()>0. else 0.
        histos['Gamma'].Scale(scalef)
        histos['GammaReweight'].Draw('psame')
        leg4.AddEntry(histos['Gamma'] , 'Gamma#bullet{0:.3f}'.format(scalef))
        leg4.AddEntry(histos['GammaReweight'] , 'Gamma#bulletR(Z/#gamma)')
    else:
        leg4.AddEntry(histos['Gamma'] , 'Gamma')
    if 'Data' in histos.keys(): histos['Data'].Draw('same')
    leg4.Draw('same')

    if 'Data' in  histos.keys():
        histos['Gamma'].SetMaximum(4*max(histos['Data'].GetMaximum(),histos['Znunu'].GetMaximum()))
        histos['Gamma'].SetMinimum(0.5*max(1,min(histos['Data'].GetMinimum(),histos['Znunu'].GetMinimum())))
    else:
        histos['Gamma'].SetMaximum(4*max(histos['Gamma'].GetMaximum(),histos['Znunu'].GetMaximum()))
        histos['Gamma'].SetMinimum(0.5*max(1,min(histos['Gamma'].GetMinimum(),histos['Znunu'].GetMinimum())))

    ratio = histos['Gamma'].Clone(histos['Gamma'].GetName()+'_ratgZ')
    ratio.Sumw2()
    ratio.Divide(histos['Znunu'])
    ratio.SetMinimum(0)
    ratio.SetMaximum(2.5)

    c1.cd()
    pad2 = ROOT.TPad('pad2','pad2',0. ,0.0, 1.,0.3  )
    pad2.SetTopMargin(0);
    pad2.SetGrid(0,1)
    pad2.Draw()
    pad2.cd()

    if 'cutflow' in histos['Znunu'].GetName():
        pad2.SetBottomMargin(0.6)
        pad2.SetRightMargin(0.3)
        pad1.SetRightMargin(0.3)
        histos['Gamma'].SetMinimum(1)

    ratio.GetYaxis().SetTitle('#gamma / Z');
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
    ratio.GetXaxis().SetTitle(histoKey.GetName().replace('RJVars','').replace('cry_tight','').replace('no_cuts','').replace('_','').replace('$','')) #RJVars_QCD_dPhiR_cry_tight

    ratio.Draw('l')
    if 'GammaReweight' in histos.keys():
        ratio2 = histos['GammaReweight'].Clone(histos['GammaReweight'].GetName()+'_ratGZ')
        ratio2.Sumw2()
        ratio2.Divide(histos['Znunu'])
        ratio2.Draw('psame')
    else:
        ratio.SetMaximum(15)
    if 'Data' in histos.keys():
        ratio3 = histos['Data'].Clone(histos['Data'].GetName()+'_ratDZ')
        ratio3.Sumw2()
        ratio3.Divide(histos['Znunu'])
        ratio3.Draw('psame')

    c1.cd()
    c1.Print(outputdir+c1.GetName()+'.eps')
    histos = None

#    printHisto(histoKey)

import time
#time.sleep(120)
