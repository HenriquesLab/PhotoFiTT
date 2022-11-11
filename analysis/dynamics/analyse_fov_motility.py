from tifffile import imread, imsave
import matplotlib.pyplot as plt
import os
import sys
import numpy as np
## Include the following lines to access the code in Python Console
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
SCRIPT_DIR = '/Users/esti/Documents/PROYECTOS/PHX/mitosis-mediated-phototoxic'
sys.path.append(SCRIPT_DIR)
from utils.fov_motility import extract_dynamics_metrics
from utils.display import plot_smooth_curves,  plot_conditions_with_aggregates

main_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/masks/scaled_1.5709_results/stardist_prob03/"
output_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/results/scaled_1.5709_results/stardist_prob03"
folder = "dynamics"
if not os.path.exists(os.path.join(output_path, folder)):
    os.mkdir(os.path.join(output_path, folder))

dynamics_metrics = extract_dynamics_metrics(main_path, save_steps=False)
dynamics_metrics.to_csv(os.path.join(output_path, folder, "data_dynamics.csv"))

for c in np.unique(dynamics_metrics["Subcategory-01"]):
    dynamics_group = dynamics_metrics[dynamics_metrics["Subcategory-01"]==c].reset_index(drop=True)

    plot_smooth_curves(dynamics_group, "mitoses", "Dynamics_variance_{}".format(c),
                       os.path.join(output_path, folder), "Dynamics_variance_1_{}.png".format(c))
    plot_conditions_with_aggregates(dynamics_group, "mitoses",  "Dynamics_variance_{}".format(c),
                                    os.path.join(output_path, folder), "Dynamics_variance_2_{}.png".format(c),
                                    hue="Subcategory-02", style="Subcategory-01")
