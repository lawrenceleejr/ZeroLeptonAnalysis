from  ChannelConfig import * 

###########################################################
# definition of the control regions
###########################################################



regionDict={}
regionDict["SR"]=Region("SR","SRAll",["1"]) #'(cleaning&3)==0'
regionDict["CRW"]=Region("CRW","CRWT",["nBJet==0 && 30<mt && mt<100 && lep1Pt>25. && (cleaning&15)==0 && abs(timing)<4"],["bTagWeight"])#,"leptonWeight"])
regionDict["CRT"]=Region("CRT","CRWT",["nBJet>0 && 30<mt && mt<100 && lep1Pt>25. && (cleaning&15)==0 && abs(timing)<4"],["bTagWeight"])#,"leptonWeight"])


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




regionDict["CRY"]=Region("CRY","CRY",["(phSignal==1 && dPhi>=0.4 && phPt>130. && jetPt[0]>130.)"],[])#extra weights should be applied only to gamma+jets
regionDict["VRYf"]=Region("VRY","CRY",[],[])#extra weights should be applied only to gamma+jets
#regionDict["CRY"]=Region("CRY","CRY",["(phQuality == 2 && phIso < 5000. && nLep == 0)"],["photonWeight","triggerWeight"])#extra weights should be applied only to gamma+jets
regionDict["CRQ"]=Region("CRQ","SRAll")#ATT: qcd weight
regionDict["VRQ1"]=Region("VRQ1","SRAll")#ATT: qcd weight
regionDict["VRQ2"]=Region("VRQ2","SRAll")#ATT: qcd weight
regionDict["VRQ3"]=Region("VRQ3","SRAll")#ATT: qcd weight
regionDict["VRQ4"]=Region("VRQ4","SRAll")#ATT: qcd weight
regionDict["VRZ"]=Region("VRZ","CRZ",[],[])#ATT: leptonWeight
regionDict["VRZf"]=Region("VRZf","CRZ",[],[])#ATT: leptonWeight
regionDict["VRT2L"]=Region("VRT2L","CRZ_VR1b",["(mll>116000 &&  lep1Pt<200000 && lep2Pt<100000)"],["leptonWeight"])#ATT: qcd weight


###########################################################
# definition of the channels
###########################################################

allChannelsDict={}

#----------------------------------------------------------
# SR2j Moriond
#----------------------------------------------------------
anaSR2jMoriond=ChannelConfig("SR2jMoriond",regionDict)
anaSR2jMoriond.nJet=2
anaSR2jMoriond.dPhi=0.4
anaSR2jMoriond.dPhiR=0.2
anaSR2jMoriond.met_over_meffNj=0.4
anaSR2jMoriond.meff=1800
allChannelsDict[anaSR2jMoriond.name]=anaSR2jMoriond


#----------------------------------------------------------
# SR5j Moriond
#----------------------------------------------------------
anaSR5jMoriond=ChannelConfig("SR5jMoriond",regionDict)
anaSR5jMoriond.nJet=5
anaSR5jMoriond.pt0=200.
anaSR5jMoriond.pt1=200.  
anaSR5jMoriond.dPhi=0.4
anaSR5jMoriond.dPhiR=0.2
anaSR5jMoriond.met_over_meffNj=0.2
anaSR5jMoriond.meff=2400
allChannelsDict[anaSR5jMoriond.name]=anaSR5jMoriond

#----------------------------------------------------------
# newSRs
#----------------------------------------------------------
anaSR2jvt=ChannelConfig("SR2jvt",regionDict)
anaSR2jvt.nJet=2
anaSR2jvt.jetPtThreshold=160.
anaSR2jvt.pt0=anaSR2jvt.jetPtThreshold
anaSR2jvt.pt1=anaSR2jvt.jetPtThreshold
anaSR2jvt.met=200.
anaSR2jvt.dPhi=1.0
anaSR2jvt.metsig=16
anaSR2jvt.meff=1600
allChannelsDict[anaSR2jvt.name]=anaSR2jvt

anaSRNew=ChannelConfig("SR4jAp",regionDict)
anaSRNew.nJet=4
anaSRNew.dPhi=0.4
anaSRNew.dPhiR=0.2
anaSRNew.met_over_meffNj=0.2
anaSRNew.Ap=0.04
anaSRNew.pt0=200.
anaSRNew.pt1=200.
anaSRNew.pt2=150.
anaSRNew.pt3=150.
anaSRNew.meff=2200
allChannelsDict[anaSRNew.name]=anaSRNew

# New SRs
allChannelsDict={}
# 1400_0
anaSRNew=ChannelConfig("SR4j-MetoMeff0.2-Meff2400-sljetpt200-34jetpt150-dphi0.4-ap0.02",regionDict)
anaSRNew.nJet=4
anaSRNew.dPhi=0.4
anaSRNew.dPhiR=0.2
anaSRNew.met_over_meffNj=0.2
anaSRNew.Ap=0.02
anaSRNew.pt0=200.
anaSRNew.pt1=200.
anaSRNew.pt2=150.
anaSRNew.pt3=150.
anaSRNew.meff=2400
allChannelsDict[anaSRNew.name]=anaSRNew

