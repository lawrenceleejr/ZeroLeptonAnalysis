#!/usr/bin/python 


import os, sys
print sys.argv
for fn in os.listdir(sys.argv[1]):
     print fn
     os.system('python CollectAndWriteHypoTestResults.py -F  %s/*hypotest*root  -f "hypo_discovery_GG_direct_%%f_%%f" -c "1" -I "mgl:mlsp"'%(sys.argv[1]+fn)  )

for fn in os.listdir("Outputs"):
	print fn
	if "fixSigXSecNominal" in fn:
		os.system( "cp Outputs/%s Outputs/%s"%(fn, fn.replace("_GG_direct_Output_fixSigXSecNominal_hypotest","").replace("ZL_","")  )      )


os.system(" tar cvzf packedUpJSON.tgz Outputs/SR*.json " )
