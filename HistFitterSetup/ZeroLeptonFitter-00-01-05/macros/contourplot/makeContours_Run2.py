#!/usr/bin/env python
# usage : 

import pprint
import time
import ROOT
import socket
import glob
import sys
import os

from array import array
from ROOT import *
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True


if not os.getenv("HISTFITTER"): 
    print "$HISTFITTER is not defined! Exiting now."
    sys.exit()

if not os.getenv("ZEROLEPTONFITTER"): 
    print "$ZEROLEPTONFITTER is not defined! Exiting now."
    sys.exit()
    
from ROOT import TGraph
ROOT.gSystem.Load("libSusyFitter.so");

ROOT.gROOT.LoadMacro("$ZEROLEPTONFITTER/macros/contourplot/ContourUtils.C");
ROOT.gROOT.LoadMacro("$ZEROLEPTONFITTER/macros/contourplot/contourmacros/GetSRName.C");
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)

INPUTDIR_SIGNALDB = "/afs/cern.ch/user/m/marijam/public/SignalDBs/"

# for 2D palette
ncontours = 99
stops = [0.00, 0.33, 0.66, 1.00]
red = [1.00, 238./255., 139./255., 0.00]
green = [1.00, 201./255., 90./255., 0.00]
blue = [1.00, 0.00, 0.00, 0.00]

s = array('d',stops)
r = array('d',red)
g = array('d',green)
b = array('d',blue)

npoints = len(s)
ROOT.TColor.CreateGradientColorTable(npoints, s, r, g, b, ncontours)
ROOT.gStyle.SetNumberContours(ncontours)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
# Import Modules                                                             # 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
import sys, os, string, shutil,pickle,subprocess
from allChannelsDict import *
from ZLFitterConfig import *


class MyGraph:
    def __init__(self, name):
        self.infoList = []
        self.name = name
        self.tgraph = None

    def Sort(self):
        self.infoList=sorted(self.infoList, key=lambda info: info[0])   # sort by x
        
    def Print(self):
        self.Sort()        
        for i in self.infoList:
            print self.name,i[0],i[1],StatTools.GetSigma(i[1]),i[2].replace("jet1","").replace("jet2","").replace("jet3","").replace("jet4","").replace("jet5","").replace("jet6","").replace("pt","").replace("metomeff","").replace("met","").replace("meff","").replace("Sig","").replace("dPhi","").replace("-",",")

    def DeltaMin(self, graph, xmax=-1, xmin=-1):
        deltamin = 10000
        xmin = -999
        for i in range(len(self.infoList)):
            if True:
                for j in range(len(graph.infoList)):
                    if self.infoList[i][0] == graph.infoList[j][0]:

                        delta = self.infoList[i][1]-graph.infoList[j][1]
                        if delta < deltamin:
                            deltamin = delta
                            xmin = graph.infoList[i][0]
        return (deltamin, xmin)
        
    def addPoint(self, x, y, ana=""):
        found=False
        for i in range(len(self.infoList)):
            if x == self.infoList[i][0]:
                found = True
                if y < self.infoList[i][1]:
                    self.infoList[i] = (x, y, ana)

        if not found:                
            self.infoList.append((x, y, ana))

    def getTGraph(self, color=1):
        if len(self.infoList) == 0: 
            return None

        self.Sort()

        g = TGraph(len(self.infoList))
        counter = 0
        for i in self.infoList:
            g.SetPoint(counter, i[0], i[1])
            #g.SetPoint(counter,i[0],StatTools.GetSigma(i[1]))
            
            counter+=1

        g.SetName(self.name)
        g.SetLineColor(color)
        g.SetMarkerColor(color) 
        g.SetLineWidth(2)        
        self.tgraph=g
        return g

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
# Some global variables
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#

# CHECK:
# INPUTDIR has the workspaces from HistFitter
INPUTDIR="%s/results/" % (os.getenv("ZEROLEPTONFITTER"))
INPUTDIR+="" 

# OUTPUTDIR is where the combination of these using hadd will go, as well as 
#           all the list files for the contours, the histograms and the plots
OUTPUTDIR = "Outputs/"
PLOTSDIR = "plots/"

if not os.path.exists(OUTPUTDIR): os.mkdir(OUTPUTDIR)
if not os.path.exists(PLOTSDIR): os.mkdir(PLOTSDIR)    

# List of grids: key maps to array of (xlabel, ylabel, xmin, xmax, ymin, ymax)
# Add your favourite grid here. Note: if interpretation is not hypo_<grid>_<pointX>_<pointY>,
# change makeContours()
gridInfo = {}
gridInfo["NUHMG"]=("m_{H_{1}}^{2} [TeV^{2}]","m_{1/2} [GeV]",1800000,7400000,430,910,[3])
#gridInfo["NUHMG"]=("Gluino mass [GeV]","Squark mass [GeV]",1000,1410,900,1260,[3])
gridInfo["SM_SS_direct"] = ("Squark mass [GeV]", "Neutralino1 mass [GeV]", 0, 1200, 25, 800, [3])
gridInfo["SM_SG_direct"] = ("Gluino mass [GeV]", "Neutralino1 mass [GeV]", 200, 1800, 25, 1800, range(0, 3))#ATT ???
gridInfo["SM_GG_direct"] = ("Gluino mass [GeV]", "Neutralino1 mass [GeV]", 200, 1500, 25, 1100, [1])
gridInfo["mssm"] = ("Gluino mass [GeV]", "Squark mass [GeV]", 800, 3200, 800, 3200, range(0, 3))#ATT ???
gridInfo["msugra_0_10_P"] = ("m_{0} [GeV]", "m_{1/2} [GeV]", 100, 6000, 300, 1000, [0, 44])
gridInfo["msugra_30_P"] = ("m_{0} [GeV]", "m_{1/2} [GeV]", 100, 6000, 300, 1000, [0, 44])
gridInfo["bRPV"] = ("m_{0} [GeV]", "m_{1/2} [GeV]", 100, 6000, 300, 1000, [0, 44])
gridInfo["nGM"] = ("m_{#tilde{#tau}} [GeV]", "m_{#tilde{g}} [GeV]", 115, 340, 395, 1300, [0, 44])

gridInfo["SM_GG_onestep_LSP60"] = ("Gluino mass [GeV]", "x = #Deltam(#chi^{#pm}, LSP)/#Deltam(#tilde{g}, LSP)", 200, 1500, 0, 1.8, [1])
gridInfo["SM_SS_onestep_LSP60"] = ("Squark mass [GeV]", "x = #Deltam(#chi^{#pm}, LSP)/#Deltam(#tilde{q}, LSP)", 200, 1500, 0, 1.5, [3])
gridInfo["SM_GG_onestep_X05"] = ("Gluino mass [GeV]", "Neutralino1 mass [GeV]", 200, 1500, 25, 1100, [1])
gridInfo["SM_SS_onestep_X05"] = ("Squark mass [GeV]", "Neutralino1 mass [GeV]", 200, 1500, 25, 1100, [3])

gridInfo["SM_GG_twostep_WWZZ"] = ("Gluino mass [GeV]", "Neutralino1 mass [GeV]", 200, 1600, 25, 1600, [1])
gridInfo["SM_SS_twostep_WWZZ"] = ("Squark mass [GeV]", "Neutralino1 mass [GeV]", 200, 1600, 25, 1600, [3])

gridInfo["pMSSM_qL_to_h_M160"] = ("Squark mass [GeV]", "M_{2} [GeV]", 250, 1600, 200, 1600, range(0,3) )
gridInfo["pMSSM_qL_to_h_M1M2"] = ("Squark mass [GeV]", "M_{2} [GeV]", 250, 1600, 200, 1600, range(0,3) )

gridInfo["Gluino_Stop_charm"] = ("m_{#tilde{g}} [GeV]", "m_{#tilde{t}} [GeV]", 300, 1320, 120, 1000,[1]) 
gridInfo["Gtt"] = ("m_{#tilde{g}} [GeV]", "m_{#tilde{t}} [GeV]", 300, 2000, 120, 1000,[1]) 
gridInfo["SM_TT_directCC"]=("Neutralino1 mass [GeV]","Stop1 mass [GeV]",95,350,50,350,[3])

gridInfo["Gluino_gluon"] = ("Gluino mass [GeV]", "Neutralino1 mass [GeV]", 200, 1500, 25, 1100, [1])

gridInfo["SS_direct"] = ("m(#tilde{q}) [GeV]", "m(#chi^{0}_{1}) [GeV]", 0, 1200, 25, 800, [3])
gridInfo["GG_direct"] = ("m(#tilde{g}) [GeV]", "m(#chi^{0}_{1}) [GeV]", 200, 2000, 5, 2000, [1])

# Cross sections to use. (Up, down is the theory uncertainty)
# Our plotting always uses Nominal for exp+obs+yellow band, up and down only for two extra obs curves
allXS=["Nominal"]
#allXS=["Nominal", "Up", "Down"]

###########################################################################
# useful functions
###########################################################################

def makeLegendName(name, shape):
    return name
    
    legComponents = name.split("-")
    #0 -> regions
    #1 -> meffcut
    #2 -> met/meff
    #10 -> metSig
    #13 -> nBins, #14 -> minBin, #15 -> maxBin
    meffcut = legComponents[1].replace("meffInc", "")
    metomeff = legComponents[2].replace("metomeff", "")
    metsig = legComponents[10].replace("metSig", "")    
    Wunres = legComponents[12].replace("Wunres", "")
    Wres = legComponents[13].replace("Wres", "")

    if shape:
        nBins = legComponents[13].replace("nBins", "")
        minbin = (int(legComponents[14])/1000)
        maxbin = (int(legComponents[15])/1000)

    legName = legComponents[0]
    if not shape:
        legName += " meffInc>%s" % meffcut
    else:
        legName += " meffInc %d-%d+" % (minbin, maxbin)
    
    if metomeff != "0": 
        legName += ", met/meffNj>%s" % metomeff

    if metsig != "0":
        legName += ", met/#sqrt{H_{T}}>%s" % metsig
    
    if Wunres != "0" or Wres != "0":
        legName += ", Wu#geq%s, Wr#geq%s" % (Wunres,Wres)

    return legName

def parseCmdLine(args):
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-m", dest="doMerge", help="merge output root files", action='store_true', default=False)
    parser.add_option("-c", dest="makeContours", help="create contours", action='store_true', default=False)
    parser.add_option("-o", dest="doOring", help="Analysis Oring", action='store_true', default=False)
    parser.add_option("-p", dest="makePlots", help="create plots", action='store_true', default=False)
    parser.add_option("-a", dest="makeATLASplots", help="create ATLAS plots", action='store_true', default=False)
    parser.add_option("-l", dest="makeLines", help="create lines", action='store_true', default=False)
    parser.add_option("-N", dest="numSquarks", default=1, type="int", help="number of squarks (divisor for xsec)")
    parser.add_option("--opti", dest="opti", help="use ana for optimization", action='store_true', default=False)
    parser.add_option("--modeL", dest="modeL", choices=["comb","metomeff","metsig","all"], default="comb", help="comb (default), metomeff or metsig; or all")
    parser.add_option("--inputDir", dest="inputDir", help="input directory", default=INPUTDIR)
    parser.add_option("--all", dest="doAll", help="do all steps", action='store_true', default=False)
    parser.add_option("--grid", dest="grid", help="grid name", default="SS_direct") #"GG_onestepCC")#
    parser.add_option("--shape", action="store_true", default=False, dest="shape", help="use MyAnaList_Shape.py when --opti, else the shape regions for Paper '13")
    parser.add_option("--suffix", dest="suffix", help="suffix to append after grid name in output files (default empty)", default="")
    parser.add_option("--match", dest="match", help="name to match input files against", default="")
    parser.add_option("--filter", dest="filter", help="name to filter input files against", default="")
    parser.add_option("--legend", dest="legend", help="legend entry for 'combined'", default="combined")
    parser.add_option("--ul", dest="makeUL", help="do upper limits", action='store_true', default=False)
    parser.add_option("--discovery", dest="discovery", help="use discovery lines", action='store_true', default=True)
    parser.add_option("--merge-ul-only", help="only merge UL files", action='store_true', default=False)
    parser.add_option("--compare", dest="compare", help="plot user-set lines in one graph", action="store_true", default=False)
    parser.add_option("--acceff", dest="acceff", help="path to the acc*eff pickle file", default="")

    (config, args) = parser.parse_args(args)

    if config.filter != "" and config.match != "" and (config.filter.find(config.match) != -1 or config.match.find(config.filter) != -1):
        print "--match and --filter overlap and negate each other -> zero input files by default! Exiting now."
        sys.exit()
    
    if config.makeUL and config.discovery:
        print "--ul and --discovery cannot be used simultaneously!"
        sys.exit()

    if not config.doAll and not config.doMerge and not config.makeContours and not config.doOring and not (config.makePlots or config.makeATLASplots):
        print "No step to execute specified!"

    print "Grid name: ", config.grid, ", Output name: config.outputName"    
        
    config.outputName = config.grid + config.suffix

    return config

