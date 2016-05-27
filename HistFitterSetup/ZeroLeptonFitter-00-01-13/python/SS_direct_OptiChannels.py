import pickle

from ChannelConfig import * 
from ChannelsDict import *


SS_directOptiChannels={}

meffList=[1200,1400,1600,1800,2000,2200,2400,2600]
metsigList=[16,18,20,22]
dPhiList=[0.4,0.8]
jetPtList=[200]

for meff in meffList:
    for metsig in metsigList:
        for dPhi in dPhiList:
            for jetPt in jetPtList:


                name=str(meff)+"-"+str(metsig)+"-"+str(dPhi)+"-"+str(jetPt)
                
                ana = ChannelConfig(name="SS-2j-"+name, regionDict=regionDict, fullname="SS-2jbase-"+name)
                ana.nJets = 2
                ana.dPhi = dPhi
                ana.METsig = metsig
                ana.MET_over_meffNj = 0.0
                ana.jetPtThreshold = jetPt
                ana.meffIncl = meff
                SS_directOptiChannels[ana.name] = ana




                # ana = ChannelConfig(name="SS-3j-"+name, regionDict=regionDict, fullname="SS-3jbase-"+name)
                # ana.nJets = 3
                # ana.dPhi = dPhi
                # ana.METsig = metsig
                # ana.jetPtThreshold = jetPt
                # ana.meffIncl = meff
                # SS_directOptiChannels[ana.name] = ana

#save signal regions in a pkl file
pickle.dump(SS_directOptiChannels,open('SS_directOptiChannels.pkl','wb'))

