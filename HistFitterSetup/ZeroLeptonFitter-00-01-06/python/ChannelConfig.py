#################################################
# Channel configuration
#################################################

from collections import OrderedDict
from copy import deepcopy
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

current_path = ROOT.gROOT.GetMacroPath()
new_path = ':'.join([os.environ['ZEROLEPTONFITTER'],current_path,])
ROOT.gROOT.SetMacroPath(new_path)

def createChannelConfigFromString(s, prefix="", finalVar="meffIncl"):
    # we assume the string s is a comma-separated string of key:value pairs
    
    # for the fullname, we will convert the commas to underscores and the colons to hyphens
    # we set the optimisation flag to true, so that the fullname can be used as the name

    # the name for "finalVar" is used to strip that variable out of the fullname
    # this allows for the recycling of histograms

    d = OrderedDict(u.split(":") for u in s.split(","))

    # remove it, ensure it's at the end. construct a dict without final var for the data name
    if finalVar in d:
        finalValue = d[finalVar]
        del d[finalVar]
        dictForName = deepcopy(d)

        d.update({finalVar: finalValue})

    fullname = s.replace(":","-").replace(",","_")
    fullnameForData = "_".join("%s-%s" % (key,val) for (key,val) in dictForName.iteritems() ) 
   
    if prefix != "":
        fullname = "%s_%s" % (prefix, fullname)
        fullnameForData = "%s_%s" % (prefix, fullnameForData)

    d['optimisationRegion'] = True
    d['name'] = fullname
    d['fullname'] = fullname 
    d['fullnameForData'] = fullnameForData 
    c = ChannelConfig(**d)

    return c

########################################################
#
########################################################
class Region:
    def __init__(self, regionName, treeName, extraCutList = [], extraWeightList = []):
        
        self.name = regionName
        self.suffixTreeName = treeName
        self.extraWeightList = extraWeightList
        self.extraCutList = extraCutList        
        return

    def __str__(self):
        retval = ("Region          : %s\n"
                  "SuffixTree      : %s\n"
                  "extraWeightList : %s\n"
                  "extraCutList    : %s") % (self.name, self.suffixTreeName, self.extraWeightList, self.extraCutList)
        return retval

