#!/usr/bin/env python


from ROOT import *
from summary_harvest_tree_description import treedescription

dummy, myvars = treedescription()
myvars = myvars.split(":")

MEffInput = "MEff/GG_direct/GG_direct_combined_fixSigXSecNominal__1_harvest_list"
RJRInput = "RJR/GG/GG_direct_combined_fixSigXSecNominal__1_harvest_list"

# MEffInput = "MEff/SS_direct/SS_direct_combined_fixSigXSecNominal__1_harvest_list"
# RJRInput = "RJR/SS/SS_direct_combined_fixSigXSecNominal__1_harvest_list"

print myvars.index("m0/F")

m0index = myvars.index("m0/F")
m12index = myvars.index("m12/F")
CLsexpindex = myvars.index("CLsexp/F")
fIDindex = myvars.index("fID/F")

print fIDindex

outputfile = open(MEffInput.split("/")[-1].replace("_combined_","_MEffRJRCombined_"),"w")

for MEffline in open(MEffInput).readlines():

	MEffline = MEffline.strip()
	MEffdata = MEffline.split()

	for RJRline in open(RJRInput).readlines():

		RJRline = RJRline.strip()
		RJRdata = RJRline.split()

		RJRdata[fIDindex] = str(int(RJRdata[fIDindex])+100)
		RJRline = " ".join(RJRdata)

		if MEffdata[m0index]!=RJRdata[m0index]:
			continue
		if MEffdata[m12index]!=RJRdata[m12index]:
			continue

		# print "MEff:\t%s\t%s\t%s"%(RJRdata[m0index],RJRdata[m12index],MEffdata[CLsexpindex])
		# print "RJR:\t%s\t%s\t%s"%(RJRdata[m0index],RJRdata[m12index],RJRdata[CLsexpindex])

		# print MEffdata[CLsexpindex] < RJRdata[CLsexpindex]

		if float(MEffdata[CLsexpindex]) < float(RJRdata[CLsexpindex]):
			print "MEff:\t%s\t%s\t%s"%(RJRdata[m0index],RJRdata[m12index],MEffdata[CLsexpindex])
			outputfile.write(MEffline+'\n')
		elif float(MEffdata[CLsexpindex]) >= float(RJRdata[CLsexpindex]):
			print "RJR:\t%s\t%s\t%s"%(RJRdata[m0index],RJRdata[m12index],RJRdata[CLsexpindex])
			outputfile.write(RJRline+"\n")



outputfile.close()
