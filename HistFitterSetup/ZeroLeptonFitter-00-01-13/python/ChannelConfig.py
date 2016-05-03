#################################################
# Channel configuration
#################################################

from collections import OrderedDict
from copy import deepcopy
import os
import sys
import ROOT
import math
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
        elif len(self.name) >= 40:
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

        self.commonWeightList = ["normWeight", "genWeight"] # Note: eventweight has been moved to sysweight

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

        #jet 
        self.fatjet1MassMin = -1
        self.fatjet1MassMax = -1
        self.fatjet2MassMin = -1
        self.fatjet2MassMax = -1

        # jet pts - note the threshold above
        self.jetpt1 = 200
        self.jetpt2 = 50
        self.jetpt3 = -1
        self.jetpt4 = -1
        self.jetpt5 = -1
        self.jetpt6 = -1
        self.jetpt7 = -1
        self.jetpt8 = -1

        #met based variables
        self.MET = 200
        self.MET_upper = -1
        self.METsig = -1
        self.MET_over_meffNj = -1.0
        self.METsigCRQ = -1
        self.MET_over_meffNjCRQ = -1.0

        #angular cuts
        self.dPhiCRQ = 0.2
        self.dPhiRCRQ = 0.1
        self.dPhi = -1.0
        self.dPhiR = -1.0
        
        #effective mass
        self.meffIncl = -1
        self.meffInclLoose = -1

        #effective mass upper cut
        self.meffInclUpperCut = -1

        #Aplanary
        self.Ap = -1.0

        #Aplanary
        self.ApUpperCut = -1.

        #region for Loose CR
        self.regionForLooseCRList = ["CRYL","CRWL","CRTL","CRZllL","VRZL"]

        #region for Very Loose CR
        self.regionForVeryLooseCRList =["CRWVL","CRZllVL","VRZVL","CRTVL"]

        #region for minimum MET cuts 
        self.regionWithMinimumMETCutsList =["CRYlmlA","CRYlmtA","VRWlmtA","VRWlmlA","VRZlmtA","VRZlmlA"]+self.regionForLooseCRList
        #self.regionWithMinimumMETCutsList =self.regionForLooseCRList
        #self.regionWithMinimumMETCutsList =[]

        #regions with looser meff cuts
        self.regionsWithLooserMeffCuts = []
        
        #region with fully inverted dphi cuts
        self.regionsWithFullyInvertedDPHICutList = ["CRQ","VRQ1"]

        #region with intermediate dphi cuts
        self.regionsWithIntermediateDPHICutList = ["VRQ4","VRQ3"]

        #region with inverted metsig cuts
        self.regionsWithInvertedMETSIGCutList = ["CRQ","VRQ2","VRQ4"]

        #region with inverted metovermeff cuts
        self.regionsWithInvertedMETOVERMEFFCutList = ["CRQ","VRQ2","VRQ4"]

        #region with inverted MET cut
        self.regionsWithInvertedMETCutList = self.regionForVeryLooseCRList

        #region where the dphi cut is not applied
        self.regionsWithoutDPHICutList = ["CRWT","CRW","CRT","CRZ","VRZ","VRWTplus","VRWTminus","VRWM","VRTM","VRWTplus","VRWTminus","VRT2L"]+self.regionForVeryLooseCRList 
        
        #region where the met/meff cut is not applied
        #self.regionsWithoutMETOVERMEFFCutList = self.regionsWithoutDPHICutList+self.regionWithMinimumMETCutsList
        self.regionsWithoutMETOVERMEFFCutList = self.regionsWithoutDPHICutList+self.regionForLooseCRList + ["CRYlmtA","CRYlmlA","VRWlmtA","VRWlmlA","VRZlmtA","VRZlmlA"]

        #region where the mass cut is not applied
        self.regionsWithoutMASSCutList = self.regionsWithoutDPHICutList

        #region where the met significance cut is not applied
        #self.regionsWithoutMETSIGCutList = self.regionsWithoutDPHICutList+self.regionWithMinimumMETCutsList
        self.regionsWithoutMETSIGCutList = self.regionsWithoutDPHICutList+self.regionForLooseCRList+ ["CRYlmtA","CRYlmlA","VRWlmtA","VRWlmlA","VRZlmtA","VRZlmlA"]

        # region where the Ap cut is not applied
        #self.regionsWithoutApCutList = self.regionsWithoutDPHICutList+["CRY","CRQ","VRQ1","VRQ2","VRQ3","VRQ4"]+self.regionForLooseCRList
        self.regionsWithoutApCutList = self.regionsWithoutDPHICutList+["CRY","CRQ","VRQ1","VRQ2","VRQ3","VRQ4"]

        #region with same cut as SR
        self.regionWithSRCutList = ["CRYtmtA","VRWtmtA"]

        #region with inverted Ap cut
        self.regionsWithInvertedApCutList = ["CRYtmlA","CRYlmlA","VRWtmlA","VRWlmlA","VRZtmlA","VRZlmlA"]
        #self.regionsWithInvertedApCutList = ["CRYtmlA","CRYlmlA","VRWtmlA","VRWlmlA","VRZtmlA","VRZlmlA"]+self.regionForLooseCRList

        #region with inverted meff cut
        self.regionsWithInvertedMeffCutList = ["CRYlmtA","CRYlmlA","VRWlmtA","VRWlmlA","VRZlmtA","VRZlmlA"]+self.regionForVeryLooseCRList+self.regionForLooseCRList
        #self.regionsWithInvertedMeffCutList = ["CRYlmtA","CRYlmlA","VRWlmtA","VRWlmlA","VRZlmtA","VRZlmlA"]+self.regionForVeryLooseCRList

        #region with inverted SRcut
        #self.regionsWithInvertedSRCutList = self.regionForLooseCRList
        self.regionsWithInvertedSRCutList = []


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
        if self.meffIncl >= 0 and not(self.WithoutMeffCut) and regionName not in self.regionsWithInvertedMeffCutList and regionName not in self.regionsWithInvertedSRCutList: 
            if regionName in self.regionsWithLooserMeffCuts:
                cutList.append(" meffInc >= %f " % self.meffInclLoose)
            else:
                cutList.append(" meffInc >= %f " % self.meffIncl)



        #effective mass cut upper cut              
        if self.meffInclUpperCut >= 0:
            cutList.append(" meffInc <= %f " % (self.meffInclUpperCut))
        
        # met cuts
        if self.MET > 0 and regionName not in self.regionsWithInvertedMETCutList and not(self.WithoutMetOverMeffCut):
            cutList.append("met >= %f" % self.MET)
        
        # met upper cuts
        if self.MET_upper > 0:
            cutList.append("met < %f" % self.MET_upper)
        
        # jet cuts
        #if not self.useFilteredNtuples:
        cutList.append("nJet >= %d" % self.nJets) # filtered nutples have correct nJets automatically

        if self.nJets > 0 and not(self.WithoutJetpT1Cut):
            cutList.append("jetPt[0] >= %f" % max(self.jetpt1, self.jetPtThreshold))
        if self.nJets > 1 and not(self.WithoutJetpT2Cut) and regionName not in self.regionForVeryLooseCRList:
            cutList.append("jetPt[1] >= %f" % max(self.jetpt2, self.jetPtThreshold))
        if self.nJets > 2 and not(self.WithoutJetpT3Cut) and regionName not in self.regionForVeryLooseCRList:
            cutList.append("jetPt[2] >= %f" % max(self.jetpt3, self.jetPtThreshold))
        if self.nJets > 3 and not(self.WithoutJetpT4Cut) and regionName not in self.regionForVeryLooseCRList:
            cutList.append("jetPt[3] >= %f" % max(self.jetpt4, self.jetPtThreshold))
        if self.nJets > 4:
            cutList.append("jetPt[4] >= %f" % max(self.jetpt5, self.jetPtThreshold))
        if self.nJets > 5:
            cutList.append("jetPt[5] >= %f" % max(self.jetpt6, self.jetPtThreshold))
        if self.nJets > 6:
            cutList.append("jetPt[6] >= %f" % max(self.jetpt7, self.jetPtThreshold))
        if self.nJets > 7:
            cutList.append("jetPt[7] >= %f" % max(self.jetpt8, self.jetPtThreshold))


        # fat jet mass cuts
        if regionName not in self.regionsWithoutMASSCutList:
            if  self.fatjet1MassMin >0:
                cutList.append("RTjetM[0] >= %f" % self.fatjet1MassMin)
            if  self.fatjet1MassMax >0:
                cutList.append("RTjetM[0] < %f" % self.fatjet1MassMax)
            if  self.fatjet2MassMin >0:
                cutList.append("RTjetM[1] >= %f" % self.fatjet2MassMin)
            if  self.fatjet2MassMax >0:
                cutList.append("RTjetM[1] < %f" % self.fatjet2MassMax)


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
                myString += " dPhi < %f" % (self.dPhiCRQ)
            elif regionName in self.regionsWithIntermediateDPHICutList:
                myString += "( dPhi > %f && dPhi < %f )" % (self.dPhiCRQ, self.dPhi)
            else:
                myString += " dPhi >= %f " % (self.dPhi)
                
            # add also the dphiR cut
            if self.dPhiR >= 0 and self.nJets >= 4:  
                if self.dPhiRCRQ < 0: 
                    self.dPhiRCRQ = self.dPhiR/2 # if dPhiRCRQ is not defined, take the half: 0.2==>0.1
                if regionName in self.regionsWithFullyInvertedDPHICutList+self.regionsWithIntermediateDPHICutList:                
                    myString += " || dPhiR < %f" % (self.dPhiRCRQ)
                else:
                    myString += " && dPhiR >= %f" % (self.dPhiR)
                                    
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

            varName = "met/sqrt(meffInc-met)"
            if regionName in self.regionsWithInvertedMETSIGCutList:
                cutList.append("%s >= %f && %s < %f" % (varName, self.METsigCRQ, varName, self.METsig)) 
            else:
                cutList.append("%s >= %f" % (varName, self.METsig)) 


        # Aplanary cut   
        if self.Ap>=0 and (regionName not in self.regionsWithoutApCutList) and (regionName not in self.regionsWithInvertedApCutList):
            cutList.append("Ap >= %f" % (self.Ap))

        # Aplanary upper cut   
        if regionName in self.regionsWithInvertedApCutList and self.Ap>=0 and (regionName not in self.regionsWithoutApCutList):
            cutList.append(" Ap < %f" % (self.Ap))

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

            varName="met/(met"
            for ijet in range(self.nJets):
                varName += " + jetPt[%d]" % ijet
            varName += ")"
            
            if regionName in self.regionsWithInvertedMETOVERMEFFCutList:
                #cutList.append(varName+">="+str(self.MET_over_meffNjCRQ)+" && "+varName+"<"+str(self.MET_over_meffNj))
                cutList.append("%s >= %f && %s < %f" % (varName, self.MET_over_meffNjCRQ, varName, self.MET_over_meffNj))
            else:
                if not(self.WithoutMetOverMeffCut):
                    #cutList.append(varName+">="+str(self.MET_over_meffNj)) 
                    cutList.append("%s >= %f " % (varName, self.MET_over_meffNj)) 
        
        #minimum MET cut
        minMETcut=200.
        if regionName in self.regionWithMinimumMETCutsList:
            minMETcut=200.
            if self.MET_over_meffNj > 0:
                minMETcut = max(self.meffIncl*self.MET_over_meffNj,minMETcut)
            elif self.METsig > 0:
                minMETcut = max(math.pow(self.METsig,2)*(-1.+math.sqrt(1+4.*self.meffIncl/math.pow(self.METsig,2)))/2.,minMETcut)
            cutList.append("met >= %f" % minMETcut)

        #inverted MET cut
        if regionName in self.regionsWithInvertedMETCutList:
            minMETcut=200.
            maxMETcut=self.MET
            if self.MET_over_meffNj > 0:
                maxMETcut = max(self.meffIncl*self.MET_over_meffNj, maxMETcut)
            elif self.METsig >0:
                maxMETcut = max(math.pow(self.METsig,2)*(-1.+math.sqrt(1+4.*self.meffIncl/math.pow(self.METsig,2)))/2., maxMETcut)
            cutList.append("met >= %f" % minMETcut)
            cutList.append(" met < %f " % maxMETcut)

        #effective mass inverted cut               
        if regionName in self.regionsWithInvertedMeffCutList:
            minMeffcut=700
            minMeffcut+=minMETcut
            maxMeffcut=self.meffIncl
            if regionName not in self.regionForVeryLooseCRList and regionName not in self.regionForLooseCRList:
            #if regionName not in self.regionForVeryLooseCRList:
                if self.nJets > 2 and not(self.WithoutJetpT3Cut):
                    minMeffcut+=max(self.jetpt3, self.jetPtThreshold)
                if self.nJets > 3 and not(self.WithoutJetpT4Cut):
                    minMeffcut+=max(self.jetpt4, self.jetPtThreshold)
                if self.nJets > 4:
                    minMeffcut+=max(self.jetpt5, self.jetPtThreshold)
                if self.nJets > 5:
                    minMeffcut+=max(self.jetpt6, self.jetPtThreshold)
                if self.nJets > 6:
                    minMeffcut+=max(self.jetpt7, self.jetPtThreshold)
                if self.nJets > 7:
                    minMeffcut+=max(self.jetpt8, self.jetPtThreshold)
            else :
                if self.nJets > 2:
                    minMeffcut+=self.jetPtThreshold
                if self.nJets > 3:
                    minMeffcut+=self.jetPtThreshold
                if self.nJets > 4:
                    minMeffcut+=self.jetPtThreshold
                if self.nJets > 5:
                    minMeffcut+=self.jetPtThreshold
                if self.nJets > 6:
                    minMeffcut+=self.jetPtThreshold
                if self.nJets > 7:
                    minMeffcut+=self.jetPtThreshold
            
            #this is temporary method   
            if minMeffcut >= maxMeffcut:
                minMeffcut=maxMeffcut-200.
            cutList.append(" meffInc >= %f " % minMeffcut) 
            if not(self.WithoutMeffCut):
                cutList.append(" meffInc < %f " % (self.meffIncl))

        #forSR Inverted CR
        if regionName in self.regionsWithInvertedSRCutList:
            cutforInvSR="("
            if self.Ap>=0:
                cutforInvSR+="Ap <"+str(self.Ap) +"||"
            """
            if self.MET_over_meffNj>0:
                varName="met/(met"
                for ijet in range(self.nJets):
                    varName += " + jetPt[%d]" % ijet
                varName += ")"
                cutforInvSR+=varName+"<"+str(self.MET_over_meffNj)+"||"
            if self.METsig >0:
                varName = "met/sqrt(meffInc-met)"
                cutforInvSR+=varName+"<"+str(self.METsig)+"||"
            """
            if self.meffIncl >0:
                cutforInvSR+="meffInc"+"<"+str(self.meffIncl)+")"
            cutList.append(cutforInvSR)
    
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
        print "Regions without Aplanarity cut     : ", self.regionsWithoutApCutList
        print "Regions with inverted dphi cut     : ", self.regionsWithFullyInvertedDPHICutList
        print "Regions with intermediate dphi cut : ", self.regionsWithIntermediateDPHICutList
        print "Regions with inverted metsig cut   : ", self.regionsWithInvertedMETSIGCutList
        print "Regions with inverted met/meff cut : ", self.regionsWithInvertedMETOVERMEFFCutList
        print "Regions with inverted aplanaritycut: ", self.regionsWithInvertedApCutList
        print "Regions with inverted met cut      : ", self.regionsWithInvertedMETCutList
        print "Regions with inverted meff cut     : ", self.regionsWithInvertedMeffCutList
        print "Regions with minimum met cut       : ", self.regionWithMinimumMETCutsList
     
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
        
        if printLevel > 0:

            print "=================================================="
            for regionName, region in self.regionDict.items():
                print region
                if printLevel > 1:  
                    print "Additional debugging info for %s:" % regionName
                    print "\t Suffix for tree name: %s" % self.getSuffixTreeName(regionName)
                    print "\t Cuts: %s " % (self.getCuts(regionName))
                    #print "\t Weights: %s " % (self.getWeights(regionName))

                print "=================================================="


#CRT (nBJet>0)
#CRW (nBJet==0)
#CRY (phQuality == 2 && phIso < 5000.) && (nLep == 0)
#CRQ
