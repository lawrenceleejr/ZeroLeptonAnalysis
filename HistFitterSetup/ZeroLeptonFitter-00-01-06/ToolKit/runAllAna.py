#!/usr/bin/env python
# usage : 

__doc__ = """

"""

from ChannelsDict import *
from makeSignalPointPickle import *

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
# Import Modules                                                             # 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
import sys, os, string, shutil,pickle,subprocess

def parseCmdLine(args):
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--all", dest="all", help=" all", action='store_false', default=True)
    parser.add_option("--run", dest="run", help=" execute", action='store_true', default=False)
    parser.add_option("--noVR", dest="noVR", help=" no Validation region", action='store_true', default=False)
    parser.add_option("-x", dest="doXML", help=" doXML", action='store_true', default=False)
    parser.add_option("-d", dest="doPlots", help=" doPlots", action='store_true', default=False)
    parser.add_option("--fit", dest="FitType", help="fit type {0:bkg, 1: disc, 2: excl, 3: p0}", default=0)
    parser.add_option("--alt", help="use alternative baseline (Top=McAtNlo, W=Alpgen)", default=False, action="store_true")

    (config, args) = parser.parse_args(args)
    return config

def main():
    config = parseCmdLine(sys.argv[1:])
    
    
    scriptname = os.environ['ZEROLEPTONFITTER']+"/analysis/ZeroLepton_Run2_RJigsaw.py" #ATT
    runList = finalChannelsDict.keys()


    option = "-t -w -f "
    
    if config.doXML==True:
        option += " -x "
    
    #if config.doPlots==True:
    option += " -D allPlots "
    
    if int(config.FitType)==0:
        option += " -F bkg "
        if not config.noVR:
            option += " -V "
    elif int(config.FitType)==1:
        option += " -z -F disc"
    elif int(config.FitType)==2:
        option += "  -F excl -p -l"
    elif int(config.FitType)==3:
        option += " -z -F excl "  

    for ana in runList:
        log=" >& "+ana+"_Bkg.log"
        if int(config.FitType)==1:
            log=" >& "+ana+"_Disc.log"
        if int(config.FitType)==2:
            log=" >& "+ana+"_Excl.log"
        if int(config.FitType)==3:
            log=" >& "+ana+"_ExclPz.log"
            
        if int(config.FitType)!=2 and int(config.FitType)!=3:
            if config.all==True: log+="&"
            cmd= "HistFitter.py "+option+" -r "+ana+" "+scriptname+log        
            print "\n",cmd
            if config.run:
                subprocess.call(cmd, shell=True)
                print "Execution done"
        else:   
            grid="GG_direct"
            points=['1200_0','1400_0']
#            for key,info in pointdict [grid].items():
#                pointstr=str(info[0])+"_"+str(info[1])
            for pointstr in points:
                log2=log+"_"+pointstr+".log"
                if config.all==True: log2+="&"
                cmd= "HistFitter.py "+option+" -g grid"+grid+","+pointstr+ " -r "+ana+" "+scriptname+log2
                print cmd
                if config.run:
                    subprocess.call(cmd, shell=True)

###########################################################################
#Main
###########################################################################
if __name__ == "__main__":
    main()

