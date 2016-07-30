#!/usr/bin/env python


from ROOT import *
from summary_harvest_tree_description import treedescription

import json

dummy, myvars = treedescription()
myvars = myvars.split(":")

# for xs in ["Nominal","Up","Down"]:
for xs in ["Nominal"]:


	Input =          "RJR/GG_direct_combined_fixSigXSec%s__1_harvest_list"%xs
	InjectionInput = "Refit/GG/GG_direct_SRJigsawSRG3b_fixSigXSec%s__1_harvest_list.json"%xs
	InjectionInputFID = 999

	# print myvars.index("m0/F")

	m0index = myvars.index("m0/F")
	m12index = myvars.index("m12/F")
	CLsindex = myvars.index("CLs/F")
	CLsexpindex = myvars.index("CLsexp/F")
	clsu1sindex = myvars.index("clsu1s/F")
	clsd1sindex = myvars.index("clsd1s/F")
	fIDindex = myvars.index("fID/F")

	print fIDindex

	outputfile = open(Input.split("/")[-1].replace("_combined_","_injected_"),"w")

	print InjectionInput
	with open(InjectionInput) as data_file:    
	    injectiondata = json.load(data_file)

	# print injectiondata

	for line in open(Input).readlines():

		line = line.strip()
		data = line.split()

		for injectionline in injectiondata:

			# print float(data[m0index]) , float(injectionline["m0"])
			if 	float(data[m0index]) != float(injectionline["m0"]):
				continue
			if 	float(data[m12index]) != float(injectionline["m12"]):
				continue

			print "%f %f"%(float(data[CLsexpindex]), float(injectionline["CLsexp"]))

			if float(data[CLsexpindex]) > float(injectionline["CLsexp"]):
				data[CLsexpindex] = str(injectionline["CLsexp"])
				data[CLsindex] = str(injectionline["CLs"])
				data[clsu1sindex] = str(injectionline["clsu1s"])
				data[clsd1sindex] = str(injectionline["clsd1s"])
				data[fIDindex] = str(InjectionInputFID)
				newdataline = " ".join(data)
				outputfile.write(newdataline+'\n')
				print "INJECTING %f %f"%(injectionline["m0"], injectionline["m12"]) 
			else:
				newdataline = " ".join(data)
				outputfile.write(newdataline+'\n')

		# for RJRline in open(RJRInput).readlines():

		# 	RJRline = RJRline.strip()
		# 	RJRdata = RJRline.split()

		# 	RJRdata[fIDindex] = str(int(RJRdata[fIDindex])+100)
		# 	RJRline = " ".join(RJRdata)

		# 	if MEffdata[m0index]!=RJRdata[m0index]:
		# 		continue
		# 	if MEffdata[m12index]!=RJRdata[m12index]:
		# 		continue

		# 	# print "MEff:\t%s\t%s\t%s"%(RJRdata[m0index],RJRdata[m12index],MEffdata[CLsexpindex])
		# 	# print "RJR:\t%s\t%s\t%s"%(RJRdata[m0index],RJRdata[m12index],RJRdata[CLsexpindex])

		# 	# print MEffdata[CLsexpindex] < RJRdata[CLsexpindex]

		# 	if float(MEffdata[CLsexpindex]) < float(RJRdata[CLsexpindex]):
		# 		print "MEff:\t%s\t%s\t%s"%(RJRdata[m0index],RJRdata[m12index],MEffdata[CLsexpindex])
		# 		outputfile.write(MEffline+'\n')
		# 	elif float(MEffdata[CLsexpindex]) >= float(RJRdata[CLsexpindex]):
		# 		print "RJR:\t%s\t%s\t%s"%(RJRdata[m0index],RJRdata[m12index],RJRdata[CLsexpindex])
		# 		outputfile.write(RJRline+"\n")



	outputfile.close()
