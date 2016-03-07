import copy

def cuts_from_dict(cutdict):
    return "*".join( ["(%s)"%mycut for mycut in cutdict.keys() ])

no_cuts = {}
no_cuts["1"] = [10,0,1000]

dphi   = {}
dphi["dPhi<4."] = [10, 0 , 4]

met50 = no_cuts.copy()
met50["met>50"] = [10,0,1000]

met100 = no_cuts.copy()
met100["met>100"] = [10,0,1000]

met160 = no_cuts.copy()
met160["met>160"] = [10,0,1000]

met300 = no_cuts.copy()
met300["met>300"] = [10,0,1000]

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
# print cry_cuts

## Define your cut strings here....
cuts = {
        "no_cuts"     : cuts_from_dict(no_cuts),
        "base_meff"   : cuts_from_dict(baseline_cuts),
        "cry_tight"   : cuts_from_dict(cry_cuts),
        "met50"       : cuts_from_dict(met50),
        "met100"      : cuts_from_dict(met100),
        "met160"      : cuts_from_dict(met160),
        "met300"      : cuts_from_dict(met300),
        "met50_2jet"  : cuts_from_dict(met50_2jet),
        "met100_2jet" : cuts_from_dict(met100_2jet),
        "met300_2jet" : cuts_from_dict(met300_2jet)
        }
