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
wl = sys.argv[4]  # "new_data, None, wl, uv, ...
method = sys.argv[5]  # "intensity"

if condition != "None":
    pass

else:
    condition = None

folder = "activity_clahe-{}".format(method)
os.makedirs(os.path.join(output_path, folder), exist_ok=True)

action_metrics = extract_activity(main_path, method=method, save_steps=False, enhance_contrast=True,
                                  output_path=os.path.join(output_path, folder), condition=condition)

if wl == "None" or wl == None:
    action_metrics.to_csv(os.path.join(output_path, folder, "data_activity_{0}.csv".format(method)))
else:
    action_metrics.to_csv(os.path.join(output_path, folder, "data_activity_{0}_{1}.csv".format(method, wl)))

y_var = [c for c in action_metrics.columns if c.__contains__("activity") or c.__contains__("active cells")]
for y in y_var:
    print(y)
    if wl == "None" or wl == None:
        conditions_with_aggregates(action_metrics, y, f"{y}_{method}_variance",
                                   os.path.join(output_path, folder),
                                   f"{y}_{method}_variance.png", hue="Subcategory-02",
                                   style="Subcategory-01")
    else:
        conditions_with_aggregates(action_metrics, y, f"{y}_{method}_variance_{wl}",
                                   os.path.join(output_path, folder),
                                   f"{y}_{method}_variance_{wl}.png", hue="Subcategory-02",
                                   style="Subcategory-01")