def wait(sec):
    os.system('setterm -cursor off')
    while sec > 0:
        sys.stdout.write(str(sec) + '...     \r')
        sys.stdout.flush()
        sec -= 1
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            os.system('setterm -cursor on')
            print
            sys.exit()
    os.system('setterm -cursor on')

def getFileList(inputdir):
    cachefile = os.getenv("ZEROLEPTONFITTER")+"/macros/contourplot/results.cache"
    readDir = False
    readDir = True

    if os.path.exists(cachefile) and os.path.isfile(cachefile):
        f = open(cachefile)
        filenames = [l.strip() for l in f.readlines() if l.strip()]
        f.close()

        if len(filenames) == 0: readDir = True
    else:
        readDir = True

    if readDir:
        dirnames = os.listdir(inputdir)
        filenames = []
        i=1
        print "Found %d directories, reading them all..." % len(dirnames)
        for d in dirnames:
            sys.stdout.write('%d / %d \r' % (i, len(dirnames)))
            sys.stdout.flush()
            
            fnames = os.listdir(os.path.join(inputdir, d))
            for f in fnames:
                filenames.append(os.path.join(inputdir, d, f))
            i+=1

        f = open(cachefile, "w")
        for n in filenames:
            f.write("%s\n" % n)
        f.close()
    else:
        print "INFO: read %d lines from results.cache (file modified: %s)" % (len(filenames), time.ctime(os.path.getmtime(cachefile)))
        print "Waiting 3 seconds in case this is not correct and you want to delete the file..."
        wait(3)

    return filenames

def MergeFiles(config):
    filenames = getFileList(config.inputDir) 
   
    #filenames = glob.glob("%s/*.root" % config.inputDir)
    
    grid_name=config.grid
    name_match=config.match
    name_filter=config.filter

    if grid_name == "SM_GG_onestep_LSP60":
        grid_name="SM_GG_onestep"
    elif grid_name == "SM_GG_onestep_X05":
        grid_name="SM_GG_onestep"
    elif grid_name == "SM_SS_onestep_LSP60":
        grid_name="SM_SS_onestep"
    elif grid_name == "SM_SS_onestep_X05":
        grid_name="SM_SS_onestep"
    elif grid_name == "pMSSM_qL_to_h_M160":
        grid_name="pMSSM_qL_to_h"
        #extra_match="_60_Output"    
    elif grid_name == "pMSSM_qL_to_h_M1M2":
        grid_name="pMSSM_qL_to_h"
        #extra_filter="_60_Output"
    elif grid_name == "GG_direct" or grid_name == "SS_direct" or grid_name == "GG_onestepCC": 
        # config.anaList = ["SR4j-MetoMeff0.2-Meff2400-sljetpt200-34jetpt150-dphi0.4-ap0.02", "SR4j-MetoMeff0.2-Meff2400-sljetpt200-34jetpt60-dphi0.4-ap0.02", "SR4j-MetoMeff0.2-Meff1600-sljetpt200-34jetpt150-dphi0.4-ap0.02"]
        # config.anaList = ["SR5jbase-MetoMeff0.25-Meff1600-sljetpt100-34jetpt100-dphi0.4-ap0.04", "SR4jbase-MetoMeff0.2-Meff2200-sljetpt100-34jetpt100-dphi0.4-ap0.04"]
        config.anaList = ["SRJigsawSR1Loose"]

    # CHECK: Add your anaList            
    else:
        print "grid_name is not defined."
        config.anaList = allChannelsDict.keys()

    #merge histfitter output root files
    for ana in config.anaList:
        thisAnaFilenames = []

        # First, filter everything for this analysis
        for filename in filenames:
            if not filename.endswith(".root"):
                continue

            if filename.find(ana) == -1: 
                continue

            if filename.find(grid_name) == -1:
                continue
            
            if name_match != "" and filename.find(name_match) == -1:
                continue
            
            if name_filter != "" and filename.find(name_filter) != -1: 
                continue

            thisAnaFilenames.append(filename)
      
        thisFilenames = {}
        for xs in allXS:
            thisFilenames[xs] = []

        thisULFilenames = []
        
        # Now, split our output by UL and hypotest files
        for filename in thisAnaFilenames:
            if filename.find("upperlimit") != -1:
                thisULFilenames.append(filename)
            else:
                for xs in allXS:
                    
                    if filename.find(xs) != -1:
                        thisFilenames[xs].append(filename)
                        break

        for xs in allXS:
            if config.merge_ul_only:
                print "Not merging %s, %s, %s, --merge-only-ul used" % (config.grid, ana, xs)
            elif len(thisFilenames[xs]) == 0:
                print "No files for %s, %s, %s -> skipping" % (config.grid, ana, xs)
            else:
                if len(thisFilenames[xs])<200:
                    inputFiles = " ".join(thisFilenames[xs])
                    outputFilename = OUTPUTDIR+config.outputName+"_"+ana+"_fixSigXSec"+xs+".root"
                    cmd="hadd -f "+outputFilename+" "+inputFiles
                    subprocess.call(cmd, shell=True)
                else:
                    inputFiles = " ".join(thisFilenames[xs][:200])
                    outputFilename1 = OUTPUTDIR+config.outputName+"1_"+ana+"_fixSigXSec"+xs+".root"
                    cmd="hadd -f "+outputFilename1+" "+inputFiles 
                    subprocess.call(cmd, shell=True)
                    inputFiles = " ".join(thisFilenames[xs][200:])
                    outputFilename2 = OUTPUTDIR+config.outputName+"2_"+ana+"_fixSigXSec"+xs+".root"
                    cmd="hadd -f "+outputFilename2+" "+inputFiles 
                    subprocess.call(cmd, shell=True)
                    outputFilename = OUTPUTDIR+config.outputName+"_"+ana+"_fixSigXSec"+xs+".root"            
                    cmd="hadd -f "+outputFilename+" "+outputFilename1+" " +outputFilename2
                    subprocess.call(cmd, shell=True)
                    os.remove(outputFilename1)
                    os.remove(outputFilename2)

        if config.makeUL:
            if len(thisULFilenames) == 0:
                print "No UL files for %s, %s -> skipping" % (config.grid, ana)
            else:
                if len(thisULFilenames)<200:
                    outputFilename = OUTPUTDIR+config.outputName+"_"+ana+"_upperlimit.root"
                    inputFiles = " ".join(thisULFilenames)
                    cmd="hadd -f "+outputFilename+" "+inputFiles 
                    subprocess.call(cmd, shell=True)
                else:
                    inputFiles = " ".join(thisULFilenames[:200])
                    outputFilename1 = OUTPUTDIR+config.outputName+"1_"+ana+"_upperlimit.root"
                    cmd="hadd -f "+outputFilename1+" "+inputFiles 
                    subprocess.call(cmd, shell=True)
                    inputFiles = " ".join(thisULFilenames[200:])
                    outputFilename2 = OUTPUTDIR+config.outputName+"2_"+ana+"_upperlimit.root"
                    cmd="hadd -f "+outputFilename2+" "+inputFiles 
                    subprocess.call(cmd, shell=True)
                    outputFilename = OUTPUTDIR+config.outputName+"_"+ana+"_upperlimit.root"            
                    cmd="hadd -f "+outputFilename+" "+outputFilename1+" " +outputFilename2
                    subprocess.call(cmd, shell=True)
                    os.remove(outputFilename1)
                    os.remove(outputFilename2)

def getDSIDs(config):
    #open file containing relation (stored as a dict) between mc channel and sparticle mass information
    try:
        picklefile = open('signalPointPickle.pkl', 'rb')
    except:
        cmd="python $ZEROLEPTONFITTER/ToolKit/makeSignalPointPickle.py"
        print cmd
        subprocess.call(cmd, shell=True)
        picklefile = open('signalPointPickle.pkl','rb')    
        pass
    
    pointdict = pickle.load(picklefile)
    picklefile.close()

    grid= config.grid
    if "_LSP60" in grid: grid= grid.replace("_LSP60","")
    if "_X05" in grid: grid= grid.replace("_X05","")
    if "_M160" in grid: grid = grid.replace("_M160","")
    if "_M1M2" in grid: grid = grid.replace("_M1M2","")
   
    DSIDs = {}
    for key, info in pointdict[grid].items():
        if len(info) == 2: 
            s = "%s_%s" % (info[0], info[1]) 
        elif len(info) == 3: 
            s = "%s_%s_%s" % (info[0], info[1], info[2]) 
        else:  
            print "grid has neither 2 nor 3 parameters!!!!!!!!!!"
  
        DSIDs[s] = key

    return DSIDs

def extractCrossSections(config, DBfile):
    grid = config.grid
    if "_X05" in grid: grid = grid.replace("_X05","");
    if "_LSP60" in grid: grid = grid.replace("_LSP60","");
    if "_M160" in grid:
        grid = grid.replace("_M160","");
    if "_M1M2" in grid:
        grid = grid.replace("_M1M2","");
    
    map = DBfile.Get("runNumToXsec")
    DSIDs = getDSIDs(config)
        
    if config.numSquarks > 1:
        print  "WARNING! Will divide all cross sections by %d" % config.numSquarks
        wait(3)

    xsecs = {}
    for key in DSIDs:
        xsec = 0
        
        MCid = DSIDs[key]
        
        gridName = config.grid
        if config.grid == "SM_SS_direct_compressedPoints":
            gridName = "SM_SS_direct"
        
        procs = gridInfo[gridName]
        
        if "SM_TT_directCC" not in config.grid:
            for proc in procs[6]:
                newkey = str(MCid)+":"+str(proc)
                vec = map.GetValue(newkey)
                if vec != None:
                     xsec_per_proc = float(vec[0])
                     xsec += xsec_per_proc
        else:
            for proc in range(1,55):
                newkey = str(MCid)+":"+str(proc)
                vec = map.GetValue(newkey)
                if vec != None:
                    xsec_per_proc = float(vec[0])
                    xsec += xsec_per_proc
       
        xsec = xsec / config.numSquarks

        print "match for MC %s -> %s => xsec = %.2e" % (DSIDs[key], key, xsec)
        xsecs[key] = xsec

    return xsecs       
		       
