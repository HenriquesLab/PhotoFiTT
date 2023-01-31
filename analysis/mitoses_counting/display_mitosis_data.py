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
from utils.display import plot_info_wrt_peak, plot_mitosis, plot_conditions, plot_size_chnage_wrt_peak
from utils.statistics import extract_gaussian_params

output_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/CHO/results/scaled_1.5709_results/stardist_prob03/"
folder = "mitosis_mediated_analysis"
condition = ["UV_clean", "475_clean", "630_clean", "568_clean"]
data = pd.read_csv(
    os.path.join(output_path, folder, "data_clean.csv"))
data = data[data["processing"]=="Raw"].reset_index(drop=True)
aux = data[data["Subcategory-02"] == 'UV1000ms']
data.loc[aux.index.to_list(), ["Subcategory-02"]] = ['UV01sec']
conditions = ['Control-sync', 'Synchro', 'UV25ms', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV01sec',
                'UV05sec',  'UV10sec', 'UV15sec', 'UV20sec', 'UV25sec']
## Model cell size distribution
variable = "cell_size"
# distribution_data = extract_gaussian_params(data, variable)
# distribution_data.to_csv(os.path.join(output_path, folder, "cell_size_statistics.csv"))
distribution_data = pd.read_csv(os.path.join(output_path, folder, "cell_size_statistics.csv"))

for c in np.unique(data["Subcategory-01"]):
    data_c = data[data["Subcategory-01"]==c].reset_index(drop=True)

    output_path_plots = os.path.join(output_path, folder, c)
    os.makedirs(output_path_plots, exist_ok=True)

    # plot_mitosis(data_c, output_path_plots, conditions, "mitosis")

    data_c = quantify_peaks(data_c, "mitosis")
    # hue_order = np.unique(data_c["Subcategory-00"])
    # plot_info_wrt_peak(data_c, conditions, hue_order, output_path_plots)

    aux = distribution_data[distribution_data["Subcategory-01"] == c].reset_index(drop=True)
    # aux["ratio"] = aux["GaussianMixtureCovariance_0"] / aux["GaussianMixtureCovariance_1"]
    # aux["subt_0"] = abs(aux["average"] - aux["GaussianMixtureMean_0"])
    # aux["subt_1"] = abs(aux["average"] - aux["GaussianMixtureMean_1"])

    # # plot_mitosis(aux, output_path_plots, conditions, "average")
    # values = ["average", "derivative-average", "variance", 'GaussianMixtureMean_0', 'GaussianMixtureMean_1',
    #           'GaussianMixtureCovariance_0', 'GaussianMixtureCovariance_1']
    # for v in values:
    #     print(v)
    #     plot_conditions(aux, v, "Cell size {}".format(v), "Subcategory-02", output_path_plots,
    #                     "size_{0}_{1}.png".format(v, c), style_condition="Subcategory-01", hue_order=conditions)

    data_synchro = data_c[data_c["Subcategory-02"]=="Synchro"]
    peak_timepoint = np.percentile(data_synchro["peak_time"], 75)
    data_synchro = aux[aux["Subcategory-02"] == "Synchro"]
    time_point = np.where(abs(data_synchro["frame"]-peak_timepoint) == np.min(abs(data_synchro["frame"]-peak_timepoint)))
    synchro_mean_size = np.mean(data_synchro["average"].iloc[time_point])
    peak_data = []
    for exp in np.unique(aux["Subcategory-02"]):
        data_exp = aux[aux["Subcategory-02"]==exp]
        data_exp["compared_peak"] = data_exp["average"] - synchro_mean_size
        data_exp = data_exp[data_exp["frame"]>60]
        for f in np.unique(data_exp["Subcategory-00"]):
            data_f = data_exp[data_exp["Subcategory-00"] == f]
            t = np.min(data_f[data_f["compared_peak"] < 0]["frame"])
            peak_data.append([t] + [f] + [exp])
    peak_dataframe = pd.DataFrame(peak_data, columns=['mitosis_t', 'Subcategory-00', 'Subcategory-02'])
    plot_size_chnage_wrt_peak(peak_dataframe, conditions, "mitosis_t", np.unique(data_exp["Subcategory-00"]), output_path_plots)
