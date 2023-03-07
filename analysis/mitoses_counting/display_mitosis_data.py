"""
Created on 20223
Henriques Lab

This script displays the information extracted from mitosis counting.
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
from utils.mitosis_counting import quantify_peaks
from utils.statistics import extract_gaussian_params
from utils.display import plot_info_wrt_peak, plot_mitosis, plot_conditions, plot_size_chnage_wrt_peak

output_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/CHO/results/scaled_1.5709_results/stardist_prob03/"
# output_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/HELA/results/scaled_1.5709_results/stardist_prob03/"
folder = "mitosis_mediated_analysis"
# folder = "mitosis-mediated-results"
data = pd.read_csv(
    os.path.join(output_path, folder, "data_clean.csv"))
data = data[data["processing"]=="Raw"].reset_index(drop=True)
aux = data[data["Subcategory-02"] == 'UV1000ms']
data.loc[aux.index.to_list(), ["Subcategory-02"]] = ['UV01sec']
conditions = ['Control-sync', 'Synchro', 'UV25ms', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV01sec',
                'UV05sec',  'UV10sec', 'UV15sec', 'UV20sec', 'UV25sec']
## Model cell size distribution
variable = "cell_size"
distribution_data = extract_gaussian_params(data, variable)
distribution_data.to_csv(os.path.join(output_path, folder, "cell_size_statistics.csv"))
distribution_data = pd.read_csv(os.path.join(output_path, folder, "cell_size_statistics.csv"))

for c in np.unique(data["Subcategory-01"]):
    data_c = data[data["Subcategory-01"]==c].reset_index(drop=True)

    output_path_plots = os.path.join(output_path, folder, c)
    os.makedirs(output_path_plots, exist_ok=True)

    # plot_mitosis(data_c, output_path_plots, conditions, "mitosis")

    data_c = quantify_peaks(data_c, "mitosis")
    hue_order = np.unique(data_c["Subcategory-00"])
    # plot_info_wrt_peak(data_c, conditions, hue_order, output_path_plots)

    aux = distribution_data[distribution_data["Subcategory-01"] == c].reset_index(drop=True)
    # aux["ratio"] = aux["GaussianMixtureCovariance_0"] / aux["GaussianMixtureCovariance_1"]
    # aux["subt_0"] = abs(aux["average"] - aux["GaussianMixtureMean_0"])
    # aux["subt_1"] = abs(aux["average"] - aux["GaussianMixtureMean_1"])

    plot_mitosis(aux, output_path_plots, conditions, "average")
    values = ["average", "derivative-average", "variance", 'GaussianMixtureMean_0', 'GaussianMixtureMean_1',
              'GaussianMixtureCovariance_0', 'GaussianMixtureCovariance_1']
    for v in values:
        print(v)
        plot_conditions(aux, v, "Cell size {}".format(v), "Subcategory-02", output_path_plots,
                        "size_{0}_{1}.png".format(v, c), style_condition="Subcategory-01", hue_order=conditions)
    ## We calculate the mean size of detected cells in the synchro group in the peak (as we assume it's going to be the
    ## daughter ones)
    data_synchro = data_c[data_c["Subcategory-02"]=="Synchro"]
    ## Obtain the averaged timepoints in which the synchronised field of views for this specific replica got the maximum
    ## number of cells: understood as cell division
    peak_timepoint = np.percentile(data_synchro["peak_time"], 75)
    data_synchro = aux[aux["Subcategory-02"] == "Synchro"]
    ## We get the shape of the cells at the estimated cell division time-point. We could also get it at each peak of
    ## each FOV but they should be very similar.
    time_point = np.where(abs(data_synchro["frame"]-peak_timepoint) == np.min(abs(data_synchro["frame"]-peak_timepoint)))
    synchro_mean_size = np.mean(data_synchro["average"].iloc[time_point])
    peak_data = []
    for exp in np.unique(aux["Subcategory-02"]):
        data_exp = aux[aux["Subcategory-02"]==exp].reset_index(drop=True)
        data_exp["compared_peak"] = data_exp["average"] - synchro_mean_size
        data_exp = data_exp[data_exp["frame"] > (peak_timepoint/2)].reset_index(drop=True)
        for f in np.unique(data_exp["Subcategory-00"]):
            data_f = data_exp[data_exp["Subcategory-00"] == f].reset_index(drop=True)
            t = np.min(data_f[data_f["compared_peak"] < 0]["frame"])
            peak_data.append([t, f, exp])
    peak_dataframe = pd.DataFrame(peak_data, columns=['mitosis_t', 'Subcategory-00', 'Subcategory-02'])
    plot_size_chnage_wrt_peak(peak_dataframe, conditions, "mitosis_t", np.unique(aux["Subcategory-00"]),
                              output_path_plots, y_lim=[0, 300])







### PLOTS FOR THE PAPER
c = 'WL UV - high density'
output_path_plots = os.path.join(output_path, "PAPER-PLOTS", c)
os.makedirs(output_path_plots, exist_ok=True)
hue_order = ['Control-sync', 'Synchro', 'UV25ms', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV01sec',
                'UV05sec',  'UV10sec', 'UV15sec', 'UV20sec', 'UV25sec']
LEN_C = len(hue_order)
data_c = data[data["Subcategory-01"]==c].reset_index(drop=True)

non_conditions = ['UV25ms', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms',  'UV01sec', 'UV10sec', 'UV15sec',
                  'UV20sec', 'UV25sec']
for c in non_conditions:
    aux = data_c[data_c["Subcategory-02"] == c]
    index = aux.index.to_list()
    data_c = data_c.drop(index)
data_c = data_c.reset_index(drop=True)

import seaborn as sns
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(5, 8))
plt.rcParams.update({'font.size': 15})
sns.lineplot(x="frame", y="mitosis", hue="Subcategory-02", data=data_c,
             palette=sns.color_palette("husl", 14), legend=False,
             hue_order=hue_order, linewidth=1.5, alpha=1)
plt.tight_layout()
plt.xlabel("Time (minutes)")
plt.ylabel("Counts of rounded cells")



distribution_data = extract_gaussian_params(data_c, "cell_size")

fig = plt.figure(figsize=(5, 8))
plt.rcParams.update({'font.size': 15})
sns.lineplot(x="frame", y="average", hue="Subcategory-02", data=distribution_data,
             palette=sns.color_palette("husl", 14), legend=False,
             hue_order=hue_order, linewidth=1.5, alpha=1)
plt.tight_layout()
plt.xlabel("Time (minutes)")
plt.ylabel("Cell size (pixels)")



plt.title("{0} along time".format("mitosis"))
# fig.savefig(os.path.join(output_path_plots, "data_{}_counting.png".format("mitosis")), format='png',
#             transparent=True)

c = 'WL UV - high density'
folder = "dynamics_clahe"
dynamics_metrics = pd.read_csv(
    os.path.join(output_path, folder, "data_dynamics_intensity_{}.csv".format(c)))

aux = dynamics_metrics[dynamics_metrics["Subcategory-02"] == 'UV1000ms']
dynamics_metrics.loc[aux.index.to_list(), ["Subcategory-02"]] = ['UV01sec']
for c in non_conditions:
    aux = dynamics_metrics[dynamics_metrics["Subcategory-02"] == c]
    index = aux.index.to_list()
    dynamics_metrics = dynamics_metrics.drop(index)
dynamics_metrics = dynamics_metrics.reset_index(drop=True)


fig = plt.figure(figsize=(5, 8))
plt.rcParams.update({'font.size': 15})
sns.lineplot(x="frame", y="time_variance", hue="Subcategory-02", data=dynamics_metrics,
             palette=sns.color_palette("husl", 14), legend=False,
             hue_order=hue_order, linewidth=1.5, alpha=1)
plt.tight_layout()
plt.xlabel("Time (minutes)")
plt.ylabel("Cell shape dynamics")

plt.title("{0} along time".format("mitosis"))








    ## ALTERNATIVE
    ## We calculate the mean size of detected cells in the synchro group in the peak (as we assume it's going to be the
    ## daughter ones)
    # peak_data = []
    # for f in np.unique(data_c["Subcategory-00"]):
    #     ## Estimate the cell size in the synchronised group at the time of cell division, folderwise as the experiments
    #     ## will have a bias on each replica.
    #     data_cf = data_c[data_c["Subcategory-00"] == f].reset_index(drop=True)
    #     data_synchro = data_cf[data_cf["Subcategory-02"]=="Synchro"]
    #     ## Obtain the averaged timepoints in which the synchronised field of views for this specific replica got the maximum
    #     ## number of cells: understood as cell division
    #     peak_timepoint = np.percentile(data_synchro["peak_time"], 75)
    #     aux_f = aux[aux["Subcategory-00"] == f].reset_index(drop=True)
    #     data_synchro = aux_f[aux_f["Subcategory-02"] == "Synchro"].reset_index(drop=True)
    #     ## We get the shape of the cells at the estimated cell division time-point. We could also get it at each peak of
    #     ## each FOV but they should be very similar.
    #     time_point = np.where(abs(data_synchro["frame"]-peak_timepoint) == np.min(abs(data_synchro["frame"]-peak_timepoint)))
    #     synchro_mean_size = np.mean(data_synchro["average"].iloc[time_point])
    #     ## Go for each video, estimating the cell division time point. Each folder has a unique name for the videos. So
    #     ## we don't need to go through the conditions
    #     for v in np.unique(aux_f["video_name"]):
    #         data_exp = aux_f[aux_f["video_name"]==v].reset_index(drop=True)
    #         data_exp["compared_peak"] = data_exp["average"] - synchro_mean_size
    #         data_exp = data_exp[data_exp["frame"]>60].reset_index(drop=True)
    #         if len(data_exp) > 0:
    #             ## We only add information of those videos which detected some cells (mitoses occurs from 60 minutes on)
    #             t = np.min(data_exp[data_exp["compared_peak"] < 0]["frame"])
    #             exp = data_exp['Subcategory-02'].iloc[0]
    #             peak_data.append([t, f, exp, v])
    #     peak_dataframe = pd.DataFrame(peak_data, columns=['mitosis_t', 'Subcategory-00', 'Subcategory-02', 'video_name'])
    # plot_size_chnage_wrt_peak(peak_dataframe, conditions, "mitosis_t", np.unique(aux["Subcategory-00"]),
    #                           output_path_plots, y_lim=[0, np.max(peak_data[mitosis_t])])
