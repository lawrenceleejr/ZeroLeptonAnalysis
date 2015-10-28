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

from allChannelsDict import *
from ZLFitterConfig import *

###########################################################################
#
########################################################################### 
myscript= "analysis/ZeroLepton_Paper13.py"

MYWORKINGDIR=os.getcwd().strip()+"/"
HISTFITTERDIR=os.popen("echo $HISTFITTER").readlines()[0].strip()+"/"
ZEROLEPTONFITTERDIR=os.popen("echo $ZEROLEPTONFITTER").readlines()[0].strip()+"/"



###########################################################################
#MyAnalysis
###########################################################################

         
###########################################################################
# useful functions
###########################################################################
def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def split_seq(seq, size):
    if size==0: return [seq]
    newseq = []
    splitsize = 1.0/size*len(seq)
    for i in range(size):
        newseq.append(seq[int(round(i*splitsize)):int(round((i+1)*splitsize))])
    return newseq

def listToString(seq):
    mystring=""
    for s in seq:
        mystring+=str(s)+","
        pass
    last=mystring[-1:]
    if last==",":
        mystring=mystring[:-1]
    return mystring

def skipThisPoint(grid, x, y):
    if grid == "Tt":
        if x > 750  or y>250: 
            return True

        
    if grid == "Gluino_Stop_charm":
        if y!=120:
            return True


    if grid == "SS_direct":
#        if y!=0: return True
        #if x < 600 and y < 200:# and y>=1: 
        #    return True
        if x >= 1100 or y >= 500: 
            return True
    
        #if  y!=0:# and x!=450:
        #    return True

    if grid == "SM_GG_direct":
        if x >= 1400 or y > 700: 
            return True
        if x < 1000 and y < 300: 
            return True            
    
    if grid == "SM_SG_direct":
        if x >= 1800 or y > 1000: 
            return True
        if x < 1300 and y < 300: 
            return True           
    
    if grid == "msugra_30_P":
        if y < 400: 
            return True
        if x > 1600 and y > 700: 
            return True          
    
    if grid == "mssm":
        if y < 1200 or x<1200: 
            return True
        if y > 2200 and x>1800: 
            return True

    return False

def isOptimisationPoint(grid, x, y):
    if grid == "GG_onestep":
        return True
    
    if grid == "SS_onestep":
        return True

    if grid == "Gluino_Stop_charm":
        if x==1000:
            return True
        if y==200:
            return True
        
    if grid == "SS_direct":        
        if y == 0 and x < 1300:
            return True
        if x == 487:
            return True
        if x == 300:
            return True
        if x == 375:
            return True
        if x == 600 and y <= 500: 
            return True
        if x == 750 and y <= 500: 
            return True
        if x == 900 and y <= 500: 
             return True
        if x == 1050 and y <= 500: 
            return True
        if x == 1200 and y <= 500: 
            return True
        
    if grid == "GG_direct":
        if y == 0 and x < 1500 and x >= 500:
            return True
        if x == 1125: 
            return True
        if x == 700:
            return True

    if grid == "Tt":
        #if y == 1 and x < 700 and x <= 400:
        #    return True
        
        if y == 1 and x < 750:
            return True
        if y == 50 and x < 750:
            return True
        if x == 550 and y<250 and y>0:
            return True

        #if x == 450 and y<250 and y>0:
        #    return True

        
    if grid == "SG_direct":
        if y == 0 and x >= 800 and x < 1700:
            return True
        if x == 1012 and y <= 1100: 
            return True
        if x == 1387 and y <= 900:
            return True

    return False

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
    parser.add_argument("--nb", dest="nb", help="nb of point per jobs", default=20)
    parser.add_argument("--mult", dest="mult", help="execute multiple points in one job", default=True, action='store_false')
    parser.add_argument("--saveWS", dest="saveWS", help="saveWS to extract sumW after cuts", default=False, action='store_true')
    parser.add_argument("--opti", dest="opti", help="run only on optimization points", default=False, action='store_true')
    parser.add_argument("--ul", dest="ul", help="add -l to HistFitter options to run limits (--opti implies this)", default=False, action="store_true")
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

    if config.ul or config.opti:
        config.option += " -w -f  -p  -l -L WARNING -F excl"
    elif not config.only_ul: 
        config.option += " -w -f  -p  -L WARNING -F excl"

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

