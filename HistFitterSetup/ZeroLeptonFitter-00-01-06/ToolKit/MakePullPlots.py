#!/usr/bin/env python

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.Reset()
ROOT.gROOT.SetBatch(True)
ROOT.gSystem.Load("libSusyFitter.so")
from math import *

from optparse import OptionParser
import sys, os, string, shutil, pickle, subprocess, copy
from YieldsTable import latexfitresults

from ChannelsDict import *
from ZLFitterConfig import *

import pullPlotUtils
from pullPlotUtils import makePullPlot

###################################################
# config file
###################################################

showErrorBeforeFits = True

###################################################
#
###################################################
def makeRegionsArray(regionsStr):
    regions = regionsStr.split(",")
    for i, r in enumerate(regions):
        regions[i] = r.replace("_cuts", "").replace("_meffInc", "")

    return regions

###################################################
#
###################################################
def makeCaption(shortname, regionsStr):
    regions = makeRegionsArray(regionsStr)

    tableCaption = "{\\bf %s} : Background fit results for the %s and %s regions, for an integrated luminosity of \ourintlumi~\ifb. Nominal MC expectations (normalised to MC cross-sections) are given for comparison. The errors shown are the statistical plus systematic uncertainties. The errors shown for the signal region are systematic uncertainties only." % (shortname, ", ".join(regions[:-1]), regions[-1])

    return tableCaption

###################################################
#
###################################################
def makeLabel(shortname, regionsStr):
    regions = makeRegionsArray(regionsStr)
    tableLabel = "table.results.systematics.in.logL.fit.%s.%s" % ( ".".join(regions), shortname )

    return tableLabel

###################################################
#
###################################################
def renameRegions(useChargeAsymmetry, useVRWTM):
    #rename regions if needed
    myRegionDict = {}
    if useChargeAsymmetry:
        myRegionDict["VRWTPlus"] = "CRWT+"
        myRegionDict["VRWTMinus"] = "CRWT-"
        myRegionDict["CRT"] = "VRT"
        myRegionDict["CRW"] = "VRW"
    elif useVRWTM:
        myRegionDict["VRWM"] = "CRWM"
        myRegionDict["VRTM"] = "CRTM"
        myRegionDict["CRT"] = "VRT"
        myRegionDict["CRW"] = "VRW"
    else:
        myRegionDict["VRWTPlus"] = "VRWT+"
        myRegionDict["VRWTMinus"] = "VRWT-"
        myRegionDict["VRWTPlusf"] = "VRWTf+"
        myRegionDict["VRWTMinusf"] = "VRWTf-"

    return myRegionDict

###################################################
#
###################################################
def getRegionColor(name):
    if name.find("VRWTau") != -1: return ROOT.kRed
    if name.find("VRttbarTau") != -1: return ROOT.kRed
    if name.find("VRWT") != -1: return ROOT.kYellow
    if name.find("VRZ") != -1:  return ROOT.kBlue+3
    if name.find("VRW") != -1:  return ROOT.kAzure-4
    if name.find("VRT") != -1:  return ROOT.kGreen-9
    if name.find("VRQ") != -1:  return ROOT.kOrange
    if name.find("CRW") != -1:  return ROOT.kAzure-4
    if name.find("CRT") != -1:  return ROOT.kGreen-9
    if name.find("SR") != -1:   return ROOT.kBlack
    if name.find("BVR") != -1:  return ROOT.kRed+2
    return 1

###################################################
#
###################################################
def makeYieldTables(anaconv, filename, regionList, samples, renamedRegions, useShapeFit=False, doVR=False, doBlind=True,doPrintOnly=False):
    suffix="_cuts"
    if useShapeFit: suffix="_meffInc"

    regionsForTables = ""
    regionsForTablesAll = ""
    for region in regionList:
        region2 = region

        if region2 in renamedRegions.keys():
            region2 = renamedRegions[region2]

        regionsForTablesAll += region+suffix+","
        if region2.find("SR") >= 0 or region2.find("CR") >= 0 or region2=="VRZ": #" or region2=="VRWM":
            regionsForTables += region+suffix+","

    #remove last comma
    if regionsForTablesAll[-1]==",":
        regionsForTablesAll=regionsForTablesAll[:-1]

    if regionsForTables[-1]==",":
        regionsForTables=regionsForTables[:-1]

    cmd = "YieldsTable.py "
    if doBlind:
        cmd += "-B "
    if showErrorBeforeFits:
        cmd += "-b "
    cmd += "-c %s -s %s -w %s -C \"%s\" -L \"%s\" -o plots/yield_%s.tex -t %s" % (regionsForTables, samples, filename, makeCaption(anaconv, regionsForTables), makeLabel(anaconv, regionsForTables), anaconv, anaconv)
    print cmd
    if not doPrintOnly:subprocess.call(cmd, shell=True)

    # make plots for subset of VRs if doVR==True
    if doVR and len(regionsForTablesAll.split(',')) - len(regionsForTables.split(',')) > 6:
        nVRs = len(regionsForTablesAll.split(',')) - len(regionsForTables.split(','))
        for i in range(nVRs/6):
            theRegions=copy.deepcopy(regionsForTables)
            j = 0
            for region in regionsForTablesAll.split(','):
                if 'CR' in region or 'SR' in region: continue
                if j < i * 6 or j >= (i + 1) * 6:
                    j += 1
                    continue
                theRegions += ','+region
                j += 1
            cmd = "YieldsTable.py "
            if doBlind:
                cmd += "-B "
            if showErrorBeforeFits:
                cmd += "-b "
            cmd += "-c %s -s %s -w %s -C \"%s\" -L \"%s\" -o plots/yield_%s_all%d.tex -t %s" % (theRegions, samples, filename, makeCaption(anaconv, theRegions), makeLabel(anaconv, theRegions), anaconv, i+1, anaconv)
            print i,nVRs,nVRs/8,cmd
            if  not doPrintOnly: subprocess.call(cmd, shell=True)

    # make combined table with all VRs and all CRs (note: we always need this for the pickle not  not )
    cmd = "YieldsTable.py "
    if doBlind:
        cmd += "-B "
    if showErrorBeforeFits:
        cmd += "-b "
    cmd += "-c %s -s %s -w %s -C \"%s\" -L \"%s\" -o plots/yield_%s_all.tex -t %sall" % (regionsForTablesAll, samples, filename, makeCaption(anaconv, regionsForTablesAll), makeLabel(anaconv, regionsForTablesAll), anaconv, anaconv)
    print cmd
    if  not doPrintOnly:subprocess.call(cmd, shell=True)

    return

