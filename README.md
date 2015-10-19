These scripts are for doing studies on the ntuples made by the ZeroLeptonRun2 factory. I think you'll find some of these to be very simple to use and dive into, so feel free to use/contribute if you find it useful for your own studies.

Many of these require SampleHandler and an ASG setup

	source setup.sh
	rc find_packages
	rc compile

run.py reads in an example region defined by a bunch of cuts and uses MultiDraw to produce plots in that region for whatever variables you want, N-1 plots, and a cutflow plot. This also crudely scales and hadds everything together so that you can just plot the final histograms in the output root files. 

The scripts in the optimization folder also use SH to easily create trees to hand to TMVA and is set to run a cut optimization currently.

There is additionally a plottingScripts folder which has my plotting scripts used on the output files from run.py. This uses rootpy and matplotlib so those are dependencies for these scripts. 

If you're in an ATLAS environment, you can do 

	localSetupSFT --cmtConfig=x86_64-slc6-gcc47-opt pytools/1.8_python2.7,pyanalysis/1.3_python2.7,lapack/3.4.0,blas/20110419

which setups up matplotlib/numpy/etc. On lxplus, you can follow the instructions here: 

http://www.rootpy.org/start.html#try-rootpy-on-cern-s-lxplus

Or if you want to install rootpy on your own computer, it can be a pain to make sure that python versions are carried through correctly, so these instructions are a bit handy:

https://fieldsofdata.wordpress.com/2014/10/15/data-analysis-packages-on-mac-os-x-10-8/

