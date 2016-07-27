



#################################################
# Channel configuration
#################################################

from collections import OrderedDict
from copy import deepcopy
import os
import sys
import ROOT
import copy
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

lastcuts = {
    'SRG': "HT5PP",
    'SRS': "HT3PP",
    'SRC': "PTISR"
}

ratiocuts = {
    'SRG': "R_H2PP_H5PP",
    'SRS': "R_H2PP_H3PP",
    'SRC': "RISR"
}

########################################################
#
########################################################
class ChannelConfig:
    def __init__(self, **kwargs):
        self.setCommonVars()

        print kwargs
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
        self.dphiMin2CRQ = -1.0
        self.dPhiRCRQ = -1.0
        self.dPhi = -1.0
        self.dphiMin2 = -1.0
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

        self.MDR                     = None #-1
        self.deltaQCD                = None #-999
        self.deltaQCD_loose          = None #-999
        self.H2PP                    = None #-1
        self.H2PP_loose              = None #-1

        #Squark Variables
        self.RPT_HT3PP_upper         = None #+999
        self.RPT_HT3PP_upper_loose   = None #+999

        self.R_H2PP_H3PP             = None #-1
        self.R_H2PP_H3PP_loose       = None #-1
        self.R_H2PP_H3PP_upper       = None #+999
        self.R_H2PP_H3PP_upper_loose = None #+999

        self.RPZ_HT3PP_upper         = None #+999
        self.RPZ_HT3PP_upper_loose   = None #+999

        self.R_pTj2_HT3PP            = None #-1
        self.cosP_upper              = None #+999
        self.HT3PP                   = None #-1
        self.R_pTj2_HT3PP_loose      = None #-1
        self.cosP_upper_loose        = None #+999
        self.HT3PP_loose             = None #-1

        #Gluino Variables
        self.RPT_HT5PP_upper         = None #+999
        self.R_H2PP_H5PP             = None #-1
        self.R_HT5PP_H5PP            = None #-1
        self.RPZ_HT5PP_upper         = None #+999
        self.minR_pTj2i_HT3PPi       = None #-1
        self.maxR_H1PPi_H2PPi_upper  = None #+999
        self.dangle_upper            = None #+999
        self.HT5PP                   = None #-1

        self.RPT_HT5PP_upper_loose        = None #+999
        self.R_H2PP_H5PP_loose            = None #-1
        self.R_HT5PP_H5PP_loose           = None #-1
        self.RPZ_HT5PP_upper_loose        = None #+999
        self.minR_pTj2i_HT3PPi_loose      = None #-1
        self.maxR_H1PPi_H2PPi_upper_loose = None #+999
        self.dangle_upper_loose           = None #+999
        self.HT5PP_loose                  = None #-1

        #Compressed Variables
        self.RISR                    = None #0
        self.MS                      = None #0
        self.dphiISRI                = None #0
        self.PTISR                   = None #0
        self.NV                      = None #0

        self.RISR_loose              = None #0
        self.RISR_range              = None
        self.RISR_qcdlooseAndInverted  = None #0
        self.MS_loose                = None #0
        self.dphiISRI_loose          = None #0
        self.PTISR_loose             = None #0
        self.NV_loose                = None #0

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
        self.regionsWithoutDPHICutList = ["CRWT","CRW","CRT","CRZ","VRZ","VRWTplus","VRWTminus","VRWM","VRTM","VRWTplus","VRWTminus","VRT2L"]

        #region where the met/meff cut is not applied
        self.regionsWithoutMETOVERMEFFCutList = self.regionsWithoutDPHICutList

        #region where the met significance cut is not applied
        self.regionsWithoutMETSIGCutList = self.regionsWithoutDPHICutList

        # region where the Ap cut is not applied
        self.regionsWithoutApCutList = self.regionsWithoutDPHICutList+["CRY","CRQ","VRQ1","VRQ2","VRQ3","VRQ4"]


        ##################################################
        ## LL RJigsaw

        self.regionsWithInvertedDangleCutList = ["VRTZL","CRQ","VRQ","VRQ2"]
        self.regionsWithInvertedRPZCutList = ["VRTZL"]
        # self.regionsWithInvertedDangleCutList = ["CRT"]
        # self.regionsWithInvertedRPZCutList = ["CRT"]





        self.CRList = ["CRT","CRW","CRY","CRQ"]
        VRList      = ["VRWa", "VRWb","VRTa","VRTb","VRZa","VRZb" ] #, "VRTZL"
        VRList      += [ "VRQ", "VRQa" , "VRQb" , "VRQc", "VRZ", "VRW", "VRT", "VRZc", "VRZca"]
        self.regionListDict =  dict([ (l, {} ) for l in self.CRList + VRList + ["SR"] ])


        #any var that can be loose
        for k,v in self.regionListDict.iteritems() :
            for varName in dir(self) :
                if ('_loose' in varName) : v[varName.replace('_loose','')] = ""

        for k,v in self.regionListDict.iteritems() :
            #loosen the VR*a and the CRs
            if k.endswith('a') or k in self.CRList :
                   v["H2PP" ] = "loosen"
        for k,v in self.regionListDict.iteritems() :
            #loosen the VR*b and the CRs
               if k.endswith('b') or k in self.CRList:
                   v["HT3PP"] = "loosen"
                   v["HT5PP"] = "loosen"
        for k,v in self.regionListDict.iteritems():
            #check if this is a compresed CRY
            isNotCompressedRegionCRY = not ('SRJigsawSRC' in self.name and 'CRY' in k)
            for varName in dir(self) :
                    if varName not in ['H2PP', 'HT3PP', 'HT5PP' ,
                                       'H2PP_loose', 'HT3PP_loose', 'HT5PP_loose'
                                       ] :
                        if isNotCompressedRegionCRY or varName not in [ 'RISR','dphiISRI','NV',
                                                                        'RISR_loose','dphiISRI_loose','NV_loose',
                                                                        ] :
                            if '_loose' in  varName and (k in self.CRList or k.endswith('a') or k.endswith('b')) :
                                v[varName.replace('_loose', '') ] = "loosen"

        #let's treat these a bit special.
        #this is getting a bit out of hand
        self.regionListDict["CRQ"] ["RISR"]        =  "qcd_invertAndLoosen"
        self.regionListDict["VRQc"]["RISR"]        =  "qcd_range"

        self.regionListDict["CRQ"]["H2PP"] =  "invert"
        self.regionListDict["CRQ"]["deltaQCD"] = "invert"

        self.regionListDict["VRQa"]["deltaQCD"] = "invert"

        self.regionListDict["VRQb"]["H2PP"] =  "invert"
        self.regionListDict["VRZc"] ["dphiISRI"] =  "invert"
        self.regionListDict["VRZca"]["dphiISRI"] =  "invertAndLoosen"


        self.WithoutLastCut = False
        self.WithoutRatioCut = False

        # Hope to avoid these as much as possible
