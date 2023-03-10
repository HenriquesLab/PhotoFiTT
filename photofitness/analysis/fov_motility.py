import numpy as np
from tifffile import imread, imsave
import pandas as pd
from photofitness.normalisation import normalise_phc_timelapse
import os
from skimage.exposure import equalize_adapthist
from scipy.ndimage import gaussian_filter

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

def piv_time_variability(im, winsize=30, searchsize=35, overlap=10, dt=0.01, threshold=1.05):
    """

    :param im:
    :param winsize: pixels, interrogation window size in frame A
    :param searchsize: pixels, search in image B
    :param overlap: pixels, 50% overlap
    :param dt: sec, time interval between pulses
    :param threshold:
    :return:
    """
    from openpiv import pyprocess, validation, filters
    piv_t = []
    for t in range(len(im) - 1):
        frame_a = im[t]
        frame_b = im[t + 1]
        u0, v0, sig2noise = pyprocess.extended_search_area_piv(frame_a.astype(np.float32),
                                                               frame_b.astype(np.float32),
                                                               window_size=winsize,
                                                               overlap=overlap,
                                                               dt=dt,
                                                               search_area_size=searchsize,
                                                               sig2noise_method='peak2peak')
        flags = validation.sig2noise_val(sig2noise,
                                         threshold=threshold)
        u0, v0 = filters.replace_outliers(u0, v0,
                                          flags,
                                          method='localmean',
                                          max_iter=3,
                                          kernel_size=3)
        piv_t.append(np.multiply(u0, u0) + np.multiply(v0, v0))
    piv_t = np.array(piv_t)
    mean_piv_t = [np.mean(piv_t[t]) for t in range(len(piv_t))]
    return mean_piv_t, piv_t

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
                    new_im = normalise_phc_timelapse(im, keep_mean=False)

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
                    elif method =='piv':
                        dynamics_val, diff = piv_time_variability(new_im)
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
