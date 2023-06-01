"""
Created on 2022
Henriques Lab

This script is meant to run automatically. Results are stored as csv files with the corresponding conditions, dates and
video names so all the results can be fully tracked.
"""
import os
from photofitt.analysis import count_mitosis_all
from photofitt.display import display_data_from_masks, plot_conditions
import sys

## PARAMETERS USED TO COMPUTE PLOTS
#--------------------------------------------------------------
masks_path = sys.argv[1]
output_path = sys.argv[2]
frame_rate = sys.argv[3] # The time gap we will use to compute all the metrics
r = 0.0 # We can filter out by roundness of the segmented cells
t_win = 5 # The size of the window (kernel) that is used to smooth the curves
max_t = 300 # The maximum length in minutes of the videos that we will analyse

# GET THE DATA AND FILTER IT WITH THE PARAMETERS
#--------------------------------------------------------------
data = count_mitosis_all(masks_path, frame_rate = frame_rate)
# save the information
data.to_csv(os.path.join(output_path, "mitosis_counting.csv"))

## Read the original data
# data = pd.read_csv(os.path.join(output_path, "data.csv"))
hue_order = ['Control-sync', 'Synchro', 'UV25ms', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms',
             'UV01sec', 'UV05sec', 'UV10sec', 'UV15sec', 'UV20sec', 'UV25sec']
graph_format = 'png'

# PLOT THE RESULTS FOR EACH CONDITION SEPARATELY
#--------------------------------------------------------------
display_data_from_masks(data, output_path, frame_rate=frame_rate,
                        graph_format=graph_format, hue_order=hue_order)
