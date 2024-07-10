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


def normalise_activity(diff, save_steps=False, save_path=None):
    #TODO: correct normalisation for the entire video. Otherwise the treatment for the activity will be t dependent.

    # Raw activity:
    activity_t = [np.sum(diff[t]) for t in range(diff.shape[0])]
    # Number of pixels with activity at each time point in the FOV:
    p_t = [np.sum(normalizePercentile(diff[t], pmin=30, pmax=100, clip=True) > 0.001) for t in range(diff.shape[0])]
    # Normalize the metrics according to the pixels in which activity has been recorded.
    norm_activity_t = [activity_t[t] / p_t[t] for t in range(len(activity_t))]
    # Sum projection until time point T (raw cumulative activity)
    ca = [np.sum(diff[:t + 1], axis=0) for t in range(diff.shape[0])]
    # Binarisation of sum projection until T (total area covered by active cells until T)
    # This measure if the cells are spreading should be increasing
    cp = [np.sum(normalizePercentile(ca[t], pmin=30, pmax=100, clip=True) > 0.001) for t in range(len(ca))]
    # Cumulative activity per total cell area until T
    norm_cumulative = [np.sum(ca[t]) / cp[t] for t in range(len(ca))]

    # Estimation of the total area covered by the cells by the end of the video.
    sum_projection = normalizePercentile(ca[-1], pmin=30, pmax=100, clip=True)
    if save_steps:
        imsave(save_path, sum_projection)
    ## Number of pixels belonging to cell area at some point in the video.
    sum_projection = np.sum(sum_projection > 0.001)

    # Normalize the cumulative activity with the final total area covered by cells.
    norm_cumulative_final = [np.sum(ca[t]) / sum_projection for t in range(len(ca))]
    return activity_t, p_t, norm_activity_t, cp, norm_cumulative, norm_cumulative_final


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
                        activity_t, p_t, norm_activity_t, cp, norm_cumulative, norm_cumulative_final = \
                            normalise_activity(diff, save_steps=save_steps,
                                               save_path=os.path.join(output_path,
                                               "normalised_projection_" + f))

                        data = np.zeros((len(activity), 8))
                        data[:, 2] = activity_t
                        data[:, 3] = p_t
                        data[:, 4] = norm_activity_t
                        data[:, 5] = cp
                        data[:, 6] = norm_cumulative
                        data[:, 7] = norm_cumulative_final
                    else:
                        data = np.zeros((len(activity), 2))
                    data[:, 0] = frame_rate * np.arange(len(activity))
                    data[:, 1] = activity

                    # convert counts together with the column information into a dataframe.
                    if normalize:
                        aux = pd.DataFrame(data, columns=['frame', 'mean activity', 'SUM activity',
                                                          'area active cells', 'masked mean activity',
                                                          'total area active cells', 'masked cumulative activity',
                                                          'TOTAL masked cumulative activity'])
                    else:
                        aux = pd.DataFrame(data, columns=['frame', 'mean activity'])

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


