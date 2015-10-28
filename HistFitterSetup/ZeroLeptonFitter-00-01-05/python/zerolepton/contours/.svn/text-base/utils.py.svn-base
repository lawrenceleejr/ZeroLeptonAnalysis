# Utility functions for hypothesis test files and contour plotting

import ConfigParser
import json
import os
import shutil
import subprocess
import sys
import time

from ..utils import wait, chunks
from .listmaker import ListMaker

from copy import copy

from collections import namedtuple
from collections import OrderedDict

from functools import partial
from multiprocessing.dummy import Pool

def buildCutString(cuts):
    # helper to ensure we alwasy have the same order. bit ugly.
    variables = ["nJets", "MET", "jetpt1", "jetpt2", "jetpt3", "jetpt4", "jetpt5", "jetpt6", "jetpt7", "dPhi", "dPhiR", "aplanarity", "MET_over_meffNj", "meffIncl", "METsig"]

    myCuts = []
    for var in variables:
        if not var in cuts or cuts[var] == 0: continue

        if isinstance(cuts[var], float):
            nDigits = 3
            if var == "MET": nDigits = 0
            if "jetpt" in var: nDigits = 0
            if "meffIncl" in var: nDigits = 0

            # yes, you want those round calls. otherwise some funky float->string conversion can occur (0.399 instead of 0.4)
            if nDigits == 0:
                s = "{0}:{1:0f}".format(var, round(cuts[var], nDigits))
            else:
                s = "{0}:{1:3f}".format(var, round(cuts[var], nDigits))
        elif isinstance(cuts[var], int):
            s = "{0}:{1:d}".format(var, cuts[var])

        myCuts.append(s)

    return ",".join(myCuts)

def getFileList(inputdir, cachefile = os.getenv("ZEROLEPTONFITTER")+"/macros/contourplot/results.cache", noWait=False):
    readDir = False

    if cachefile is not None and os.path.exists(cachefile) and os.path.isfile(cachefile):
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
        print "Found %d files or directories, reading them all..." % len(dirnames)
        for d in dirnames:
            sys.stdout.write('%d / %d \r' % (i, len(dirnames)))
            sys.stdout.flush()

            n = os.path.join(inputdir, d)

            if not os.path.isdir(n):
                filenames.append(n)
                continue

            fnames = os.listdir(n)
            for f in fnames:
                filenames.append(os.path.join(inputdir, d, f))
            i+=1

        if cachefile is not None:
            f = open(cachefile, "w")
            for n in filenames:
                f.write("%s\n" % n)
            f.close()
    else:
        print "INFO: read %d lines from %s (file modified: %s)" % (len(filenames), cachefile, time.ctime(os.path.getmtime(cachefile)))
        if not noWait:
            print "Waiting 3 seconds in case this is not correct and you want to delete the file..."
            wait(3)

    return filenames

def makeProgressString(percent, barLen):
    progress = ""
    for i in range(barLen):
        if i < int(barLen * percent):
            progress += "="
        else:
            progress += " "
    return progress

def drawProgressBar(i, N, barLen = 20):
    percent = float(i)/N
    suffix = "{:10d}/{:d}".format(i, N)

    sys.stdout.write("\r")
    sys.stdout.write("[ %s ] %.2f%% %s" % (makeProgressString(percent, barLen), percent * 100, suffix))
    sys.stdout.flush()

def groupFilesByRegion(files, regions):
    # I group files in a dir by region

    print "Grouping files by region - this can take a while for larger directories..."
    filesByRegion = {}
    for r in regions:
        filesByRegion[r] = []
   
    os.system('setterm -cursor off')

    # inverted loops - this is faster
    N = len(files)
    i = 0
    for f in files:
        i += 1
        drawProgressBar(i, N, 30)
        
        # we are only interested in comparing stuff that actually is a hypotest
        if not f.endswith(".root"): continue
        if not "hypotest" in f and not "upperlimit" in f: continue
       
        for r in regions:
            if r in f:
                filesByRegion[r].append(f)
                break # a file can only below to one region

    print("")
    os.system('setterm -cursor on')

    splitKeys = ["Nominal", "Down", "Up", "upperlimit"]
    emptyDict = {}
    for k in splitKeys:
        emptyDict[k] = []

    retval = {}
    for r, files in filesByRegion.iteritems():
        d = {}
        for k in splitKeys:
            if k != "upperlimit":
                d[k] = [f for f in files if k in f and not "upperlimit" in f]
            else:
                d[k] = [f for f in files if k in f]

        if d == emptyDict:
            continue
        retval[r] = d

    return retval

