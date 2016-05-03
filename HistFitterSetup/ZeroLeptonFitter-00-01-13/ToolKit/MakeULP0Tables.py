#!/usr/bin/env python

from optparse import OptionParser
import sys, os, string, shutil, pickle, subprocess, copy, time

import os
import sys
import shutil

from ChannelsDict import *

from ZLFitterConfig import *
zlFitterConfig = ZLFitterConfig()

doBlind = zlFitterConfig.blindSR
lumi = zlFitterConfig.luminosity

parser = OptionParser()

parser.add_option("-a","--asymptotic", default=False, action="store_true", help="asymptotic")
parser.add_option("-m", "--merge", default=False, action="store_true", help="Merge results")
parser.add_option("-o", "--output-dir", default="results/",
                  help="output dir under which files can be found", metavar="DIR")
(options, args) = parser.parse_args()

#options.output_dir += "/" #to be sure
options.output_dir = os.path.abspath(options.output_dir)

# loop over analysis and compute UL,p0,...
for anaName in finalChannelsDict.keys():

    # names
    fileName = os.path.join(options.output_dir, "ZL_"+anaName+"_Discovery/Fit__Discovery_combined_NormalMeasurement_model.root")
    outName="UL_%s.tex" % (anaName)
    outNameTMP=outName+".tmp"

    # options    
    nPoints = 40
    muRange = 100
    nToys = 3000

    if "2jm" in anaName:
        muRange = 120
    elif "2jt" in anaName:
        muRange = 40
    elif "4jt" in anaName:
        muRange = 40
    elif "5j" in anaName:
        muRange = 25
    elif "6j" in anaName:
        muRange = 20

    option = "-N %d -R %d" % (nPoints, muRange)  
    if options.asymptotic:
        option += " -a"
    else:
        option += " -n %d"%(nToys) 

    cmd = "python $HISTFITTER/scripts/UpperLimitTable.py %s -c combined -p mu_SIG -w %s -l %f -o %s" % (option, fileName, lumi, outNameTMP)   
    #cmd_pval = "HistFitter.py -z -F disc -r %s $ZEROLEPTONFITTER/analysis/ZeroLepton_Run2.py" % ( anaName)

    cmd+="  >&"+anaName+"_UL.log &"
    #cmd_pval+="  >&"+anaName+"_p0.log &"
        
    print cmd
    #print cmd_pval
        
    if not options.merge:
        subprocess.call(cmd, shell=True)
        #subprocess.call(cmd_pval, shell=True)        
    else:
        if os.path.exists(outNameTMP): 

            #filename = os.path.join(options.output_dir, "ZL_{0}_Discovery/ZL_{0}_Discovery_Output_fixSigXSecNominal_hypotest.root".format(anaName))
            #f = ROOT.TFile.Open(filename, "READ")
            #h = f.Get("discovery_htr_DiscoveryMode_SIG")
            #pval = "--"
            #if h and h is not None:
            #    pval = h.NullPValue()
            #f.Close()
            ##discovery_htr_DiscoveryMode_SIG->NullPValue()

            #print pval

            ## replace the last column with the p-value
            #awkCmd = 'BEGIN {FS="&";OFS="&"} $5 != "nan" {print $1,$3,$2,$4, " %.3f \\\\\\\\"}' % pval
            #cmd = "cat {0} | grep combined | grep -v label | sed -e 's/combined/{1}/g' | awk '{3}' > {2}".format(outNameTMP, anaName, outName, awkCmd)
            #print cmd

            cmd="cat "+outNameTMP+"| sed -e 's/combined/"+anaName+"/g' > "+outName
            subprocess.call(cmd, shell=True)
        else:
            print "WARNING: file %s is missing! Waiting for a few seconds." % outNameTMP
            time.sleep(1)


######################################
#merge
######################################
if options.merge:
        
    debut="""\\begin{table}
    \\centering
    \\setlength{\\tabcolsep}{0.0pc}
    \\begin{tabular*}{\\textwidth}{@{\\extracolsep{\\fill}}lccccc}
    \\noalign{\\smallskip}\\hline\\noalign{\\smallskip}
    {\\bf Signal channel}                        & $\\langle\\epsilon{\\rm \\sigma}\\rangle_{\\rm obs}^{95}$[fb]  &  $S_{\\rm obs}^{95}$  & $S_{\\rm exp}^{95}$ & $CL_{B}$ & $p(s=0)$  \\\\
    \\noalign{\\smallskip}\\hline\\noalign{\\smallskip}
    %%
    """

    cmd = """cat  UL_SR*.tex | grep SR | grep \" &\" | sort -n"""
    res = os.popen(cmd).readlines()
    milieu=""
    for aLine in res:
        milieu+=aLine

    fin="""
    %
    \\noalign{\\smallskip}\\hline\\noalign{\\smallskip}
    \\end{tabular*}
    \\caption[Breakdown of upper limits.]{
    Left to right: 95\\% CL upper limits on the visible cross section
    ($\\langle\\epsilon\\sigma\\rangle_{\\rm obs}^{95}$) and on the number of
    signal events ($S_{\\rm obs}^{95}$ ).  The third column
    ($S_{\\rm exp}^{95}$) shows the 95\\% CL upper limit on the number of
    signal events, given the expected number (and $\\pm 1\\sigma$
    excursions on the expectation) of background events.
    The last two columns
    indicate the $CL_B$ value, i.e. the confidence level observed for
    the background-only hypothesis, and the discovery $p$-value ($p(s = 0)$). 
    \\label{table.results.exclxsec.pval.upperlimit}}
    \\end{table}\n\n"""

    f=open("ULp0.tex","w")
    f.write(debut+milieu+fin)
    f.close()
