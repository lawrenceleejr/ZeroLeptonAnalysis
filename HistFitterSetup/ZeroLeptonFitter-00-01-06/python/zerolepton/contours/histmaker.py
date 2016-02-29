# Based on m0_vs_m12, but now a proper class

import imp
import os

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

ROOT.gSystem.Load('{0}/lib/libSusyFitter.so'.format(os.getenv('HISTFITTER'))) # temporary for OS X 10.11
ROOT.gInterpreter.ProcessLine('#include "{0}/src/DrawUtils.h" '.format(os.getenv('HISTFITTER')))
ROOT.gInterpreter.ProcessLine('#include "{0}/src/StatTools.h" '.format(os.getenv('HISTFITTER')))

class Histogram:
    def __init__(self, variable, interpretation, name, title, cuts):
        self.variable = variable
        self.interpretation = interpretation
        self.name = name
        self.title = title
        self.cuts = cuts

        if self.variable == "" or self.interpretation == "":
            raise ValueError("cannot construct projection")

        (x,y) = self.interpretation.split(":")
        self.projection = "{0}:{1}:{2}".format(variable, y, x)

class HistMaker:
    def __init__(self, inputFilename="", interpretation="", outputDir="Outputs/"):
    # We don't use any funky metadata from GridConfig, to be as minimal as possible

        self.inputFilename = inputFilename
        self.interpretation = interpretation
        self.outputDir = outputDir

        self.histograms = []
        self.initDefaultHistograms()

    def addHistogram(self, variable, name, title, cuts):
        self.histograms.append(Histogram(variable, self.interpretation, name, title, cuts))

    def initDefaultHistograms(self):
        self.histograms.append(Histogram("p1", self.interpretation, "hclPmin2" , "Observed CLsplusb", "p1>=0 && p1<=1"))
        self.histograms.append(Histogram("StatTools::GetSigma(p1)", self.interpretation, "sigp1" , "One-sided significance of CLsplusb", "(p1>0 && p1<=1)"))
        self.histograms.append(Histogram("CLs", self.interpretation, "sigp1clsf" , "Observed CLs", "p1>0 && p1<=1"))
        self.histograms.append(Histogram("StatTools::GetSigma( CLs )", self.interpretation, "sigp1clsf" , "One-sided significalce of observed CLs", "p1>0 && p1<=1"))
        self.histograms.append(Histogram("StatTools::GetSigma( CLsexp )", self.interpretation, "sigp1expclsf" , "One-sided significalce of expected CLs", "p1>0 && p1<=1"))
        self.histograms.append(Histogram("StatTools::GetSigma(clsu1s)", self.interpretation, "sigclsu1s" , "One-sided significalce of expected CLs (+1 sigma)", "clsu1s>0"))
        self.histograms.append(Histogram("StatTools::GetSigma(clsd1s)", self.interpretation, "sigclsd1s" , "One-sided significalce of expected CLs (-1 sigma)", "clsd1s>0"))
        self.histograms.append(Histogram("upperLimit", self.interpretation, "upperLimit" , "upperlimit","1"))
        self.histograms.append(Histogram("xsec", self.interpretation, "xsec" , "xsec","1"))
        self.histograms.append(Histogram("excludedXsec", self.interpretation, "excludedXsec" , "excludedXsec","1"))

    def readTree(self):
        self.inputTree = None

        # our description file should be stored with the file
        inputDir = os.path.dirname(self.inputFilename)
        summary_harvest_tree_description = imp.load_source('summary_harvest_tree_description', '{0}/summary_harvest_tree_description.py'.format(inputDir))

        dummy, description = summary_harvest_tree_description.treedescription()
        self.inputTree = summary_harvest_tree_description.harvesttree(self.inputFilename)

    def process(self, forceRecreate=False):
        if self.inputFilename is None or self.inputFilename == "":
            raise ValueError("Need an input file")

        outputFilename = "{0}/{1}.root".format(self.outputDir, os.path.basename(self.inputFilename))
        if not forceRecreate and (os.path.exists(outputFilename) and os.path.getmtime(outputFilename) > os.path.getmtime(self.inputFilename)):
            print("HistMaker.process(): output file ({0}) exists and is newer than input file {1} - skipping".format(os.path.basename(outputFilename), os.path.basename(self.inputFilename)))
            return

        self.readTree()
        f = ROOT.TFile.Open(outputFilename, "RECREATE")
        f.cd()

        for h in self.histograms:
            self.writeHistogram(h)

        f.Close()

        print("Wrote histograms to {0}".format(os.path.basename(outputFilename)))

    def writeHistogram(self, histogram):
        h = ROOT.DrawUtil.triwsmooth(self.inputTree, histogram.projection,  histogram.name, histogram.title, histogram.cuts)
        if h: # C++ can return NULL
            h.Write()
