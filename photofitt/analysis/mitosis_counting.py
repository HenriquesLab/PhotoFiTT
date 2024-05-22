import os
from tifffile import imread
import numpy as np
import pandas as pd
from photofitt.utils.morphology import roundnessCalculator
from photofitt.utils.utils import cell_density_FOV

def smooth(y, t_win):
    """
    Smooth a curve by convolving it with a time window of size t_win

    :param y: input 1D signal
    :param t_win: size of the convolution kernel
    :return: smooth curve y_smooth
    """
    t = np.ones(t_win) / t_win
    y_smooth = np.convolve(y, t, mode='same')
    return y_smooth

def total_cell_number(folder, type="csv"):
    """

    :param folder:
    :param type: "csv" or "image". It will read the total cell number from a csv file or compute it from the masks
    :return:
    """
    cell_number = None

    for f in os.listdir(folder):
        if not f.startswith("."):
            print(f'Processing folder {f}')
            if type=="csv":
                masks = [files for files in os.listdir(os.path.join(folder, f)) if files.endswith("_Nuclei_centre.csv")]
                for m in masks:
                    info = pd.read_csv(os.path.join(folder, f, m), header=0)
                    n = len(info)
                    video_name = m.split("_Nuclei_centre")[0]
                    aux = pd.DataFrame({
                        'Subcategory-00': f,
                        'video_name': video_name,
                        'cell_counts_stardist': n}, index=[0])
                    if cell_number is None:
                        cell_number = aux
                    else:
                        cell_number = pd.concat([cell_number, aux]).reset_index(drop=True)
            else:
                masks = [files for files in os.listdir(os.path.join(folder, f)) if files.endswith(".tif")]
                for m in masks:
                    im = imread(os.path.join(folder, f, m))
                    n = len(np.unique(im))-1
                    video_name = m.split(".tif")[0]
                    aux = pd.DataFrame({
                        'Subcategory-00': f,
                        'video_name': video_name,
                        'cell_counts_stardist': n}, index=[0])
                    if cell_number is None:
                        cell_number = aux
                    else:
                        cell_number = pd.concat([cell_number, aux]).reset_index(drop=True)

    return cell_number

def add_inferred_nuclei(data, cellnumber_data):
    replicas = np.unique(cellnumber_data["Subcategory-00"])
    data["cell_counts_stardist"] = np.nan
    for r in replicas:
        print(r)
        cell_videos = cellnumber_data.loc[lambda cellnumber_data: cellnumber_data["Subcategory-00"] == r]
        data_replica = data.loc[lambda data: data["Subcategory-00"] == r]

        videos = np.unique(cell_videos["video_name"])
        for v in videos:
            n = cell_videos.loc[lambda cell_videos: cell_videos["video_name"] == v]
            n = n.iloc[0]["cell_counts_stardist"]
            data_video = data_replica.loc[lambda data_replica: data_replica["video_name"] == v]
            index = data_video.index.to_list()
            data.loc[index, ['cell_counts_stardist']] = n
    return data

def extract_info(frame, t, frame_rate, min_roundness, column_data):
    labels = np.unique(frame)
    area = []
    r_axis = []
    r_pro = []
    count = 0
    for l in labels:
        if l > 0:
            cell = (frame == l).astype(np.uint8)
            area.append(np.sum(cell))
            r_axis.append(roundnessCalculator(cell, projected=False))
            r_pro.append(roundnessCalculator(cell, projected=True))
            if roundnessCalculator(cell, projected=False) > min_roundness:
                count += 1
    mitosis = count
    t = frame_rate * t
    # initialize list of lists
    data = [[t, mitosis, area, r_axis, r_pro] + column_data]
    columns = ["Subcategory-{:02d}".format(i) for i in range(len(column_data))]
    aux = pd.DataFrame(data,
                       columns=['frame', 'Number of cells', 'cell_size', "roundness_axis", "roundness_projected"] + columns)
    return aux

def count_mitosis(path, stacks=False, pd_dataframe=None, column_data=[], frame_rate=10, min_roundness=0.85):
    """
    This function parses all the folders contained in the path and will output a pandas data frame with each category
    and subcategory labelled, the fram, time and number of mitosis detected in the image.
    :param path: path containing the folders
    :param pd_dataframe: usually empty as it will create it. Include an old one if you want to concatenate-
    :param column_data: If you want to add an extra category, fill it. Otherwise, leave it with the default []
    :param frame_rate: Frame rate of the videos. 10 by default. Units should be controlled by the user.
    :return:updated pd_dataframe variable with the information.
    """
    folders = os.listdir(path)
    folders.sort
    print(folders)
    for f in folders:
        if f[0] != '.':
            if not f.__contains__('.'):
                pd_dataframe = count_mitosis(os.path.join(path, f), stacks=stacks, pd_dataframe=pd_dataframe,
                                             column_data=column_data + [f], frame_rate=frame_rate,
                                             min_roundness=min_roundness)
            elif f.__contains__('.tif'):
                print(f)
                im = imread(os.path.join(path, f))
                if stacks == False:
                    t = int(f.split('_')[-1].split('.')[0])  # naming 00_0000.tif'
                    aux = extract_info(im, t, frame_rate, min_roundness, column_data)
                else:
                    aux = None
                    for t in range(len(im)):
                        frame = im[t]
                        aux_t = extract_info(frame, t, frame_rate, min_roundness, column_data + [f.split('.tif')[0]])
                        if aux is None:
                            aux = aux_t
                        else:
                            aux = pd.concat([aux, aux_t]).reset_index(drop=True)
                # Concatenate pandas data frame to the previous one
                if pd_dataframe is None:
                    pd_dataframe = aux
                else:
                    pd_dataframe = pd.concat([pd_dataframe, aux]).reset_index(drop=True)

    return pd_dataframe

