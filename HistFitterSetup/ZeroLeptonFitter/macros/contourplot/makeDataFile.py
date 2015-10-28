#!/usr/bin/env python

import os
import sys
import subprocess
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from optparse import OptionParser
from summary_harvest_tree_description import treedescription

def parseCmdLine(args):
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", help="path to input file", type='str')
    parser.add_option("-e", "--expected", help="use expectedUpperLimit and not upperLimit", action="store_true", default=False)
    parser.add_option("-s", "--seperate", help="show UL and xsec, rather than UL*xsec", action="store_true", default=False)
    parser.add_option("-H", "--hepdata", help="dump ULs in hepdata format", action="store_true", default=False)

    (options, args) = parser.parse_args(args)

    if not options.filename:
        parser.error('filename not given')

    if options.seperate and options.hepdata:
        parser.error('cannot use --seperate and --hepdata simultaneously')

    return options

def GetSRName(SR):

    names = {1 : "2jm", 2 : "2jt", 3 : "2jW", 4 : "2jl", 5 : "3j", 6: "4jl", 7: "4jW", 8: "4jm", 9: "4jt", 10: "4jl-", 11 : "5j", 12: "6jm", 13: "6jt", 14: "6jt+", 15 : "5jl" }
    if not SR in names:
        return ""

    return names[SR]

def makeHepDataHeader(filename):
    # NOTE: DO NOT HACK THE GENERIC HEADER, MAKE IF-STATEMENTS BASED ON THE GRID

    string = """*dataset:
*location: Figure GIVE FIGURE NUMBER
*dscomment: COMMENT HERE
*reackey: P P --> GIVE THE PRODUCTION PROCESSES
*obskey: GIVE KEY FOR Y-AXIS VARIABLE
*qual: RE : P P --> GIVE THE PRODUCTION PROCESSES + DECAYS (IF RELEVANT)
*qual: SQRT(S) IN GEV : 8000.0
*yheader: 2D graph z axis
*xheader: 2D graph x axis : 2D graph y axis
*data: x : x : y : y"""

    if "SS" in filename and "direct" in filename:
        string = """
*dataset:
*location: Figure GIVE FIGURE NUMBER
*dscomment: Observed 95% CL cross-section upper limit for pair-produced squarks decaying directly
*reackey: P P --> SQUARK SQUARK
*obskey: NEUTRALINO1 MASS
*qual: RE : P P --> SQUARK < QUARK NEUTRALINO1 > SQUARK < QUARK NEUTRALINO1 >
*qual: SQRT(S) IN GEV : 8000.0
*yheader: Cross-section limit in FB : noZ SRs
*xheader: SQUARK MASS IN GEV : NEUTRALINO1 MASS IN GEV
*data: x : x : y : y"""

    elif "SG" in filename and "direct" in filename:
        string = """
*dataset:
*location: Figure GIVE FIGURE NUMBER
*dscomment: Observed 95% CL cross-section upper limit for associated gluino-squark production 
*reackey: P P --> SQUARK GLUINO
*obskey: NEUTRALINO1 MASS
*qual: RE : P P --> SQUARK < QUARK NEUTRALINO1 > GLUINO < QUARK QUARK NEUTRALINO1 >
*qual: SQRT(S) IN GEV : 8000.0
*yheader: Cross-section limit in FB : noZ SRs
*xheader: GLUINO MASS IN GEV : NEUTRALINO1 MASS IN GEV
*data: x : x : y : y"""
        return string

    elif "GG" in filename and "direct" in filename:
        string = """
*dataset:
*location: Figure GIVE FIGURE NUMBER
*dscomment: Observed 95% CL cross-section upper limit for pair-produced gluinos decaying directly
*reackey: P P --> GLUINO GLUINO
*obskey: NEUTRALINO1 MASS
*qual: RE : P P --> GLUINO < QUARK QUARK NEUTRALINO1 > GLUINO < QUARK QUARK NEUTRALINO1 >
*qual: SQRT(S) IN GEV : 8000.0
*yheader: Cross-section limit in FB : noZ SRs
*xheader: GLUINO MASS IN GEV : NEUTRALINO1 MASS IN GEV
*data: x : x : y : y"""
        return string
    elif "Gluino_Stop_charm" in filename:
        string = """
*dataset:
*location: Figure GIVE FIGURE NUMBER
*dscomment: Observed 95% CL cross-section upper limit for pair-produced gluinos decaying via stops into top+charm+neutralino1
*reackey: P P --> GLUINO GLUINO
*obskey: STOP MASS
*qual: RE : P P --> GLUINO < TOP CHARM NEUTRALINO1 > GLUINO < TOP CHARM NEUTRALINO1 >
*qual: SQRT(S) IN GEV : 8000.0
*yheader: Cross-section limit in FB : noZ SRs
*xheader: GLUINO MASS IN GEV : STOP MASS IN GEV
*data: x : x : y : y"""

        return string

    return string

