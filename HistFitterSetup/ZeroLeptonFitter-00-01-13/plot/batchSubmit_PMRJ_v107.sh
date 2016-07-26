for i in SR CRY CRWT CRQ VRZ VRZc VRY VRWT; do
    for j in SRG SRS; do
	for k in 1a 1b 2a 2b 3a 3b; do
	    BATCHSCRIPT="batchscripts/batchtest_${i}_${j}${k}.sh";
	    echo '#!/bin/bash' > $BATCHSCRIPT;
	    echo '# Inherit current user environment' >> $BATCHSCRIPT;
	    echo '#PBS -V' >> $BATCHSCRIPT;
#	    echo '#PBS -q adl_short' >> $BATCHSCRIPT;
#	    echo '#PBS -l nodes=1:SA' >> $BATCHSCRIPT;
	    echo 'echo $PBS_O_WORKDIR' >> $BATCHSCRIPT;
	    echo 'cd $PBS_O_WORKDIR' >> $BATCHSCRIPT;
	    echo "python plot/PlotMakerRJ.py --inputSampleDir samples_v107/ --lumi 11.3 --region $i --regionsToRun \"${j}${k}\" --baseDir=$PWD --version 107 --doSyst" >> $BATCHSCRIPT;
	    echo "exit 0" >> $BATCHSCRIPT;
	    chmod +x $BATCHSCRIPT;
	    qsub $BATCHSCRIPT;
	done;
    done;
    for j in SRC1 SRC2 SRC3 SRC4 SRC5; do
	BATCHSCRIPT="batchscripts/batchtest_${i}_${j}.sh";
	echo '#!/bin/bash' > $BATCHSCRIPT;
	echo '# Inherit current user environment' >> $BATCHSCRIPT;
	echo '#PBS -V' >> $BATCHSCRIPT;
#	echo '#PBS -q adl_short' >> $BATCHSCRIPT;
#	echo '#PBS -l nodes=1:SA' >> $BATCHSCRIPT;
	echo 'echo $PBS_O_WORKDIR' >> $BATCHSCRIPT;
	echo 'cd $PBS_O_WORKDIR' >> $BATCHSCRIPT;
	echo "python plot/PlotMakerRJ.py --inputSampleDir samples_v107/ --lumi 11.3 --region $i --regionsToRun \"${j}\" --doCompressed --baseDir=$PWD --version 107 --doSyst" >> $BATCHSCRIPT;
	echo "exit 0" >> $BATCHSCRIPT;
	chmod +x $BATCHSCRIPT;
	qsub $BATCHSCRIPT;
    done;
done