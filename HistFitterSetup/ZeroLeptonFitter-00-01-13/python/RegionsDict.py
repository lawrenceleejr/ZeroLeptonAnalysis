from ChannelConfig import * 

###########################################################
# definition of the control regions
###########################################################

# cleaningCut="( abs(jetEta[0])>2.4 || jet1Chf/jetFracSamplingMax[0]>0.1)"
cleaningCut="( abs(m_jet1_eta)>2.4 || m_jet1_chf/m_jet1_FracSamplingMax>0.1)"
# qcdCutsForVRWT="(sqrt(pow(met*cos(metPhi)-lep1Pt*cos(lep1Phi),2) + pow(met*sin(metPhi)-lep1Pt*sin(lep1Phi),2))>200)"

regionDict={}
regionDict["SR"] = Region("SR", "SRAll", [cleaningCut], [])

regionDict["CRW"] = Region("CRW", "CRWT", ["nBJet==0"], ["bTagWeight"])
regionDict["CRT"] = Region("CRT", "CRWT", ["nBJet>0"], ["bTagWeight"])
regionDict["CRWT"] = Region("CRWT", "CRWT", ["nBJet>=0"], ["bTagWeight"])


regionDict["VRWf"] = Region("VRWf", "CRWT", ["nBJet==0"], ["bTagWeight"]) #ATT: systWeights[0] is a proxy for the lepton weight
regionDict["VRTf"] = Region("VRTf", "CRWT", ["nBJet>0"], ["bTagWeight"])

# regionDict["VRWMf"] = Region("VRWMf", "VRWT", ["nBJet==0&&"+qcdCutsForVRWT], ["bTagWeight"])
# regionDict["VRTMf"] = Region("VRTMf", "VRWT", ["nBJet>0&&"+qcdCutsForVRWT], ["bTagWeight"])
# regionDict["VRWM"] = Region("VRWM", "VRWT", ["nBJet==0&&"+qcdCutsForVRWT], ["bTagWeight"])
# regionDict["VRTM"] = Region("VRTM", "VRWT", ["nBJet>0&&"+qcdCutsForVRWT], ["bTagWeight"])

regionDict["CRZ"] = Region("CRZ", "CRZ", [], [])

# regionDict["VRWTplus"] = Region("VRWTplus", "CRWT", ["lep1sign>0"], ["bTagWeight"])
# regionDict["VRWTminus"] = Region("VRWTminus", "CRWT", ["lep1sign<0"], ["bTagWeight"])
# regionDict["VRWTfplus"] = Region("VRWTfplus", "CRWT", ["lep1sign>0"], ["bTagWeight"])
# regionDict["VRWTfminus"] = Region("VRWTfminus", "CRWT", ["lep1sign<0"], ["bTagWeight"])

#regionDict["CRY"] = Region("CRY", "CRY", ["(phTopoetcone40<(0.022*phPt[0]+2450) && phPt[0]cone20/phPt[0]<0.05 && phTight==1  && phPt[0][0]>130.)"], [])
regionDict["CRY"] = Region("CRY", "CRY", ["(phSignal[0]==1 && phPt[0]>130. && (phTopoetcone40[0]==0||phTight[0]))"], [])#phTopoetcone40==0) is a dirty hack to know if I run on a truth sample
#regionDict["CRY"] = Region("CRY", "CRY", ["(phSignal[0]==1 && phTight==1  && phPt[0]>130.)"], [])

regionDict["VRYf"] = Region("VRY", "CRY", ["(phSignal[0]==1 && phTight[0]==1  && phPt[0]>130.)"], [])

regionDict["CRQ"] = Region("CRQ", "SRAll", [cleaningCut])#ATT: qcd weight
regionDict["VRQ1"] = Region("VRQ1", "SRAll", [cleaningCut])#ATT: qcd weight
regionDict["VRQ2"] = Region("VRQ2", "SRAll", [cleaningCut])#ATT: qcd weight
regionDict["VRQ3"] = Region("VRQ3", "SRAll", [cleaningCut])#ATT: qcd weight
regionDict["VRQ4"] = Region("VRQ4", "SRAll", [cleaningCut])#ATT: qcd weight

regionDict["VRZ"] = Region("VRZ", "CRZ", [], [])
regionDict["VRZf"] = Region("VRZf", "CRZ", [], [])

# regionDict["VRT2L"] = Region("VRT2L", "CRZ_VR1b", ["(mll>116000 &&  lep1Pt<200000 && lep2Pt<100000)"], [])#ATT: qcd weight


##for data-driven BG estimation##
    #regions for photon
# regionDict["CRYtmtA"] = Region("CRYtmtA", "CRY", ["(phSignal[0][0]==1 && phPt[0][0]>130.)"])
# regionDict["CRYlmtA"] = Region("CRYlmtA", "CRY", ["(phSignal[0][0]==1 && phPt[0][0]>130.)"])
# regionDict["CRYtmlA"] = Region("CRYtmlA", "CRY", ["(phSignal[0][0]==1 && phPt[0][0]>130.)"])
# regionDict["CRYlmlA"] = Region("CRYlmlA", "CRY", ["(phSignal[0][0]==1 && phPt[0][0]>130.)"])
# regionDict["CRYL"] = Region("CRYL", "CRY", ["(phSignal[0][0]==1 && phPt[0][0]>130.)"])
#     #regions for W
# regionDict["CRWL"] = Region("CRWL", "VRWT", ["nBJet==0"], ["bTagWeight"])
# regionDict["CRWVL"] = Region("CRWVL", "VRWT", ["nBJet==0"], ["bTagWeight"])
# regionDict["VRWtmtA"] = Region("VRWtmtA", "VRWT", ["nBJet==0"], ["bTagWeight"])
# regionDict["VRWlmtA"] = Region("VRWlmtA", "VRWT", ["nBJet==0"], ["bTagWeight"])
# regionDict["VRWtmlA"] = Region("VRWtmlA", "VRWT", ["nBJet==0"], ["bTagWeight"])
# regionDict["VRWlmlA"] = Region("VRWlmlA", "VRWT", ["nBJet==0"], ["bTagWeight"])
#     #regions for Top
# regionDict["CRTL"] = Region("CRTL", "VRWT", ["nBJet>0"], ["bTagWeight"])
# regionDict["CRTVL"] = Region("CRTVL", "VRWT", ["nBJet>0"], ["bTagWeight"])
#     #regions for Zll
# regionDict["CRZllL"] = Region("CRZllL", "CRZ", [], [])
# regionDict["CRZllVL"] = Region("CRZllVL", "CRZ", [], [])
#     #validation regions for Znunu
# regionDict["VRZL"] = Region("VRZL", "SRAll", [cleaningCut], [])
# regionDict["VRZVL"] = Region("VRZVL", "SRAll", [cleaningCut], [])
# regionDict["VRZlmtA"] = Region("VRZlmtA", "SRAll", [cleaningCut], [])
# regionDict["VRZtmlA"] = Region("VRZtmlA", "SRAll", [cleaningCut], [])
# regionDict["VRZlmlA"] = Region("VRZlmlA", "SRAll", [cleaningCut], [])


