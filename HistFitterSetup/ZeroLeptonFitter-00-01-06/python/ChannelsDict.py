
from ChannelConfig import *

###########################################################
# definition of the control regions
###########################################################

cleaningCut="( abs(m_jet1_eta)>2.4 || m_jet1_chf/m_jet1_FracSamplingMax>0.1)"

regionDict={}
regionDict["SR"] = Region("SR", "SRAll", [cleaningCut], [])

regionDict["CRW"] = Region("CRW", "CRWT", ["nBJet==0"], ["bTagWeight"])
regionDict["CRT"] = Region("CRT", "CRWT", ["nBJet>0"], ["bTagWeight"])
# regionDict["CRT"] = Region("CRT", "SRAll", ["nBJet>0"], ["bTagWeight"])
#regionDict["CRTZL"] = Region("CRTZL", "SRAll", ["nBJet>0",cleaningCut], ["bTagWeight"])
regionDict["CRWT"] = Region("CRWT", "CRWT", ["nBJet>=0"], ["bTagWeight"])


# regionDict["VRWf"] = Region("VRWf", "CRWT", ["nBJet==0"], ["bTagWeight"]) #ATT: systWeights[0] is a proxy for the lepton weight
# regionDict["VRTf"] = Region("VRTf", "CRWT", ["nBJet>0"], ["bTagWeight"])

# regionDict["VRWMf"] = Region("VRWMf", "VRWT", ["nBJet==0"], ["bTagWeight"])
# regionDict["VRTMf"] = Region("VRTMf", "VRWT", ["nBJet>0"], ["bTagWeight"])
# regionDict["VRWM"] = Region("VRWM", "VRWT", ["nBJet==0"], ["bTagWeight"])
# regionDict["VRTM"] = Region("VRTM", "VRWT", ["nBJet>0"], ["bTagWeight"])

# regionDict["CRZ"] = Region("CRZ", "CRZ", [], [])

# regionDict["VRWTplus"] = Region("VRWTplus", "CRWT", ["lep1sign>0"], ["bTagWeight"])
# regionDict["VRWTminus"] = Region("VRWTminus", "CRWT", ["lep1sign<0"], ["bTagWeight"])
# regionDict["VRWTfplus"] = Region("VRWTfplus", "CRWT", ["lep1sign>0"], ["bTagWeight"])
# regionDict["VRWTfminus"] = Region("VRWTfminus", "CRWT", ["lep1sign<0"], ["bTagWeight"])

# regionDict["CRY"] = Region("CRY", "CRY", ["(phSignal[0]==1)"], [" 1.6 "])#extra weights should be applied only to gamma+jets
regionDict["CRY"] = Region("CRY", "CRY", ["(phSignal[0]==1 && phPt[0]>130.)"], [])#extra weights should be applied only to gamma+jets
# regionDict["VRYf"] = Region("VRY", "CRY", ["(phSignal[0]==1 && phPt[0]>130.)"], ["1.6"])#extra weights should be applied only to gamma+jets

regionDict["CRQ"] = Region("CRQ", "SRAll", [cleaningCut])#ATT: qcd weight
regionDict["VRQ"] = Region("VRQ", "SRAll", [cleaningCut])#ATT: qcd weight
# regionDict["VRQ2"] = Region("VRQ2", "SRAll", [cleaningCut])#ATT: qcd weight
# regionDict["VRQ3"] = Region("VRQ3", "SRAll", [cleaningCut])#ATT: qcd weight
# regionDict["VRQ4"] = Region("VRQ4", "SRAll", [cleaningCut])#ATT: qcd weight

regionDict["VRZ"] = Region("VRZ", "CRZ", [], [])
regionDict["VRZa"] = Region("VRZa", "CRZ", [], [])
regionDict["VRZb"] = Region("VRZb", "CRZ", [], [])
regionDict["VRTZL"] = Region("VRTZL", "SRAll", ["nBJet>0",cleaningCut], ["bTagWeight"])

# regionDict["VRZf"] = Region("VRZf", "CRZ", [], [])

# regionDict["VRT2L"] = Region("VRT2L", "CRZ_VR1b", ["(mll>116000 &&  lep1Pt<200000 && lep2Pt<100000)"], [])#ATT: qcd weight


