import numpy as np
from tifffile import imread, imsave
import pandas as pd
from utils.normalisation import normalise_phc_timelapse
import os
import sys
SCRIPT_DIR = "/Users/esti/Documents/PROYECTOS/PHX/NanoPyx/src"
sys.path.append(SCRIPT_DIR)
from enanoscopy.methods.image.transform.cross_correlation_map import CrossCorrelationMap




def time_intensity_variability(im):
    diff = im[:-1] - im[1:]
    diff = np.multiply(diff, diff)
    mean_variability = [np.mean(diff[t]) for t in range(diff.shape[0])]
    return mean_variability, diff

def time_crosscorrelation_variability(im):
    xc = CrossCorrelationMap()
    xc_time = [xc.calculate_ccm(im[i], im[i+1], normalize=True) for i in range(im.shape[0]-1)]
    xc_mean = [np.mean(x) for x in xc_time]
    xc_time = np.array(xc_time)
    return xc_mean, xc_time

def extract_dynamics_metrics(path, dynamics_info=None, column_data=[], frame_rate=4, method="intensity", save_steps=False, output_path=''):
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
                                                         method=method, save_steps=save_steps, output_path=os.path.join(output_path, f))
            elif f.__contains__('.tif'):
                print(f)
                im = imread(os.path.join(path, f))
                new_im = normalise_phc_timelapse(im)
                if method == "cross-correlation":
                    dynamics_val, diff = time_crosscorrelation_variability(new_im)
                elif method == "intensity":
                    dynamics_val, diff = time_intensity_variability(new_im)
                if save_steps:
                    os.makedirs(os.path.join(output_path, f), exist_ok=True)
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
    return dynamics_info
