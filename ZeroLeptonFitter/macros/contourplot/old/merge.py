#!/usr/bin/env python
# usage : 

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
# Import Modules                                                             # 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
import sys, os, string, shutil,pickle,subprocess

import ROOT
ROOT.gROOT.Reset()
ROOT.gROOT.SetBatch(True)

#=========================================================================

from summary_harvest_tree_description import treedescription
dummy,description = treedescription()
allpar = description.split(':')
print dummy,description





myMap={}
selectpar="CLsexp"
par1="m0"
par2="m12"
xsecs = ["Nominal", "Up", "Down"]
regions = ["SRAmedium", "SRBmedium", "SRCloose", "SRCmedium", "SREloose", "SREmedium"]
#regions = ["SRCmedium"]

for xsec in xsecs:
    myMap = {}
    #for region in regions:
        #filename="ZL2012_gluino_stop_"+region+"_fixSigXSec"+xsec+"_hypotest__1_harvest_list"
    for filename in os.popen("ls *gluino_stop_SR*"+xsec+"*_harvest_list" ).readlines():
        filename=filename.strip()
        print filename

        f = open(filename,'r')
        for line in f.readlines():
            vals = line.strip().split(' ')
            if len(allpar)!=len(vals): 
                print 'PRB!!!!!!!!!!!!!!!!!!!!'
                print len(allpar),len(vals)
                continue
            pval =  float( vals[allpar.index(selectpar)])
            par1 =  float( vals[allpar.index("m0")])
            par2 =  float( vals[allpar.index("m12")])

            #print "%s-%s: (%d, %d) -> %s" % (region, xsec, par1, par2, pval)

            key=(par1,par2)
                
            if key not in myMap.keys():
                myMap[key]=[pval,line]
            else:
                if pval<myMap[key][0]:
                    myMap[key][0]=pval
                    myMap[key][1]=line



    #print myMap

    f=open("combined_gluino_stop"+xsec+"__1_harvest_list","w")
    for key,info in myMap.items():
        print key
        f.write(info[1])
    f.close()
    
