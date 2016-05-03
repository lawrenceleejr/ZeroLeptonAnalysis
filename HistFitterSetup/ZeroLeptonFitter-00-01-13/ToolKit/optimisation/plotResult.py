#!/usr/bin/env python

# Tool to plot optimisation results
# Note: part of the functionality herein needs to go to ContourUtils

import argparse
import copy
import datetime
import glob
import json
import operator
import os
import subprocess
import sys

if os.getenv('ZEROLEPTONFITTER') is None:
    print("Setup ZeroLeptonFitter first!")
    sys.exit()

from pprint import pprint

from zerolepton.colors import colors
from zerolepton.grids.config import GridConfig

from zerolepton.plotting.optimisationplot import OptimisationPlot

from zerolepton.contours.data import ContourData, OptimisationCut
from zerolepton.contours.utils import getFileList, createPlainTextListFileFromJSON
from zerolepton.contours.utils import groupFilesByRegion, mergeFilesByRegion, createListFileForRegion
from zerolepton.contours.histmaker import HistMaker

def findFileAndDirname(args):
    if args.filename != "" and os.path.exists(args.filename) and os.path.isdir(args.filename):
        args.outputdir = copy.deepcopy(args.filename)
        args.filename = ""

    # If we have a filename, look whether ZLF/name.json exists, if not, ZLF/name/name.json. The dir is assumed to be ZLF/name
    filename = args.filename
    dirname = os.path.abspath(args.outputdir)
    ZLF = os.getenv('ZEROLEPTONFITTER')

    searchDirs = [os.path.join(ZLF, dirname), dirname, args.outputdir]

    if filename == "":
        found = False
        dirname = None
        for d in searchDirs:
            if not os.path.exists(d) or not os.path.isdir(d): continue
            found = True
            dirname = d

        if not found:
            print("The output directory {0} does not exist".format(args.outputdir))
            sys.exit()

        filename = os.path.join(dirname, "{0}.json".format(os.path.basename(os.path.abspath(dirname))))

    if dirname == "":
        (dirname, ext) = os.path.splitext(os.path.basename(filename))
        dirname = os.path.join(ZLF, dirname)

        if not os.path.exists(filename):
            # file is probably relative in this case
            filename = os.path.join(dirname, filename)

    return (filename, dirname)

def extractData(filename):
    with open(filename) as f:
        data = json.load(f)

    print("Plotting for regions generated with:")
    print("{0}".format(data['argv']))
    print("Generated at: %s" % datetime.datetime.fromtimestamp(data['timestamp']).strftime("%d/%m/%Y, %H:%M:%S"))

    regions = []
    for (cutStr, name, cmd) in data['commands']:
        regions.append(name)

    return (data['grid'], set(regions))

def regionsToCutString(filename, regions):
    with open(filename) as f:
        data = json.load(f)

    retval = {}
    for (cutStr, name, cmd) in data['commands']:
        if name not in regions: continue
        retval[name] = cutStr

    return retval

def createContours(gridConfig, regions, outputDir):
    N = len(regions)
    i = 0
    missingFiles = {}
    for r in regions:
        i += 1
        if not createListFileForRegion(gridConfig, r, outputDir):
            filePrefix = "{0}_{1}".format(r, gridConfig.name)
            filename = os.path.join(outputDir, "{0}.root".format(filePrefix))
            missingFiles[r] = filename

        #createHistogramForRegion(gridConfig, r, outputDir)
        print(colors.OKGREEN + "Finished region {0} / {1}".format(i, N) + colors.ENDC)
    return missingFiles
    
def createHistogramForRegion(gridConfig, region, outputDir):
    # reconstruct the list file output name
    filePrefix = "{0}_{1}".format(region, grid)
    filename = os.path.join(outputDir, filePrefix)
    if gridConfig.useDiscovery:
        filename += gridConfig.listSuffix_discovery
    else:
        filename += gridConfig.listSuffix

    filenameJSON = "{0}.json".format(filename)

    if not os.path.exists(filename) and not os.path.exists(filenameJSON):
        print("createContourForRegion: neither {0} nor its JSON file exist".format(filename))
        return
    
    summaryName = os.path.join(outputDir, "summary_harvest_tree_description.py")
    if not os.path.exists(filename) or os.path.getmtime(filename) < os.path.getmtime(filenameJSON) or not os.path.exists(summaryName):
        # build it from the JSON file
        print("createContourForRegion: attempting to generate old-fashioned list from JSON output {0}".format(filenameJSON))
        createPlainTextListFileFromJSON(filenameJSON, filename)

    # Now build the histogram
    basename = os.path.basename(filename)
    dirname = os.path.dirname(os.path.abspath(filename))
    
    histMaker = HistMaker(inputFilename=filename, interpretation=gridConfig.interpretation, outputDir=dirname)
    # add additional histograms here if needed
    histMaker.addHistogram(variable="p0exp", name="p0exp", title="Expected p0", cuts="p0>=0 && p0<=1")
    histMaker.process()

    pass

