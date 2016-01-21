import ROOT, math

cutlevels = ['no_cuts','met50','met160','base_meff']
rwvars = ['met','bosonPt','bosonEt','bosonEta','dPhi']

outfile = ROOT.TFile('ratZG.root','RECREATE')
for datasource in ['reco','truth']:
    outfile.mkdir(datasource)
    zvv_in = ROOT.TFile('rundir_zvv_lo_'+datasource+'.root') if datasource == 'truth' else ROOT.TFile('rundir_zvv_nlo_'+datasource+'.root')
    zll_in = ROOT.TFile('rundir_zll_lo_'+datasource+'.root') if datasource == 'truth' else ROOT.TFile('rundir_zll_nlo_'+datasource+'.root')
    g_in = ROOT.TFile('rundir_gamma_'+datasource+'.root')

    for level in cutlevels:
        for rwvar in rwvars:
            zvvhist = zvv_in.Get(rwvar+'_'+level)
            ghist = g_in.Get(rwvar+'_'+level)

            print zvvhist, ghist
            rat = zvvhist.Clone('Rzvvg_{0}_{1}'.format(rwvar,level))
            rat.Divide(ghist)
            #rat.Scale(1./math.sqrt(rat.Integral()))
            outfile.cd(datasource)
            rat.Write()

            if datasource=='reco':
                zllhist = zll_in.Get(rwvar+'_'+level)
                print zllhist, ghist
                rat2 = zllhist.Clone('Rzllg_{0}_{1}'.format(rwvar,level))
                rat2.Divide(ghist)
                #rat2.Scale(1./math.sqrt(rat2.Integral()))
                outfile.cd(datasource)
                rat2.Write()

        for rwpair in [('bosonPt','dPhi'),('bosonEt','dPhi')]:
            zvvhist = zvv_in.Get(rwpair[0]+'_'+rwpair[1]+'_'+level)
            ghist = g_in.Get(rwpair[0]+'_'+rwpair[1]+'_'+level)

            rat = zvvhist.Clone('Rzvvg_{0}_{1}'.format(rwvar,level))
            rat.Divide(ghist)
            #rat.Scale(1./math.sqrt(rat.Integral()))
            outfile.cd(datasource)
            rat.Write()

            if datasource=='reco':
                zllhist = zll_in.Get(rwpair[0]+'_'+rwpair[1]+'_'+level)
                ghist = g_in.Get(rwpair[0]+'_'+rwpair[1]+'_'+level)

                rat2 = zllhist.Clone('Rzvvg_{0}_{1}_{2}'.format(rwpair[0],rwpair[1],level))
                rat2.Divide(ghist)
                #rat.Scale(1./math.sqrt(rat.Integral()))
                outfile.cd(datasource)
                rat2.Write()

effvars = ['bosonPt','bosonEta']
outfile.mkdir('efficiency')
for process in ['zvv','gamma']:#'zll'
    reco_in = {'zvv':ROOT.TFile('rundir_zvv_nlo_reco.root'),'zll':ROOT.TFile('rundir_zll_nlo_reco.root'),'gamma':ROOT.TFile('rundir_gamma_reco.root')}[process]
    truth_in = {'zvv':ROOT.TFile('rundir_zvv_nlo_truth.root'),'zll':ROOT.TFile('rundir_zll_nlo_truth.root'),'gamma':ROOT.TFile('rundir_gamma_truth.root')}[process]
    for level in cutlevels:
        for effvar in effvars:
            recohist = reco_in.Get(effvar+'_'+level)
            truthhist = truth_in.Get(effvar+'_'+level)
            eff = recohist.Clone('Eff_{0}_{1}_{2}'.format(effvar,process,level))
            eff.Divide(truthhist)
            outfile.cd('efficiency')
            eff.Write()

        for effpair in [('bosonPt','bosonEta')]:
            recohist = reco_in.Get(effpair[0]+'_'+effpair[1]+'_'+level)
            truthhist = truth_in.Get(effpair[0]+'_'+effpair[1]+'_'+level)
            eff = recohist.Clone('Eff_{0}_{1}_{2}_{3}'.format(effpair[0],effpair[1],process,level))
            eff.Divide(truthhist)
            outfile.cd('efficiency')
            eff.Write()

outfile.Close()
