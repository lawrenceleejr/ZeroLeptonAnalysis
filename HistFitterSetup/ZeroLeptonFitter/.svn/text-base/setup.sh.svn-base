# check Root environment setup again
if [ ! $HISTFITTER ]; then
  echo "Warning: No valid HistFitter environment (HISTFITTER) defined. Please do so first!"
  return
fi

echo "Using HistFitter from $HISTFITTER"

# setup combination package
export ZEROLEPTONFITTER=$PWD

# put root & python stuff into PATH, LD_LIBRARY_PATH
export PATH=$ZEROLEPTONFITTER/scripts:${PATH}

export LD_LIBRARY_PATH=$ZEROLEPTONFITTER/lib:${LD_LIBRARY_PATH}

# PYTHONPATH contains all directories that are used for 'import bla' commands
export PYTHONPATH=$ZEROLEPTONFITTER/python:$ZEROLEPTONFITTER/scripts:$ZEROLEPTONFITTER/macros:$ZEROLEPTONFITTER/lib:$PYTHONPATH

# Hack for mac over ssh
export LC_ALL=C

alias go=$PWD
