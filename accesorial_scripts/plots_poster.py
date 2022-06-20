import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from utils.display import plot_conditions, plot_distributions


output_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_initial_experiments/results/scaled_x8/stardist_prob03"
## PARAMETERS USED TO COMPUTE PLOTS
#--------------------------------------------------------------
r = 0.0 # We can filter out by roundness of the segmented cells
t_win = 5 # The size of the window (kernel) that is used to smooth the curves
max_t = 300 # The maximum length in minutes of the videos that we will analyse
max_frame_rate = 10 # The time gap we will use to compute all the metrics
data = pd.read_csv("/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_initial_experiments/results/scaled_x8/stardist_prob03/data.csv")
classes = np.unique(data['Subcategory-02'])




for c in classes:
    data_c = data[data["Subcategory-02"]==c].reset_index(drop=True)
    if c == 'Control-sync':
        max_t = 800
    else:
        max_t = 300
    data_c = data_c[data_c.frame < max_t].reset_index(drop=True)
    # data_c["Subcategory-03"] = data_c["Subcategory-03"].replace(np.nan, " ")
    # data_c["unique_name"] = data_c["Subcategory-01"] + data_c["Subcategory-02"] + data_c["Subcategory-03"] + data_c["video_name"]

    data_c["unique_name"] = data_c["Subcategory-01"] + data_c["Subcategory-02"] + data_c["video_name"]

    y_var = "mitosis"
    name = c + "_" + y_var + "_roundness-{}.svg".format(r)

    fig = plt.figure(figsize=(10, 15))
    sns.set(font_scale=3, style="white")
    plt.subplot(2, 1, 1)
    sns.lineplot(x="frame", y=y_var, hue="unique_name", data=data_c[data_c["processing"] == "Averaged-kernel5"], legend = False,
                 linewidth=5, alpha=1)
    plt.legend([])
    plt.ylabel("Mitosis (n)")
    plt.xlabel("Time (min)")

    # Plot the results per category
    ax = plt.subplot(2, 1, 2)
    data_s = data_c[data_c.processing == "Averaged-kernel5"].reset_index(drop=True)
    sns.lineplot(x="frame", y=y_var, hue="Subcategory-02",
                 data=data_s[np.mod(data_s.frame, max_frame_rate) == 0].reset_index(drop=True), legend = False,
                 linewidth=1, alpha=0.75)
    plt.xlabel("Time (min)")
    plt.ylabel("Mitosis (n)")
    ax.legend(bbox_to_anchor=(0.85, 0.5))
    plt.tight_layout()
    fig.savefig(os.path.join(output_path, name), format='svg')
    plt.show()

#
# # TEMPORAL DISTRIBUTION OF SIZE
# ## Obtain cell size
# max_t = 150 # The maximum length in minutes of the videos that we will analyse
# max_frame_rate = 20
# pixel_size = 0.1083333
# scaling_factor = 8
# data = data[data.frame < max_t].reset_index(drop=True)
# data = data[np.mod(data.frame, max_frame_rate) == 0].reset_index(drop=True)
# data_display = None
# for i in range(len(data)):
#     cell = data.iloc[i]
#     if cell.cell_size != [] and cell.cell_size != '[]':
#         CS = cell.cell_size[1:-1]
#         CS = CS.split(", ")
#         RA = cell.roundness_axis[1:-1]
#         RA = RA.split(", ")
#         t = cell.frame
#         S0 = cell["Subcategory-01"]
#         S1 = cell["Subcategory-02"]
#         aux_data = [[t, float(CS[f])*((pixel_size*scaling_factor)**2), float(RA[f]), S0, S1] for f in range(len(RA)) if float(RA[f]) > r]
#         col_names = ["frame", "cell_size", "roundness_axis", "Subcategory-00", "Subcategory-01"]
#         aux = pd.DataFrame(aux_data, columns=col_names)
#         if data_display is None:
#             data_display = aux
#         else:
#             data_display = pd.concat([data_display, aux]).reset_index(drop=True)
#
# # variable = "roundness_axis"
# variable = "cell_size"
# data_display["processing"] = "raw"
# plot_conditions(data_display, variable, "Cell size (pixels)", "Subcategory-01", output_path,
#                 variable + "_roundness-{}.png".format(r), style_condition="processing")
# groups = np.unique(data_display["Subcategory-01"])
# for g in groups:
#     data = data_display[data_display["Subcategory-01"] == g]
#     # Create the data
#     df = pd.DataFrame(dict(variable=data[variable], frame=data["frame"]))
#     plot_distributions(df, "Cell Size ($\mu$m)", g, os.path.join(output_path, g), smoothness=0.3)
