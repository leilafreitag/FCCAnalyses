
#!/bin/bash

# Manually listing the input files for the comparison plotting in summary_plots_leila.py so that order of legend is the way I want.
#input_files=("FCCee/vertex/Zmumu_ecm91_standard_plots/plots.root
#              FCCee/vertex/Zmumu_ecm91_R1.3_plots/plots.root
#             ")

#echo $input_files



#THE ONES I USE:
#python FCCee/vertex/plotting_leila_gun.py -i ParticleGun_Mu_*10GeV*.root
#python FCCee/vertex/plotting_leila_gun.py -i ParticleGun_Mu_*1GeV*.root
#python FCCee/vertex/plotting_leila_gun.py -i ParticleGun_Mu_*100GeV*.root

#python FCCee/vertex/plotting_leila_gun.py -i ParticleGun_Mu_*_0.5GeV_*.root
#python FCCee/vertex/plotting_leila_gun.py -i ParticleGun_Mu_*.root

#python FCCee/vertex/summary_plots_particle_gun.py --analysis impact_parameter 

python FCCee/vertex/summary_plots_particle_gun_fits.py --analysis impact_parameter #for fitting

#python FCCee/vertex/summary_plots_particle_gun_extra.py --analysis impact_parameter #for 0.5 GeV