####################
# Main script here
####################

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", default="", type=str)
parser.add_argument("-o", "--outputdir", default="", type=str, help="output dir of the optimisation results")
parser.add_argument("-e", "--exclusion", default=False, action="store_true")
parser.add_argument("-s", "--skip-create", default=False, action="store_true", help="Skip merging output files and hypotest->list conversion. Useful if you just have a dir with json files.")
args = parser.parse_args()

if args.filename == "" and args.outputdir == "":
    print("Cannot run without ither a filename or the output dir")
    sys.exit()

if args.exclusion:
    discovery = False
    print("Running in exclusion mode")
else:
    discovery = True
    print("Running in discovery mode")

(filename, dirname) = findFileAndDirname(args)

print("Constructed filename as {0}".format(filename))
print("Constructed dirname as {0}".format(dirname))

try:
    assert(os.path.exists(filename))
except:
    print("Input JSON filename {0} cannot be found.".format(filename))
    sys.exit()
    
try:
    assert(os.path.exists(dirname))
except:
    print("Input directory {0} cannot be found.".format(dirname))
    sys.exit()

resultsDir = os.path.join(dirname, "results")
outputDir = os.path.join(dirname, "Output")
if not os.path.exists(outputDir): os.makedirs(outputDir)

if not args.skip_create:
    files = getFileList(resultsDir, cachefile = os.path.join(dirname, "results.cache"), noWait=True)

(grid, regions) = extractData(filename)
gridConfig = GridConfig(grid, discovery)

print("Found {0} regions in optimisation file".format(len(regions)))

regionNameDump = os.path.join(outputDir, "filesByRegion.json")
if os.path.exists(regionNameDump):
    with open(regionNameDump) as f:
        filesByRegion = json.load(f)
else:
    filesByRegion = groupFilesByRegion(files, regions)
    with open(regionNameDump, "w") as f:
        json.dump(filesByRegion, f) 

if not args.skip_create:
    mergeFilesByRegion(filesByRegion, grid, outputDir)
    missingFiles = createContours(gridConfig, regions, outputDir)

    if len(missingFiles) > 0:
        regionsToCutStrings = regionsToCutString(filename, missingFiles.keys())
        print("WARNING: the following {0} input files were not found".format(len(missingFiles)))
        for r in missingFiles: 
            print ("\t{0}".format(missingFiles[r]))
        print("That are these cuts:")
        for r in missingFiles: 
            print ("\t{0}".format(regionsToCutStrings[r]))
        
        if(len(missingFiles) > 10):
            # too much. dump and exit.
            filenameRerun, ext = os.path.splitext(os.path.basename(filename))
            filenameRerun = os.path.join(os.getenv('ZEROLEPTONFITTER'), "{0}-MISSING{1}".format(filenameRerun,ext))
            with open(filenameRerun, "w") as f:
                json.dump(regionsToCutStrings, f)
            print(colors.FATAL + "Too many missing files" + colors.ENDC)
            print("You're missing so many files that I wrote the missing cutstrings to {0}. Rerun these!".format(filenameRerun))
            sys.exit()

plotFilename = os.path.join(dirname, "plots", os.path.splitext(os.path.basename(filename))[0] + ".pdf")
optimisationPlot = OptimisationPlot(gridConfig, plotFilename, outputDir)
optimisationPlot.write()

# write combined data to a file
combinedFilename = os.path.join(outputDir, "combined_{0}{1}".format(gridConfig.name, gridConfig.getSuffix()))
combinedFilenameJSON = "{0}.json".format(combinedFilename)
try:
    # no default return for max() in case of empty list 
    lastFile = max(glob.iglob(os.path.join(outputDir,'SR*.json')), key=os.path.getmtime)
except:
    lastFile = None
if not os.path.exists(combinedFilenameJSON) or (lastFile and os.path.getmtime(combinedFilenameJSON) < os.path.getmtime(lastFile)):
    optimisationPlot.contourData.writeCombinedData(combinedFilenameJSON)

optimisationPlot.writeContour()

# # write to TH2D 
# if os.path.exists(combinedFilenameJSON) and not os.path.exists(combinedFilename) or os.path.getmtime(combinedFilename) < os.path.getmtime(combinedFilenameJSON):
#     createPlainTextListFileFromJSON(combinedFilenameJSON, combinedFilename)
# histMaker = HistMaker(inputFilename=combinedFilename, interpretation=gridConfig.interpretation, outputDir=outputDir)
# histMaker.addHistogram(variable="p0exp", name="p0exp", title="Expected p0", cuts="p0>=0 && p0<=1")

# combinedFilenameROOT = "{0}.root".format(combinedFilename)
# if not os.path.exists(combinedFilenameROOT) or os.path.getmtime(combinedFilenameROOT) < os.path.getmtime(combinedFilename):
#     histMaker.process()
# else:
#     print "Output file {0} already exists and is newer; not overwriting".format(combinedFilenameROOT)
