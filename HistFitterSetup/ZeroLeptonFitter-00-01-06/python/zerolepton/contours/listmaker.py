import ctypes
import os
import subprocess
import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

ROOT.gSystem.Load('{0}/lib/libSusyFitter.so'.format(os.getenv('HISTFITTER'))) # temporary for OS X 10.11

from CollectAndWriteHypoTestResults import CollectAndWriteHypoTestResults

class ListMaker:
    def __init__(self, inputFilename="", format="", interpretation="", cutStr="", outputDir="Outputs/"):
        # We don't use any funky metadata from GridConfig, to be as minimal as possible

        self.inputFilename = inputFilename
        self.format = format
        self.interpretation = interpretation
        self.cutStr = cutStr
        self.outputDir = outputDir

        self.automaticRejection = False;
        self.prefix = ""

    def writeList(self):
        if self.inputFilename is None or self.inputFilename == "":
            raise ValueError("Need an input file")

        if self.format == "":
            raise ValueError("No format specified")
        
        if self.interpretation == "":
            raise ValueError("No interpretation specified")
 
        if self.cutStr == "":
            raise ValueError("No cut string specified")

        CollectAndWriteHypoTestResults( self.inputFilename, self.format, self.interpretation, self.cutStr, int(self.automaticRejection), self.outputDir, self.prefix )

