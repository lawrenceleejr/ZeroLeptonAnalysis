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

def createChannelConfigFromString(s, prefix="", finalVar="meffIncl"):
    # we assume the string s is a comma-separated string of key:value pairs
    
    # for the fullname, we will convert the commas to underscores and the colons to hyphens
    # we set the optimisation flag to true, so that the fullname can be used as the name

    # the name for "finalVar" is used to strip that variable out of the fullname
    # this allows for the recycling of histograms

    d = dict(u.split(":") for u in s.split(","))
    fullname = s.replace(":","-").replace(",","_")
    
    if prefix != "":
        fullname = "%s_%s" % (prefix, fullname)

    d['optimisationRegion'] = True
    d['name'] = fullname
    d['fullname'] = fullname 
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

    def setCommonVars(self):
        # NOTE: I SHOULD BE CALLED BY ANY CONSTRUCTOR. PYTHON WILL PUNCH YOU IN THE FACE IF YOU DONT USE ME.

        # Note: please make sure the types are correct, i.e. set dPhi to -1.0 and not -1. The optimisation regions 
        # convert to your exisiting type -> if you put -1 for dPhi, optimisations of eg 0.4 become 0.

        self.name = ""
        self.fullname = ""

        self.optimisationRegion = False

        #LL Changing weight to new ntuple format
        self.commonWeightList = ["weight"] # Note: eventweight has been moved to sysweight

        #cuts common to all regions (CR,SR,...=
        self.commonCutList = "veto==0"

        #cleaning cuts
        self.doTimingCut = True
        self.doCleaning = True
        self.cleaningCuts = "1" 
        #self.cleaningCuts+="&& (cleaning&15)==0"
        
        #jet multiplicity
        self.nJets = 2
        self.jetPtThreshold = 50

        # jet pts - note the threshold above
        self.jetpt1 = 130
        self.jetpt2 = 60
        self.jetpt3 = -1
        self.jetpt4 = -1
        self.jetpt5 = -1
        self.jetpt6 = -1
        self.jetpt7 = -1
        self.jetpt8 = -1

        #met based variables
        self.MET = 160
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


        #LH added
        # RJigsaw variables
        self.H2PP=-1   
        self.H6PP=-1   

        #region with inverted Ap cut
        self.regionsWithInvertedApCutList = []
        
        #region with fully inverted dphi cuts
        self.regionsWithFullyInvertedDPHICutList = ["CRQ","VRQ1"]

        #region with intermediate dphi cuts
        self.regionsWithIntermediateDPHICutList = ["VRQ4","VRQ3"]

        #region with inverted metsig cuts
        self.regionsWithInvertedMETSIGCutList = ["CRQ","VRQ2","VRQ4"]

        #region with inverted metovermeff cuts
        self.regionsWithInvertedMETOVERMEFFCutList = ["CRQ","VRQ2","VRQ4"]

        #region where the dphi cut is not applied
        self.regionsWithoutDPHICutList = ["CRWT","CRW","CRT","CRZ","VRZ","VRWTplus","VRWTminus","VRWM","VRTM","VRWTplus","VRWTminus","VRT2L"]
        
        #region where the met/meff cut is not applied
        self.regionsWithoutMETOVERMEFFCutList = self.regionsWithoutDPHICutList

        #region where the met significance cut is not applied
        self.regionsWithoutMETSIGCutList = self.regionsWithoutDPHICutList

        # region where the Ap cut is not applied
        #self.regionsWithoutApCutList = ["CRY","CRWT","CRW","CRT","CRZ","VRZ","VRWTplus","VRWTminus","VRWM","VRTM","VRWTplus","VRWTminus","VRT2L", "VRWf", "VRWMf", "VRWM", "VRTf", "VRTMf", "CRQ","VRQ1","VRQ2","VRQ3","VRQ4"]

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
            cutsDict[regionName] = self.getCuts(regionName)
        
        return cutsDict
        
    def getCuts(self, regionName="SR"):
        if regionName not in self.regionDict.keys():
            print "Region %s is unknown. Exit" % regionName
            sys.exit()

        cutList = []
        cutList.append(self.commonCutList)

        # timing cuts
        if self.doTimingCut==True:
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

        # jet cuts
        cutList.append("NJet >= %f" % self.nJets)
        if self.nJets > 0 and not(self.WithoutJetpT1Cut):
            cutList.append("pT_jet1 >= %f" % max(self.jetpt1, self.jetPtThreshold))
        if self.nJets > 1 and not(self.WithoutJetpT2Cut):
            cutList.append("pT_jet2 >= %f" % max(self.jetpt2, self.jetPtThreshold))
        # if self.nJets > 2 and not(self.WithoutJetpT3Cut):
        #     cutList.append("pT_jet3 >= %f" % max(self.jetpt3, self.jetPtThreshold))
        # if self.nJets > 3 and not(self.WithoutJetpT4Cut):
        #     cutList.append("pT_jet4 >= %f" % max(self.jetpt4, self.jetPtThreshold))
        # if self.nJets > 4:
        #     cutList.append("pT_jet5 >= %f" % max(self.jetpt5, self.jetPtThreshold))
        # if self.nJets > 5:
        #     cutList.append("pT_jet6 >= %f" % max(self.jetpt6, self.jetPtThreshold))


        # met cuts
        if self.MET > 0:
            cutList.append("MET >= %f" % self.MET)

        # met upper cuts
        if self.MET_upper > 0:
            cutList.append("MET < %f" % self.MET_upper)

        # # met significance
        # if regionName not in self.regionsWithoutMETSIGCutList and self.METsig > 0:
            
        #     #compute the lower cut if not specified
        #     if self.METsigCRQ < 0:
        #         if self.METsig <= 8:
        #             self.METsigCRQ = self.METsig-2
        #         elif self.METsig<=10:
        #             self.METsigCRQ = self.METsig-4
        #         else:
        #             self.METsigCRQ = self.METsig-6

        #     varName = "met/sqrt(meffInc-met)"
        #     if regionName in self.regionsWithInvertedMETSIGCutList:
        #         cutList.append("%s >= %f && %s < %f" % (varName, self.METsigCRQ, varName, self.METsig)) 
        #     else:
        #         cutList.append("%s >= %f" % (varName, self.METsig)) 


        # Aplanary upper cut   
        # if "SR" in regionName and not(self.WithoutApCut): # in self.regionsWithoutApCutList
        #     cutList.append("Ap >= %f" % (self.Ap))


        # if regionName in self.regionsWithInvertedApCutList:
        #     cutList.append(" Ap < %f" % (self.ApUpperCut))


        #met over meff
        # if regionName not in self.regionsWithoutMETOVERMEFFCutList and self.MET_over_meffNj > 0:

        #     #compute the lower cut if not specified
        #     if self.MET_over_meffNjCRQ < 0:
        #         if self.MET_over_meffNj >= 0.4:    
        #             self.MET_over_meffNjCRQ = self.MET_over_meffNj-0.25
        #         elif self.MET_over_meffNj <= 0.2:    
        #             self.MET_over_meffNjCRQ = self.MET_over_meffNj-0.05
        #         else:
        #             self.MET_over_meffNjCRQ = self.MET_over_meffNj-0.15

        #     varName="met/(met"
        #     for ijet in range(self.nJets):
        #         varName += " + jetPt[%d]" % ijet
        #     varName += ")"
            
        #     if regionName in self.regionsWithInvertedMETOVERMEFFCutList:
        #         #cutList.append(varName+">="+str(self.MET_over_meffNjCRQ)+" && "+varName+"<"+str(self.MET_over_meffNj))
        #         cutList.append("%s >= %f && %s < %f" % (varName, self.MET_over_meffNjCRQ, varName, self.MET_over_meffNj))
        #     else:
        #         if not(self.WithoutMetOverMeffCut):
        #             #cutList.append(varName+">="+str(self.MET_over_meffNj)) 
        #             cutList.append("%s >= %f " % (varName, self.MET_over_meffNj)) 

        # #angular cuts
        # if self.dPhi>=0 and regionName not in self.regionsWithoutDPHICutList:
        #     myString="("  

        #     #first the dphi cut
        #     if self.dPhiCRQ<0: self.dPhiCRQ=self.dPhi/2 # if PhiCRQ is not defined, take the half: 0.4==>0.2
        #     if regionName in self.regionsWithFullyInvertedDPHICutList:
        #         myString += " dPhi < %f" % (self.dPhiCRQ)
        #     elif regionName in self.regionsWithIntermediateDPHICutList:
        #         myString += "( dPhi > %f && dPhi < %f )" % (self.dPhiCRQ, self.dPhi)
        #     else:
        #         myString += " dPhi >= %f " % (self.dPhi)
                
        #     #add also the dphiR cut
        #     if self.dPhiR >= 0 and self.nJets >= 4:  
        #         if self.dPhiRCRQ < 0: 
        #             self.dPhiRCRQ = self.dPhiR/2 # if dPhiRCRQ is not defined, take the half: 0.2==>0.1
        #         if regionName in self.regionsWithFullyInvertedDPHICutList+self.regionsWithIntermediateDPHICutList:                
        #             myString += " || dPhiR < %f" % (self.dPhiRCRQ)
        #         else:
        #             myString += " && dPhiR >= %f" % (self.dPhiR)
                                    
        #     myString += ")"
        #     if not(self.WithoutdPhiCut):
        #         cutList.append(myString) 
            
        # #effective mass cut              
        # if self.meffIncl >= 0 and not(self.WithoutMeffCut): 
        #     cutList.append(" meffInc >= %f " % (self.meffIncl))

        # #effective mass cut upper cut              
        # if self.meffInclUpperCut >= 0:
        #     cutList.append(" meffInc <= %f " % (self.meffInclUpperCut))

        #extra cuts from CR
        cutList += self.regionDict[regionName].extraCutList


        # LH added. RJigsaw variables
        if self.H2PP>0: # default is -1, if set in config then apply cut
            cutList.append(" H2PP>"+str(self.H2PP))
        if self.H6PP>0: # default is -1, if set in config then apply cut
            cutList.append(" H6PP>"+str(self.H6PP))





        cutStr = " && ".join(cutList)
        return "(%s)" % cutStr

    def Print(self, printLevel=2):
        print "##################################################"
        print "# ANALYSIS : ",self.name
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
        self.regionsWithFullyInvertedDPHICutList = ["CRQ","VRQ1"]

        #region with intermediate dphi cuts
        self.regionsWithIntermediateDPHICutList = ["VRQ4","VRQ3"]

        #region with inverted metsig cuts
        self.regionsWithInvertedMETSIGCutList = ["CRQ","VRQ2","VRQ4"]

        #region with inverted metovermeff cuts
        self.regionsWithInvertedMETOVERMEFFCutList = ["CRQ","VRQ2","VRQ4"]

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
        #LH added: RJigsaw
        print "H2PP  :",self.H2PP
        print "H6PP  :",self.H6PP
        

        
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