#        self.WithoutMeffCut = False
#        self.WithoutMetOverMeffCut = False
#        self.WithoutdPhiCut = False
#        self.WithoutApCut = False
#        self.WithoutJetpT1Cut = False
#        self.WithoutJetpT2Cut = False
#        self.WithoutJetpT3Cut = False
#        self.WithoutJetpT4Cut = False

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

        if self.doCleaning:
            self.cleaningCuts = "((cleaning&0x30F)==0)"
            cutList.append(self.cleaningCuts)

        '''
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

        if self.dphiMin2>=0 and regionName not in self.regionsWithoutDPHICutList:
            myString="("

            #first the dphi cut
            if self.dphiMin2CRQ<0: self.dphiMin2CRQ=self.dphiMin2/2 # if PhiCRQ is not defined, take the half: 0.4==>0.2
            if regionName in self.regionsWithFullyInvertedDPHICutList:
                myString += " dphiMin2 < %f" % (self.dphiMin2CRQ)
            elif regionName in self.regionsWithIntermediateDPHICutList:
                myString += "( dphiMin2 > %f && dphiMin2 < %f )" % (self.dphiMin2CRQ, self.dphiMin2)
            else:
                myString += " dphiMin2 >= %f " % (self.dphiMin2)



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

        '''

        ###############################################################################
        ###############################################################################
        ###############################################################################

        # LL RJigsaw
        passDict = self.regionListDict

        self.addCutsToCutList( cutList, passDict , regionName )

        #extra cuts from CR
        cutList += self.regionDict[regionName].extraCutList

        cutStr = " && ".join(cutList)
        return "(%s)" % cutStr

    def addCutsToCutList( self, cutList , regionDict, regionName = None ) :
        if not regionName :
            print "NO REGION NAME, exiting"
            sys.exit(1)

        for reg, idict in regionDict.iteritems() :
            if regionName == reg :
                for var,val in idict.iteritems() :
                    finalCutString = ""
                    stringVarValue = str(getattr(self, var)) if getattr(self, var)!=None else None
                    #print "current var:", var, stringVarValue, val
                    if stringVarValue != None :#can be zero, so use this
