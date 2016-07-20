#!/usr/bin/env python

#You'll have to have matplotlib and root setup side-by-side
#
#> localSetupSFT --cmtConfig=x86_64-slc6-gcc48-opt releases/LCG_79/pytools/1.9_python2.7,releases/LCG_79/pyanalysis/1.5_python2.7
#> lsetup root

import ROOT

import matplotlib as mpl
mpl.use('pdf')
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate

import json

import argparse
import math


parser = argparse.ArgumentParser()
parser.add_argument("--inputFile", type=str, help="input harvest file", default = "Outputs/8.3ifb_RJigsaw/GG_direct/GG_direct_combined_fixSigXSecNominal__1_harvest_list")
parser.add_argument("--outputFile", type=str, help="output ROOT file", default = "output.root")
parser.add_argument("--interpolation", type=str, help="type of interpolation", default = "linear")
parser.add_argument("--level", type=float, help="contour level output", default = ROOT.RooStats.PValueToSignificance( 0.05 ))
args = parser.parse_args()


def main():

	# Step 1 - Read in harvest list in either text or json format and dump it into a dictionary
	tmpdict = harvestToDict( args.inputFile )

	addZerosToDict(tmpdict,maxyvalue = 1000)

	# Step 2 - Interpolate the fit results
	print ">>> Interpolating mass plane"
	(xi,yi,zi) = interpolateMassPlane( tmpdict , args.interpolation )


	f = ROOT.TFile(args.outputFile,"recreate")

	# from array import array

	# if np.isnan(zi["CLsexp"]).any():
	# 	print "something's nan!"
	# if np.isinf(zi["CLsexp"]).any():
	# 	print "something's inf!"

	# gr = ROOT.TGraph2D(len(xi),
	# 	array('f',xi),
	# 	array('f',yi),
	# 	array('f',zi["CLsexp"] ) )


	# gr.Write()
	# f.Close()
	# return

	print ">>> Writing contours out"
	# Step 3 -
	for whichEntry in ["CLs","CLsexp","clsu1s","clsu2s","clsd1s","clsd2s"]:
		contourList = getContourPoints(xi,yi,zi[whichEntry], args.level)

		for i,contour in enumerate(contourList):
			if (contour[1]>contour[0]).all():
				continue
			graph =	ROOT.TGraph(len(contour[0]), contour[0].flatten('C'), contour[1].flatten('C') )
			graph.Write("%s_Contour_%d"%(whichEntry,i)  )

	print ">>> Closing file"

	f.Write()
	f.Close()


def harvestToDict( harvestInputFileName = "" ):
	print ">>> entering harvestToDict()"

	massPlaneDict = {}

	harvestInput = open(harvestInputFileName,"r")


	from summary_harvest_tree_description import treedescription
	dummy,fieldNames = treedescription()
	fieldNames = fieldNames.split(':')

	if ".json" in harvestInputFileName and 0:
		print ">>> Interpreting json file"

		with open(harvestInput) as inputJSONFile:
			inputJSONFile = json.load(inputJSONFile)

	else:
		print ">>> Interpreting text file"

		for massLine in harvestInput.readlines():
			values = massLine.split()
			values = dict(zip(fieldNames, values))

			massPoint = (  float(values["m0/F"])  , float(values["m12/F"])   )

			massPlaneDict[massPoint] = {
				"CLs":        ROOT.RooStats.PValueToSignificance( float(values["CLs/F"])     ) ,
				"CLsexp":     ROOT.RooStats.PValueToSignificance( float(values["CLsexp/F"])  ) ,
				"clsu1s":     ROOT.RooStats.PValueToSignificance( float(values["clsu1s/F"])  ) ,
				"clsu2s":     ROOT.RooStats.PValueToSignificance( float(values["clsu2s/F"])  ) ,
				"clsd1s":     ROOT.RooStats.PValueToSignificance( float(values["clsd1s/F"])  ) ,
				"clsd2s":     ROOT.RooStats.PValueToSignificance( float(values["clsd2s/F"])  ) ,
			}

	return massPlaneDict


