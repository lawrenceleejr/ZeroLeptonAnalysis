#!/usr/bin/env python
# usage : 

__doc__ = """

"""

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
# Import Modules                                                             # 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
import sys, os, string, shutil,pickle,subprocess



MYWORKINGDIR=os.getcwd().strip()+"/"
HISTFITTERDIR=os.popen("echo $HISTFITTER").readlines()[0].strip()+"/"
ZEROLEPTONFITTERDIR=os.popen("echo $ZEROLEPTONFITTER").readlines()[0].strip()+"/"
INPUTDIR_LYON="/afs/in2p3.fr/home/m/makovec/TREES/ZeroLepton-00-00-50_Light/"


from ChannelsDict import *


def parseCmdLine(args):
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--eff", dest="doEfficiency", help=" ", action='store_true', default=False)
    parser.add_option("--all", dest="all", help=" all", action='store_true', default=False)
    parser.add_option("--submit", dest="submit", help=" execute", action='store_true', default=False)
    parser.add_option("--shape", dest="shape", help="use shape fits", action='store_true', default=False)
    parser.add_option("--noVR", dest="noVR", help=" no Validation region", action='store_true', default=False)
    parser.add_option("-x", dest="doXML", help=" doXML", action='store_true', default=False)
    parser.add_option("-d", dest="doPlots", help=" doPlots", action='store_true', default=False)
    parser.add_option("--fit", dest="FitType", help="fit type {0:bkg, 1: disc}", default=0)
    parser.add_option("--alt", help="use alternative baseline (Top=McAtNlo, W=Alpgen)", default=False, action="store_true")

    (config, args) = parser.parse_args(args)
    return config

def main():
    config = parseCmdLine(sys.argv[1:])
    scriptname = os.environ['ZEROLEPTONFITTER']+"/analysis/ZeroLepton_Run2.py"


#    grid="SM_SS_direct"
#    points=['412_37', '412_187', '487_112', '600_0', '412_337', '487_262', '600_150', '750_0', '412_387', '487_412', '600_300', '750_150', '900_0', '487_462', '600_450', '750_300', '1050_0', '750_450']


    grid="NUHMG"
    points=['2000000_450','2800000_450','2800000_490']

    option = "-t -w -f "
    #option = " -w -f "
    
    if config.alt:
        option += " -u=\"--useAlternativeBaseline\" "
    
    if config.doXML==True:
        option += " -x "
    
    if config.doPlots==True:
        option += " -d "
    
    if int(config.FitType)==0:
        option += "  -F bkg "
        if not config.noVR:
            option += " -V "
    elif int(config.FitType)==1:
        #option += " -l -p -F disc"
        option += " -z -F disc"
    elif int(config.FitType)==2:
        option += "  -F excl -p -l"

    if not config.shape:
        runList = finalChannelsDict.keys()
    else:
        runList = anaListMoriond13Shape

    for ana in runList:
        filename=MYWORKINGDIR+"/Jobs/job_"
        log=MYWORKINGDIR+"Logs/joob_"+ana+"_"

        if int(config.FitType)==1:
            filename +="Disc"
            log+="Disc.log"
        else:            
            filename +="Bkg"    
            log+="Bkg.log"

        if int(config.FitType)!=2:
            cmd= "HistFitter.py "+option+" -r "+ana+" "+scriptname



        filename += "-"+ana+".sh"
        f=open(filename,'w')
        
        f.write("#!/bin/zsh\n")
        f.write("XCWD=$PWD\n")
        f.write("cd "+MYWORKINGDIR+"\n")
        f.write("which gcc \n")            
        f.write("MYHERE=$PWD\n")        
        #for line in open(HISTFITTERDIR+"/setup.sh","r").readlines():                
        #    f.write(line)    
    
        f.write("source mysetup.sh\n")            
        f.write("cd $XCWD\n")            
        f.write("if [ ! -d results ]; then mkdir -v results; fi\n")
        f.write("if [ ! -d config ]; then mkdir -v config; fi\n")
        
        f.write("/bin/cp -r $ZEROLEPTONFITTER/python .\n")
        f.write("/bin/cp -r $ZEROLEPTONFITTER/data .\n")
        
        f.write("ls -ltr\n")
        f.write("echo $ROOTSYS \n")
        f.write("which gcc \n")
        f.write("hostname \n")
        f.write("echo '=============' \n")
        f.write(cmd+"\n")
        f.write("/bin/cp -rf results/* "+MYWORKINGDIR+"results/\n")
        f.write("/bin/cp -rf data/* "+MYWORKINGDIR+"data/\n")
        f.write("/bin/cp -rf config/* "+MYWORKINGDIR+"config/\n")
   
        f.close()
        
        cmd="chmod u+x "+filename
        subprocess.call(cmd, shell=True)
    


        err=log
        qsub_option=" -P P_atlas -l ct=20000,vmem=2048M,fsize=17G,sps=1 "
        cmd="bsub -q 1nd -e "+err+" -o "+log+" "+filename
    
        print "\n"
        print cmd
        if config.submit:
            subprocess.call(cmd, shell=True)

       
###########################################################################
#Main
###########################################################################
if __name__ == "__main__":
    main()

