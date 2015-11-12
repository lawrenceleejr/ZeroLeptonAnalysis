from  ChannelConfig import * 

###########################################################
# definition of the control regions
###########################################################

regionDict={}
regionDict["SR"]=Region("SR","SRAll")
#regionDict["CRW"]=Region("CRW","CRWT",["nBJet==0"],["bTagWeight"])#,"leptonWeight"])
#regionDict["CRT"]=Region("CRT","CRWT",["nBJet>0"],["bTagWeight"])#,"leptonWeight"])
regionDict["CRW"]=Region("CRW","CRWT",[],[])
regionDict["CRT"]=Region("CRT","CRWT",[],[])

regionDict["VRWf"]=Region("VRWf","CRWT",["nBJet==0"],["bTagWeight"])#,"leptonWeight"])
regionDict["VRTf"]=Region("VRTf","CRWT",["nBJet>0"],["bTagWeight"])#,"leptonWeight"])


regionDict["VRWMf"]=Region("VRWMf","VRWT",["nBJet==0"],["bTagWeight"])#,"leptonWeight"])
regionDict["VRTMf"]=Region("VRTMf","VRWT",["nBJet>0"],["bTagWeight"])#,"leptonWeight"])
regionDict["VRWM"]=Region("VRWM","VRWT",["nBJet==0"],["bTagWeight"])#,"leptonWeight"])
regionDict["VRTM"]=Region("VRTM","VRWT",["nBJet>0"],["bTagWeight"])#,"leptonWeight"])


regionDict["VRWTplus"]=Region("VRWTplus","CRWT",["lep1sign>0"],[])
regionDict["VRWTminus"]=Region("VRWTminus","CRWT",["lep1sign<0"],[])
regionDict["VRWTfplus"]=Region("VRWTfplus","CRWT",["lep1sign>0"],[])
regionDict["VRWTfminus"]=Region("VRWTfminus","CRWT",["lep1sign<0"],[])



regionDict["CRY"]=Region("CRY","CRY")#LL#,["(phQuality == 2 && phIso < 5000. && nLep == 0)"],["photonWeight","triggerWeight"])#extra weights should be applied only to gamma+jets
regionDict["CRQ"]=Region("CRQ","SRAll")#ATT: qcd weight
regionDict["VRQ1"]=Region("VRQ1","SRAll")#ATT: qcd weight
regionDict["VRQ2"]=Region("VRQ2","SRAll")#ATT: qcd weight
regionDict["VRQ3"]=Region("VRQ3","SRAll")#ATT: qcd weight
regionDict["VRQ4"]=Region("VRQ4","SRAll")#ATT: qcd weight
#regionDict["VRZ"]=Region("VRZ","CRZ",[],["leptonWeight"])
regionDict["VRZ"]=Region("VRZ","CRZ",[],[])

regionDict["VRZf"]=Region("VRZf","CRZ",[],["leptonWeight"])
regionDict["VRT2L"]=Region("VRT2L","CRZ_VR1b",["(mll>116000 &&  lep1Pt<200000 && lep2Pt<100000)"],["leptonWeight"])#ATT: qcd weight


###########################################################
# definition of the channels
###########################################################

allChannelsDict={}

# #----------------------------------------------------------
# # SR2jl
# #----------------------------------------------------------

# anaSR2jl=ChannelConfig("SR2jl",regionDict)
# anaSR2jl.nJet=2
# anaSR2jl.dPhi=0.4
# anaSR2jl.metsig=8    
# anaSR2jl.meff=800*1000
# #only needed for SR2jl where the same cuts are applied in SR,CR and CRs
# anaSR2jl.regionsWithoutDPHICut=[]
# anaSR2jl.regionsWithoutMETOVERMEFFCut=[]
# anaSR2jl.regionsWithoutMETSIGCut=[]
# allChannelsDict[anaSR2jl.name]=anaSR2jl



# #----------------------------------------------------------
# # SR2jm
# #----------------------------------------------------------

# anaSR2jm=ChannelConfig("SR2jm",regionDict)
# anaSR2jm.nJet=2
# anaSR2jm.dPhi=0.4
# anaSR2jm.metsig=15    
# anaSR2jm.meff=1200*1000
# allChannelsDict[anaSR2jm.name]=anaSR2jm



# #----------------------------------------------------------
# # SR2jt
# #----------------------------------------------------------

# anaSR2jt=ChannelConfig("SR2jt",regionDict)
# anaSR2jt.nJet=2
# anaSR2jt.dPhi=0.4
# anaSR2jt.metsig=15    
# anaSR2jt.meff=1600*1000
# allChannelsDict[anaSR2jt.name]=anaSR2jt




