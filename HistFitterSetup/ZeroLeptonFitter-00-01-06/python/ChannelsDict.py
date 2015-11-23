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
# regionDict["CRTZL"] = Region("CRTZL", "SRAll", ["nBJet>0", cleaningCut], ["bTagWeight"])
#regionDict["CRTZL"] = Region("CRTZL", "SRAll", ["nBJet>0",cleaningCut], ["bTagWeight"])
regionDict["CRWT"] = Region("CRWT", "CRWT", ["nBJet>=0"], ["bTagWeight"])


# regionDict["VRWf"] = Region("VRWf", "CRWT", ["nBJet==0"], ["bTagWeight"]) #ATT: systWeights[0] is a proxy for the lepton weight
# regionDict["VRTf"] = Region("VRTf", "CRWT", ["nBJet>0"], ["bTagWeight"])

# regionDict["VRWMf"] = Region("VRWMf", "VRWT", ["nBJet==0"], ["bTagWeight"])
# regionDict["VRTMf"] = Region("VRTMf", "VRWT", ["nBJet>0"], ["bTagWeight"])
# regionDict["VRWM"] = Region("VRWM", "VRWT", ["nBJet==0"], ["bTagWeight"])
# regionDict["VRTM"] = Region("VRTM", "VRWT", ["nBJet>0"], ["bTagWeight"])

regionDict["CRZ"] = Region("CRZ", "CRZ", [], [])

# regionDict["VRWTplus"] = Region("VRWTplus", "CRWT", ["lep1sign>0"], ["bTagWeight"])
# regionDict["VRWTminus"] = Region("VRWTminus", "CRWT", ["lep1sign<0"], ["bTagWeight"])
# regionDict["VRWTfplus"] = Region("VRWTfplus", "CRWT", ["lep1sign>0"], ["bTagWeight"])
# regionDict["VRWTfminus"] = Region("VRWTfminus", "CRWT", ["lep1sign<0"], ["bTagWeight"])

# regionDict["CRY"] = Region("CRY", "CRY", ["(phSignal[0]==1)"], [" 1.6 "])#extra weights should be applied only to gamma+jets
regionDict["CRY"] = Region("CRY", "CRY", ["(phSignal[0]==1 && phPt[0]>130.)"], ["1.6"])#extra weights should be applied only to gamma+jets
# regionDict["VRYf"] = Region("VRY", "CRY", ["(phSignal[0]==1 && phPt[0]>130.)"], ["1.6"])#extra weights should be applied only to gamma+jets

regionDict["CRQ"] = Region("CRQ", "SRAll", [cleaningCut])#ATT: qcd weight
regionDict["VRQ1"] = Region("VRQ1", "SRAll", [cleaningCut])#ATT: qcd weight
regionDict["VRQ2"] = Region("VRQ2", "SRAll", [cleaningCut])#ATT: qcd weight
# regionDict["VRQ3"] = Region("VRQ3", "SRAll", [cleaningCut])#ATT: qcd weight
# regionDict["VRQ4"] = Region("VRQ4", "SRAll", [cleaningCut])#ATT: qcd weight

regionDict["VRZ"] = Region("VRZ", "CRZ", [], [])
# regionDict["VRZf"] = Region("VRZf", "CRZ", [], [])

# regionDict["VRT2L"] = Region("VRT2L", "CRZ_VR1b", ["(mll>116000 &&  lep1Pt<200000 && lep2Pt<100000)"], [])#ATT: qcd weight


# ##for data-driven BG estimation##
# regionDict["VRW"] = Region("VRW", "CRWT", ["nBJet==0"], ["bTagWeight"])
# regionDict["CRWL"] = Region("VRWL", "CRWT", ["nBJet==0"], ["bTagWeight"])
# regionDict["CRWVL"] = Region("VRWVL", "CRWT", ["nBJet==0"], ["bTagWeight"])
# regionDict["VRT"] = Region("VRT", "CRWT", ["nBJet>0"], ["bTagWeight"])
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


