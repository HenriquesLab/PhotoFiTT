import os
import sys
from utils.mitosis_counting import count_mitosis_all, smooth
from utils.display import plot_conditions
import numpy as np

# main_path = sys.argv[1]
main_path = "/Users/esti/Documents/PHX/mitosis_mediated_data/masks/scaled_x8/stardist_prob03"
output_path = "/Users/esti/Documents/PHX/mitosis_mediated_data/results/scaled_x8/stardist_prob03"

## PARAMETERS USED TO COMPUTE PLOTS
#--------------------------------------------------------------
r = 0.0 # We can filter out by roundness of the segmented cells
t_win = 5 # The size of the window (kernel) that is used to smooth the curves
max_t = 400 # The maximum length in minutes of the videos that we will analyse
max_frame_rate = 10 # The time gap we will use to compute all the metrics

# GET THE DATA AND FILTER IT WITH THE PARAMETERS
#--------------------------------------------------------------
data = count_mitosis_all(main_path, stacks=True, min_roundness=r, t_win=t_win)
data = data[data.frame < max_t].reset_index(drop=True)
data = data[np.mod(data.frame, max_frame_rate) == 0].reset_index(drop=True)

## PLOTS
title = "Minimum roundness {}".format(r)
condition = "Subcategory-02"
y_var = "mitosis"
plot_conditions(data, y_var, title, condition, output_path,  y_var + "_roundness-{}.png".format(r),
                style_condition="processing")
y_var = "mitosis_normalised"
plot_conditions(data, y_var, title, condition, output_path, y_var + "_roundness-{}.png".format(r),
                style_condition="processing")


condition = "Subcategory-01"
y_var = "mitosis"
plot_conditions(data, y_var, title, condition, output_path,  y_var + condition + "_roundness-{}.png".format(r),
                style_condition="processing")
y_var = "mitosis_normalised"
plot_conditions(data, y_var, title, condition, output_path, y_var + condition + "_roundness-{}.png".format(r),
                style_condition="processing")

# TEMPORAL DISTRIBUTION OF SIZE
## Obtain cell size
import pandas as pd
from utils.display import plot_distributions
data_display = None
for i in range(len(data)):
    cell = data.iloc[i]
    if cell.cell_size != []:
        CS = cell.cell_size
        RA = cell.roundness_axis
        t = cell.frame
        S0 = cell["Subcategory-01"]
        S1 = cell["Subcategory-02"]
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
                variable + "_roundness-{}.png".format(r), style_condition="processing")
groups = np.unique(data_display["Subcategory-01"])
for g in groups:
    data = data_display[data_display["Subcategory-01"] == g]
    # Create the data
    df = pd.DataFrame(dict(variable=data[variable], frame=data["frame"]))
    plot_distributions(df, "Cell Size (pixels)", g, os.path.join(output_path, g), smoothness=0.3)