#!/usr/bin/python 


import os, sys
import glob

print sys.argv

folder = sys.argv[1]

regions = [

"SRJigsawSR1A",
"SRJigsawSR1B",
"SRJigsawSR1C",
"SRJigsawSR2A",
"SRJigsawSR2B",
"SRJigsawSR2C",
"SRJigsawSR3A",
"SRJigsawSR3B",
"SRJigsawSR3C",

"SRJigsawSR1ASq",
"SRJigsawSR1BSq",
"SRJigsawSR2ASq",
"SRJigsawSR2BSq",
"SRJigsawSR3ASq",
"SRJigsawSR3BSq",

"SRJigsawSR1ACo",
"SRJigsawSR1BCo",
"SRJigsawSR2ACo",
"SRJigsawSR2BCo",
"SRJigsawSR3ACo",
"SRJigsawSR3BCo",
"SRJigsawSR4ACo",
"SRJigsawSR4BCo",

]

grids = ["GG_direct","SS_direct"]

grids = [folder.split("-")[1] ]

os.system("mkdir {0}/combinedResults".format(folder)  )

for grid in grids:
	for region in regions:
		if glob.glob('{0}/results/ZL_{1}_{2}_*'.format(folder,region,grid) ):
			os.system(" hadd -f {0}/combinedResults/{1}_{2}.root {0}/results/ZL_{1}_{2}_*/*hypotest*root ".format(folder,region,grid)     )
			os.system('python CollectAndWriteHypoTestResults.py -F  {0}/combinedResults/{1}_{2}.root  -f "hypo_{2}_%f_%f" -c "1" -I "mgl:mlsp"'.format(folder,region,grid)  )



# for fn in os.listdir(sys.argv[1]):
#      print fn
#      os.system('python CollectAndWriteHypoTestResults.py -F  %s/*hypotest*root  -f "hypo_discovery_GG_direct_%%f_%%f" -c "1" -I "mgl:mlsp"'%(sys.argv[1]+fn)  )

# for fn in os.listdir("Outputs"):
# 	print fn
# 	if "fixSigXSecNominal" in fn:
# 		os.system( "cp Outputs/%s Outputs/%s"%(fn, fn.replace("_GG_direct_Output_fixSigXSecNominal_hypotest","").replace("ZL_","")  )      )


	os.system(" tar cvzf packedUpJSON_{0}.tgz Outputs/SR*{0}*.json ".format(grid)    )
