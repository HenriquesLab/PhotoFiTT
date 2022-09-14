import os
import sys

# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))
SCRIPT_DIR = '/Users/esti/Documents/PROYECTOS/PHX/mitosis-mediated-phototoxic'
sys.path.append(SCRIPT_DIR)
from utils.statistics import run_fitting, gaussian_function, data_statistics
from utils.mitosis_counting import smooth
from utils.display import plot_conditions_with_aggregates
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

## Main path to the data with all the mitotic counts
main_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/results/scaled_1.5709_results/stardist_prob03/"
data_path = os.path.join(main_path, "data_old.csv")
# Read the original data
data_raw = pd.read_csv(data_path)
data_raw = data_raw[data_raw["processing"] == "Raw"]
# Create a the grouping column to run curve fitting
unique_col = [i for i in data_raw.keys() if i.__contains__("Subcategory") and i != "Subcategory-00"]
unique_name = data_raw[unique_col].apply("-".join, axis=1)
data_raw["unique_name"] = unique_name
# data = run_fitting(data_raw, "frame", "mitosis", "unique_name", symmetric2padding=True)

### Data WL = UV
data_UV = data_raw[data_raw["Subcategory-01"] == "WL UV - high density"]
ref_group = "WL UV - high density-Synchro"
var0 = "frame"
var1 = "mitosis"
group_var = "unique_name"
probability_function = "gauss-least-squares"
ref_lim_var0 = 80
DS = data_statistics(data_UV, var0, var1, group_var, probability_function=probability_function, ref_group=ref_group)
fitted_groups_UV, dev_UV = DS.estimate_deviation(ref_lim_var0=ref_lim_var0, fixed_peak=True)
print("Estimated mean value: {}".format(DS.ref_mu))
print("Estimated standard deviation: {}".format(DS.ref_sigma))
plot_conditions_with_aggregates(fitted_groups_UV, "mitosis",
                                "ref and biases {}".format(ref_group),
                                os.path.join(main_path),
                                "ref and biases {}.png".format(ref_group),
                                hue="unique_name", style="type")
ref_group_index = (np.where(data_UV[group_var] == ref_group)[0])
data_ref_group = data_UV.iloc[ref_group_index]
x = np.squeeze(np.array(data_ref_group[var0]))
y = gaussian_function(x, DS.ref_mu, DS.ref_sigma, DS.ref_amplitude)
data_ref_gaussian = data_ref_group.copy()
data_ref_gaussian[var1] = y
data_ref_gaussian["processing"] = "Gaussian fit"
data_ref_group = pd.concat([data_ref_group, data_ref_gaussian]).reset_index(drop=True)
plot_conditions_with_aggregates(data_ref_group, "mitosis",
                                "ref {}".format(ref_group),
                                os.path.join(main_path),
                                "ref {}.png".format(ref_group),
                                hue="Subcategory-00", style="processing")

### Data WL = 568
data_568 = data_raw[data_raw["Subcategory-01"] == "WL 568 - high density"]
ref_group = "WL 568 - high density-Synchro"
DS = data_statistics(data_568, var0, var1, group_var, probability_function=probability_function, ref_group=ref_group)
fitted_groups_568, dev_568 = DS.estimate_deviation(ref_lim_var0=ref_lim_var0, fixed_peak=True)
print("Estimated mean value: {}".format(DS.ref_mu))
print("Estimated standard deviation: {}".format(DS.ref_sigma))
plot_conditions_with_aggregates(fitted_groups_568, "mitosis",
                                "ref and biases {}".format(ref_group),
                                os.path.join(main_path),
                                "ref and biases {}.png".format(ref_group),
                                hue="unique_name", style="type")
