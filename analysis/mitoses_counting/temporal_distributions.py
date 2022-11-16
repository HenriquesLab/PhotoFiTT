"""
Created on 2022
Henriques Lab

This script is meant to run automatically. Results are stored as png and svg figures. It will calculate the
morphological measures of the segmented cells and display their distribution in time.
"""
from utils.display import plot_distributions, plot_smooth_curves
from utils.mitosis_counting import count_mitosis
import pandas as pd
import numpy as np
import os
import sys

main_path = sys.argv[1]
output_path = sys.argv[2]
frame_rate = int(sys.argv[3])
# main_path = "/Users/esti/Documents/PHX/mitosis_mediated_data/results/2021-12-20/scaled_x8/stardist_prob03"
# path = "/Users/esti/Documents/PHX/mitosis_mediated_data/annotations/2021-12-20/CHO_DIC_fast-acq_/"

r = 0.0 # Roundness
t_factor = 4  # In minutes
folders = os.listdir(main_path)
for f in folders:
    path = os.path.join(main_path, f)

    if os.path.isdir(path):
        if frame_rate == "unknown":
            if path.__contains__("damage_merged"):
                frame_rate = 10
            elif path.__contains__("fast"):
                frame_rate = 2
            elif path.__contains__("10"):
                frame_rate = 10
            elif path.__contains__("4"):
                frame_rate = 4
            else:
                print("Unrecognized group of data. Please indicate the frame rate in the code.")
                break
        data = count_mitosis(path, stacks=True, frame_rate=frame_rate, min_roundness=r)
        data = data[np.mod(data.frame, t_factor) == 0].reset_index(drop=True)
        ## Obtain cell size
        data_display = None
        for i in range(len(data)):
            cell = data.iloc[i]
            if cell.cell_size != []:
                CS = cell.cell_size
                RA = cell.roundness_axis
                t = cell.frame
                S0 = cell["Subcategory-00"]
                S1 = cell["Subcategory-01"]
                aux_data = [[t, CS[f], RA[f], S0, S1] for f in range(len(RA)) if RA[f] > r]
                col_names = ["frame", "cell_size", "roundness_axis", "Subcategory-00", "Subcategory-01"]
                aux = pd.DataFrame(aux_data, columns=col_names)
                if data_display is None:
                    data_display = aux
                else:
                    data_display = pd.concat([data_display, aux]).reset_index(drop=True)
        del data
        # variable = "roundness_axis"
        variable = "cell_size"
        data_display["Subcategory-02"] = "raw"
        plot_smooth_curves(data_display, variable, "Cell size (pixels)", path, "cell_size.png")
        groups = np.unique(data_display["Subcategory-00"])
        if not os.path.exists(os.path.join(output_path, f)):
            os.mkdir(os.path.join(output_path, f))
        for g in groups:
            data = data_display[data_display["Subcategory-00"] == g]
            # Create the data
            df = pd.DataFrame(dict(variable=data[variable], frame=data["frame"]))
            plot_distributions(df, "Cell Size (pixels)", g, os.path.join(output_path, f, g), smoothness=0.3)
