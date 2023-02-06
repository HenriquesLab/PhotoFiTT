[import pandas as pd
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
from scipy.ndimage import gaussian_filter]

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




import numpy as np
from scipy.optimize import minimize
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



def gaussian_function(x, sigma, mu, a):
    """
    Non normalised gaussian density (area under the curve >1)
    :param x: input value
    :param sigma: standard deviation
    :param mu: mean value
    :param a: scaling factor and the maximum value expected for the non-normalised Gaussian density
    :return: the probability density value of a Gaussian with mean x0, and standard deviation sigma.
    """
    return a * np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))

def gaussian_mixture_function(x, sigma1, sigma2, mu1, mu2, a1, a2, p):
    """
    Non normalised gaussian density (area under the curve >1)
    :param x: input value
    :param sigma: standard deviation
    :param mu: mean value
    :param a: scaling factor and the maximum value expected for the non-normalised Gaussian density
    :return: the probability density value of a Gaussian with mean x0, and standard deviation sigma.
    """
    return p*(gaussian_function(x, sigma1, mu1, a1)) + (1-p)*(gaussian_function(x, sigma2, mu2, a2))
class lsq_minimiser():
    def __init__(self, x, y, mean=None, sigma=None, amplitude=None, prob_dist="gaussian"):
        # Store the parameters in the class
        self.x = np.squeeze(x)
        self.y = np.squeeze(y)
        self.mean = mean
        self.sigma = sigma
        self.amplitude = amplitude
        self.prob_dist = prob_dist
    def __least_squares__(self, params):
        # Define the function to minimise
        if self.prob_dist == "gaussian":
            # split input params
            if len(params)==3:
                sigma, mean, a = params
                return sum((self.y - gaussian_function(self.x, sigma, mean, a)) ** 2)
            elif len(params)==2:
                mean, a = params
                return sum((self.y - gaussian_function(self.x, self.sigma, mean, a)) ** 2)
            else:
                a = params
                return sum((self.y - gaussian_function(self.x, self.sigma, self.mean, a)) ** 2)

        elif self.prob_dist == "poisson":
            mean = params
            return sum((self.y - poisson_function(self.x, mean)) ** 2)

        elif self.prob_dist == "poisson_jacobian":
            mean = params
            return sum((self.y - tfm_poisson_pdf(self.x, mean)) ** 2)
    def run_minimisation(self, options={}, **kwargs):
        return minimize(self.__least_squares__, self.x0, options=options, **kwargs)

impath = "/Users/esti/Downloads/im.tif"
stack = imread(impath)
frame_a = stack[40]
frame_b = stack[41]
winsize = 30 # pixels, interrogation window size in frame A
searchsize = 35  # pixels, search in image B
overlap = 10 # pixels, 50% overlap
dt = 0.5# sec, time interval between pulses
disp = []
for t in range(len(stack)-1):
    frame_a = stack[t]
    frame_b = stack[t+1]
    u0, v0, sig2noise = pyprocess.extended_search_area_piv(frame_a.astype(np.int32),
                                                           frame_b.astype(np.int32),
                                                           window_size=winsize,
                                                           overlap=overlap,
                                                           dt=dt,
                                                           search_area_size=searchsize,
                                                           sig2noise_method='peak2peak')

    x, y = pyprocess.get_coordinates(image_size=frame_a.shape,
                                     search_area_size=searchsize,
                                     overlap=overlap)
    flags = validation.sig2noise_val(sig2noise,
                                     threshold=1.05)
    u0, v0 = filters.replace_outliers(u0, v0,
                                      flags,
                                      method='localmean',
                                      max_iter=3,
                                      kernel_size=3)
    disp.append(np.multiply(u0, u0) + np.multiply(v0, v0))
disp = np.array(disp)
imwrite("/Users/esti/Downloads/disp.tif", disp.astype(np.float32))



# convert x,y to mm
# convert u,v to mm/sec
x, y, u3, v3 = scaling.uniform(x, y, u2, v2,
                               scaling_factor = 1 ) # 96.52 microns/pixel
# 0,0 shall be bottom left, positive rotation rate is counterclockwise
x, y, u3, v3 = tools.transform_coordinates(x, y, u3, v3)
tools.save('/Users/esti/Downloads/exp1_001.txt', x, y, u3, v3, flags)
fig, ax = plt.subplots(figsize=(8,8))
tools.display_vector_field('/Users/esti/Downloads/exp1_001.txt',
                           ax=ax, scaling_factor=0.5,
                           scale=100, # scale defines here the arrow length
                           width=0.0035, # width is the thickness of the arrow
                           on_img=False) # overlay on the image)
disp =np.multiply(u0,u0) + np.multiply(v0, v0)
plt.imshow(disp)
plt.imshow(u0)