anaSRJigsawSR1Common = copy.deepcopy( anaSRJigsawBasic )
anaSRJigsawSR1Common.name = "SRJigsawSR1Common"
anaSRJigsawSR1Common.RPTHT5PP_upper = 0.08
anaSRJigsawSR1Common.R_H2PP_H5PP = 0.35
anaSRJigsawSR1Common.R_HT5PP_H5PP = 0.8
anaSRJigsawSR1Common.RPZ_HT5PP_upper = 0.5
anaSRJigsawSR1Common.minR_pTj2i_HT3PPi = 0.125
anaSRJigsawSR1Common.maxR_H1PPi_H2PPi_upper = 0.95
anaSRJigsawSR1Common.dangle_upper = 0.5
anaSRJigsawSR1Common.nJets = 4

anaSRJigsawSR1A = copy.deepcopy( anaSRJigsawSR1Common )
anaSRJigsawSR1A.name = "SRJigsawSR1A"
anaSRJigsawSR1A.HT5PP = 800
anaSRJigsawSR1A.H2PP = 550

finalChannelsDict[anaSRJigsawSR1A.name]=anaSRJigsawSR1A


anaSRJigsawSR1B = copy.deepcopy( anaSRJigsawSR1Common )
anaSRJigsawSR1B.name = "SRJigsawSR1B"
anaSRJigsawSR1B.HT5PP = 1000
anaSRJigsawSR1B.H2PP = 550

finalChannelsDict[anaSRJigsawSR1B.name]=anaSRJigsawSR1B

anaSRJigsawSR1C = copy.deepcopy( anaSRJigsawSR1Common )
anaSRJigsawSR1C.name = "SRJigsawSR1C"
anaSRJigsawSR1C.HT5PP = 1200
anaSRJigsawSR1C.H2PP = 550

finalChannelsDict[anaSRJigsawSR1C.name]=anaSRJigsawSR1C

###################################################################

###################################################################


anaSRJigsawSR2Common = copy.deepcopy( anaSRJigsawBasic )
anaSRJigsawSR2Common.name = "SRJigsawSR2Common"
anaSRJigsawSR2Common.RPTHT5PP_upper = 0.08
anaSRJigsawSR2Common.R_H2PP_H5PP = 0.25
anaSRJigsawSR2Common.R_HT5PP_H5PP = 0.75
anaSRJigsawSR2Common.RPZ_HT5PP_upper = 0.55
anaSRJigsawSR2Common.minR_pTj2i_HT3PPi = 0.11
anaSRJigsawSR2Common.maxR_H1PPi_H2PPi_upper = 0.97
anaSRJigsawSR2Common.nJets = 4

anaSRJigsawSR2A = copy.deepcopy( anaSRJigsawSR2Common )
anaSRJigsawSR2A.name = "SRJigsawSR2A"
anaSRJigsawSR2A.HT5PP = 1400
anaSRJigsawSR2A.H2PP = 750

finalChannelsDict[anaSRJigsawSR2A.name]=anaSRJigsawSR2A


anaSRJigsawSR2B = copy.deepcopy( anaSRJigsawSR2Common )
anaSRJigsawSR2B.name = "SRJigsawSR2B"
anaSRJigsawSR2B.HT5PP = 1600
anaSRJigsawSR2B.H2PP = 750

finalChannelsDict[anaSRJigsawSR2B.name]=anaSRJigsawSR2B

anaSRJigsawSR2C = copy.deepcopy( anaSRJigsawSR2Common )
anaSRJigsawSR2C.name = "SRJigsawSR2C"
anaSRJigsawSR2C.HT5PP = 1800
anaSRJigsawSR2C.H2PP = 750

finalChannelsDict[anaSRJigsawSR2C.name]=anaSRJigsawSR2C

###################################################################

###################################################################


