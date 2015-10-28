# Module with utilities to run jobs

# TODO: parts of this should be changed into a proper class, with a setting to run locally or to run commands on a batch system

import ConfigParser
import subprocess

from ..colors import colors
from ..utils import chunks
from functools import partial
from multiprocessing.dummy import Pool
import os
import subprocess
import string
import sys
import time

try:
    input = raw_input
except NameError:
    pass

def runLocalCommands(args, outputDir, commands):
    # NOTE: this is going to BREAK meff optimisation if we re-cycle histograms.
    # Needs to be updated to run in successive orde if we implement that.
    N = len(commands)

    if N > 50:
        print("")
        print("Are you sure you want to run %d commands locally?" % N)
        if args.dry_run:
            print("[NB: this is a dry run]")
        var = input("Press enter to continue")
        print("")

    cmds = []
    for i, x in enumerate(commands):
        (cuts, name, cmd) = x
        cmd = "cd %s && echo '%d/%d\t%s' && %s 2>&1 >/dev/null" % (outputDir, i+1, N, cmd, cmd)
        cmds.append(cmd)

    if args.dry_run:
        print("Would run following commands:")
        for cmd in cmds:
            print("   %s" % cmd)
        return

    pool = Pool(10) # concurrent commands at a time
    for i, returncode in enumerate(pool.imap(partial(subprocess.call, shell=True), cmds)):
        if returncode != 0:
           print(("%d command failed: %d" % (i, returncode)))

def getBatchConfiguration(site):
    config = ConfigParser.RawConfigParser({"use_multiple" : False, "number_to_combine" : 1})
    config.read('%s/settings/batch.cfg' % os.getenv('ZEROLEPTONFITTER'))

    if not config.has_section(site):
        print(colors.ERROR + "Configuration settings/batch.cfg has no site {0}".format(site) + colors.ENDC)
        sys.exit()

    queue = config.get(site, 'queue').replace('"', '')
    use_multiple = config.getboolean(site, 'use_multiple')
    number_to_combine = config.getint(site, 'number_to_combine')
    command = config.get(site, 'command').replace('"', '')

    cfg = { 'queue' : queue, 'use_multiple' : use_multiple, 'number_to_combine' : number_to_combine, 'command' : command }

    return cfg

def submitFile(args, filename, batchConfig):
    (basename, ext) = os.path.splitext(filename)
    queue = batchConfig['queue'].replace('"', "")
    if args.queue is not None and args.queue != "":
        queue = args.queue
  
    logFilename = os.path.join(os.getenv('ZEROLEPTONFITTER'), "Logs", os.path.basename(basename))

    values = {"QUEUE" : queue, "SCRIPT" : filename, "LOG" : "%s.log" % logFilename, "ADDITIONAL_OPTS" : args.additional_opts}

    cmdTemplate = string.Template(batchConfig['command'])
    cmd = cmdTemplate.safe_substitute(values)
    print(cmd)
    
    if args.dry_run: return
    subprocess.call(cmd, shell=True)

def runBatchCommands(args, outputDir, commands):
    # NOTE: this is going to BREAK meff optimisation if we re-cycle histograms. Needs to be updated to run in successive order.

    batchConfig = getBatchConfiguration(args.site)

    # We load the script that gets run from batchJob.template and set the appropriate variables

    with open('%s/ToolKit/optimisation/batchJob.template' % os.getenv('ZEROLEPTONFITTER')) as f:
        template = string.Template( f.read() )

    # Ensure 'Jobs' dir exists
    if not os.path.exists(os.path.join(os.getenv('ZEROLEPTONFITTER'), 'Jobs')):
        os.makedirs(os.path.join(os.getenv('ZEROLEPTONFITTER'), 'Jobs'))

    # Create the output files
    timestamp = time.strftime("%d/%m/%Y, %H:%M:%S")
    cmdTemplate = string.Template(batchConfig['command'].replace('"',""))

    useMultiple = False
    if batchConfig['use_multiple'] and batchConfig['number_to_combine'] > 1:
        useMultiple = True

    jobFilenames = []
    for i, x in enumerate(commands):
        filename = '%s/Jobs/%s-%d.sh' % (os.getenv('ZEROLEPTONFITTER'), os.path.basename(outputDir), i+1)
        
        if not os.path.exists(filename):
            (cuts, name, cmd) = x
            d = {"DIR" : outputDir, "HISTFITTER" : os.getenv('HISTFITTER'), "ZEROLEPTONFITTER" : os.getenv('ZEROLEPTONFITTER'), "CMD" : cmd, "GENERATED_AT": timestamp}
            s = template.safe_substitute(d)

            with open(filename, 'w') as f:
                f.write(s)

        print("Wrote batch job file %s" % filename)

        if not useMultiple:
            submitFile(args, filename, batchConfig)

        jobFilenames.append(filename)

    if useMultiple:
        for i, c in enumerate(chunks(jobFilenames, batchConfig['number_to_combine'])):
            filename = '%s/Jobs/%s-combined-%d.sh' % (os.getenv('ZEROLEPTONFITTER'), os.path.basename(outputDir), i+1)
            if not os.path.exists(filename):
                with open(filename, 'w') as f:
                    f.write("#!/bin/bash\n\n")
                    for cmd in c:
                        f.write("bash %s\n" % cmd)

            print("Wrote combined file %s" % filename)
            submitFile(args, filename, batchConfig)
