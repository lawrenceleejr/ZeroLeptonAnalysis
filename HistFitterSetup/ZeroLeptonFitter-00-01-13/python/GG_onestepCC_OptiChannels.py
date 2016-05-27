import pickle

from ChannelConfig import * 
from ChannelsDict import *


GG_onestepCCOptiChannels={}

meffList=[1400,1600,1800,2000,2200]
metomeffList=[0.15,0.2,0.25,0.3]
ApList=[0.04]
jetPtThresList=[50]
 

for meff in meffList:
    for metomeff in metomeffList:
        for jetPtThres in jetPtThresList:
            for Ap in ApList: 

                name=str(meff)+"-"+str(metomeff)+"-"+str(jetPtThres)
                name=name+"-"+str(Ap)

                ana = ChannelConfig(name="GGOSCC-5j-"+name, regionDict=regionDict, fullname="GGOSCC-5jbase-"+name)
                ana.nJets = 5
                ana.dPhi = 0.4
                ana.dPhiR = 0.2
                ana.MET_over_meffNj = metomeff
                ana.Ap = Ap
                ana.jetpt5 = jetPtThres
                ana.meffIncl = meff
                GG_onestepCCOptiChannels[ana.name] = ana


                ana = ChannelConfig(name="GGOSCC-6j-"+name, regionDict=regionDict, fullname="GGOSCC-6jbase-"+name)
                ana.nJets = 6
                ana.dPhi = 0.4
                ana.dPhiR = 0.2
                ana.MET_over_meffNj = metomeff
                ana.Ap = Ap
                ana.jetpt6 = jetPtThres
                ana.meffIncl = meff
                GG_onestepCCOptiChannels[ana.name] = ana


                ana = ChannelConfig(name="GGOSCC-7j-"+name, regionDict=regionDict, fullname="GGOSCC-7jbase-"+name)
                ana.nJets = 7
                ana.dPhi = 0.4
                ana.dPhiR = 0.2
                ana.MET_over_meffNj = metomeff
                ana.Ap = Ap
                ana.jetpt7 = jetPtThres
                ana.meffIncl = meff
                GG_onestepCCOptiChannels[ana.name] = ana



# myAna=[
#     ]
# for key,info in GG_onestepCCOptiChannels.items():
#     if key not in myAna: del GG_onestepCCOptiChannels[key]

pickle.dump(GG_onestepCCOptiChannels,open('GG_onestepCCOptiChannels.pkl','wb'))