anaSRJigsawSR3Common = copy.deepcopy( anaSRJigsawBasic )
anaSRJigsawSR3Common.name = "SRJigsawSR3Common"
anaSRJigsawSR3Common.RPTHT5PP_upper = 0.08
anaSRJigsawSR3Common.R_H2PP_H5PP = 0.2
anaSRJigsawSR3Common.R_HT5PP_H5PP = 0.65
anaSRJigsawSR3Common.RPZ_HT5PP_upper = 0.6
anaSRJigsawSR3Common.minR_pTj2i_HT3PPi = 0.09
anaSRJigsawSR3Common.maxR_H1PPi_H2PPi_upper = 0.98
anaSRJigsawSR3Common.nJets = 4

anaSRJigsawSR3A = copy.deepcopy( anaSRJigsawSR3Common )
anaSRJigsawSR3A.name = "SRJigsawSR3A"
anaSRJigsawSR3A.HT5PP = 2000
anaSRJigsawSR3A.H2PP = 850

finalChannelsDict[anaSRJigsawSR3A.name]=anaSRJigsawSR3A


anaSRJigsawSR3B = copy.deepcopy( anaSRJigsawSR3Common )
anaSRJigsawSR3B.name = "SRJigsawSR3B"
anaSRJigsawSR3B.HT5PP = 2250
anaSRJigsawSR3B.H2PP = 850

finalChannelsDict[anaSRJigsawSR3B.name]=anaSRJigsawSR3B

anaSRJigsawSR3C = copy.deepcopy( anaSRJigsawSR3Common )
anaSRJigsawSR3C.name = "SRJigsawSR3C"
anaSRJigsawSR3C.HT5PP = 2500
anaSRJigsawSR3C.H2PP = 850

finalChannelsDict[anaSRJigsawSR3C.name]=anaSRJigsawSR3C





#----------------------------------------------------------
# RJigsaw SRs - Squarks
#----------------------------------------------------------

###################################################################


anaSRJigsawSR1SqCommon = copy.deepcopy( anaSRJigsawBasic )
anaSRJigsawSR1SqCommon.name = "SRJigsawSR1SqCommon"
anaSRJigsawSR1SqCommon.RPTHT3PP_upper = 0.08
anaSRJigsawSR1SqCommon.R_H2PP_H3PP = 0.6
anaSRJigsawSR1SqCommon.R_H2PP_H3PP_upper = 0.95
anaSRJigsawSR1SqCommon.RPZ_HT3PP_upper = 0.55
anaSRJigsawSR1SqCommon.R_ptj2_HT3PP = 0.16
anaSRJigsawSR1SqCommon.cosP_upper = 0.65
anaSRJigsawSR1SqCommon.nJets = 2


anaSRJigsawSR1ASq = copy.deepcopy( anaSRJigsawSR1SqCommon )
anaSRJigsawSR1ASq.name = "SRJigsawSR1ASq"
anaSRJigsawSR1ASq.HT3PP = 1100
anaSRJigsawSR1ASq.H2PP = 900
finalChannelsDict[anaSRJigsawSR1ASq.name]=anaSRJigsawSR1ASq


anaSRJigsawSR1BSq = copy.deepcopy( anaSRJigsawSR1SqCommon )
anaSRJigsawSR1BSq.name = "SRJigsawSR1BSq"
anaSRJigsawSR1BSq.HT3PP = 1200
anaSRJigsawSR1BSq.H2PP = 1000
finalChannelsDict[anaSRJigsawSR1BSq.name]=anaSRJigsawSR1BSq

####################################################################


anaSRJigsawSR2SqCommon = copy.deepcopy( anaSRJigsawBasic )
anaSRJigsawSR2SqCommon.name = "SRJigsawSR2SqCommon"
anaSRJigsawSR2SqCommon.RPTHT3PP_upper = 0.08
anaSRJigsawSR2SqCommon.R_H2PP_H3PP = 0.55
anaSRJigsawSR2SqCommon.R_H2PP_H3PP_upper = 0.96
anaSRJigsawSR2SqCommon.RPZ_HT3PP_upper = 0.6
anaSRJigsawSR2SqCommon.R_ptj2_HT3PP = 0.15
anaSRJigsawSR2SqCommon.cosP_upper = 0.7
anaSRJigsawSR2SqCommon.nJets = 2


