if [ "${0}" != "${BASH_SOURCE}" ]; then
  if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
  else
    echo "INFO: Key4hep stack already set up."
  fi
  export PYTHONPATH=$PWD:$PYTHONPATH
  export PYTHONPATH=$PWD/python:$PYTHONPATH
  export PATH=$PWD/bin:$PATH
  export LD_LIBRARY_PATH=$PWD/install/lib:$LD_LIBRARY_PATH
  export CMAKE_PREFIX_PATH=$PWD/install:$CMAKE_PREFIX_PATH
  export ROOT_INCLUDE_PATH=$PWD/install/include:$ROOT_INCLUDE_PATH
  export LOCAL_DIR=$PWD
  export LD_LIBRARY_PATH=`python -m awkward.config --libdir`:$LD_LIBRARY_PATH
  export ONNXRUNTIME_ROOT_DIR=`python -c "import onnxruntime; print(onnxruntime.__path__[0]+'/../../../..')"`
  export LD_LIBRARY_PATH=$ONNXRUNTIME_ROOT_DIR/lib:$LD_LIBRARY_PATH
else
  echo "ERROR: This script is meant to be sourced!"
fi

# Source the needed flavour packages that have been installed in FCCeePhysicsPerformance/case-studies/flavour/dataframe with FCCeePhysicsPerformance/setup.sh
cd /afs/cern.ch/user/l/lfreitag/FCCeePhysicsPerformance/case-studies/flavour/dataframe
source ./localSetup.sh
cd /afs/cern.ch/user/l/lfreitag/FCCAnalyses
