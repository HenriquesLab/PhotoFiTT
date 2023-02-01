"""
Created on 2022
Henriques Lab

This script analyses the motility metrics extracted with `extract_fov_motility`.

The script is not meant to run automatically. It has sections to clean the data or concatenate it.
"""
import pandas as pd
import numpy as np
import os
import sys
## Include the following lines to access the code in Python Console
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
SCRIPT_DIR = '/Users/esti/Documents/PROYECTOS/PHX/mitosis-mediated-phototoxic'
sys.path.append(SCRIPT_DIR)
from utils.display import plot_info_wrt_peak, plot_mitosis, plot_size_chnage_wrt_peak
from utils.mitosis_counting import quantify_peaks

## GENERAL INFORMATION
## ------------------------
output_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/CHO/results/scaled_1.5709_results/stardist_prob03/"
output_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/HELA/results/scaled_1.5709_results/stardist_prob03/"

conditions = ['Control-sync', 'Synchro', 'UV25ms', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV01sec',
                'UV05sec',  'UV10sec', 'UV15sec', 'UV20sec', 'UV25sec']

# Read mitosis information to be used later
# -----------------------------------------
folder = "mitosis_mediated_analysis"
folder = "mitosis-mediated-results"
data = pd.read_csv(
    os.path.join(output_path, folder, "data_clean.csv"))
data = data[data["processing"]=="Raw"].reset_index(drop=True)
aux = data[data["Subcategory-02"] == 'UV1000ms']
data.loc[aux.index.to_list(), ["Subcategory-02"]] = ['UV01sec']


# Read information about motility
folder = "dynamics_clahe"
# condition = ["UV_clean", "475_clean", "630", "568"]
condition = ['WL 475 - high density', 'WL 568 - high density',
       'WL 630 - high density', 'WL UV - high density']
condition = ['WL UV - high density']
for c in condition:
    ## Folder for the outputs
    output_path_plots = os.path.join(output_path, folder, c)
    os.makedirs(output_path_plots, exist_ok=True)
    ## Read motility data and plot it
    dynamics_metrics = pd.read_csv(
        os.path.join(output_path, folder, "data_dynamics_intensity_{}.csv".format(c)))
    aux = dynamics_metrics[dynamics_metrics["Subcategory-02"] == 'UV1000ms']
    dynamics_metrics.loc[aux.index.to_list(), ["Subcategory-02"]] = ['UV01sec']
    plot_mitosis(dynamics_metrics, output_path_plots, conditions, "time_variance")

    ## Get motility peaks (may not make sense) and plot it.
    data_dynamics_peaks = quantify_peaks(dynamics_metrics, "time_variance")
    hue_order = np.unique(dynamics_metrics["Subcategory-00"])
    plot_info_wrt_peak(data_dynamics_peaks, conditions, hue_order, output_path_plots)


    ## Calculate the mitoses peaks
    data_c = data[data["Subcategory-01"] == c].reset_index(drop=True)
    data_c = quantify_peaks(data_c, "mitosis")
    motility = []
    for f in np.unique(data_c["Subcategory-00"]):
        data_cf = data_c[data_c["Subcategory-00"]==f].reset_index(drop=True)
        dynamics_metrics_f = dynamics_metrics[dynamics_metrics["Subcategory-00"]==f].reset_index(drop=True)
        for v in np.unique(data_cf["video_name"]):
            data_cfv = data_cf[data_cf["video_name"] == v].reset_index(drop=True)
            dynamics_metrics_fv = dynamics_metrics_f[dynamics_metrics_f["video_name"] == v].reset_index(drop=True)
            peak = data_cfv["peak_time"].iloc[0]
            #peak=120
            mean_dynamics = np.mean(dynamics_metrics_fv[dynamics_metrics_fv["frame"]>peak]["time_variance"])
            motility.append([peak, mean_dynamics, f, v, c, dynamics_metrics_fv["Subcategory-02"].iloc[0]])
    motility_dataframe = pd.DataFrame(motility, columns=['peak', 'averaged_time_variance', 'Subcategory-00',
                                                         "video_name", 'Subcategory-01', "Subcategory-02"])
    plot_size_chnage_wrt_peak(motility_dataframe, conditions, "averaged_time_variance",
                              np.unique(motility_dataframe["Subcategory-00"]),
                              output_path_plots, y_lim=[0, 0.004])
#
#
# conditions = ['Control-sync', 'Synchro', 'UV25ms', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV01sec',
#               'UV05sec', 'UV10sec', 'UV15sec', 'UV20sec', 'UV25sec']
#


### TIME PEAK --------------------------------------------------------------------
### BOXPLOTS TIME POINTS
# conditions = ['Control-sync', 'Synchro', 'UV25ms', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV01sec',
#               'UV05sec', 'UV10sec', 'UV15sec', 'UV20sec', 'UV25sec']


# conditions_folders = ['2022-08-03', '2022-08-03-night', '2022-08-09', '2022-08-09-night',
#        '2022-08-10', '2022-09-08-night']



# plt.figure()
# sns.set_theme(style="whitegrid")
# # Draw a nested barplot by species and sex
# conditions = ['Control-sync', 'Synchro', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV1000ms', 'UV01sec',
#                     'UV05sec', 'UV10sec', 'UV15sec', 'UV20sec', 'UV25ms', 'UV25sec']
# g = sns.catplot(
#     data=aux, kind="violin", x="Subcategory-02", y="ratio", hue="Subcategory-01", order=conditions,
#     palette="dark", alpha=.6, height=6
# )
# g.despine(left=True)
# g.set_axis_labels("", "motility")
# plt.yscale("log")
# plt.show()

#
# # aux = aux[aux["Subcategory-00"]=='2022-08-09-night']
# aux1 = dynamics_metrics_data[dynamics_metrics_data["Subcategory-02"]=='UV25sec']
# plt.figure()
# # ax = sns.swarmplot(data=aux1, x="Subcategory-02", y="ratio", hue="video_name", palette="dark")
# ax = sns.lineplot(data=aux1, x="frame", y="time_variance", hue="video_name", palette="dark")
# plt.yscale("log")
# sns.set(font_scale=1)
# # plt.ylim([0,10])
# # plt.yscale("log")
# plt.show()

#
# sns.set_theme(style="dark")
#
# # Plot each year's time series in its own facet
# g = sns.relplot(
#     data=dynamics_metrics,
#     x="frame", y="time_variance", col="Subcategory-02", hue="Subcategory-00",
#     kind="line", palette="crest", linewidth=4, zorder=5,
#     col_wrap=3, height=2, aspect=1.5, legend=False,
# )
#
# # Iterate over each subplot to customize further
# for year, ax in g.axes_dict.items():
#
#     # Add the title as an annotation within the plot
#     ax.text(.8, .85, year, transform=ax.transAxes, fontweight="bold")
#
#     # Plot every year's time series in the background
#     sns.lineplot(
#         data=dynamics_metrics, x="frame", y="time_variance", units="Subcategory-02",
#         estimator=None, color=".7", linewidth=1, ax=ax,
#     )
#
# # Reduce the frequency of the x axis ticks
# ax.set_xticks(ax.get_xticks()[::2])
#
# # Tweak the supporting aspects of the plot
# g.set_titles("")
# g.set_axis_labels("", "Passengers")
# g.tight_layout()