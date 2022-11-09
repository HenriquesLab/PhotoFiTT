from tifffile import imread, imsave
import matplotlib.pyplot as plt
import os
import sys
## Include the following lines to access the code in Python Console
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
SCRIPT_DIR = '/Users/esti/Documents/PROYECTOS/PHX/mitosis-mediated-phototoxic'
sys.path.append(SCRIPT_DIR)
from utils.fov_motility import normalise_phc_timelapse, time_intensity_variability


# Synchro
im_control_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/inputs/scaled_1.5709_results/2022-09-08-night/WL UV - high density/Synchro/CHO_live_UV_live-01-Scene-02-P3-A01.tif"
# High UV radiation
im_UV_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/inputs/scaled_1.5709_results/2022-09-08-night/WL UV - high density/UV20sec/CHO_live_UV_live-01-Scene-58-P4-B03.tif"

im_control = imread(im_control_path)
new_im = normalise_phc_timelapse(im_control)
im_control_val, diff = time_intensity_variability(new_im)
# backRemoval, background = background_subtr_medFilt(new_im)
imsave("/Users/esti/Downloads/normalised_raw_synchro.tif", new_im)
imsave("/Users/esti/Downloads/normalised_raw_synchro_diff.tif", diff)
# imsave("/Users/esti/Downloads/normalised_raw_synchro_background.tif", background)
# imsave("/Users/esti/Downloads/normalised_raw_synchro_background_removal.tif", backRemoval)

im_UV = imread(im_UV_path)
new_im = normalise_phc_timelapse(im_UV)
im_UV_val, diff = time_intensity_variability(new_im)
# backRemoval, background = background_subtr_medFilt(new_im)
imsave("/Users/esti/Downloads/normalised_raw_UV.tif", new_im)
imsave("/Users/esti/Downloads/normalised_raw_UV_diff.tif", diff)
# imsave("/Users/esti/Downloads/normalised_raw_UV_background.tif", background)
# imsave("/Users/esti/Downloads/normalised_raw_UV_background_removal.tif", backRemoval)

plt.figure()
plt.plot(im_control_val, 'r-')
plt.plot(im_UV_val, 'b-')
plt.legend(["Control", "UV radiation"])
plt.show()