def cumulative_activity(activity_metrics, y_var, use_starting_point=None, starting_point=0, data_peaks=None):
    """

    :param activity_metrics:
    :param y_var:
    :param use_starting_point: One between None, "event peak", or "fixed". None by default
    :param starting_point:  The time-point from which the cummulation will be done.
                            If set to 0 will be the same effect as use_starting_point=None
    :param data_peaks: pandas dataframe in which the peak of mitotic events are stored.
    :return: activity_dataframe, activity_metrics:
    """

    # Initialise the parameters
    assert isinstance(use_starting_point,
                      str), 'cumulative_activity() parameter use_starting_point={} not of <class "str">'.format(
        use_starting_point)
    assert starting_point >= 0, f"starting_point >= 0 expected, got: {starting_point}"

    activity_metrics[f"Cumulative {y_var}"] = 0
    activity = []

    # Cover each folder and each video to process each independent acquisition
    for f in np.unique(activity_metrics["Subcategory-00"]):
        # Create a new data set to filter the experimental replica.
        activity_metrics_f = activity_metrics[activity_metrics["Subcategory-00"] == f]

        # Process each video acquired on the day f
        for v in np.unique(activity_metrics_f["video_name"]):
            activity_metrics_fv = activity_metrics_f[activity_metrics_f["video_name"] == v]
            if use_starting_point is not None:
                if use_starting_point == "event peak":
                    # Recover the time point at which the peak is achieved
                    data_cf = data_peaks[data_peaks["Subcategory-00"] == f].reset_index(drop=True)
                    data_cfv = data_cf[data_cf["video_name"] == v].reset_index(drop=True)
                    # Recover the time point at which the peak is achieved
                    starting_point = data_cfv["Peak time point (min)"].iloc[0]

                # Compute the cumulative cell growth only after the mitosis
                after_aux = activity_metrics_fv[activity_metrics_fv["frame"] > starting_point]
                index = after_aux.index.to_list()
                cumulative_data = after_aux[y_var].cumsum()
                activity_metrics.loc[index, [f"Cumulative {y_var}"]] = cumulative_data
                # Average the cell growth
                mean_activity = np.mean(after_aux[y_var])
            else:
                index = activity_metrics_fv.index.to_list()
                cumulative_data = activity_metrics[y_var].cumsum()
                activity_metrics.loc[index, [f"Cumulative {y_var}"]] = cumulative_data
                # Average the cell growth
                mean_activity = np.mean(activity_metrics[y_var])
            # Estimate the slope
            cumulative_data = np.array(cumulative_data)
            frame = np.array(activity_metrics.loc[index, ["frame"]])
            slope = (cumulative_data[1:] - cumulative_data[:-1]) / (frame[1:] - frame[:-1])
            slope = np.mean(slope)
            activity.append([mean_activity, slope, v, f, activity_metrics_fv["Subcategory-01"].iloc[0],
                             activity_metrics_fv["Subcategory-02"].iloc[0]])

    activity_dataframe = pd.DataFrame(activity, columns=['Mean activity', 'activity slope', "video_name",
                                                         'Subcategory-00', 'Subcategory-01', "Subcategory-02"])
    return activity_dataframe, activity_metrics


def estimate_proportional_deviations(data,
                          variable,
                          reference_category='0 J/cm2',
                          reference_variable="Light dose cat",
                          unique_id_var = "video_name",
                          grouping_variable=None, add_columns=None):

    if grouping_variable is None:
        # Create a fake variable
        data["aux_var"] = "aux_var"
        grouping_variable_aux = "aux_var"
    else:
        grouping_variable_aux = grouping_variable


    GROUPS = np.unique(data[grouping_variable_aux])
    new_data = None
    for g in GROUPS:
        data_g = data.loc[lambda data: data[grouping_variable] == g]
        ## Mean values per condition regardless of the FOV or unique measurements
        m = data_g.groupby(reference_variable)[variable].mean()
        s_mean = m[reference_category] # recover the average of the control group
        m = m.reset_index()
        m = m.rename(columns={variable: f"{grouping_variable_aux} mean {variable}"})
        ## Mean values for each FOV and each condition
        m_unique = data_g.groupby([reference_variable, unique_id_var])[variable].mean()
        m_unique = m_unique.reset_index()
        m_unique = m_unique.rename(columns={variable: f"mean {variable}"})
        # Obtain the final image
        means_data = m_unique.merge(m)
        means_data[grouping_variable_aux] = g

        means_data[f"difference_per_{unique_id_var}"] = s_mean-means_data[f"mean {variable}"]
        means_data[f"difference_per_{grouping_variable_aux}"] = s_mean - means_data[f"{grouping_variable_aux} mean {variable}"]
        means_data[f"proportional_difference_per_{unique_id_var}"] = 100 * means_data[f"difference_per_{unique_id_var}"] / s_mean
        means_data[f"proportional_difference_per_{grouping_variable_aux}"] = 100 * means_data[f"difference_per_{grouping_variable_aux}"] / s_mean

        if add_columns is not None:
            for i in add_columns:
                means_data[i] = data_g[i].iloc[0]
        if new_data is None:
            new_data = means_data
        else:
            new_data = pd.concat([new_data, means_data]).reset_index(drop=True)

    # Remove the fake column
    if grouping_variable is None:
        new_data.drop([grouping_variable_aux, f"proportional_difference_per_{grouping_variable_aux}",
                      f"difference_per_{grouping_variable_aux}", f"{grouping_variable_aux} mean {variable}"], axis=1)
    return new_data
