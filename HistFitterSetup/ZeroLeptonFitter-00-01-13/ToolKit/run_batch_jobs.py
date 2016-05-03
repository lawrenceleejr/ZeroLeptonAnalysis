#!/usr/bin/env python
# usage : 

__doc__ = """
This script can be used to launch batch jobs
Usage: please see
ToolKit/run_batch_jobs.py --help
"""


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
# Import Modules                                                             # 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
import sys, os, string, shutil,pickle,subprocess
import pprint

from ChannelsDict import *
from ZLFitterConfig import *

from OldBatchUtils import *

def parseCmdLine(args):
    #from optparse import OptionParser
    import argparse

    parser = argparse.ArgumentParser() 
    parser.add_argument("--trees", action="store_true", default=False, help="use full trees (SLOW!!!!)")
    parser.add_argument("--alt", action="store_true", default=False, help="use alternative baseline (Top=McAtNlo, W=Alpgen)")
    parser.add_argument("--useNonDegenerateSquarks", action="store_true", default=False)
    parser.add_argument("--numSquarks", type=int, choices=[1,2,4,8], default=8)
    parser.add_argument("--submit", dest="doSubmission", help="submit bacth jobs, by defaut the job is not launched", action='store_true', default=False)
    parser.add_argument("--queue", dest="queue", help="batch queue", default=" 8nh ")
    parser.add_argument("--grid", dest="grid", help="grid name", default="SS_direct")
    parser.add_argument("--only-skipped-points", help="run only on those points that get skipped with not using --allpoints", default=False, action="store_true")
    parser.add_argument("--allpoints", dest="allpoints", help="all points", action='store_true', default=False)
    parser.add_argument("--nb", dest="nb", help="nb of point per jobs", default=100)
    parser.add_argument("--mult", dest="mult", help="execute multiple points in one job", default=True, action='store_false')
    parser.add_argument("--saveWS", dest="saveWS", help="saveWS to extract sumW after cuts", default=False, action='store_true')
    parser.add_argument("--opti", dest="opti", help="run only on optimization points", default=False, action='store_true')
    parser.add_argument("--ul", dest="ul", help="add -l to HistFitter options to run limits (--opti implies this)", default=False, action="store_true")
    parser.add_argument("--discovery", dest="discovery", help="compute p0", default=False, action="store_true")
    parser.add_argument("--only-ul", dest="only_ul", help="change options to '-f -p -l', assume that workspaces already exist. Overrides other options.", default=False, action="store_true")
    parser.add_argument("--lyon", dest="lyon", help="generate batch files for use @ lyon", default=False, action='store_true')
    parser.add_argument("--nikhef", dest="nikhef", help="generate batch files for use @ Nikhef", default=False, action='store_true')
    parser.add_argument("--bfg", dest="bfg", help="generate batch files for use @ Bfg", default=False, action='store_true')
    parser.add_argument("--jobdir", dest="jobdirname", help="Directory where scripts are written", default="Jobs/")
    parser.add_argument("--logdir", dest="logdirname", help="Directory where log files are written", default=MYWORKINGDIR+"/Logs/")
    parser.add_argument("--shape", dest="shape", action="store_true", default=False, help="use MyAnaList_Shape.py for --opti; or the Moriond '13 for the normal runs")
    parser.add_argument("-N", type=int, default=1, help="bundle N jobs together in one job submission to decrease number of jobs")

    config = parser.parse_args(args)
    
    # use fallback by default
    userArgs = "-C"
    config.option = ""

    if config.trees:
        userArgs = ""
        config.option = "-t"

    if config.discovery:
        config.option += " -w -f  -z  -L WARNING -F excl " 
    else:
        if config.ul:# or config.opti:
            config.option += " -w -f  -p  -l -L WARNING -F excl"
        elif not config.only_ul: 
            config.option += " -w -f  -p  -L WARNING -F excl "
        if config.only_ul:
            config.option += " -f  -p  -l -L WARNING -F excl"



    if config.ul and (config.grid.find("direct") == -1 and config.grid.find("onestep") == -1):
        print "Upper limits normally only calculated for {SS,GG,SG}_direct and {SS,GG}_onestep!"
        raw_input("Press enter to run ULs for a grid other than onestep or direct grids")

    # stuff that goes into userargs
    if config.alt or config.useNonDegenerateSquarks:
        if (config.grid != "SS_direct" and config.grid != "SS_onestep") and config.useNonDegenerateSquarks:
            print "--useNonDegenerateSquarks only makes sense for SS_direct and SS_onestep"
            sys.exit()

        if config.alt:
            userArgs += " --useAlternativeBaseline"

        if config.useNonDegenerateSquarks:
            userArgs += " --useNonDegenerateSquarks --numSquarks=%d" % config.numSquarks
       
    if userArgs != "":
        config.option += " -u=\"%s\"" % userArgs

    if config.allpoints and config.only_skipped_points:
        print "allpoints and only-skipped-points both set, exiting!"
        sys.exit()

    if config.allpoints and config.opti:
        print "allpoints and opti both set, exiting!"
        sys.exit()

    if config.opti and config.only_skipped_points:
        print "opti and only_skipped_points both set, exiting!"
        sys.exit()

    return config

