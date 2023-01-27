import numpy as np
from tifffile import imread, imsave
import pandas as pd
from utils.normalisation import normalise_phc_timelapse
import os
import sys
SCRIPT_DIR = "/Users/esti/Documents/PROYECTOS/PHX/NanoPyx/src"
sys.path.append(SCRIPT_DIR)

from skimage.exposure import equalize_adapthist
from scipy.ndimage import gaussian_filter
from numba import njit

@njit()
def time_intensity_variability(im):
    diff = im[:-1] - im[1:]
    diff = np.multiply(diff, diff)
    mean_variability = [np.mean(diff[t]) for t in range(diff.shape[0])]
    return mean_variability, diff

def time_crosscorrelation_variability(im):
    from enanoscopy.methods.image.transform.cross_correlation_map import CrossCorrelationMap
    xc = CrossCorrelationMap()
    xc_time = [np.squeeze(xc.calculate_ccm(im[i], im[i+1], normalize=False)) for i in range(im.shape[0]-1)]
    # xcorr is in the Fourier Space.
    # The value can be positive or negative but we only care about strong/weak correlations.
    # If there are many random movements,
    # the normalised maximum value should be smaller than the maximum value of a static case
    xc_mean = [np.max(np.abs(x)) for x in xc_time]
    xc_time = np.array(xc_time)
    return xc_mean, xc_time

def extract_dynamics_metrics(path, dynamics_info=None, column_data=[], frame_rate=4, enhance_contrast=False,
                             method="intensity", save_steps=False, output_path='', condition=None):
    folders = os.listdir(path)
    folders.sort
    print(folders)
    for f in folders:
        if f[0] != '.':
            if not f.__contains__('.'):

                dynamics_info = extract_dynamics_metrics(os.path.join(path, f), dynamics_info=dynamics_info,
                                                         column_data=column_data + [f], frame_rate=frame_rate,
                                                         enhance_contrast=enhance_contrast, method=method,
                                                         save_steps=save_steps, output_path=os.path.join(output_path, f),
                                                         condition=condition)
            elif f.__contains__('.tif'):
                if condition is not None:
                    process_file = [column_data[i].__contains__(condition) for i in range(len(column_data))]
                    process_file = sum(process_file)
                else:
                    process_file = 1
                if process_file > 0:
                    print(f)
                    im = imread(os.path.join(path, f))
                    new_im = normalise_phc_timelapse(im)

                    if enhance_contrast:
                        low = np.min(new_im)
                        upper = np.max(new_im)
                        new_im = (1 / (upper - low)) * (new_im - low)
                        new_im = equalize_adapthist(new_im, kernel_size=25, clip_limit=0.01, nbins=256)
                        # Smoothing goes after to ensure that the noise from the background has disappear,
                        # rather than enhancing it with CLAHE afterwards
                        new_im = np.array([gaussian_filter(new_im[t], 1) for t in range(new_im.shape[0])])
                    if method == "cross-correlation":
                        dynamics_val, diff = time_crosscorrelation_variability(new_im)
                    elif method == "intensity":
                        dynamics_val, diff = time_intensity_variability(new_im)
                    if save_steps:
                        print()
                        os.makedirs(output_path, exist_ok=True)
                        imsave(os.path.join(output_path, "normalised_" + f), new_im)
                        imsave(os.path.join(output_path, "diff_" + f), diff)

                    data = np.zeros((len(dynamics_val), 2))
                    data[:, 0] = frame_rate * np.arange(len(dynamics_val))
                    data[:, 1] = dynamics_val
                    # convert counts together with the column information into a dataframe.
                    aux = pd.DataFrame(data, columns=['frame', 'time_variance'])

                    for i in range(len(column_data)):
                        aux["Subcategory-{:02d}".format(i)] = column_data[i]

                    aux['video_name'] = f.split('.tif')[0]
                    # Concatenate pandas data frame to the previous one
                    if dynamics_info is None:
                        dynamics_info = aux
                    else:
                        dynamics_info = pd.concat([dynamics_info, aux]).reset_index(drop=True)
                    os.makedirs(output_path.split("stardist")[0], exist_ok=True)
                    dynamics_info.to_csv(
                        os.path.join(output_path.split("stardist")[0], "data_dynamics_{0}_{1}_temp.csv".format(method, condition)))

    return dynamics_info


def dynamics_peaks(dynamics_metrics, frame_rate=4, alpha_init=25, alpha_end=100, beta_init=250, beta_end=300):
    """
    This is to calculate the motility peak and the ratio between
    the first part of the video and the second one.
    This code estimates the peak of motility in the control group
    so we can compute the delay between treated conditions

    :param dynamics_metrics:
    :param frame_rate:
    :param alpha_init: time in min
    :param alpha_end: time in min
    :param beta_init: time in min
    :param beta_end: time in min
    :return:
    """
    aux = None
    for v in np.unique(dynamics_metrics["video_name"]):
        video_data = dynamics_metrics[dynamics_metrics["video_name"] == v].reset_index(drop=True)
        frame_rate = frame_rate
        init_mit = int(alpha_init / frame_rate)  # 30
        final_mit = int(alpha_end / frame_rate)  # 80
        alpha = np.max(video_data.iloc[init_mit:final_mit]["time_variance"])
        peak_time = video_data.loc[video_data.iloc[init_mit:final_mit]["time_variance"].idxmax(skipna=True), "frame"]
        init_mit = int(beta_init / frame_rate)
        final_mit = int(beta_end / frame_rate)
        beta = np.mean(video_data.iloc[init_mit:]["time_variance"])
        columns = [c for c in video_data.columns if c.__contains__("Subcategory")]
        data = [video_data.iloc[0][c] for c in columns]
        if alpha == 0. and beta == 0.:
            ratio = 0.
        elif beta == 0.:
            print(v)
            ratio = np.infty
        else:
            ratio = alpha / beta
        # ratio = (alpha - beta) / (alpha + beta)
        data += [v, alpha, beta, ratio, peak_time]
        columns += ["video_name", "alpha", "beta", "ratio", "peak_time"]

        if aux is None:
            aux = pd.DataFrame(np.expand_dims(np.array(data), axis=0), columns=columns)
        else:
            aux = pd.concat([aux,
                             pd.DataFrame(np.expand_dims(np.array(data), axis=0), columns=columns)]).reset_index(
                drop=True)
    aux = aux.astype({'ratio': 'float32', 'alpha': 'float32', 'beta': 'float32', 'peak_time': 'float32'})

    aux_1 = None
    for f in np.unique(aux["Subcategory-00"]):
        folder_wise = aux[aux["Subcategory-00"] == f].reset_index(drop=True)
        s_mean = np.mean(folder_wise[folder_wise["Subcategory-02"] == "Synchro"]["peak_time"])
        folder_wise["delay_synchro"] = (folder_wise["peak_time"] - s_mean)
        folder_wise["proportional_delay_synchro"] = (folder_wise["peak_time"] - s_mean) * (100 / s_mean)
        if aux_1 is None:
            aux_1 = folder_wise
        else:
            aux_1 = pd.concat([aux_1, folder_wise]).reset_index(drop=True)
    # synchro_data = aux_1[aux_1["Subcategory-02"]=="Synchro"]
    # index = synchro_data.index.to_list()
    # aux_1 = aux_1.drop(index)
    # synchro_data = aux_1[aux_1["Subcategory-02"]=="Control-sync"]
    # index = synchro_data.index.to_list()
    # aux_1 = aux_1.drop(index)
    # aux_1 = aux_1.reset_index(drop=True)
    return aux_1