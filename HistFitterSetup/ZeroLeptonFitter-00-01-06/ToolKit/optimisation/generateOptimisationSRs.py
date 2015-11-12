#!/usr/bin/env python

import argparse
import datetime
import itertools
import json
import math
import os
import socket
import sys
import textwrap
import time

if os.getenv("ZEROLEPTONFITTER") is None:
    print("Cannot run without ZeroLeptonFitter setup!")
    sys.exit()

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

from copy import copy
from pprint import pprint

from ChannelConfig import createChannelConfigFromString
#from ContourUtils import buildCutString
#from Utils import chunks
#from Utils import cartesian_product
from zerolepton.utils import chunks
from zerolepton.utils import cartesian_product
from zerolepton.contours.utils import buildCutString

from zerolepton.colors import colors

# simple script to generate a list of optimisation commands that would get run
# we take a set of passed cuts and generate a command from it

# example command:
# ./generateOptimisationSRs.py --grid=SM_GG_direct --point 1350_250 --nJets 2 --MET 200 --jetpt1 200 300 --jetpt2 200 300 --jetpt3 60 100 150 --jetpt4 60 100 150 --dPhi123 0.4 0.8 1.2 --aplanarity 0.02 --METovermeffNj 0.2 0.25 0.3 --meff 800 1000 1200 1400

# NOTE: new variables must always be added to zerolepton.contours.utils' buildCutString() method!

def loadGridPoints(grid):
    import pickle
    with open(os.path.join(os.getenv("ZEROLEPTONFITTER"), "ToolKit", "signalPointPickle.pkl"), "rb") as f:
        pointDict = pickle.load(f)

    if not grid in pointDict:
        print("Grid name {0} not in points dictionary".format(grid))
        sys.exit()

    return pointDict[grid].values()

parser = argparse.ArgumentParser()
parser.add_argument("--grid", default=None, type=str)
parser.add_argument("--point", default=[], type=str, action='append')
parser.add_argument("--pointsPerCommand", default=10, type=int)
parser.add_argument("--entire-grid", default=False, action="store_true", help="use entire grid")
parser.add_argument("--outputSuffix", default="", type=str, help="output filename suffix. A timestamp is used by default.")
parser.add_argument('--mode', choices=['discovery', 'exclusion', 'exclusionUL', 'all'], default='discovery', help="Run discovery, exclusion or exclusion ULs to optimise")
parser.add_argument("--nJets", default=[2], type=int, nargs='+')
parser.add_argument("--MET", default=[200], type=float, nargs='+')
parser.add_argument("--jetpt1", default=[200], type=float, nargs='+')
parser.add_argument("--jetpt2", default=[200], type=float, nargs='+')
parser.add_argument("--jetpt3", default=[0], type=float, nargs='+')
parser.add_argument("--jetpt4", default=[0], type=float, nargs='+')
parser.add_argument("--jetpt5", default=[0], type=float, nargs='+')
parser.add_argument("--jetpt6", default=[0], type=float, nargs='+')
parser.add_argument("--jetpt7", default=[0], type=float, nargs='+')
parser.add_argument("--dPhi", default=[0.4], type=float, nargs='+')
parser.add_argument("--dPhiR", default=[0], type=float, nargs='+')
parser.add_argument("--aplanarity", default=[0], type=float, nargs='+')
parser.add_argument("--MET_over_meffNj", default=[0], type=float, nargs='+')
parser.add_argument("--METsig", default=[0], type=float, nargs='+')
parser.add_argument("--meffIncl", default=[800], type=float, nargs='+')

args = parser.parse_args()
modeMap = {"discovery": "-z", "exclusion" : "-p", "exclusionUL" : "-p -l", "all" : "-z -p -l"}

grid = args.grid
points = args.point
mode = args.mode
outputSuffix = args.outputSuffix
pointsPerCommand = args.pointsPerCommand

if grid is None:
    print("Can't run without a grid!")
    sys.exit()

if not mode in modeMap:
    print("Don't know HistFitter argument for optimisation mode {0}".format(mode))
    sys.exit()
   
from zerolepton.grids.config import GridConfig
discovery = False
if mode == discovery: 
    discovery = True
gridConfig = GridConfig(grid, discovery)