###################################################
#
###################################################
def makeSystematicsTables(anaconv, filename, useShapeFit=False,doPrintOnly=False):
    region = "SR_cuts"
    if useShapeFit:
        region = "SR_meffInc"

    #cmd = "BkgSysTable.py -a True -w %s -c %s -o systtable_%s.tex -t %s" % (filename, region, anaconv, anaconv)

    # "-m <method>: switch between method 1 (extrapolation) and method 2 (refitting with 1 parameter constant)"
    # "-b: shows the error on samples Before the fit (by default After fit is shown)"
    # "-%: also show the individual errors as percentage of the total systematic error (off by default)"
    # "-y: take symmetrized average of minos errors"

    cmd = "python $ZEROLEPTONFITTER/ToolKit/SysTable.py -%s  -m 1 -w %s -c %s -o plots/systtable_%s.tex -n %s" % ("%",filename, region, anaconv,anaconv)
    print cmd
    if  not doPrintOnly: subprocess.call(cmd, shell=True)
    return

###################################################
#
###################################################

def makeSummaryPlots(doPrintOnly=False):
    print " ******** Make summary plots *********"
    cmd = "python $ZEROLEPTONFITTER/ToolKit/PlotMU_NP.py"
    print cmd
    if not doPrintOnly: subprocess.call(cmd, shell=True)

    cmd = "python $ZEROLEPTONFITTER/ToolKit/PlotSRs.py"
    print cmd
    if not doPrintOnly: subprocess.call(cmd, shell=True)

    return

##############################################################################
#    Main
##############################################################################
def main(zlFitterConfig):

    doBlind = False #unfortunately blinds everything.......LL
    useVRWTM = False
    useChargeAsymmetry = False

    parser = OptionParser()
    parser.add_option("--PrintOnly", default=False, action="store_true", help="do not execute the command")
    parser.add_option("--doVR", default=False, action="store_true", help="include tables with VRs that are not the _all.tex version")#ATT: remove
    parser.add_option("-s", "--shape", default=False, action="store_true", help="workspace has shape fits")#ATT: remove
    parser.add_option("-o", "--output-dir", default="results/",
                      help="output dir under which files can be found", metavar="DIR")
    (options, args) = parser.parse_args()

    options.output_dir += "/" #to be sure

    print options

    ###############################################################################

    #samples = "Diboson,GAMMAjets,Multijets,Top,Wjets,Zjets"
    samples = ",".join(zlFitterConfig.sampleNameList)

    renamedRegions = renameRegions(useChargeAsymmetry, useVRWTM)
    myAnaList = finalChannelsDict.keys()

    for anaName in myAnaList:
        regionList = zlFitterConfig.allRegionsList()

        # Filename containing workspace
        filename = os.path.join(options.output_dir, "ZL_%s_Background/Fit__Background_combined_NormalMeasurement_model_afterFit.root" % anaName)

        if not os.path.exists(filename):
            print "filename %s does not exist - continuing" % filename
            continue

        #Systematics
        makeSystematicsTables(anaName, filename, doPrintOnly=options.PrintOnly)

        #Yields
        makeYieldTables(anaName, filename, regionList, samples, renamedRegions, options.shape, options.doVR, doBlind,doPrintOnly=options.PrintOnly)

        #pull
        if not options.PrintOnly:
            pickleFilename = "plots/yield_%s_all.pickle" % (anaName)
            # makePullPlot(pickleFilename, regionList, samples, renamedRegions, anaName, doBlind)
            makePullPlot(pickleFilename, regionList, samples, renamedRegions, anaName, True)#ATT Nikola

    makeSummaryPlots(options.PrintOnly)

if __name__ == "__main__":
    zlFitterConfig = ZLFitterConfig()
    pullPlotUtils.getRegionColor = getRegionColor
    pullPlotUtils.getSampleColor = zlFitterConfig.getSampleColor
    main(zlFitterConfig)
