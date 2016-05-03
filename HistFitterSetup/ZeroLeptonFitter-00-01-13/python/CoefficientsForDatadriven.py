#######################################
# The Coeffients in this file are the 
# Coefficiens for  the datadriven BG estimation
#######################################
####################################################
#
####################################################
class ChannelCoefficients:
    def __init__(self, Channel, isABCD):
        self.CoefficientDict =  self.setChannelCoefficients(Channel, isABCD)
    def getCoefficient(self,regionName):
        for coefficient in self.CoefficientDict:
            if regionName == coefficient.regionName:
                return coefficient
            else:
                continue
    def getCoefficientsDict(self):
        return self.CoefficientDict
    def Print(self):
        print "=================================================="
        for name,coeff in self.CoefficientDict.items():
            print coeff
#            coeff.Print()
        print "=================================================="
    def setChannelCoefficients(self, Channel, isABCD):
        CoefficientDict={}
        if Channel=="SR2jt":
            if not isABCD:
                coeff = Coefficient(Channel, "CRYtmtA", isABCD, 1., 0., 200.)
                CoefficientDict[coeff.name]=coeff
                coeff = Coefficient(Channel, "CRYlmlA", isABCD, 1., 0., 200.)
                CoefficientDict[coeff.name]=coeff
                coeff = Coefficient(Channel, "CRWL", isABCD, 1., 0., 200.)
                CoefficientDict[coeff.name]=coeff
                coeff = Coefficient(Channel, "CRZllVL", isABCD, 1., 0., 200.)
            else:
                coeff = Coefficient(Channel, "CRYtmtA", isABCD, 1., 0., 200.)
                CoefficientDict[coeff.name]=coeff
                coeff = Coefficient(Channel, "CRYtmlA", isABCD, 1., 0., 200.)
                CoefficientDict[coeff.name]=coeff
                coeff = Coefficient(Channel, "CRYlmtA", isABCD, 1., 0., 200.)
                CoefficientDict[coeff.name]=coeff
                coeff = Coefficient(Channel, "CRYlmlA", isABCD, 1., 0., 200.)
                CoefficientDict[coeff.name]=coeff
                coeff = Coefficient(Channel, "CRWL", isABCD, 1., 0., 200.)
                CoefficientDict[coeff.name]=coeff
                coeff = Coefficient(Channel, "CRZllVL", isABCD, 1., 0., 200.)
        elif Channel=="SR4jt":
            coeff = Coefficient(Channel, "CRYtmtA", isABCD, 1.55, 0., 2.*1.55)
            CoefficientDict[coeff.name]=coeff
            coeff = Coefficient(Channel, "CRWL", isABCD, 0.51, 0., 2.*0.51)
            CoefficientDict[coeff.name]=coeff
            coeff = Coefficient(Channel, "CRYL", isABCD, 2.8, 0., 2.*2.8)
            CoefficientDict[coeff.name]=coeff
            coeff = Coefficient(Channel, "CRZllVL", isABCD, 312., 0., 2.*312.)
            CoefficientDict[coeff.name]=coeff
            coeff = Coefficient(Channel, "SF_nunuperll", isABCD, 6.92, 6.92-0.23, 6.92 +0.23)
            CoefficientDict[coeff.name]=coeff
            coeff = Coefficient(Channel, "SF_llpernunu", isABCD, 0.1443, 0.1443-0.005, 0.1443 +0.005)
            CoefficientDict[coeff.name]=coeff
            coeff = Coefficient(Channel, "R_YperZ", isABCD, 0.87, 0.87-0.13, 0.87+0.13)
            CoefficientDict[coeff.name]=coeff
            coeff = Coefficient(Channel, "R_ZperW", isABCD, 1.04,  1.04-0.06, 1.04 +0.06)
            CoefficientDict[coeff.name]=coeff
            if not isABCD:
                coeff = Coefficient(Channel, "CRYlmlA", isABCD, 12.04, 0., 2*12.04)
                CoefficientDict[coeff.name]=coeff
            else:
                coeff = Coefficient(Channel, "CRYtmlA", isABCD, 1.543, 0.,  2.*1.543)
                CoefficientDict[coeff.name]=coeff
                coeff = Coefficient(Channel, "CRYlmtA", isABCD, 25., 0., 2*25.)
                CoefficientDict[coeff.name]=coeff
        return CoefficientDict
       

####################################################
#
####################################################
class Coefficient:
    def __init__(self,Channel, regionName, isABCD, val, minval, maxval):
        self.channel = Channel
        self.name = regionName
        self.IsABCD = isABCD
        self.Value  = val
        self.Minval = minval
        self.Maxval = maxval
        return
    def __str__(self):
        retval = ("Channel      : %s\n"
                  "Region       : %s\n"
                  "IsABCD       : %s\n"
                  "Value        : %s\n"
                  "Minval       : %s\n"
                  "Maxval       : %s") % (self.channel, self.name, self.IsABCD, self.Value, self.Minval, self.Maxval)
        return retval    
    def Print(self):

        print "Channel  : %s" % self.channel
        print "Region   : %s" % self.name
        print "IsABCD   : %s" % self.IsABCD
        print "Value    : %s" % self.Value
        print "Minval   : %s" % self.Minval
        print "Maxval   : %s" % self.Maxval