########################################################
#
########################################################
class ChannelConfig:
    def __init__(self, **kwargs):
        self.setCommonVars()
       
        #print kwargs
        for key in kwargs:
            val = kwargs[key]
           
            # do some automatic type conversions based on the existing defaults
            original = getattr(self, key, None)
            if original is not None and isinstance(original, int):
                val = int(float(val))
            elif original is not None and isinstance(original, float):
                val = float(val)
            elif original is not None and isinstance(original, bool):
                val = bool(val)
            elif original is None and 'optimisationRegion' in kwargs:
                print "Cannot set new attribute %s for optimisation region" % key
                sys.exit()
                
            setattr(self, key, val)

        if hasattr(self, 'optimisationRegion') and self.optimisationRegion == True:
            # don't force the full name requirement for optimisation regions
            pass
        elif len(self.name) >= 20:
            print "************************************************************"
            print "Problem with SR:", self.name
            print "The name of your SR is too long. It should have less than 20 characters."
            print "Please make it shorter. If you want a longer name, you can use the member fullname"
            print "Will exit...."
            print "************************************************************"
            sys.exit()
       
        if self.name == "":
            print "Cannot have an SR without name. Exiting."
            sys.exit()

        if not self.name.strip().replace("_", "").replace("-", "").replace(".","").isalnum():
            print "Cannot have an SR with non-alphanumeric characters (name='%s'). Exiting." % self.name
            sys.exit()

        if os.sep in self.name:
            print "Cannot have an SR with the path separator in it. Exiting"
            sys.exit()

        if " " in self.name:
            print "Cannot have an SR with a space in the name. Exiting"
            sys.exit()

        if self.fullname == "":
            self.fullname = self.name

        if self.fullnameForData == "":
            self.fullnameForData = self.fullname

    def setCommonVars(self):
        # NOTE: I SHOULD BE CALLED BY ANY CONSTRUCTOR. PYTHON WILL PUNCH YOU IN THE FACE IF YOU DONT USE ME.

        self.useFilteredNtuples = False
        
        # Note: please make sure the types are correct, i.e. set dPhi to -1.0 and not -1. The optimisation regions 
        # convert to your exisiting type -> if you put -1 for dPhi, optimisations of eg 0.4 become 0.

        self.name = ""
        self.fullname = ""
        self.fullnameForData = ""

        self.optimisationRegion = False

        # self.commonWeightList = ["pileupWeight", "normWeight", "genWeight"] # Note: eventweight has been moved to sysweight
        self.commonWeightList = ["weight"] # Note: eventweight has been moved to sysweight
        # self.commonWeightList = ["(weight*(weight>0) + 1*(weight==0) )"] # Note: eventweight has been moved to sysweight
        # self.commonWeightList = ["1"]

        #cuts common to all regions (CR,SR,...=
        self.commonCutList = ["veto==0"]

        #cleaning cuts
        self.doTimingCut = True
        self.doCleaning = True
        self.cleaningCuts = "1" 
        #self.cleaningCuts+="&& (cleaning&15)==0"
        
        #jet multiplicity
        self.nJets = 2
        self.jetPtThreshold = 50

        # jet pts - note the threshold above
        self.jetpt1 = -1
        self.jetpt2 = -1
        self.jetpt3 = -1
        self.jetpt4 = -1
        self.jetpt5 = -1
        self.jetpt6 = -1
        self.jetpt7 = -1
        self.jetpt8 = -1

        #met based variables
        self.MET = -1
        self.MET_upper = -1
        self.METsig = -1
        self.MET_over_meffNj = -1.0
        self.METsigCRQ = -1
        self.MET_over_meffNjCRQ = -1.0

        #angular cuts
        self.dPhiCRQ = -1.0
        self.dPhiRCRQ = -1.0
        self.dPhi = -1.0
        self.dPhiR = -1.0
        
        #effective mass
        self.meffIncl = -1

        #effective mass upper cut
        self.meffInclUpperCut = -1

        #Aplanary
        self.Ap = -1.0

        #Aplanary
        self.ApUpperCut = -1.


        ########################################
        #LL RJigsaw Variables

        #Common Variables

        self.MDR=-1
        self.deltaQCD=-1
        self.H2PP=-1
        self.H2PP_loose=-1

        #Squark Variables
        self.RPTHT3PP_upper=+999

        self.R_H2PP_H3PP=-1
        self.R_H2PP_H3PP_upper=+999

        self.RPZ_HT3PP_upper=+999

        self.R_ptj2_HT3PP=-1
        self.cosP_upper = +999
        self.HT3PP=-1
        self.HT3PP_loose=-1

        #Gluino Variables

        self.RPTHT5PP_upper=+999
        self.R_H2PP_H5PP=-1
        self.R_HT5PP_H5PP=-1
        self.RPZ_HT5PP_upper=+999
        self.minR_pTj2i_HT3PPi=-1
        self.maxR_H1PPi_H2PPi_upper=+999
        self.dangle_upper=+999
        self.HT5PP=-1
        self.HT5PP_loose=-1


        #Compressed Variables
        self.RPTHT1CM_upper=+999
        self.PIoHT1CM=-1
        self.PIoHT1CM_CR=-1
        self.cosS=-1
        self.MS=-1
        self.MS_loose=-1
        self.HT1CM=-1
        self.HT1CM_loose=-1




        #region with inverted Ap cut
        self.regionsWithInvertedApCutList = []
        
        #region with fully inverted dphi cuts
        self.regionsWithFullyInvertedDPHICutList = ["CRQ"]

        #region with intermediate dphi cuts
        self.regionsWithIntermediateDPHICutList = ["VRQ4","VRQ3"]

        #region with inverted metsig cuts
        self.regionsWithInvertedMETSIGCutList = []#["CRQ","VRQ2","VRQ4"]

        #region with inverted metovermeff cuts
        self.regionsWithInvertedMETOVERMEFFCutList = ["CRQ","VRQ2"]

        #region where the dphi cut is not applied
        self.regionsWithoutDPHICutList = ["CRWT","CRW","CRT","CRZ","VRWTplus","VRWTminus","VRWM","VRTM","VRWTplus","VRWTminus","VRT2L"]
        
        #region where the met/meff cut is not applied
        self.regionsWithoutMETOVERMEFFCutList = self.regionsWithoutDPHICutList

        #region where the met significance cut is not applied
        self.regionsWithoutMETSIGCutList = self.regionsWithoutDPHICutList

        # region where the Ap cut is not applied
        self.regionsWithoutApCutList = self.regionsWithoutDPHICutList+["CRY","CRQ","VRQ1","VRQ2","VRQ3","VRQ4"]


        ##################################################
        ## LL RJigsaw


        self.regionsWithInvertedDangleCutList = ["VRTZL","CRQ","VRQ1","VRQ2"]
        self.regionsWithInvertedRPZCutList = ["VRTZL"]
        # self.regionsWithInvertedDangleCutList = ["CRT"]
        # self.regionsWithInvertedRPZCutList = ["CRT"]

        self.regionsWithLooserDeltaQCDCutList = ["VRTZL"]
        self.regionsWithoutDeltaQCDCutList = []
        self.regionsWithoutRPTCutList = ["CRQ","VRQ1","VRQ2"]

        self.regionsWithInvertedDeltaQCDCutList = ["CRQ","VRQ1"]
        self.regionsWithInvertedRPTCutList = []
        # self.regionsWithInvertedRPTCutList = ["CRQ"]

        self.regionsWithInvertedMSCutList = []
        self.regionsWithInvertedPIoHT1CMCutList = []#["CRQ"]

        # self.regionsWithLooserScaleCuts = ["VRTZL","CRT","CRW","CRY", "VRZa","VRWa","VRTa"]
        # self.regionsWithLooserMSCutList = ["VRTZL","CRT","CRW","CRY", "VRZb","VRWb","VRTb"]
        # self.regionsWithLooserH2PPCutList = ["VRTZL","CRT","CRW","CRY", "VRZb","VRWb","VRTb"]

        self.regionsWithLooserScaleCuts = ["VRTZL","CRT","CRW", "VRZa","VRWa","VRTa"]
        self.regionsWithoutMSCutList = []#self.regionsWithLooserScaleCuts
        self.regionsWithLooserMSCutList = ["VRTZL","CRT","CRW", "VRZb","VRWb","VRTb"]
        self.regionsWithLooserH2PPCutList = ["VRTZL","CRT","CRW", "VRZb","VRWb","VRTb"]

        self.regionsWithoutScaleCuts = ["VRZAndreas"]
        self.regionsWithoutMinCut = ["VRZAndreas"]
        self.regionsWithoutMaxCut = ["VRZAndreas"]

        self.CRList = ["CRT","CRW","CRY"]


        self.WithoutMeffCut = False
        self.WithoutMetOverMeffCut = False 
        self.WithoutdPhiCut = False
        self.WithoutApCut = False
        self.WithoutJetpT1Cut = False
        self.WithoutJetpT2Cut = False
        self.WithoutJetpT3Cut = False
        self.WithoutJetpT4Cut = False 

        return
    
    def getSuffixTreeName(self,regionName = "SR"):
        if regionName not in self.regionDict.keys():
            print "Region %s is unknown. Exit" % regionName
            sys.exit()
        return self.regionDict[regionName].suffixTreeName

    def getWeights(self, regionName="SR", onlyExtraWeights=False):
        if regionName not in self.regionDict.keys():
            print "Region %s is unknown. Exit" % regionName
            sys.exit()

        weightList = []
        if not onlyExtraWeights:
            weightList += self.commonWeightList

        weightList += self.regionDict[regionName].extraWeightList

        return " * ".join(weightList)


    def getCutsDict(self):
        cutsDict = {}
        for regionName,region in self.regionDict.items():
            cutsDict[regionName] = self.getCuts(regionName=regionName)
        
        return cutsDict
        
    def getCuts(self, regionName="SR"):
        if regionName not in self.regionDict.keys():
            print "Region %s is unknown. Exit" % regionName
            sys.exit()

        cutList = []
        # Start with cuts take away a huge chunk
        
        #effective mass cut              
        if self.meffIncl >= 0 and not(self.WithoutMeffCut): 
            cutList.append(" Meff >= %f " % (self.meffIncl))

        #effective mass cut upper cut              
        if self.meffInclUpperCut >= 0:
            cutList.append(" Meff <= %f " % (self.meffInclUpperCut))
        
        # met cuts
        if self.MET > 0:
            cutList.append("MET >= %f" % self.MET)
        
        # met upper cuts
        if self.MET_upper > 0:
            cutList.append("MET < %f" % self.MET_upper)
        

        
        #LH commenting out 
        #jets cuts
        cutList.append("NJet>="+str(self.nJets))
        if self.nJets>0:
            # max(self.pt0,self.jetPtThreshold)
            cutList.append(" pT_jet1>="+str(self.jetpt1  ))
        if self.nJets>1:
            cutList.append(" pT_jet2>="+str(self.jetpt2  ))
        if self.nJets>2:
            cutList.append(" pT_jet3>="+str(self.jetpt3  ))
        if self.nJets>3:
            cutList.append(" pT_jet4>="+str(self.jetpt4  ))
        if self.nJets>4:
            cutList.append(" pT_jet5>="+str(self.jetpt5  ))
        if self.nJets>5:
            cutList.append(" pT_jet6>="+str(self.jetpt6  ))
        # if self.nJet>6:
        #     cutList.append(" jetP>="+str(max(self.pt6,self.jetPtThreshold)))
        # if self.nJet>7:
        #     cutList.append(" jetPt[7]>="+str(max(self.pt7,self.jetPtThreshold)))
        #"""

        # Now on to the rest
        if self.commonCutList != []:
            cutList+=self.commonCutList

        # timing cuts
        if self.doTimingCut == True:
            cutList.append("(abs(timing)<4)")
       
        # cleaning cuts
        if self.doCleaning:
            if self.regionDict[regionName].suffixTreeName == "SRAll":
                self.cleaningCuts = "((cleaning&3) == 0)"
            elif self.regionDict[regionName].suffixTreeName == "CRWT":
                self.cleaningCuts = "((cleaning&15) == 0)"
            elif self.regionDict[regionName].suffixTreeName == "VRWT":
                self.cleaningCuts = "((cleaning&15) == 0)"
            elif self.regionDict[regionName].suffixTreeName == "CRZ":
                self.cleaningCuts = "((cleaning&7) == 0)"
            elif self.regionDict[regionName].suffixTreeName == "CRY":
                self.cleaningCuts = "((cleaning&15) == 0)"   
            elif self.regionDict[regionName].suffixTreeName == "CRQ":
                self.cleaningCuts = "((cleaning&3)==0)"   
            else: 
                self.cleaningCuts = "(1)"
            
            cutList.append(self.cleaningCuts)

        #angular cuts
        if self.dPhi>=0 and regionName not in self.regionsWithoutDPHICutList:
            myString="("  

            #first the dphi cut
            if self.dPhiCRQ<0: self.dPhiCRQ=self.dPhi/2 # if PhiCRQ is not defined, take the half: 0.4==>0.2
            if regionName in self.regionsWithFullyInvertedDPHICutList:
                myString += " dphi < %f" % (self.dPhiCRQ)
            elif regionName in self.regionsWithIntermediateDPHICutList:
                myString += "( dphi > %f && dphi < %f )" % (self.dPhiCRQ, self.dPhi)
            else:
                myString += " dphi >= %f " % (self.dPhi)
                
            # add also the dphiR cut
            if self.dPhiR >= 0 and self.nJets >= 4:  
                if self.dPhiRCRQ < 0: 
                    self.dPhiRCRQ = self.dPhiR/2 # if dPhiRCRQ is not defined, take the half: 0.2==>0.1
                if regionName in self.regionsWithFullyInvertedDPHICutList+self.regionsWithIntermediateDPHICutList:                
                    myString += " || dphiR < %f" % (self.dPhiRCRQ)
                else:
                    myString += " && dphiR >= %f" % (self.dPhiR)
                                    
            myString += ")"
            if not(self.WithoutdPhiCut):
                cutList.append(myString) 

        # met significance
        if regionName not in self.regionsWithoutMETSIGCutList and self.METsig > 0:
            
            #compute the lower cut if not specified
            if self.METsigCRQ < 0:
                if self.METsig <= 8:
                    self.METsigCRQ = self.METsig-2
                elif self.METsig<=10:
                    self.METsigCRQ = self.METsig-4
                else:
                    self.METsigCRQ = self.METsig-6

            varName = "MET/sqrt(Meff-MET)"
            if regionName in self.regionsWithInvertedMETSIGCutList:
                cutList.append("%s >= %f && %s < %f" % (varName, self.METsigCRQ, varName, self.METsig)) 
            else:
                cutList.append("%s >= %f" % (varName, self.METsig)) 


        # Aplanary upper cut   
        if self.Ap>=0 and regionName not in self.regionsWithoutApCutList:
            cutList.append("Aplan >= %f" % (self.Ap))

        if regionName in self.regionsWithInvertedApCutList:
            cutList.append(" Aplan < %f" % (self.ApUpperCut))

        #met over meff
        if regionName not in self.regionsWithoutMETOVERMEFFCutList and self.MET_over_meffNj > 0:

            #compute the lower cut if not specified
            if self.MET_over_meffNjCRQ < 0:
                if self.MET_over_meffNj >= 0.4:    
                    self.MET_over_meffNjCRQ = self.MET_over_meffNj-0.25
                elif self.MET_over_meffNj <= 0.2:    
                    self.MET_over_meffNjCRQ = self.MET_over_meffNj-0.05
                else:
                    self.MET_over_meffNjCRQ = self.MET_over_meffNj-0.15

            varName="MET/(MET"
            for ijet in range(self.nJets):
                varName += " + pT_jet%s"%(str(ijet+1) )
            varName += ")"
            
            if regionName in self.regionsWithInvertedMETOVERMEFFCutList:
                #cutList.append(varName+">="+str(self.MET_over_meffNjCRQ)+" && "+varName+"<"+str(self.MET_over_meffNj))
                cutList.append("%s >= %f && %s < %f" % (varName, self.MET_over_meffNjCRQ, varName, self.MET_over_meffNj))
            else:
                if not(self.WithoutMetOverMeffCut):
                    #cutList.append(varName+">="+str(self.MET_over_meffNj)) 
                    cutList.append("%s >= %f " % (varName, self.MET_over_meffNj)) 
            


        ###############################################################################
        ###############################################################################
        ###############################################################################

        # LL RJigsaw


        if self.MS>=0:
            if regionName in self.regionsWithInvertedMSCutList:
                cutList.append( " MS <= %f"%self.MS )
            elif regionName in self.regionsWithoutMSCutList:
                pass
            elif regionName in self.regionsWithLooserMSCutList:
                cutList.append( " MS >= %f"%self.MS_loose )
            else:
                cutList.append( " MS >= %f"%self.MS )

        if self.deltaQCD>=0:
            if regionName in self.regionsWithLooserDeltaQCDCutList:
                cutList.append( " deltaQCD >= -0.5"  )
            elif regionName in self.regionsWithInvertedDeltaQCDCutList:
                cutList.append( " deltaQCD <= %f"%self.deltaQCD )
            elif regionName in self.regionsWithoutDeltaQCDCutList:
                pass
            else:
                cutList.append( " deltaQCD >= %f"%self.deltaQCD )

        if regionName in self.regionsWithInvertedRPTCutList:
            if self.RPTHT3PP_upper<=990:
                cutList.append( " RPT_HT3PP >= %f"%self.RPTHT3PP_upper   )
            if self.RPTHT5PP_upper<=990:
                cutList.append( " RPT_HT5PP >= %f"%self.RPTHT5PP_upper   )
            if self.RPTHT1CM_upper<=990:
                cutList.append(  " RPT_HT1CM >= %f "%self.RPTHT1CM_upper   )
        elif regionName not in self.regionsWithoutRPTCutList:            
            if self.RPTHT3PP_upper<=990:
                cutList.append( " RPT_HT3PP <= %f"%self.RPTHT3PP_upper   )
            if self.RPTHT5PP_upper<=990:
                cutList.append( " RPT_HT5PP <= %f"%self.RPTHT5PP_upper   )
            if self.RPTHT1CM_upper<=990:
                cutList.append(  " RPT_HT1CM <= %f "%self.RPTHT1CM_upper   )

        if regionName in self.regionsWithInvertedMETOVERMEFFCutList:

            if self.R_H2PP_H5PP>=0:
                cutList.append( " R_H2PP_H5PP <= %f"%self.R_H2PP_H5PP   )
            if self.R_H2PP_H3PP>=0:
                cutList.append( " R_H2PP_H3PP <= %f"%self.R_H2PP_H3PP   )

        elif regionName not in self.regionsWithoutMETOVERMEFFCutList:

            if self.R_H2PP_H5PP>=0:
                cutList.append( " R_H2PP_H5PP >= %f"%self.R_H2PP_H5PP   )
            if self.R_H2PP_H3PP>=0:
                cutList.append( " R_H2PP_H3PP >= %f"%self.R_H2PP_H3PP   )
            if self.R_H2PP_H3PP_upper<=990:
                cutList.append( " R_H2PP_H3PP <= %f"%self.R_H2PP_H3PP_upper   )
                    

        if self.R_HT5PP_H5PP>=0:
            cutList.append( " R_HT5PP_H5PP >= %f"%self.R_HT5PP_H5PP   )

        if not(regionName in self.regionsWithoutMinCut):
            if self.minR_pTj2i_HT3PPi>=0:
                cutList.append( " minR_pTj2i_HT3PPi >= %f"%self.minR_pTj2i_HT3PPi   )
        if not(regionName in self.regionsWithoutMaxCut):
            if self.maxR_H1PPi_H2PPi_upper<=990:
                cutList.append( " maxR_H1PPi_H2PPi <= %f"%self.maxR_H1PPi_H2PPi_upper   )

        if self.RPZ_HT3PP_upper<=990:
            if regionName not in self.regionsWithInvertedRPZCutList:
                cutList.append( " RPZ_HT3PP <= %f"%self.RPZ_HT3PP_upper   )
            else:
                cutList.append( " RPZ_HT3PP >= %f"%self.RPZ_HT3PP_upper   )

        if self.RPZ_HT5PP_upper<=990:
            if regionName not in self.regionsWithInvertedRPZCutList:
                cutList.append( " RPZ_HT5PP <= %f"%self.RPZ_HT5PP_upper   )
            else:
                cutList.append( " RPZ_HT5PP >= %f"%self.RPZ_HT5PP_upper   )


        if self.R_ptj2_HT3PP>=0:
            cutList.append( " pT_jet2 / HT3PP >= %f"%self.R_ptj2_HT3PP   )

        if self.cosP_upper<=990:
            cutList.append( " abs(cosP) <= %f"%self.cosP_upper   )

        if self.dangle_upper<=990:
            if regionName not in self.regionsWithInvertedDangleCutList:
                cutList.append( " dangle <= %f"%self.dangle_upper   )
            else:
                cutList.append( " dangle >= %f"%self.dangle_upper   )

        if self.PIoHT1CM_CR>=0 and regionName in self.CRList:
            cutList.append(  " PIoHT1CM >= %f "%self.PIoHT1CM_CR   )
        elif self.PIoHT1CM>=0:
            if regionName in self.regionsWithInvertedPIoHT1CMCutList:
                cutList.append(  " PIoHT1CM <= %f "%self.PIoHT1CM   )
            else:
                cutList.append(  " PIoHT1CM >= %f "%self.PIoHT1CM   )
        if self.cosS>=0:
            cutList.append(  " cosS >= %f "%self.cosS   )



        if regionName in self.regionsWithLooserH2PPCutList:
            if self.H2PP>=0:
                cutList.append( " H2PP >= %f"%self.H2PP_loose   )
        else:
            if self.H2PP>=0:
                cutList.append( " H2PP >= %f"%self.H2PP   )


        if regionName in self.regionsWithoutScaleCuts:
            pass

        elif regionName in self.regionsWithLooserScaleCuts:

            if self.HT1CM>=0:
                cutList.append( " HT1CM >= %f"%self.HT1CM_loose   )
            if self.HT5PP>=0:
                cutList.append( " HT5PP >= %f"%self.HT5PP_loose   )
            if self.HT3PP>=0:
                cutList.append( " HT3PP >= %f"%self.HT3PP_loose   )

        else:
            if self.HT1CM>=0:
                cutList.append( " HT1CM >= %f"%self.HT1CM   )
            if self.HT5PP>=0:
                cutList.append( " HT5PP >= %f"%self.HT5PP   )
            if self.HT3PP>=0:
                cutList.append( " HT3PP >= %f"%self.HT3PP   )

        if self.MDR>=0:
            cutList.append(" MDR >= %f"%self.MDR)



        #extra cuts from CR
        cutList += self.regionDict[regionName].extraCutList

        cutStr = " && ".join(cutList)
        return "(%s)" % cutStr

    def Print(self, printLevel=2):
        print "##################################################"
        print "# ANALYSIS : ",self.name
        print "##################################################"
        print "=================================================="
        print "General settings:"
        print " "
        print "Use filtered ntuples:              : ", self.useFilteredNtuples
        print "Weights applied to all regions     : ", self.commonWeightList
        print "Cuts applied to all regions        : ", self.commonCutList
        print "doCleaning                         : ", self.doCleaning
        print "Cleaning cuts                      : ", self.cleaningCuts
        print "Regions without dPhi/dPhiR cuts    : ", self.regionsWithoutDPHICutList
        print "Regions without METSIG cuts        : ", self.regionsWithoutMETSIGCutList
        print "Regions without METOVERMEFF cuts   : ", self.regionsWithoutMETOVERMEFFCutList
        print "Regions with inverted dphi cut     : ", self.regionsWithFullyInvertedDPHICutList
        print "Regions with intermediate dphi cut : ", self.regionsWithIntermediateDPHICutList
        print "Regions with inverted metsig cut   : ", self.regionsWithInvertedMETSIGCutList
        print "Regions with inverted met/meff cut : ", self.regionsWithInvertedMETOVERMEFFCutList
        print "Using LL's RJigsaw Version........"

        print "Regions with self.regionsWithLooserScaleCuts   : ", self.regionsWithLooserScaleCuts           
        print "Regions with self.regionsWithoutMSCutList      : ", self.regionsWithoutMSCutList           
        print "Regions with self.regionsWithLooserMSCutList   : ", self.regionsWithLooserMSCutList           
        print "Regions with self.regionsWithLooserH2PPCutList : ", self.regionsWithLooserH2PPCutList           



        print "=================================================="
        print "Cuts:" 
        print " "
        print "nJets              : ", self.nJets
        print "jetpt1             : ", max(self.jetpt1, self.jetPtThreshold)
        print "jetpt2             : ", max(self.jetpt2, self.jetPtThreshold)
        print "jetpt3             : ", max(self.jetpt3, self.jetPtThreshold)
        print "jetpt4             : ", max(self.jetpt4, self.jetPtThreshold)
        print "jetpt5             : ", max(self.jetpt5, self.jetPtThreshold)
        print "jetpt6             : ", max(self.jetpt6, self.jetPtThreshold)
        print "met                : ", self.MET
        print "METsig             : ", self.METsig
        print "MET_over_meffNj    : ", self.MET_over_meffNj
        print "METsigCRQ          : ", self.METsigCRQ
        print "MET_over_meffNjCRQ : ", self.MET_over_meffNjCRQ
        print "dPhi               : ", self.dPhi
        print "dPhiCRQ            : ", self.dPhiCRQ
        print "dPhiR              : ", self.dPhiR
        print "meffIncl           : ", self.meffIncl
        print "Ap                 : ", self.Ap
        
        if printLevel > 0:

            print "=================================================="
            for regionName, region in self.regionDict.items():
                print region
                if printLevel > 1:  
                    print "Additional debugging info for %s:" % regionName
                    print "\t Suffix for tree name: %s" % self.getSuffixTreeName(regionName)
                    print "\t Cuts: %s " % (self.getCuts(regionName))
                    print "\t Weights: %s " % (self.getWeights(regionName))

                print "=================================================="


#CRT (nBJet>0)
#CRW (nBJet==0)
#CRY (phQuality == 2 && phIso < 5000.) && (nLep == 0)
#CRQ
