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
from utils.display import plot_info_wrt_peak, plot_mitosis, plot_conditions
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

for c in np.unique(data["Subcategory-01"]):
    data_c = data[data["Subcategory-01"]==c].reset_index(drop=True)

    output_path_plots = os.path.join(output_path, folder, c)
    os.makedirs(output_path_plots, exist_ok=True)

    plot_mitosis(data_c, output_path_plots, conditions, "mitosis")

    data_c = quantify_peaks(data_c, "mitosis")
    hue_order = np.unique(data_c["Subcategory-00"])
    plot_info_wrt_peak(data_c, conditions, hue_order, output_path_plots)


## Model cell size distribution
variable = "cell_size"
distribution_data = extract_gaussian_params(data, variable)
distribution_data.to_csv(os.path.join(output_path, folder, "cell_size_statistics.csv"))


for g in np.unique(distribution_data["Subcategory-01"]):
    aux = distribution_data[distribution_data["Subcategory-01"] == g].reset_index(drop=True)
    aux["ratio"] = aux["GaussianMixtureCovariance_0"] / aux["GaussianMixtureCovariance_1"]
    output_path_plots = os.path.join(output_path, folder, g)
    plot_mitosis(aux, output_path_plots, conditions, "ratio")
    plot_conditions(aux, "ratio", "Cell size average", "Subcategory-02", os.path.join(output_path, folder),
                    "size_ratio_{}.png".format(g), style_condition="Subcategory-01")
