from ChannelConfig import * 
from RegionsDict import *
from GG_onestepCC_OptiChannels import *
from GG_direct_OptiChannels import *
from SS_direct_OptiChannels import *

from ChannelsDict_Plotting import *
from ChannelsDict_2015Paper import *

from RJigsawChannelDict import *

###########################################################
# definition of the final analysis channels
###########################################################

# FAR SRs
finalChannelsDict = {}

anaSR2jW = ChannelConfig(name="SR2jW", regionDict=regionDict, fullname="")
anaSR2jW.nJets = 2
anaSR2jW.dPhi = 0.4
anaSR2jW.METsig = 20
anaSR2jW.MET_over_meffNj = 0.0
anaSR2jW.jetpt1 = 50
anaSR2jW.jetpt2 = 50
anaSR2jW.fatjet1MassMin = 60
anaSR2jW.fatjet1MassMax = 100
anaSR2jW.fatjet2MassMin = 60
anaSR2jW.fatjet2MassMax = 100
anaSR2jW.meffIncl = 1800
finalChannelsDict[anaSR2jW.name] = anaSR2jW


anaSR2jZ = ChannelConfig(name="SR2jZ", regionDict=regionDict, fullname="")
anaSR2jZ.nJets = 2
anaSR2jZ.dPhi = 0.4
anaSR2jZ.METsig = 20
anaSR2jZ.MET_over_meffNj = 0.0
anaSR2jZ.jetpt1 = 50
anaSR2jZ.jetpt2 = 50
anaSR2jZ.fatjet1MassMin = 70
anaSR2jZ.fatjet1MassMax = 110
anaSR2jZ.fatjet2MassMin = 70
anaSR2jZ.fatjet2MassMax = 110
anaSR2jZ.meffIncl = 1800
finalChannelsDict[anaSR2jZ.name] = anaSR2jZ




anaSR2jtprime = ChannelConfig(name="SR2jtprime", regionDict=regionDict, fullname="")
anaSR2jtprime.nJets = 2
anaSR2jtprime.dPhi = 0.8
anaSR2jtprime.METsig = 14
anaSR2jtprime.MET_over_meffNj = 0.0
anaSR2jtprime.jetpt1 = 200
anaSR2jtprime.jetpt2 = 200
anaSR2jtprime.meffIncl = 1800
finalChannelsDict[anaSR2jtprime.name] = anaSR2jtprime


anaSR3j = ChannelConfig(name="SR3j", regionDict=regionDict, fullname="")
anaSR3j.nJets = 3
anaSR3j.dPhi = 0.4
anaSR3j.METsig = 14
anaSR3j.meffIncl = 1200
finalChannelsDict[anaSR3j.name] = anaSR3j


anaSR4jl = ChannelConfig(name="SR4jl", regionDict=regionDict, fullname="")
anaSR4jl.nJets = 4
anaSR4jl.dPhi = 0.4
anaSR4jl.dPhiR = 0.2
anaSR4jl.MET_over_meffNj = 0.25
anaSR4jl.Ap=0.04
anaSR4jl.jetpt4 = 50
anaSR4jl.meffIncl = 1200
finalChannelsDict[anaSR4jl.name] = anaSR4jl


anaSR4jm = ChannelConfig(name="SR4jm", regionDict=regionDict, fullname="")
anaSR4jm.nJets = 4
anaSR4jm.dPhi = 0.4
anaSR4jm.dPhiR = 0.2
anaSR4jm.MET_over_meffNj = 0.2
anaSR4jm.Ap=0.04
anaSR4jm.jetpt4 = 50
anaSR4jm.meffIncl = 1800
finalChannelsDict[anaSR4jm.name] = anaSR4jm


anaSR4jtprime = ChannelConfig(name="SR4jtprime", regionDict=regionDict, fullname="")
anaSR4jtprime.nJets = 4
anaSR4jtprime.dPhi = 0.4
anaSR4jtprime.dPhiR = 0.2
anaSR4jtprime.MET_over_meffNj = 0.2
anaSR4jtprime.Ap=0.04
anaSR4jtprime.jetpt4 = 150
anaSR4jtprime.meffIncl = 2400
finalChannelsDict[anaSR4jtprime.name] = anaSR4jtprime


anaSR5jt = ChannelConfig(name="SR5jt", regionDict=regionDict, fullname="")
anaSR5jt.nJets = 5
anaSR5jt.dPhi = 0.4
anaSR5jt.dPhiR = 0.2
anaSR5jt.MET_over_meffNj = 0.15
anaSR5jt.Ap=0.04
anaSR5jt.meffIncl = 2200
finalChannelsDict[anaSR5jt.name] = anaSR5jt



anaSR6jmprime = ChannelConfig(name="SR6jmprime", regionDict=regionDict, fullname="")
anaSR6jmprime.nJets = 6
anaSR6jmprime.dPhi = 0.4
anaSR6jmprime.dPhiR = 0.2
anaSR6jmprime.MET_over_meffNj = 0.2
anaSR6jmprime.Ap=0.04
anaSR6jmprime.meffIncl = 1400
finalChannelsDict[anaSR6jmprime.name] = anaSR6jmprime

anaSR7j = ChannelConfig(name="SR7j", regionDict=regionDict, fullname="")
anaSR7j.nJets = 7
anaSR7j.dPhi = 0.4
anaSR7j.dPhiR = 0.2
anaSR7j.MET_over_meffNj = 0.15
anaSR7j.Ap=0.04
anaSR7j.meffIncl = 2000
finalChannelsDict[anaSR7j.name] = anaSR7j




###########################################################
# Opti
###########################################################
#finalChannelsDict.update(GG_directOptiChannels)
#finalChannelsDict.update(SS_directOptiChannels)
#finalChannelsDict.update(GG_onestepCCOptiChannels)
#finalChannelsDict.update(newChannelsDict)
#finalChannelsDict=newChannelsDict

###########################################################
# all channels
###########################################################

allChannelsDict = finalChannelsDict.copy()
allChannelsDict.update(channelsForPlottingDict)
allChannelsDict.update(RJigsawChannelDict)




