#!/usr/bin/env python

import sys
import subprocess
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from optparse import OptionParser
from summary_harvest_tree_description import treedescription

def parseCmdLine(args):
    parser = OptionParser()
    parser.add_option("-g", "--grid", type="str")
    parser.add_option("-p", "--point", help="point to print", type="str")
    parser.add_option("-e", "--expected", help="use expectedUpperLimit and not upperLimit", action="store_true", default=False)
    parser.add_option("-s", "--seperate", help="show UL and xsec, rather than UL*xsec", action="store_true", default=False)

    (options, args) = parser.parse_args(args)

    if not options.grid:
        parser.error('grid not given')
    
    if not options.point:
        parser.error('point not given')

    return options

def main():
    options = parseCmdLine(sys.argv)
    
    dummy,description = treedescription()
    allpar = description.split(':')

    xsecIdx = allpar.index('xsec')
    ULIdx   = allpar.index('upperLimit')
    if options.expected:
        ULIdx   = allpar.index('expectedUpperLimit')
    m0Idx   = allpar.index('m0')
    m12Idx  = allpar.index('m12')
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

    #f = open(options.filename, "r")
    
    # get files to read 
    f = open("Outputs/%s_combined_fixSigXSecNominal__1_harvest_list_infoFile" % options.grid, "r")
    filenames = {}
    for l in f.readlines():
        (N, fname) = l.strip().split(":")
        filenames[int(N.strip())] = "Outputs/%s_%s_fixSigXSecNominal__1_harvest_list" % (options.grid, fname.strip())
    f.close()

    data = {}
    CLsdata = {}
    for N in filenames:
        f = open(filenames[N])
        for l in f.readlines():
            vals = l.strip().split(' ')
            key = "%d_%d" % (int(float(vals[m0Idx])), int(float(vals[m12Idx])))
            if key != options.point:
                continue
            
            data[N] = [float(vals[ULIdx]), float(vals[xsecIdx]), N]
            CLsdata[N] = [float(vals[p0Idx]), float(vals[p1Idx]), float(vals[CLsIdx]), float(vals[CLsexpIdx])]

        f.close()

    if options.seperate:
        print "# x\ty\tUL\txsec\tSR\tCLs"
    else:
        print "# x\ty\tUL*xsec\tSR"
    
    for N in sorted(data):
        (x, y) = options.point.split("_")
        x = int(x)
        y = int(y)

        if options.seperate:
            print "%d\t%d\t%f\t%f\t%d\t%.2f\t%.2f (exp)" % (x, y, data[N][0], data[N][1], data[N][2], CLsdata[N][2], CLsdata[N][3])
        else:
            print "%d\t%d\t%f\t%d" % (x, y, data[N][0] * data[N][1], data[N][2])

        covqual = int(float(vals[covqualIdx]))
        dodgycov = int(float(vals[dodgycovIdx]))
        failedcov = int(float(vals[failedcovIdx]))
        failedfit = int(float(vals[failedfitIdx]))
        failedp0 = int(float(vals[failedp0Idx]))
        failedstatus = int(float(vals[failedstatusIdx]))
        fitstatus = int(float(vals[fitstatusIdx]))

        # verbose print line to see what's going on with a point
        print "\t ==> covqual = %d, dodgycov = %d, failedcov = %d, failedfit = %d, failedp0 = %d, failedstatus = %d, fitstatus = %d" % (covqual, dodgycov, failedcov, failedfit, failedp0, failedstatus, fitstatus)

    return

if __name__ == '__main__':
    main()
