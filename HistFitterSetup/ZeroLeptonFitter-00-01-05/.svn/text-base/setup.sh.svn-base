# HistFitter tag we want to rely on (used for autofinding only)
HISTFITTER_TAG="HistFitter-00-00-51"

function setZeroLeptonFitter {
    if [ -z ${ZSH_NAME} ] && [ "$(dirname ${BASH_ARGV[0]})" == "." ]; then
      if [ ! -f setup.sh ]; then
        echo ERROR: must "cd where/ZeroLeptonFitter/is" before calling "source setup.sh" for this version of bash!
        export ZEROLEPTONFITTER=;
        return
      fi
      export ZEROLEPTONFITTER=$(pwd);
    else
      # get param to "."
      scriptname=${BASH_SOURCE:-$0}
      DIR=$( cd "$( dirname "${scriptname}" )" && pwd )
      #thishistfitter=$(dirname ${BASH_ARGV[0]})
      export ZEROLEPTONFITTER=${DIR};
    fi
}

function findHistFitter {
  dir=""
  if [[ -d "${ZEROLEPTONFITTER}/../HistFitter" ]]; then
    dir="${ZEROLEPTONFITTER}/../HistFitter"
  elif [[ -d "${ZEROLEPTONFITTER}/../${HISTFITTER_TAG}" ]]; then 
    dir="${ZEROLEPTONFITTER}/../${HISTFITTER_TAG}"
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
    unset ZEROLEPTONFITTER
    return
  fi
}

IWASHERE=$PWD
IWASHEREBEFORE=$OLDPWD

setZeroLeptonFitter

if [ ! $HISTFITTER ]; then
  findHistFitter
fi
  
if [ ! $HISTFITTER ]; then
  unset ZEROLEPTONFITTER
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

export TEXINPUTS=$ZEROLEPTONFITTER/ToolKit/Tex:$TEXINPUTS

# PYTHONPATH contains all directories that are used for 'import bla' commands
export PYTHONPATH=$ZEROLEPTONFITTER/python:$ZEROLEPTONFITTER/scripts:$ZEROLEPTONFITTER/macros:$ZEROLEPTONFITTER/lib:$PYTHONPATH

# Hack for mac over ssh
export LC_ALL=C

cd $IWASHERE
export OLDPWD=$IWASHEREBEFORE