def mergeFileList(config, clsFileName, upperFileName):
    # This method merges the two files where the hypotest and hypotestinverter results are stored
    # Information on the cross-section is also added
  
    print "Merging UL and CLs files"

    from summary_harvest_tree_description import treedescription
    dummy,description = treedescription()
    allpar = description.split(':')
    
    #get list of process
    gridName = config.grid
    if config.grid == "SM_SS_direct_compressedPoints":
        gridName = "SM_SS_direct"
    procs = gridInfo[gridName][6]
    
    #open the first file and get info
    myMap = {}
    try:
        f = open(clsFileName, 'r')
    except:
        print "WARNING: ",clsFileName,"can't be found. skipped"        
        return
    
    for line in f.readlines():
        elements = line.strip().split()
        if "onestep" in config.grid:
            key = (elements[-4], elements[-3], elements[-2])
            myMap[key] = elements
            #print "myMap= ",myMap[key]
        elif "pMSSM_qL" in config.grid: 
            key = (elements[allpar.index('M1')], elements[allpar.index('M2')], elements[allpar.index('msq')])
            myMap[key] = elements
            #print "key= ", key
            #print "elements=%s" % elements
        else:
            key = (elements[-3], elements[-2])
            myMap[key] = elements
    f.close()
    
    #open the second file and get info
    try:
        f = open(upperFileName, 'r')
    except:
        print "WARNING: ",upperFileName,"can't be found. skipped"        
        return
 
    for line in f.readlines():
        elements = line.strip().split()
        key = (elements[-3],elements[-2]) #key id (m0,m12)
        if "onestep" in config.grid:
            key = (elements[-4], elements[-3], elements[-2])
        elif "pMSSM_qL" in config.grid: 
            key = (elements[allpar.index('M1')], elements[allpar.index('M2')], elements[allpar.index('msq')])
        else:
            key = (elements[-3], elements[-2]) #key id (m0,m12)
        
        if key not in myMap.keys():
            print "KEY %s NOT IN orignal map -> replacing with info from UL file" % ("_".join(key))
            if "onestep" in config.grid or "pMSSM_qL" in config.grid: 
                myMap[key] = elements
            else: 
                myMap[key] = elements
        else:
            #replace info on upperlimits
            myMap[key] = myMap[key][:19] + elements[19:26] + myMap[key][26:] 
    f.close()

    #read the acc*eff
    acceffdict = {}
    if config.acceff != "":
        try:
            picklefile = open(config.acceff,'rb')
            acceffdict = pickle.load(picklefile)
            picklefile.close()   
        except:
            print "WARNING: ",config.acceff,"can't be found. skipped"        
            return    	

    grid = config.grid
    if "_X05" in grid: 
        grid = grid.replace("_X05","");
    if "_LSP60" in grid: 
        grid = grid.replace("_LSP60","");
    if "_M160" in grid:
        grid = grid.replace("_M160","");
    if "_M1M2" in grid:
        grid = grid.replace("_M1M2","");

    if grid == "SM_SS_direct_compressedPoints":
        # generator efficiency is taken care of in the norm weights already, so use the one without them
        grid = "SM_SS_direct_compressedPoints_NoGenEff" 

    #open SignalDB file
    DBfile = ROOT.TFile.Open(INPUTDIR_SIGNALDB+"SignalDB_"+grid+".root")
    try:
        map = DBfile.Get("runNumToXsec")
    except:
        print "cannot get map in ",INPUTDIR_SIGNALDB+"SignalDB_"+grid+".root"
        
    if not (config.grid.find("onestep") != -1 or config.grid.find("direct") != -1 or config.grid.find("pMSSM_qL_to_h") != -1 or config.grid == "Gluino_Stop_charm" or config.grid == "bRPV" or config.grid == "Gluino_gluon"):
        print "Grid %s undefined - not extracting cross-sections" % (config.grid)
        print "Look for this message and add the grid if you're trying to run with --ul and this is supposed to make sense"
        
        # hard exit, otherwise we get confusing output!
        sys.exit() 

    newfile = open(clsFileName, 'w')
    DSIDs = getDSIDs(config)
    xsecs = extractCrossSections(config, DBfile)

    for key,infos in myMap.items():
        xsec = 1
        acc_eff = 1
        #need to extract info from tomas file here
        for line in acceffdict.items():
            key2 = "(%s, %s, %s)" % (key[2].replace(".000000", ""), 
                                     key[0].replace(".000000", ""), 
                                     key[1].replace(".000000", ""))	
            SR = line[0].replace(key2, "")
            
            if key2 in line[0] and SR in clsFileName: 
                acc_eff = float(line[1][0])
                if acc_eff < 0.0 : 
                    acc_eff = 0.0
                xsec = float(line[1][1])

        #extract x-section from the SignalDB file
        if "GG_onestep" in config.grid: 
            m1 = key[1] #gluino
            m2 = key[0] #chargino
            m3 = key[2] #lsp
            s = "%d_%d_%d" % (float(key[1]), float(key[0]), float(key[2]))
        elif "SS_onestep" in config.grid: 
            m1 = key[2] #squark
            m2 = key[0] #chargino
            m3 = key[1] #lsp
            s = "%d_%d_%d" % (float(key[2]), float(key[0]), float(key[1]))
        elif "direct" in config.grid: 
            m1 = key[0] #squark/gluino
            m2 = key[1] #lsp
            m3 = 0
            s = "%d_%d" % (float(key[0]), float(key[1]))
        elif "pMSSM_qL" in config.grid:
            m1 = key[0] #M1
            m2 = key[1] #M2
            m3 = key[2] #mqL
            s = "%d_%d_%d" % (float(key[0]), float(key[1]), float(key[2]))
        elif "Gluino_Stop_charm" or "bRPV" in config.grid: 
            m1 = key[0] #squark/gluino
            m2 = key[1] #lsp
            m3 = 0
            s = "%d_%d" % (float(key[0]), float(key[1]))

        xsec = xsecs[s]
        infos[allpar.index("xsec")] = xsec*1000 # note: units in fb

        # multiply upperLimits by xsec*acc_eff, if defined
        if config.acceff != "":
            for i in range(19,26):
                infos[i] = float(infos[i])*xsec*1000*acc_eff #beware of the units pb-1 vs fb-1
                #infos[i]=float(infos[i])*xsec*1000 #beware of the units pb-1 vs fb-1

        # write to combined file
        line = ""
        for info in infos:
            line += " " + str(info) 
        
        newfile.write(line+"\n")
    
    if DBfile!=None:
        DBfile.Close()    
    newfile.close()

def MakeContours(config):
    automaticRejection = False # automatic rejection of bad points in HistFitter

    #merge histfitter output root files
    for ana in config.anaList:        
        print "MakeContours:", ana

        for xs in allXS:
            if config.discovery and xs != "Nominal":
                print "--discovery only uses nominal values, ignoring xsec %s" % xs
                continue
            
            basename = OUTPUTDIR+config.outputName+"_"+ana+"_fixSigXSec"+xs

            basenameUL = OUTPUTDIR+config.outputName+"_"+ana+"_upperlimit"  
            
            cutStr = "1"; # accept everything
            
            # Format of the hypotests, normally follows e.g. hypo_<grid>_2000_1000 
            format     = "hypo_"+config.grid+"_%f_%f";
            interpretation = "m0:m12";            
            
            # pMSSM is different; if your grid is also different, add here
            if config.grid == "pMSSM":
                format     = "hypo_"+config.grid+"_%f";
                interpretation = "id";  

            if config.grid == "mssm":
                format     = "hypo_"+config.grid+"_%f_%f_%f";
                interpretation = "msq:mgl:mlsp"; 
            
            if config.grid.find("SM_GG_twostep")!=-1:
                format     = "hypo_SM_GG_twostep_WWZZ_%f_%f_%f";
                interpretation = "mgluino:mchargino:mlsp"; 
            
            if config.grid.find("SM_SS_twostep")!=-1:
                format     = "hypo_SM_SS_twostep_WWZZ_%f_%f_%f";
                interpretation = "msquark:mchargino:mlsp"; 
            
            if config.grid.find("SM_GG_onestep")!=-1:
                format     = "hypo_SM_GG_onestep_%f_%f_%f";
                interpretation = "mgluino:mchargino:mlsp"; 
            
            if config.grid.find("SM_SS_onestep")!=-1:
                format     = "hypo_SM_SS_onestep_%f_%f_%f";
                interpretation = "msquark:mchargino:mlsp";
            
            if config.grid.find("pMSSM_qL_to_h")!=-1:
                format     = "hypo_pMSSM_qL_to_h_%f_%f_%f";
                interpretation = "M1:M2:msq";

            if config.grid=="MUED":
                format = "hypo_MUED_%f_%f";
                interpretation = "oneOverR:LambdaR";

            if config.grid.find("GG_onestepCC")!=-1:
                format     = "hypo_GG_onestepCC_%f_%f_%f";
                interpretation = "mgluino:mchargino:mlsp";
                
            if config.discovery:
                format = format.replace("hypo", "hypo_discovery")
            
            print "INFO: format set to %s" % format

            listSuffix = "__1_harvest_list"

            # LSP60 wants mlsp==60, other onestep grids want mlsp != 60
            if config.grid.find("onestep") != -1 and config.grid.find("LSP60") != -1:
                cutStr = "mlsp==60"
                listSuffix = "__mlspEE60_harvest_list"
            elif config.grid.find("onestep") != -1 and config.grid.find("LSP60") == -1:
                # tmp cutStr = "mlsp!=60"
                # tmp listSuffix = "__mlspNE60_harvest_list"
                print "removed mlsp!=60 temtatively"
            # M160 wants M1==60, other pMSSM grids want M1 != 60
            if config.grid.find("pMSSM_qL") != -1 and config.grid.find("M160") != -1:
                cutStr = "M1==60"
                listSuffix = "__M1EE60_harvest_list"
            elif config.grid.find("pMSSM_qL") != -1 and config.grid.find("M160") == -1:
                cutStr = "M1!=60"
                listSuffix = "__M1NE60_harvest_list"

            if config.discovery:                
                listSuffix = "_discovery_1_harvest_list"
                
            inputfile = basename+".root"
            print "MakeContours: inputfile name", inputfile
            if os.path.isfile(inputfile):
                #CollectAndWriteHypoTestResults( inputfile, format, interpretation, cutStr, int(automaticRejection) ) ;
                
                # weird concept, but this prevents a memleak
                cmd = "$ZEROLEPTONFITTER/macros/contourplot/CollectAndWriteHypoTestResults.py -F %s -f %s -I %s -c %s" % (inputfile, format, interpretation, cutStr)
                if config.discovery:
                    cmd += " -d"
                print "Executing: ", cmd
                subprocess.call(cmd, shell=True)
                subprocess.call('ls *list', shell=True)
                cmd="mv *_list "+OUTPUTDIR
                subprocess.call(cmd, shell=True)


            # get extra information from upper limits computation and merge the files
            if config.makeUL and xs == "Nominal":
                inputfile = basenameUL+".root"
                if os.path.isfile(inputfile):
                    #CollectAndWriteHypoTestResults( inputfile, format, interpretation, cutStr, int(automaticRejection) ) ;
                    
                    # by defition, ULs are not discovery -> don't care about passing -d
                    # weird concept, but this prevents a memleak
                    cmd = "$ZEROLEPTONFITTER/macros/contourplot/CollectAndWriteHypoTestResults.py -F %s -f %s -I %s -c %s" % (inputfile, format, interpretation, cutStr)
                    print "Executing %s" % cmd
                    subprocess.call(cmd, shell=True)
                    
                    cmd="mv *_list "+OUTPUTDIR
                    print "Executing %s" % cmd
                    subprocess.call(cmd, shell=True)
                    
                    #merge the 2 files in 1
                    mergeFileList(config, basename+listSuffix, basenameUL+listSuffix)
            
            if not os.path.exists(basename+listSuffix):
                # Does it exist in JSON format?
                JSONname = "%s.json" % (basename+listSuffix)
                if os.path.exists(JSONname):
                    print "INFO: attempting to generate old-fashioned list from JSON output %s" % (JSONname)
                    cmd = "GenerateTreeDescriptionFromJSON.py -f %s" % JSONname
                    subprocess.call(cmd, shell=True)

                # Now does it exist?
                if not os.path.exists(basename+listSuffix):
                    print "INFO: file %s does not exist, skipping call to makecontourhists.C" % (basename+listSuffix)
                    continue

            cmd="mv *_list "+OUTPUTDIR
            subprocess.call(cmd, shell=True)
           
            if False:
              gROOT.LoadMacro("m0m12tomglmsq.h");
              from ROOT import m0m12tomgl,m0m12tomsq

              # hack (m0,m12) to (mgl,msq)
              from summary_harvest_tree_description import treedescription
              dummy,description = treedescription()
              allpar = description.split(':')

              fname = basename+listSuffix
              os.system('mv %s %s.bak'%(fname,fname))
              fin = open('%s.bak'%fname)
              fout = open('%s'%fname,'w')
              for line in fin:
                words = line.split()
                m0 = float(words[allpar.index("m0")])
                m12 = float(words[allpar.index("m12")])
                mgl = m0m12tomgl(m0,m12)
                msq = m0m12tomsq(m0,m12)
                words[allpar.index("m0")]=str(mgl)
                words[allpar.index("m12")]=str(msq)
                print 'hack m0=',m0,'m12=',m12,'to mgl=',mgl,'msq=',msq
                line_new = ' '.join(words)+'\n'
                fout.write(line_new)
            # NUHMG, put True, change macro in makecontourplot_NUHMG.C
            if False and config.grid=="NUHMG":
              gROOT.LoadMacro("m0m12tomglmsq.h");
              from ROOT import m0m12tomgl_nuhmg,m0m12tomsq_nuhmg

              # hack (m0,m12) to (mgl,msq)
              from summary_harvest_tree_description import treedescription
              dummy,description = treedescription()
              allpar = description.split(':')

              fname = basename+listSuffix
              os.system('mv %s %s.bak'%(fname,fname))
              fin = open('%s.bak'%fname)
              fout = open('%s'%fname,'w')
              for line in fin:
                words = line.split()
                m0 = float(words[allpar.index("m0")])
                m12 = float(words[allpar.index("m12")])
                mgl = round(m0m12tomgl_nuhmg(m0,m12),2)
                msq = round(m0m12tomsq_nuhmg(m0,m12),2)
                words[allpar.index("m0")]=str(mgl)
                words[allpar.index("m12")]=str(msq)
                print 'hack m0=',m0,'m12=',m12,'to mgl=',mgl,'msq=',msq
                line_new = ' '.join(words)+'\n'
                fout.write(line_new)

            cmd = "root -b -q \"$ZEROLEPTONFITTER/macros/contourplot/makecontourhists.C(\\\""+basename+listSuffix+"\\\",\\\""+config.grid+"\\\")\""
            print cmd
            subprocess.call(cmd, shell=True)
                        
            cmd = "mv -v *_list.root "+OUTPUTDIR
            print cmd
            subprocess.call(cmd, shell=True)

            pass
        pass
    pass

