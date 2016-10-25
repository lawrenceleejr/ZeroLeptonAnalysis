#!/usr/local/bin/python

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

doBlind=False
lumi=20.3

################################################################################

import os
import sys

# from AnaList import *

parser = OptionParser()
parser.add_option("--asymptotic", default=False, action="store_true", help="asymptotic")
parser.add_option("-o", "--output-dir", default="results/",
                  help="output dir under which files can be found", metavar="DIR")
(options, args) = parser.parse_args()
options.output_dir += "/" #to be sure

#loop over analysis and compute UL,p0,...
for anaShortname in ["SR1"]:
    # anaShortname = anaShortname

    cmd = "HistFitter.py -w -t -f -r %s %s/ToolKit/simpleUL/SimpleUL.py" % (anaShortname, os.getenv("ZEROLEPTONFITTER") )
    print cmd
    subprocess.call(cmd, shell=True)

    fileName = "%s/SimpleUL_%s/SPlusB_combined_NormalMeasurement_model.root" % (options.output_dir, anaShortname)

    outName="UL_%s.tex" % (anaShortname)
    outNameTMP=outName+".tmp"

    nPoints = 20
    nToys = 10000

    if anaShortname == "SR1":
        muRange = 3000
        nPoints = 40
    
    if anaShortname == "SR4jl":
        nPoints = 50
    
    if anaShortname == "SR2jW":
        muRange = 10
    
    if anaShortname == "SR2jm" or anaShortname == "SR5j":
        muRange = 300

    if anaShortname == "SR4jl-":
        muRange = 500
    
    if anaShortname == "SR3j" or anaShortname == "SR4jt" or anaShortname == "SR6jt" or anaShortname == "SR6jt+":
        muRange = 20
    
    if anaShortname == "SR4jW": 
        muRange = 40
    
    if anaShortname == "SR4jm":
        muRange = 40
    
    option = "-N %d -R %d" % (nPoints, muRange) 

    if options.asymptotic:
        option += " -a"#asymptotic instead of toys

    cmd = "python $ZEROLEPTONFITTER/scripts/UpperLimitTable.py %s -c combined -n %d -p mu_SIG -w %s -l %.3f -o %s" % (option, nToys, fileName, lumi, outNameTMP)   
    cmd_pval = "cd %s/.. && HistFitter.py -z -r %s $ZEROLEPTONFITTER/ToolKit/simpleUL/SimpleUL.py && cd -" % (options.output_dir, anaShortname)

    print cmd,">&"+anaShortname+".log &"
    subprocess.call(cmd, shell=True)
        
    if os.path.exists(outNameTMP): 
        cmd="cat "+outNameTMP+"| sed -e 's/combined/"+anaShortname+"/g' > "+outName
        subprocess.call(cmd, shell=True)
    else:
        print "WARNING: file %s is missing! Waiting for a few seconds." % outNameTMP
        time.sleep(3)

######################################
#merge
######################################

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