def mergeFilesByRegion(filesByRegion, grid, outputDir):
    # Merge a set of files by region into the specified dir
    # Key is up/down/nominal etc
    N = 0 
    for r in filesByRegion:
        for key in filesByRegion[r]:
            if filesByRegion[r][key] == []: continue
            N += 1 

    for r in filesByRegion:
        for key in filesByRegion[r]:
            if filesByRegion[r][key] == []: continue

            N -= 1 

            # Merge the files in chunks of 50, and then merge these chunks

            # The whole idea behind this exercise is to avoid exceeding the maximum length of
            # of a command allowed in bash.

            outputFiles = []
            filePrefix = "%s_%s" % (r, grid)

            filename = os.path.join(outputDir, "%s.root" % (filePrefix) )
            if os.path.exists(filename):
                print("Output file {0} exists - skipping".format(os.path.basename(filename)))
                continue

            i=1
            for subset in chunks(filesByRegion[r][key], 50):
                print("Merging subset {0:d}...".format(i))
                filename = os.path.join(outputDir, "%s_%03d.root" % (filePrefix, i) )
                outputFiles.append(filename)

                if len(subset) == 1:
                    shutil.copy(subset[0], filename)
                else:
                    cmd = "hadd -f %s %s" % (filename, " ".join(subset))
                    subprocess.call(cmd, shell=True)

                i+=1

            print("Merging all subsets")
            filename = os.path.join(outputDir, "%s.root" % (filePrefix) )

            if len(outputFiles) == 1:
                # only 1 file, so just rename it
                os.rename(outputFiles[0], filename)
            else:
                cmd = "hadd -f %s %s" % (filename, " ".join(outputFiles))
                subprocess.call(cmd, shell=True)

            print("Done merging subsets; removing temporary files")
            for f in outputFiles:
                if not os.path.exists(f): continue
                os.remove(f)

            print("=> Created file for {0}; {1} files remaining".format(r, N))

def createListFileForRegion(gridConfig, region, outputDir):
    # Create the HistFitter list files for the specified region
    filePrefix = "{0}_{1}".format(region, gridConfig.name)
    filename = os.path.join(outputDir, "{0}.root".format(filePrefix))

    if not os.path.exists(filename) or not os.path.isfile(filename):
        print("createListFileForRegion: input {0} is not a file".format(filename))
        return

    # Does our output exist?
    outputFilename = filename.replace('.root','')
    if gridConfig.useDiscovery:
        outputFilename += gridConfig.listSuffix_discovery + ".json"
    else:
        outputFilename += gridConfig.listSuffix + ".json"
    if os.path.exists(outputFilename):
        print("Output {0} exists - skipping".format(os.path.basename(outputFilename)))
        return

    print("createListFileForRegion: using input file {0}".format(filename))

    fmt = gridConfig.format
    if gridConfig.useDiscovery:
        fmt = gridConfig.format_discovery

    listMaker = ListMaker(inputFilename=filename, interpretation=gridConfig.interpretation, format=fmt, cutStr=gridConfig.cutStr, outputDir=outputDir)
    listMaker.automaticRejection = False 
    if gridConfig.useDiscovery:
        listMaker.prefix = "discovery"

    listMaker.writeList()

    pass

def createPlainTextListFileFromJSON(filename, outputFilename = None):
    from GenerateTreeDescriptionFromJSON import writeListFile

    if outputFilename is None or outputFilename == "":
        # strip off .json for the output file
        outputFilename = copy(filename).replace(".json", "")

    if outputFilename == filename:
        raise ValueError(" Would overwrite input file! Make sure it ends in .json")

    writeListFile(filename, outputFilename)