def MakeLines(config):

    from summary_harvest_tree_description import treedescription
    dummy,description = treedescription()
    allpar = description.split(':')

    config.modeL=config.modeL.replace(" ","")
    if config.grid=="SM_SS_direct":
        allLines=[
            ("d",25,300,600)
            ]    
    elif config.grid=="SM_GG_direct":
        allLines=[("v",700,0,700),
                  ("h",0,400,2000),
                  ("v",1125,00,750)]
        
    elif config.grid=="SM_SG_direct":
        allLines=[("v",1012,0,1100),
                  ("h",0,1000,1700),
                  ("v",1387,0,900)]
        
    elif config.grid=="Gluino_Stop_charm":
        allLines=[("v",1000,0,800),
                  ("h",200,400,1500)
                  ]

    elif config.grid=="NUHMG":
        allLines=[("v",0,1800000,7400000),
                  ("h",0,430,910),
                  ("v",0,1800000,7400000)]
 
    elif config.grid=="pMSSM_qL_to_h_M160":
        allLines=[("s",950,200,900),
                  ("s",1050,200,1000),
                  ("s",1150,200,1100),
                  ("s",1250,200,1200)]

    elif config.grid=="GG_direct":
        allLines=[("v",1200,0,2000),
                  ("h",0,800,2000),
                  ]
        
    for aLine in allLines:

        MIN=0.05
        MAX=50
        logY=True#False
            
        MASSMIN=aLine[2]#0
        MASSMAX=aLine[3]#600
        line=aLine[0]
        cut=aLine[1]

        canvas = TCanvas("","");
        if logY:
            canvas.SetLogy()
            MAX=50
        if config.discovery:
            MAX=10
            MIN=0.00000001
            
        leg= TLegend(0.11,0.5,0.65,0.89);
        if config.discovery:
            leg= TLegend(0.6,0.11,0.89,0.4);
        leg.SetTextSize( 0.03 );
        leg.SetTextFont( 42 );
        leg.SetFillColor( 0 );
        leg.SetFillStyle(1001);

        colors = [0,1,2,3,4,6,ROOT.kOrange,7,15,50,35,42,27,38,ROOT.kPink,45,56]*100
        counter=0

        best = MyGraph("best")
        bestPaper13 = MyGraph("bestPaper13")
        bestMETSig = MyGraph("best MET significance")
        bestMETOMEFF = MyGraph("best MET/meff")
        bestNOMEFF = MyGraph("best no meff")
        bestDPhi0 = MyGraph("best no extra dphi cut")
        
        xsecGraph= MyGraph("xsec")

        allMyGraphs=[]
        missingFiles=[]

        listSuffix = "__1_harvest_list"
        if config.discovery:
            listSuffix = "_discovery_1_harvest_list"
        if config.grid.find("M160") != -1:
            listSuffix = "__M1EE60_harvest_list"
        elif config.grid.find("M1M2") != -1:
            listSuffix = "__M1NE60_harvest_list"

        for ana in config.anaList:
            filename = OUTPUTDIR+config.outputName+"_"+ana+"_fixSigXSecNominal"+listSuffix
            
            if config.match != "" and filename.find(config.match) == -1:
                continue
            
            if config.filter != "" and filename.find(config.filter) != -1: 
                continue
            
            print "OPEN: ",filename
            try:                
                textfile = open(filename)
            except:
                missingFiles.append(filename)
                print "WARNING: ",filename,"can't be found. skipped"        
                continue
            
            graph = MyGraph(ana)
            for text in textfile.readlines():
                text = text.strip().split()
                UL = float(text[allpar.index("expectedUpperLimit")])
                #if UL<0.05: continue #ATT!!!!!
                #UL=float(text[allpar.index("CLsexp")])
                #UL=StatTools.GetSigma(float(text[allpar.index("CLsexp")]))
                if config.discovery:
                    UL = float(text[allpar.index("p0exp")])
                xsec = float(text[allpar.index("xsec")])

                m0 = float(text[-3])#600
                m12 = float(text[-2])#50
                deltaM = m0-m12

                if "pMSSM_qL_to_h" in filename:
                    m0 = float(text[allpar.index("M1")])
                    m12 = float(text[allpar.index("M2")])
                    mqL = float(text[allpar.index('msq')])
                    deltaM = m0-m12

                ####print m0,UL
                #print m0, m12, UL
                
                if UL <= 0:
                    print "%s skipping point with UL<0" % ana
                    continue

                var=0
                if line=="d":
                    if deltaM != cut:
                        print "%s deltaM cut failed" % ana
                        continue
                    var=m0
                elif line=="s":
                    # cuts on mqL for the pMSSM grid
                    if mqL != cut:
                        print "%s mqL cut failed: mqL=%.2f cut=%.2f" % (ana, mqL, cut)
                        continue
                    var = m12 #this really is M2

                elif line=="h":
                    if m12 != cut:
                        #print "DEBUG: %s m12 cut failed" % ana
                        continue
                    var=m0
                else:
                    if m0 != cut:
                        #print "DEBUG: %s m0 cut failed: m0=%.2f cut=%.2f" % (ana, m0, cut)
                        continue
                    var = m12
                    #print UL,m12,ana

                #print "DEBUG: %s point passed cuts; checking ranges" % ana

                if var<MASSMIN:
                    #print "DEBUG: %s: var %.2f lower than min " % (ana, var)
                    continue      
                if var>MASSMAX: 
                    #print "DEBUG: %s: var %.2f higher than max " % (ana, var)
                    continue
                
                #print "DEBUG: ranges pass; data: %.2f UL=%.8f ana=%s" % (var, UL, ana)

                #print ana,"==========="
                isPaper13=False
                if config.discovery==False and ana in [AnaConvert(tmp) for tmp in anaInvDictPaper13.keys()]: 
                    bestPaper13.addPoint(var, UL, ana)
                    isPaper13=True
                    #continue
                
                if ana.find("-meff0-")>= 0:
                    bestNOMEFF.addPoint(var,UL,ana)
                    #continue

                if ana.find("Sig0-")< 0 and not isPaper13:                 
                    bestMETSig.addPoint(var,UL,ana)
                    #continue
                    
                if ana.find("metomeff0-")<0 and not isPaper13:                    
                    bestMETOMEFF.addPoint(var, UL, ana)
                else:                    
                    bestMETSig.addPoint(var, UL, ana)
                    #continue
                
                if ana.find("-dPhi0")>=0 and ana.find("-dPhi0.") <0 and not isPaper13:
                    bestDPhi0.addPoint(var, UL, ana) 
                    
                if config.modeL == "comb" and not isPaper13:
                    best.addPoint(var, UL, ana)
                    graph.addPoint(var, UL, ana)
                    #continue
                
                #reject Paper13 ana
                if config.modeL != "comb" and (ana.find("loose")>=0 or ana.find("medium")>=0  or ana.find("tight")>=0):
                    continue

                if config.modeL == "nomeff" and ana.find("-meff0-")<0:
                    continue

                if config.modeL == "metomeff" and ana.find("-metomeff0-")>=0:
                    continue

                if config.modeL == "metsig" and ana.find("-metSig0-")>=0:
                    continue            

                graph.addPoint(var, UL, ana)
                best.addPoint(var, UL, ana)

                xsecGraph.addPoint(var,xsec,ana)

            allMyGraphs.append(graph)
            textfile.close()

        # only print graphs contributing to the best line
        selectedMyGraphs=[]
        for mg in allMyGraphs:
            counter += 1
            deltaMin = mg.DeltaMin(best, xmax=MASSMAX, xmin=MASSMIN)[0]
            #print deltaMin
            #print mg.name
            if deltaMin < 0.01 and config.modeL != "comb":                
                selectedMyGraphs.append(mg)
                #print "====>", mg.name
        
        #selectedMyGraph=sorted(allMyGraphs, key=lambda toto: toto.DeltaMin(best,xmax=MASSMAX,xmin=MASSMIN)[0])   # sort by x

        ###best=sorted(best, key=lambda toto: toto[0])   # sort by x
        best.Print()

        # no analyses available
        if config.modeL != "comb" and len(selectedMyGraphs) == 0:
            print "ERROR: len(selectedMyGraphs) == 0 -> this mode has no lines that are the best, nothing to plot"
            return

        g = best.getTGraph()
        g2 = xsecGraph.getTGraph()
        if g:
            g.SetMaximum(MAX)
            g.SetMinimum(MIN)
            g.SetMarkerStyle(20)
            g.GetXaxis().SetLimits(MASSMIN,MASSMAX)
            g.GetYaxis().SetTitle("#sigma_{excluded}/#sigma_{nominal}" if not config.discovery else "Discovery p_{0}")
                    
        xaxis="TOTO"
        if g and line == "h":
            xaxis = gridInfo[config.grid][0]            
            g.SetTitle(gridInfo[config.grid][1]+" = "+str(cut))
        if g and ( line == "v" or line == "s"): #pMSSM sq cut "s" also uses 2nd var
            xaxis=gridInfo[config.grid][1]            
            g.SetTitle(gridInfo[config.grid][0]+" = "+str(cut))
            
        if g:
            g.GetXaxis().SetTitle(xaxis)
      
        if g:
            g.Draw("APL")
            if config.discovery:
                leg.AddEntry(g,config.legend,"PL")
            else:
                leg.AddEntry(g,"Best all analysis","PL")
                
        value=1##0.05###1.64485
        tline=TLine(MASSMIN,value,MASSMAX,value)
        tline.SetLineStyle(2)
        tline.Draw("same")
        
        if config.discovery:
            values=[0.5, 0.317*0.5,0.0455*0.5,0.0027*0.5,0.00006*0.5,3.0*0.0000001]
            tlines=[]
            for sigma, pzerovalue in enumerate(values):
                tlines.append(TLine(MASSMIN,pzerovalue,MASSMAX,pzerovalue))
                tlines[sigma].SetLineStyle(7)
                tlines[sigma].SetLineWidth(2)
                print TColor
                tlines[sigma].SetLineColor(ROOT.kRed+2)
                tlines[sigma].Draw("same")

            lsigma=[]
            for sigma, ysigma in enumerate([0.725, 0.65, 0.545, 0.4, 0.22]):
                lsigma.append(TLatex(0.91,ysigma,str((int(sigma)+1))+" #sigma"))
                lsigma[sigma].SetTextColor(ROOT.kRed+2);
                lsigma[sigma].SetNDC(kTRUE);
                lsigma[sigma].SetTextSize(0.04);
                lsigma[sigma].SetTextFont(42);
                lsigma[sigma].Draw("same");

            l2=TLatex(0.118,0.83,"#bf{#it{ATLAS}} Simulation Internal   Discovery reach in 0-lepton+jets+E_{T}^{miss}: "+config.grid);
            l2.SetNDC(kTRUE);
            l2.SetTextSize(0.035);
            l2.SetTextFont(42);
            l2.Draw("same");
            
                
        if config.grid=="SM_SS_direct":
            value2=1/8.
            tline2=TLine(MASSMIN,value2,MASSMAX,value2)
            tline2.SetLineStyle(2)
            tline2.Draw("same")
            value3=1/4.
            tline3=TLine(MASSMIN,value3,MASSMAX,value3)
            tline3.SetLineStyle(3)
            tline3.Draw("same")
            
        if config.modeL == "comb":
            gPaper13=bestPaper13.getTGraph(2)
            if gPaper13:
                gPaper13.SetLineWidth(3)
                leg.AddEntry(gPaper13,"Best of Paper13 analyses","L")
                gPaper13.Draw("PL")
                        
            gMETOMEFF=bestMETOMEFF.getTGraph(4)
            if gMETOMEFF and not config.discovery:
                leg.AddEntry(gMETOMEFF,"Best met/meff analyses","L")
                gMETOMEFF.Draw("PL")
            
            gMETSig=bestMETSig.getTGraph(3)
            if gMETSig and not config.discovery:
                leg.AddEntry(gMETSig,"Best METSig analyses","L")
                gMETSig.Draw("PL")
            
            gNOMEFF=bestNOMEFF.getTGraph(6)
            if gNOMEFF:
                leg.AddEntry(gNOMEFF,"Best no meff analyses","L")
                gNOMEFF.Draw("PL")

        #gDPhi0=bestDPhi0.getTGraph(6)
        #leg.AddEntry(gDPhi0,"oring of analysis without tighten dphi cut","L")
        #gDPhi0.Draw("PL")
        
        #g2.Draw("L*")
        counter=0
        for mg in selectedMyGraphs:
            counter+=1
            g=mg.getTGraph(color=colors[counter])
            if g == None:
                continue
            
            leg.AddEntry(g, makeLegendName(mg.name, config.shape), "L")
           # leg.AddEntry(g,mg.name.replace("jet1","").replace("jet2","").replace("jet3","").replace("jet4","").replace("jet5","").replace("jet6","").replace("pt","").replace("metomeff","").replace("met","").replace("meff","").replace("Sig","").replace("dPhi","").replace("-",",").replace("Wunres","").replace("Wres",""), "L")

            g.SetMarkerStyle(24)
            g.SetLineStyle(1)
            if g.GetName().find("loose")>=0 or g.GetName().find("medium")>=0  or g.GetName().find("tight")>=0 :
                g.SetLineStyle(1)
            g.Draw("L")

        leg.Draw("same")

        canvas.Print(PLOTSDIR+"/"+config.outputName+"_"+line+str(cut)+"_mode_"+str(config.modeL)+".eps")
        canvas.Print(PLOTSDIR+"/"+config.outputName+"_"+line+str(cut)+"_mode_"+str(config.modeL)+".pdf")
        canvas.Print(PLOTSDIR+"/"+config.outputName+"_"+line+str(cut)+"_mode_"+str(config.modeL)+".png")
        
        if len(missingFiles) > 0:
            print "##########################################################"
            print "##########################################################"
            print "##########################################################"
            print "# Missing files:                             "
            for file in missingFiles:
                print file
            print "##########################################################"

