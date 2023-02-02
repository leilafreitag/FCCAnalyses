#!/bin/bash

sample_folder="~/basic_stage/simulation_files"
#sample_folder="/eos/user/a/afehr/simulation_files_latest2"

files=(
#       	"Zmumu_ecm91_standard.root"
#        "Zmumu_ecm91_R1.3.root"
#        "Zmumu_ecm91_R1.3_w30.root"
#        "Zmumu_ecm91_R1.3_w50.root"
#        "Zmumu_ecm91_R1.3_w100.root"
        "Zmumu_ecm91_R1.3_w30_DSK.root"
        "Zmumu_ecm91_R1.3_w50_DSK.root"
        "Zmumu_ecm91_R1.3_w100_DSK.root"
        "Zmumu_ecm91_R1.3_L1_w30.root"
)


#files=("Zmumu_ecm91_R1.3_L1_w30.root")
#files=("Zmumu_ecm91_R1.3_w30.root")


#files=("ParticleGun_Mu_standard_1GeV_10degrees.root")


#FOR ZMUMU ----------------

#for file in "${files[@]}"; do
#        echo $file
	# nohup python ~/FCCeePhysicsPerformance/case-studies/flavour/VertexExamples/analysis_Bs2DsK.py ${sample_folder}/${file} > /dev/null 2>&1
	# nohup python ~/FCCeePhysicsPerformance/case-studies/flavour/VertexExamples/analysis_Bs2JPsiPhi.py ${sample_folder}/${file}  > ${file}.log & #/dev/null 2>&1
#    nohup fccanalysis run  ~/FCCAnalyses/examples/FCCee/vertex/validation_tkParam_adj.py --files-list ${sample_folder}/${file} --output $file  > ${file}.log &
#done


#FOR PARTICLE GUN ----------------
for filepath in ~/basic_stage/simulation_files/ParticleGun_Mu_standard_1GeV*.root; do
        echo $filepath
        name=(`echo $filepath | cut -d '/' -f 9`) #get only the file name from the path
        nohup fccanalysis run ~/FCCAnalyses/examples/FCCee/vertex/validation_tkParam_adj.py --files-list $filepath --output $name  > ${name}.log &
        echo $name
done

