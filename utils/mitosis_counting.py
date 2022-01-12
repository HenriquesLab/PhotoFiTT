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
