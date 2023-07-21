import os
from stardist.models import StarDist2D 
from stardist import random_label_cmap
from tifffile import imread, imsave
from csbdeep.utils import normalize
import cv2
from skimage import img_as_float32, img_as_ubyte
import pandas as pd
import numpy as np

def segment_stack(path, model):
    timelapse = imread(path)
    # normalize channels independently
    axis_norm = (0,1) 
    timelapse = normalize(timelapse, 1,99.8, axis=(0,)+tuple(1+np.array(axis_norm)))
    n_timepoint = timelapse.shape[0]
    prediction_stack = []

    for t in range(n_timepoint):
        labels, polygons = model.predict_instances(timelapse[t])      
        prediction_stack.append(labels)
    prediction_stack = np.array(prediction_stack)
    
    return(prediction_stack)

                
                
def process_folder(input_path, output_path, model):
    folders = os.listdir(input_path)
    os.makedirs(output_path, exist_ok=True)
    for f in folders:
        print(os.path.join(input_path, f))
        if f[0] != '.':
            if not f.__contains__('.'):
                os.makedirs(os.path.join(output_path, f), exist_ok=True)
                process_folder(os.path.join(input_path, f), os.path.join(output_path, f), model)
            elif f.__contains__('.tif'):
                mask = segment_stack(os.path.join(input_path, f), model)
                imsave(os.path.join(output_path, f), mask.astype(np.uint16))


input_path = "/media/ocb/EGM/PHX/DATA/DOWNSAMPLE/CHO-UNSYNCH/"
output_path = "/media/ocb/EGM/PHX/DATA/MASKS/CHO-UNSYNCH/"

Prediction_model_folder = "/home/ocb/Documents/EGM/PHX/STARDIST-MODELS/STARDIST-BRIGHTFIELD-27082022" #@param {type:"string"}
#Here we find the loaded model name and parent path
Prediction_model_name = os.path.basename(Prediction_model_folder)
Prediction_model_path = os.path.dirname(Prediction_model_folder)

model = StarDist2D(None, name = Prediction_model_name, basedir = Prediction_model_path)

process_folder(input_path, output_path, model)
print("PROCESS FINISHED SUCCESSFULLY")