ref_group_index = (np.where(data_568[group_var] == ref_group)[0])
data_ref_group = data_568.iloc[ref_group_index]
x = np.squeeze(np.array(data_ref_group[var0]))
y = gaussian_function(x, DS.ref_mu, DS.ref_sigma, DS.ref_amplitude)
data_ref_gaussian = data_ref_group.copy()
data_ref_gaussian[var1] = y
data_ref_gaussian["processing"] = "Gaussian fit"
data_ref_group = pd.concat([data_ref_group, data_ref_gaussian]).reset_index(drop=True)
plot_conditions_with_aggregates(data_ref_group, "mitosis",
                                "ref {}".format(ref_group),
                                os.path.join(main_path),
                                "reef {}.png".format(ref_group),
                                hue="Subcategory-00", style="processing")







# Run the fitting
# contains the temporal curves smoothed for each independent field of view
data_smooth = pd.DataFrame()
# One experiment (replica) is composed by different field of vies (of the wheel). We first smooth them to get rid of the false positives and negatives,
# and then, we average the results to get an estimate for each experiment (wheel).
data_average = pd.DataFrame()
for v in np.unique(data_raw['unique_name']):
    video = data_raw[data_raw["unique_name"] == v]
    video = video.sort_values('frame')
    # video['Subcategory-03'] = 'Raw'
    # smooth
    aux_unique = pd.DataFrame()
    for fov_name in video["video_name"].unique():
        t_win = 5
        fov = video[video["video_name"] == fov_name]
        y = smooth(fov['mitosis'], t_win)
        # store smooth values
        video3 = fov.copy()
        video3['processing'] = 'Averaged-kernel{}'.format(t_win)
        video3['mitosis'] = y
        # video = pd.concat([video,video3]).reset_index(drop=True)
        aux_unique = pd.concat([aux_unique, video3]).reset_index(drop=True)
    data_smooth = pd.concat([data_smooth, aux_unique]).reset_index(drop=True)

    # Compute the average for each replicate
    aux = fov[['frame', 'mitosis', 'Subcategory-00', 'Subcategory-01', 'Subcategory-02', 'unique_name']].reset_index(
        drop=True)
    # aux['Subcategory-00'] = aux_unique['Subcategory-00'].iloc[0]
    # aux['Subcategory-01'] = aux_unique['Subcategory-01'].iloc[0]
    # aux['Subcategory-02'] = aux_unique['Subcategory-02'].iloc[0]
    # aux['unique_name'] = aux_unique['unique_name'].iloc[0]
    averages = []
    aux = aux.sort_values('frame')
    for t in aux["frame"].unique():
        averages.append(np.mean(aux_unique["mitosis"].iloc[list(np.where(aux_unique["frame"] == t)[0])]))
    aux['mitosis'] = averages
    data_average = pd.concat([data_average, aux]).reset_index(drop=True)
del video, video3

# plot_conditions_with_aggregates(data_average, "mitosis",
#                                         "Mean values per experiment",
#                                         os.path.join(main_path),
#                                         "Mean values per experiment.png",
#                                         hue="unique_name", style="unique_name")


print("Data averaged successfully")

data = run_fitting(data_average, "frame", "mitosis", "unique_name", symmetric2padding=False)
# data = run_fitting(data_smooth, "frame", "mitosis", "unique_name", symmetric2padding=True)

## Print the distribution of the fitted parameters
print(data.keys())
order = ['Control-sync', 'Synchro', 'UV25ms', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms',
         'UV01sec', 'UV05sec', 'UV10sec', 'UV15sec', 'UV20sec', 'UV25sec']

for WL in data["Subcategory-01"].unique():
    data_WL = data[data["Subcategory-01"] == WL]
    fig = plt.figure(figsize=(7, 7))
    plt.rcParams.update({'font.size': 8})
    plt.subplot(2, 2, 1)
    sns.boxplot(data=data_WL, x="upper_bound", y="Subcategory-02", order=order)
    # plt.xlim([-100, 400])
    plt.subplot(2, 2, 2)
    sns.boxplot(data=data_WL, x="mu", y="Subcategory-02", order=order)
    # plt.xlim([-200, 1000])

    plt.subplot(2, 2, 3)
    sns.boxplot(data=data_WL, x="sigma", y="Subcategory-02", order=order)
    # plt.xlim([0, 1500])
    plt.subplot(2, 2, 4)
    sns.boxplot(data=data_WL, x="least_squares", y="Subcategory-02", order=order)

    plt.tight_layout()
    fig.savefig(os.path.join(main_path, "gaussian_params_replicates_{}.png".format(WL)), format='png')
    plt.show()
