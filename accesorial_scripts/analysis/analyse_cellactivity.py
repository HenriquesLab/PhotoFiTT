"""
Created on 2024
Henriques Lab

"""

import os
import photofitt
from photofitt.analysis import extract_activity

images_path = "/home/ocb/HardDrive_4TB/EGM/PHX/DATA/DOWNSAMPLE/CHO-UNSYNCH"
frame_rate = 4 # The time gap we will use to compute all the metrics
output_path =  "/home/ocb/HardDrive_4TB/EGM/PHX/ANALYSIS/UNSYNCHRO/NEW-ACTIVITY"
## Parameters for activity method estimation
method="intensity"
folder = "activity_clahe-normalised-all-{}".format(method)

os.makedirs(os.path.join(output_path, folder),exist_ok=True)
os.makedirs(os.path.join(output_path, "plots"), exist_ok=True)

activity_metrics = extract_activity(images_path, method=method, save_steps=False, enhance_contrast=True,
                                            output_path=os.path.join(output_path, folder), condition=None)
## Save the results
activity_metrics.to_csv(os.path.join(output_path, folder, f"data_activity_{method}.csv"))