def addZerosToDict(mydict, maxyvalue = 0):
	for x in np.linspace( 0, 2000, 100 ):
		mydict[(x,x)] = {
				"CLs":    0,
				"CLsexp": 0,
				"clsu1s": 0,
				"clsu2s": 0,
				"clsd1s": 0,
				"clsd2s": 0,
			}

	if maxyvalue:
		for x in np.linspace( 0, 2000, 100 ):
			mydict[(x,maxyvalue)] = {
					"CLs":    0,
					"CLsexp": 0,
					"clsu1s": 0,
					"clsu2s": 0,
					"clsd1s": 0,
					"clsd2s": 0,
				}


	# return mydict


def interpolateMassPlane(massPlaneDict = {}, interpolationFunction = "linear"):

	massPoints = massPlaneDict.keys()
	massPointsValues = massPlaneDict.values()

	x =   list( zip( *massPoints )[0] )
	y =   list( zip( *massPoints )[1] )

	zValues = {}
	for whichEntry in ["CLs","CLsexp","clsu1s","clsu2s","clsd1s","clsd2s"]:
		zValues[whichEntry] = [ tmpEntry[whichEntry] for tmpEntry in massPointsValues]


	# print zValues



	if np.isinf( zValues["CLs"]  ).any():
		print "infs!"

	while np.isinf( zValues["CLs"]  ).any():
		myindex = np.isinf( zValues["CLs"]  ).tolist().index(True)
		x.pop(myindex)
		y.pop(myindex)

		for k,v in zValues.iteritems():
			zValues[k].pop(myindex)

	# for i in xrange(len(zValues["CLs"]) ):
	# 	if i-1 > len(zValues["CLs"]):
	# 		break
	# 	if np.isinf(zValues["CLs"][i]):
	# 		x.pop(i)
	# 		y.pop(i)
	# 		for k,v in zValues.iteritems():
	# 			zValues[k].pop(i)
	# 		i = i-1
	if np.isinf( zValues["CLs"]  ).any():
		print "still infs!"



	xArray = np.array(x)
	yArray = np.array(y)
	zValuesArray = {}
	for k,v in zValues.iteritems():
		zValuesArray[k] = np.array( v )

	xi, yi = np.linspace(xArray.min(), xArray.max(), 100), np.linspace(yArray.min(), yArray.max(), 100)
	xi, yi = np.meshgrid(xi, yi)

	zi = {}
	for whichEntry in ["CLs","CLsexp","clsu1s","clsu2s","clsd1s","clsd2s"]:
		print ">>>> Interpolating %s"%whichEntry
		print len(x)
		print len(zValues[whichEntry])
		rbf = LSQ_Rbf(x, y, zValues[whichEntry], function=interpolationFunction)
		print "setting zi"
		zi[whichEntry] = rbf(xi, yi)

	return (xi,yi,zi)
	# return (x,y,zValues)



def getContourPoints(xi,yi,zi,level ):

	c = plt.contour(xi,yi,zi, [level])
	contour = c.collections[0]

	contourList = []

	for i in xrange( len(contour.get_paths() ) ):
		v = contour.get_paths()[i].vertices

		x = v[:,0]
		y = v[:,1]

		contourList.append( (x,y) )

	return contourList



class LSQ_Rbf(scipy.interpolate.Rbf):

    def __init__(self, *args, **kwargs):
        self.xi = np.asarray([np.asarray(a, dtype=float).flatten()
                           for a in args[:-1]])
        self.N = self.xi.shape[-1]
        self.di = np.asarray(args[-1]).flatten()

        if not all([x.size == self.di.size for x in self.xi]):
            raise ValueError("All arrays must be equal length.")

        self.norm = kwargs.pop('norm', self._euclidean_norm)
        r = self._call_norm(self.xi, self.xi)
        self.epsilon = kwargs.pop('epsilon', None)
        if self.epsilon is None:
            self.epsilon = r.mean()
        self.smooth = kwargs.pop('smooth', 0.0)

        self.function = kwargs.pop('function', 'multiquadric')

        # attach anything left in kwargs to self
        #  for use by any user-callable function or
        #  to save on the object returned.
        for item, value in kwargs.items():
            setattr(self, item, value)

        self.A = self._init_function(r) - np.eye(self.N)*self.smooth
        # use linalg.lstsq rather than linalg.solve to deal with
        # overdetermined cases
        self.nodes = np.linalg.lstsq(self.A, self.di)[0]





if __name__ == "__main__":
	main()
