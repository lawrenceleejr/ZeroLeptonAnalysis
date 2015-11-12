#!/usr/bin/python 


import os, sys
print sys.argv
for fn in os.listdir(sys.argv[1]):
     print fn
     if "GG_direct" in fn:
          os.system('python CollectAndWriteHypoTestResults.py -F  %s  -f "hypo_GG_direct_%%f_%%f" -c "1" -I "mgl:mlsp"'%(sys.argv[1]+fn)  )
