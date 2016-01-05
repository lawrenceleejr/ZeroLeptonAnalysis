import ROOT, math

cutlevels = ['no_cuts','met50','met160','base_meff']
rwvars = ['met','bosonPt','bosonEt','bosonEta','dPhi']

outfile = ROOT.TFile('ratZG.root','RECREATE')
for datasource in ['reco','truth']:
    outfile.mkdir(datasource)
    z_in = ROOT.TFile('rundir_z_lo_'+datasource+'.root') if datasource == 'truth' else ROOT.TFile('rundir_z_nlo_'+datasource+'.root')
    g_in = ROOT.TFile('rundir_gamma_'+datasource+'.root')

    for level in cutlevels:
        for rwvar in rwvars:
            zhist = z_in.Get(rwvar+'_'+level)
            ghist = g_in.Get(rwvar+'_'+level)
            rat = zhist.Clone('Rzg_{0}_{1}'.format(rwvar,level))
            rat.Divide(ghist)
            #rat.Scale(1./math.sqrt(rat.Integral()))
            outfile.cd(datasource)
            rat.Write()

        for rwpair in [('bosonPt','dPhi'),('bosonEt','dPhi')]:
            zhist = z_in.Get(rwpair[0]+'_'+rwpair[1]+'_'+level)
            ghist = g_in.Get(rwpair[0]+'_'+rwpair[1]+'_'+level)
            rat = zhist.Clone('Rzg_{0}_{1}_{2}'.format(rwpair[0],rwpair[1],level))
            rat.Divide(ghist)
            #rat.Scale(1./math.sqrt(rat.Integral()))
            outfile.cd(datasource)
            rat.Write()

        reweighthist1 = outfile.Get(datasource+'/Rzg_bosonPt_'+level)
        reweighthist2 = outfile.Get(datasource+'/Rzg_dPhi_'+level)
        #reweighthist2.Scale(1./reweighthist2.Integral())
        reweighthist = ROOT.TH2D('Rzg_bosonPt_dPhi_'+level+'_alt','Rzg_bosonPt_dPhi_'+level+'_alt',
                                 reweighthist1.GetNbinsX(),reweighthist1.GetXaxis().GetXmin(),reweighthist1.GetXaxis().GetXmax(),
                                 reweighthist2.GetNbinsX(),reweighthist2.GetXaxis().GetXmin(),reweighthist2.GetXaxis().GetXmax())
        for ibin in range(1,reweighthist1.GetNbinsX()+2):
            for jbin in range(1,reweighthist2.GetNbinsX()+1):
                reweighthist.SetBinContent(ibin,jbin,reweighthist1.GetBinContent(ibin)*reweighthist2.GetBinContent(jbin)*reweighthist2.GetNbinsX()/reweighthist2.Integral())
        reweighthist.Write()

effvars = ['bosonPt','bosonEta']
outfile.mkdir('efficiency')
for process in ['z','gamma']:
    reco_in = {'z':ROOT.TFile('rundir_z_nlo_reco.root'),'gamma':ROOT.TFile('rundir_gamma_reco.root')}[process]
    truth_in = {'z':ROOT.TFile('rundir_z_nlo_truth.root'),'gamma':ROOT.TFile('rundir_gamma_truth.root')}[process]
    for level in cutlevels:
        for effvar in effvars:
            recohist = reco_in.Get(effvar+'_'+level)
            truthhist = truth_in.Get(effvar+'_'+level)
            eff = recohist.Clone('Eff_{0}_{1}_{2}'.format(effvar,process,level))
            eff.Divide(truthhist)
            outfile.cd('efficiency')
            eff.Write()

outfile.Close()
