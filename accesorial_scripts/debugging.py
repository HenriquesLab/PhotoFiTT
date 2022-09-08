import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import pandas as pd
def gaussian_function(x, a, x0, sigma):
    """
    Non normalised gaussian density (area under the curve >1)
    :param x: input value
    :param a: scaling factor and the maximum value expected for the non-normalised Gaussian density
    :param x0: mean value
    :param sigma: standard deviation
    :return: the probability density value of a Gaussian with mean x0, and standard deviation sigma.
    """
    return a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))


main_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/results/scaled_1.5709_results/stardist_prob03/"
data_path = os.path.join(main_path, "data.csv")
data = run_fitting(data_path, "frame", "mitosis")

temporal_data = pd.read_csv(data_path)
unique_col = [i for i in temporal_data.keys() if i.__contains__("Subcategory")] + ["video_name"]
unique_name = temporal_data[unique_col].apply("-".join, axis=1)
temporal_data["unique_name"] = unique_name

data1 = pd.DataFrame()
for v in np.unique(data['unique_name']):
    video = temporal_data[temporal_data["unique_name"]==v]
    video = video.sort_values('frame')
    video['Subcategory-03'] = 'Raw'

    # Estimated gaussian function
    gauss_params = data[data["unique_name"]==v]["dist_param"]
    a, x0, sigma = np.squeeze(gauss_params)
    frames = video['frame']
    gaussian_estimates = gaussian_function(frames, a, x0, sigma)
    video2 = video.copy()
    video2['Subcategory-03'] = 'Gaussian'
    video2['mitosis'] = gaussian_estimates
    video = pd.concat([video, video2]).reset_index(drop=True)
    data1 = pd.concat([data1, video]).reset_index(drop=True)

v = '2022-08-03-night-WL UV - high density-Synchro-CHO_live_night_live-01-Scene-08-P8-A01'
video = temporal_data[temporal_data["unique_name"]==v]
yval = np.squeeze(video["mitosis"])
xval = np.squeeze(video["frame"])
numpyDiff = np.diff(yval)/np.diff(xval)

plt.plot(video["frame"], video["mitosis"], '.')
plt.plot(video["frame"][1:], numpyDiff, '-')
plt.plot(video["frame"][1:], np.diff(yval), '--')

sum(xval * yval) / sum(xval)