#                        if "minusone" in  var:
#                           print "omit var cut", var
#                           continue
                        if val == 'qcd_range' :
                            neededRange = getattr(self, var + "_range") if getattr(self, var+"_range")!=None else None
                            if not neededRange : print reg,var,val, var+"_range"
                            finalCutString = "(" + var + " >= "+ str( neededRange[0]) + ")" + "*" + "(" +  var + " <= " +str( neededRange[1]) + ")"
                        elif val == 'qcd_invertAndLoosen' :
                             cutValue = getattr(self, var + "_looseAndInverted") if getattr(self, var+"_looseAndInverted")!=None else None
                             if not cutValue : print reg,var,val, var+"_looseAndInverted"
                             finalCutString = str( var  + " < " + str(cutValue))
                        else :
                             if "dangle_upper" in var :
                                 removeUpper = var.replace("upper","").strip("_")
                                 if not val         : finalCutString = "abs(dangle) <= "  + stringVarValue
                             elif "upper" in var :
                                 removeUpper = var.replace("upper","").strip("_")
                                 if not val         : finalCutString = removeUpper + " <= "  + stringVarValue
                                 if val == 'invert' : finalCutString = removeUpper + " >  "  + stringVarValue
                                 if val == 'loosen' :
                                     loosenedStringVarValue = str(getattr(self, var + "_loose")) if getattr(self, var+"_loose")!=None else None
                                     if not loosenedStringVarValue : print reg,var,val
                                     finalCutString                  = removeUpper + " <=  " + loosenedStringVarValue
                             else  :
                                 if not val         : finalCutString = var         + " >= " + stringVarValue
                                 if val == 'invert' : finalCutString = var         + " <  " + stringVarValue
                                 if val == 'tightendphiMin2': finalCutString = var         + " >= 0.4 "
                                 if val == 'loosen' :
                                     loosenedStringVarValue = str(getattr(self, var + "_loose")) if getattr(self, var+"_loose")!=None else None
                                     if not loosenedStringVarValue : print reg,var,val, var+"_loose"
                                     finalCutString                  = var         + " >=  " + loosenedStringVarValue
                                 if val == "invertAndLoosen":
                                     loosenedStringVarValue = str(getattr(self, var + "_loose")) if getattr(self, var+"_loose")!=None else None
                                     finalCutString                  = var         + " <  " + loosenedStringVarValue

                    if finalCutString:
                        cutList.append(finalCutString)

                            #print finalCutString
                            #print regionName, "cutlist", cutList

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