anaSRJigsawSR2ASq = copy.deepcopy( anaSRJigsawSR2SqCommon )
anaSRJigsawSR2ASq.name = "SRJigsawSR2ASq"
anaSRJigsawSR2ASq.HT3PP = 1300
anaSRJigsawSR2ASq.H2PP = 1100
finalChannelsDict[anaSRJigsawSR2ASq.name]=anaSRJigsawSR2ASq


anaSRJigsawSR2BSq = copy.deepcopy( anaSRJigsawSR2SqCommon )
anaSRJigsawSR2BSq.name = "SRJigsawSR2BSq"
anaSRJigsawSR2BSq.HT3PP = 1450
anaSRJigsawSR2BSq.H2PP = 1200
finalChannelsDict[anaSRJigsawSR2BSq.name]=anaSRJigsawSR2BSq


####################################################################


anaSRJigsawSR3SqCommon = copy.deepcopy( anaSRJigsawBasic )
anaSRJigsawSR3SqCommon.name = "SRJigsawSR3SqCommon"
anaSRJigsawSR3SqCommon.RPTHT3PP_upper = 0.08
anaSRJigsawSR3SqCommon.R_H2PP_H3PP = 0.5
anaSRJigsawSR3SqCommon.R_H2PP_H3PP_upper = 0.98
anaSRJigsawSR3SqCommon.RPZ_HT3PP_upper = 0.63
anaSRJigsawSR3SqCommon.R_ptj2_HT3PP = 0.13
anaSRJigsawSR3SqCommon.cosP_upper = 0.8
anaSRJigsawSR3SqCommon.nJets = 2


anaSRJigsawSR3ASq = copy.deepcopy( anaSRJigsawSR3SqCommon )
anaSRJigsawSR3ASq.name = "SRJigsawSR3ASq"
anaSRJigsawSR3ASq.HT3PP = 1600
anaSRJigsawSR3ASq.H2PP = 1350
finalChannelsDict[anaSRJigsawSR3ASq.name]=anaSRJigsawSR3ASq


anaSRJigsawSR3BSq = copy.deepcopy( anaSRJigsawSR3SqCommon )
anaSRJigsawSR3BSq.name = "SRJigsawSR3BSq"
anaSRJigsawSR3BSq.HT3PP = 1800
anaSRJigsawSR3BSq.H2PP = 1500
finalChannelsDict[anaSRJigsawSR3BSq.name]=anaSRJigsawSR3BSq






#----------------------------------------------------------
# RJigsaw SRs - Compressed Stuff
#----------------------------------------------------------

###################################################################


anaSRJigsawSR1CoCommon = copy.deepcopy( anaSRJigsawCoBasic )
anaSRJigsawSR1CoCommon.name = "SRJigsawSR1CoCommon"
anaSRJigsawSR1CoCommon.RPTHT1CM_upper = 0.15
anaSRJigsawSR1CoCommon.PIoHT1CM = 0.9
anaSRJigsawSR1CoCommon.cosS = 0.8
anaSRJigsawSR1CoCommon.nJets = 2


anaSRJigsawSR1ACo = copy.deepcopy( anaSRJigsawSR1CoCommon )
anaSRJigsawSR1ACo.name = "SRJigsawSR1ACo"
anaSRJigsawSR1ACo.HT1CM = 700
finalChannelsDict[anaSRJigsawSR1ACo.name]=anaSRJigsawSR1ACo

anaSRJigsawSR1BCo = copy.deepcopy( anaSRJigsawSR1CoCommon )
anaSRJigsawSR1BCo.name = "SRJigsawSR1BCo"
anaSRJigsawSR1BCo.HT1CM = 900
finalChannelsDict[anaSRJigsawSR1BCo.name]=anaSRJigsawSR1BCo

