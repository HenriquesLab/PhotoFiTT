"""
Created on 2022
Henriques Lab

This script is meant to run automatically. Results are stored as csv files with the corresponding conditions, dates and
video names so all the results can be fully tracked.
"""
import sys
import os
## Include the following lines to access the code in Python Console
sys.path.append("/Users/esti/Documents/PROYECTOS/PHX/mitosis-mediated-phototoxic")
from utils.mitosis_counting import count_mitosis_all, smooth
from utils.display import plot_conditions, plot_one_condition, plot_distributions
import numpy as np
import pandas as pd

# main_path = sys.argv[1]
# output_path = sys.argv[2]
main_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/HELA/masks/scaled_1.5709_results/stardist_prob03"
output_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/HELA/results/scaled_1.5709_results/stardist_prob03/"


## PARAMETERS USED TO COMPUTE PLOTS
#--------------------------------------------------------------
r = 0.0 # We can filter out by roundness of the segmented cells
t_win = 5 # The size of the window (kernel) that is used to smooth the curves
max_t = 300 # The maximum length in minutes of the videos that we will analyse
max_frame_rate = 4 # The time gap we will use to compute all the metrics

# GET THE DATA AND FILTER IT WITH THE PARAMETERS
#--------------------------------------------------------------
data = count_mitosis_all(main_path, stacks=True, min_roundness=r, t_win=t_win, frame_rate=4)
data.to_csv(os.path.join(output_path, "data.csv"))
# # Read the original data
# data = pd.read_csv(os.path.join(output_path, "data.csv"))


# PLOT THE RESULTS FOR EACH CONDITION SEPARATELY
#--------------------------------------------------------------
# Subcategory-02 filters out the different conditions such as control, synch, uv10sec or uv 30sec
density = np.unique(data['Subcategory-01'])
classes = np.unique(data['Subcategory-02'])
for d in density:
    data_d = data[data["Subcategory-01"]==d].reset_index(drop=True)
    for c in classes:
        data_c = data_d[data_d["Subcategory-02"]==c].reset_index(drop=True)
        data_c["unique_name"] = data_c["Subcategory-00"] + data_c["Subcategory-01"] + data_c["Subcategory-02"] +\
                                data_c["video_name"]

        y_var = "mitosis_normalised"
        name = d + "_" + c + "_" + y_var + "_roundness-{}.png".format(r)
        plot_one_condition(data_c, y_var, output_path, name, hue1="unique_name", hue2="Subcategory-02",
                           frame_rate=max_frame_rate)

        y_var = "mitosis"
        name = d + "_" + c + "_" + y_var + "_roundness-{}.png".format(r)
        plot_one_condition(data_c, y_var, output_path, name, hue1="unique_name", hue2="Subcategory-02",
                           frame_rate=max_frame_rate)
    ## PLOT ALL THE CONDITIONS FOR EACH DENSITY VALUE
    title = "Minimum roundness {}".format(r)
    condition = "Subcategory-02"
    y_var = "mitosis"
    name = d + "_" + y_var + "_roundness-{}.png".format(r)
    plot_conditions(data_d, y_var, title, condition, output_path, name, style_condition="processing")

    y_var = "mitosis_normalised"
    name = d + "_" + y_var + "_roundness-{}.png".format(r)
    plot_conditions(data_d, y_var, title, condition, output_path, name, style_condition="processing")

    # TEMPORAL DISTRIBUTION OF SIZE
    # --------------------------------------------------------------
    ## Obtain cell size
    data_display = None
    for i in range(len(data_d)):
        cell = data_d.iloc[i]
        if cell.cell_size != []:
            CS = cell.cell_size
            RA = cell.roundness_axis
            t = cell.frame
            S0 = cell["Subcategory-01"] # Density
            S1 = cell["Subcategory-02"] # Condition
            aux_data = [[t, CS[f], RA[f], S0, S1] for f in range(len(RA)) if RA[f] > r]
            col_names = ["frame", "cell_size", "roundness_axis", "Subcategory-00", "Subcategory-01"]
            aux = pd.DataFrame(aux_data, columns=col_names)
            if data_display is None:
                data_display = aux
            else:
                data_display = pd.concat([data_display, aux]).reset_index(drop=True)

    # variable = "roundness_axis"
    variable = "cell_size"
    data_display["processing"] = "raw"
    plot_conditions(data_display, variable, "Cell size (pixels)", "Subcategory-01", output_path,
                    d + "_" + variable + "_roundness-{}.png".format(r), style_condition="processing")
    groups = np.unique(data_display["Subcategory-01"])
    for g in groups:
        data_g = data_display[data_display["Subcategory-01"] == g]
        # Create the data
        df = pd.DataFrame(dict(variable=data_g[variable], frame=data_g["frame"]))
        plot_distributions(df, "Cell Size (pixels)", g, os.path.join(output_path, d + "_" + g), smoothness=0.3)
