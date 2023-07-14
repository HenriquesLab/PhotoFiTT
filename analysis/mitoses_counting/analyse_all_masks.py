"""
Created on 2022
Henriques Lab

This script is meant to run automatically. Results are stored as csv files with the corresponding conditions, dates and
video names so all the results can be fully tracked.
"""
import os
import photofitt
from photofitt.analysis import count_mitosis_all
from photofitt.display import display_data_from_masks, conditions
import sys
import seaborn as sns
import numpy as np

## PARAMETERS USED TO COMPUTE PLOTS
#--------------------------------------------------------------
#masks_path = sys.argv[1]
output_path = "/Users/esti/Documents/PROYECTOS/PHX/DOCS/MANUSCRIPT/CODE/exploratory_plots" # sys.argv[2]
frame_rate = 4 #sys.argv[3] # The time gap we will use to compute all the metrics
r = 0.0 # We can filter out by roundness of the segmented cells
t_win = 5 # The size of the window (kernel) that is used to smooth the curves
max_t = 300 # The maximum length in minutes of the videos that we will analyse

# GET THE DATA AND FILTER IT WITH THE PARAMETERS
#--------------------------------------------------------------
#data = count_mitosis_all(masks_path, frame_rate = frame_rate)
# save the information
#data.to_csv(os.path.join(output_path, "mitosis_counting.csv"))

## Read the original data
# data = pd.read_csv(os.path.join(output_path, "data.csv"))
import pandas as pd
# data = pd.read_csv("/Users/esti/Documents/PROYECTOS/PHX/DOCS/MANUSCRIPT/CODE/data/mitosis_CHO_UV_clean.csv")
#data = pd.read_csv("/Users/esti/Documents/PROYECTOS/PHX/DOCS/MANUSCRIPT/CODE/data/mitosis_CHO_475_clean_new.csv")
data = pd.read_csv("/Users/esti/Documents/PROYECTOS/PHX/DOCS/MANUSCRIPT/CODE/data/mitosis_CHO_568_clean.csv")
# data = pd.read_csv("/Users/esti/Documents/PROYECTOS/PHX/DOCS/MANUSCRIPT/CODE/data/mitosis_CHO_630_clean_new.csv")


# hue_order = ['Control-sync', 'Synchro', '25ms', '50ms', '100ms', '200ms', '400ms', '800ms', '01sec', '05sec', '10sec',
#              '15sec', '20sec', '25sec', '30sec']

## Estimate the ligth dose
light_power = 6.255662
data = photofitt.utils.numerical_dose(data, column_name="Subcategory-02", power=light_power)

## Generate categorical variables for the light dose
light_dose = np.unique(data["Light dose"])
data["Light dose cat"] = ''
for l in light_dose:
    if l > 0:
        cat = np.str(np.round(l, decimals=1)) + " J/cm2"
    else:
        cat = 'non-synchro-0 J/cm2'
    data["Light dose cat"][data["Light dose"] == l] = cat

data["Light dose cat"][data["Subcategory-02"] == "Synchro"] = '0 J/cm2'
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