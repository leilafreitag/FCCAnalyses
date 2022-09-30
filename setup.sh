path=$PWD     # Default one
#path=/cvmfs/sw.hsf.org/spackages/linux-centos7-x86_64/gcc-8.3.0/fccanalyses-0.3.0-av3c7xyuiyuxighdswldo6ut7wspgnmr  # Remote
echo $path

#!/bin/bash
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
#source ~/Key4hep_nightly.sh

export PYTHONPATH=$path:$PYTHONPATH
export LD_LIBRARY_PATH=$path/install/lib:$LD_LIBRARY_PATH
export ROOT_INCLUDE_PATH=$path/install/include/FCCAnalyses:$ROOT_INCLUDE_PATH
export LD_LIBRARY_PATH=`python -m awkward.config --libdir`:$LD_LIBRARY_PATH

# Source the needed flavour packages that have been installed in FCCeePhysicsPerformance/case-studies/flavour/dataframe with FCCeePhysicsPerformance/setup.sh
cd /afs/cern.ch/user/a/afehr/FCCeePhysicsPerformance/case-studies/flavour/dataframe
source ./localSetup.sh
cd /afs/cern.ch/user/a/afehr/FCCAnalyses