# ##for data-driven BG estimation##
regionDict["VRW"] = Region("VRW", "CRWT", ["nBJet==0"], ["bTagWeight"])
regionDict["VRWa"] = Region("VRWa", "CRWT", ["nBJet==0"], ["bTagWeight"])
regionDict["VRWb"] = Region("VRWb", "CRWT", ["nBJet==0"], ["bTagWeight"])
# regionDict["CRWL"] = Region("VRWL", "CRWT", ["nBJet==0"], ["bTagWeight"])
# regionDict["CRWVL"] = Region("VRWVL", "CRWT", ["nBJet==0"], ["bTagWeight"])
regionDict["VRT"] = Region("VRT", "CRWT", ["nBJet>0"], ["bTagWeight"])
regionDict["VRTa"] = Region("VRTa", "CRWT", ["nBJet>0"], ["bTagWeight"])
regionDict["VRTb"] = Region("VRTb", "CRWT", ["nBJet>0"], ["bTagWeight"])
# regionDict["CRTL"] = Region("VRTL", "CRWT", ["nBJet>0"], ["bTagWeight"])
# regionDict["CRTVL"] = Region("VRTVL", "CRWT", ["nBJet>0"], ["bTagWeight" ])
# regionDict["CRYL"] = Region("CRYL", "CRY", ["(phSignal==1 && phPt>130."], [])#extra weights should be applied only to gamma+jets
# regionDict["CRZL"] = Region("CRZL", "CRZ", [], [])
# regionDict["CRZVL"] = Region("CRZVL", "CRZ", [], [])
# regionDict["SRZVL"] = Region("SRZVL", "SRAll", ["( abs(jetEta[0])>2.4 || jet1Chf/jetFracSamplingMax[0]>0.1)"], [])






###########################################################
# definition of the final analysis channels
###########################################################

# FAR SRs
finalChannelsDict = {}

#SS_direct_800_400 2jl
# SR2jbase-MeSig15-Meff1200-sljetpt200-dphi0.8-ap0.00
anaSRFAR = ChannelConfig(name="SR2jl", regionDict=regionDict, fullname="SR2jbase-MeSig15-Meff1200-sljetpt200-dphi0.8-ap0.00")
anaSRFAR.nJets = 2
anaSRFAR.dPhi = 0.8
anaSRFAR.MET_over_meffNj = 0.0
anaSRFAR.METsig = 15
anaSRFAR.jetpt1 = 200.
anaSRFAR.jetpt2 = 200.
anaSRFAR.meffIncl = 1200
finalChannelsDict[anaSRFAR.name] = anaSRFAR

#GG_direct_750_650, GG_onestep_825_785_745 2jm
# SR2jbase-MeSig20-Meff1800-sljetpt60-dphi0.4-ap0.00
anaSRFAR = ChannelConfig(name="SR2jm", regionDict=regionDict, fullname="SR2jbase-MeSig20-Meff1800-sljetpt50-dphi0.4-ap0.00")
anaSRFAR.nJets = 2
anaSRFAR.dPhi = 0.4
anaSRFAR.MET_over_meffNj = 0.0
anaSRFAR.METsig = 20
anaSRFAR.jetpt1 = 200.
anaSRFAR.jetpt2 = 50.
anaSRFAR.meffIncl = 1800
finalChannelsDict[anaSRFAR.name] = anaSRFAR

#SS_direct_1200_0 2jt
# SR2jbase-MeSig20-Meff2000-sljetpt200-dphi0.8-ap0.00
anaSRFAR = ChannelConfig(name="SR2jt", regionDict=regionDict, fullname="SR2jbase-MeSig20-Meff2000-sljetpt200-dphi0.8-ap0.00")
anaSRFAR.nJets = 2
anaSRFAR.dPhi = 0.8
anaSRFAR.MET_over_meffNj = 0.0
anaSRFAR.METsig = 20
anaSRFAR.jetpt1 = 200.
anaSRFAR.jetpt2 = 200.
anaSRFAR.meffIncl = 2000
finalChannelsDict[anaSRFAR.name] = anaSRFAR

# GG_direct_1400_0 4jt
anaSRFAR = ChannelConfig(name="SR4jt", regionDict=regionDict, fullname="SR4jbase-MetoMeff0.2-Meff2200-sljetpt100-34jetpt100-dphi0.4-ap0.04")
anaSRFAR.nJets = 4
anaSRFAR.dPhi = 0.4
anaSRFAR.dPhiR = 0.2
anaSRFAR.MET_over_meffNj = 0.2
anaSRFAR.MET = 200
anaSRFAR.METsig = 0
anaSRFAR.Ap = 0.04
anaSRFAR.jetpt1 = 200.
anaSRFAR.jetpt2 = 100.
anaSRFAR.jetpt3 = 100.
anaSRFAR.jetpt4 = 100.
anaSRFAR.meffIncl = 2200
finalChannelsDict[anaSRFAR.name] = anaSRFAR

