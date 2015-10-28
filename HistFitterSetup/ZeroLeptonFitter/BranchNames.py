#!/usr/bin/env python

#------------------------------------------------
# A script to take a reference D3PD and new D3PD
# and compare branch contents (in the 'susy'
# TTree) by:
#  1 - printing out the number of branches
#  2 - comparing the difference between the content
#
# Louise Heelan
# May 2011
#-----------------------------------------------


import ROOT
import sys

if (len(sys.argv) != 2):
    print "ERROR: python BranchNames.py needs one arguments"
    print "ERROR: ./BranchNames.py needs two arguments"
    print "Usage: ./BranchNames.py <root file> "
    sys.exit(0)


fileName = sys.argv[1]

f = ROOT.TFile.Open(fileName)
t = f.Get('Top_SRAll')



listOfBranches = t.GetListOfBranches()
numBranches = listOfBranches.GetEntries()



print "------------------------------------------------------------"
print "Number of branches = ", numBranches
print "Branch names ...."
# 1. Find the new branches
# loop through new branches and find in ref branches
for br in range (0,numBranches):
     thisBranchName = (listOfBranches.At(br)).GetName()
     print thisBranchName

     
     pass # end loop over new