###########################################################################
# Batch file writing functions
###########################################################################
def writeAndSubmitJob(config, ana, points, jobdirname, counter):
    filename=jobdirname+"/job_"+"_"+config.grid
    if config.alt:
        filename += "_alt"
    if config.useNonDegenerateSquarks:
        filename += "_nonDegenerateSquarks_N%d" % config.numSquarks

    filename += "_"+ana+"_"+str(counter)+".sh"

    f=open(filename,'w')

    f.write("#!/bin/zsh\n")
    f.write("XCWD=$PWD\n")
    f.write("cd "+MYWORKINGDIR+"\n")
    f.write("which gcc \n")            
    f.write("MYHERE=$PWD\n")        
    for line in open(HISTFITTERDIR+"/setup.sh","r").readlines():                
        f.write(line)    
    
    #f.write("cd $HISTFITTER\n")
    #f.write("source setup.sh\n")                        
    #f.write("cd $MYHERE\n")

    f.write("source setup.sh\n")            
    f.write("cd $XCWD\n")            
    f.write("if [ ! -d results ]; then mkdir -v results; fi\n")
#    f.write("if [ ! -d data ]; then mkdir -v data; fi\n")
    f.write("if [ ! -d config ]; then mkdir -v config; fi\n")
    
    #f.write("cp "+MYWORKINGDIR+"config/HistFactorySchema.dtd config/.\n")
    f.write("/bin/cp -r $ZEROLEPTONFITTER/python .\n")
    f.write("/bin/cp -r $ZEROLEPTONFITTER/data .\n")
    
    f.write("ls -ltr\n")
    f.write("echo $ROOTSYS \n")
    f.write("which gcc \n")
    f.write("hostname \n")
    f.write("echo '=============' \n")
    
    if config.mult==False:
        option2="grid"+config.grid+","+listToString(points)
        f.write("HistFitter.py "+config.option+" -r "+ana+" -g "+option2+" "+MYWORKINGDIR+myscript+" "+" > /dev/null \n")
        f.write("/bin/mv results/* "+MYWORKINGDIR+"results/\n")
        #f.write("/bin/mv results/*hypo*root "+MYWORKINGDIR+"results/\n")
        #f.write("/bin/mv results/*upperlimit*root "+MYWORKINGDIR+"results/\n")
        if config.saveWS:
            f.write("ls results/ZL2013*/*_model_afterFit.root| awk -F\/ '{print \"mkdir "+MYWORKINGDIR+"/results//\"$2\"; cp \"$0\" "+MYWORKINGDIR+"/results/\"$2\"/\"}'|zsh  \n")#not very nice :-S
    else:
        #print "Execute separately for each point!"                
        for point in points:
            option2="grid"+config.grid+","+point
            cmd="HistFitter.py "+config.option+" -r "+ana+" -g "+option2+" "+MYWORKINGDIR+myscript+" > /dev/null "
            f.write("echo "+cmd+" \n")
            f.write(cmd+" \n")
            ana2name=ana.replace(",","")
            f.write("sleep 2; \n")
            f.write("/bin/mv results/* "+MYWORKINGDIR+"results/\n")
            #f.write("/bin/mv results/*hypo*root "+MYWORKINGDIR+"results/\n")
            #f.write("/bin/mv results/*upperlimit*root "+MYWORKINGDIR+"results/\n")
            if config.saveWS:
                f.write("ls results/ZL2013*/*_model_afterFit.root| awk -F\/ '{print \"mkdir "+MYWORKINGDIR+"/results//\"$2\"; cp \"$0\" "+MYWORKINGDIR+"/results/\"$2\"/\"}'|zsh  \n")#not very nice :-S

            
    f.close()
    cmd="chmod u+x "+filename
    subprocess.call(cmd, shell=True)
    
    log=config.logdirname+"job_"+ana+"_"+config.grid+"_"+"_"+str(counter)+".log"
    #err=MYWORKINGDIR+config.logdirname+"job_"+ana+"_"+config.grid+"_"+"_"+str(counter)+".err"
    err=log
    cmd="bsub -q "+config.queue+" -e "+err+" -o "+log+" "+filename

    if config.doSubmission==False:
        print cmd
    else:
        subprocess.call(cmd, shell=True)


    

