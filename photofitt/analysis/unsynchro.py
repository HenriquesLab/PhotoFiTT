
import numpy as np
from tifffile import imread
import pandas as pd
import cv2
import os

def extract_tracking_from_file(path2file, frame_rate=4):
    """

    :param path2file: path to a video with labels for the cells in mitosis.
            It expects the same label (a dot in the middle of the cell for the same cell across time and if it divides,
            two dots (separated) with the same label. In this way we identify divisions.
    :param frame_rate: in minutes, set to 4 by default
    :return:
    """
    V = imread(path2file)
    V = np.squeeze(V)
    # Make sure that frames are in the first dimension
    if V.shape[0] != np.min(V.shape):
        V = np.transpose(V, axis=[-1, 0, 1])
    tracks = np.unique(V)
    # Ensure the track list is not empty
    data = None
    if len(tracks) > 1:
        # Remove the label=0 (background) from the list
        tracks = tracks[1:]  #
        for t in tracks:
            index_t = np.where(V == t)[0]
            t0 = np.min(index_t)
            tend = np.max(index_t)
            # Inspect for divisions
            analysis = cv2.connectedComponentsWithStats(np.int8(V[tend] == t))
            if analysis[0] > 2:
                # there are two points representing the division
                # (labels = background and connected components)
                division = True
                division_t = tend
                tend -= 1
            else:
                division = False
                division_t = -1

            mitosis_time = tend - t0
            aux = pd.DataFrame(data=[[t,
                                      t0 * frame_rate,
                                      tend * frame_rate,
                                      division,
                                      division_t * frame_rate,
                                      mitosis_time * frame_rate]],
                               columns=["ID",
                                        "Initial t",
                                        "Final t",
                                        "Division",
                                        "Division timepoint",
                                        "Mitosis duration"])
            # update dataframe
            if data is None:
                data = aux
            else:
                data = pd.concat([data, aux]).reset_index(drop=True)
    return data

def read_tracking(input_dir, data=None, column_data=[], frame_rate = 4):
    """

    :param input_dir: The directory with subfolders containing the videos with the tracking labels
    :param data: None unless you want to concatenate to an existing one
    :param column_data: [] unless you want to concatenate additional columns to the data
    :param frame_rate: in minutes, set to 4 by default
    :return:
    """
    folders = [f for f in os.listdir(input_dir) if not f.startswith(".")]
    #folders = [f for f in folders if f!="labeling"]
    for f in folders:
        print(f)
        if f.endswith(".tif"):
            tracking_data = extract_tracking_from_file(os.path.join(input_dir,f), frame_rate = frame_rate)
            for i in range(len(column_data)):
                tracking_data["Subcategory-{:02d}".format(i)] = column_data[i]
            tracking_data["video_name"] = f.split('.tif')[0]
            if data is None:
                data = tracking_data
            else:
                data = pd.concat([data, tracking_data]).reset_index(drop=True)

        else:
            data = read_tracking(os.path.join(input_dir,f), data=data, column_data=column_data + [f])
    return data