# #----------------------------------------------------------
# # SR3j
# #----------------------------------------------------------

# anaSR3j=ChannelConfig("SR3j",regionDict)
# anaSR3j.nJet=3
# anaSR3j.dPhi=0.4
# anaSR3j.met_over_meffNj=0.3    
# anaSR3j.meff=2200*1000
# allChannelsDict[anaSR3j.name]=anaSR3j



# #----------------------------------------------------------
# # SR4jlminus
# #----------------------------------------------------------

# anaSR4jlminus=ChannelConfig("SR4jlminus",regionDict)
# anaSR4jlminus.nJet=4
# anaSR4jlminus.dPhi=0.4
# anaSR4jlminus.dPhiR=0.2
# anaSR4jlminus.metsig=10        
# anaSR4jlminus.meff=700*1000
# allChannelsDict[anaSR4jlminus.name]=anaSR4jlminus


# #----------------------------------------------------------
# # SR4jl
# #----------------------------------------------------------

# anaSR4jl=ChannelConfig("SR4jl",regionDict)
# anaSR4jl.nJet=4
# anaSR4jl.dPhi=0.4
# anaSR4jl.dPhiR=0.2
# anaSR4jl.metsig=10        
# anaSR4jl.meff=1000*1000
# allChannelsDict[anaSR4jl.name]=anaSR4jl

# #----------------------------------------------------------
# # SR4jm
# #----------------------------------------------------------

# anaSR4jm=ChannelConfig("SR4jm",regionDict)
# anaSR4jm.nJet=4
# anaSR4jm.dPhi=0.4
# anaSR4jm.dPhiR=0.2
# anaSR4jm.met_over_meffNj=0.4        
# anaSR4jm.meff=1300*1000
# allChannelsDict[anaSR4jm.name]=anaSR4jm

#----------------------------------------------------------
# SR4jt
#----------------------------------------------------------

anaSR4jt=ChannelConfig("SR4jt",regionDict)
anaSR4jt.nJet=4
anaSR4jt.dPhi=0.4
anaSR4jt.dPhiR=0.2
anaSR4jt.met_over_meffNj=0.25
anaSR4jt.meff=2200*1000
allChannelsDict[anaSR4jt.name]=anaSR4jt 


#----------------------------------------------------------
# SR5j
#----------------------------------------------------------

anaSR5j=ChannelConfig("SR5j",regionDict)
anaSR5j.nJet=5
anaSR5j.dPhi=0.4
anaSR5j.dPhiR=0.2
anaSR5j.met_over_meffNj=0.2
anaSR5j.meff=1200*1000
allChannelsDict[anaSR5j.name]=anaSR5j 


# #----------------------------------------------------------
# # SR6jl
# #----------------------------------------------------------
# anaSR6jl=ChannelConfig("SR6jl",regionDict)
# anaSR6jl.nJet=6
# anaSR6jl.dPhi=0.4
# anaSR6jl.dPhiR=0.2
# anaSR6jl.met_over_meffNj=0.2
# anaSR6jl.meff=900*1000
# allChannelsDict[anaSR6jl.name]=anaSR6jl 

# #----------------------------------------------------------
# # SR6jm
# #----------------------------------------------------------

# anaSR6jm=ChannelConfig("SR6jm",regionDict)
# anaSR6jm.nJet=6
# anaSR6jm.dPhi=0.4
# anaSR6jm.dPhiR=0.2
# anaSR6jm.met_over_meffNj=0.2
# anaSR6jm.meff=1200*1000
# allChannelsDict[anaSR6jm.name]=anaSR6jm 

# #----------------------------------------------------------
# # SR6jt
# #----------------------------------------------------------

# anaSR6jt=ChannelConfig("SR6jt",regionDict)
# anaSR6jt.nJet=6
# anaSR6jt.dPhi=0.4
# anaSR6jt.dPhiR=0.2
# anaSR6jt.met_over_meffNj=0.25
# anaSR6jt.meff=1500*1000
# allChannelsDict[anaSR6jt.name]=anaSR6jt 

# #----------------------------------------------------------
# # SR6jtplus
# #----------------------------------------------------------

# anaSR6jtplus=ChannelConfig("SR6jtplus",regionDict)
# anaSR6jtplus.nJet=6
# anaSR6jtplus.dPhi=0.4
# anaSR6jtplus.dPhiR=0.2
# anaSR6jtplus.met_over_meffNj=0.15
# anaSR6jtplus.meff=1700*1000
# allChannelsDict[anaSR6jtplus.name]=anaSR6jtplus 