###########################################################################
# Batch file writing functions for BFG
###########################################################################
def writeAndSubmitJobForBfg(config, ana, points, jobdirname, counter):
    filename=jobdirname+"/job_"+"_"+config.grid
    if config.alt:
        filename += "_alt"
    if config.useNonDegenerateSquarks:
        filename += "_nonDegenerateSquarks_N%d" % config.numSquarks

    filename += "_"+ana+"_"+str(counter)+".sh"
    f=open(filename,'w')

    f.write("#!/bin/zsh\n") 
    f.write("cd /home/zr23/\n")
    f.write("source .bashrc\n")
    f.write("OutputDir=/storage/users/zr23/HistFitterOutput_00-00-21/"+config.grid+"\n\n")
    f.write("cd "+HISTFITTERDIR+"\n")
    f.write("source setup.sh\n")                        
    f.write("cd "+MYWORKINGDIR+"\n")
    f.write("source setup.sh\n")            
    f.write("cd $OutputDir\n")  
            
    f.write("if [ ! -d results ]; then mkdir -v results; fi\n")
    f.write("if [ ! -d data ]; then mkdir -v data; fi\n")
    f.write("if [ ! -d config ]; then mkdir -v config; fi\n")
    f.write("if [ ! -d Logs ]; then mkdir -v Logs; fi\n")
    
    #f.write("cp "+MYWORKINGDIR+"config/HistFactorySchema.dtd config/.\n")

    f.write("ls -ltr\n")
    f.write("echo $ROOTSYS \n")
    f.write("which gcc \n")
    f.write("hostname \n")
    f.write("echo '=============' \n")
    
    
    if config.mult==False:
        log=config.logdirname+"job_"+ana+"_"+config.grid+"_"+listToString(points)+"_"+str(counter)+".log"
        option2="grid"+config.grid+","+listToString(points)
        f.write("HistFitter.py "+config.option+" -r "+ana+" -g "+option2+" "+MYWORKINGDIR+myscript+" > "+log+" > /dev/null \n")   
    else:
        #print "Execute separately for each point!"                
        for point in points:
            if config.useNonDegenerateSquarks:
                log="Logs/job_"+ana+"_"+config.grid+"_nonDegenerateSquarks_N"+str(config.numSquarks)+"_"+point+"_"+str(counter)+".log"
            else:
                log="Logs/job_"+ana+"_"+config.grid+"_"+point+"_"+str(counter)+".log"
            option2="grid"+config.grid+","+point
            cmd="HistFitter.py "+config.option+" -r "+ana+" -g "+option2+" "+MYWORKINGDIR+myscript+" > "+log
            f.write("echo "+cmd+" \n")
            f.write(cmd+" \n")
            ana2name=ana.replace(",","")
            f.write("sleep 2; \n")

            
    f.close()
    cmd="chmod u+x "+filename
    subprocess.call(cmd, shell=True)
    
    cmd="qsub -q "+config.queue+" "+filename

    if config.doSubmission==False:
        print cmd
    else:
        subprocess.call(cmd, shell=True)


def writeAndSubmitJobForLyon(config, ana, points, jobdirname, counter):
    filename=jobdirname+"/job_"+"_"+config.grid
    if config.alt:
        filename += "_alt"
    if config.useNonDegenerateSquarks:
        filename += "_nonDegenerateSquarks_N%d" % config.numSquarks

    filename += "_"+ana+"_"+str(counter)+".sh"
    f=open(filename,'w')

    #setup
    f.write("#!/bin/zsh\n")
    f.write("XCWD=$PWD\n")
    f.write("cp -r "+HISTFITTERDIR+" . \n")
    f.write("cp -r "+ZEROLEPTONFITTERDIR+" . \n")
    f.write("cd  "+ZEROLEPTONFITTERDIR.split("/")[-2]+"  \n")
    f.write("source mysetup.sh\n")             
    f.write("/bin/rm -f results/*root*\n")
    f.write("rm -f MY_INPUTS \n")
    f.write("cp -r "+INPUTDIR_LYON+" MY_INPUTS \n")
    f.write("if [ ! -d results ]; then mkdir -v results; fi\n")
    f.write("if [ ! -d data ]; then mkdir -v data; fi\n")
    f.write("if [ ! -d config ]; then mkdir -v config; fi\n")
        
    if config.mult==False:
        option2="grid"+config.grid+","+listToString(points)
        f.write("HistFitter.py "+config.option+" -r "+ana+" -g "+option2+" "+MYWORKINGDIR+myscript+" "+" > /dev/null \n")   
    else:
        #print "Execute separately for each point!"                
        for point in points:

##             #Nikola
##             meff=float(ana.split(",")[1])
##             msquark=float(point.split("_")[0])
##             if config.grid=="SS_direct" and config.opti:
##                 print msquark,meff
##                 if msquark>800 and meff<1300: continue
##                 if msquark<800 and meff>1300: continue 

            option2="grid"+config.grid+","+point
            cmd="HistFitter.py "+config.option+" -r "+ana+" -g "+option2+" "+MYWORKINGDIR+myscript + " > /dev/null "
            f.write("echo "+cmd+" \n")
            f.write(cmd+" \n")
            ana2name=ana.replace(",","")
            f.write("sleep 2; \n")


    #f.write("/bin/mv results/*hypo*root "+MYWORKINGDIR+"results/\n")
    #f.write("/bin/mv results/*upperlimit*root "+MYWORKINGDIR+"results/\n")
    tarname=filename.split("/")[-1]+".tar.gz"
    dirtarname=MYWORKINGDIR+"/results/"
    f.write("cd results/ \n")
    f.write("tar -zcvf "+tarname+" *upperlimit*root *hypo*root \n")
    f.write("mv "+tarname+" "+MYWORKINGDIR+"/results/ \n")
    #f.write("cd "+MYWORKINGDIR+"/results/  \n")
    #f.write("tar -zxvf "+tarname+" \n")
    f.write("rm -f "+tarname+" \n")

#            if config.saveWS:
#                f.write("ls results/ZL2013*/*_model_afterFit.root| awk -F\/ '{print \"mkdir "+MYWORKINGDIR+"/results//\"$2\"; cp \"$0\" "+MYWORKINGDIR+"/results/\"$2\"/\"}'|zsh  \n")#not very nice :-S

            
    f.close()
    cmd="chmod u+x "+filename
    subprocess.call(cmd, shell=True)
    
    log=config.logdirname+"job_"+ana+"_"+config.grid+"_"+"_"+str(counter)+".log"
    #err=MYWORKINGDIR+config.logdirname+"job_"+ana+"_"+config.grid+"_"+"_"+str(counter)+".err"
    err=log
    qsub_option=" -P P_atlas -l ct=20000,vmem=2048M,fsize=17G,sps=1 "
    cmd="qsub "+qsub_option+" -e "+err.replace(",","-")+" -o "+log.replace(",","-")+" "+filename
    #cmd="qsub "+qsub_option+" -e "+log+" "+filename
    
    if config.doSubmission==False:
        print cmd
    else:
        subprocess.call(cmd, shell=True)