#GG_onestepCC_1265_945_625 at 4/fb 5j
# SR5jbase-MetoMeff0.25-Meff1600-sljetpt100-34jetpt100-dphi0.4-ap0.02
anaSRFAR = ChannelConfig(name="SR5j", regionDict=regionDict, fullname="SR5jbase-MetoMeff0.25-Meff1600-sljetpt100-34jetpt100-dphi0.4-ap0.04")
anaSRFAR.nJets = 5
anaSRFAR.dPhi = 0.4
anaSRFAR.dPhiR = 0.2
anaSRFAR.MET_over_meffNj = 0.25
anaSRFAR.METsig = 0
anaSRFAR.Ap = 0.04
anaSRFAR.jetpt1 = 200.
anaSRFAR.jetpt2 = 100.
anaSRFAR.jetpt3 = 100.
anaSRFAR.jetpt4 = 100.
anaSRFAR.jetpt5 = 50.
anaSRFAR.meffIncl = 1600
finalChannelsDict[anaSRFAR.name] = anaSRFAR

#GG_onestepCC_1265_945_625 at 4/fb 6jm
# SR6jbase-MetoMeff0.25-Meff1600-sljetpt100-34jetpt100-dphi0.4-ap0.02
anaSRFAR = ChannelConfig(name="SR6jm", regionDict=regionDict, fullname="SR6jbase-MetoMeff0.25-Meff1600-sljetpt100-34jetpt100-dphi0.4-ap0.04")
anaSRFAR.nJets = 6
anaSRFAR.dPhi = 0.4
anaSRFAR.dPhiR = 0.2
anaSRFAR.MET_over_meffNj = 0.25
anaSRFAR.METsig = 0
anaSRFAR.Ap = 0.04
anaSRFAR.jetpt1 = 200.
anaSRFAR.jetpt2 = 100.
anaSRFAR.jetpt3 = 100.
anaSRFAR.jetpt4 = 100.
anaSRFAR.jetpt5 = 50.
anaSRFAR.jetpt6 = 50.
anaSRFAR.meffIncl = 1600
finalChannelsDict[anaSRFAR.name] = anaSRFAR

#GG_onestepCC_1545_785_25 at 4/fb
# SR6jbase-MetoMeff0.2-Meff1800-sljetpt100-34jetpt100-dphi0.4-ap0.02
anaSRFAR = ChannelConfig(name="SR6jt", regionDict=regionDict, fullname="SR6jbase-MetoMeff0.2-Meff1800-sljetpt100-34jetpt100-dphi0.4-ap0.04")
anaSRFAR.nJets = 6
anaSRFAR.dPhi = 0.4
anaSRFAR.dPhiR = 0.2
anaSRFAR.MET_over_meffNj = 0.2
anaSRFAR.METsig = 0
anaSRFAR.Ap = 0.04
anaSRFAR.jetpt1 = 200.
anaSRFAR.jetpt2 = 100.
anaSRFAR.jetpt3 = 100.
anaSRFAR.jetpt4 = 100.
anaSRFAR.jetpt5 = 50.
anaSRFAR.jetpt6 = 50.
anaSRFAR.meffIncl = 2000
finalChannelsDict[anaSRFAR.name] = anaSRFAR














# ###########################################################
# # definition of the channels for plotting purpose
# ###########################################################

# channelsForPlottingDict = {}

# #SRs used for plotting
# anaSR2jrun1 = ChannelConfig(name="SR2jrun1", regionDict=regionDict)
# anaSR2jrun1.nJets = 2
# anaSR2jrun1.jetpt1 = 130
# anaSR2jrun1.jetpt2 = 60
# anaSR2jrun1.MET = 160
# anaSR2jrun1.dPhi = 0.4
# #anaSR2jrun1.MET_over_meff  =  0.1
# channelsForPlottingDict[anaSR2jrun1.name] = anaSR2jrun1

# anaSR3jrun1 = ChannelConfig(name="SR3jrun1", regionDict=regionDict)
# anaSR3jrun1.nJets = 3
# anaSR3jrun1.jetpt1 = 130
# anaSR3jrun1.jetpt2 = 60
# anaSR3jrun1.jetpt3 = 60
# anaSR3jrun1.MET = 160
# anaSR3jrun1.dPhi = 0.4
# #anaSR3jrun1.MET_over_meff  =  0.1
# channelsForPlottingDict[anaSR3jrun1.name] = anaSR3jrun1