def CompareLines(config, fileList, outputName):
    from summary_harvest_tree_description import treedescription
    dummy,description = treedescription()
    allpar = description.split(':')
    
    config.modeL=config.modeL.replace(" ","")
    if config.grid=="SM_SS_direct":
        allLines=[
            ("h",0,250,1200),
            ("v",487,0,550),
            ("v",750,0,550)
            ]    
    elif config.grid=="SM_GG_direct":
        allLines=[("v",700,0,700),
                  ("h",0,700,1400),
                  ("v",1125,00,750)]
        
    elif config.grid=="SM_SG_direct":
        allLines=[("v",1012,0,1100),
                  ("h",0,1000,1700),
                  ("v",1387,0,900)]

    elif config.grid=="SM_GG_onestep_LSP60":
        allLines=[("v",1012,0,1500),
                  ("h",0,200,1500),
                  ("v",1012,0,1.5)]

 
    for aLine in allLines:

        MIN=0.05
        MAX=5
        logY=False
            
        MASSMIN=aLine[2]#0
        MASSMAX=aLine[3]#600
        line=aLine[0]
        cut=aLine[1]

        canvas = TCanvas("","");
        if logY:
            canvas.SetLogy()
            MAX=50
 
        leg= TLegend(0.11,0.6,0.57,0.89);
        if config.discovery:
            leg= TLegend(0.6,0.1,0.8,0.4);
        leg.SetTextSize( 0.03 );
        leg.SetTextFont( 42 );
        leg.SetFillColor( 0 );
        leg.SetFillStyle(1001);

        colors = [0,1,2,3,4,6,ROOT.kOrange,7,15,50,35,42,27,38,ROOT.kPink,45,56]*100
        counter=0

        allMyGraphs=[]
        missingFiles=[]

        for f in fileList:
            filename = f['filename']
            #print "OPEN: ",filename
            try:                
                textfile=open(filename)
            except:
                missingFiles.append(filename)
                print "WARNING: ",filename,"can't be found. skipped"        
                continue
           
            ana = filename.split("/")[-1]
            ana = ana.replace("_fixSigXSecNominal__1_harvest_list", "")
            if ana.find(config.grid) == -1:
                print "analysis %s does not contain grid %s, exiting to be safe" % (ana, config.grid)
                sys.exit()

            myPoints=[]
            graph = MyGraph(f['name'])
            for text in textfile.readlines():
                text = text.strip().split()
                UL = float(text[allpar.index("expectedUpperLimit")])
                #UL=float(text[allpar.index("CLsexp")])
                #UL=StatTools.GetSigma(float(text[allpar.index("CLsexp")]))
                xsec = float(text[allpar.index("xsec")])

                m0 = float(text[-4])#600
                m12 = float(text[-3])#50
                deltaM = m0-m12
                if UL <= 0: 
                    continue

                var=0
                if line=="d":
                    if deltaM != cut: 
                        continue
                    var=m0
                elif line=="h":
                    if m12 != cut:
                        continue
                    var=m0
                else:
                    if m0 != cut:
                        continue
                    var = m12
                    #print UL,m12,ana

                if var<MASSMIN: continue      
                if var>MASSMAX: continue

                graph.addPoint(var, UL, ana)
                c1 = TCanvas()
                graph.Draw()
                c1.SaveAs("graphs.eps")

            allMyGraphs.append(graph)
            textfile.close()

        counter=1
        print allMyGraphs
        firstGraph = allMyGraphs.pop(0)
        g = firstGraph.getTGraph(color=colors[counter])
        g.SetMaximum(MAX)
        g.SetMinimum(MIN)
        #g.SetMarkerStyle(25)
        
        g.GetXaxis().SetLimits(MASSMIN,MASSMAX)
        g.GetYaxis().SetTitle("#sigma_{excluded}/#sigma_{nominal}")

        xaxis="TOTO"
        if line == "h":
            xaxis = gridInfo[config.grid][0]            
            g.SetTitle(gridInfo[config.grid][1]+" = "+str(cut))
        if line == "v":
            xaxis=gridInfo[config.grid][1]            
            g.SetTitle(gridInfo[config.grid][0]+" = "+str(cut))
            
        leg.AddEntry(g, g.GetName(),"L")
        print g.GetName()
        g.Print()
        g.Draw("APL")

        for mg in allMyGraphs:
            counter+=1
            g=mg.getTGraph(color=colors[counter])
            if g == None:
                continue
           
            #g.GetXaxis().SetTitle(xaxis)
            leg.AddEntry(g, g.GetName(),"L")
            g.SetMarkerStyle(24)
            g.SetLineStyle(1)

            if g.GetName().find("meff ") == -1: #hack to see which is cut&count
                g.SetLineStyle(2)
            else:
                g.SetLineStyle(1)

            print g.GetName()
            g.Print()
            g.Draw("L")

        leg.Draw("same")
        value=1##0.05###1.64485
        tline=TLine(MASSMIN,value,MASSMAX,value)
        tline.SetLineStyle(2)
        tline.Draw()

        
        if config.grid=="SM_SS_direct":
            value2=1/8.
            tline2=TLine(MASSMIN,value2,MASSMAX,value2)
            tline2.SetLineStyle(2)
            tline2.Draw("same")

        
        canvas.Print(PLOTSDIR+"/"+config.grid+"_"+outputName+"_"+line+str(cut)+".eps")
        canvas.Print(PLOTSDIR+"/"+config.grid+"_"+outputName+"_"+line+str(cut)+".pdf")
        canvas.Print(PLOTSDIR+"/"+config.grid+"_"+outputName+"_"+line+str(cut)+".png")
        
        if len(missingFiles) > 0:
            print "##########################################################"
            print "##########################################################"
            print "##########################################################"
            print "# Missing files:                             "
            for file in missingFiles:
                print file
            print "##########################################################"