def main():
    options = parseCmdLine(sys.argv)
    
    dummy,description = treedescription()
    allpar = description.split(':')

    if options.filename.find("Moriond13") != -1:
        # from HistFitter v24 source code
        description = "p0:p1:CLs:"
        description += "mode:nexp:"
        description += "seed:"
        description += "CLsexp:"
        description += "fID:sigma0:sigma1:"
        description += "clsu1s:clsd1s:clsu2s:clsd2s:"
        description += "upperLimit:upperLimitEstimatedError:expectedUpperLimit:expectedUpperLimitPlus1Sig:expectedUpperLimitPlus2Sig:expectedUpperLimitMinus1Sig:expectedUpperLimitMinus2Sig:xsec:excludedXsec:"
        description += "m0:m12"

        allpar = description.split(':')

    xsecIdx = allpar.index('xsec')
    ULIdx   = allpar.index('upperLimit')
    if options.expected:
        ULIdx   = allpar.index('expectedUpperLimit')
    
    if not "pMSSM" in options.filename: 
        m0Idx   = allpar.index('m0')
        m12Idx  = allpar.index('m12')
    else:
        m0Idx   = allpar.index('M1')
        m12Idx  = allpar.index('M2')
    
    fIdIdx  = allpar.index('fID')
   
    p0Idx = allpar.index('p0')
    p1Idx = allpar.index('p1')
    CLsIdx = allpar.index('CLs')
    CLsexpIdx = allpar.index('CLsexp')

    covqualIdx = allpar.index('covqual')
    dodgycovIdx = allpar.index('dodgycov')
    failedcovIdx = allpar.index('failedcov')
    failedfitIdx = allpar.index('failedfit')
    failedp0Idx = allpar.index('failedp0')
    failedstatusIdx = allpar.index('failedstatus')
    fitstatusIdx = allpar.index('fitstatus')    

    f = open(options.filename, "r")

    data = {}
    CLsdata = {}
    for l in f.readlines():
        vals = l.strip().split(' ')
        key = "%d_%d" % (int(float(vals[m0Idx])), int(float(vals[m12Idx])))
        data[key] = [float(vals[ULIdx]), float(vals[xsecIdx]), int(vals[fIdIdx])]
        CLsdata[key] = [float(vals[p0Idx]), float(vals[p1Idx]), float(vals[CLsIdx]), float(vals[CLsexpIdx])]

    if options.seperate:
        print "# x\ty\tUL\txsec\tSR\tCLs"
    elif options.hepdata:
        print makeHepDataHeader(options.filename)
    else:
        print "# x\ty\tUL*xsec\tSR"
    
    for key in sorted(data.iterkeys(), key=lambda a:map(int,a.split('_'))):
        (x, y) = key.split("_")
        x = int(x)
        y = int(y)

        ## HACK to filter e.g. rectangle (easier to isolate crashed points)
        #if not (x > 200 and x < 300): continue
        #if not (y > 100 and y < 200): continue

        #if not y == 0: continue

        if options.seperate:
            print "%d\t%d\t%f\t%f\t%d\t%e\t%e (exp)" % (x, y, data[key][0], data[key][1], data[key][2], CLsdata[key][2], CLsdata[key][3])
        elif options.hepdata:
            UL = data[key][0] * data[key][1]
            SR = GetSRName(data[key][2])
            print "%d; %d; %e; %s" % (x, y, UL, SR)
        else:
            print "%d\t%d\t%f\t%d" % (x, y, data[key][0] * data[key][1], data[key][2])

        covqual = int(float(vals[covqualIdx]))
        dodgycov = int(float(vals[dodgycovIdx]))
        failedcov = int(float(vals[failedcovIdx]))
        failedfit = int(float(vals[failedfitIdx]))
        failedp0 = int(float(vals[failedp0Idx]))
        failedstatus = int(float(vals[failedstatusIdx]))
        fitstatus = int(float(vals[fitstatusIdx]))

        # verbose print line to see what's going on with a point
        #print "\t ==> covqual = %d, dodgycov = %d, failedcov = %d, failedfit = %d, failedp0 = %d, failedstatus = %d, fitstatus = %d" % (covqual, dodgycov, failedcov, failedfit, failedp0, failedstatus, fitstatus)

    return

if __name__ == '__main__':
    del os.environ['TERM']
    main()
