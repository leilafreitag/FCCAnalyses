#!/bin/bash

# Manually listing the input files for the comparison plotting in summary_plots_leila.py so that order of legend is the way I want.
input_files=("FCCee/vertex/Zmumu_ecm91_standard_plots/plots.root
              FCCee/vertex/Zmumu_ecm91_R1.3_plots/plots.root
              FCCee/vertex/Zmumu_ecm91_R1.3_w100_plots/plots.root
              FCCee/vertex/Zmumu_ecm91_R1.3_w100_DSK_plots/plots.root
       	      FCCee/vertex/Zmumu_ecm91_R1.3_w50_plots/plots.root
              FCCee/vertex/Zmumu_ecm91_R1.3_w50_DSK_plots/plots.root
              FCCee/vertex/Zmumu_ecm91_R1.3_w30_plots/plots.root
              FCCee/vertex/Zmumu_ecm91_R1.3_w30_DSK_plots/plots.root
             ")

#echo $input_files


#python FCCee/vertex/plotting_armin.py -i Zmumu_ecm91*.root
#python FCCee/vertex/summary_plots.py --analysis impact_parameter -i FCCee/vertex/Zmumu_ecm91*/plots.root 

#python FCCee/vertex/plotting_leila.py -i Zmumu_ecm91*.root
python FCCee/vertex/plotting_leila.py -i Zmumu_ecm91_standard.root
#python FCCee/vertex/summary_plots_leila.py --analysis impact_parameter -i $input_files

