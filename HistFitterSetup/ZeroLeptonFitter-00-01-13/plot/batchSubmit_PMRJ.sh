for i in SR CRY CRWT CRQ VRZ VRZc VRY VRWT; do
    for j in SRG SRS; do
	for k in 1a 1b 2a 2b 3a 3b; do
	    python plot/PlotMakerRJ.py --inputSampleDir samples/ --lumi 11.78 --region $i --regionsToRun "SR${j}${k}" --inputDataFile="samples/DataMain_303304.root";
	done;
    done;
    for j in SRC1 SRC2 SRC3 SRC4 SRC5; do
	python plot/PlotMakerRJ.py --inputSampleDir samples/ --lumi 11.78 --region $i --regionsToRun "SR${j}" --inputDataFile="samples/DataMain_303304.root" --doCompressed;
	done;
    done;
done