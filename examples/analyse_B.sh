#!/bin/bash

sample_folder="~/basic_stage/simulation_files"


for filepath in ~/basic_stage/simulation_files/evtGen_ecm91_Bs2JpsiPhi*L1_w30.root; do
        echo $filepath
        name=(`echo $filepath | cut -d '/' -f 9`) #get only the file name from the path
        echo $name

        #nohup fccanalysis run ~/FCCAnalyses/examples/FCCee/vertex/validation_tkParam_adj.py --files-list $filepath --output $name  > ${name}.log &
        nohup fccanalysis run ~/FCCeePhysicsPerformance/case-studies/flavour/VertexExamples/analysis_Bs2JPsiPhi.py --files-list $filepath --output $name > ${name}.log &

done

