"""
Created on 2022
Henriques Lab

This script is meant to run automatically. Results are stored as csv files with the corresponding conditions, dates and
video names so all the results can be fully tracked.
"""
import os
from photofitt.analysis import count_mitosis_all
from photofitt.display import display_data_from_masks
from photofitt.utils import numerical_dose, power_conversion
import sys
import seaborn as sns
import numpy as np

## PARAMETERS USED TO COMPUTE PLOTS
#--------------------------------------------------------------
masks_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/HELA/masks/scaled_1.5709_results/stardist_prob03" #sys.argv[1]
output_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/HELA/results/scaled_1.5709_results/stardist_prob03/new_analysis" # sys.argv[2]
frame_rate = 4 # sys.argv[3] # The time gap we will use to compute all the metrics
r = 0.0 # We can filter out by roundness of the segmented cells
t_win = 5 # The size of the window (kernel) that is used to smooth the curves
max_t = 300 # The maximum length in minutes of the videos that we will analyse

os.makedirs(output_path, exist_ok=True)

# GET THE DATA AND FILTER IT WITH THE PARAMETERS
#--------------------------------------------------------------
data = count_mitosis_all(masks_path, frame_rate = frame_rate)
# Save the information
data.to_csv(os.path.join(output_path, "mitosis_counting.csv"))

## Read the original data
import pandas as pd
data = pd.read_csv(os.path.join(output_path, "mitosis_counting.csv"))

## Estimate the ligth dose
light_power = 6.255662
data = numerical_dose(data, column_name="Subcategory-02", power=light_power)
data = power_conversion(data)
hue_order = ['non-synchro-0 J/cm2', '0 J/cm2', '0.2 J/cm2',
             '0.3 J/cm2', '0.6 J/cm2', '1.3 J/cm2', '2.5 J/cm2',
             '5.0 J/cm2', '6.3 J/cm2', '31.3 J/cm2',
             '62.6 J/cm2', '93.8 J/cm2', '125.1 J/cm2', '156.4 J/cm2']
graph_format = 'png'
hue = "Light dose cat"
print(data.columns)

# PLOT THE RESULTS FOR EACH CONDITION SEPARATELY
#--------------------------------------------------------------
y_var = 'Number of cells'
display_data_from_masks(data,  y_var, output_path, frame_rate=frame_rate,
                        graph_format=graph_format, hue=hue, hue_order=hue_order,
                        palette=sns.color_palette("CMRmap_r", 17))