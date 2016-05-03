#!/bin/bash

#sleep 20000

export nb=${#}

if [ $nb == 1 ]
then
export GRID=$1
else
export GRID=SS_direct
fi

export DIR=../../results/

python getJSONFiles.py -i $DIR --gridName $GRID -d
python makeContour.py  -o --gridName $GRID  -r -d





