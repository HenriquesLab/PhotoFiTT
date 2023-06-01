"""
Created on 20223
Henriques Lab

This script displays the information extracted from mitosis counting.
"""
import pandas as pd
import numpy as np
import os
from photofitt.analysis import quantify_peaks, compare_peaks, extract_gaussian_params
from photofitt.display import display_data_from_masks, plot_conditions, plot_info_wrt_peak, plot_mitosis, \
                                plot_size_chnage_wrt_peak
import sys
## PARAMETERS USED TO COMPUTE PLOTS
#--------------------------------------------------------------
output_path = sys.argv[1]
folder = sys.argv[2]

# output_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/CHO/results/scaled_1.5709_results/stardist_prob03/"
# output_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/HELA/results/scaled_1.5709_results/stardist_prob03/"
# folder = "mitosis_mediated_analysis"
# folder = "mitosis-mediated-results"
data = pd.read_csv(
    os.path.join(output_path, folder, "data_clean.csv"))
data = data[data["processing"]=="Raw"].reset_index(drop=True)
aux = data[data["Subcategory-02"] == 'UV1000ms']
data.loc[aux.index.to_list(), ["Subcategory-02"]] = ['UV01sec']

## Model cell size distribution
variable = "cell_size"
distribution_data = extract_gaussian_params(data, variable)
distribution_data.to_csv(os.path.join(output_path, folder, "cell_size_statistics.csv"))
distribution_data = pd.read_csv(os.path.join(output_path, folder, "cell_size_statistics.csv"))


groups_comparison = np.unique(data["Subcategory-01"])
# Specified to ensure that all the plots have the same distribution of colors.
conditions = ['Control-sync', 'Synchro', 'UV25ms', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV01sec',
                'UV05sec',  'UV10sec', 'UV15sec', 'UV20sec', 'UV25sec']
for c in groups_comparison:
    output_path_plots = os.path.join(output_path, folder, c)
    os.makedirs(output_path_plots, exist_ok=True)
    # Filter the data for each group of the analysis.
    data_c = data[data["Subcategory-01"] == c].reset_index(drop=True)
    plot_mitosis(data_c, output_path_plots, conditions, "mitosis")

    # Integrate the information about the temporal peaks of mitosis
    data_c = quantify_peaks(data_c, "mitosis")
    plot_info_wrt_peak(data_c, conditions, conditions, output_path_plots)

    # Obtain statistics about the data.
    aux = distribution_data[distribution_data["Subcategory-01"] == c].reset_index(drop=True)
    # aux["ratio"] = aux["GaussianMixtureCovariance_0"] / aux["GaussianMixtureCovariance_1"]
    # aux["subt_0"] = abs(aux["average"] - aux["GaussianMixtureMean_0"])
    # aux["subt_1"] = abs(aux["average"] - aux["GaussianMixtureMean_1"])
    plot_mitosis(aux, output_path_plots, conditions, "average")

    # Display some of these statistics
    values = ["average", "derivative-average", "variance", 'GaussianMixtureMean_0', 'GaussianMixtureMean_1',
              'GaussianMixtureCovariance_0', 'GaussianMixtureCovariance_1']
    for v in values:
        print(v)
        plot_conditions(aux, v, "Cell size {}".format(v), "Subcategory-02", output_path_plots,
                        "size_{0}_{1}.png".format(v, c), style_condition="Subcategory-01", hue_order=conditions)

    # Compare the temporal peaks between groups and display them
    peak_dataframe = compare_peaks(data_c, aux, peak_percentile=75)
    plot_size_chnage_wrt_peak(peak_dataframe, conditions, "mitosis_t", np.unique(aux["Subcategory-00"]),
                              output_path_plots, y_lim=[0, 300])