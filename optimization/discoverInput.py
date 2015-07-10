import ROOT
import logging
import shutil
import os


def discover(sh, search_directories):

	# scan for datasets in the given directories
	for directory in search_directories:
	    ROOT.SH.scanDir(sh, directory)


	logging.info("%d different datasets found scanning all directories", len(sh))

	return sh



def addTags(sh_all):
	for sample in sh_all:

		short_name = sample.getMetaString("sample_name").split(".")[4]
		sample.setMetaString( "short_name" , short_name )

		if "physics_" in short_name:
			sample.addTag("data")

		if "GG_direct" in short_name:
			sample.addTag("signal")
			sample.addTag("gg_direct")
		if "SS_direct" in short_name:
			sample.addTag("signal")
			sample.addTag("ss_direct")

		if "ttbar" in short_name:
			sample.addTag("top")
			sample.addTag("ttbar")
		if "Wt_inclusive" in short_name:
			sample.addTag("top")
			sample.addTag("singletop")
		if "PowHPEvG_singletop" in short_name:
			sample.addTag("top")
			sample.addTag("singletop")

		if "jetjet" in short_name:
			sample.addTag("qcd")

		if "1Gam" in short_name:
			sample.addTag("gamma")

		# if "Wmunu" in short_name:
		# 	sample.addTag("wjets")
		# 	sample.addTag("wmunu")
		# if "Wenu" in short_name:
		# 	sample.addTag("wjets")
		# 	sample.addTag("wenu")
		# if "Wtaunu" in short_name:
		# 	sample.addTag("wjets")
		# 	sample.addTag("wtaunu")

		# if "Zmumu" in short_name:
		# 	sample.addTag("zjets")
		# 	sample.addTag("zmumu")
		# if "Zee" in short_name:
		# 	sample.addTag("zjets")
		# 	sample.addTag("zee")
		# if "Ztautau" in short_name:
		# 	sample.addTag("zjets")
		# 	sample.addTag("ztautau")
		# if "Znunu" in short_name:
		# 	sample.addTag("zjets")
		# 	sample.addTag("znunu")

		if "PowHP8EvG_W" in short_name:
			sample.addTag("wjets")
		if "PowHP8EvG_Z" in short_name:
			sample.addTag("zjets")
		if "Znunu" in short_name:
			sample.addTag("zjets")
		if "Sherpa_Wqq" in short_name:
			sample.addTag("zjets")