if (points == [] or points[0] == "") and not args.entire_grid:
    print("Attempting to find optimisation points in grids.cfg")

    pointDict = loadGridPoints(grid)

    # dict of "m0 -> 0", "m12 -> 1" like items
    interpretation_idx = {item: i for i, item in enumerate(gridConfig.interpretation.split(":"))}

    # sanity check
    for c in gridConfig.optimisation_cuts:
        if "-" in c.key: 
            (key1, key2) = c.key.split("-")
            keys = [key1, key2]
        else:
            keys = [c.key]
        
        for k in keys:
            if k not in interpretation_idx:
                print(colors.BOLD + colors.FAIL + "FATAL: unknown variable {0} used in optimisation string - check settings/grids.cfg!".format(k) + colors.ENDC)
                sys.exit()

    for p in pointDict:
        # now test if it passes the cuts
        for c in gridConfig.optimisation_cuts:
            if "-" in c.key:
                (idx1, idx2) = [interpretation_idx[i] for i in c.key.split("-")]
                #print idx1, idx2, c.value
                if p[idx1] - p[idx2] == c.value:
                    points.append("_".join(str(i) for i in p))
                    break
            else:
                # now we have only a normal key left
                if p[interpretation_idx[c.key]] == c.value:
                    points.append("_".join(str(i) for i in p))
                    break

    # ensure we didn't put any duplicates in
    points = set(points)
    
    print(colors.OKGREEN + "=> Loaded {0} optimisation points based on your cuts".format(len(points)) + colors.ENDC)
   
    first = True
    for line in textwrap.wrap(", ".join(points), 80):
        if first: print "=> {0}".format(line); first=False
        else:     print "   {0}".format(line)

if args.entire_grid:
    print("Overriding points settings - using entire grid")
    points = list({"_".join(str(i) for i in x) for x in loadGridPoints(grid)})

if points == []:
    print("Can't run without a grid point!")
    sys.exit()

# check whethe these points exist
if not os.path.exists(gridConfig.filename):
    print("Input file {0} does not exist - skipping existence of check whether points exist in ntuple".format(gridConfig.filename))
else:
    print("Before filtering: {0:d} points".format(len(points)))
    f = ROOT.TFile.Open(gridConfig.filename)
    if f:
        filteredPoints = [p for p in points if f.GetListOfKeys().Contains("{0}_{1}_SRAll".format(grid, p))]
        removedPoints = list(set(points) - set(filteredPoints))
        points = filteredPoints
        f.Close()
    print("After filtering: {0:d} points".format(len(points)))

    if len(removedPoints) > 0:
        print "="*80
        print(colors.BOLD + colors.MAJORWARNING + "WARNING: The following points were removed:" + colors.ENDC)
        for line in textwrap.wrap(", ".join(removedPoints), 80):
            print "   {0}".format(line)
        print "="*80

# build a dictionary out of the cuts
cuts = vars(args)
# remove the useless args
cuts.pop('grid', None)
cuts.pop('point', None)
cuts.pop('mode', None)
cuts.pop('outputSuffix', None)
cuts.pop('entire_grid', None)
cuts.pop('pointsPerCommand', None)

#print cuts
#for var in cuts:
#    print var, len(cuts[var])

commands = []
cutStrings = set()
i = 0

nChunks = int(math.ceil(float(len(points)) / pointsPerCommand))
prevN = pointsPerCommand
# Now re=calcultate to make each job equally long
if nChunks != 1:
    pointsPerCommand = int(math.ceil( float(len(points))/nChunks))
    nChunks = int(math.ceil(float(len(points)) / pointsPerCommand))
    if prevN != pointsPerCommand:
        print(colors.OKBLUE + "Redefined number of points per command to {0:d} to make each job equally long".format(pointsPerCommand))
    print(colors.OKBLUE + "Splitting {0} points into {1:d} chunks to make jobs".format(len(points), nChunks ) + colors.ENDC)