def writeAndSubmitJobForNikhef(config, ana, points, jobdirname, counter):
   filename=jobdirname+"/job_"+"_"+config.grid
   if config.only_ul:
       filename += "_UL"
   if config.alt:
       filename += "_alt"
   if config.useNonDegenerateSquarks:
       filename += "_nonDegenerateSquarks_N%d" % config.numSquarks

   filename += "_"+ana+"_"+str(counter)+".sh"
   f=open(filename,'w')

   f.write("#!/bin/zsh\n")
   f.write("echo '============================'\n")
   f.write("date\n")
   f.write("echo '============================'\n")
   f.write("XCWD=$PWD\n")
   f.write("cd "+MYWORKINGDIR+"\n")
   ####f.write("source /afs/cern.ch/sw/lcg/external/gcc/4.3.2/x86_64-slc5/setup.sh\n")
   f.write("which gcc \n")            
   f.write("MYHERE=$PWD\n")            
   ###f.write("cd ../HistFitter-00-00-21/\n")
   f.write("cd "+HISTFITTERDIR+"\n")
   f.write("source setup.sh\n")                        
   f.write("cd "+MYWORKINGDIR+"\n")
   f.write("source setup.sh\n")            
   
   ## TODO symlinks to output dir on glusterfs
   #f.write("if [ ! -d results ]; then mkdir -v results; fi\n")
   #f.write("if [ ! -d data ]; then mkdir -v data; fi\n")
   #f.write("if [ ! -d config ]; then mkdir -v config; fi\n")
   
   #f.write("cp "+MYWORKINGDIR+"config/HistFactorySchema.dtd config/.\n")

   f.write("ls -ltr\n")
   f.write("echo $ROOTSYS \n")
   f.write("which gcc \n")
   f.write("hostname \n")
   f.write("echo '=============' \n")


   if config.mult == False:
       option2 = "grid"+config.grid+","+listToString(points)
       f.write("HistFitter.py "+config.option+" -r "+ana+" -g "+option2+" "+MYWORKINGDIR+myscript+" "+" > /dev/null \n")   
   else:
       print "Execute separately for each point!"                
       for point in points:
           option2="grid"+config.grid+","+point
           cmd="HistFitter.py "+config.option+" -r "+ana+" -g "+option2+" "+MYWORKINGDIR+myscript+" > /dev/null"
           f.write("echo \"point = %s\"\n" % point)
           f.write("echo \""+cmd+"\" \n")
           f.write(cmd+" \n")
           ana2name=ana.replace(",","")
           f.write("sleep 2; \n")
           if config.saveWS:
               f.write("ls results/ZL2013*/*_model_afterFit.root| awk -F\/ '{print \"mkdir "+MYWORKINGDIR+"/\"$2\"; cp \"$0\" "+MYWORKINGDIR+"/\"$2\"/\"}' ") #not very nice :-S

   f.write("echo '============================'\n")
   f.write("date\n")
   f.write("echo '============================'\n")
   f.write("echo \"Done running job!\"\n")
   f.close()
   cmd="chmod u+x "+filename
   subprocess.call(cmd, shell=True)
   
   log = config.logdirname+"/job_"+"_"+config.grid
   if config.alt:
       log += "_alt"
   if config.useNonDegenerateSquarks:
       log += "_nonDegenerateSquarks_N%d" % config.numSquarks

   log += "_"+ana+"_"+str(counter)+".log"
   err = log
   
   # --GJ 18/12/12
   # -d: specify working Directory
   # -N: name of job in qstat
   # -v set envvars var1=foo,var2=bar
   # -t submit array of jobs (see manpage)
   cmd = "qsub -q "+config.queue+" -o "+log+" -j oe "+filename

   if config.N == 1: 
       print cmd
       if config.doSubmission:
           subprocess.call(cmd, shell=True)
   
   return filename

def writeCombinedJobForNikhef(config, jobFilenames):
    i=1
    for c in chunks(jobFilenames, config.N):
        grid = config.grid
        if config.useNonDegenerateSquarks and config.grid == "SS_direct":
            grid += "_nonDegenerateSquarks_N%d" % config.numSquarks
        
        combinedFilename = config.jobdirname+"/job_combined_%s_%d.sh" % (grid, i) 
        logFilename = config.logdirname+"/job_combined_%s_%d.log" % (grid, i) 
        
        if config.only_ul:
            combinedFilename = config.jobdirname+"/job_combined_UL_%s_%d.sh" % (grid, i) 
            logFilename = config.logdirname+"/job_combined_UL_%s_%d.log" % (grid, i) 

        f = open(combinedFilename, "w")
        f.write("#!/bin/sh\n\n")
        for j in c:
            f.write("%s\n" % j)
        f.close()

        subprocess.call("chmod +x %s" % combinedFilename, shell=True)

        cmd = "qsub -q %s -o %s -j oe %s" % (config.queue, logFilename, combinedFilename)

        print cmd 
        if config.doSubmission:
            subprocess.call(cmd, shell=True)
        
        i += 1

###########################################################################
# Main
###########################################################################

def main():
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
    anaList =  allChannelsDict.keys()
   
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

###########################################################################
#Main
###########################################################################
if __name__ == "__main__":
    main()
