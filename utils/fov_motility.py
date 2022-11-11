import numpy as np
from tifffile import imread, imsave
import pandas as pd
from utils.normalisation import normalise_phc_timelapse
import os

def time_intensity_variability(im):
    diff = im[:-1] - im[1:]
    diff = np.multiply(diff, diff)
    mean_variability = [np.mean(diff[t]) for t in range(diff.shape[0])]
    return mean_variability, diff

def extract_dynamics_metrics(path, dynamics_info=None, column_data=[], frame_rate=4, save_steps=False, output_path=''):
    folders = os.listdir(path)
    folders.sort
    print(folders)
    for f in folders:
        if f[0] != '.':
            if not f.__contains__('.'):

                if save_steps:
                    os.makedirs("path/to/directory", exist_ok=True)
                dynamics_info = extract_dynamics_metrics(os.path.join(path, f), dynamics_info=dynamics_info,
                                                         column_data=column_data + [f], frame_rate=frame_rate,
                                                         save_steps=save_steps, output_path=os.path.join(output_path, f))
            elif f.__contains__('.tif'):
                print(f)
                im = imread(os.path.join(path, f))
                new_im = normalise_phc_timelapse(im)
                im_control_val, diff = time_intensity_variability(new_im)
                if save_steps:
                    os.makedirs(os.path.join(output_path, f), exist_ok=True)
                    imsave(os.path.join(output_path, "normalised_" + f), new_im)
                    imsave(os.path.join(output_path, "diff_" + f), diff)

                data = np.zeros((len(diff), 2))
                data[:, 0] = frame_rate * np.arange(len(diff))
                data[:, 1] = diff
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
    return dynamics_info