# anaSR4jrun1 = ChannelConfig(name="SR4jrun1", regionDict=regionDict)
# anaSR4jrun1.nJets = 4
# anaSR4jrun1.jetpt1 = 130
# anaSR4jrun1.jetpt2 = 60
# anaSR4jrun1.jetpt3 = 60
# anaSR4jrun1.jetpt4 = 60
# anaSR4jrun1.MET = 160
# anaSR4jrun1.dPhi = 0.4
# #anaSR4jrun1.MET_over_meff  =  0.1
# channelsForPlottingDict[anaSR4jrun1.name] = anaSR4jrun1

# anaSR2jEPS = ChannelConfig(name="SR2jEPS", regionDict=regionDict)
# anaSR2jEPS.nJets = 2
# anaSR2jEPS.jetpt1 = 100
# anaSR2jEPS.jetpt2 = 60
# anaSR2jEPS.MET = 100
# #anaSR2jEPS.dPhi = 0.4
# channelsForPlottingDict[anaSR2jEPS.name] = anaSR2jEPS


# ###########################################################
# # special channel to compute kappa
# # very loose selection to compute kappa correction
# # CRT and CRW should be add as constraining regions
# # CRZ and VRZ should be add as validation regions
# ###########################################################
# #finalChannelsDict={}
# anaVL=ChannelConfig(name="VLForKappa",regionDict=regionDict)
# anaVL.nJets=2
# anaVL.dPhi=0
# anaVL.MET=200
# anaVL.MET_upper=300
# anaVL.jetpt1 = 200.
# #finalChannelsDict[anaVL.name]=anaVL

# ###########################################################
# # SR for testing the fit
# # Upper cut on meff are applied
# ###########################################################

# testChannelsDict={}

# anaSR = ChannelConfig(name="SR2jTest", regionDict=regionDict)
# anaSR.nJets = 2
# anaSR.dPhi = 0.4
# anaSR.METsig = 10
# anaSR.jetpt1 = 200.
# anaSR.meffIncl = 800
# anaSR.meffInclUpperCut = 1000
# testChannelsDict[anaSR.name] = anaSR


# anaSR = ChannelConfig(name="SR3jTest", regionDict=regionDict)
# anaSR.nJets = 3
# anaSR.dPhi = 0.4
# anaSR.METsig = 10
# anaSR.jetpt1 = 200.
# anaSR.meffIncl = 800
# anaSR.meffInclUpperCut = 1000
# testChannelsDict[anaSR.name] = anaSR


# anaSR = ChannelConfig(name="SR4jTest", regionDict=regionDict)
# anaSR.nJets = 4
# anaSR.dPhi = 0.4
# anaSR.dPhiR = 0.2
# anaSR.METsig = 10
# #anaSR.MET_over_meffNj = 0.15
# anaSR.jetpt1 = 200.
# anaSR.meffIncl = 800
# anaSR.meffInclUpperCut = 1000
# testChannelsDict[anaSR.name] = anaSR


# anaSR = ChannelConfig(name="SR5jTest", regionDict=regionDict)
# anaSR.nJets = 5
# anaSR.dPhi = 0.4
# anaSR.dPhiR = 0.2
# anaSR.METsig = 10
# #anaSR.MET_over_meffNj = 0.2
# anaSR.jetpt1 = 200.
# anaSR.meffIncl = 800
# anaSR.meffInclUpperCut = 1000
# testChannelsDict[anaSR.name] = anaSR



# anaSR = ChannelConfig(name="SR6jTest", regionDict=regionDict)
# anaSR.nJets = 6
# anaSR.dPhi = 0.4
# anaSR.dPhiR = 0.2
# anaSR.METsig = 10
# #anaSR.MET_over_meffNj = 0.2
# anaSR.jetpt1 = 200.
# anaSR.meffIncl = 800
# anaSR.meffInclUpperCut = 1000
# testChannelsDict[anaSR.name] = anaSR



# #This is temporary and will be removed with the actual SR to find SUSY
# #to be removed
# #finalChannelsDict=testChannelsDict
# #finalChannelsDict.update(testChannelsDict)












# finalChannelsDict = {}




#----------------------------------------------------------
# RJigsaw
#----------------------------------------------------------
anaSRJigsawBasic=ChannelConfig(name="SRJigsawBasic",regionDict=regionDict)