nJetList = cuts.pop('nJets')
for nJets in nJetList:
    # Split by nJets 
    
    j = 0
    nRemoved = 0
    myCuts = copy(cuts)
    removedCuts = []

    # Removed obsolete jet cuts
    for N in range(3, 8):
        name = 'jetpt{0}'.format(N)
        if nJets < N and name in myCuts:
            if myCuts[name] != [0]: removedCuts.append(name)
            del myCuts[name]

    if nJets < 4:
        if "dPhiR" in myCuts:
            removedCuts.append("dPhiR")
            del myCuts["dPhiR"]

    if removedCuts != []:
        print(colors.OKBLUE + "Removed cuts on {0} for nJets={1}".format(", ".join(removedCuts), nJets) + colors.ENDC)

    for c in cartesian_product(myCuts):
        # add the nJet cut to this
        c['nJets'] = nJets

        # are the jet pt's nicely descending?
        ignoreCut = False
        maxJetPt = 200
        if "jetpt1" in c: 
            maxJetPt = c['jetpt1']

        myJetPts = [maxJetPt]
        for N in range(2, nJets+1):
            # check if we are lower than the current maximum
            
            name = 'jetpt{0}'.format(N)
            # if we're not in - falls back to the default of 50
            myJetPt = 50
            if name in c: myJetPt = c[name]

            myJetPts.append(myJetPt)

            if myJetPt > maxJetPt:
                ignoreCut = True
            
            maxJetPt = myJetPt

        if ignoreCut:
            #print "nJet = {0}; skipping jet cuts {1}".format(nJets, " ".join([str(s) for s in myJetPts]))
            nRemoved += 1
            continue
        else:
            pass
            #print "nJet = {0}; keeping jet cuts {1}".format(nJets, " ".join([str(s) for s in myJetPts]))

        # Now build the string
        cutStr = buildCutString(c)
        cutStrings.add(cutStr)

        # NOTE: the prefix must match to what the analysis script does internally - we only construct the channel to get its full name out later
        channel = createChannelConfigFromString(cutStr, "SR{0:d}j".format(nJets))

        for subsetPoints in chunks(points, pointsPerCommand):
            i += 1
            j += 1

            # ROOT5 has a tendency to crash if we don't run the -t step seperately, so do that
            myCmds = []
            for HFargs in ("-t", "-w -f {0}".format(modeMap[mode]) ):
                myCmds.append('HistFitter.py {0} -F excl -ggrid{1},{2} -u "-R {3} -P SR{4}j" {5}/analysis/ZeroLepton_Run2.py'.format(HFargs, grid, ",".join(subsetPoints), cutStr, nJets, os.getenv('ZEROLEPTONFITTER')))

            cmd = " && ".join(myCmds)

            # NOTE: I need to become clever enough to recycle histograms for the final discriminating variable.
            commands.append( (cutStr, channel.fullname, cmd) )

        pass
   
    if nRemoved > 0:
        print(colors.OKBLUE + "Removed {0} useless jet pt settings for nJet={1}".format(nRemoved, nJets) + colors.ENDC)
    print(colors.OKBLUE + "Wrote {0} commands for nJet={1}".format(j, nJets) + colors.ENDC)
timestamp = time.time()

data = {}
data['argv'] = " ".join(sys.argv)
data['mode'] = mode
data['timestamp'] = timestamp
data['grid'] = grid
data['points'] = points
data['commands'] = commands
data['cutStrings'] = list(cutStrings)

suffix = datetime.datetime.fromtimestamp(timestamp).strftime("%Y%m%d-%H%M%S")
if outputSuffix is not None and outputSuffix != "":
    suffix = outputSuffix

# store 2 files. we do this to prevent accidental deletion.
defaultDir = os.path.join(os.getenv('ZEROLEPTONFITTER'), 'optimisation')
if not os.path.exists(defaultDir): os.makedirs(defaultDir)
filenames = ["{0}/optimisation-{1}-{2}.json".format(defaultDir, grid, suffix)]
if os.getenv('PWD') != defaultDir and os.getenv('PWD') != os.getenv('ZEROLEPTONFITTER'):
    filenames.append("{0}/optimisation-{1}-{2}.json".format(os.getenv('PWD'), grid, suffix))

for filename in filenames:
	with open(filename, 'w') as outfile:
		json.dump(data, outfile)

	print(colors.OKGREEN + "Wrote {1} optimisation commands to {0}".format(filename, i) + colors.ENDC)