def count_mitosis_all(path, stacks=True, pd_dataframe=None, column_data=[], frame_rate=4, min_roundness=0.0, t_win=5):
    """
    This function parses all the folders contained in the path and will output a pandas data frame with each category
    and subcategory labelled, the fram, time and number of mitosis detected in the image.
    :param t_win: The size of the window (kernel) that is used to smooth the curves
    :param min_roundness: We can filter out by roundness of the segmented cells
    :param stacks: If the files are given as videos (True) or each time point is an individual file (False)
    :param path: path containing the folders
    :param pd_dataframe: usually empty as it will create it. Include an old one if you want to concatenate-
    :param column_data: If you want to add an extra category, fill it. Otherwise, leave it with the default []
    :param frame_rate: Frame rate of the videos. 10 by default. Units should be controlled by the user.
    :return:updated pd_dataframe variable with the information.
    """
    folders = os.listdir(path)
    folders.sort
    print(folders)
    cells_FOV = cell_density_FOV()
    for f in folders:
        if f[0] != '.':
            if not f.__contains__('.'):
                if f.__contains__("CHO"): # folder for which the frame-rate is defined
                    if f.__contains__("fast"):
                        frame_rate = 2
                    elif f.__contains__("4"):
                        frame_rate = 4
                    else:
                        frame_rate = 10
                print("Frame rate of this folder is {}".format(frame_rate))
                pd_dataframe = count_mitosis_all(os.path.join(path, f), stacks=stacks, pd_dataframe=pd_dataframe,
                                                 column_data=column_data + [f], frame_rate=frame_rate,
                                                 min_roundness=min_roundness, t_win=t_win)
            elif f.__contains__('.tif'):
                print(f)
                im = imread(os.path.join(path, f))

                aux = None
                for t in range(len(im)):
                    frame = im[t]
                    aux_t = extract_info(frame, t, frame_rate, min_roundness, column_data)
                    if aux is None:
                        aux = aux_t
                    else:
                        aux = pd.concat([aux, aux_t]).reset_index(drop=True)
                # Normalise and smooth the values for each video
                M = np.max(aux['Number of cells'])
                aux['Norm. Number of cells'] = aux['Number of cells'] / M
                aux['NormFOV. Number of cells'] = aux['Number of cells'] / cells_FOV

                aux["processing"] = "Raw"
                y = smooth(aux['Number of cells'], t_win)
                y_norm = y / M
                y_norm_FOV = y / cells_FOV
                aux2 = aux.copy()
                aux2['processing'] = 'Averaged-kernel{}'.format(t_win)
                aux2['Number of cells'] = y
                aux2['Norm. Number of cells'] = y_norm
                aux2['NormFOV. Number of cells'] = y_norm_FOV
                aux3 = pd.concat([aux, aux2]).reset_index(drop=True)
                aux3['video_name'] = f.split('.tif')[0]

                # Concatenate pandas data frame to the previous one
                if pd_dataframe is None:
                    pd_dataframe = aux3
                else:
                    pd_dataframe = pd.concat([pd_dataframe, aux3]).reset_index(drop=True)

    return pd_dataframe