# trigger
anaSRJigsawBasic.met=100
anaSRJigsawBasic.MDR=300
anaSRJigsawBasic.deltaQCD=0


anaSRJigsawCoBasic=ChannelConfig(name="SRJigsawCoBasic",regionDict=regionDict)

# trigger
anaSRJigsawCoBasic.met=100


#----------------------------------------------------------
# RJigsaw SRs - Gluinos
#----------------------------------------------------------

import copy

###################################################################


anaSRJigsawSRG1Common = copy.deepcopy( anaSRJigsawBasic )
anaSRJigsawSRG1Common.name = "SRJigsawSRG1Common"
anaSRJigsawSRG1Common.RPTHT5PP_upper = 0.08
anaSRJigsawSRG1Common.R_H2PP_H5PP = 0.35
anaSRJigsawSRG1Common.R_HT5PP_H5PP = 0.8
anaSRJigsawSRG1Common.RPZ_HT5PP_upper = 0.5
anaSRJigsawSRG1Common.minR_pTj2i_HT3PPi = 0.125
anaSRJigsawSRG1Common.maxR_H1PPi_H2PPi_upper = 0.95
anaSRJigsawSRG1Common.dangle_upper = 0.5
anaSRJigsawSRG1Common.nJets = 4
anaSRJigsawSRG1Common.HT5PP_loose = 800
anaSRJigsawSRG1Common.H2PP_loose = 550

anaSRJigsawSRG1a = copy.deepcopy( anaSRJigsawSRG1Common )
anaSRJigsawSRG1a.name = "SRJigsawSRG1a"
anaSRJigsawSRG1a.HT5PP = 800
anaSRJigsawSRG1a.H2PP = 550

finalChannelsDict[anaSRJigsawSRG1a.name]=anaSRJigsawSRG1a


anaSRJigsawSRG1b = copy.deepcopy( anaSRJigsawSRG1Common )
anaSRJigsawSRG1b.name = "SRJigsawSRG1b"
anaSRJigsawSRG1b.HT5PP = 1000
anaSRJigsawSRG1b.H2PP = 550

finalChannelsDict[anaSRJigsawSRG1b.name]=anaSRJigsawSRG1b

anaSRJigsawSRG1c = copy.deepcopy( anaSRJigsawSRG1Common )
anaSRJigsawSRG1c.name = "SRJigsawSRG1c"
anaSRJigsawSRG1c.HT5PP = 1200
anaSRJigsawSRG1c.H2PP = 550

finalChannelsDict[anaSRJigsawSRG1c.name]=anaSRJigsawSRG1c

###################################################################

###################################################################


anaSRJigsawSRG2Common = copy.deepcopy( anaSRJigsawBasic )
anaSRJigsawSRG2Common.name = "SRJigsawSRG2Common"
anaSRJigsawSRG2Common.RPTHT5PP_upper = 0.08
anaSRJigsawSRG2Common.R_H2PP_H5PP = 0.25
anaSRJigsawSRG2Common.R_HT5PP_H5PP = 0.75
anaSRJigsawSRG2Common.RPZ_HT5PP_upper = 0.55
anaSRJigsawSRG2Common.minR_pTj2i_HT3PPi = 0.11
anaSRJigsawSRG2Common.maxR_H1PPi_H2PPi_upper = 0.97
anaSRJigsawSRG2Common.nJets = 4
anaSRJigsawSRG2Common.HT5PP_loose = 800
anaSRJigsawSRG2Common.H2PP_loose = 550

anaSRJigsawSRG2a = copy.deepcopy( anaSRJigsawSRG2Common )
anaSRJigsawSRG2a.name = "SRJigsawSRG2a"
anaSRJigsawSRG2a.HT5PP = 1400
anaSRJigsawSRG2a.H2PP = 750

finalChannelsDict[anaSRJigsawSRG2a.name]=anaSRJigsawSRG2a


anaSRJigsawSRG2b = copy.deepcopy( anaSRJigsawSRG2Common )
anaSRJigsawSRG2b.name = "SRJigsawSRG2b"
anaSRJigsawSRG2b.HT5PP = 1600
anaSRJigsawSRG2b.H2PP = 750

finalChannelsDict[anaSRJigsawSRG2b.name]=anaSRJigsawSRG2b

anaSRJigsawSRG2c = copy.deepcopy( anaSRJigsawSRG2Common )
anaSRJigsawSRG2c.name = "SRJigsawSRG2c"
anaSRJigsawSRG2c.HT5PP = 1800
anaSRJigsawSRG2c.H2PP = 750

