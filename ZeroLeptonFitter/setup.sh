# HistFitter tag we want to rely on (used for autofinding only)
HISTFITTER_TAG="HistFitter-00-00-50"

# setup combination package
export ZEROLEPTONFITTER=$PWD


function findHistFitter {
  dir=""
  if [[ -d "../HistFitter" ]]; then
    dir="../HistFitter"
  elif [[ -d "../${HISTFITTER_TAG}" ]]; then 
    dir="../${HISTFITTER_TAG}"
  fi

  if [[ -d $dir ]]; then
    echo "Found ${dir} - using that directory since you did not setup HistFitter first"
    if [[ `hostname -f` = b*.cern.ch ]] || [[ `hostname -f` = l*.cern.ch ]]; then
	cd ${dir}
	source "setup_afs.sh"
	cd $ZEROLEPTONFITTER 
        return
    else
	cd ${dir}
        source "setup.sh"
	cd $ZEROLEPTONFITTER
        return
    fi
  else
    echo "Warning: No valid HistFitter environment (HISTFITTER) defined. Please do so first!"
    exit
  fi
}

if [ ! $HISTFITTER ]; then
  findHistFitter
fi
  
if [ ! $HISTFITTER ]; then
  return 
fi

echo "Using HistFitter from $HISTFITTER - version $HISTFITTER_VERSION"

if [ ! $ROOTSYS ]; then
  echo "No \$ROOTSYS defined - please set up ROOT first"
  return
fi


if [ -n "${VIRTUAL_ENV+1}" ]; then
    echo "Using Python virtual environment in ${VIRTUAL_ENV}"
else    
    if [ -d "venv" ]; then
        echo "Setting up Python virtual environment from ${PWD}/venv"
        source venv/bin/activate
    fi
fi


# put root & python stuff into PATH, LD_LIBRARY_PATH
export PATH=$ZEROLEPTONFITTER/scripts:${PATH}

export LD_LIBRARY_PATH=$ZEROLEPTONFITTER/lib:${LD_LIBRARY_PATH}

# PYTHONPATH contains all directories that are used for 'import bla' commands
export PYTHONPATH=$ZEROLEPTONFITTER/python:$ZEROLEPTONFITTER/scripts:$ZEROLEPTONFITTER/macros:$ZEROLEPTONFITTER/lib:$PYTHONPATH

# Hack for mac over ssh
export LC_ALL=C

alias go=$PWD
