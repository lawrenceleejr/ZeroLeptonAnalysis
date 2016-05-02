#!/usr/bin/python


import os, sys
import glob
import ROOT

print sys.argv

folder = sys.argv[1]

regions = [
"SR2jl",
"SR2jm",
"SR2jt",
"SR4jt",
"SR5j",
"SR6jm",
"SR6jt",

"SRJigsawSRG1a",
"SRJigsawSRG1b",
"SRJigsawSRG1c",
"SRJigsawSRG2a",
"SRJigsawSRG2b",
"SRJigsawSRG2c",
"SRJigsawSRG3a",
"SRJigsawSRG3b",
"SRJigsawSRG3c",

"SRJigsawSRS1a",
"SRJigsawSRS1b",
"SRJigsawSRS2a",
"SRJigsawSRS2b",
"SRJigsawSRS3a",
"SRJigsawSRS3b",

"SRJigsawSRC1",
"SRJigsawSRC2",
"SRJigsawSRC3",
"SRJigsawSRC4",
"SRJigsawSRC5",

]

def isFileCorrupted(filename) :
	ROOT.gEnv.SetValue("TFile.Recover=0")
#	print "checking file : " + filename
	rfile = ROOT.TFile(filename)
	if not rfile : return True
	return rfile.IsZombie()

grids = ["GG_direct","SS_direct"]

grids = [folder.split("-")[1] ]

os.system("mkdir {0}/combinedResults".format(folder)  )

hypotests = []

print os.path.join(folder, "results")
for root, dirs , files in os.walk(os.path.join(folder, "results")) :
	for ifile in  files :
		if "hypotest" in ifile :
			hypotests.append(os.path.join(root, ifile))

failedFitFile = open("corruptedFiles_"+grids[0]+".txt", "w")

for grid in grids:
	for region in regions:
		allhypotests = [test for test in hypotests if (region     in test
							       and grid   in test
							       and region in test)]
		safehypotests = [test for test in allhypotests if not isFileCorrupted(test)]
		corrhypotests = [test for test in allhypotests if     isFileCorrupted(test)]

		if corrhypotests :
			print "These hypotests appear to be corrupted, skipping! : "
			for test in corrhypotests :
				print test
				failedFitFile.write(test+"\n")
			print ""

		cmdHadd         = "hadd -v 0 -f {0}/combinedResults/{1}_{2}.root ".format(folder,region,grid) + " ".join(safehypotests)
		cmdCollectTests	= 'python CollectAndWriteHypoTestResults.py -F  {0}/combinedResults/{1}_{2}.root  -f "hypo_{2}_%f_%f" -c "1" -I "mgl:mlsp"'.format(folder,region,grid)
		os.system(cmdHadd)
		os.system(cmdCollectTests)
	cmdTar = "tar cvzf packedUpJSON_{0}.tgz Outputs/SR*{0}*.json ".format(grid)
	os.system(cmdTar)

failedFitFile.close()

# for fn in os.listdir(sys.argv[1]):
#      print fn
#      os.system('python CollectAndWriteHypoTestResults.py -F  %s/*hypotest*root  -f "hypo_discovery_GG_direct_%%f_%%f" -c "1" -I "mgl:mlsp"'%(sys.argv[1]+fn)  )

# for fn in os.listdir("Outputs"):
# 	print fn
# 	if "fixSigXSecNominal" in fn:
# 		os.system( "cp Outputs/%s Outputs/%s"%(fn, fn.replace("_GG_direct_Output_fixSigXSecNominal_hypotest","").replace("ZL_","")  )      )