def quantify_peaks(input_data, variable, frame_rate=4, alpha_init=25, alpha_end=120, beta_init=250, beta_end=350):
    """
    This is to calculate the motility peak and the ratio between
    the first part of the video and the second one.
    This code estimates the peak of motility in the control group
    so we can compute the delay between treated conditions

    :param input_data:
    :param data:
    :param variable:
    :param frame_rate:
    :param alpha_init: time in min
    :param alpha_end: time in min
    :param beta_init: time in min
    :param beta_end: time in min
    :return:
    """
    aux = None
    for f in np.unique(input_data["Subcategory-00"]):
        input_data_f = input_data[input_data["Subcategory-00"] == f].reset_index(drop=True)
        for v in np.unique(input_data_f["video_name"]):
            video_data = input_data_f[input_data_f["video_name"] == v].reset_index(drop=True)
            frame_rate = frame_rate
            init_mit = int(alpha_init / frame_rate)  # 30
            final_mit = int(alpha_end / frame_rate)  # 80
            alpha = np.max(video_data.iloc[init_mit:final_mit][variable])
            peak_time = video_data.loc[video_data.iloc[init_mit:final_mit][variable].idxmax(skipna=True), "frame"]
            init_mit = int(beta_init / frame_rate)
            final_mit = int(beta_end / frame_rate)
            beta = np.mean(video_data.iloc[init_mit:][variable])
            columns = ["Subcategory-01", "Subcategory-02"]
            data = [video_data.iloc[0][c] for c in columns]
            if alpha == 0. and beta == 0.:
                ratio = 0.
            elif beta == 0.:
                ratio = np.infty
            else:
                ratio = alpha / beta
            # ratio = (alpha - beta) / (alpha + beta)
            data += [f, v, alpha, beta, ratio, peak_time]
            columns += ["Subcategory-00", "video_name", "alpha", "beta", "ratio", "peak_time"]
            if aux is None:
                aux = pd.DataFrame(np.expand_dims(np.array(data), axis=0), columns=columns)
            else:
                aux = pd.concat([aux,
                                 pd.DataFrame(np.expand_dims(np.array(data), axis=0), columns=columns)]).reset_index(
                    drop=True)
    aux = aux.astype({'ratio': 'float32', 'alpha': 'float32', 'beta': 'float32', 'peak_time': 'float32'})

    aux_1 = None
    for f in np.unique(aux["Subcategory-00"]):
        ## The loop runs by replica
        folder_wise = aux[aux["Subcategory-00"] == f].reset_index(drop=True)
        s_mean = np.mean(folder_wise[folder_wise["Subcategory-02"] == "Synchro"]["peak_time"])
        folder_wise["delay_synchro"] = (folder_wise["peak_time"] - s_mean)
        folder_wise["proportional_delay_synchro"] = (folder_wise["peak_time"] - s_mean) * (100 / s_mean)
        input_data_f = input_data[input_data["Subcategory-00"] == f].reset_index(drop=True)

        # Initialise the value
        folder_wise['Number of resistant cells'] = 0
        for v in np.unique(input_data_f["video_name"]):
            video_data = input_data_f[input_data_f["video_name"] == v].reset_index(drop=True)
            # Get the numnber of cell detection at the peak of synchronisation (it's the ground truth)
            peak_index = video_data.loc[video_data["frame"] <= s_mean]["frame"].idxmax(skipna=True)
            resistant_cells = video_data.loc[peak_index, variable]
            # Get the index to this specific video, to update the info.
            index_v = folder_wise[folder_wise["video_name"] == v].index.to_list()
            folder_wise.loc[index_v, 'Number of resistant cells'] = resistant_cells

        folder_wise_synchro = folder_wise[folder_wise["Subcategory-02"] == "Synchro"]
        r_mean = np.mean(folder_wise_synchro["Number of resistant cells"])
        folder_wise["Resistant cell decrease"] = (r_mean - folder_wise["Number of resistant cells"])
        folder_wise["Proportional resistant decrease"] = (r_mean - folder_wise["Number of resistant cells"]) * (
                    100 / r_mean)

        #### keep developing
        if aux_1 is None:
            aux_1 = folder_wise
        else:
            aux_1 = pd.concat([aux_1, folder_wise]).reset_index(drop=True)
    return aux_1

def compare_peaks(data_mitosis, data_cellsize ):
    ## We calculate the mean size of detected cells in the synchro group in the peak (as we assume it's going to be the
    ## daughter ones)
    data_synchro = data_mitosis[data_mitosis["Subcategory-02"] == "Synchro"]
    ## Obtain the averaged timepoints in which the synchronised field of views for this specific replica got the maximum
    ## number of cells: understood as cell division
    peak_timepoint = np.percentile(data_synchro["peak_time"], 75)
    data_synchro = data_cellsize[data_cellsize["Subcategory-02"] == "Synchro"]
    ## We get the shape of the cells at the estimated cell division time-point. We could also get it at each peak of
    ## each FOV but they should be very similar.
    time_point = np.where(
        abs(data_synchro["frame"] - peak_timepoint) == np.min(abs(data_synchro["frame"] - peak_timepoint)))
    synchro_mean_size = np.mean(data_synchro["average"].iloc[time_point])
    peak_data = []
    for exp in np.unique(data_cellsize["Subcategory-02"]):
        data_exp = data_cellsize[data_cellsize["Subcategory-02"] == exp].reset_index(drop=True)
        data_exp["compared_peak"] = data_exp["average"] - synchro_mean_size
        data_exp = data_exp[data_exp["frame"] > (peak_timepoint / 2)].reset_index(drop=True)
        for f in np.unique(data_exp["Subcategory-00"]):
            data_f = data_exp[data_exp["Subcategory-00"] == f].reset_index(drop=True)
            t = np.min(data_f[data_f["compared_peak"] < 0]["frame"])
            peak_data.append([t, f, exp])
    peak_dataframe = pd.DataFrame(peak_data, columns=['mitosis_t', 'Subcategory-00', 'Subcategory-02'])

    return peak_dataframe