# The actual script is below.
config = parseCmdLine(sys.argv[1:])

###########################################################################
#get grid points
###########################################################################
try:
    picklefile = open(MYWORKINGDIR+'/ToolKit/signalPointPickle.pkl','rb')
except:
    cmd="cd "+MYWORKINGDIR+"/ToolKit && python makeSignalPointPickle.py && cd -"
    subprocess.call(cmd, shell=True)
    print cmd
    picklefile = open(MYWORKINGDIR+'/ToolKit/signalPointPickle.pkl','rb')
      
pointdict = pickle.load(picklefile)
picklefile.close()   
tmppoints=[]

gridName = config.grid

for key,info in pointdict[gridName].items():
    point = str(info[0])
           
    if len(info) >= 2:
        point += "_"+str(info[1])
    if len(info) >= 3:
        point += "_"+str(info[2])

    #this is the default: no --all, --only-skipped or --opti, so we skip some excluded points
    if not config.allpoints and not config.only_skipped_points and not config.opti and skipThisPoint(config.grid, info[0], info[1]):
        print "1) skipping ",point
        continue
    # using --only skipped, (and not --opti), take only the points skipped above 
    elif config.only_skipped_points and not config.opti and not skipThisPoint(config.grid, info[0], info[1]):
        print "2) skipping ",point
        continue
    # using --opti, we take a special set of points
    elif config.opti and not config.only_skipped_points and not isOptimisationPoint(config.grid, info[0], info[1]):
        print "3) skipping ",point
        continue

    tmppoints.append(point) 

#print tmppoints
pointsList = split_seq(tmppoints, int(len(tmppoints)/int(config.nb)))

print len(pointsList),pointsList


###########################################################################
# create scripts
###########################################################################

jobdirname=MYWORKINGDIR+"/"+config.jobdirname
if not os.path.exists(jobdirname):            
    os.mkdir(jobdirname)
    pass
if not os.path.exists(config.logdirname):            
    os.mkdir(config.logdirname)
    pass

# list of channels and settings to run over. 
anaList =  finalChannelsDict.keys()

jobFilenames = []
for ana in anaList:    
    counter=0
    for points in pointsList:
        counter+=1

        if config.nikhef:
            jobFilenames += [writeAndSubmitJobForNikhef(config, ana, points, jobdirname, counter)]
        elif config.bfg:
            writeAndSubmitJobForBfg(config, ana, points, jobdirname, counter)
        elif config.lyon:
            writeAndSubmitJobForLyon(config, ana, points, jobdirname, counter)
        else:
            writeAndSubmitJob(config, ana, points, jobdirname, counter)

if config.nikhef and config.N > 1:
    # jobs have by definition not been submitted yet, make a combined file
    writeCombinedJobForNikhef(config, jobFilenames)

