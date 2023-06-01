"""
Created on 2021
Henriques Lab

This script is meant to run automatically.
"""

from photofitt.display import build_mosaics
import os
import sys

## PARAMETERS USED TO COMPUTE PLOTS
#--------------------------------------------------------------
path_masks = sys.argv[1]
path_raw = sys.argv[2]
output_path = sys.argv[3] # The time gap we will use to compute all the metrics

if not os.path.exists(os.path.join(output_path, "mosaics")):
    os.mkdir(os.path.join(output_path, "mosaics"))

roundness = [0.0, 0.5, 0.85, 0.9, 0.95, 0.97]

for r in roundness:
    output_path_folder = os.path.join(output_path, "mosaics", "mosaics_roundness_{}".format(r))
    build_mosaics(path_masks, path_raw, output_path_folder, min_roundness=r)
