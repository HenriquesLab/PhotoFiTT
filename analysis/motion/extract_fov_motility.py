"""
Created on 2022
Henriques Lab

This scripts extracts the motility metrics from normlised videos. It analyses full directories and stores the data with
the corresponding conditions, dates and video names so all the results can be fully tracked.

It stores a csv file in the chosen output directory.

"""

import os
import sys
from photofitt.analysis import extract_activity
from photofitt.display import smooth_curves, conditions_with_aggregates

# main_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/inputs/scaled_1.5709_results/2022-08-10/"
# main_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/inputs/scaled_1.5709_results/2022-08-10/WL UV - high density/Synchro"
# output_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/results/scaled_1.5709_results/stardist_prob03"

main_path = sys.argv[1]
output_path = sys.argv[2]
condition = sys.argv[3]  # "630", "WL UV - high..."
wl = sys.argv[4] # "new_data, None, wl, uv, ...
method = sys.argv[5]  # "intensity"

if condition != "None":
    pass

else:
    condition = None

folder = "activity_clahe-{}".format(method)
if not os.path.exists(os.path.join(output_path, folder)):
    os.mkdir(os.path.join(output_path, folder))

action_metrics = extract_activity(main_path, method=method, save_steps=True, enhance_contrast=True,
                                output_path=os.path.join(output_path, folder), condition=condition)
print(action_metrics)
if wl == "None" or wl==None:
    action_metrics.to_csv(os.path.join(output_path, folder, "data_activity_{0}.csv".format(method)))
    conditions_with_aggregates(action_metrics, "time_variance", "Activity_{0}_variance".format(method),
                               os.path.join(output_path, folder),
                               "Activity_{0}_variance_0.png".format(method), hue="Subcategory-02",
                               style="Subcategory-01")
else:

    action_metrics.to_csv(os.path.join(output_path, folder, "data_activity_{0}_{1}.csv".format(method, wl)))
    conditions_with_aggregates(action_metrics, "time_variance", "Activity_{0}_variance_{1}".format(method, wl),
                               os.path.join(output_path, folder),
                               "Activity_{0}_variance_0_{1}.png".format(method, wl), hue="Subcategory-02",
                               style="Subcategory-01")
