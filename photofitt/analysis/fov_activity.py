import numpy as np
from tifffile import imread, imsave
import pandas as pd
from photofitt.utils.normalisation import normalise_phc_timelapse, normalizePercentile
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

def normalise_activity(activity, diff, save_steps=False, save_path=None):

    # Estimation of the total area covered by the cells in the video.
    sum_projection = np.sum(diff, axis=0)
    sum_projection = normalizePercentile(sum_projection, pmin=30, pmax=100, clip=True)
    total_area = sum_projection.shape[0] * sum_projection.shape[1]

    if save_steps:
        imsave(save_path, sum_projection)
    sum_projection = np.sum(sum_projection > 0.001)

    # Normalize the metrics acording to the number of cells.
    norm_activity = [activity[t]/(sum_projection/total_area) for t in range(len(activity))]
    return norm_activity


def extract_activity(path, activity_info=None, column_data=[], frame_rate=4, enhance_contrast=False,
                   method="intensity", save_steps=False, output_path='', condition=None, normalize=True):
    folders = os.listdir(path)
    folders.sort
    print(folders)
    for f in folders:
        if f[0] != '.':
            if not f.__contains__('.'):

                activity_info = extract_activity(os.path.join(path, f), activity_info=activity_info,
                                             column_data=column_data + [f], frame_rate=frame_rate,
                                             enhance_contrast=enhance_contrast, method=method,
                                             save_steps=save_steps, output_path=os.path.join(output_path, f),
                                             condition=condition, normalize=normalize)
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
                        activity, diff = time_crosscorrelation_variability(new_im)
                    elif method == "intensity":
                        activity, diff = time_intensity_variability(new_im)
                    elif method == 'piv':
                        activity, diff = piv_time_variability(new_im)
                    if save_steps:
                        print()
                        os.makedirs(output_path, exist_ok=True)
                        imsave(os.path.join(output_path, "normalised_" + f), new_im)
                        imsave(os.path.join(output_path, "diff_" + f), diff)

                    if normalize:
                        norm_activity = normalise_activity(activity, diff, save_steps=save_steps, save_path=os.path.join(output_path, "normalised_projection_" + f))
                        data = np.zeros((len(activity), 3))
                        data[:, 2] = norm_activity
                    else:
                        data = np.zeros((len(activity), 2))
                    data[:, 0] = frame_rate * np.arange(len(activity))
                    data[:, 1] = activity

                    # convert counts together with the column information into a dataframe.
                    if normalize:
                        aux = pd.DataFrame(data, columns=['frame', 'activity', 'normalised_activity'])
                    else:
                        aux = pd.DataFrame(data, columns=['frame', 'activity'])

                    for i in range(len(column_data)):
                        aux["Subcategory-{:02d}".format(i)] = column_data[i]

                    aux['video_name'] = f.split('.tif')[0]
                    # Concatenate pandas data frame to the previous one
                    if activity_info is None:
                        activity_info = aux
                    else:
                        activity_info = pd.concat([activity_info, aux]).reset_index(drop=True)

                    os.makedirs(output_path.split("stardist")[0], exist_ok=True)
                    activity_info.to_csv(os.path.join(output_path.split("stardist")[0],
                                                      "data_activity_{0}_{1}_temp.csv".format(method, condition)))
    return activity_info


def cummulative_activity(activity_metrics, y_var, use_starting_point=None, starting_point=0, data_peaks=None):
    """

    :param use_starting_point: One between None, "event peak", or "fixed". None by default
    :param starting_point:  The time-point from which the cummulation will be done.
                            If set to 0 will be the same effect as use_starting_point=None
    :param data_peaks: pandas dataframe in which the peak of mitotic events are stored.
    :return: activity_dataframe, activity_metrics:
    """

    # Initialise the parameters
    assert isinstance(use_starting_point,
                      str), 'cummulative_activity() parameter use_starting_point={} not of <class "str">'.format(
        use_starting_point)
    assert starting_point >= 0, f"starting_point >= 0 expected, got: {starting_point}"

    activity_metrics[f"Cummulative {y_var}"] = 0
    activity = []

    # Cover each folder and each video to process each independent acquisition
    for f in np.unique(activity_metrics["Subcategory-00"]):
        # Create a new data set to filter the experimental replica.
        activity_metrics_f = activity_metrics[activity_metrics["Subcategory-00"] == f]

        # Process each video acquired on the day f
        for v in np.unique(activity_metrics_f["video_name"]):
            activity_metrics_fv = activity_metrics_f[activity_metrics_f["video_name"] == v]
            if use_starting_point != None:
                if use_starting_point == "event peak":
                    # Recover the time point at which the peak is achieved
                    data_cf = data_peaks[data_peaks["Subcategory-00"] == f].reset_index(drop=True)
                    data_cfv = data_cf[data_cf["video_name"] == v].reset_index(drop=True)
                    starting_point = data_cfv["Peak time point (min)"].iloc[0]

                # Compute the cummulative cell growth only after the mitosis
                after_aux = activity_metrics_fv[activity_metrics_fv["frame"] > starting_point]
                index = after_aux.index.to_list()
                cummulative_activity = after_aux[y_var].cumsum()
                activity_metrics.loc[index, [f"Cummulative {y_var}"]] = cummulative_activity
                # Average the cell growth
                mean_activity = np.mean(after_aux[y_var])
            else:
                index = activity_metrics_fv.index.to_list()
                cummulative_activity = activity_metrics[y_var].cumsum()
                activity_metrics.loc[index, [f"Cummulative {y_var}"]] = cummulative_activity
                # Average the cell growth
                mean_activity = np.mean(activity_metrics[y_var])
            # Estimate the slope
            cummulative_activity = np.array(cummulative_activity)
            frame = np.array(activity_metrics.loc[index, ["frame"]])
            slope = (cummulative_activity[1:] - cummulative_activity[:-1]) / (frame[1:] - frame[:-1])
            slope = np.mean(slope)
            activity.append([mean_activity, slope, v, f, activity_metrics_fv["Subcategory-01"].iloc[0],
                           activity_metrics_fv["Subcategory-02"].iloc[0]])

    activity_dataframe = pd.DataFrame(activity, columns=['Mean activity', 'activity slope', "video_name",
                                                     'Subcategory-00', 'Subcategory-01', "Subcategory-02"])
    return activity_dataframe, activity_metrics