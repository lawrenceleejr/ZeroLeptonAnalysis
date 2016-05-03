# Module for plotting

import copy
import datetime
import os
import re
from ..contours.utils import getFileList
from ..contours.data import ContourData

import numpy as np
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt

import matplotlib.cm as cmx
import matplotlib.colors as colors

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
#rc('text', usetex=True)

import scipy.interpolate
import scipy.ndimage

import pprint

def get_cmap(N):
    '''Returns a function that maps each index in 0, 1, ... N-1 to a distinct 
    RGB color.'''
    color_norm  = colors.Normalize(vmin=0, vmax=N-1)
    scalar_map = cmx.ScalarMappable(norm=color_norm, cmap='hsv') 
    def map_index_to_rgb_color(index):
        return scalar_map.to_rgba(index)
    return map_index_to_rgb_color

class OptimisationPlot:
    # Class to make an optimisation plot. Give it an input dir and it will combine all the files.
    
    def __init__(self, gridConfig, outputFilename, inputDir):
        self.gridConfig = gridConfig
        self.outputFilename = outputFilename
        self.inputDir = inputDir

        self.contourData = None
        pass

    def createOutputDir(self):
        dirname = os.path.dirname(self.outputFilename)
        if os.path.exists(dirname):
            return

        os.makedirs(dirname)

    def writePreHook(self):
        if self.contourData is not None:
            return

        self.findFiles()
        self.contourData = ContourData(self.gridConfig, self.files)

    def findFiles(self):
        print("Finding files for plot")
        self.files = [f for f in getFileList(self.inputDir, cachefile=None, noWait=True) if f.endswith("json") and not "combined" in f and not "filesByRegion" in f]
        pass

    def write(self):
        self.writePreHook()

        for cut in self.contourData.filteredCombinedData:
            # Add cut to the output filename
            (outputFilename, ext) = os.path.splitext(self.outputFilename)
            outputFilename = "{0}_{1}_{2:.0f}{3}".format(outputFilename, cut.key, cut.value, ext)

            plt.ioff()
            plt.figure(figsize=(8,6))
            #plt.yscale('log')
            plt.ylim([0,1.0])
            plt.figtext(0.05, 0.96, 'Cut: {0} = {1:.0f}'.format(cut.key, cut.value), color='grey', size='small')
            plt.figtext(0.05, 0.93, 'Plot written at {:%d/%m/%Y %H:%M}'.format(datetime.datetime.now()), color='grey', size='small')

            for f in self.contourData.contributingRegionsFiltered[cut]:
                data = self.contourData.filteredData[f][cut]
                label = filterLabel(f, self.gridConfig)

                if not cut.isSimple():
                    plt.xticks( np.arange(len(data)), ["%d_%d" % (x[self.gridConfig.x], x[self.gridConfig.y]) for x in data.values()])
                    xLabel = "Grid point"
                else:
                    var = self.gridConfig.x
                    if cut.key == var: 
                        var = self.gridConfig.y
                    xLabel = var
                    plt.xticks( np.arange(len(data)), ["%d" % (x[var]) for x in data.values()])
                print [x[self.contourData.combineOn] for x in data.values()]
                plt.plot( [x[self.contourData.combineOn] for x in data.values()], label=label )

                plt.plot( [0.05 for x in data.values()], color='r', linestyle='--', linewidth=2)

            plt.title('Optimisation result', weight='bold')
            plt.xlabel(xLabel, position=(1,0), horizontalalignment='right', weight='bold')
            plt.ylabel('p0exp', position=(0,1), horizontalalignment='right', weight='bold')

            legend = plt.legend(loc='upper right', shadow=False, fontsize='x-small')

            if not os.path.exists(os.path.dirname(outputFilename)):
                print("Creating output dir {0}".format(os.path.dirname(outputFilename)))
                os.makedirs(os.path.dirname(outputFilename))

            plt.savefig(outputFilename, close=False, verbose=True)
            print("\n=> Wrote result to {0}".format(outputFilename))

        pass

    def writeContour(self):
        key = "CLsexp"
        if self.gridConfig.useDiscovery:
            key = "p0exp"

        self.writePreHook()

        x = np.array([p[self.gridConfig.x] for p in self.contourData.combinedData.values() if p[self.contourData.combineOn] is not None])
        y = np.array([p[self.gridConfig.y] for p in self.contourData.combinedData.values() if p[self.contourData.combineOn] is not None])
        z = np.array([p[self.contourData.combineOn] for p in self.contourData.combinedData.values() if p[self.contourData.combineOn] is not None])

        if x.size == 0 or y.size == 0 or z.size == 0:
            print("No data points for for contour")
            return

        # Set up a regular grid of interpolation points
        xMin = 0
        yMin = 0
        xMax = x.max()
        yMax = y.max()

        # vertical levels array for the plot
        v = np.linspace(0, 1.0, 21, endpoint=True)
        plt.ioff()
        fig = plt.figure(figsize=(20,6))
        ax = plt.subplot(111)

        triang = matplotlib.tri.Triangulation(x, y)
        CS = plt.tricontour(triang, z, v, linewidths=3.5, colors=('blue'), levels=[0.05])
        plt.tricontourf(triang, z, v, cmap=plt.cm.jet_r)
        CB = plt.colorbar(ticks=v)

        lines = [CS.collections[0]]
        labels = ["Combined"]

        cmap = get_cmap(len(self.contourData.contributingRegions))
        i=0
        for f in self.contourData.contributingRegions:
            i+=1
            rX = np.array([p[self.gridConfig.x] for p in self.contourData.data[f].values() if p[self.contourData.combineOn] is not None])
            rY = np.array([p[self.gridConfig.y] for p in self.contourData.data[f].values() if p[self.contourData.combineOn] is not None])
            rZ = np.array([p[self.contourData.combineOn] for p in self.contourData.data[f].values() if p[self.contourData.combineOn] is not None])
            
            triang = matplotlib.tri.Triangulation(rX, rY)
            # we have exactly 1 contour, so set our tuple to that
            rCS = plt.tricontour(triang, rZ, v, linewidths=1.5, colors=(cmap(i),), linestyle='--', levels=[0.05])

            label = filterLabel(f, self.gridConfig)
            labels.append(label)
            lines.append(rCS.collections[0])

        plt.title('Optimisation result', weight='bold')
        plt.xlabel('%s [GeV]' % (self.gridConfig.x), position=(1,0), horizontalalignment='right', weight='bold')
        plt.ylabel('%s [GeV]' % (self.gridConfig.y), position=(0,1), horizontalalignment='right', weight='bold')

        (outputFilename, ext) = os.path.splitext(self.outputFilename)
        outputFilename = "%s.contour%s" % (outputFilename, ext)

        # Shrink current axis by 50%
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.5, box.height])

        # Put a legend to the right of the current axis
        ax.legend(lines, labels, loc='center left', bbox_to_anchor=(1, 0.5), shadow=False, fontsize='x-small')

        #legend = plt.legend(lines, labels, loc='upper right', shadow=False, fontsize='x-small')
        
        if not os.path.exists(os.path.dirname(outputFilename)):
            print("Creating output dir {0}".format(os.path.dirname(outputFilename)))
            os.makedirs(os.path.dirname(outputFilename))

        plt.savefig(outputFilename, close=False, verbose=True, bbox_inches='tight')
        print("\n=> Wrote contour to {0}".format(outputFilename))

def filterLabel(f, gridConfig):
    label = os.path.basename(f).replace("_harvest_list.json","")

    # strip out our name
    label = label.replace(gridConfig.name, "")
    label = label.replace(gridConfig.format_discovery, "")
    label = label.replace(gridConfig.format, "")
    label = label.replace("_discovery__1", "")
    label = label.replace("__", "_")
    label = label.replace("_discovery_1", "")
    label = label.replace("MET_over_meff", "MET/meff")
    label = label.replace("jetpt","j")

    # remove trailing zeroes after decimals in the output. stolen from stackoverflow.
    return (re.sub(r'(?<=\.)([0-9]+?)(0+)(?=\D|$)',lambda m:m.group(1)+''*len(m.group(2)), label))
