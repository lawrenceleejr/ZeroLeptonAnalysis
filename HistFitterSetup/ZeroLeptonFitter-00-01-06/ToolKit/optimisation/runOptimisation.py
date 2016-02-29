#!/usr/bin/env python

# Run a bunch of optimisation commands in a JSON file.
# Will place the output of the optimisation run in its own directory.

import argparse
import ConfigParser
import datetime
import filecmp
import glob
import json
import os
import shutil
import string
import subprocess
import sys
import time

from zerolepton.inputs.config import InputConfig
from zerolepton.batch.utils import runLocalCommands
from zerolepton.batch.utils import runBatchCommands
from zerolepton.colors import colors

if os.getenv('ZEROLEPTONFITTER') is None:
    print("Setup ZeroLeptonFitter first!")
    sys.exit()

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", default=None, type=str)
parser.add_argument("-F", "--force", default=False, action="store_true")
parser.add_argument("-o", "--outputdir", default="", type=str, help="output dir under which the dir for the optimisation will be placed")
parser.add_argument("--local", action='store_true', default=False, help="run these commands locally?")
parser.add_argument("--dry_run", action='store_true', default=False, help="dry run?")
parser.add_argument("--grid", default=None, type=str, help="Attempt to detect most recent optimisation file for this grid, and use it")
parser.add_argument("--site", default="default", type=str, help="Site to take from settings/batch.cfg")
parser.add_argument("-m", "--missing-filename", default=None, type=str, help="filename with cut strings to run again")
parser.add_argument("--queue", default=None, type=str, help="Override queue name for site from settings/batch.cfg")
parser.add_argument("--additional-opts", default="", type=str, help="Additional options (e.g. walltime limit, nCPU, log redirection) to pass to the submission call")
args = parser.parse_args()

# Can we find a file for the grid?
if args.grid is not None and args.grid != "":
    print("Attempting autodetection for grid %s" % args.grid)

    globStr = "%s/optimisation-*%s*.json" % (os.getenv('ZEROLEPTONFITTER'), args.grid)
    newest = max(glob.iglob(globStr), key=os.path.getctime)

    if newest is not None and newest != "":
        print("Found most recent optimisation definitions: %s" % os.path.basename(newest))

        if args.filename is not None and args.filename != "":
            print("WARNING: you specified filename. The autodetected filename will be overwritten later...")

        args.filename = newest

if args.filename is None or args.filename == "":
    print("Cannot run without a file!")
    sys.exit()

# not an absolute path? assume it's relative to ZEROLEPTONFITTER
if not os.path.isabs(args.filename) and not os.path.exists(args.filename):
    print("Assuming a relative path is given; prepending $ZEROLEPTONFITTER (%s)" % (os.getenv('ZEROLEPTONFITTER')))
    args.filename = os.path.join(os.getenv('ZEROLEPTONFITTER'), args.filename)

if not os.path.exists(args.filename):
    print("The file %s does not exist!" % args.filename)
    sys.exit()

print("Using file %s" % args.filename)
runMissing = False
if args.missing_filename is not None:
    if not os.path.exists(args.missing_filename):
        print("The file with missing cuts %s does not exist!" % args.missing_filename)
        sys.exit()

    with open(args.missing_filename) as f:
        missingCutStrings = json.load(f)

    runMissing = True

# Check if we already used this file: the output will be in $ZEROLEPTONFITTER/<dirname>, where <dirname> is the file without its extension
(name, ext) = os.path.splitext(os.path.basename(args.filename))

outputdir = os.getenv('ZEROLEPTONFITTER')
if args.outputdir:
    outputdir = args.outputdir
    if not os.path.exists(args.outputdir) and not args.dry_run:
        os.makedirs(args.outputdir)
        print("Created outputdir %s" % args.outputdir)

dirname = os.path.join(outputdir, name)
if not args.force and os.path.exists(dirname) and not args.dry_run:
    print("")
    print("The directory %s already exists! Exiting now.\n\nIf this was intended, move the directory. We will not re-run the same optimisation file twice." % dirname)
    sys.exit()

print("Will write optimisation output in %s" % dirname)
if not os.path.exists(dirname) and not args.dry_run:
    os.makedirs(dirname)
    print("Created output directory %s" % dirname)

with open(args.filename) as f:
    data = json.load(f)

print("Loaded SRs generated with %s" % data['argv'])
print("Generated at: %s" % datetime.datetime.fromtimestamp(data['timestamp']).strftime("%d/%m/%Y, %H:%M:%S"))
print("")
print(colors.OKBLUE + "Will run on grid: %s" % data['grid'] + colors.ENDC)
print("Optimisation mode: %s" % data['mode'])
print("Using the following points: %s" % ", ".join(data['points']))

if args.force:
    print("")
    print(colors.WARNING + "USING --force COULD POLLUTE YOUR OUTPUT DIRECTORY" + colors.ENDC)
    print("")

if not args.local and args.site == "default":
    inputConfig = InputConfig()
    args.site = inputConfig.site

print(colors.OKGREEN + "Running %d commands" % len(data['commands']) + colors.ENDC)

# We can either do this locally, or on a grid
if args.local:
    runLocalCommands(args, dirname, data['commands'])
else:
    commandsToRun = data['commands']
    if runMissing: # clean the non-needed commands
        uniqueCutStrings = []
        for r in missingCutStrings:
            uniqueCutStrings.append(missingCutStrings[r])
        uniqueCutStrings = set(uniqueCutStrings)
        
        missingCommands = []
        for c in commandsToRun:
            print c[0]
            if c[0] not in uniqueCutStrings: continue
            missingCommands.append(c)

        commandsToRun = missingCommands
    runBatchCommands(args, dirname, commandsToRun, runMissing)

# Keep a copy of the optimisation used in the output dir
copiedFilename = os.path.join(dirname, os.path.basename(args.filename))
if not args.dry_run and os.path.abspath(args.filename) != os.path.abspath(copiedFilename):
    shutil.copyfile(args.filename, os.path.join(copiedFilename))
