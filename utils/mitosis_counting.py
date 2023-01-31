import os
from tifffile import imread
import numpy as np
import pandas as pd
from utils.morphology import roundnessCalculator



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
                       columns=['frame', 'mitosis', 'cell_size', "roundness_axis", "roundness_projected"] + columns)
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


def count_mitosis_all(path, stacks=False, pd_dataframe=None, column_data=[], frame_rate=10, min_roundness=0.85, t_win=5):
    """
    This function parses all the folders contained in the path and will output a pandas data frame with each category
    and subcategory labelled, the fram, time and number of mitosis detected in the image.
    :param min_roundness:
    :param stacks:
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
                M = np.max(aux['mitosis'])
                aux['mitosis_normalised'] = aux['mitosis'] / M
                aux["processing"] = "Raw"
                y = smooth(aux['mitosis'], t_win)
                y_norm = smooth(aux['mitosis_normalised'], t_win)
                aux2 = aux.copy()
                aux2['processing'] = 'Averaged-kernel{}'.format(t_win)
                aux2['mitosis'] = y
                aux2['mitosis_normalised'] = y_norm
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
    for v in np.unique(input_data["video_name"]):
        video_data = input_data[input_data["video_name"] == v].reset_index(drop=True)
        frame_rate = frame_rate
        init_mit = int(alpha_init / frame_rate)  # 30
        final_mit = int(alpha_end / frame_rate)  # 80
        alpha = np.max(video_data.iloc[init_mit:final_mit][variable])
        peak_time = video_data.loc[video_data.iloc[init_mit:final_mit][variable].idxmax(skipna=True), "frame"]
        init_mit = int(beta_init / frame_rate)
        final_mit = int(beta_end / frame_rate)
        beta = np.mean(video_data.iloc[init_mit:][variable])
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