def MakePlots(config):

    listSuffix = "__1_harvest_list"
    if config.grid.find("LSP60") != -1:
        listSuffix = "__mlspEE60_harvest_list"
    elif config.grid.find("X05") != -1:
        listSuffix = "__mlspNE60_harvest_list"
    elif config.grid.find("M160") != -1:
        listSuffix = "__M1EE60_harvest_list"
    elif config.grid.find("M1M2") != -1:
        listSuffix = "__M1NE60_harvest_list"

    if config.discovery:
        listSuffix = "_discovery_1_harvest_list"
        
        
    from summary_harvest_tree_description import treedescription
    dummy,description = treedescription()
    allpar = description.split(':')

    canvas = TCanvas("","")
    canvas.SetLeftMargin(0.15)
    canvas.SetBottomMargin(0.15)

    gridName = config.grid
    suffix = ""
    
    if gridName.find("truth.Gluino_Stop_charm.dM") != -1:
        suffix = gridName.split(".")[-1]
        gridName = "Gluino_Stop_charm"

    frame = TH2F("frame", "", 100,gridInfo[gridName][2], gridInfo[gridName][3]
                     , 100, gridInfo[gridName][4], gridInfo[gridName][5] )

    allMyHists=[]

    ###set common frame style
    ###CombinationGlob::SetFrameStyle2D( frame, 1.0 ) // the size (scale) is 1.0  
    frame.SetXTitle( gridInfo[gridName][0])
    frame.SetYTitle( gridInfo[gridName][1] )
    frame.GetYaxis().SetTitleOffset(1.35)    
    frame.GetXaxis().SetTitleFont( 42 )
    frame.GetYaxis().SetTitleFont( 42 )
    frame.GetXaxis().SetLabelFont( 42 )
    frame.GetYaxis().SetLabelFont( 42 )        
    frame.GetXaxis().SetTitleSize( 0.05 )
    frame.GetYaxis().SetTitleSize( 0.05 )
    frame.GetXaxis().SetLabelSize( 0.05 )
    frame.GetYaxis().SetLabelSize( 0.05 )        
    frame.Draw()
    
    leg= TLegend(0.4,0.6,0.89,0.89);
    leg.SetTextSize( 0.03 );
    leg.SetTextFont( 42 );
    leg.SetFillColor( 0 );
    leg.SetFillStyle(1001);
   
    colors = [0,1,2,3,4,6,ROOT.kOrange,7,15,50,35,ROOT.kPink,45,56]
    counter = 0
    c_myExp = TColor.GetColor("#28373c")
    c_myYellow = TColor.GetColor("#ffe938")

    mycontours =[]
    
    for ana in config.anaList+["combined"]:#+["Paper13"]: 
    #for ana in ["combined_cutcount", "combined_5bin"]: #combine multiple by hand
        # the combined analysis always called "combined", if you want to change this 
        # look for more occurances in this script
        counter += 1
        filename = OUTPUTDIR+config.outputName+"_"+ana+"_fixSigXSecNominal"+listSuffix+".root"
        
        if not os.path.exists(filename):
            continue
        
        if config.match != "" and filename.find(config.match) == -1:
            continue
        
        if config.filter != "" and filename.find(config.filter) != -1: 
            continue

        print "MakeContours:", ana, filename
        file = TFile.Open(filename)
        hist = file.Get("p0exp" if config.discovery else "sigp1expclsf")
        
        if not hist:
            print "skip histo for ",ana
            continue

        contour = FixAndSetBorders( hist, ana, ana, 0 )
            
        linewidth = 4
        
        if counter >= len(colors):
            linestyle = 3
            counter=0
        else :
            linestyle = 1
            color = colors[counter]     
   
        if ana.find("combined") >= 0:
            linestyle = 1#counter#1
            linestyle_updown = 2
            color = c_myExp
            linewidth = 2
            legName = config.legend

            #get band
            if not config.discovery:
                contour_su1 = FixAndSetBorders( file.Get("sigclsu1s"), ana, ana, 0 )        
                contour_sd1 = FixAndSetBorders( file.Get("sigclsd1s"), ana, ana, 0 )
                h_su1 = DrawContourLine95(None, contour_su1, "up", color, linestyle_updown, linewidth)
                h_sd1 = DrawContourLine95(None, contour_sd1, "down", color, linestyle_updown, linewidth)
        else:
            legName = makeLegendName(ana, config.shape)

            #dirty hack for shape fit linestyle, to be automatised later
            if config.shape and gridName == "SM_SG_direct":
                #print legCompoents[0], metomeff, minbin
                if (legName.find("SRA") != -1 and legName.find("0.4") != -1 and legName.find("1000") != -1) or \
                   (legName.find("SRB") != -1 and legName.find("0.3") != -1 and legName.find("1700") != -1) or \
                   (legName.find("SRB") != -1 and legName.find("0.4") != -1 and legName.find("2300") != -1) or \
                   (legName.find("SRC") != -1 and legName.find("0.25") != -1 and legName.find("1200") != -1):
                    linestyle = 1
                else:
                    linestyle = 2

            if config.shape and gridName == "SM_SS_direct":
                if (legName.find("SRA") != -1 and legName.find("0.4") != -1 and legName.find("700") != -1) or \
                   (legName.find("SRA") != -1 and legName.find("0.4") != -1 and legName.find("1000") != -1) or \
                   (legName.find("SRA") != -1 and legName.find("15") != -1 and legName.find("1200") != -1) or \
                   (legName.find("SRC") != -1 and legName.find("0.3") != -1 and legName.find("1100") != -1):
                    linestyle = 1
                else:
                    linestyle = 2

            if config.shape and gridName == "SM_GG_direct":
                if (legName.find("SRC") != -1 and legName.find("0.3") != -1 and legName.find("800") != -1) or \
                   (legName.find("SRD") != -1 and legName.find("0.15") != -1 and legName.find("1500") != -1) or \
                   (legName.find("SRD") != -1 and legName.find("0.3") != -1 and legName.find("1300") != -1):
                    linestyle = 1
                else:
                    linestyle = 2

        leg_each= TLegend(0.4,0.75,0.9,0.9);
        leg_each.SetTextSize( 0.025 );
        leg_each.SetTextFont( 42 );
        leg_each.SetFillColor( 0 );
        leg_each.SetFillStyle(0000);

        hist.Draw("colz")
        leg_each.SetHeader(legName)
        DrawContourLine1sigma( leg_each, contour, '1#sigma discovery', ROOT.kGreen+3, 3, 2);
        DrawContourLine2sigma( leg_each, contour, '2#sigma discovery', ROOT.kBlue+1,  7, 2);
        DrawContourLine3sigma( leg_each, contour, '3#sigma discovery', ROOT.kRed+2,   1, 2);
        
        leg_each.Draw("same")
        frame.Draw("axis,same")        
        canvas.SaveAs(PLOTSDIR+"/"+config.outputName+"_"+ana+"_each.eps")

        if config.makeUL:
            local_canvas = TCanvas("local","local");
            local_canvas.SetLogz()
            frame.Draw()
            latex=TLatex()
            latex.SetTextSize(0.015)
            histUL = file.Get("expectedUpperLimit");             
            if not histUL:
                print "skip histo expectedUpperLimit for ",ana
                continue
            contourUL = FixAndSetBorders( histUL, ana, ana, 0 );

            level=array('d', [1])
            #contourUL.SetContour(len(level),level)            
            #contourUL.Draw("cont3") #colz")
            contourULbis=contourUL.Clone()
            for ix in range(1,contourULbis.GetNbinsX()+1):
                for iy in range(1,contourULbis.GetNbinsY()+1):
                    content=0
                    if contourULbis.GetBinContent(ix,iy):
                        content=1/contourULbis.GetBinContent(ix,iy)
                    contourULbis.SetBinContent(ix,iy,content)

                     
            level=array('d', [1])
            contourULbis.SetContour(len(level),level) 
            contourULbis.SetLineWidth(3)
            contourULbis.Draw("cont3") #colz")
            
            level=array('d', [4])
            contourUL4=contourULbis.Clone()
            contourUL4.SetLineColor(3)
            contourUL4.SetContour(len(level),level) 
            contourUL4.SetLineWidth(3)
            contourUL4.Draw("cont3,same") #colz")

            level=array('d', [8])
            contourUL8=contourULbis.Clone()
            contourUL8.SetLineColor(2)
            contourUL8.SetContour(len(level),level) 
            contourUL8.SetLineWidth(3)
            contourUL8.Draw("cont3,same") #colz")

            textfile=open(OUTPUTDIR+config.outputName+"_"+ana+"_fixSigXSecNominal__1_harvest_list")
            for line in textfile.readlines():
                line=line.strip().split()
                tt="%.2f" % float(line[allpar.index("expectedUpperLimit")])
                #tt="%.2f" % float(line[allpar.index("CLsexp")])
                latex.DrawText(float(line[-3]),float(line[-2]),tt)

                #print tt,"!!!!!!!!!!!!!!!!!!!!!!!!!"
                
            fakeleg= TLegend(0.2,0.6,0.95,0.89);
            #h = DrawContourLine95( fakeleg, contour, legName, 1, linestyle, linewidth );
            local_canvas.Print(PLOTSDIR+"/"+config.outputName+"_"+ana+".pdf")
            local_canvas.Print(PLOTSDIR+"/"+config.outputName+"_"+ana+".eps")
            local_canvas.Print(PLOTSDIR+"/"+config.outputName+"_"+ana+".png")

        
    box = TBox(200, 25, 900, 350)
    box.SetFillColor(0)
    box.SetLineColor(1)
    #box.Draw("same,L")
    
    frame.Draw("axis,same")

    canvas.Update()                
    canvas.Print(PLOTSDIR+"/"+config.outputName+".eps")
    canvas.Print(PLOTSDIR+"/"+config.outputName+".pdf")
    canvas.Print(PLOTSDIR+"/"+config.outputName+".png")

