import pickle

from ChannelConfig import * 
from ChannelsDict import *


GG_directOptiChannels={}

meffList=[2600,2800,3000]
metomeffList=[0.2]
ApList=[0.02,0.04,0.06]
jet4PtList=[150]
 
for meff in meffList:
    for metomeff in metomeffList:
        for jet4Pt in jet4PtList:

            for Ap in ApList:

                name=str(meff)+"-"+str(metomeff)+"-"+str(jet4Pt)+"-"+str(Ap)          
                name=name.replace(".","")


                ana = ChannelConfig(name="GG-4j-"+name, regionDict=regionDict, fullname="GG-4jbase-"+name)
                ana.nJets = 4
                ana.dPhi = 0.4
                ana.dPhiR = 0.2
                ana.MET_over_meffNj = metomeff
                ana.Ap = Ap
                ana.jetpt4 = jet4Pt
                ana.meffIncl = meff
                GG_directOptiChannels[ana.name] = ana


                # ana = ChannelConfig(name="GG-5j-"+name, regionDict=regionDict, fullname="GG-5jbase-"+str(meff)+"_"+str(metomeff))
                # ana.nJets = 5
                # ana.dPhi = 0.4
                
                #                ana.jetpt4 = jet4Pt
                # ana.dPhiR = 0.2
                # ana.MET_over_meffNj = metomeff
                # ana.Ap = Ap
                # ana.meffIncl = meff
                # GG_directOptiChannels[ana.name] = ana
                




pickle.dump(GG_directOptiChannels,open('GG_directOptiChannels.pkl','wb'))


