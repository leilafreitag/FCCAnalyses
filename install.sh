rm -rf build install
mkdir build install
cd build/
cmake .. -DCMAKE_INSTALL_PREFIX=../install -DFCCANALYSES_INCLUDE_PATH=../install/include/FCCAnalyses
make install
cd ..