# Merge regions into combination based on best region (simply pick lowest p-value)
def Oring(config):
    # uncomment to easily see what you have to put in GetSRName.C
    #for indx,ana in enumerate(config.anaList):
        #print indx, ana

    #return

    import sys, os, string, shutil, pickle, subprocess    
    import ROOT

    from summary_harvest_tree_description import treedescription
    dummy,description = treedescription()
    allpar = description.split(':')

    ROOT.gROOT.Reset()
    ROOT.gROOT.SetBatch(True)

    # For all xsecs, merge on best selectpar (normally expected CLs)
    for xsecStr in allXS:
        myMap = {}

        if config.discovery and xsecStr != "Nominal":
            continue

        # if no UL's available, merge on CLsexp. Otherwise, use expectedUpperLimit
        selectpar = "CLsexp"
        if config.makeUL and xsecStr == "Nominal": # ULs only available for Nominal
            selectpar = "expectedUpperLimit"

        # select best SR based on p0exp    
        if config.discovery:
            selectpar = "p0exp"

        print "Using selectpar = %s" % selectpar

        par1_s = "m0"
        par2_s = "m12"
        par3_s = ""

        if config.grid.find("SM_GG_onestep")!=-1 or config.grid.find("GG_onestep")!=-1:
            print "Ordering SM_GG_onestep"
            par1_s = "mgluino"
            par2_s = "mchargino"
            par3_s = "mlsp"
        
        if config.grid.find("SM_GG_twostep_WWZZ")!=-1:
            print "Ordering SM_GG_twostep_WWZZ"
            par1_s = "mgluino"
            par2_s = "mchargino"
            par3_s = "mlsp"
        
        if config.grid.find("SM_SS_twostep_WWZZ")!=-1:
            print "Ordering SM_SS_twostep_WWZZ"
            par1_s = "msquark"
            par2_s = "mchargino"
            par3_s = "mlsp"

        if config.grid.find("SM_SS_onestep")!=-1:
            print "Ordering SM_SS_onestep"
            par1_s = "msquark"
            par2_s = "mchargino"
            par3_s = "mlsp"
        
        if config.grid.find("pMSSM_qL_to_h")!=-1:
            print "Ordering pMSSM_qL_to_h"
            par1_s = "M1"
            par2_s = "M2"
            par3_s = "msq"

        if config.grid.find("MUED")!=-1:
            print "Ordering mUED"
            par1_s = "LambdaR"
            par2_s = "oneOverR"
            par3_s = ""

        if config.grid.find("mssm")!=-1:
            par1_s = "mgl"
            par2_s = "msq"
            par3_s = "mlsp"


        listSuffix = "__1_harvest_list"
        if config.discovery:
            listSuffix = "_discovery_1_harvest_list"

        if config.grid.find("LSP60") != -1:
            listSuffix = "__mlspEE60_harvest_list"
        elif config.grid.find("X05") != -1:
            listSuffix = "__mlspNE60_harvest_list"
        elif config.grid.find("M160") != -1:
            listSuffix = "__M1EE60_harvest_list"
        elif config.grid.find("M1M2") != -1:
            listSuffix = "__M1NE60_harvest_list"

        infoFilename = OUTPUTDIR+config.outputName+"_combined_fixSigXSec"+xsecStr+listSuffix+"_infoFile"
        f_info = open(infoFilename,"w")
	   
        # make our own temporary inverse analist so that we can print short names below
        anaInvDict = {}
        '''
        for l in anaInvDictPaper13:
            anaInvDict[AnaConvert(l)] = anaInvDictPaper13[l]
        '''

        for indx,ana in enumerate(config.anaList):
            anaShortname = ana
            #if ana in anaInvDict:
            #    anaShortname = anaInvDict[ana]

            filename = OUTPUTDIR+config.outputName+"_"+ana+"_fixSigXSec"+xsecStr+listSuffix
            print filename
            infoline="%i : %s\n"%(indx+1,ana)
            f_info.write(infoline)
            if not os.path.exists(filename):
                print "file does not exist -> skip"
                continue
						
            f = open(filename,'r')
            for line in f.readlines():
                vals = line.strip().split(' ')
                if len(allpar) != len(vals): 
                    print 'PRB!!!!!!!!!!!!!!!!!!!!'
                    print "summary file says %d components; file has %d per line" % (len(allpar),len(vals))
                    continue
                
                vals[allpar.index("fID")]="%s"%(indx+1)
 
                pval = float( vals[allpar.index(selectpar)])
                par1 = float( vals[allpar.index(par1_s)])
                par2 = float( vals[allpar.index(par2_s)])
                key = "%d_%d" % (par1, par2)

                if config.grid.find("onestep")!=-1 or config.grid.find("pMSSM_qL")!=-1: 
                    par3 = float( vals[allpar.index(par3_s)])
                    key += "_%d" % par3
                if config.grid.find("mssm")!=-1: 
                    par3 = float( vals[allpar.index(par3_s)])
                    key += "_%d" % par3
           
                if pval < 0:#remove negative pvalue
                    print "INFO: %s removing negative selectpar (%s = %.2e) for %s" % (anaShortname, selectpar, pval, key)
                    continue 
	      
                #print "DEBUG: %s selectpar=%.2e for %s" % (anaShortname, pval, key)

                    
                if selectpar == "expectedUpperLimit" and pval < 0.00001:
                    print "INFO: %s removing %s < 0.00001 for %s" % (anaShortname, selectpar, key)
                    continue
               
                # 110 is 20 times our default step -> this is almost certainly a bug
                if selectpar == "expectedUpperLimit" and pval == 110.0:
                    print "INFO: %s removing expUL==110.0 for %s" % (anaShortname, key)
                    continue

                # if -1sig, -2sig == 0 and +1sig, 2sig == 100 -> almost certainly a bug too
                if selectpar == "expectedUpperLimit" and float(vals[allpar.index("expectedUpperLimitMinus1Sig")]) == 0.0 and float(vals[allpar.index("expectedUpperLimitMinus2Sig")]) == 0.0 and float(vals[allpar.index("expectedUpperLimitPlus1Sig")]) == 100.0 and float(vals[allpar.index("expectedUpperLimitPlus2Sig")]) == 100.0:
                    print "INFO: %s removing point %s with expULMinus1Sig == expULMinus2Sig == 0 and expULPlus1Sig == expULPlus2Sig == 100" % (anaShortname, key)
                    continue

                if selectpar == "expectedUpperLimit" and float(vals[allpar.index("upperLimit")]) == 0.0:
                    print "INFO: %s removing obsUL=0.0 for %s" % (anaShortname, key)
                    continue


                # throw away points with CLsexp > 0.99 and UL < 1.0 and CLs=-1 and UL<1 when merging on UL              		
                CLsExp = float( vals[allpar.index("CLsexp")])
                if selectpar == "expectedUpperLimit" and pval < 1.0 and (CLsExp>0.99 or CLsExp<0) and float( vals[allpar.index("upperLimit")])<1:                   
                    if CLsExp>0.99: print "INFO: %s replacing CLsexp with 0.01 since UL < 1.0  and CLsexp=1 for %s" % (anaShortname, key)
                    elif CLsExp<0: print "INFO: %s replacing CLsexp with 0.01 since UL < 1.0  and CLsexp=-1 for %s" % (anaShortname, key)
                    vals[allpar.index("CLsexp")] = str(0.01)
                    vals[allpar.index("CLs")] = str(0.01)
                    vals[allpar.index("clsu1s")] = str(0.01)
                    vals[allpar.index("clsd1s")] = str(0.01)
                    vals[allpar.index("p1")] = str(0.01)
                 
                
                newline=""
                for val in vals:
                    newline += val+" "
                newline = newline.rstrip(" ")
                newline += "\n"

                
                # float strings -> so make them float, then an int to throw away .0000 and then to bool
                failedcov =  bool(int(float(vals[allpar.index("failedcov")])))  # Mediocre cov matrix quality
                covqual = int(float(vals[allpar.index("covqual")]))             # covqual
                failedfit = bool(int(float(vals[allpar.index("failedfit")])))   # Fit failure
                failedp0 = bool(int(float(vals[allpar.index("failedp0")])))     # Base p0 ~ 0.5 (this can reject good fits)!
                fitstatus = bool(int(float(vals[allpar.index("fitstatus")])))   # Fit status from Minuit
                nofit = bool(int(float(vals[allpar.index("nofit")])))           # Whether there's a fit present
                
                if failedfit and 0:
                    print "INFO: %s removing failedfit=true for %s" % (anaShortname, key)
                    continue

                if failedcov and 0:
                    print "INFO: %s removing failedcov=true for %s" % (anaShortname, key)

                if covqual < 3 and covqual != -1 and 0:
                    print "INFO: %s removing check if (covqual<3 and covqual!=-1) for %s (found covqual=%d)" % (anaShortname, key, covqual)
                    continue
    
                key = (par1,par2)
                if config.grid.find("onestep")!=-1: 
                    key = (par1,par2,par3)
                if config.grid.find("pMSSM_qL")!=-1: 
                    key = (par1,par2,par3)
                if config.grid.find("mssm")!=-1:
                    key = (par1,par2,par3)
                
                if key not in myMap.keys():
                    myMap[key] = [pval,newline]
                else:
                    if pval < myMap[key][0] and pval>=0:
                        #print "DEBUG: %s found new best value - selectpar=%.2e < previous=%e for %s" % (anaShortname, pval, myMap[key][0], key)
                        myMap[key][0] = pval
                        myMap[key][1] = newline
            f.close()

        #print myMap
        combined_filename = OUTPUTDIR+config.outputName+"_combined_fixSigXSec"+xsecStr+listSuffix
        f = open(combined_filename,"w")
        for key,info in myMap.items():
            f.write(info[1])
        f.close()
        f_info.close()
        cmd="root -b -q \"$ZEROLEPTONFITTER/macros/contourplot/makecontourhists.C(\\\""+combined_filename+"\\\",\\\""+config.grid+"\\\")\""
        print cmd
        subprocess.call(cmd, shell=True)
        cmd="mv *_list.root "+OUTPUTDIR
        subprocess.call(cmd, shell=True)

def MakeATLASPlots(config) :
    listSuffix = "__1_harvest_list"
    if config.grid.find("LSP60") != -1:
        listSuffix = "__mlspEE60_harvest_list"
    elif config.grid.find("X05") != -1:
        listSuffix = "__mlspNE60_harvest_list"
    elif config.grid.find("M16") != -1:
        listSuffix = "__M1EE60_harvest_list"
    elif config.grid.find("M1M2") != -1:
        listSuffix = "__M1NE60_harvest_list"

    combined_filename = OUTPUTDIR+config.outputName+"_combined_fixSigXSecNominal"+listSuffix+".root"

    if config.grid == "SM_GG_onestep_LSP60" or config.grid == "SM_SS_onestep_LSP60": 
        plotMacro = "makecontourplots_onestep_LSP60.C"
    elif config.grid == "SM_GG_onestep_X05" or config.grid == "SM_SS_onestep_X05": 
        plotMacro = "makecontourplots_onestep_X05.C"
    elif config.grid == "pMSSM_qL_to_h_M160": 
        plotMacro = "makecontourplots_pMSSMqL.C"
    elif config.grid == "pMSSM_qL_to_h_M1M2": 
        plotMacro = "makecontourplots_pMSSMqL.C"
    elif config.grid.find("Gluino_Stop_charm") != -1 or config.grid.find("Gtt") != -1: 
        plotMacro = "makecontourplots_Gluino_Stop_charm.C"
    elif "SM_SS_direct" in config.grid or config.grid == "SM_GG_direct" or config.grid == "SM_SG_direct" or config.grid == "GG_direct" or config.grid == "SS_direct":
        plotMacro = "makecontourplots_direct.C"
    elif config.grid == "MUED" :
        plotMacro = "makecontourplots_MUED.C"
    elif config.grid == "NUHMG":
        plotMacro="makecontourplots_NUHMG.C"
    elif config.grid == "bRPV":
        plotMacro = "makecontourplots_bRPV.C"
    elif config.grid == "nGM":
        plotMacro = "makecontourplots_nGM.C"
    elif config.grid == "SM_TT_directCC":
        plotMacro="makecontourplots_SM_TT_directCC.C"
    else:
        print "There is no plotting macro defined for the grid %s" % (config.grid)
        return
    
    plotMacro = "%s/macros/contourplot/%s" % (os.getenv('ZEROLEPTONFITTER'), plotMacro)

    if not os.path.exists(plotMacro):
        print "Plotting macro %s appears to be missing!" % plotMacro
        return

    if plotMacro == "makecontourplots_direct.C":
        if config.grid == "SM_SS_direct" and combined_filename.find("nonDegenerate") == -1:
            # make the normal one first
            cmd="root -b -q \"%s(\\\"%s\\\", \\\"%s\\\", \\\"\\\", \"%s\", \"true\")\"" % (plotMacro, combined_filename, config.grid, str(config.shape).lower())
            print cmd
            subprocess.call(cmd, shell=True)
           
            # now the combined one
            grid_N2 = "SM_SS_direct_nonDegenerateSquarks_N2"
            grid_N4 = "SM_SS_direct_nonDegenerateSquarks_N4"
            grid_N8 = "SM_SS_direct_nonDegenerateSquarks_N8"

            filename_N2 = combined_filename.replace("SM_SS_direct", grid_N2)
            filename_N4 = combined_filename.replace("SM_SS_direct", grid_N4)
            filename_N8 = combined_filename.replace("SM_SS_direct", grid_N8)

            if not os.path.exists(filename_N2): filename_N2 = ""
            if not os.path.exists(filename_N4): filename_N4 = ""
            if not os.path.exists(filename_N8): filename_N8 = ""
           
            # combined plot has nominal and /8
            filename_N2 = ""
            filename_N4 = ""

            cmd="root -b -q \"%s(\\\"%s\\\", \\\"%s\\\", \\\"%s\\\", \"%s\", \"false\", \\\"%s\\\", \\\"%s\\\", \\\"%s\\\")\"" % (plotMacro, combined_filename, config.grid, "allXsec_", str(config.shape).lower(), filename_N2, filename_N4, filename_N8)
            print cmd
        elif config.grid == "SM_SS_direct":
            # don't show 7 TeV results for non degenerate squarks
            cmd="root -b -q \"%s(\\\"%s\\\", \\\"%s\\\", \\\"\\\", \"%s\", \"true\")\"" % (plotMacro, combined_filename, config.grid, str(config.shape).lower())
        else:
            cmd="root -b -q \"%s(\\\"%s\\\", \\\"%s\\\", \\\"\\\", \"%s\", \"true\")\"" % (plotMacro, combined_filename, config.grid, str(config.shape).lower())
            #cmd="root -b -q \"%s(\\\"%s\\\", \\\"%s\\\", \"%s\", \\\"\\\")\"" % (plotMacro, combined_filename, config.grid, str(config.shape).lower())
    
    else:
        cmd="root -b -q \"%s(\\\"%s\\\", \"%s\")\"" % (plotMacro, combined_filename, str(config.shape).lower())

    print cmd
    subprocess.call(cmd, shell=True)

###########################################################################
#Main
###########################################################################

