#!/usr/bin/env python

import sys
import math
import copy
import pickle
import subprocess
import os
from optparse import OptionParser
from Grid import *
from multiprocessing import *

import ROOT
from ROOT import *
ROOT.gROOT.SetBatch(True) # Turn off online histogram drawing


from ChannelsDict import *
from ZLFitterConfig import *
zlFitterConfig = ZLFitterConfig() 

parser = OptionParser()
parser.add_option("-d", "--discovery",action="store_true", default=False)
parser.add_option("-o", "--outputDir", help="", default = "Outputs/")
parser.add_option("-i", "--inputDir", help="", default = "../../results/")
parser.add_option("-g", "--gridName", help="", default = "GG_direct")
parser.add_option("-s", "--doSyst", help="", default = False,action="store_true")
parser.add_option("-p", "--printOnly", help="", default = False,action="store_true")
parser.add_option("-n", "--nbProcess", default="4")
(options, args) = parser.parse_args()


interpretation="m0:m1"
format="%f_%f"
if options.gridName.find("GG_onestepCC")>=0 or options.gridName.find("SM_GG_N2")>=0:
    interpretation="m0:m1:m2"
    format="%f_%f_%f"

resList=["Nominal"]
if options.doSyst:
    resList+=["Up","Down"]


channelList=finalChannelsDict.keys()

nbProcess=int(options.nbProcess)
if len(channelList)<=nbProcess:
    nbProcess=len(channelList)



nbFilePerProcess=int(len(channelList)/nbProcess)

print len(channelList)
print options.nbProcess,nbProcess
print nbFilePerProcess

splittedChannelList = [channelList[i:i+nbFilePerProcess] for i in xrange(0, len(channelList), nbFilePerProcess)]





counter=0
for myList in splittedChannelList:
    counter+=1
    filename="get"+options.gridName+str(counter)+".sh"
    f=open(filename,"w")
    for anaName in myList:
        for res in resList:
            outName= options.outputDir+"/ZL_"+anaName+"_"+allGrids[options.gridName].basename+"_Output_fixSigXSec"+res+"_hypotest.root "
            fitType="hypo"
            if options.discovery:
                fitType="hypo_discovery"

            f.write("hadd -f "+outName+" "+options.inputDir+"ZL*"+allGrids[options.gridName].basename+"*/*"+anaName+"_"+"*fixSigXSec"+res+"_hypotest.root;\n")
            f.write("./CollectAndWriteHypoTestResults.py -F "+outName+"  -f "+fitType+"_"+allGrids[options.gridName].basename+"_"+format+" -I " +interpretation+" -c 1 ;\n")

    print "================="
    f.close()
    if not options.printOnly:        
        subprocess.call("chmod u+x ./"+filename+"", shell=True)
        subprocess.call("nohup ./"+filename+"&", shell=True)

