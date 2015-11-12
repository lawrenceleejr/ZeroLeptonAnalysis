# Utility functions for hypothesis test files and contour plotting

import ConfigParser
import json
import os
import signal
import shutil
import subprocess
import sys
import time

import ROOT
ROOT.gROOT.SetBatch(True)

from ..utils import wait, chunks
from .listmaker import ListMaker

from copy import copy

from collections import namedtuple
from collections import OrderedDict

from functools import partial
from multiprocessing.dummy import Pool as ThreadPool 

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
        i=0
        print "Found %d files or directories, reading them all..." % len(dirnames)
        for d in dirnames:
            i+=1
            sys.stdout.write('%d / %d \r' % (i, len(dirnames)))
            sys.stdout.flush()

            n = os.path.join(inputdir, d)

            if not os.path.isdir(n):
                filenames.append(n)
                continue

            fnames = [os.path.join(inputdir, d, f) for f in os.listdir(n)]
            filenames.extend(fnames)

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

def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def mergeFilesByRegion(filesByRegion, grid, outputDir):
    # Merge a set of files by region into the specified dir
    # Key is up/down/nominal etc
    N = 0
    filesToWrite = {}
    for r in filesByRegion:
        for key in filesByRegion[r]:
            if filesByRegion[r][key] == []: 
                if key == "Nominal":
                    print("WARNING: no input files for region {0} key {1}".format(r, key))
                continue
            
            filePrefix = "%s_%s" % (r, grid)
            filename = os.path.join(outputDir, "%s.root" % (filePrefix) )
            if os.path.exists(filename):
                print("Output file {0} exists - skipping".format(os.path.basename(filename)))
                continue
            
            filesToWrite[filename] = {"region" : r, "files" : filesByRegion[r][key]}
            N += 1 

    # Got anything?
    if filesToWrite == {}:
        return

    # build the pool arguments
    args = []
    for filename in filesToWrite:
        N -= 1
        args.append((filename, filesToWrite[filename]['files'], False, filesToWrite[filename]['region'], N,))
    
    pool = ThreadPool(8, init_worker) 
    try:
        #results = pool.map(mergeFiles, args)
        results = pool.imap_unordered(mergeFiles, args)
        pool.close() 
        pool.join() 
    except KeyboardInterrupt:
        print "Caught KeyboardInterrupt, terminating workers"
        pool.terminate()
        pool.join()

    return

    # Below is to be removed legacy code relying on hadd

    for r in filesByRegion:
        for key in filesByRegion[r]:
            if filesByRegion[r][key] == []: continue

            N -= 1 

            # Merge the files in chunks of 50, and then merge these chunks

            # The whole idea behind this exercise is to avoid exceeding the maximum length of
            # of a command allowed in bash.

            filePrefix = "%s_%s" % (r, grid)
            filename = os.path.join(outputDir, "%s.root" % (filePrefix) )
            if os.path.exists(filename):
                print("Output file {0} exists - skipping".format(os.path.basename(filename)))
                continue

            mergeFiles(filename, filesByRegion[r][key])
            
            #fileMerger = ROOT.TFileMerger()
            #fileMerger.OutputFile(filename)
            #for f in filesByRegion[r][key]:
            #    fileMerger.AddFile(f)
            #fileMerger.Merge()

            #i=1
            #print("Attempting to make file {0}".format(filename))
            #for subset in chunks(filesByRegion[r][key], 50):
            #    print("Merging subset {0:d}...".format(i))
            #    filename = os.path.join(outputDir, "%s_%03d.root" % (filePrefix, i) )
            #    outputFiles.append(filename)
            #
            #    if len(subset) == 1:
            #        shutil.copy(subset[0], filename)
            #    else:
            #        cmd = "hadd -f %s %s" % (filename, " ".join(subset))
            #        subprocess.call(cmd, shell=True)
            #
            #    i+=1

            #print("Merging all subsets")
            #filename = os.path.join(outputDir, "%s.root" % (filePrefix) )

            #if len(outputFiles) == 1:
            #    # only 1 file, so just rename it
            #    os.rename(outputFiles[0], filename)
            #else:
            #    cmd = "hadd -f %s %s" % (filename, " ".join(outputFiles))
            #    subprocess.call(cmd, shell=True)

            #print("Done merging subsets; removing temporary files")
            #for f in outputFiles:
            #    if not os.path.exists(f): continue
            #    os.remove(f)

            print("=> Created file for {0}; {1} files remaining".format(r, N))

def mergeFiles(args):
    _mergeFiles(*args)

def _mergeFiles(outputFilename, inputFilenames, ignoreDuplicates=False, label="", remaining=0):
    #print("Merging {0} from inputs {1}".format(outputFilename, ", ".join(inputFilenames)))

    if label == "":
        label = os.path.basename(outputFilename)

    # The output file cannot be one of the input files
    for n in inputFilenames:
        if not os.path.exists(n) or os.path.abspath(outputFilename) == os.path.abspath(n):
            inputFilenames.remove(n)
    
    # Anything left?
    if len(inputFilenames) == 0: return

    # Start with a copy of the first file
    firstFile = inputFilenames.pop()
    shutil.copyfile(firstFile, outputFilename)
    
    # Nothing left - exit
    if len(inputFilenames) == 0:
        print("=> Created file for {0}; {1} files remaining".format(label, remaining))
        return
    
    # We now have the output file that we have to update
    fOut = ROOT.TFile(outputFilename, "UPDATE")
    processedKeys = []
    if ignoreDuplicates: 
        processedKeys = f.GetListOfKeys() # the keys of the first file are the ones we processed
    for n in inputFilenames:
        f = ROOT.TFile(n, "READ")
        f.cd()

        keys = f.GetListOfKeys()
        objects = []

        # Read all the objects from this file
        for k in keys:
            name = k.GetName()
            if "Process" in name: continue # boring
            if ignoreDuplicates and name in processedKeys: 
                print "mergeFiles(): {0}: skipping duplicate {1}".format(n, name)
                continue
            objects.append(f.Get(name))

        # Now write all the objects
        fOut.cd()
        for obj in objects:
            obj.Write()
            if ignoreDuplicates: 
                processedKeys.append(obj.GetName())
            del obj

        f.Close()

    fOut.Close()
    print("=> Created file for {0}; {1} files remaining".format(label, remaining))

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
        print("createListFileForRegion: output {0} exists - skipping".format(os.path.basename(outputFilename)))
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