def main():
    config = parseCmdLine(sys.argv[1:])

    anaList = []
    if config.opti and not config.shape:
        if config.grid == "SM_SS_direct":
            anaList = anaListOPTI_SS
            pass
        elif config.grid == "SM_GG_direct":
            anaList = anaListOPTI_GG
        elif config.grid == "Gluino_Stop_charm":
            anaList = anaListOPTI_Gluino_Stop_charm
        elif config.grid == "SM_SG_direct":
            anaList = anaListOPTI_SG
        elif config.grid == "MUED":
            anaList = anaListOPTI_MUED
        elif config.grid == "pMSSM_qL_to_h_M160" or "pMSSM_qL_to_h_M1M2":
            anaList = anaListOPTI_pMSSM

        elif config.grid == "SM_GG_onestep_LSP60":
            anaList = anaList_onestepPaper2013

        elif config.grid == "SM_GG_onestep_X05":
            anaList = anaList_onestepPaper2013

        elif config.grid == "SM_SS_onestep_LSP60":
            anaList = anaList_onestepPaper2013

        elif config.grid == "SM_SS_onestep_X05":
            anaList = anaList_onestepPaper2013
        elif config.grid == "Gtt":
            anaList = allChannelsDict.keys()
        elif config.grid == "GG_direct":
            anaList = ['SR4jAp', 'SR2jvt']
            
    elif config.opti and config.shape:
        if config.grid == "SM_SS_direct":
            anaList = anaListShape_SS
        elif config.grid == "SM_GG_direct":
            anaList = anaListShape_GG
        elif config.grid == "SM_SG_direct":
            anaList = anaListShape_SG
        elif config.grid.find("onestep") != -1:    
        # take only SRE for the onestep grids for now - SRA-D optimised using the others
            anaList = anaListShape_SRE

    if config.shape:
        #strip off the last two to be able to run AnaConvert and then append the shape part
        minBins = {}
        nBins = {}
        for idx, ana in enumerate(anaList):
            thisAna = ana.split(",")
         
            bins = thisAna.pop()
            minBin = thisAna.pop()
            thisStr = ",".join(thisAna)
            
            anaList[idx] = thisStr
            nBins[idx] = bins
            minBins[idx] = minBin

    config.anaList=anaList
    print config.anaList
    
    if config.shape:
        #reappend shape info 
        for (idx,ana) in enumerate(config.anaList):
            min = int(minBins[idx])*1000
            max = (int(minBins[idx])+1000)*1000
            ana += "-meffInc-nBins"+nBins[idx]+"-"+str(min)+"-"+str(max)
            config.anaList[idx] = ana

    if config.doMerge or config.doAll:
        MergeFiles(config)
        
    if config.makeContours or config.doAll:
        MakeContours(config)

    if config.doOring or config.doAll:
        Oring(config)
  
    if config.makePlots or config.doAll:
        MakePlots(config)

    if config.makeATLASplots or (config.doAll and 0):
        # tentaively turning off
        MakeATLASPlots(config)
    
    if (config.makeLines or config.doAll) and config.grid != "NUHMG" and config.grid != "SM_TT_directCC":
        if config.modeL == "all":
            config.modeL = "comb"
            MakeLines(config)
            config.modeL = "metsig"
            MakeLines(config)
            config.modeL = "metomeff"
            MakeLines(config)
            config.modeL = "nomeff"
            MakeLines(config)
        else:
            MakeLines(config)

    if config.compare:
        # GG
        if config.grid == "SM_GG_direct":
            list = [ 
            {"name": "SRC met/meff>0.3, meff 1300-2300", "filename": "Outputs/SM_GG_direct5bin_SRC-meff1600-metomeff0.3-met160-jet1pt130-jet2pt60-jet3pt60-jet4pt60-jet5pt0-jet6pt0-metSig0-dPhi0-meffInc-nBins5-1300000-2300000_fixSigXSecNominal__1_harvest_list"},
            {"name": "SRC met/meff>0.3, meff 1000-2000", "filename": "Outputs/SM_GG_direct5bin_SRC-meff1000-metomeff0.3-met160-jet1pt130-jet2pt60-jet3pt60-jet4pt60-jet5pt0-jet6pt0-metSig0-dPhi0-meffInc-nBins5-800000-1800000_fixSigXSecNominal__1_harvest_list"},
            {"name": "SRD met/meff>0.15, meff 1800-2800", "filename": "Outputs/SM_GG_direct5bin_SRD-meff1800-metomeff0.15-met160-jet1pt130-jet2pt60-jet3pt60-jet4pt60-jet5pt60-jet6pt0-metSig0-dPhi0-meffInc-nBins5-1800000-2800000_fixSigXSecNominal__1_harvest_list"},
            #
            {"name" : "SRC met/meff>0.3 meff>1000", "filename": "Outputs_Nikola_21fb/SM_GG_direct_SRC-meff1000-metomeff0.3-met160-jet1pt130-jet2pt60-jet3pt60-jet4pt60-jet5pt0-jet6pt0-metSig0-dPhi0_fixSigXSecNominal__1_harvest_list"},
            {"name" : "SRC met/meff>0.25, meff>2200", "filename": "Outputs_Nikola_21fb/SM_GG_direct_SRC-meff2200-metomeff0.25-met160-jet1pt130-jet2pt60-jet3pt60-jet4pt60-jet5pt0-jet6pt0-metSig0-dPhi0_fixSigXSecNominal__1_harvest_list"},
            {"name" : "SRD met/meff>0.2, meff>1600", "filename" : "Outputs_Nikola_21fb/SM_GG_direct_SRD-meff1600-metomeff0.2-met160-jet1pt130-jet2pt60-jet3pt60-jet4pt60-jet5pt60-jet6pt0-metSig0-dPhi0_fixSigXSecNominal__1_harvest_list"}
            ]
        
        # SG
        if config.grid == "SM_SG_direct":
            list = [
            {"name": "SRA, met/meff>0.4, meff 900-1900", "filename": "Outputs/SM_SG_direct5bin_SRA-meff1000-metomeff0.4-met160-jet1pt130-jet2pt60-jet3pt0-jet4pt0-jet5pt0-jet6pt0-metSig0-dPhi0-meffInc-nBins5-900000-1900000_fixSigXSecNominal__1_harvest_list"},
            {"name": "SRB, met/meff>0.3, meff 1700-2700", "filename" : "Outputs/SM_SG_direct5bin_SRB-meff1800-metomeff0.3-met160-jet1pt130-jet2pt60-jet3pt60-jet4pt0-jet5pt0-jet6pt0-metSig0-dPhi0-meffInc-nBins5-1700000-2700000_fixSigXSecNominal__1_harvest_list" },
            {"name": "SRB, met/meff>0.4, meff 2300-3000", "filename" : "Outputs/SM_SG_direct5bin_SRB-meff2200-metomeff0.4-met160-jet1pt130-jet2pt60-jet3pt60-jet4pt0-jet5pt0-jet6pt0-metSig0-dPhi0-meffInc-nBins5-2300000-3300000_fixSigXSecNominal__1_harvest_list"},
            {"name": "SRC, met/meff>0.25, meff 1200-2200", "filename" : "Outputs/SM_SG_direct5bin_SRC-meff1200-metomeff0.25-met160-jet1pt130-jet2pt60-jet3pt60-jet4pt60-jet5pt0-jet6pt0-metSig0-dPhi0-meffInc-nBins5-1200000-2200000_fixSigXSecNominal__1_harvest_list"},
            #
            {"name" : "SRB met/meff>0.3, meff>1800", "filename" : "Outputs_Nikola_21fb/SM_SG_direct_SRB-meff1800-metomeff0.3-met160-jet1pt130-jet2pt60-jet3pt60-jet4pt0-jet5pt0-jet6pt0-metSig0-dPhi0_fixSigXSecNominal__1_harvest_list"},
            {"name" : "SRB met/meff>0.4, meff>2200", "filename" : "Outputs_Nikola_21fb/SM_SG_direct_SRB-meff2200-metomeff0.4-met160-jet1pt130-jet2pt60-jet3pt60-jet4pt0-jet5pt0-jet6pt0-metSig0-dPhi0_fixSigXSecNominal__1_harvest_list"},
            {"name" : "SRC met/meff>0.25, meff>1200", "filename" : "Outputs_Nikola_21fb/SM_SG_direct_SRC-meff1200-metomeff0.25-met160-jet1pt130-jet2pt60-jet3pt60-jet4pt60-jet5pt0-jet6pt0-metSig0-dPhi0_fixSigXSecNominal__1_harvest_list"}
            ]
        
        #SS
        if config.grid == "SM_SS_direct":
            list = [
                {"name" : "SRA met/meff>0.4, meff 1000-2000", "filename" : "Outputs/SM_SS_direct5bin_SRA-meff1000-metomeff0.4-met160-jet1pt130-jet2pt60-jet3pt0-jet4pt0-jet5pt0-jet6pt0-metSig0-dPhi0-meffInc-nBins5-1000000-2000000_fixSigXSecNominal__1_harvest_list"},
                {"name" : "SRA met/meff>0.4, meff 700-1700", "filename" : "Outputs/SM_SS_direct5bin_SRA-meff1000-metomeff0.4-met160-jet1pt130-jet2pt60-jet3pt0-jet4pt0-jet5pt0-jet6pt0-metSig0-dPhi0-meffInc-nBins5-700000-1700000_fixSigXSecNominal__1_harvest_list"},
                {"name" : "SRA metsig>15, meff 11000-2100", "filename" : "Outputs/SM_SS_direct5bin_SRA-meff1200-metomeff0-met160-jet1pt130-jet2pt60-jet3pt0-jet4pt0-jet5pt0-jet6pt0-metSig15-dPhi0-meffInc-nBins5-1100000-2100000_fixSigXSecNominal__1_harvest_list"},
                {"name" : "SRA metsig>15, meff 1200-2200", "filename" : "Outputs/SM_SS_direct5bin_SRA-meff1200-metomeff0-met160-jet1pt130-jet2pt60-jet3pt0-jet4pt0-jet5pt0-jet6pt0-metSig15-dPhi0-meffInc-nBins5-1200000-2200000_fixSigXSecNominal__1_harvest_list"},
                {"name" : "SRC met/meff>0.3, meff 1000-2000", "filename" : "Outputs/SM_SS_direct5bin_SRC-meff1000-metomeff0.3-met160-jet1pt130-jet2pt60-jet3pt60-jet4pt60-jet5pt0-jet6pt0-metSig0-dPhi0-meffInc-nBins5-1000000-2000000_fixSigXSecNominal__1_harvest_list"},
            #
                {"name" : "SRA metsig>15, meff>1200", "filename" : "Outputs_Nikola_21fb/SM_SS_direct_SRA-meff1200-metomeff0-met160-jet1pt130-jet2pt60-jet3pt0-jet4pt0-jet5pt0-jet6pt0-metSig15-dPhi0_fixSigXSecNominal__1_harvest_list"},
                {"name" : "SRA metsig>15, meff>1400", "filename" : "Outputs_Nikola_21fb/SM_SS_direct_SRA-meff1400-metomeff0-met160-jet1pt130-jet2pt60-jet3pt0-jet4pt0-jet5pt0-jet6pt0-metSig15-dPhi0_fixSigXSecNominal__1_harvest_list"},
                {"name" : "SRC met/meff>0.3 meff>1000", "filename": "Outputs_Nikola_21fb/SM_SS_direct_SRC-meff1000-metomeff0.3-met160-jet1pt130-jet2pt60-jet3pt60-jet4pt60-jet5pt0-jet6pt0-metSig0-dPhi0_fixSigXSecNominal__1_harvest_list"}
            ]
        if config.grid == "SM_GG_onestep_LSP60":
              list = [{"name" : "Current-0lepton combined", "filename" : "Outputs_0lepton/SM_GG_onestep_LSP60_combined_fixSigXSecNominal__mlspEE60_harvest_list"},{"name" : "With Wfinder combined", "filename" : "Outputs_Wfinder/SM_GG_onestep_LSP60_combined_fixSigXSecNominal__mlspEE60_harvest_list"}]


        CompareLines(config, list, "cc_vs_5bin")

if __name__ == "__main__":
    main()
