#!/bin/bash

sample_folder="~/simulation_files"
#sample_folder="/eos/user/a/afehr/simulation_files_latest2"

files=(
#		"Zmumu_ecm91_FullSilicon_R1.0_simple_130mrad.root"
#		"Zmumu_ecm91_FullSilicon_R1.0_simple_120mrad.root"
#		"Zmumu_ecm91_FullSilicon_R1.0_simple_110mrad.root"
#        "Zmumu_ecm91_FullSilicon_R1.0_130mrad_shorteningWholeBarrel_compactEndcap.root"
#        "Zmumu_ecm91_FullSilicon_R1.0_120mrad_shorteningWholeBarrel_compactEndcap.root"
#        "Zmumu_ecm91_FullSilicon_R1.0_110mrad_shorteningWholeBarrel_compactEndcap.root"
#        "Zmumu_ecm91_FullSilicon_R1.0_130mrad_shorteningWholeBarrel.root"
#        "Zmumu_ecm91_FullSilicon_R1.0_120mrad_shorteningWholeBarrel.root"
#        "Zmumu_ecm91_FullSilicon_R1.0_110mrad_shorteningWholeBarrel.root"
        "Zmumu_ecm91_FullSilicon.root"
        "Zmumu_ecm91_FullSilicon_R1.0_simple.root"
#		"Zmumu_ecm91_FullSilicon_noFirstLayer.root"
#		"Zmumu_ecm91_FullSilicon_beamPipe125.root"
#		"Zmumu_ecm91_FullSilicon_R1.0_shorteningWholeBarrel_compactEndcap.root"
#		"Zmumu_ecm91_FullSilicon_R1.0_shorteningWholeBarrel.root"
#        "Zmumu_ecm91_standard.root"
#	"evtGen_ecm91_Bs2DsK.root"
#	"evtGen_ecm91_Bs2DsK_FullSilicon.root"
#	"evtGen_ecm91_Bs2DsK_FullSilicon_R1.0_110mrad_shorteningWholeBarrel.root"
#	"evtGen_ecm91_Bs2DsK_FullSilicon_R1.0_110mrad_shorteningWholeBarrel_compactEndcap.root"
#	"evtGen_ecm91_Bs2DsK_FullSilicon_R1.0_120mrad_shorteningWholeBarrel.root"
#	"evtGen_ecm91_Bs2DsK_FullSilicon_R1.0_120mrad_shorteningWholeBarrel_compactEndcap.root"
#	"evtGen_ecm91_Bs2DsK_FullSilicon_R1.0_130mrad_shorteningWholeBarrel.root"
#	"evtGen_ecm91_Bs2DsK_FullSilicon_R1.0_130mrad_shorteningWholeBarrel_compactEndcap.root"
#	"evtGen_ecm91_Bs2DsK_FullSilicon_R1.0_shorteningWholeBarrel.root"
#	"evtGen_ecm91_Bs2DsK_FullSilicon_R1.0_shorteningWholeBarrel_compactEndcap.root"
#	"evtGen_ecm91_Bs2DsK_FullSilicon_R1.0_simple.root"
#	"evtGen_ecm91_Bs2DsK_FullSilicon_R1.0_simple_110mrad.root"
#	"evtGen_ecm91_Bs2DsK_FullSilicon_R1.0_simple_120mrad.root"
#	"evtGen_ecm91_Bs2DsK_FullSilicon_R1.0_simple_130mrad.root"
#	"evtGen_ecm91_Bs2DsK_FullSilicon_beamPipe125.root"
#	"evtGen_ecm91_Bs2DsK_FullSilicon_noFirstLayer.root"
#    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon.root"
#    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_R1.0_110mrad_shorteningWholeBarrel.root"
#    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_R1.0_110mrad_shorteningWholeBarrel_compactEndcap.root"
#    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_R1.0_120mrad_shorteningWholeBarrel.root"
#    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_R1.0_120mrad_shorteningWholeBarrel_compactEndcap.root"
#    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_R1.0_130mrad_shorteningWholeBarrel.root"
#    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_R1.0_130mrad_shorteningWholeBarrel_compactEndcap.root"
#    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_R1.0_shorteningWholeBarrel.root"
#    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_R1.0_shorteningWholeBarrel_compactEndcap.root"
#    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_R1.0_simple.root"
#    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_R1.0_simple_110mrad.root"
#    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_R1.0_simple_120mrad.root"
#    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_R1.0_simple_130mrad.root"
#    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_beamPipe125.root"
#    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_noFirstLayer.root"
#	"evtGen_ecm91_Bs2JpsiPhi_standard.root"
)

#files=(
#    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon.root"
##    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_R1.0_110mrad_shorteningWholeBarrel.root"
##    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_R1.0_110mrad_shorteningWholeBarrel_compactEndcap.root"
##    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_R1.0_120mrad_shorteningWholeBarrel.root"
##    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_R1.0_120mrad_shorteningWholeBarrel_compactEndcap.root"
##    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_R1.0_130mrad_shorteningWholeBarrel.root"
##    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_R1.0_130mrad_shorteningWholeBarrel_compactEndcap.root"
#    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_R1.0_shorteningWholeBarrel.root"
#    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_R1.0_shorteningWholeBarrel_compactEndcap.root"
#    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_R1.0_simple.root"
#    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_R1.0_simple_110mrad.root"
#    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_R1.0_simple_120mrad.root"
#    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_R1.0_simple_130mrad.root"
##    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_beamPipe125.root"
##    "evtGen_ecm91_Bs2JpsiPhi_FullSilicon_noFirstLayer.root"
#    "evtGen_ecm91_Bs2JpsiPhi_standard.root"
#)

# Forward
#files=(
# "evtGen_ecm91_Bs2JpsiPhi_forward_FullSilicon_R1.0_simple_110mrad.root"
# "evtGen_ecm91_Bs2JpsiPhi_forward_FullSilicon_R1.0_simple.root"
# "evtGen_ecm91_Bs2JpsiPhi_forward_FullSilicon.root"
# "evtGen_ecm91_Bs2JpsiPhi_forward_FullSilicon_R1.0_simple_130mrad.root"
# "evtGen_ecm91_Bs2JpsiPhi_forward_FullSilicon_R1.0_simple_120mrad.root"
#"evtGen_ecm91_Bs2JpsiPhi_forward_FullSilicon_R1.0_shorteningWholeBarrel_compactEndcap.root"
#"evtGen_ecm91_Bs2JpsiPhi_forward_FullSilicon_R1.0_shorteningWholeBarrel.root"
#)




for file in "${files[@]}"; do
	echo $file
	#python FCCee/vertex/validation_tkParam_adj.py ~/simulation_files_latest/${file}
#	nohup python ~/FCCeePhysicsPerformance/case-studies/flavour/VertexExamples/analysis_Bs2DsK.py ${sample_folder}/${file} > /dev/null 2>&1 
#    nohup python ~/FCCeePhysicsPerformance/case-studies/flavour/VertexExamples/analysis_Bs2JPsiPhi.py ${sample_folder}/${file}  > ${file}.log & #/dev/null 2>&1
    nohup fccanalysis run  ~/FCCAnalyses/examples/FCCee/vertex/validation_tkParam_adj.py --files-list ${sample_folder}/${file} --output $file  > ${file}.log & 
done

#python FCCee/vertex/plotting_armin.py -i FCCee/vertex/*.root
