import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
SCRIPT_DIR = '/Users/esti/Documents/PROYECTOS/PHX/mitosis-mediated-phototoxic'
sys.path.append(SCRIPT_DIR)
from utils.statistics import run_fitting
from utils.statistics import run_fitting, gaussian_function
from utils.mitosis_counting import smooth
from utils.display import plot_conditions_with_aggregates
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

## Main path to the data with all the mitotic counts
main_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/results/scaled_1.5709_results/stardist_prob03/"
data_path = os.path.join(main_path, "data.csv")
# Read the original data
data_raw = pd.read_csv(data_path)

# Create a the grouping column to run curve fitting
unique_col = [i for i in data_raw.keys() if i.__contains__("Subcategory")]
unique_name = data_raw[unique_col].apply("-".join, axis=1)
data_raw["unique_name"] = unique_name
# data = run_fitting(data_raw, "frame", "mitosis", "unique_name", symmetric2padding=True)

# Run the fitting
data_smooth = pd.DataFrame()
for v in np.unique(data_raw['unique_name']):
    video = data_raw[data_raw["unique_name"] == v]
    video = video.sort_values('frame')
    video['Subcategory-03'] = 'Raw'
    # smooth
    for fov_name in video["video_name"].unique():
        t_win = 25
        fov = video[video["video_name"]==fov_name]
        y = smooth(fov['mitosis'], t_win)
        # store smooth values
        video3 = fov.copy()
        video3['Subcategory-03'] = 'Averaged'
        video3['mitosis'] = y
        # video = pd.concat([video,video3]).reset_index(drop=True)
        data_smooth = pd.concat([data_smooth, video3]).reset_index(drop=True)

del video, video3

data = run_fitting(data_smooth, "frame", "mitosis", "unique_name", symmetric2padding=True)

## Print the distribution of the fitted parameters
print(data.keys())
order = ['Control-sync', 'Synchro', 'UV25ms', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms',
         'UV01sec', 'UV05sec', 'UV10sec', 'UV15sec', 'UV20sec', 'UV25sec']

for WL in data["Subcategory-01"].unique():
    data_WL = data[data["Subcategory-01"] == WL]
    fig = plt.figure(figsize=(7,7))
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
    video['Subcategory-03'] = 'Raw'

    # Estimated gaussian function
    gauss_params = data[data["unique_name"] == v]["dist_param"]
    a, x0, sigma = np.squeeze(gauss_params)
    frames = video['frame']
    gaussian_estimates = gaussian_function(frames, a, x0, sigma)
    video2 = video.copy()
    video2['Subcategory-03'] = 'Gaussian'
    video2['mitosis'] = gaussian_estimates
    # video = pd.concat([video, video2]).reset_index(drop=True)
    # data1 = pd.concat([data1, video]).reset_index(drop=True)
    video3 = data_smooth[data_smooth["unique_name"]==v]
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
                                        hue="Subcategory-00", style="Subcategory-03")
