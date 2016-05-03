from ChannelConfig import * 
from RegionsDict import *
from GG_onestepCC_OptiChannels import *
from GG_direct_OptiChannels import *
from SS_direct_OptiChannels import *

###########################################################
# definition of the channels for plotting purpose
###########################################################

channelsForPlottingDict = {}

#SRs used for plotting
anaSR2jrun1 = ChannelConfig(name="SR2jrun1", regionDict=regionDict)
anaSR2jrun1.nJets = 2
anaSR2jrun1.jetpt1 = 130
anaSR2jrun1.jetpt2 = 60
anaSR2jrun1.MET = 160
anaSR2jrun1.dPhi = 0.4
#anaSR2jrun1.MET_over_meff  =  0.1
channelsForPlottingDict[anaSR2jrun1.name] = anaSR2jrun1

anaSR3jrun1 = ChannelConfig(name="SR3jrun1", regionDict=regionDict)
anaSR3jrun1.nJets = 3
anaSR3jrun1.jetpt1 = 130
anaSR3jrun1.jetpt2 = 60
anaSR3jrun1.jetpt3 = 60
anaSR3jrun1.MET = 160
anaSR3jrun1.dPhi = 0.4
#anaSR3jrun1.MET_over_meff  =  0.1
channelsForPlottingDict[anaSR3jrun1.name] = anaSR3jrun1

anaSR4jrun1 = ChannelConfig(name="SR4jrun1", regionDict=regionDict)
anaSR4jrun1.nJets = 4
anaSR4jrun1.jetpt1 = 130
anaSR4jrun1.jetpt2 = 60
anaSR4jrun1.jetpt3 = 60
anaSR4jrun1.jetpt4 = 60
anaSR4jrun1.MET = 160
anaSR4jrun1.dPhi = 0.4
#anaSR4jrun1.MET_over_meff  =  0.1
channelsForPlottingDict[anaSR4jrun1.name] = anaSR4jrun1

anaSR2jEPS = ChannelConfig(name="SR2jEPS", regionDict=regionDict)
anaSR2jEPS.nJets = 2
anaSR2jEPS.jetpt1 = 100
anaSR2jEPS.jetpt2 = 60
anaSR2jEPS.MET = 100
#anaSR2jEPS.dPhi = 0.4
channelsForPlottingDict[anaSR2jEPS.name] = anaSR2jEPS

anaSR2jlPres = ChannelConfig(name="SR2jlPres", regionDict=regionDict, fullname="SR2jbase-sljetpt200-dphi0.8")
anaSR2jlPres.nJets = 2
anaSR2jlPres.dPhi = 0.8
anaSR2jlPres.jetpt1 = 200.
anaSR2jlPres.jetpt2 = 200.
anaSR2jlPres.MET = 200.
channelsForPlottingDict[anaSR2jlPres.name] = anaSR2jlPres

anaSR2jmPres = ChannelConfig(name="SR2jmPres", regionDict=regionDict, fullname="SR2jbase-dphi0.4")
anaSR2jmPres.nJets = 2
anaSR2jmPres.dPhi = 0.4
anaSR2jmPres.jetpt1 = 200.
anaSR2jmPres.jetpt2 = 50.
anaSR2jmPres.MET = 200.
channelsForPlottingDict[anaSR2jmPres.name] = anaSR2jmPres

anaSR4jPres = ChannelConfig(name="SR4jPres", regionDict=regionDict, fullname="SR4jbase-dphi0.4")
anaSR4jPres.nJets = 4
anaSR4jPres.dPhi = 0.4
anaSR4jPres.MET = 200
anaSR4jPres.jetpt1 = 200.
anaSR4jPres.jetpt2 = 100.
anaSR4jPres.jetpt3 = 100.
anaSR4jPres.jetpt4 = 100.
channelsForPlottingDict[anaSR4jPres.name] = anaSR4jPres

anaSR5jPres = ChannelConfig(name="SR5jPres", regionDict=regionDict, fullname="SR5jbase-dphi0.4")
anaSR5jPres.nJets = 5
anaSR5jPres.dPhi = 0.4
anaSR5jPres.MET = 200.
anaSR5jPres.jetpt1 = 200.
anaSR5jPres.jetpt2 = 100.
anaSR5jPres.jetpt3 = 100.
anaSR5jPres.jetpt4 = 100.
anaSR5jPres.jetpt5 = 50.
channelsForPlottingDict[anaSR5jPres.name] = anaSR5jPres

anaSR6jPres = ChannelConfig(name="SR6jPres", regionDict=regionDict, fullname="SR6jbase-dphi0.4")
anaSR6jPres.nJets = 6
anaSR6jPres.dPhi = 0.4
anaSR6jPres.MET = 200.
anaSR6jPres.jetpt1 = 200.
anaSR6jPres.jetpt2 = 100.
anaSR6jPres.jetpt3 = 100.
anaSR6jPres.jetpt4 = 100.
anaSR6jPres.jetpt5 = 50.
anaSR6jPres.jetpt6 = 50.
channelsForPlottingDict[anaSR6jPres.name] = anaSR6jPres



