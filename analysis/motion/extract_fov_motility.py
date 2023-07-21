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
from photofitt.display import smooth_curves, conditions_with_aggregates, conditions
from photofitt.utils import numerical_dose, power_conversion
import numpy as np

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

# action_metrics = extract_activity(main_path, method=method, save_steps=False, enhance_contrast=True,
#                                  output_path=os.path.join(output_path, folder), condition=condition)
import pandas as pd

print("Reading data")
action_metrics = pd.read_csv(os.path.join(output_path, folder, "data_activity_{0}.csv".format(method)))

# Estimate the ligth dose
print("Estimating the light dose and power conditions")
light_power = 6.255662
action_metrics = numerical_dose(action_metrics, column_name="Subcategory-02", power=light_power)
action_metrics = power_conversion(action_metrics)

# if wl == "None" or wl == None:
#    action_metrics.to_csv(os.path.join(output_path, folder, "data_activity_{0}.csv".format(method)))
# else:
#    action_metrics.to_csv(os.path.join(output_path, folder, "data_activity_{0}_{1}.csv".format(method, wl)))

y_var = [c for c in action_metrics.columns if c.__contains__("activity") or c.__contains__("active cells")]
hue = "Light dose cat"
hue_order = ['non-synchro-0 J/cm2', '0 J/cm2', '0.2 J/cm2',
             '0.3 J/cm2', '0.6 J/cm2', '1.3 J/cm2', '2.5 J/cm2',
             '5.0 J/cm2', '6.3 J/cm2', '31.3 J/cm2',
             '62.6 J/cm2', '93.8 J/cm2', '125.1 J/cm2', '156.4 J/cm2', '187.7 J/cm2']

for y in y_var:
    print(y)
    if wl == "None" or wl == None:
        conditions_with_aggregates(action_metrics, y, f"{y}_{method}_variance",
                                   os.path.join(output_path, folder),
                                   f"{y}_{method}_variance.png", hue=hue,
                                   style="Subcategory-01")
        for w in np.unique(action_metrics["Subcategory-01"]):
            print(w)
            import seaborn as sns
            action_metrics_w = action_metrics[action_metrics["Subcategory-01"] == w].reset_index(drop=True)

            conditions(action_metrics_w, y,
                       f"{y}_{method}_variance_{w}",
                       hue,
                       os.path.join(output_path, folder),
                       f"{y}_{method}_variance_{w}.png",
                       hue_order=hue_order,
                       palette=sns.color_palette("CMRmap_r", 17),
                       figsize=(7, 5), style=None)
    else:
        conditions_with_aggregates(action_metrics, y, f"{y}_{method}_variance_{wl}",
                                   os.path.join(output_path, folder),
                                   f"{y}_{method}_variance_{wl}.png", hue="Subcategory-02",
                                   style="Subcategory-01")
