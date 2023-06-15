"""
Created on 2022
Henriques Lab

This scripts extracts the motility metrics from normlised videos. It analyses full directories and stores the data with
the corresponding conditions, dates and video names so all the results can be fully tracked.

It stores a csv file in the chosen output directory.

"""

import os
import sys
from photofitt.analysis import extract_motion
from photofitt.display import smooth_curves, conditions_with_aggregates




main_path = sys.argv[1]
output_path = sys.argv[2]
condition = sys.argv[3] # "630", "WL UV - high..."



# main_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/inputs/scaled_1.5709_results/2022-08-10/"
# main_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/inputs/scaled_1.5709_results/2022-08-10/WL UV - high density/Synchro"
# output_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/results/scaled_1.5709_results/stardist_prob03"


method = sys.argv[4] # "intensity"

folder = "motion_clahe-{}".format(method)
if not os.path.exists(os.path.join(output_path, folder)):
    os.mkdir(os.path.join(output_path, folder))

motion_metrics = extract_motion(main_path, method=method, save_steps=False, enhance_contrast=True,
                                            output_path=os.path.join(output_path, folder), condition=condition)
print(motion_metrics)
motion_metrics.to_csv(os.path.join(output_path, folder, "data_motion_{0}_{1}.csv".format(method, condition)))
conditions_with_aggregates(motion_metrics, "time_variance", "Motion_{0}_variance_{1}".format(method, condition),
                                os.path.join(output_path, folder),
                                "Motion_{0}_variance_0_{1}.png".format(method, condition), hue="Subcategory-02",
                                style="Subcategory-01")
#
# for c in np.unique(motion_metrics["Subcategory-01"]):
#     motion_group = motion_metrics[motion_metrics["Subcategory-01"] == c].reset_index(drop=True)
#
#     # smooth_curves(motion_group, "time_variance", "Motion_variance_{}".format(c),
#     #                    os.path.join(output_path, folder), "Motion_variance_1_{}.png".format(c))
#     conditions_with_aggregates(motion_group, "time_variance", "Motion_{0}_variance_{1}".format(method, c),
#                                     os.path.join(output_path, folder),
#                                     "Motion_{0}_variance_2_{1}.png".format(method, c), hue="Subcategory-02",
#                                     style="Subcategory-01")
#
#
