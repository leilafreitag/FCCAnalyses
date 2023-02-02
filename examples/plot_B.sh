#!/bin/bash

# Manually listing the input files for the comparison plotting in summary_plots_leila.py so that order of legend is the way I want.
input_files=("FCCee/vertex/evtGen_ecm91_Bs2JpsiPhi_standard_plots/plots.root
              FCCee/vertex/evtGen_ecm91_Bs2JpsiPhi_R1.3_plots/plots.root
              FCCee/vertex/evtGen_ecm91_Bs2JpsiPhi_R1.3_w100_plots/plots.root
              FCCee/vertex/evtGen_ecm91_Bs2JpsiPhi_R1.3_w100_DSK_plots/plots.root
       	      FCCee/vertex/evtGen_ecm91_Bs2JpsiPhi_R1.3_w50_plots/plots.root
              FCCee/vertex/evtGen_ecm91_Bs2JpsiPhi_R1.3_w50_DSK_plots/plots.root
              FCCee/vertex/evtGen_ecm91_Bs2JpsiPhi_R1.3_w30_plots/plots.root
              FCCee/vertex/evtGen_ecm91_Bs2JpsiPhi_R1.3_w30_DSK_plots/plots.root
             ")
input_files=("FCCee/vertex/evtGen_ecm91_Bs2JpsiPhi_standard_plots/plots.root
              FCCee/vertex/evtGen_ecm91_Bs2JpsiPhi_R1.3_plots/plots.root
              FCCee/vertex/evtGen_ecm91_Bs2JpsiPhi_R1.3_L1_w30_plots/plots.root
              FCCee/vertex/evtGen_ecm91_Bs2JpsiPhi_R1.3_w100_plots/plots.root
              FCCee/vertex/evtGen_ecm91_Bs2JpsiPhi_R1.3_w50_plots/plots.root
              FCCee/vertex/evtGen_ecm91_Bs2JpsiPhi_R1.3_w30_plots/plots.root
              FCCee/vertex/evtGen_ecm91_Bs2JpsiPhi_R1.3_w30_DSK_plots/plots.root
              FCCee/vertex/evtGen_ecm91_Bs2JpsiPhi_FullSilicon_plots/plots.root
             ")

#echo $input_files

#input_files=("FCCee/vertex/evtGen_ecm91_Bs2JpsiPhi_standard_plots/plots.root")


#HERE WE ARE:
#python FCCee/vertex/plotting_leila_B.py -i evtGen_ecm91_Bs2JpsiPhi*.root
#python FCCee/vertex/plotting_leila_B.py -i evtGen_ecm91_Bs2JpsiPhi_standard.root
python FCCee/vertex/summary_plots_B.py --analysis stuff -i $input_files

