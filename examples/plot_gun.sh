
#!/bin/bash

# Manually listing the input files for the comparison plotting in summary_plots_leila.py so that order of legend is the way I want.
#input_files=("FCCee/vertex/Zmumu_ecm91_standard_plots/plots.root
#              FCCee/vertex/Zmumu_ecm91_R1.3_plots/plots.root
#             ")

#echo $input_files


#python FCCee/vertex/plotting_armin.py -i Zmumu_ecm91*.root
#python FCCee/vertex/summary_plots.py --analysis impact_parameter -i FCCee/vertex/Zmumu_ecm91*/plots.root

#THE ONES I USE:
#python FCCee/vertex/plotting_leila_gun.py -i ParticleGun_Mu_standard_10GeV_20degrees.root
#python FCCee/vertex/plotting_leila_gun.py -i ParticleGun_Mu_*_1*GeV_*.root
#python FCCee/vertex/plotting_leila_gun.py -i ParticleGun_Mu_*.root
python FCCee/vertex/summary_plots_particle_gun.py --analysis impact_parameter 
