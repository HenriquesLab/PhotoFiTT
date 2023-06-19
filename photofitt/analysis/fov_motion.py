import numpy as np
from tifffile import imread, imsave
import pandas as pd
from photofitt.utils import normalise_phc_timelapse
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
    xc_time = [np.squeeze(xc.calculate_ccm(im[i], im[i + 1], normalize=False)) for i in range(im.shape[0] - 1)]
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


def extract_motion(path, motion_info=None, column_data=[], frame_rate=4, enhance_contrast=False,
                   method="intensity", save_steps=False, output_path='', condition=None):
    folders = os.listdir(path)
    folders.sort
    print(folders)
    for f in folders:
        if f[0] != '.':
            if not f.__contains__('.'):

                motion_info = extract_motion(os.path.join(path, f), motion_info=motion_info,
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
                        motion_val, diff = time_crosscorrelation_variability(new_im)
                    elif method == "intensity":
                        motion_val, diff = time_intensity_variability(new_im)
                    elif method == 'piv':
                        motion_val, diff = piv_time_variability(new_im)
                    if save_steps:
                        print()
                        os.makedirs(output_path, exist_ok=True)
                        imsave(os.path.join(output_path, "normalised_" + f), new_im)
                        imsave(os.path.join(output_path, "diff_" + f), diff)

                    data = np.zeros((len(motion_val), 2))
                    data[:, 0] = frame_rate * np.arange(len(motion_val))
                    data[:, 1] = motion_val
                    # convert counts together with the column information into a dataframe.
                    aux = pd.DataFrame(data, columns=['frame', 'time_variance'])

                    for i in range(len(column_data)):
                        aux["Subcategory-{:02d}".format(i)] = column_data[i]

                    aux['video_name'] = f.split('.tif')[0]
                    # Concatenate pandas data frame to the previous one
                    if motion_info is None:
                        motion_info = aux
                    else:
                        motion_info = pd.concat([motion_info, aux]).reset_index(drop=True)
                    os.makedirs(output_path.split("stardist")[0], exist_ok=True)
                    motion_info.to_csv(
                        os.path.join(output_path.split("stardist")[0],
                                     "data_motion_{0}_{1}_temp.csv".format(method, condition)))

    return motion_info


def cummulative_motion(motion_metrics, use_starting_point=None, starting_point=0, data_peaks=None):
    """

    :param use_starting_point: One between None, "event peak", or "fixed". None by default
    :param starting_point:  The time-point from which the cummulation will be done.
                            If set to 0 will be the same effect as use_starting_point=None
    :param data_peaks: pandas dataframe in which the peak of mitotic events are stored.
    :return: motion_dataframe, motion_metrics:
    """

    # Initialise the parameters
    assert isinstance(use_starting_point,
                      str), 'cummulative_motion() parameter use_starting_point={} not of <class "str">'.format(
        use_starting_point)
    assert starting_point >= 0, f"starting_point >= 0 expected, got: {starting_point}"

    motion_metrics["Cummulative cell motion"] = 0
    motion = []

    # Cover each folder and each video to process each independent acquisition
    for f in np.unique(motion_metrics["Subcategory-00"]):
        # Create a new data set to filter the experimental replica.
        motion_metrics_f = motion_metrics[motion_metrics["Subcategory-00"] == f]

        # Process each video acquired on the day f
        for v in np.unique(motion_metrics_f["video_name"]):
            motion_metrics_fv = motion_metrics_f[motion_metrics_f["video_name"] == v]
            if use_starting_point is not None:
                if use_starting_point == "event peak":
                    # Recover the time point at which the peak is achieved
                    data_cf = data_peaks[data_peaks["Subcategory-00"] == f].reset_index(drop=True)
                    data_cfv = data_cf[data_cf["video_name"] == v].reset_index(drop=True)
                    starting_point = data_cfv["Peak time point (min)"].iloc[0]

                # Compute the cummulative cell growth only after the mitosis
                after_aux = motion_metrics_fv[motion_metrics_fv["frame"] > starting_point]
                index = after_aux.index.to_list()
                cummulative_motion = after_aux["Cell motion"].cumsum()
                motion_metrics.loc[index, ["Cummulative cell motion"]] = cummulative_motion
                # Average the cell growth
                mean_motion = np.mean(after_aux["Cell motion"])
            else:
                index = motion_metrics_fv.index.to_list()
                cummulative_motion = motion_metrics["Cell motion"].cumsum()
                motion_metrics.loc[index, ["Cummulative cell motion"]] = cummulative_motion
                # Average the cell growth
                mean_motion = np.mean(motion_metrics["Cell motion"])
            # Estimate the slope
            cummulative_motion = np.array(cummulative_motion)
            frame = np.array(motion_metrics.loc[index, ["frame"]])
            slope = (cummulative_motion[1:] - cummulative_motion[:-1]) / (frame[1:] - frame[:-1])
            slope = np.mean(slope)
            motion.append([mean_motion, slope, v, f, motion_metrics_fv["Subcategory-01"].iloc[0],
                           motion_metrics_fv["Subcategory-02"].iloc[0]])

    motion_dataframe = pd.DataFrame(motion, columns=['Mean motion', 'Motion slope', "video_name",
                                                     'Subcategory-00', 'Subcategory-01', "Subcategory-02"])
    return motion_dataframe, motion_metrics