finalChannelsDict[anaSRJigsawSRG2c.name]=anaSRJigsawSRG2c

###################################################################

###################################################################


anaSRJigsawSRG3Common = copy.deepcopy( anaSRJigsawBasic )
anaSRJigsawSRG3Common.name = "SRJigsawSRG3Common"
anaSRJigsawSRG3Common.RPTHT5PP_upper = 0.08
anaSRJigsawSRG3Common.R_H2PP_H5PP = 0.2
anaSRJigsawSRG3Common.R_HT5PP_H5PP = 0.65
anaSRJigsawSRG3Common.RPZ_HT5PP_upper = 0.6
anaSRJigsawSRG3Common.minR_pTj2i_HT3PPi = 0.09
anaSRJigsawSRG3Common.maxR_H1PPi_H2PPi_upper = 0.98
anaSRJigsawSRG3Common.nJets = 4
anaSRJigsawSRG3Common.HT5PP_loose = 800
anaSRJigsawSRG3Common.H2PP_loose = 550

anaSRJigsawSRG3a = copy.deepcopy( anaSRJigsawSRG3Common )
anaSRJigsawSRG3a.name = "SRJigsawSRG3a"
anaSRJigsawSRG3a.HT5PP = 2000
anaSRJigsawSRG3a.H2PP = 850

finalChannelsDict[anaSRJigsawSRG3a.name]=anaSRJigsawSRG3a


anaSRJigsawSRG3b = copy.deepcopy( anaSRJigsawSRG3Common )
anaSRJigsawSRG3b.name = "SRJigsawSRG3b"
anaSRJigsawSRG3b.HT5PP = 2250
anaSRJigsawSRG3b.H2PP = 850

finalChannelsDict[anaSRJigsawSRG3b.name]=anaSRJigsawSRG3b

anaSRJigsawSRG3c = copy.deepcopy( anaSRJigsawSRG3Common )
anaSRJigsawSRG3c.name = "SRJigsawSRG3c"
anaSRJigsawSRG3c.HT5PP = 2500
anaSRJigsawSRG3c.H2PP = 850

finalChannelsDict[anaSRJigsawSRG3c.name]=anaSRJigsawSRG3c





#----------------------------------------------------------
# RJigsaw SRs - Squarks
#----------------------------------------------------------

###################################################################


anaSRJigsawSRS1Common = copy.deepcopy( anaSRJigsawBasic )
anaSRJigsawSRS1Common.name = "SRJigsawSRS1Common"
anaSRJigsawSRS1Common.RPTHT3PP_upper = 0.08
anaSRJigsawSRS1Common.R_H2PP_H3PP = 0.6
anaSRJigsawSRS1Common.R_H2PP_H3PP_upper = 0.95
anaSRJigsawSRS1Common.RPZ_HT3PP_upper = 0.55
anaSRJigsawSRS1Common.R_ptj2_HT3PP = 0.16
anaSRJigsawSRS1Common.cosP_upper = 0.65
anaSRJigsawSRS1Common.nJets = 2
anaSRJigsawSRS1Common.HT3PP_loose = 1100
anaSRJigsawSRS1Common.H2PP_loose = 900

anaSRJigsawSRS1a = copy.deepcopy( anaSRJigsawSRS1Common )
anaSRJigsawSRS1a.name = "SRJigsawSRS1a"
anaSRJigsawSRS1a.HT3PP = 1100
anaSRJigsawSRS1a.H2PP = 900
finalChannelsDict[anaSRJigsawSRS1a.name]=anaSRJigsawSRS1a


anaSRJigsawSRS1b = copy.deepcopy( anaSRJigsawSRS1Common )
anaSRJigsawSRS1b.name = "SRJigsawSRS1b"
anaSRJigsawSRS1b.HT3PP = 1200
anaSRJigsawSRS1b.H2PP = 1000
finalChannelsDict[anaSRJigsawSRS1b.name]=anaSRJigsawSRS1b

####################################################################


anaSRJigsawSRS2Common = copy.deepcopy( anaSRJigsawBasic )
anaSRJigsawSRS2Common.name = "SRJigsawSRS2Common"
anaSRJigsawSRS2Common.RPTHT3PP_upper = 0.08
anaSRJigsawSRS2Common.R_H2PP_H3PP = 0.55
anaSRJigsawSRS2Common.R_H2PP_H3PP_upper = 0.96
anaSRJigsawSRS2Common.RPZ_HT3PP_upper = 0.6
anaSRJigsawSRS2Common.R_ptj2_HT3PP = 0.15
anaSRJigsawSRS2Common.cosP_upper = 0.7
anaSRJigsawSRS2Common.nJets = 2
anaSRJigsawSRS2Common.HT3PP_loose = 1100
anaSRJigsawSRS2Common.H2PP_loose = 900