# GG_direct_750_650
anaSRNew=ChannelConfig("SR4j-MetoMeff0.2-Meff2400-sljetpt200-34jetpt60-dphi0.4-ap0.02",regionDict)
anaSRNew.nJet=4
anaSRNew.dPhi=0.4
anaSRNew.dPhiR=0.2
anaSRNew.met_over_meffNj=0.2
anaSRNew.Ap=0.02
anaSRNew.pt0=200.
anaSRNew.pt1=200.
anaSRNew.pt2=60.
anaSRNew.pt3=60.
anaSRNew.meff=2400
allChannelsDict[anaSRNew.name]=anaSRNew

# GG_direct_1100_500
anaSRNew=ChannelConfig("SR4j-MetoMeff0.2-Meff1600-sljetpt200-34jetpt150-dphi0.4-ap0.02",regionDict)
anaSRNew.nJet=4
anaSRNew.dPhi=0.4
anaSRNew.dPhiR=0.2
anaSRNew.met_over_meffNj=0.2
anaSRNew.Ap=0.02
anaSRNew.pt0=200.
anaSRNew.pt1=200.
anaSRNew.pt2=150.
anaSRNew.pt3=150.
anaSRNew.meff=1600
allChannelsDict[anaSRNew.name]=anaSRNew

# GG_direct_1600_0
anaSRNew=ChannelConfig("SR4j-MetoMeff0.2-Meff2600-sljetpt200-34jetpt150-dphi0.4-ap0.02",regionDict)
anaSRNew.nJet=4
anaSRNew.dPhi=0.4
anaSRNew.dPhiR=0.2
anaSRNew.met_over_meffNj=0.2
anaSRNew.Ap=0.02 # same as 0.04
anaSRNew.pt0=200.
anaSRNew.pt1=200.
anaSRNew.pt2=150.
anaSRNew.pt3=150.
anaSRNew.meff=2600
allChannelsDict[anaSRNew.name]=anaSRNew


#----------------------------------------------------------
# RJigsaw
#----------------------------------------------------------
anaSRJigsaw=ChannelConfig("SRJigsaw",regionDict)

anaSRJigsaw.nJet=2
anaSRJigsaw.pt0=60  # leading jet pt cut-->to check
anaSRJigsaw.pt1=60  # subleading jet pt cut-->to check
anaSRJigsaw.jetPtThreshold=30  # general jet pt cut-->to check
anaSRJigsaw.met=100
anaSRJigsaw.RJVars_PP_MDeltaR=300*1000 # always check units (currently MeV for Jigsaw, GeV all others)
anaSRJigsaw.RJVars_P_0_Jet1_pT=200*1000
anaSRJigsaw.RJVars_P_1_Jet1_pT=200*1000
anaSRJigsaw.RJVars_P_0_Jet2_pT=100*1000
anaSRJigsaw.RJVars_P_1_Jet2_pT=100*1000
anaSRJigsaw.RJVars_P_0_PInvHS=0.17 
anaSRJigsaw.RJVars_P_1_PInvHS=0.17 
anaSRJigsaw.RJVars_P_0_CosTheta=-0.5
anaSRJigsaw.RJVars_P_1_CosTheta=-0.5
anaSRJigsaw.RJVars_C_0_CosTheta_upperValue=0.8
anaSRJigsaw.RJVars_C_1_CosTheta_upperValue=0.8
anaSRJigsaw.RJVars_P_0_dPhiGC_lowerValue=-0.9
anaSRJigsaw.RJVars_P_0_dPhiGC_upperValue=0.6
anaSRJigsaw.RJVars_P_1_dPhiGC_lowerValue=-0.9
anaSRJigsaw.RJVars_P_1_dPhiGC_upperValue=0.6
anaSRJigsaw.RJVars_DeltaBetaGG_upperValue=0.9
anaSRJigsaw.RJVars_QCD_Rpt_upperValue=0.3
anaSRJigsaw.RJVars_QCD_Delta1_times_Rpsib=-0.7
anaSRJigsaw.RJVars_PP_VisShape=0.1
anaSRJigsaw.RJVars_MG=600*1000
allChannelsDict[anaSRJigsaw.name]=anaSRJigsaw


# #----------------------------------------------------------
# # very loose selection to compute kappa correction
# #----------------------------------------------------------
# allChannelsDict={}
# anaVL=ChannelConfig("VL",regionDict)
# anaVL.nJet=2
# anaVL.dPhi=0
# anaVL.met=160    
# anaVL.met_upper=300    
# anaVL.regionsWithoutMETSIGCut=[]
# allChannelsDict[anaVL.name]=anaVL


