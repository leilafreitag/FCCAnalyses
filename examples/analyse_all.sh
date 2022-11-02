#!/bin/bash

sample_folder="~/basic_stage/simulation_files"
#sample_folder="/eos/user/a/afehr/simulation_files_latest2"

files=(
       	"Zmumu_ecm91_standard.root"
        "Zmumu_ecm91_R1.3.root"
        "Zmumu_ecm91_R1.3_w30.root"
        "Zmumu_ecm91_R1.3_w50.root"
        "Zmumu_ecm91_R1.3_w100.root"
        "Zmumu_ecm91_R1.3_w30_DSK.root"
        "Zmumu_ecm91_R1.3_w50_DSK.root"
        "Zmumu_ecm91_R1.3_w100_DSK.root"
)


for file in "${files[@]}"; do
        echo $file
        #python FCCee/vertex/validation_tkParam_adj.py ~/simulation_files_latest/${file}
#	nohup python ~/FCCeePhysicsPerformance/case-studies/flavour/VertexExamples/analysis_Bs2DsK.py ${sample_folder}/${file} > /dev/null 2>&1
#    nohup python ~/FCCeePhysicsPerformance/case-studies/flavour/VertexExamples/analysis_Bs2JPsiPhi.py ${sample_folder}/${file}  > ${file}.log & #/dev/null 2>&1
    nohup fccanalysis run  ~/FCCAnalyses/examples/FCCee/vertex/validation_tkParam_adj.py --files-list ${sample_folder}/${file} --output $file  > ${file}.log &
done

#python FCCee/vertex/plotting_armin.py -i FCCee/vertex/*.root
