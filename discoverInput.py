import ROOT
import logging
import shutil
import os


def discover(sh, search_directories):

	print "searching directories : "
	print search_directories
	# scan for datasets in the given directories
	for directory in search_directories:
		print directory
		ROOT.SH.scanDir(sh, directory)


	logging.info("%d different datasets found scanning all directories", len(sh))
	sh.printContent()

	return sh



def addTags(sh_all):
	for sample in sh_all:
		name = sample.getMetaString("sample_name")
		print "NAME: ", name
#		short_name = sample.getMetaString("sample_name").split(".")[4]
#		sample.setMetaString( "short_name" , short_name )
#		print short_name

		if "physics_" in name:
			sample.addTag("data")

		if "GG_direct" in name:
			sample.addTag("signal")
			sample.addTag("gg_direct")
		if "SS_direct" in name:
			sample.addTag("signal")
			sample.addTag("ss_direct")

		if "ttbar" in name:
			sample.addTag("top")
			sample.addTag("ttbar")
		if "Wt_inclusive" in name:
			sample.addTag("top")
			sample.addTag("singletop")
		if "PowHPEvG_singletop" in name:
			sample.addTag("top")
			sample.addTag("singletop")

		if "jetjet" in name:
			sample.addTag("qcd")

		if "1Gam" in name:
			sample.addTag("gamma")

		if "Znunu_Pt" in name:
			sample.addTag("znunu_nlo")

		if "Znunu_LO" in name:
			sample.addTag("znunu_lo")

		if "PowHP8EvG_W" in name:
			sample.addTag("wjets")
		if "Sherpa_Znunu" in name :
			if "SUSY1" in name :
				sample.addTag("zjets_reco")
			if "TRUTH1" in name :
				sample.addTag("zjets_truth")

		if "Sherpa_1Gam" in name :
			if "SUSY1" in name :
				sample.addTag("gamma_reco")
			if "TRUTH1" in name :
				sample.addTag("gamma_truth")

#		if "Znunu" in name:
#			sample.addTag("zjets")
		if "Sherpa_Wqq" in name:
			sample.addTag("zjets")

# For merged files
		# if "Zjets" in name:
		# 	print name, ">>", "zjets"
		# 	sample.addTag("zjets")
		# if "GammaJet" in name:
		# 	print name, ">>", "gamma"
		# 	sample.addTag("gamma")
