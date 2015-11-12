#################################################
# Channel configuration
#################################################

import os
import sys


import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

current_path = ROOT.gROOT.GetMacroPath()
new_path = ':'.join([os.environ['ZEROLEPTONFITTER'],current_path,])
ROOT.gROOT.SetMacroPath(new_path)


########################################################
#
########################################################
class Region:
    def __init__(self,regionName,treeName,extraCutList=[],extraWeightList=[]):
        
        self.name=regionName
        self.suffixTreeName=treeName
        self.extraWeightList=extraWeightList
        self.extraCutList=extraCutList        
        return
    
    def Print(self):
        print "Region     :",self.name
        print "SuffixTree :",self.suffixTreeName
        print "extraWeightList : ",self.extraWeightList
        print "extraCutList : ",self.extraCutList

########################################################
#
########################################################
class ChannelConfig:
    def __init__(self,name,regionDict):
       #default values; overwritten if set through command-line

        self.name=name

        self.regionDict=regionDict

        #self.commonWeightList=["pileupWeight","normWeight","genWeight"]
        self.commonWeightList=["weight"]

        #cuts common to all regions (CR,SR,...=
        self.commonCutList="veto==0"

        #cleaning cuts
        self.doCleaning=False # LH True
        self.cleaningCuts="(!( (abs(jetEta[0])<2. && jet1Chf<0.02) || (abs(jetEta[0])<2. && jet1Chf<0.05 && jet1Emf>0.9) ||  (jetEta[0]<-0.1 && jetEta[0]>-0.2 && jetPhi[0]<2.35 && jetPhi[0]>2.25 && jet1Chf<0.3 && jet1Emf<0.25 )) && abs(timing)<4)"

        #jet multiplicity
        self.nJet=2
        self.jetPtThreshold=60

        #jet pts
        self.pt0=130
        self.pt1=60
        self.pt2=-1
        self.pt3=-1
        self.pt4=-1
        self.pt5=-1
        self.pt6=-1
        self.pt7=-1

        #met based variables
        self.met=160
        self.metsig=-1
        self.met_over_meffNj=-1
        self.metsigCRQ=-1
        self.met_over_meffNjCRQ=-1

        #angular cuts
        self.dPhiCRQ=-1
        self.dPhiRCRQ=-1
        self.dPhi=-1
        self.dPhiR=-1
        
        #effective mass
        self.meff=-1

        #LH Jigsaw variables
        # self.MDR=-1
        # self.minH3P=-1
        # self.H2PP=-1
        # self.deltaQCD=-10
        # self.RPT_upper=+999     

        self.deltaQCD=-1
        self.RPTHT3PP_upper=+999
        self.RPTHT5PP_upper=+999
        self.RPT_upper=+999
        self.R_H2PP_H5PP=-1
        self.R_HT5PP_H5PP=-1
        self.RPZ_upper=+999
        self.minR_pTj2i_HT3PPi=-1
        self.maxR_H1PPi_H2PPi_upper=+999
        self.dangle_upper=+999
        self.HT5PP=-1
        self.H2PP=-1
 
        #region with fully inverted dphi cuts
        self.regionsWithFullyInvertedDPHICutList=["CRQ","VRQ1"]

        #region with intermediate dphi cuts
        self.regionsWithIntermediateDPHICutList=["VRQ4","VRQ3"]

        #region with inverted metsig cuts
        self.regionsWithInvertedMETSIGCutList=["CRQ","VRQ2","VRQ4"]

        #region with inverted metovermeff cuts
        self.regionsWithInvertedMETOVERMEFFCutList=["CRQ","VRQ2","VRQ4"]



        #region where the dphi cut is not applied
        self.regionsWithoutDPHICutList=["CRW","CRT","VRZ","VRWTplus","VRWTminus","VRWM","VRTM","VRWTplus","VRWTminus","VRT2L"]

        #region where the met/meff cut is not applied
        self.regionsWithoutMETOVERMEFFCutList=self.regionsWithoutDPHICutList

        #region where the met significance cut is not applied
        self.regionsWithoutMETSIGCutList=self.regionsWithoutDPHICutList


        return


    def getSuffixTreeName(self,regionName="SR"):
        if regionName not in self.regionDict.keys():
            print "Region ",regionName," is unknow. exit"
            sys.exicut()
        return self.regionDict[regionName].suffixTreeName

    def getWeights(self,regionName="SR",onlyExtraWeights=False):

        if regionName not in self.regionDict.keys():
            print "Region ",regionName," is unknow. exit"
            sys.exicut()

        weightList=[]

        if not onlyExtraWeights:
            weightList+=self.commonWeightList

        weightList+=self.regionDict[regionName].extraWeightList

        return "*".join(weightList)


    def getCutsDict(self):
        
        print "iii"
        cutsDict={}
        for regionName,region in self.regionDict.items():
            print regionName,self.getCuts(regionName)
            cutsDict[regionName]=self.getCuts(regionName)
        return cutsDict
        

    def getCuts(self,regionName="SR"):

        if regionName not in self.regionDict.keys():
            print "Region ",regionName," is unknow. exit"
            sys.exicut()

            
        cutList=[]

        cutList.append(self.commonCutList)
        if self.doCleaning:
            cutList.append(self.cleaningCuts)
       
        """
        LH commenting out 
        #jets cuts
        cutList.append("nJet>="+str(self.nJet))
        if self.nJet>0:
            max(self.pt0,self.jetPtThreshold)
            cutList.append(" jetPt[0]>="+str(max(self.pt0,self.jetPtThreshold)))
        if self.nJet>1:
            cutList.append(" jetPt[1]>="+str(max(self.pt1,self.jetPtThreshold)))
        if self.nJet>2:
            cutList.append(" jetPt[2]>="+str(max(self.pt2,self.jetPtThreshold)))
        if self.nJet>3:
            cutList.append(" jetPt[3]>="+str(max(self.pt3,self.jetPtThreshold)))
        if self.nJet>4:
            cutList.append(" jetPt[4]>="+str(max(self.pt4,self.jetPtThreshold)))
        if self.nJet>5:
            cutList.append(" jetPt[5]>="+str(max(self.pt5,self.jetPtThreshold)))
        if self.nJet>6:
            cutList.append(" jetPt[6]>="+str(max(self.pt6,self.jetPtThreshold)))
        if self.nJet>7:
            cutList.append(" jetPt[7]>="+str(max(self.pt7,self.jetPtThreshold)))
        """
        #met cuts
        if self.met>0:
            cutList.append(" MET>="+str(self.met))


        #metsig
        if regionName not in self.regionsWithoutMETSIGCutList and self.metsig>0:
            
            #compute the lower cut if not specified
            if self.metsigCRQ<0:
                if self.metsig<=8:
                    self.metsigCRQ=self.metsig-2
                elif self.metsig<=10:
                    self.metsigCRQ=self.metsig-4
                else:
                    self.metsigCRQ=self.metsig-6

            varName="met/1000/sqrt((meffInc-met)/1000)"
            if regionName in self.regionsWithInvertedMETSIGCutList:
                cutList.append(varName+">="+str(self.metsigCRQ)+" && "+varName+"<"+str(self.metsig))
            else:
                cutList.append(varName+">="+str(self.metsig))





        #met over meff
        if regionName not in self.regionsWithoutMETOVERMEFFCutList and  self.met_over_meffNj>0:

            #compute the lower cut if not specified
            if self.met_over_meffNjCRQ<0:
                if self.met_over_meffNj >= 0.4:    
                    self.met_over_meffNjCRQ=self.met_over_meffNj- 0.25
                elif self.met_over_meffNj <= 0.2:    
                    self.met_over_meffNjCRQ=self.met_over_meffNj- 0.05
                else:
                    self.met_over_meffNjCRQ=self.met_over_meffNj- 0.15

            varName="met/(met"
            for ijet in range(self.nJet):
                varName+="+jetPt["+str(ijet)+"]"
            varName+=")"
            if regionName in self.regionsWithInvertedMETOVERMEFFCutList:
                cutList.append(varName+">="+str(self.met_over_meffNjCRQ)+" && "+varName+"<"+str(self.met_over_meffNj))
            else:
                cutList.append(varName+">="+str(self.met_over_meffNj))



        #angular cuts
        if self.dPhi>=0 and regionName not in self.regionsWithoutDPHICutList:
            myString="("  

            #first the dphi cut
            if self.dPhiCRQ<0: self.dPhiCRQ=self.dPhi/2 # if PhiCRQ is not defined, take the half: 0.4==>0.2
            if regionName in self.regionsWithFullyInvertedDPHICutList:
                myString+=" dPhi<"+str(self.dPhiCRQ)
            elif regionName in self.regionsWithIntermediateDPHICutList:
                myString+="( dPhi>"+str(self.dPhiCRQ)
                myString+=" && dPhi<"+str(self.dPhi)+")"
            else:
                myString+=" dPhi>="+str(self.dPhi)
                
            #add also the dphiR cut
            if self.dPhiR>=0 and self.nJet>=4:  
                if self.dPhiRCRQ<0: self.dPhiRCRQ=self.dPhiR/2 # if dPhiRCRQ is not defined, take the half: 0.2==>0.1
                if regionName in self.regionsWithFullyInvertedDPHICutList+self.regionsWithIntermediateDPHICutList:                
                    myString+="  || dPhiR<"+str(self.dPhiRCRQ)
                else:
                    myString+=" && dPhiR>="+str(self.dPhiR)
                                    
            myString+=")"
            cutList.append(myString)

        #effective mass cut              
        if self.meff>=0:
            cutList.append(" meffInc>="+str(self.meff))


        # LH Jigsaw variables
        # if self.MDR>=0:
        #     cutList.append(" MDR>="+str(self.MDR))

        # if self.minH3P>=0:
        #     cutList.append(" min(H3Pa,H3Pb)>="+str(self.minH3P)) 

        # if self.H2PP>=0:
        #     cutList.append(" H2PP>="+str(self.H2PP))

        # if self.deltaQCD>-9:
        #     cutList.append(" deltaQCD>="+str(self.deltaQCD))

        # if self.RPT_upper<=990:
        #     cutList.append(" RPT<="+str(self.RPT_upper))
        #     pass  
 

        if self.deltaQCD>=0:
            cutList.append( " deltaQCD >= %f"%self.deltaQCD   )
        if self.RPTHT3PP_upper<=990:
            cutList.append( " (pTCM / ( pTCM + HT3PP) ) <= %f"%self.RPTHT3PP_upper   )
        if self.RPTHT5PP_upper<=990:
            cutList.append( " (pTCM / ( pTCM + HT5PP) ) <= %f"%self.RPTHT5PP_upper   )
        if self.RPT_upper<=990:
            cutList.append( " RPT <= %f"%self.RPT_upper   )
        if self.R_H2PP_H5PP>=0:
            cutList.append( " R_H2PP_H5PP >= %f"%self.R_H2PP_H5PP   )
        if self.R_HT5PP_H5PP>=0:
            cutList.append( " R_HT5PP_H5PP >= %f"%self.R_HT5PP_H5PP   )
        if self.RPZ_upper<=990:
            cutList.append( " RPZ <= %f"%self.RPZ_upper   )
        if self.minR_pTj2i_HT3PPi>=0:
            cutList.append( " minR_pTj2i_HT3PPi >= %f"%self.minR_pTj2i_HT3PPi   )
        if self.maxR_H1PPi_H2PPi_upper<=990:
            cutList.append( " maxR_H1PPi_H2PPi <= %f"%self.maxR_H1PPi_H2PPi_upper   )
        if self.dangle_upper<=990:
            cutList.append( " dangle <= %f"%self.dangle_upper   )
        if self.HT5PP>=0:
            cutList.append( " HT5PP >= %f"%self.HT5PP   )
        if self.H2PP>=0:
            cutList.append( " H2PP >= %f"%self.H2PP   )


        #extra cuts from CR
        cutList+=self.regionDict[regionName].extraCutList


        return "("+" && ".join(cutList)+")"

    def Print(self,printLevel=2):
        print "##################################################"
        print "# Analysis :",self.name
        print "##################################################"
        print "=================================================="
        print "General settings:"
        print " "
        print "Weights applied to all regions     : ",self.commonWeightList
        print "Cuts applied to all regions        : ",self.commonCutList
        print "doCleaning                         : ",self.doCleaning
        print "Cleaning cuts                      : ",self.cleaningCuts
        print "Regions without dPhi/dPhiR cuts    : ",self.regionsWithoutDPHICutList
        print "Regions without METSIG cuts        : ",self.regionsWithoutMETSIGCutList
        print "Regions without METOVERMEFF cuts   : ",self.regionsWithoutMETOVERMEFFCutList
        print "Regions with inverted dphi cut     : ",self.regionsWithFullyInvertedDPHICutList
        print "Regions with intermediate dphi cut : ",self.regionsWithIntermediateDPHICutList
        print "Regions with inverted metsig cut   : ",self.regionsWithInvertedMETSIGCutList
        print "Regions with inverted met/meff cut : ",self.regionsWithInvertedMETOVERMEFFCutList
     


        #region with fully inverted dphi cuts
        self.regionsWithFullyInvertedDPHICutList=["CRQ","VRQ1"]

        #region with intermediate dphi cuts
        self.regionsWithIntermediateDPHICutList=["VRQ4","VRQ3"]

        #region with inverted metsig cuts
        self.regionsWithInvertedMETSIGCutList=["CRQ","VRQ2","VRQ4"]

        #region with inverted metovermeff cuts
        self.regionsWithInvertedMETOVERMEFFCutList=["CRQ","VRQ2","VRQ4"]



        print "=================================================="
        print "Cuts:" 
        print " "
        print "nJet               :",self.nJet
        print "pt0                :",self.pt0
        print "pt1                :",self.pt1
        print "pt2                :",self.pt2
        print "pt3                :",self.pt3
        print "pt4                :",self.pt4
        print "pt5                :",self.pt5
        print "met                :",self.met
        print "metsig             :",self.metsig
        print "met_over_meffNj    :",self.met_over_meffNj
        print "metsigCRQ          :",self.metsigCRQ
        print "met_over_meffNjCRQ :",self.met_over_meffNjCRQ
        print "dPhi               :",self.dPhi
        print "dPhiCRQ            :",self.dPhiCRQ
        print "dPhiR              :",self.dPhiR
        print "meff               :",self.meff
        


        if printLevel>0:

            print "=================================================="
            for regionName,region in self.regionDict.items():
                region.Print()
                if printLevel>1:                    
                    print self.getSuffixTreeName(regionName)
                    print self.getCuts(regionName)
                    print self.getWeights(regionName)

                print "=================================================="


#CRT (nBJet>0)
#CRW (nBJet==0)
#CRY (phQuality == 2 && phIso < 5000.) && (nLep == 0)
#CRQ