del data_WL
## Visualize the results with respect with the true data
# Build data with original numbers and the fitted distributions
# temporal_data = pd.read_csv(data_path)
# unique_col = [i for i in temporal_data.keys() if i.__contains__("Subcategory")] #+ ["video_name"]
# unique_name = temporal_data[unique_col].apply("-".join, axis=1)
# temporal_data["unique_name"] = unique_name

data1 = pd.DataFrame()
for v in np.unique(data['unique_name']):
    video = data_raw[data_raw["unique_name"] == v]
    video = video.sort_values('frame')
    video['processing'] = 'Raw'

    # Estimated gaussian function
    gauss_params = data[data["unique_name"] == v]["dist_param"]
    a, x0, sigma = np.squeeze(gauss_params)
    frames = video['frame']
    gaussian_estimates = gaussian_function(frames, a, x0, sigma)
    video2 = video.copy()
    video2['processing'] = 'Gaussian'
    video2['mitosis'] = gaussian_estimates
    # video = pd.concat([video, video2]).reset_index(drop=True)
    # data1 = pd.concat([data1, video]).reset_index(drop=True)
    # video3 = data_smooth[data_smooth["unique_name"]==v]
    video3 = data_average[data_average["unique_name"] == v]
    video3['processing'] = 'Averaged'
    video = pd.concat([video, video2, video3]).reset_index(drop=True)
    data1 = pd.concat([data1, video]).reset_index(drop=True)

    # # smooth
    # video = pd.concat([video, video2]).reset_index(drop=True)
    # for fov_name in video["video_name"].unique():
    #     t_win = 25
    #     fov = video[video["video_name"]==fov_name]
    #     y = smooth(fov['mitosis'], t_win)
    #     # store smooth values
    #     video3 = fov.copy()
    #     video3['Subcategory-03'] = 'Averaged'
    #     video3['mitosis'] = y
    #     video = pd.concat([video,video3]).reset_index(drop=True)
    # data1 = pd.concat([data1, video]).reset_index(drop=True)

del video, video2, video3

# # Generate plots for all the videos to review the results
# experiments = data1["Subcategory-00"].unique()
# for exp in experiments:
#     data_exp = data1[data1["Subcategory-00"] == exp]
#     dosage = data_exp["Subcategory-02"].unique()
#     for d in dosage:
#         data_exp_d = data_exp[data_exp["Subcategory-02"] == d]
#         wl_folder = str(np.squeeze(data_exp_d["Subcategory-01"].unique()))
#         plot_conditions_with_aggregates(data_exp_d, "mitosis",
#                                         "Gaussian fit - {}".format(exp + "-" + wl_folder + "-" + d),
#                                         os.path.join(main_path),
#                                         "gaussian_fit_{}.png".format(exp + "-" + wl_folder + "-" + d),
#                                         hue="Subcategory-02", style="Subcategory-03")

# Generate plots for all the videos to review the results
experiments = data1["Subcategory-01"].unique()
for exp in experiments:
    data_exp = data1[data1["Subcategory-01"] == exp]
    dosage = data_exp["Subcategory-02"].unique()
    for d in dosage:
        data_exp_d = data_exp[data_exp["Subcategory-02"] == d]
        plot_conditions_with_aggregates(data_exp_d, "mitosis",
                                        "Gaussian fit - {}".format(exp + "-" + d),
                                        os.path.join(main_path),
                                        "gaussian_fit_{}.png".format(exp + "-" + d),
                                        hue="Subcategory-00", style="processing")