#----------------------------------------------------------
# RJigsaw
#----------------------------------------------------------
anaSRJigsawBasic=ChannelConfig("SRJigsawBasic",regionDict)

# trigger
anaSRJigsawBasic.met=100
anaSRJigsawBasic.MDR=300
anaSRJigsawBasic.deltaQCD=0

#----------------------------------------------------------
# RJigsaw SRs
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

anaSRJigsawSR1A = copy.deepcopy( anaSRJigsawSR1Common )
anaSRJigsawSR1A.name = "SRJigsawSR1A"
anaSRJigsawSR1A.HT5PP = 800
anaSRJigsawSR1A.H2PP = 550

allChannelsDict[anaSRJigsawSR1A.name]=anaSRJigsawSR1A


anaSRJigsawSR1B = copy.deepcopy( anaSRJigsawSR1Common )
anaSRJigsawSR1B.name = "SRJigsawSR1B"
anaSRJigsawSR1B.HT5PP = 1000
anaSRJigsawSR1B.H2PP = 550

allChannelsDict[anaSRJigsawSR1B.name]=anaSRJigsawSR1B

anaSRJigsawSR1C = copy.deepcopy( anaSRJigsawSR1Common )
anaSRJigsawSR1C.name = "SRJigsawSR1C"
anaSRJigsawSR1C.HT5PP = 1200
anaSRJigsawSR1C.H2PP = 550

allChannelsDict[anaSRJigsawSR1C.name]=anaSRJigsawSR1C

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

anaSRJigsawSR2A = copy.deepcopy( anaSRJigsawSR2Common )
anaSRJigsawSR2A.name = "SRJigsawSR2A"
anaSRJigsawSR2A.HT5PP = 1400
anaSRJigsawSR2A.H2PP = 750

allChannelsDict[anaSRJigsawSR2A.name]=anaSRJigsawSR2A


anaSRJigsawSR2B = copy.deepcopy( anaSRJigsawSR2Common )
anaSRJigsawSR2B.name = "SRJigsawSR2B"
anaSRJigsawSR2B.HT5PP = 1600
anaSRJigsawSR2B.H2PP = 750

allChannelsDict[anaSRJigsawSR2B.name]=anaSRJigsawSR2B

anaSRJigsawSR2C = copy.deepcopy( anaSRJigsawSR2Common )
anaSRJigsawSR2C.name = "SRJigsawSR2C"
anaSRJigsawSR2C.HT5PP = 1800
anaSRJigsawSR2C.H2PP = 750

allChannelsDict[anaSRJigsawSR2C.name]=anaSRJigsawSR2C

###################################################################

###################################################################


anaSRJigsawSR3Common = copy.deepcopy( anaSRJigsawBasic )
anaSRJigsawSR3Common.name = "SRJigsawSR3Common"
anaSRJigsawSR3Common.RPTHT5PP_upper = 0.08
anaSRJigsawSR3Common.R_H2PP_H5PP = 0.2
anaSRJigsawSR3Common.R_HT5PP_H5PP = 0.65
anaSRJigsawSR3Common.RPZ_HT5PP_upper = 0.5
anaSRJigsawSR3Common.minR_pTj2i_HT3PPi = 0.09
anaSRJigsawSR3Common.maxR_H1PPi_H2PPi_upper = 0.98

anaSRJigsawSR3A = copy.deepcopy( anaSRJigsawSR3Common )
anaSRJigsawSR3A.name = "SRJigsawSR3A"
anaSRJigsawSR3A.HT5PP = 2000
anaSRJigsawSR3A.H2PP = 850

allChannelsDict[anaSRJigsawSR3A.name]=anaSRJigsawSR3A


anaSRJigsawSR3B = copy.deepcopy( anaSRJigsawSR3Common )
anaSRJigsawSR3B.name = "SRJigsawSR3B"
anaSRJigsawSR3B.HT5PP = 2250
anaSRJigsawSR3B.H2PP = 850

allChannelsDict[anaSRJigsawSR3B.name]=anaSRJigsawSR3B

anaSRJigsawSR3C = copy.deepcopy( anaSRJigsawSR3Common )
anaSRJigsawSR3C.name = "SRJigsawSR3C"
anaSRJigsawSR3C.HT5PP = 2500
anaSRJigsawSR3C.H2PP = 850

allChannelsDict[anaSRJigsawSR3C.name]=anaSRJigsawSR3C

###################################################################
