import pandas as pd
import numpy as np
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
SCRIPT_DIR = '/Users/esti/Documents/PROYECTOS/PHX/mitosis-mediated-phototoxic'
sys.path.append(SCRIPT_DIR)
import matplotlib.pyplot as plt
from tifffile import imread, imwrite
from utils.normalisation import normalise_phc_timelapse
from utils.fov_motility import time_intensity_variability, time_crosscorrelation_variability
from skimage.exposure import equalize_adapthist
from scipy.ndimage import gaussian_filter

## Include the following lines to access the code in Python Console
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
SCRIPT_DIR = '/Users/esti/Documents/PROYECTOS/PHX/mitosis-mediated-phototoxic'
sys.path.append(SCRIPT_DIR)
from utils.fov_motility import dynamics_peaks
from utils.display import plot_motility_peak_measurements, plot_motility
output_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/CHO/results/scaled_1.5709_results/stardist_prob03/"
folder = "dynamics_clahe"
condition = ["UV_clean", "475_clean", "630", "568"]
c = "UV_clean"

dynamics_metrics = pd.read_csv(
        os.path.join(output_path, folder, "data_dynamics_intensity_{}.csv".format(c)))


video_new = dynamics_metrics[dynamics_metrics["video_name"]=="CHO_night_live-01-Scene-10-P8-A01"].reset_index(drop=True)

dynamics_metrics_old = pd.read_csv("/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/CHO/results/scaled_1.5709_results/stardist_prob03/dynamics_clahe/data_dynamics_intensity_all_old.csv")


video_new_old = dynamics_metrics_old[dynamics_metrics_old["video_name"]=="CHO_night_live-01-Scene-10-P8-A01"].reset_index(drop=True)


# path_video = "/Volumes/TOSHIBA EXT/HENRIQUES-LAB/PROJECTS/PHOTOTOXICITY/mitosis_mediated_data_itqb_3/CHO/inputs/scaled_1.5709_results/2022-08-09/WL UV - high density/UV01sec/CHO_live-01-Scene-20-P9-A02.tif"
path_video = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/CHO/inputs/scaled_1.5709_results/2022-08-10/WL UV - high density/Synchro/CHO_night_live-01-Scene-10-P8-A01.tif"
plt.plot(video_new["frame"], video_new["time_variance"])
plt.plot(video_new_old["frame"], video_new_old["time_variance"])

im = imread(path_video)
new_im = normalise_phc_timelapse(im, keep_mean=False)
# new_im = np.copy(im)
imwrite("/Users/esti/Downloads/raw.tif", im)
imwrite("/Users/esti/Downloads/normalised.tif", new_im)

enhance_contrast=True
low = np.min(new_im)
upper = np.max(new_im)
new_im = (1 / (upper - low)) * (new_im - low)
new_im = equalize_adapthist(new_im, kernel_size=50, clip_limit=0.05, nbins=256) #25
imwrite("/Users/esti/Downloads/equalised.tif", new_im)

new_im = np.array([gaussian_filter(new_im[t], 1) for t in range(new_im.shape[0])])#2
imwrite("/Users/esti/Downloads/gaussian_1.tif", new_im)


dynamics_val, diff = time_intensity_variability(new_im)
# dynamics_val, diff = time_crosscorrelation_variability(im)
plt.plot(video_new["frame"], video_new["time_variance"])
plt.plot(video_new_old["frame"], video_new_old["time_variance"])
plt.plot(video_new_old["frame"][1:], dynamics_val)
plt.show()
imwrite("/Users/esti/Downloads/diff.tif", diff)