anaSRJigsawSRS2a = copy.deepcopy( anaSRJigsawSRS2Common )
anaSRJigsawSRS2a.name = "SRJigsawSRS2a"
anaSRJigsawSRS2a.HT3PP = 1300
anaSRJigsawSRS2a.H2PP = 1100
finalChannelsDict[anaSRJigsawSRS2a.name]=anaSRJigsawSRS2a


anaSRJigsawSRS2b = copy.deepcopy( anaSRJigsawSRS2Common )
anaSRJigsawSRS2b.name = "SRJigsawSRS2b"
anaSRJigsawSRS2b.HT3PP = 1450
anaSRJigsawSRS2b.H2PP = 1200
finalChannelsDict[anaSRJigsawSRS2b.name]=anaSRJigsawSRS2b


####################################################################


anaSRJigsawSRS3Common = copy.deepcopy( anaSRJigsawBasic )
anaSRJigsawSRS3Common.name = "SRJigsawSRS3Common"
anaSRJigsawSRS3Common.RPTHT3PP_upper = 0.08
anaSRJigsawSRS3Common.R_H2PP_H3PP = 0.5
anaSRJigsawSRS3Common.R_H2PP_H3PP_upper = 0.98
anaSRJigsawSRS3Common.RPZ_HT3PP_upper = 0.63
anaSRJigsawSRS3Common.R_ptj2_HT3PP = 0.13
anaSRJigsawSRS3Common.cosP_upper = 0.8
anaSRJigsawSRS3Common.nJets = 2
anaSRJigsawSRS3Common.HT3PP_loose = 1100
anaSRJigsawSRS3Common.H2PP_loose = 900

anaSRJigsawSRS3a = copy.deepcopy( anaSRJigsawSRS3Common )
anaSRJigsawSRS3a.name = "SRJigsawSRS3a"
anaSRJigsawSRS3a.HT3PP = 1600
anaSRJigsawSRS3a.H2PP = 1350
finalChannelsDict[anaSRJigsawSRS3a.name]=anaSRJigsawSRS3a


anaSRJigsawSRS3b = copy.deepcopy( anaSRJigsawSRS3Common )
anaSRJigsawSRS3b.name = "SRJigsawSRS3b"
anaSRJigsawSRS3b.HT3PP = 1800
anaSRJigsawSRS3b.H2PP = 1500
finalChannelsDict[anaSRJigsawSRS3b.name]=anaSRJigsawSRS3b






#----------------------------------------------------------
# RJigsaw SRs - Compressed Stuff
#----------------------------------------------------------

###################################################################


anaSRJigsawSRC1Common = copy.deepcopy( anaSRJigsawCoBasic )
anaSRJigsawSRC1Common.name = "SRJigsawSRC1Common"
anaSRJigsawSRC1Common.RPTHT1CM_upper = 0.15
anaSRJigsawSRC1Common.PIoHT1CM = 0.9
anaSRJigsawSRC1Common.cosS = 0.8
anaSRJigsawSRC1Common.nJets = 2
anaSRJigsawSRC1Common.MS = 0
anaSRJigsawSRC1Common.HT1CM_loose = 300
anaSRJigsawSRC1Common.MS_loose = 0
anaSRJigsawSRC1Common.R_H2PP_H3PP = 0
anaSRJigsawSRC1Common.dPhi = 0.4


anaSRJigsawSRC1a = copy.deepcopy( anaSRJigsawSRC1Common )
anaSRJigsawSRC1a.name = "SRJigsawSRC1a"
anaSRJigsawSRC1a.HT1CM = 700
finalChannelsDict[anaSRJigsawSRC1a.name]=anaSRJigsawSRC1a

anaSRJigsawSRC1b = copy.deepcopy( anaSRJigsawSRC1Common )
anaSRJigsawSRC1b.name = "SRJigsawSRC1b"
anaSRJigsawSRC1b.HT1CM = 900
finalChannelsDict[anaSRJigsawSRC1b.name]=anaSRJigsawSRC1b

###################################################################


