"""
Created on 2022
Henriques Lab

This scripts extracts the motility metrics from normlised videos. It analyses full directories and stores the data with
the corresponding conditions, dates and video names so all the results can be fully tracked.

It stores a csv file in the chosen output directory.

"""

import os
import sys
## Include the following lines to access the code in Python Console
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
SCRIPT_DIR = '/Users/esti/Documents/PROYECTOS/PHX/mitosis-mediated-phototoxic'
sys.path.append(SCRIPT_DIR)
from utils.fov_motility import extract_dynamics_metrics
from utils.display import plot_smooth_curves, plot_conditions_with_aggregates

main_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/masks/scaled_1.5709_results/stardist_prob03/"
# main_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/inputs/scaled_1.5709_results/2022-08-10/"
# main_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/inputs/scaled_1.5709_results/2022-08-10/WL UV - high density/Synchro"

output_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/results/scaled_1.5709_results/stardist_prob03"
folder = "dynamics_clahe"
if not os.path.exists(os.path.join(output_path, folder)):
    os.mkdir(os.path.join(output_path, folder))

method = "intensity"
condition = sys.argv[1] # "630"
dynamics_metrics = extract_dynamics_metrics(main_path, method=method, save_steps=False, enhance_contrast=True,
                                            output_path=os.path.join(output_path, folder), condition=condition)

dynamics_metrics.to_csv(os.path.join(output_path, folder, "data_dynamics_{0}_{1}.csv".format(method, condition)))
plot_conditions_with_aggregates(dynamics_metrics, "time_variance", "Dynamics_{0}_variance_{1}".format(method, condition),
                                os.path.join(output_path, folder),
                                "Dynamics_{0}_variance_2_{1}.png".format(method, condition), hue="Subcategory-02",
                                style="Subcategory-01")
#
# for c in np.unique(dynamics_metrics["Subcategory-01"]):
#     dynamics_group = dynamics_metrics[dynamics_metrics["Subcategory-01"] == c].reset_index(drop=True)
#
#     # plot_smooth_curves(dynamics_group, "time_variance", "Dynamics_variance_{}".format(c),
#     #                    os.path.join(output_path, folder), "Dynamics_variance_1_{}.png".format(c))
#     plot_conditions_with_aggregates(dynamics_group, "time_variance", "Dynamics_{0}_variance_{1}".format(method, c),
#                                     os.path.join(output_path, folder),
#                                     "Dynamics_{0}_variance_2_{1}.png".format(method, c), hue="Subcategory-02",
#                                     style="Subcategory-01")
#
#
