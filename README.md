These scripts are for doing studies on the ntuples made by the ZeroLeptonRun2 factory. I think you'll find some of these to be very simple to use and dive into, so feel free to use/contribute if you find it useful for your own studies.

Many of these require SampleHandler and an ASG setup

	source setup.sh
	rc find_packages
	rc compile

run.py reads in an example region defined by a bunch of cuts and uses MultiDraw to produce plots in that region for whatever variables you want, N-1 plots, and a cutflow plot. This also crudely scales and hadds everything together so that you can just plot the final histograms in the output root files. 

The scripts in the optimization folder also use SH to easily create trees to hand to TMVA and is set to run a cut optimization currently.

There is additionally a plottingScripts folder which has my plotting scripts used on the output files from run.py. This uses rootpy and matplotlib so those are dependencies for these scripts. I know there is a localSetupROOT option that allows for a fully working rootpy+matplotlib installation, but I don't know what that is (if anyone knows please let me know!). I'm only using these scripts on my local machine. 