anaSRJigsawSRC2Common = copy.deepcopy( anaSRJigsawCoBasic )
anaSRJigsawSRC2Common.name = "SRJigsawSRC2Common"
anaSRJigsawSRC2Common.RPTHT1CM_upper = 0.15
anaSRJigsawSRC2Common.PIoHT1CM = 0.8
anaSRJigsawSRC2Common.MS = 100
anaSRJigsawSRC2Common.cosS = 0.8
anaSRJigsawSRC2Common.nJets = 2
anaSRJigsawSRC2Common.HT1CM_loose = 300
anaSRJigsawSRC2Common.MS_loose = 0
anaSRJigsawSRC2Common.R_H2PP_H3PP = 0
anaSRJigsawSRC2Common.dPhi = 0.4


anaSRJigsawSRC2a = copy.deepcopy( anaSRJigsawSRC2Common )
anaSRJigsawSRC2a.name = "SRJigsawSRC2a"
anaSRJigsawSRC2a.HT1CM = 700
finalChannelsDict[anaSRJigsawSRC2a.name]=anaSRJigsawSRC2a

anaSRJigsawSRC2b = copy.deepcopy( anaSRJigsawSRC2Common )
anaSRJigsawSRC2b.name = "SRJigsawSRC2b"
anaSRJigsawSRC2b.HT1CM = 900
finalChannelsDict[anaSRJigsawSRC2b.name]=anaSRJigsawSRC2b

###################################################################


anaSRJigsawSRC3Common = copy.deepcopy( anaSRJigsawCoBasic )
anaSRJigsawSRC3Common.name = "SRJigsawSRC3Common"
anaSRJigsawSRC3Common.RPTHT1CM_upper = 0.15
anaSRJigsawSRC3Common.PIoHT1CM = 0.7
anaSRJigsawSRC3Common.MS = 200
anaSRJigsawSRC3Common.cosS = 0.8
anaSRJigsawSRC3Common.nJets = 2
anaSRJigsawSRC3Common.HT1CM_loose = 300
anaSRJigsawSRC3Common.MS_loose = 0
anaSRJigsawSRC3Common.R_H2PP_H3PP = 0
anaSRJigsawSRC3Common.dPhi = 0.4


anaSRJigsawSRC3a = copy.deepcopy( anaSRJigsawSRC3Common )
anaSRJigsawSRC3a.name = "SRJigsawSRC3a"
anaSRJigsawSRC3a.HT1CM = 700
finalChannelsDict[anaSRJigsawSRC3a.name]=anaSRJigsawSRC3a

anaSRJigsawSRC3b = copy.deepcopy( anaSRJigsawSRC3Common )
anaSRJigsawSRC3b.name = "SRJigsawSRC3b"
anaSRJigsawSRC3b.HT1CM = 900
finalChannelsDict[anaSRJigsawSRC3b.name]=anaSRJigsawSRC3b


###################################################################


anaSRJigsawSRC4Common = copy.deepcopy( anaSRJigsawCoBasic )
anaSRJigsawSRC4Common.name = "SRJigsawSRC4Common"
anaSRJigsawSRC4Common.RPTHT1CM_upper = 0.15
anaSRJigsawSRC4Common.PIoHT1CM = 0.6
anaSRJigsawSRC4Common.MS = 400
anaSRJigsawSRC4Common.cosS = 0.8
anaSRJigsawSRC4Common.nJets = 2
anaSRJigsawSRC4Common.MS_loose = 0
anaSRJigsawSRC4Common.HT1CM_loose = 300
anaSRJigsawSRC4Common.PIoHT1CM_CR = 0.7
anaSRJigsawSRC4Common.R_H2PP_H3PP = 0
anaSRJigsawSRC4Common.dPhi = 0.4

anaSRJigsawSRC4a = copy.deepcopy( anaSRJigsawSRC4Common )
anaSRJigsawSRC4a.name = "SRJigsawSRC4a"
anaSRJigsawSRC4a.HT1CM = 700
finalChannelsDict[anaSRJigsawSRC4a.name]=anaSRJigsawSRC4a

anaSRJigsawSRC4b = copy.deepcopy( anaSRJigsawSRC4Common )
anaSRJigsawSRC4b.name = "SRJigsawSRC4b"
anaSRJigsawSRC4b.HT1CM = 900
finalChannelsDict[anaSRJigsawSRC4b.name]=anaSRJigsawSRC4b






###########################################################
# all channels
###########################################################

finalChannelsDict = finalChannelsDict.copy()
# finalChannelsDict.update(channelsForPlottingDict)





