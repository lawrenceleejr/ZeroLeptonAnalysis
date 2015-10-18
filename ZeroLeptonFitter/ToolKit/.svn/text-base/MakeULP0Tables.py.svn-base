#!/usr/bin/env python

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.Reset()
ROOT.gROOT.SetBatch(True)
ROOT.gSystem.Load("libSusyFitter.so")

from optparse import OptionParser
from ROOT import TFile, RooWorkspace, TObject, TString, RooAbsReal, RooRealVar, RooFitResult, RooDataSet, RooAddition, RooArgSet, RooFormulaVar, RooAbsData, RooRandom
from ROOT import *
from ROOT import Util, TMath, TMap, RooExpandedFitResult
import sys, os, string, shutil, pickle, subprocess, copy, time

ROOT.gROOT.SetBatch(True)

################################################################################
import os
import sys

################################################################################
from allChannelsDict import *

from ZLFitterConfig import *
zlFitterConfig = ZLFitterConfig()

doBlind=zlFitterConfig.blindSR
lumi=zlFitterConfig.luminosity

################################################################################





parser = OptionParser()

parser.add_option("-a","--asymptotic", default=False, action="store_true", help="asymptotic")
parser.add_option("-m", "--merge", default=False, action="store_true", help="Merge results")
parser.add_option("-o", "--output-dir", default="results/",
                  help="output dir under which files can be found", metavar="DIR")
(options, args) = parser.parse_args()
options.output_dir += "/" #to be sure


#loop over analysis and compute UL,p0,...
for anaName in allChannelsDict.keys():

    #names
    fileName = options.output_dir+"/ZL_"+anaName+"_Discovery/Fit__Discovery_combined_NormalMeasurement_model.root"
    outName="UL_%s.tex" % (anaName)
    outNameTMP=outName+".tmp"

    #options    
    nPoints = 40
    muRange = 100
    nToys=3000
    option = "" #-N %d -R %d" % (nPoints, muRange)  #ATT: Need to add again NPoints and muRange
    if options.asymptotic:
        option += " -a"
    else:
        option += "-n %d"%(nToys) 


    cmd = "python $HISTFITTER/scripts/UpperLimitTable.py %s -c combined -p mu_SIG -w %s -l %d -o %s" % (option, fileName, lumi, outNameTMP)   
    cmd_pval = "HistFitter.py -z -F disc -r %s $ZEROLEPTONFITTER/analysis/ZeroLepton_Run2.py" % ( anaName)

    cmd+="  >&"+anaName+"_UL.log &"
    cmd_pval+="  >&"+anaName+"_p0.log &"

    print cmd
    print cmd_pval

    if not options.merge:
        subprocess.call(cmd, shell=True)
        subprocess.call(cmd_pval, shell=True)        
    else:
        if os.path.exists(outNameTMP): 
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
    \\begin{center}
    \\setlength{\\tabcolsep}{0.0pc}
    \\begin{tabular*}{\\textwidth}{@{\\extracolsep{\\fill}}lccccc}
    \\noalign{\\smallskip}\\hline\\noalign{\\smallskip}
    {\\bf Signal channel}                        & $\\langle\\epsilon{\\rm \\sigma}\\rangle_{\\rm obs}^{95}$[fb]  &  $S_{\\rm obs}^{95}$  & $S_{\\rm exp}^{95}$ & $CL_{B}$ & $p(s=0)$  \\\\
    \\noalign{\\smallskip}\\hline\\noalign{\\smallskip}
    %%
    """

    cmd = """cat  UL_SR*.tex| grep SR| grep \" &\"|sort -nr"""
    res = os.popen(cmd).readlines()
    milieu=""
    for aLine in res:
        milieu+=aLine

    fin="""
    %
    \\noalign{\\smallskip}\\hline\\noalign{\\smallskip}
    \\end{tabular*}
    \\end{center}
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
    \\end{table}"""

    f=open("ULp0.tex","w")
    f.write(debut+milieu+fin)
    f.close()