###################################################################


anaSRJigsawSR2CoCommon = copy.deepcopy( anaSRJigsawCoBasic )
anaSRJigsawSR2CoCommon.name = "SRJigsawSR2CoCommon"
anaSRJigsawSR2CoCommon.RPTHT1CM_upper = 0.15
anaSRJigsawSR2CoCommon.PIoHT1CM = 0.8
anaSRJigsawSR2CoCommon.MS = 100
anaSRJigsawSR2CoCommon.cosS = 0.8
anaSRJigsawSR2CoCommon.nJets = 2


anaSRJigsawSR2ACo = copy.deepcopy( anaSRJigsawSR2CoCommon )
anaSRJigsawSR2ACo.name = "SRJigsawSR2ACo"
anaSRJigsawSR2ACo.HT1CM = 700
finalChannelsDict[anaSRJigsawSR2ACo.name]=anaSRJigsawSR2ACo

anaSRJigsawSR2BCo = copy.deepcopy( anaSRJigsawSR2CoCommon )
anaSRJigsawSR2BCo.name = "SRJigsawSR2BCo"
anaSRJigsawSR2BCo.HT1CM = 900
finalChannelsDict[anaSRJigsawSR2BCo.name]=anaSRJigsawSR2BCo

###################################################################


anaSRJigsawSR3CoCommon = copy.deepcopy( anaSRJigsawCoBasic )
anaSRJigsawSR3CoCommon.name = "SRJigsawSR3CoCommon"
anaSRJigsawSR3CoCommon.RPTHT1CM_upper = 0.15
anaSRJigsawSR3CoCommon.PIoHT1CM = 0.7
anaSRJigsawSR3CoCommon.MS = 200
anaSRJigsawSR3CoCommon.cosS = 0.8
anaSRJigsawSR3CoCommon.nJets = 2


anaSRJigsawSR3ACo = copy.deepcopy( anaSRJigsawSR3CoCommon )
anaSRJigsawSR3ACo.name = "SRJigsawSR3ACo"
anaSRJigsawSR3ACo.HT1CM = 700
finalChannelsDict[anaSRJigsawSR3ACo.name]=anaSRJigsawSR3ACo

anaSRJigsawSR3BCo = copy.deepcopy( anaSRJigsawSR3CoCommon )
anaSRJigsawSR3BCo.name = "SRJigsawSR3BCo"
anaSRJigsawSR3BCo.HT1CM = 900
finalChannelsDict[anaSRJigsawSR3BCo.name]=anaSRJigsawSR3BCo


###################################################################


anaSRJigsawSR4CoCommon = copy.deepcopy( anaSRJigsawCoBasic )
anaSRJigsawSR4CoCommon.name = "SRJigsawSR4CoCommon"
anaSRJigsawSR4CoCommon.RPTHT1CM_upper = 0.15
anaSRJigsawSR4CoCommon.PIoHT1CM = 0.6
anaSRJigsawSR4CoCommon.MS = 400
anaSRJigsawSR4CoCommon.cosS = 0.8
anaSRJigsawSR4CoCommon.nJets = 2


anaSRJigsawSR4ACo = copy.deepcopy( anaSRJigsawSR4CoCommon )
anaSRJigsawSR4ACo.name = "SRJigsawSR4ACo"
anaSRJigsawSR4ACo.HT1CM = 700
finalChannelsDict[anaSRJigsawSR4ACo.name]=anaSRJigsawSR4ACo

anaSRJigsawSR4BCo = copy.deepcopy( anaSRJigsawSR4CoCommon )
anaSRJigsawSR4BCo.name = "SRJigsawSR4BCo"
anaSRJigsawSR4BCo.HT1CM = 900
finalChannelsDict[anaSRJigsawSR4BCo.name]=anaSRJigsawSR4BCo










###########################################################
# all channels
###########################################################

finalChannelsDict = finalChannelsDict.copy()
# finalChannelsDict.update(channelsForPlottingDict)





